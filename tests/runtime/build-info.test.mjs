"use strict";

import { test } from "node:test";
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

import { resolveCommit, validatedVersion, writeBuildInfo } from "../../packaging/spec-lifecycle-manager/generate-build-info.mjs";

function fixture() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "slm-build-info-"));
  const files = [
    "package.json",
    "packaging/spec-lifecycle-manager/package-manifest.json",
    "plugins/spec-lifecycle-manager/.codex-plugin/plugin.json",
    "plugins/spec-lifecycle-manager/claude-plugin/.claude-plugin/plugin.json",
  ];
  for (const relative of files) {
    fs.mkdirSync(path.dirname(path.join(root, relative)), { recursive: true });
    fs.writeFileSync(path.join(root, relative), '{"version":"1.2.3"}\n');
  }
  for (const relative of [
    "plugins/spec-lifecycle-manager/build-info.json",
    "plugins/spec-lifecycle-manager/claude-plugin/build-info.json",
  ]) {
    fs.mkdirSync(path.dirname(path.join(root, relative)), { recursive: true });
  }
  return root;
}

test("GITHUB_SHA takes precedence and generated data is deterministic and path-free", () => {
  const root = fixture();
  try {
    const sha = "A".repeat(40);
    const result = writeBuildInfo("generate", root, { GITHUB_SHA: sha });
    assert.deepEqual(result.build_identity, `git:${sha.toLowerCase()}`);
    const codex = JSON.parse(fs.readFileSync(path.join(root, result.paths[0]), "utf8"));
    const claude = JSON.parse(fs.readFileSync(path.join(root, result.paths[1]), "utf8"));
    assert.deepEqual(codex, { name: "spec-lifecycle-manager", package_version: "1.2.3", build_identity: `git:${sha.toLowerCase()}` });
    assert.deepEqual(codex, claude);
    assert.equal(JSON.stringify(codex).includes(root), false);
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});

test("invalid GITHUB_SHA falls back to the full git HEAD", () => {
  const root = fixture();
  try {
    assert.equal(spawnSync("git", ["init"], { cwd: root }).status, 0);
    assert.equal(spawnSync("git", ["config", "user.email", "test@example.com"], { cwd: root }).status, 0);
    assert.equal(spawnSync("git", ["config", "user.name", "Test"], { cwd: root }).status, 0);
    assert.equal(spawnSync("git", ["add", "."], { cwd: root }).status, 0);
    assert.equal(spawnSync("git", ["commit", "-m", "fixture"], { cwd: root }).status, 0);
    const expected = spawnSync("git", ["rev-parse", "HEAD"], { cwd: root, encoding: "utf8" }).stdout.trim();
    assert.equal(resolveCommit(root, { GITHUB_SHA: "short" }), expected);
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});

test("non-Git generation records an explicit unknown identity", () => {
  const root = fixture();
  try {
    assert.equal(resolveCommit(root, { GITHUB_SHA: "invalid" }), "unknown");
    const result = writeBuildInfo("generate", root, {});
    assert.equal(result.build_identity, "unknown");
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});

test("reset restores unknown identity and version disagreement fails closed", () => {
  const root = fixture();
  try {
    writeBuildInfo("generate", root, { GITHUB_SHA: "b".repeat(64) });
    assert.equal(writeBuildInfo("reset", root).build_identity, "unknown");
    const info = JSON.parse(fs.readFileSync(path.join(root, "plugins/spec-lifecycle-manager/build-info.json"), "utf8"));
    assert.deepEqual(info, { name: "spec-lifecycle-manager", package_version: "1.2.3", build_identity: "unknown" });
    fs.writeFileSync(path.join(root, "package.json"), '{"version":"9.9.9"}\n');
    assert.throws(() => validatedVersion(root), /versions disagree/);
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});
