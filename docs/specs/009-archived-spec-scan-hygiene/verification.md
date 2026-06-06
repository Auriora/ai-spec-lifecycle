---
title: Archived spec scan hygiene verification
doc_type: spec
artifact_type: verification
status: archived
owner: platform
last_reviewed: 2026-06-06
---

# Verification

## Scope

This verification record covers spec 009 tasks T001 through T006: archived scan
classification, default active-health skipping, explicit archived audit mode,
MCP exposure, tests, durable docs, and installed skill sync.

## Quality Gates

| Gate | Required? | Status | Evidence |
|------|-----------|--------|----------|
| Requirements acceptance criteria reviewed | yes | pass | Requirements 1-4 mapped to runtime, MCP, tests, and docs. |
| Task evidence complete | yes | pass | `tasks.md` records evidence for T001-T006. |
| Automated tests pass or alternate verification recorded | yes | pass | Full regression suite passed. |
| Durable documentation updates identified | yes | pass | Runtime reference and lifecycle design identified. |
| Durable documentation promoted or explicitly deferred | yes | pass | Runtime reference, lifecycle design, and skill guidance updated. |
| Governance or policy conflicts resolved | yes | pass | Behavior preserves archived history and direct lint strictness. |

## Validation Commands

| Command | Purpose | Result | Evidence |
|---------|---------|--------|----------|
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'` | Full regression tests | pass | 39 tests passed. |
| `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py lint docs/specs/009-archived-spec-scan-hygiene` | Spec package lint | pass | No diagnostics. |
| `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py closure-check docs/specs/009-archived-spec-scan-hygiene` | Closure readiness | pass | Ready with no blockers. |
| `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py scan .` | Default scan behavior | pass | Archived specs retained in inventory with skipped archived health; active summary reported. |
| `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py scan . --include-archived-lint` | Archived audit behavior | pass | Spec 001 archived diagnostics visible with error severity and 47 diagnostics. |
| `rsync -a --delete skills/spec-lifecycle-manager/ "$HOME/.codex/skills/spec-lifecycle-manager/"` | Installed skill sync | pass | User-level installed skill updated from repository source. |
| `git diff --check` | Diff whitespace hygiene | pass | No whitespace errors reported. |

## Evidence Log

| Date | Evidence | Result | Notes |
|------|----------|--------|-------|
| 2026-06-06 | Implementation review | pass | Runtime, MCP, tests, and docs updated before validation. |
| 2026-06-06 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'` | pass | 39 tests passed. |
| 2026-06-06 | `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py lint docs/specs/009-archived-spec-scan-hygiene` | pass | No diagnostics. |
| 2026-06-06 | `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py closure-check docs/specs/009-archived-spec-scan-hygiene` | pass | Ready with no blockers. |
| 2026-06-06 | Default scan | pass | `summary.archived` is 4; archived specs report skipped archived health. |
| 2026-06-06 | Archived scan audit | pass | Spec 001 reports error severity with 47 diagnostics when audit mode is enabled. |
| 2026-06-06 | Installed skill sync | pass | User-level `~/.codex/skills/spec-lifecycle-manager/` updated from repo source. |
| 2026-06-06 | `git diff --check` | pass | No whitespace errors reported. |

## Requirement Coverage

| Requirement | Acceptance criteria covered | Evidence | Residual risk |
|-------------|-----------------------------|----------|---------------|
| Requirement 1 | AC1, AC2, AC3 | `scan_specs`, `health_summary`, runtime tests | Existing consumers may ignore new summary fields. |
| Requirement 2 | AC1, AC2, AC3 | CLI flag, MCP argument, direct lint unchanged | MCP clients pass booleans inconsistently, so string values are accepted. |
| Requirement 3 | AC1, AC2, AC3 | Runtime reference and lifecycle design | None known. |
| Requirement 4 | AC1, AC2, AC3 | Runtime and MCP tests | None known. |

## Residual Risks

- Existing third-party consumers that only inspect per-spec `health.severity`
  must treat `archived` as a skipped historical state, not a failing state.

## Task Evidence

| Task ID | Status | Evidence | Notes |
|---------|--------|----------|-------|
| T001 | complete | Spec package created. | Includes requirements, design, tasks, traceability, and verification. |
| T002 | complete | Runtime scan classifies lifecycle and skips archived lint by default. | Active and archived summary counts added. |
| T003 | complete | CLI and MCP audit option added. | Direct lint remains strict. |
| T004 | complete | Runtime and MCP tests updated. | Full regression suite passed. |
| T005 | complete | Durable docs updated. | Runtime reference, lifecycle design, and skill guidance updated. |
| T006 | complete | Validation complete; installed skill synced. | Evidence recorded after final run. |

## Durable Promotion And Cleanup

| Spec content | Durable destination or deferral | Status | Evidence |
|--------------|---------------------------------|--------|----------|
| Default active-health semantics | `docs/reference/spec-lifecycle-runtime.md` | complete | Archived scan behavior section added. |
| Historical package migration guidance | `docs/design/spec-lifecycle-management.md` | complete | Reconciliation and runtime support sections updated. |
| MCP audit option | `docs/reference/spec-lifecycle-runtime.md` | complete | `include_archived_lint` documented. |
| Codex hook advisory guidance | `docs/reference/spec-lifecycle-runtime.md`, `docs/reference/spec-lifecycle-manager-mcp-install.md`, `skills/spec-lifecycle-manager/SKILL.md` | complete | Advisory Codex hook wrapper documented and installed after spec 009 implementation. |

### Spec Cleanup Decision

- **Cleanup action:** retain as history note
- **Reason:** The package records archived scan hygiene implementation evidence
  and remains useful for validating scan behavior.
- **Final spec commit:** `1095b7f`
- **Closure log path:** `docs/history/spec-closure-log.md`
- **Closure log entry updated:** yes
- **Closure cleanup commit:** `ccba3e9`
- **Active indexes updated:** yes
- **Durable docs linked back to evidence where useful:** yes
- **Residual spec-only content:** Implementation evidence remains in spec 009
  as retained history.

## Ship Or Closure Risk

- **Risk level:** low
- **Breaking change:** no
- **Blast radius checked:** yes
- **Rollback path:** revert runtime scan changes and documentation updates
- **Requires human review:** optional
- **Release notes needed:** no
- **Follow-up issue or spec needed:** yes, Codex hook dogfooding in spec 010

## Readiness Decision

- **Ready for promotion:** yes
- **Ready for release:** yes
- **Ready for closure:** yes; retained as historical evidence.
