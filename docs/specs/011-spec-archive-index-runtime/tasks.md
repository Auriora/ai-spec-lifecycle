---
title: Spec archive index runtime tasks
doc_type: spec
artifact_type: tasks
status: archived
owner: platform
last_reviewed: 2026-06-06
---

# Tasks

## Task Dependency Graph

```text
T001 -> T002 -> T003 -> T004 -> T005 -> T006
       T002 -> T007
       T004 -> T008
```

## Phase 1: Spec And Baseline

- [x] T001 Create archive index implementation spec.
  - Depends on: none
  - Files: `docs/specs/011-spec-archive-index-runtime/`
  - Acceptance: Requirements, design, tasks, traceability, and verification
    exist with durable baseline and acceptance criteria.
  - Evidence: Spec package created and linted as the next active roadmap item.

- [x] T002 Add durable archive index document.
  - Depends on: T001
  - Files: `docs/history/spec-archive-index.md`,
    `docs/design/spec-lifecycle-management.md`, `docs/README.md`
  - Acceptance: Archive index format, retained/removed semantics, and closure
    relationship are documented.
  - Evidence: Added `docs/history/spec-archive-index.md`, linked it from
    `docs/README.md`, and documented archive-index semantics in
    `docs/design/spec-lifecycle-management.md`.

## Phase 2: Runtime Support

- [x] T003 Implement archive index parser and validator.
  - Depends on: T002
  - Files: `skills/spec-lifecycle-manager/scripts/spec_runtime.py`,
    `tests/runtime/test_spec_runtime.py`
  - Acceptance: Runtime returns entries, summary counts, and diagnostics for
    malformed, missing, or drifting archive index data.
  - Evidence: Added `archive_index()` parser/validator and tests covering the
    current index plus malformed missing-commit/drift cases.

- [x] T004 Add CLI command and hook-ready diagnostics.
  - Depends on: T003
  - Files: `skills/spec-lifecycle-manager/scripts/spec_runtime.py`,
    `docs/reference/spec-lifecycle-runtime.md`
  - Acceptance: `spec_runtime.py archive-index .` emits deterministic JSON and
    command documentation is updated.
  - Evidence: `spec_runtime.py archive-index .` emits deterministic JSON with
    9 retained entries, 1 legacy gap, and 0 diagnostics; runtime reference
    docs updated.

- [x] T005 Expose archive index through MCP.
  - Depends on: T004
  - Files: `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`,
    `tests/runtime/test_spec_mcp_server.py`,
    `docs/reference/spec-lifecycle-runtime.md`
  - Acceptance: MCP exposes read-only archive index state through a tool or
    resource.
  - Evidence: MCP server exposes `archive_index` tool and
    `history://spec-archive-index` resource; MCP tests cover both surfaces.

## Phase 3: Validation And Close

- [x] T006 Validate archive index against current closed specs.
  - Depends on: T005
  - Files: `docs/history/spec-archive-index.md`,
    `docs/specs/011-spec-archive-index-runtime/verification.md`
  - Acceptance: Current archived specs are indexed without removing packages.
  - Evidence: Archive index validation reports 9 retained closed-spec entries,
    1 legacy gap for spec 001, and 0 diagnostics; no packages removed.

- [x] T007 Update roadmap and backlog disposition.
  - Depends on: T002
  - Files: `docs/backlog/README.md`, `docs/roadmap/README.md`
  - Acceptance: B003/R001 reflect implementation status and next work.
  - Evidence: B003 is promoted to spec 011 and R001 is the active roadmap item;
    later hook/governance/audit work remains deferred or proposed.

- [x] T008 Close spec 011.
  - Depends on: T006, T007
  - Files: `docs/specs/011-spec-archive-index-runtime/`,
    `docs/history/spec-closure-log.md`
  - Acceptance: Durable docs promoted, tests pass, closure log updated, and
    retained/removed package decision recorded.
  - Evidence: Final spec commit `4712010` recorded; package retained as
    historical; closure log and archive index updated with cleanup evidence
    pending this closure commit.

## Related Artifacts

- Requirements: [requirements.md](requirements.md)
- Design: [design.md](design.md)
- Traceability: [traceability.md](traceability.md)
- Verification: [verification.md](verification.md)
