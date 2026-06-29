"use strict";

import { test } from "node:test";
import assert from "node:assert/strict";

import {
  resolvePython,
  candidatesFor,
  splitCommand,
} from "../../packaging/spec-lifecycle-manager/resolve-python.mjs";

// Deterministic probe: only the listed command vectors "report Python 3".
const probeAccepting = (...accepted) => {
  const keys = new Set(accepted.map((cmd) => cmd.join(" ")));
  return (command) => keys.has(command.join(" "));
};
const probeAll = () => true;
const probeNone = () => false;

test("splitCommand parses a command string into a vector", () => {
  assert.deepEqual(splitCommand("py -3"), ["py", "-3"]);
  assert.deepEqual(splitCommand("  python3  "), ["python3"]);
  assert.deepEqual(splitCommand("/opt/py/bin/python"), ["/opt/py/bin/python"]);
});

test("candidate order: win32 prefers py -3 then python then python3", () => {
  assert.deepEqual(candidatesFor("win32"), [["py", "-3"], ["python"], ["python3"]]);
});

test("candidate order: POSIX prefers python3 then python (OQ2 reorder is win-only)", () => {
  assert.deepEqual(candidatesFor("linux"), [["python3"], ["python"]]);
  assert.deepEqual(candidatesFor("darwin"), [["python3"], ["python"]]);
});

test("win32 selects py -3 when available", () => {
  const cmd = resolvePython({ env: {}, platform: "win32", probe: probeAll });
  assert.deepEqual(cmd, ["py", "-3"]);
});

test("win32 falls back to python when py -3 is absent", () => {
  const cmd = resolvePython({
    env: {},
    platform: "win32",
    probe: probeAccepting(["python"], ["python3"]),
  });
  assert.deepEqual(cmd, ["python"]);
});

test("POSIX selects python3", () => {
  const cmd = resolvePython({ env: {}, platform: "linux", probe: probeAll });
  assert.deepEqual(cmd, ["python3"]);
});

test("POSIX falls back to python when python3 is absent", () => {
  const cmd = resolvePython({
    env: {},
    platform: "darwin",
    probe: probeAccepting(["python"]),
  });
  assert.deepEqual(cmd, ["python"]);
});

test("SPEC_LIFECYCLE_PYTHON override is honored verbatim, not probe-gated", () => {
  // probeNone => auto-detect would fail; the override must still win.
  const cmd = resolvePython({
    env: { SPEC_LIFECYCLE_PYTHON: "/opt/custom/python3.12" },
    platform: "win32",
    probe: probeNone,
  });
  assert.deepEqual(cmd, ["/opt/custom/python3.12"]);
});

test("override carries its own args (e.g. py -3)", () => {
  const cmd = resolvePython({
    env: { SPEC_LIFECYCLE_PYTHON: "py -3" },
    platform: "linux",
    probe: probeNone,
  });
  assert.deepEqual(cmd, ["py", "-3"]);
});

test("blank override is ignored and probing proceeds", () => {
  const cmd = resolvePython({
    env: { SPEC_LIFECYCLE_PYTHON: "   " },
    platform: "linux",
    probe: probeAll,
  });
  assert.deepEqual(cmd, ["python3"]);
});

test("throws an actionable error when no interpreter resolves (P4)", () => {
  assert.throws(
    () => resolvePython({ env: {}, platform: "linux", probe: probeNone }),
    (err) => {
      assert.match(err.message, /Python 3 not found/);
      assert.match(err.message, /SPEC_LIFECYCLE_PYTHON/);
      return true;
    },
  );
});
