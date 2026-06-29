"use strict";

import { spawnSync } from "node:child_process";

// Spec 028: there is no single Python command name that resolves on Windows,
// macOS, and Linux. Resolve the interpreter explicitly instead of assuming one.
//
// Order (design.md Resolved Decisions §2): Windows prefers the PEP 397 launcher
// `py -3`, then `python`, then `python3`. POSIX prefers `python3`, then
// `python`. A documented `SPEC_LIFECYCLE_PYTHON` override (§3) wins on every OS
// and is honored verbatim so it can rescue environments where probing itself
// cannot run.

const WIN_CANDIDATES = [["py", "-3"], ["python"], ["python3"]];
const POSIX_CANDIDATES = [["python3"], ["python"]];

const NOT_FOUND_MESSAGE = [
  "Python 3 not found.",
  "Install it (Windows: python.org or 'winget install Python.Python.3';",
  "macOS: 'brew install python'; Linux: your distribution's python3 package),",
  "or set SPEC_LIFECYCLE_PYTHON to the interpreter command.",
].join(" ");

/** Split a command string ("py -3") into a command vector (["py", "-3"]). */
export function splitCommand(value) {
  return String(value).trim().split(/\s+/).filter(Boolean);
}

/** Candidate command vectors for the given platform, in resolution order. */
export function candidatesFor(platform) {
  return platform === "win32" ? WIN_CANDIDATES : POSIX_CANDIDATES;
}

/**
 * Spawn `<command> [...args] --version` and report whether it is Python >= 3.
 * Returns false on any spawn error, non-zero exit, or unparseable output.
 */
export function reportsPython3(command) {
  const [bin, ...args] = command;
  if (!bin) return false;
  const result = spawnSync(bin, [...args, "--version"], {
    encoding: "utf8",
    windowsHide: true,
  });
  if (result.error || result.status !== 0) return false;
  const text = `${result.stdout || ""}${result.stderr || ""}`;
  const match = text.match(/Python\s+(\d+)\./i);
  return match ? Number(match[1]) >= 3 : false;
}

/**
 * Resolve the Python interpreter command vector for the host.
 *
 * @param {object} [options]
 * @param {NodeJS.ProcessEnv} [options.env]   environment (for the override)
 * @param {string} [options.platform]          process.platform value
 * @param {(command: string[]) => boolean} [options.probe]  candidate verifier
 * @returns {string[]} command vector, e.g. ["py", "-3"] or ["python3"]
 * @throws {Error} actionable message when no Python 3 interpreter resolves
 */
export function resolvePython({
  env = process.env,
  platform = process.platform,
  probe = reportsPython3,
} = {}) {
  const override = env.SPEC_LIFECYCLE_PYTHON;
  if (override && override.trim()) {
    // Honored verbatim: the override is the escape hatch for environments
    // where probing cannot run or misjudges, so it must not be probe-gated.
    return splitCommand(override);
  }
  for (const candidate of candidatesFor(platform)) {
    if (probe(candidate)) return candidate;
  }
  throw new Error(NOT_FOUND_MESSAGE);
}
