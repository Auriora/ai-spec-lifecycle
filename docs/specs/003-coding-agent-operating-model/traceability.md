---
title: Coding agent operating model traceability
doc_type: spec
artifact_type: traceability
status: archived
owner: platform
last_reviewed: 2026-06-06
---

# Traceability Matrix

## Task To Context Matrix

| Task ID | Requirements | Acceptance Criteria | Design Sections | Change Impact | Verification | Durable Targets | Open Decisions |
|---------|--------------|---------------------|-----------------|---------------|--------------|-----------------|----------------|
| T001 | Requirement 1, Requirement 4, Requirement 5 | Requirement 1 AC1, AC2, AC3; Requirement 4 AC1; Requirement 5 AC1 | `design.md#workflow-levels`, `design.md#agent-roles` | none | `verification.md#evidence-log` | `docs/reference/coding-agent-workflow-research.md` | none |
| T002 | Requirement 1, Requirement 2, Requirement 3, Requirement 4, Requirement 5 | all acceptance criteria | `design.md#overview` | none | `verification.md#task-evidence` | `docs/specs/003-coding-agent-operating-model/` | none |
| T003 | Requirement 1, Requirement 2, Requirement 3, Requirement 4 | Requirement 1 AC1, AC2, AC3; Requirement 2 AC1, AC2; Requirement 3 AC1, AC2, AC3; Requirement 4 AC1, AC2, AC3 | `design.md#workflow-levels`, `design.md#decision-gates`, `design.md#evidence-rules`, `design.md#parallelism-rules` | none | `verification.md#evidence-log` | `docs/design/coding-agent-operating-model.md` | none |
| T004 | Requirement 5 | Requirement 5 AC1, AC2, AC3 | `design.md#metrics` | none | `verification.md#requirement-coverage` | `docs/design/coding-agent-operating-model.md` | none |
| T005 | Requirement 2 | Requirement 2 AC1, AC2, AC3 | `design.md#durable-documentation-boundary` | none | `verification.md#durable-promotion-and-cleanup` | `docs/design/coding-agent-operating-model.md` | none |
| T006 | Requirement 1, Requirement 3, Requirement 5 | Requirement 1 AC1, AC2, AC3; Requirement 3 AC1, AC2, AC3; Requirement 5 AC1, AC2, AC3 | `design.md#dogfood-decision` | none | `verification.md#evidence-log` | `docs/design/coding-agent-operating-model.md` | none |

## Requirement To Delivery Matrix

| Requirement | Acceptance Criteria | Design Sections | Tasks | Verification | Durable Targets |
|-------------|---------------------|-----------------|-------|--------------|-----------------|
| Requirement 1 | AC1, AC2, AC3 | workflow levels and decision gates | T001, T002, T003, T006 | `verification.md#requirement-coverage` | durable operating model |
| Requirement 2 | AC1, AC2, AC3 | durable documentation boundary | T002, T003, T005 | `verification.md#durable-promotion-and-cleanup` | durable operating model |
| Requirement 3 | AC1, AC2, AC3 | evidence rules | T002, T003, T006 | `verification.md#requirement-coverage` | durable operating model |
| Requirement 4 | AC1, AC2, AC3 | agent roles and parallelism rules | T001, T002, T003 | `verification.md#requirement-coverage` | durable operating model |
| Requirement 5 | AC1, AC2, AC3 | metrics and dogfood decision | T001, T002, T004, T006 | `verification.md#requirement-coverage` | durable operating model |

## Design To Implementation Matrix

| Design Section | Requirements | Tasks | Interfaces Or Files | Verification |
|----------------|--------------|-------|---------------------|--------------|
| `design.md#overview` | Requirement 1, Requirement 2, Requirement 3, Requirement 4, Requirement 5 | T002 | spec package | spec lint |
| `design.md#workflow-levels` | Requirement 1 | T003 | durable design | requirement coverage |
| `design.md#decision-gates` | Requirement 1, Requirement 2 | T003 | durable design | evidence log |
| `design.md#evidence-rules` | Requirement 3 | T003, T006 | durable design | task evidence |
| `design.md#parallelism-rules` | Requirement 4 | T003 | durable design | requirement coverage |
| `design.md#metrics` | Requirement 5 | T004 | durable design | requirement coverage |
| `design.md#durable-documentation-boundary` | Requirement 2 | T005 | durable design | durable promotion |
| `design.md#dogfood-decision` | Requirement 1, Requirement 3, Requirement 5 | T006 | durable design | evidence log |

## Open Decision Impact

| Decision ID | Blocks | Affected Requirements | Affected Tasks | Resolution Needed |
|-------------|--------|-----------------------|----------------|-------------------|
| none | none | none | none | none |
