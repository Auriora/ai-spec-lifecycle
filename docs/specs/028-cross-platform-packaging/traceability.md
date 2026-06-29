---
title: Cross-platform packaging traceability
doc_type: spec
artifact_type: traceability
status: active
owner: platform
last_reviewed: 2026-06-29
---

# Traceability

## Requirement To Delivery Matrix

| Requirement | Acceptance focus | Design sections | Tasks | Verification target |
|-------------|------------------|-----------------|-------|---------------------|
| R1 Shell-Free Installer | install without a POSIX shell; one shared implementation; legacy `.sh` delegated; actionable missing-Python error | Cross-platform installer, Error handling | T004, T005, T006, T008 | Windows `bin` install run; single-source guard |
| R2 Explicit Python Interpreter Resolution | resolve `py`/`python3`/`python`; pin at install; honor override; fail loud at launch | Interpreter resolver, Pinned exec-form configs | T001, T002 | `resolvePython` unit tests; MCP launch on all three OSes |
| R3 Shell-Free Hook Command | exec form (`command`+`args`); runtime plugin-root token; cross-runtime parity | Pinned exec-form configs, Documented execution-model basis | T003 | Hook execution with Claude-shaped payload on all three OSes |
| R4 Verified Platform Matrix | documented OS/Python/interpreter matrix; executed per-OS runs; resolution order + override documented | Operational Considerations, Verification | T009, T010 | CI matrix evidence; durable matrix docs |

## Correctness Property To Task Matrix

| Property | Tasks | Validation signal |
|----------|-------|-------------------|
| P1 Shell independence | T003, T004, T005, T006 | No shell/bash shebang in any install/launch/hook entry; exec-form hook |
| P2 Interpreter existence | T001, T002 | Resolver verifies `--version` ≥ 3 before selecting; pinned config uses resolved command |
| P3 Single source of truth | T002, T006, T008 | `.sh` removed or thin delegator; package-parity test green; shared installer logic |
| P4 Fail-loud prerequisites | T001, T005 | Actionable error on missing Python; no silent partial install or MCP/hook no-op |

## Task To Context Matrix

| Task | Requirements / Properties | Primary files | Evidence expected |
|------|---------------------------|---------------|-------------------|
| T001 | R2, P2, P4 | `packaging/spec-lifecycle-manager/resolve-python.mjs`, `tests/runtime/resolve-python.test.mjs`, `package.json` | Resolver unit tests; real-host smoke |
| T002 | R2, P2 | `installer.mjs` config generation; `.mcp.json` templates (both copies) | Installed `.mcp.json` uses resolved exec form |
| T003 | R3, P1 | `hooks/hooks.json`, `claude-plugin/hooks/hooks.json` | Exec-form hook (Claude); resolved-interpreter Codex entry |
| T004 | R1, P1 | `packaging/spec-lifecycle-manager/installer.mjs` (new) | Node installer reproduces `.sh` steps using `node:fs/path/os` |
| T005 | R1, P1, P4 | `packaging/spec-lifecycle-manager/npm-install.js` | No `spawnSync` of `.sh`; actionable failure |
| T006 | R1, P3 | `scripts/install-spec-lifecycle-manager-package.sh` | Removed or reduced to `node installer.mjs` delegator |
| T007 | R2 | shipped `.mcp.json`/`hooks.json` defaults; install docs | Static `python` default + PATH prerequisite encoded |
| T008 | R1, P3 | `npm-package.json`, `package-manifest.json`, root `package.json` `files` | Manifests reference `installer.mjs`; `npm pack --dry-run` green |
| T009 | R4 | CI workflow under `.github/workflows/` | Per-OS install + MCP launch + hook execution evidence |
| T010 | R4 | durable install/operations docs; `verification.md` | OS/Python matrix, resolution order, override documented |

## Design To Implementation Matrix

| Design section | Implementation tasks | Validation signal |
|----------------|----------------------|-------------------|
| Interpreter resolver | T001 | `resolvePython` unit tests; injected env/platform |
| Cross-platform installer | T004, T005, T006 | Node install run; no `.sh` spawn |
| Pinned exec-form configs (`.mcp.json`) | T002 | Installed config uses resolved command/args |
| Pinned exec-form configs (`hooks.json`) | T003 | Exec-form hook; Codex token preserved |
| Marketplace fallback (Resolved Decisions §1) | T007 | Static `python` default + prerequisite doc |
| Operational Considerations / Verification | T009, T010 | CI matrix + durable matrix docs |

## Open Decision Impact

All decisions below were resolved on 2026-06-29 before implementation; none
remain open. Retained here for traceability.

| Decision | Affected requirements | Affected tasks | Status |
|----------|-----------------------|----------------|--------|
| Marketplace static config: `python` + PATH prerequisite | R2 | T002, T003, T007 | Resolved 2026-06-29 (design.md Resolved Decisions §1) |
| Windows interpreter order `py -3` → `python` → `python3` | R2 | T001 | Resolved 2026-06-29 (§2) |
| Override variable `SPEC_LIFECYCLE_PYTHON` | R2 | T001 | Resolved 2026-06-29 (§3) |
| Codex exec-form hook support unconfirmed; ship shell-form with resolved interpreter | R3 | T003, T009 | Resolved 2026-06-29 (§4); confirm in T009 |
