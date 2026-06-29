---
title: Cross-platform packaging tasks
doc_type: spec
artifact_type: tasks
status: active
owner: platform
last_reviewed: 2026-06-29
---

# Tasks

## Task Dependency Graph

```text
T001 interpreter resolver ──┬─► T002 installer pins .mcp.json
                            └─► T003 installer pins hooks.json (exec form)
T004 installer.mjs (copy/register) ──► T005 npm-install.js wiring
                                       └─► T006 retire/delegate .sh
T007 marketplace static-config decision  (after T001)
T008 packaging manifests  (after T004/T006)
T009 platform CI matrix   (after T002, T003, T005)
T010 docs: platform/interpreter matrix  (after T009 evidence)
```

## Phase 1: Interpreter resolution

- [x] T001 Add the Python interpreter resolver.
  - Depends on: none
  - Files: `packaging/spec-lifecycle-manager/resolve-python.mjs` (new);
    `tests/runtime/resolve-python.test.mjs` (new); `package.json`
    (`test:node` script + wired into `validate`)
  - Acceptance: Honors `SPEC_LIFECYCLE_PYTHON`; else probes `py -3`/`python`/
    `python3` per platform, verifying Python ≥ 3 via `--version`; throws an
    actionable error when none resolve. Unit-tested with injected env/platform.
    Satisfies Requirement 2.1-2.4, P2, P4.
  - Evidence: `node --test tests/runtime/resolve-python.test.mjs` — 11/11 pass
    (override-honored-verbatim, win32 `py -3`→`python`→`python3` order, POSIX
    `python3`→`python` order, blank-override skip, P4 actionable throw). Real-host
    smoke: `resolvePython()` → `["python3"]` on Linux; `reportsPython3` accepts
    `python3`, rejects a missing command. Override is honored verbatim (not
    probe-gated) so it can rescue environments where probing cannot run
    (design.md Resolved Decisions §3; advisor-confirmed reading of the
    acceptance criteria).

## Phase 2: Cross-platform installer

- [ ] T002 Pin the resolved interpreter into the installed `.mcp.json`.
  - Depends on: T001, T004
  - Files: installed `.mcp.json` generation in `installer.mjs`; templates
    `plugins/spec-lifecycle-manager/.mcp.json`,
    `plugins/spec-lifecycle-manager/claude-plugin/.mcp.json`
  - Acceptance: Installed config uses exec form with the resolved `command`/
    `args`; no bare `python3` assumption. Satisfies Requirement 2.2.
  - Evidence: Pending.

- [ ] T003 Convert hook config to exec form with the resolved interpreter.
  - Depends on: T001, T004
  - Files: `plugins/spec-lifecycle-manager/hooks/hooks.json`,
    `plugins/spec-lifecycle-manager/claude-plugin/hooks/hooks.json`
  - Acceptance: `"command":"<resolved>","args":[...,"${PLUGIN_ROOT|CLAUDE_PLUGIN_ROOT}/.../codex_spec_lifecycle_hook.py"]`;
    no shell-form `python3 "..."` string. Codex matcher/token preserved.
    Satisfies Requirement 3.1-3.2.
  - Evidence: Pending.

- [ ] T004 Port the installer to Node (`installer.mjs`).
  - Depends on: none
  - Files: `packaging/spec-lifecycle-manager/installer.mjs` (new)
  - Acceptance: Reproduces `install-spec-lifecycle-manager-package.sh` steps
    (validate `--source`, copy files, register plugin/hook, honor flags) using
    only `node:fs/path/os`. Satisfies Requirement 1.1-1.2.
  - Evidence: Pending.

- [ ] T005 Wire `npm-install.js` to call `installer.mjs` in-process.
  - Depends on: T004
  - Files: `packaging/spec-lifecycle-manager/npm-install.js`
  - Acceptance: No `spawnSync` of a `.sh`; imports and calls `installer.mjs`;
    actionable failure naming the missing prerequisite. Satisfies Requirement
    1.4, P4.
  - Evidence: Pending.

- [ ] T006 Retire or delegate the legacy `.sh` installer.
  - Depends on: T004
  - Files: `scripts/install-spec-lifecycle-manager-package.sh`
  - Acceptance: Removed, or reduced to `exec node .../installer.mjs "$@"` so it
    cannot diverge. Satisfies Requirement 1.3, P3.
  - Evidence: Pending.

## Phase 3: Marketplace and packaging

- [ ] T007 Encode the marketplace static-config decision.
  - Depends on: T001
  - Files: shipped `.mcp.json`/`hooks.json` defaults; durable install docs
  - Decision (2026-06-29): static `command` is `python` + a documented
    "Python 3 on PATH" prerequisite (design.md Resolved Decisions §1). This task
    now only encodes that decision; the choice itself is settled.
  - Acceptance: shipped configs ship `python` in exec form; install docs state
    the "Python 3 on PATH" prerequisite and the `SPEC_LIFECYCLE_PYTHON` override.
  - Evidence: Pending.

- [ ] T008 Update packaging manifests for the new install model.
  - Depends on: T004, T006
  - Files: `packaging/spec-lifecycle-manager/npm-package.json`,
    `package-manifest.json`, root `package.json` `files`
  - Acceptance: `installer`/`hook_config_fallback`/`files` reference
    `installer.mjs`; `.sh` references updated or removed; `npm pack --dry-run`
    includes the new files and the package-parity test stays green.
  - Evidence: Pending.

## Phase 4: Verification

- [ ] T009 Add the cross-platform CI matrix.
  - Depends on: T002, T003, T005
  - Files: CI workflow under `.github/workflows/` (or repo CI equivalent)
  - Acceptance: Jobs on windows-latest, macos-latest, ubuntu-latest run install +
    MCP launch smoke + hook execution with a Claude-shaped payload
    (`tool_name:"Write"`). Satisfies Requirement 4.2. Record a manual run if a
    Windows runner is unavailable and note the gap.
  - Evidence: Pending.

- [ ] T010 Document the platform/interpreter matrix.
  - Depends on: T009
  - Files: durable install/operations docs; spec `verification.md`
  - Acceptance: Supported OS/Python matrix, interpreter resolution order, and
    `SPEC_LIFECYCLE_PYTHON` override documented. Satisfies Requirement 4.1, 4.3.
  - Evidence: Pending.
