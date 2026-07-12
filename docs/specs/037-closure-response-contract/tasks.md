---
title: Closure Response Contract Tasks
doc_type: spec
artifact_type: tasks
status: active
owner: maintainers
last_reviewed: 2026-07-12
---

# Tasks

## Dependency Graph

`T001 -> T002 -> T003 -> T004`

- [x] T001 [US1] Exclude irrelevant reference roots and file classes.
  - Depends on: none
  - Files: `skills/spec-lifecycle-manager/scripts/lifecycle/closure.py`
  - Acceptance: Ignore files, cache/VCS roots, databases, WAL/SHM, and binaries do not create findings.
  - Evidence: Ignore-aware scanner and focused MCP regression fixture.
- [x] T002 [US1] Add the relevant-by-construction closure manifest.
  - Depends on: T001
  - Files: `skills/spec-lifecycle-manager/scripts/lifecycle/closure.py`, `skills/spec-lifecycle-manager/scripts/lifecycle/core.py`
  - Acceptance: Agent-facing plans contain summaries and no replacement bodies; responses remain at or below 32 KiB.
  - Evidence: `test_closure_mcp_plan_is_bounded_and_actions_are_sequential_and_idempotent`.
- [x] T003 [US2] Make apply stateless, independently scoped, and idempotent.
  - Depends on: T002
  - Files: `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`, `skills/spec-lifecycle-manager/scripts/lifecycle/closure.py`
  - Acceptance: Apply regenerates and verifies the plan; record upserts do not duplicate; cleanup requires records and does not rerender them.
  - Evidence: Focused MCP tests pass, including stale fingerprint and sequential actions.
- [x] T004 Validate, synchronize bundles, and promote the public contract.
  - Depends on: T003
  - Files: `tests/runtime/test_spec_mcp_server.py`, `docs/reference/spec-lifecycle-runtime.md`, plugin bundle mirrors
  - Acceptance: Full validation, package parity, and diff checks pass.
  - Evidence: `npm run validate` passed: 306 Python tests, 25 Node tests, scan, archive index, prompts, package contract, sync guard, pack dry run, and diff check.
- [x] T005 Remove duplicate JSON from the MCP transport envelope.
  - Depends on: T004
  - Files: `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`, `tests/runtime/test_spec_mcp_server.py`, plugin bundle mirrors
  - Acceptance: `structuredContent` remains authoritative and unchanged; text `content` is a useful summary below 512 bytes and does not repeat payload collections.
  - Evidence: MCP module passed 46 tests; `npm run validate` passed 307 Python tests, 25 Node tests, package contract, bundle parity, runtime checks, pack dry run, and diff check.
