---
title: Archived spec scan hygiene tasks
doc_type: spec
artifact_type: tasks
status: draft
owner: platform
last_reviewed: 2026-06-06
---

# Tasks

**Input**: `docs/reference/spec-lifecycle-runtime.md`,
`docs/design/spec-lifecycle-management.md`,
`skills/spec-lifecycle-manager/scripts/spec_runtime.py`, and
`tests/runtime/`.

## Task Dependency Graph

```text
T001 -> T002
T002 -> T003
T003 -> T004
T004 -> T005
T005 -> T006
```

## Phase 1: Spec And Runtime

- [x] T001 Create archived scan hygiene spec.
  - Depends on: none
  - Files: `docs/specs/009-archived-spec-scan-hygiene/`
  - Acceptance: Spec package defines requirements, design, tasks,
    traceability, and verification for archived scan hygiene.
  - Evidence: Spec package created.

- [x] T002 Add archived lifecycle scan semantics.
  - Depends on: T001
  - Files: `skills/spec-lifecycle-manager/scripts/spec_runtime.py`
  - Acceptance: Default scan keeps archived packages in inventory while
    skipping authoring lint and reporting active/archived summary counts.
  - Evidence: Runtime adds lifecycle classification, skipped archived health,
    and scan summary.

- [x] T003 Add explicit archived audit option.
  - Depends on: T002
  - Files: `skills/spec-lifecycle-manager/scripts/spec_runtime.py`,
    `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`
  - Acceptance: CLI and MCP scan callers can opt into linting archived
    packages; direct lint remains strict.
  - Evidence: CLI `--include-archived-lint` and MCP `include_archived_lint`
    argument added.

## Phase 2: Tests And Docs

- [x] T004 Add regression tests.
  - Depends on: T003
  - Files: `tests/runtime/test_spec_runtime.py`,
    `tests/runtime/test_spec_mcp_server.py`
  - Acceptance: Tests cover default archived skip, archived audit mode, CLI
    flag behavior, and MCP option exposure.
  - Evidence: Runtime and MCP tests updated.

- [x] T005 Promote durable docs.
  - Depends on: T004
  - Files: `docs/reference/spec-lifecycle-runtime.md`,
    `docs/design/spec-lifecycle-management.md`
  - Acceptance: Durable docs describe active-health scan semantics, audit
    option, and historical package migration guidance.
  - Evidence: Runtime reference and lifecycle design updated.

- [x] T006 Validate and sync installed skill.
  - Depends on: T005
  - Files: `docs/specs/009-archived-spec-scan-hygiene/verification.md`,
    `~/.codex/skills/spec-lifecycle-manager/`
  - Acceptance: Tests, spec lint, closure check, diff check, and installed
    skill sync complete.
  - Evidence: Verification record captures command results after validation.

## Related Artifacts

- Requirements: requirements.md
- Design: design.md
- Traceability: traceability.md
- Verification: verification.md
