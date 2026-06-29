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

async function mcpInitialize(command, args, cwd) {
  return new Promise((resolve, reject) => {
    const child = spawn(command, args, { cwd, stdio: ["pipe", "pipe", "pipe"] });
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

async function main() {
  const base = fs.mkdtempSync(path.join(os.tmpdir(), "slm-smoke-"));
  const home = path.join(base, "home");
  const mkt = path.join(base, "mkt");
  process.stdout.write(`platform=${process.platform} node=${process.version}\n`);

  try {
    // 1) Shell-free install (skip codex registration; CI runners have no codex).
    const code = await install([
      "--source", repoRoot,
      "--codex-home", home,
      "--marketplace-root", mkt,
      "--skip-plugin-add",
    ]);
    if (code !== 0) fail(`install exited ${code}`);
    ok("install completed shell-free");

    const pluginRoot = path.join(home, "plugins", "spec-lifecycle-manager");

    // 2) MCP launch + initialize handshake using the installed (pinned) config.
    const mcp = JSON.parse(fs.readFileSync(path.join(pluginRoot, ".mcp.json"), "utf8"));
    const server = mcp.mcpServers["spec-lifecycle-manager"];
    const serverCwd = server.cwd === "." || !server.cwd ? pluginRoot : path.resolve(pluginRoot, server.cwd);
    const resp = await mcpInitialize(server.command, server.args, serverCwd);
    if (!resp.result || !resp.result.protocolVersion) fail(`initialize missing protocolVersion: ${JSON.stringify(resp)}`);
    if (resp.result.serverInfo?.name !== "spec-lifecycle-manager") fail(`unexpected serverInfo: ${JSON.stringify(resp.result.serverInfo)}`);
    ok(`MCP initialize handshake (protocolVersion=${resp.result.protocolVersion}, interpreter=${server.command})`);

    // 3) Hook fire with a Claude-shaped payload (tool_name "Write" + file_path).
    // Codex hook is shell-form ("<interp> [args] \"<script>\""); parse it into
    // an argv the same way a shell-free runtime would, then run from the repo so
    // the advisory has a spec to evaluate.
    const hooks = JSON.parse(fs.readFileSync(path.join(pluginRoot, "hooks", "hooks.json"), "utf8"));
    const hookCmd = hooks.hooks.PostToolUse[0].hooks[0];
    let command;
    let args;
    if (Array.isArray(hookCmd.args)) {
      command = hookCmd.command;
      args = hookCmd.args.map((a) => a.replace("${PLUGIN_ROOT}", pluginRoot).replace("${CLAUDE_PLUGIN_ROOT}", pluginRoot));
    } else {
      const m = hookCmd.command.match(/^(.*?)\s+"([^"]+)"\s*$/);
      if (!m) fail(`cannot parse shell-form hook command: ${hookCmd.command}`);
      const interp = m[1].split(/\s+/);
      command = interp[0];
      args = [...interp.slice(1), m[2].replace("${PLUGIN_ROOT}", pluginRoot)];
    }
    const payload = { tool_name: "Write", tool_input: { file_path: path.join(repoRoot, "docs/specs/028-cross-platform-packaging/tasks.md") } };
    const result = await fireHook(command, args, payload, repoRoot);
    if (result.code !== 0) fail(`hook exited ${result.code}. stderr:\n${result.stderr}`);
    ok(`hook executed (exit 0, ${result.out.trim() ? "advisory output emitted" : "no advisory output"})`);

    process.stdout.write("SMOKE PASS\n");
  } finally {
    fs.rmSync(base, { recursive: true, force: true });
  }
}

main().catch((err) => {
  process.stderr.write(`SMOKE FAIL: ${err.message}\n`);
  process.exit(1);
});
