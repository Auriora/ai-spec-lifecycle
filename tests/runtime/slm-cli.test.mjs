"use strict";

import { test } from "node:test";
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { createRequire } from "node:module";
import path from "node:path";
import { fileURLToPath } from "node:url";

const require = createRequire(import.meta.url);
const { dispatch } = require("../../packaging/spec-lifecycle-manager/slm-cli.js");
const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");

function queryDependencies(overrides = {}) {
  return {
    packageRoot: "/package",
    pythonCli: "/package/plugin/slm_cli.py",
    resolvePython: () => ["python3", "-I"],
    spawnSync: () => ({ status: 0 }),
    writeError: () => {},
    signalProcess: () => {},
    ...overrides,
  };
}

test("bare slm dispatches to the bundled Python specs command without a shell", async () => {
  let call;
  const code = await dispatch([], queryDependencies({
    spawnSync: (command, args, options) => {
      call = { command, args, options };
      return { status: 0 };
    },
  }));
  assert.equal(code, 0);
  assert.equal(call.command, "python3");
  assert.deepEqual(call.args, ["-I", "/package/plugin/slm_cli.py", "specs"]);
  assert.equal(call.options.shell, false);
  assert.equal(call.options.stdio, "inherit");
});

test("query arguments and child exit status are forwarded unchanged", async () => {
  let forwarded;
  const code = await dispatch(["tasks", "039", "--json"], queryDependencies({
    spawnSync: (_command, args) => {
      forwarded = args;
      return { status: 2 };
    },
  }));
  assert.equal(code, 2);
  assert.deepEqual(forwarded.slice(-3), ["tasks", "039", "--json"]);
});

test("install is routed in-process with package source and separator removed", async () => {
  let forwarded;
  const code = await dispatch(["install", "--", "--help"], queryDependencies({
    install: async (args) => {
      forwarded = args;
      return 0;
    },
  }));
  assert.equal(code, 0);
  assert.deepEqual(forwarded, ["--source", "/package", "--help"]);
});

test("Python resolution and spawn failures return runtime exit one", async () => {
  const errors = [];
  const resolution = await dispatch(["specs"], queryDependencies({
    resolvePython: () => { throw new Error("no python"); },
    writeError: (message) => errors.push(message),
  }));
  const spawn = await dispatch(["specs"], queryDependencies({
    spawnSync: () => ({ error: new Error("spawn failed") }),
    writeError: (message) => errors.push(message),
  }));
  assert.equal(resolution, 1);
  assert.equal(spawn, 1);
  assert.match(errors.join(""), /no python/);
  assert.match(errors.join(""), /spawn failed/);
});

test("child signals are forwarded to the parent process", async () => {
  let forwarded;
  const code = await dispatch(["specs"], queryDependencies({
    spawnSync: () => ({ status: null, signal: "SIGTERM" }),
    signalProcess: (signal) => { forwarded = signal; },
  }));
  assert.equal(code, 1);
  assert.equal(forwarded, "SIGTERM");
});

test("repo-root ./slm launches the source-backed public CLI", () => {
  const launcher = path.join(repoRoot, "slm");
  const command = process.platform === "win32" ? process.execPath : launcher;
  const args = process.platform === "win32" ? [launcher, "--help"] : ["--help"];
  const result = spawnSync(command, args, {
    cwd: repoRoot,
    encoding: "utf8",
  });
  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /usage: slm/);
  assert.match(result.stdout, /specs/);
  assert.match(result.stdout, /install/);
});
