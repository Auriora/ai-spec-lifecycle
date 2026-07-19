#!/usr/bin/env node
"use strict";

// Spec 028 cross-platform smoke: install the package shell-free, launch the
// installed MCP server and complete an `initialize` handshake, then fire the
// PostToolUse hook with a Claude-shaped payload. Exits non-zero on any failure.
// Run on windows-latest / macos-latest / ubuntu-latest in CI; runnable locally.

import { spawn } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { install } from "../../packaging/spec-lifecycle-manager/installer.mjs";

const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..");

function ok(msg) { process.stdout.write(`  ok  ${msg}\n`); }
function fail(msg) { throw new Error(msg); }

async function mcpInitialize(command, args, cwd, env = process.env) {
  return new Promise((resolve, reject) => {
    const child = spawn(command, args, { cwd, env, stdio: ["pipe", "pipe", "pipe"] });
    let out = "";
    let stderr = "";
    const timer = setTimeout(() => {
      child.kill();
      reject(new Error(`MCP server timed out without responding. stderr:\n${stderr}`));
    }, 20000);
    child.stdout.on("data", (chunk) => {
      out += chunk;
      const line = out.split(/\r?\n/).find((l) => l.trim());
      if (line) {
        clearTimeout(timer);
        child.kill();
        try {
          resolve(JSON.parse(line));
        } catch (err) {
          reject(new Error(`Non-JSON MCP response: ${line} (${err.message})`));
        }
      }
    });
    child.stderr.on("data", (chunk) => { stderr += chunk; });
    child.on("error", (err) => { clearTimeout(timer); reject(err); });
    child.stdin.write(`${JSON.stringify({ jsonrpc: "2.0", id: 1, method: "initialize", params: {} })}\n`);
    child.stdin.end();
  });
}

function fireHook(command, args, payload, cwd) {
  return new Promise((resolve, reject) => {
    const child = spawn(command, args, { cwd, stdio: ["pipe", "pipe", "pipe"] });
    let out = "";
    let stderr = "";
    const timer = setTimeout(() => { child.kill(); reject(new Error("hook timed out")); }, 20000);
    child.stdout.on("data", (c) => { out += c; });
    child.stderr.on("data", (c) => { stderr += c; });
    child.on("error", (err) => { clearTimeout(timer); reject(err); });
    child.on("close", (code) => { clearTimeout(timer); resolve({ code, out, stderr }); });
    child.stdin.write(JSON.stringify(payload));
    child.stdin.end();
  });
}

function fireShellHook(command, payload, cwd) {
  return new Promise((resolve, reject) => {
    const child = spawn(command, { cwd, shell: true, stdio: ["pipe", "pipe", "pipe"] });
    let out = "";
    let stderr = "";
    const timer = setTimeout(() => { child.kill(); reject(new Error("hook timed out")); }, 20000);
    child.stdout.on("data", (c) => { out += c; });
    child.stderr.on("data", (c) => { stderr += c; });
    child.on("error", (err) => { clearTimeout(timer); reject(err); });
    child.on("close", (code) => { clearTimeout(timer); resolve({ code, out, stderr }); });
    child.stdin.write(JSON.stringify(payload));
    child.stdin.end();
  });
}

