---
title: Spec archive index runtime verification
doc_type: spec
artifact_type: verification
status: draft
owner: platform
last_reviewed: 2026-06-06
---

# Verification

## Scope

This verification record covers archive index durable documentation, runtime
validation, MCP exposure, current closed-spec indexing, and closure readiness.

## Quality Gates

| Gate | Required? | Status | Evidence |
|------|-----------|--------|----------|
| Requirements acceptance criteria reviewed | yes | pending | |
| Task evidence complete | yes | pending | T001 complete; implementation tasks pending. |
| Automated tests pass or alternate verification recorded | yes | pending | |
| Durable documentation updates identified | yes | pass | Archive index, lifecycle design, runtime reference, backlog, roadmap. |
| Durable documentation promoted or explicitly deferred | yes | pending | |
| Spec cleanup decision recorded | yes | pending | |
| Governance or policy conflicts resolved | yes | pending | No conflict known; cleanup policy must remain deliberate. |

## Validation Commands

| Command | Purpose | Result | Evidence |
|---------|---------|--------|----------|
| `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py lint docs/specs/011-spec-archive-index-runtime` | Spec package lint | pass | 0 diagnostics after T003-T006 updates. |
| `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py next-task docs/specs/011-spec-archive-index-runtime` | Next task selection | pass | Selected T008 with no traceability gaps after T003-T006 completion. |
| `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py archive-index .` | Archive index validation | pass | 9 retained entries, 1 legacy gap, 0 diagnostics. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_spec_runtime tests.runtime.test_spec_mcp_server` | Focused runtime and MCP tests | pass | 37 tests passed. |
| `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py closure-check docs/specs/011-spec-archive-index-runtime` | Closure readiness | expected blocked | Only T008 remains incomplete until closure. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'` | Full regression tests | pass | 45 tests passed. |
| `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py scan .` | Active scan | pass | Spec 011 is the only active spec and has pass health. |
| `git diff --check` | Diff whitespace hygiene | pass | No whitespace errors. |

## Evidence Log

| Date | Evidence | Result | Notes |
|------|----------|--------|-------|
| 2026-06-06 | Spec package created | pass | Requirements, design, tasks, traceability, and verification created. |
| 2026-06-06 | Durable planning and archive-index baseline added | pass | Roadmap, backlog, archive index, lifecycle design, and docs index updated. |
| 2026-06-06 | Archive index runtime and MCP support added | pass | CLI, parser, validator, MCP tool/resource, docs, and tests completed for T003-T006. |

## Task Evidence

| Task ID | Status | Evidence | Notes |
|---------|--------|----------|-------|
| T001 | complete | Spec package created as active roadmap item R001. | |
| T002 | complete | Archive index durable doc created and linked from lifecycle docs and docs index. | |
| T003 | complete | Runtime parser/validator implemented and tested. | Commit syntax and path consistency only; no Git object inspection. |
| T004 | complete | CLI command and runtime docs added. | `archive-index` returns deterministic JSON. |
| T005 | complete | MCP tool/resource exposed and tested. | Read-only. |
| T006 | complete | Current archive index validates cleanly. | 9 retained entries, 1 legacy gap, no removals. |
| T007 | complete | B003 promoted to spec 011; R001 marked active; later work routed to backlog/roadmap. | |
| T008 | pending | | |

## Durable Promotion And Cleanup

| Spec content | Durable destination or deferral | Status | Evidence |
|--------------|---------------------------------|--------|----------|
| Archive index format | `docs/history/spec-archive-index.md` | complete | Initial index created for specs with closure-log evidence. |
| Lifecycle cleanup rules | `docs/design/spec-lifecycle-management.md` | complete | Archive-index role documented. |
| Runtime command and MCP surface | `docs/reference/spec-lifecycle-runtime.md` | complete | `archive-index`, `archive_index`, and `history://spec-archive-index` documented. |
| Planning status | `docs/backlog/README.md`, `docs/roadmap/README.md` | partial | Initial roadmap/backlog entries created. |

## Residual Risks

- Spec 001 predates the closure-log workflow and is intentionally listed as a
  legacy gap until a separate audit records or rejects reconstructed evidence.
- Runtime validation checks commit syntax and path consistency, not Git object
  history.
- This spec does not remove retained archived packages.

### Spec Cleanup Decision

- **Cleanup action:** pending
- **Reason:** Implementation not complete.
- **Final spec commit:** pending
- **Closure log path:** `docs/history/spec-closure-log.md`
- **Closure log entry updated:** pending
- **Closure cleanup commit:** pending
- **Active indexes updated:** pending
- **Durable docs linked back to evidence where useful:** pending
- **Residual spec-only content:** pending

## Readiness Decision

- **Ready for promotion:** no
- **Ready for release:** no
- **Ready for closure:** no

## Related Artifacts

- Requirements: requirements.md
- Design: design.md
- Tasks: tasks.md
- Traceability: traceability.md
