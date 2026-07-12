// Copyright 2026 Auriora
// SPDX-License-Identifier: GPL-3.0-or-later

"use strict";

import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const DEFAULT_ROOT = path.resolve(HERE, "..", "..");
const HEX_COMMIT = /^[0-9a-fA-F]{40}(?:[0-9a-fA-F]{24})?$/;

const VERSION_FILES = [
  ["package.json", "npm package"],
  ["packaging/spec-lifecycle-manager/package-manifest.json", "package manifest"],
  ["plugins/spec-lifecycle-manager/.codex-plugin/plugin.json", "Codex plugin manifest"],
  ["plugins/spec-lifecycle-manager/claude-plugin/.claude-plugin/plugin.json", "Claude plugin manifest"],
];
const BUILD_FILES = [
  "plugins/spec-lifecycle-manager/build-info.json",
  "plugins/spec-lifecycle-manager/claude-plugin/build-info.json",
];

function readObject(root, relative, label) {
  const value = JSON.parse(fs.readFileSync(path.join(root, relative), "utf8"));
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    throw new Error(`${label} must be a JSON object: ${relative}`);
  }
  return value;
}

export function validatedVersion(root = DEFAULT_ROOT) {
  const entries = VERSION_FILES.map(([relative, label]) => {
    const version = readObject(root, relative, label).version;
    if (typeof version !== "string" || !version) throw new Error(`${label} has no version: ${relative}`);
    return { relative, label, version };
  });
  const versions = new Set(entries.map((entry) => entry.version));
  if (versions.size !== 1) {
    throw new Error(`Package versions disagree: ${entries.map((entry) => `${entry.relative}=${entry.version}`).join(", ")}`);
  }
  return entries[0].version;
}

export function resolveCommit(root = DEFAULT_ROOT, env = process.env) {
  const supplied = env.GITHUB_SHA;
  if (supplied && HEX_COMMIT.test(supplied)) return supplied.toLowerCase();
  const result = spawnSync("git", ["rev-parse", "HEAD"], { cwd: root, encoding: "utf8", windowsHide: true });
  const commit = result.status === 0 ? result.stdout.trim() : "";
  return HEX_COMMIT.test(commit) ? commit.toLowerCase() : "unknown";
}

export function writeBuildInfo(mode, root = DEFAULT_ROOT, env = process.env) {
  const version = validatedVersion(root);
  const commit = mode === "reset" ? "unknown" : resolveCommit(root, env);
  const buildIdentity = commit === "unknown" ? "unknown" : `git:${commit}`;
  const content = `${JSON.stringify({ name: "spec-lifecycle-manager", package_version: version, build_identity: buildIdentity }, null, 2)}\n`;
  for (const relative of BUILD_FILES) fs.writeFileSync(path.join(root, relative), content, "utf8");
  return { version, build_identity: buildIdentity, paths: [...BUILD_FILES] };
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const mode = process.argv[2] || "generate";
  if (!new Set(["generate", "reset"]).has(mode)) {
    process.stderr.write("Usage: generate-build-info.mjs [generate|reset]\n");
    process.exitCode = 2;
  } else {
    try {
      writeBuildInfo(mode);
    } catch (error) {
      process.stderr.write(`${error.message}\n`);
      process.exitCode = 1;
    }
  }
}
