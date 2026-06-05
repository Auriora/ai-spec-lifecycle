---
title: Feature traceability matrix title
doc_type: spec
artifact_type: traceability
status: draft
owner: team-or-person
last_reviewed: YYYY-MM-DD
---

# Traceability Matrix

## Purpose

Map requirements, design sections, tasks, verification evidence, durable-doc
targets, and open decisions in both directions. Use this file when a package is
large enough that agents may miss relevant context by reading `tasks.md` alone.

Before implementing a task, review the row for that task ID and the linked
requirement/design rows. If this matrix is stale or incomplete, reconcile it
against the full spec package before coding.

## Task To Context Matrix

| Task ID | Requirements | Acceptance Criteria | Design Sections | Change Impact | Verification | Durable Targets | Open Decisions |
|---------|--------------|---------------------|-----------------|---------------|--------------|-----------------|----------------|
| T001 | Requirement 1 | AC1, AC2 | `design.md#section` | `change-impact.md#delta` or none | `verification.md#gate` | `docs/path.md` or TBD | D001 or none |

## Requirement To Delivery Matrix

| Requirement | Acceptance Criteria | Design Sections | Tasks | Verification | Durable Targets |
|-------------|---------------------|-----------------|-------|--------------|-----------------|
| Requirement 1 | AC1, AC2 | `design.md#section` | T001, T002 | `verification.md#gate` | `docs/path.md` |

## Design To Implementation Matrix

| Design Section | Requirements | Tasks | Interfaces Or Files | Verification |
|----------------|--------------|-------|---------------------|--------------|
| `design.md#section` | Requirement 1 | T001 | `src/path`, `tests/path` | Test, command, or review |

## Open Decision Impact

| Decision ID | Blocks | Affected Requirements | Affected Tasks | Resolution Needed |
|-------------|--------|-----------------------|----------------|-------------------|
| D001 | Design, implementation, verification, or closure | Requirement 1 | T001 | Decision needed |

## Maintenance Notes

- Update this matrix when requirements, design sections, task IDs, verification
  gates, durable targets, or open decisions change.
- Keep entries specific enough that an agent can start from a task ID and find
  the relevant specification context before implementation.
- If a row cannot be completed, record `TBD` and the blocker rather than
  leaving the relationship implicit.
