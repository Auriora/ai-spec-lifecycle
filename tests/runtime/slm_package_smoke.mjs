#!/usr/bin/env node
"use strict";

import { spawnSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..");

function run(command, args, options = {}) {
  const result = spawnSync(command, args, {
    cwd: options.cwd || repoRoot,
    encoding: "utf8",
    windowsHide: true,
    env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1", ...(options.env || {}) },
  });
  if (result.error || result.status !== 0) {
    throw new Error(
      `${command} ${args.join(" ")} failed (${result.status}):\n${result.stderr || result.error || ""}`,
    );
  }
  return result;
}

const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), "slm-package-smoke-"));
try {
  const pack = run("npm", ["pack", "--json", "--pack-destination", tempRoot], {
    env: { npm_config_cache: path.join(tempRoot, "npm-cache") },
  });
  const tarballName = JSON.parse(pack.stdout)[0].filename;
  const tarball = path.join(tempRoot, tarballName);
  const installRoot = path.join(tempRoot, "install");
  run("npm", ["install", "--prefix", installRoot, "--ignore-scripts", "--no-audit", "--no-fund", tarball], {
    env: { npm_config_cache: path.join(tempRoot, "npm-cache") },
  });

  const packageRoot = path.join(installRoot, "node_modules", "@auriora", "ai-spec-lifecycle");
  const dispatcher = path.join(packageRoot, "packaging", "spec-lifecycle-manager", "slm-cli.js");
  const binRoot = path.join(installRoot, "node_modules", ".bin");
  const slmShim = path.join(binRoot, process.platform === "win32" ? "slm.cmd" : "slm");
  if (!fs.existsSync(slmShim)) throw new Error("npm install did not create the slm bin shim");
  for (const legacy of ["spec-lifecycle-manager", "ai-spec-lifecycle"]) {
    const legacyShim = path.join(binRoot, process.platform === "win32" ? `${legacy}.cmd` : legacy);
    if (fs.existsSync(legacyShim)) throw new Error(`legacy bin shim still exists: ${legacy}`);
  }
  const queryRepo = path.join(tempRoot, "query-repo");
  fs.mkdirSync(path.join(queryRepo, ".git"), { recursive: true });

  const help = run(process.execPath, [dispatcher, "--help"]);
  for (const command of ["specs", "tasks", "next", "requirements", "history", "install"]) {
    if (!help.stdout.includes(command)) throw new Error(`slm --help omitted ${command}`);
  }

  const specs = run(process.execPath, [dispatcher, "specs", "--json", "-C", queryRepo]);
  const payload = JSON.parse(specs.stdout);
  if (payload.command !== "specs" || payload.repo_root !== "." || payload.records.length !== 0) {
    throw new Error(`unexpected slm specs payload: ${specs.stdout}`);
  }

  const installHelp = run(process.execPath, [dispatcher, "install", "--help"]);
  if (!installHelp.stdout.includes("Usage: slm install")) {
    throw new Error("slm install --help did not use the installer contract");
  }
  process.stdout.write("slm packaged smoke passed\n");
} finally {
  fs.rmSync(tempRoot, { recursive: true, force: true });
}
