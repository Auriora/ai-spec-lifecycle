"use strict";

import { test } from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { planLaunch } from "../../plugins/spec-lifecycle-manager/mcp-launch.mjs";

const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..");
const pluginRoot = path.join(repoRoot, "plugins", "spec-lifecycle-manager");
const serverPath = path.join(pluginRoot, "skills", "spec-lifecycle-manager", "scripts", "spec_mcp_server.py");

test("mcp launcher defaults the repo root to launch cwd", () => {
  const plan = planLaunch({}, [], "/workspace/repo");

  assert.equal(plan.command, "python3");
  assert.deepEqual(plan.args, [serverPath]);
  assert.equal(plan.options.env.SPEC_LIFECYCLE_DEFAULT_REPO_ROOT, "/workspace/repo");
  assert.equal(plan.options.cwd, undefined);
  assert.equal(plan.options.stdio, "inherit");
});

test("mcp launcher does not derive repo root from PWD", () => {
  const plan = planLaunch({ PWD: "/wrong/repo" }, [], "/workspace/repo");

  assert.equal(plan.options.env.SPEC_LIFECYCLE_DEFAULT_REPO_ROOT, "/workspace/repo");
});

test("mcp launcher preserves explicit defaults and interpreter overrides", () => {
  const plan = planLaunch(
    {
      SPEC_LIFECYCLE_DEFAULT_REPO_ROOT: "/explicit/repo",
      SPEC_LIFECYCLE_PYTHON: "py -3",
    },
    [],
    "/workspace/repo",
  );

  assert.equal(plan.command, "py");
  assert.deepEqual(plan.args, ["-3", serverPath]);
  assert.equal(plan.options.env.SPEC_LIFECYCLE_DEFAULT_REPO_ROOT, "/explicit/repo");
});

test("mcp launcher leaves default root unset when argv pins repo root", () => {
  const plan = planLaunch({}, ["--repo-root", "/fixed/repo"], "/workspace/repo");

  assert.equal(plan.options.env.SPEC_LIFECYCLE_DEFAULT_REPO_ROOT, undefined);
  assert.deepEqual(plan.args, [serverPath, "--repo-root", "/fixed/repo"]);
});