async function main() {
  const base = fs.mkdtempSync(path.join(os.tmpdir(), "slm-smoke-"));
  const home = path.join(base, "home");
  const mkt = path.join(base, "mkt");
  process.stdout.write(`platform=${process.platform} node=${process.version}\n`);

  try {
    // 1) Shell-free install (skip codex registration; CI runners have no codex).
    const previousPython = process.env.SPEC_LIFECYCLE_PYTHON;
    process.env.SPEC_LIFECYCLE_PYTHON = previousPython || "python3";
    const code = await install([
      "--source", repoRoot,
      "--codex-home", home,
      "--marketplace-root", mkt,
      "--skip-plugin-add",
    ]);
    if (previousPython === undefined) delete process.env.SPEC_LIFECYCLE_PYTHON;
    else process.env.SPEC_LIFECYCLE_PYTHON = previousPython;
    if (code !== 0) fail(`install exited ${code}`);
    ok("install completed shell-free");

    const pluginRoot = path.join(home, "plugins", "spec-lifecycle-manager");

    // 2) MCP launch + initialize handshake using the installed (pinned) config.
    const mcp = JSON.parse(fs.readFileSync(path.join(pluginRoot, ".mcp.json"), "utf8"));
    const server = mcp.mcpServers["spec-lifecycle-manager"];
    if (server.cwd) fail(`installed MCP config must not set cwd: ${JSON.stringify(server)}`);
    const resp = await mcpInitialize(server.command, server.args, repoRoot, { ...process.env, ...(server.env || {}) });
    if (!resp.result || !resp.result.protocolVersion) fail(`initialize missing protocolVersion: ${JSON.stringify(resp)}`);
    if (resp.result.serverInfo?.name !== "spec-lifecycle-manager") fail(`unexpected serverInfo: ${JSON.stringify(resp.result.serverInfo)}`);
    ok(`MCP initialize handshake (protocolVersion=${resp.result.protocolVersion}, interpreter=${server.command})`);

    // 3) Hook fire with a Claude-shaped payload (tool_name "Write" + file_path)
    // for BOTH installed hook copies. The Codex copy is shell-form
    // ("<interp> [args] \"<script>\""); the Claude copy is exec form
    // (command + args array). The exec-form path is the spec's headline fix --
    // shell-form falls back to PowerShell on Windows -- so it must be *executed*
    // on Windows, not just shape-asserted. Each is resolved into an argv the way
    // a shell-free runtime would and run from the repo so the advisory has a
    // spec to evaluate.
    // A Claude-shaped Write payload; the file_path is a stable repo doc so the
    // hook has a real path to evaluate. The smoke asserts the hook spawns and
    // exits 0 cross-platform (shell-free), not a specific advisory verdict.
    const payload = { tool_name: "Write", tool_input: { file_path: path.join(repoRoot, "docs/history/spec-closure-log.md") } };
    const hookConfigs = [
      { label: "Codex shell-form", file: path.join(pluginRoot, "hooks", "hooks.json"), tokenRoot: pluginRoot, expectExec: false },
      { label: "Claude exec-form", file: path.join(pluginRoot, "claude-plugin", "hooks", "hooks.json"), tokenRoot: path.join(pluginRoot, "claude-plugin"), expectExec: true },
    ];
    for (const cfg of hookConfigs) {
      const hooks = JSON.parse(fs.readFileSync(cfg.file, "utf8"));
      const hookCmd = hooks.hooks.PostToolUse[0].hooks[0];
      const isExec = Array.isArray(hookCmd.args);
      if (cfg.expectExec && !isExec) fail(`${cfg.label} hook is not exec form (regressed to shell-form): ${JSON.stringify(hookCmd)}`);
      const subst = (s) => s.replace("${PLUGIN_ROOT}", cfg.tokenRoot).replace("${CLAUDE_PLUGIN_ROOT}", cfg.tokenRoot);
      let result;
      if (isExec) {
        result = await fireHook(hookCmd.command, hookCmd.args.map(subst), payload, repoRoot);
      } else {
        result = await fireShellHook(subst(hookCmd.command), payload, repoRoot);
      }
      if (result.code !== 0) fail(`${cfg.label} hook exited ${result.code}. stderr:\n${result.stderr}`);
      ok(`${cfg.label} hook executed (exit 0, ${result.out.trim() ? "advisory output emitted" : "no advisory output"})`);

      const missingRoot = path.join(base, "removed-cache-version", cfg.label.replace(/\s+/g, "-"));
      const missingSubst = (s) => s.replace("${PLUGIN_ROOT}", missingRoot).replace("${CLAUDE_PLUGIN_ROOT}", missingRoot);
      const missingResult = isExec
        ? await fireHook(hookCmd.command, hookCmd.args.map(missingSubst), payload, repoRoot)
        : await fireShellHook(missingSubst(hookCmd.command), payload, repoRoot);
      if (missingResult.code !== 0 || missingResult.out || missingResult.stderr) {
        fail(`${cfg.label} missing-cache hook was not quiet: ${JSON.stringify(missingResult)}`);
      }
      ok(`${cfg.label} missing-cache hook exited quietly`);
    }

    process.stdout.write("SMOKE PASS\n");
  } finally {
    fs.rmSync(base, { recursive: true, force: true });
  }
}

main().catch((err) => {
  process.stderr.write(`SMOKE FAIL: ${err.message}\n`);
  process.exit(1);
});
