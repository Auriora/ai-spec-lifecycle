#!/usr/bin/env node
// Copyright 2026 Auriora
//
// SPDX-License-Identifier: GPL-3.0-or-later

// Portable MCP launch shim. The plugin root is used only to locate the bundled
// Python runtime; the repository root defaults to the MCP launch cwd.

import { spawn } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

export function planLaunch(env = process.env, argv = process.argv.slice(2), cwd = process.cwd()) {
  const pluginRoot = path.dirname(fileURLToPath(import.meta.url));
  const server = path.join(pluginRoot, "skills", "spec-lifecycle-manager", "scripts", "spec_mcp_server.py");
  const childEnv = { ...env };
  if (!childEnv.SPEC_LIFECYCLE_DEFAULT_REPO_ROOT && !hasRepoRootArg(argv)) {
    childEnv.SPEC_LIFECYCLE_DEFAULT_REPO_ROOT = cwd;
  }
  const [command, ...pythonArgs] = splitCommand(childEnv.SPEC_LIFECYCLE_PYTHON || "python3");
  return {
    command,
    args: [...pythonArgs, server, ...argv],
    options: { stdio: "inherit", env: childEnv },
  };
}

function splitCommand(value) {
  return String(value).trim().split(/\s+/).filter(Boolean);
}

function hasRepoRootArg(argv) {
  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === "--repo-root" && argv[index + 1]) {
      return true;
    }
    if (arg.startsWith("--repo-root=") && arg.slice("--repo-root=".length)) {
      return true;
    }
  }
  return false;
}

function main() {
  const plan = planLaunch();
  if (process.platform !== "win32" && typeof process.execve === "function") {
    const command = resolveExecutable(plan.command, plan.options.env) || plan.command;
    process.execve(command, [command, ...plan.args], plan.options.env);
  }

  const child = spawn(plan.command, plan.args, plan.options);

  for (const signal of ["SIGINT", "SIGTERM", "SIGHUP"]) {
    process.on(signal, () => child.kill(signal));
  }

  child.on("error", (error) => {
    process.stderr.write(`spec-lifecycle-manager: failed to launch MCP server: ${error.message}\n`);
    process.exit(1);
  });
  child.on("exit", (code, signal) => {
    process.exit(code ?? (signal ? 1 : 0));
  });
}

function resolveExecutable(command, env) {
  if (path.isAbsolute(command) || command.includes(path.sep)) {
    return command;
  }
  for (const dir of String(env.PATH || "").split(path.delimiter).filter(Boolean)) {
    const candidate = path.join(dir, command);
    try {
      if (fs.statSync(candidate).isFile()) {
        return candidate;
      }
    } catch {
      // Keep searching.
    }
  }
  return null;
}

const isMain = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (isMain) {
  main();
}
