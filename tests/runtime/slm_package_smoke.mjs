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

function runNpm(args, options = {}) {
  if (process.platform === "win32") {
    const npmCli = path.join(path.dirname(process.execPath), "node_modules", "npm", "bin", "npm-cli.js");
    return run(process.execPath, [npmCli, ...args], options);
  }
  return run("npm", args, options);
}

const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), "slm-package-smoke-"));
try {
  const pack = runNpm(["pack", "--json", "--pack-destination", tempRoot], {
    env: { npm_config_cache: path.join(tempRoot, "npm-cache") },
  });
  const tarballName = JSON.parse(pack.stdout)[0].filename;
  const tarball = path.join(tempRoot, tarballName);
  const installRoot = path.join(tempRoot, "install");
  runNpm(["install", "--prefix", installRoot, "--ignore-scripts", "--no-audit", "--no-fund", tarball], {
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
  const specRoot = path.join(queryRepo, "docs", "specs", "001-example");
  fs.mkdirSync(specRoot, { recursive: true });
  fs.writeFileSync(
    path.join(specRoot, "requirements.md"),
    "---\nstatus: draft\n---\n# Requirements\n\n### Requirement 1: Example\n\n**Priority:** must-have\n",
  );
  fs.writeFileSync(
    path.join(specRoot, "tasks.md"),
    "# Tasks\n\n## Phase 1: Foundation\n\n- [x] T001 Complete setup.\n  - Evidence: passed\n\n## Phase 2: Delivery\n\n- [~] T002 Deliver behavior.\n  - Depends on: T001\n  - Evidence: in progress\n",
  );

  const help = run(process.execPath, [dispatcher, "--help"]);
  for (const command of ["spec", "specs", "tasks", "next", "requirements", "history", "install"]) {
    if (!help.stdout.includes(command)) throw new Error(`slm --help omitted ${command}`);
  }

  const specs = run(process.execPath, [dispatcher, "specs", "--json", "-C", queryRepo]);
  const payload = JSON.parse(specs.stdout);
  if (payload.command !== "specs" || payload.repo_root !== "." || payload.records.length !== 1) {
    throw new Error(`unexpected slm specs payload: ${specs.stdout}`);
  }
  const record = payload.records[0];
  if (
    record.phases_complete !== 1 ||
    record.phases_total !== 2 ||
    record.current_phase !== "Phase 2: Delivery" ||
    record.phase_state !== "in_progress"
  ) {
    throw new Error(`unexpected slm phase progress: ${specs.stdout}`);
  }

  const singular = run(process.execPath, [dispatcher, "spec", "--json", "-C", queryRepo]);
  if (singular.stdout !== specs.stdout) {
    throw new Error("slm spec did not match slm specs for active inventory");
  }

  const installHelp = run(process.execPath, [dispatcher, "install", "--help"]);
  if (!installHelp.stdout.includes("Usage: slm install")) {
    throw new Error("slm install --help did not use the installer contract");
  }
  process.stdout.write("slm packaged smoke passed\n");
} finally {
  fs.rmSync(tempRoot, { recursive: true, force: true });
}
