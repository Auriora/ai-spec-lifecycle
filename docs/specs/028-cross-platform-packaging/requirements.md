---
title: Cross-platform packaging requirements
doc_type: spec
artifact_type: requirements
status: active
owner: platform
last_reviewed: 2026-06-29
---

# Requirements

## Introduction

The spec-lifecycle-manager plugin installs through a `.sh` script and launches
its MCP server and PostToolUse hook by invoking the command name `python3`. The
Python runtime itself is portable, and internal subprocess calls already use
`sys.executable` (the running interpreter), so the lifecycle logic runs anywhere
Python does. The portability gap is entirely in the **distribution and entry
layer**: a Bourne-shell installer, and the hard-coded interpreter name `python3`
in `.mcp.json` and `hooks.json`. On Windows the canonical interpreter is `py`
(the PEP 397 launcher) or `python`; `python3` is frequently absent. On some
Linux/macOS hosts `python` is absent and only `python3` exists. No single
command name resolves on all three OSes.

This spec makes the plugin install, launch its MCP server, and run its hook on
Windows, macOS, and Linux. The unifying principle mirrors the companion
agent-workbench spec: **remove the shell from the command layer** and **resolve
the Python interpreter explicitly** rather than assuming one command name. The
installer becomes a portable Node program (the `bin` is already Node), and the
interpreter used by `.mcp.json`/`hooks.json` is pinned to whatever the host
actually provides.

## Durable Source Baseline

- `packaging/spec-lifecycle-manager/npm-install.js` (line 8 resolves a `.sh`
  installer; line 38 `spawnSync(installer, ...)` executes it)
- `scripts/install-spec-lifecycle-manager-package.sh` (`.sh` installer; declared
  `hook_config_fallback` in `package-manifest.json`)
- `plugins/spec-lifecycle-manager/.mcp.json` and
  `plugins/spec-lifecycle-manager/claude-plugin/.mcp.json`
  (`"command": "python3"`)
- `plugins/spec-lifecycle-manager/hooks/hooks.json` and
  `plugins/spec-lifecycle-manager/claude-plugin/hooks/hooks.json`
  (shell-form `"command": "python3 \"${...}/codex_spec_lifecycle_hook.py\""`)
- `packaging/spec-lifecycle-manager/npm-package.json` and
  `package-manifest.json` (declare the `.sh` installer)
- `skills/spec-lifecycle-manager/scripts/*.py` (`#!/usr/bin/env python3`
  shebangs; internal subprocesses already use `sys.executable`)

## Goals

- Install the npm package on Windows, macOS, and Linux without a POSIX shell.
- Launch the MCP server from `.mcp.json` on all three OSes using an interpreter
  that actually exists on the host.
- Run the PostToolUse hook on all three OSes without depending on the `python3`
  command name or a POSIX shell.
- Keep one source of truth per concern; do not fork a parallel Windows-only
  installer/launcher/hook layer.
- Document and test the supported platform/interpreter matrix.

## Non-Goals

- Do not change the lifecycle hook or MCP business logic; it is already
  portable, and internal subprocessing already uses `sys.executable`.
- Do not drop Linux/macOS support or change the default Unix install location.
- Do not bundle or vendor a Python runtime; the host must provide Python 3.
- Do not require Windows users to install WSL, Git Bash, MSYS2, or Cygwin.

## Requirements

### Requirement 1: Shell-Free Installer

**User Story:** As a Windows user, I want `npx` install to run, so that I can
install spec-lifecycle-manager without a POSIX shell.

#### Acceptance Criteria

1. GIVEN a host with Node.js and Python 3 but no `bash`/`sh` on PATH, WHEN the
   user runs the package `bin` installer, THEN THE SYSTEM SHALL install without
   spawning a `.sh` script.
2. WHEN the installer copies files and registers the plugin/hook, THEN it SHALL
   use one cross-platform implementation shared by Windows, macOS, and Linux.
3. WHERE the legacy `scripts/install-spec-lifecycle-manager-package.sh` is
   retained for existing Unix workflows, THE SYSTEM SHALL keep it
   behavior-equivalent to the cross-platform installer or delegate to it.
4. IF Python 3 cannot be found by the installer, THEN it SHALL fail with an
   actionable message naming the missing prerequisite and per-OS remediation.

### Requirement 2: Explicit Python Interpreter Resolution

**User Story:** As a plugin user on any OS, I want the MCP server and hook to
launch with the right interpreter, so that they do not fail because `python3` is
not the local command name.

#### Acceptance Criteria

1. WHEN the MCP server or hook is launched, THEN THE SYSTEM SHALL invoke a
   Python interpreter that exists on the host (resolved from `py`, `python3`, or
   `python` per platform) rather than assuming the literal name `python3`.
2. WHERE the npm/installer distribution path is used, THE SYSTEM SHALL detect
   the available interpreter at install time and pin it into the installed
   `.mcp.json`/hook configuration or a generated launcher.
3. WHEN a user overrides the interpreter via a documented environment variable,
   THEN THE SYSTEM SHALL honor it on all three OSes.
4. IF no Python 3 interpreter resolves at launch, THEN THE SYSTEM SHALL surface
   an actionable error rather than a silent MCP/hook failure.

### Requirement 3: Shell-Free Hook Command

**User Story:** As a plugin user on any OS, I want the PostToolUse hook to run,
so that I get spec lifecycle advisory feedback regardless of shell.

#### Acceptance Criteria

1. WHEN the hook command runs, THEN it SHALL use exec form (`"command"` +
   `"args"` array) so it is spawned without a shell on Windows, macOS, and Linux.
2. WHEN the hook command references the script, THEN it SHALL use the
   runtime-provided plugin-root token (`${CLAUDE_PLUGIN_ROOT}` for Claude,
   `${PLUGIN_ROOT}` for Codex) expanded by the runtime, not by a shell.
3. WHEN the same hook runs under Codex and Claude Code on all three OSes, THEN
   it SHALL produce equivalent advisory output and never block the tool flow.

### Requirement 4: Verified Platform Matrix

**User Story:** As a maintainer, I want the supported platforms verified, so
that "cross-platform" reflects executed runs rather than static review.

#### Acceptance Criteria

1. THE SYSTEM SHALL document the supported platform/interpreter matrix (OS
   versions, Python version floor, interpreter resolution order) in durable docs.
2. WHEN portability changes land, THEN install, MCP launch, and hook execution
   SHALL be exercised on Windows, macOS, and Linux via CI or recorded manual
   runs, and the evidence SHALL be captured in `verification.md`.
3. WHERE interpreter resolution differs per OS (`py` vs `python3` vs `python`),
   THE SYSTEM SHALL document the resolution order and the override variable.

## Correctness Properties

- **P1 Shell independence:** No install, launch, or hook entry point requires a
  POSIX shell or a bash shebang on any supported OS.
- **P2 Interpreter existence:** The interpreter used to launch the MCP server
  and hook is one proven to exist on the host, not a fixed name assumed present.
- **P3 Single source of truth:** Each concern (install, MCP launch, hook) has
  one cross-platform implementation; any retained Unix variant is delegated or
  proven equivalent.
- **P4 Fail-loud prerequisites:** A missing Python 3 interpreter yields an
  actionable error, never a silent partial install or silent hook/MCP no-op.

## Success Criteria

- `npx`/`bin` install completes on a Windows host with Node + Python 3 and no
  POSIX shell.
- The MCP server launches from `.mcp.json` and the hook fires on Windows, macOS,
  and Linux using a host-resolved interpreter.
- The platform/interpreter matrix is documented in durable docs and
  install/launch/hook runs are evidenced in `verification.md`.
