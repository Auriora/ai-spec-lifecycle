---
title: Operating model governance adoption traceability
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
| T001 | Requirement 1, Requirement 2, Requirement 3 | all acceptance criteria | `design.md#overview` | create spec | `verification.md#quality-gates` | spec package | none |
| T002 | Requirement 1, Requirement 2, Requirement 3 | Requirement 1 AC1, AC2, AC3; Requirement 2 AC1, AC2, AC3; Requirement 3 AC1, AC2, AC3 | `design.md#governance-additions`, `design.md#constitution-patch` | governance update | `verification.md#task-evidence` | `docs/governance/constitution.md` | none |
| T003 | Requirement 1 | Requirement 1 AC1, AC2, AC3 | `design.md#design-doc-update`, `design.md#non-adopted-guidance` | design clarify | `verification.md#task-evidence` | `docs/design/coding-agent-operating-model.md` | none |
| T004 | Requirement 1 | Requirement 1 AC1 | `design.md#planning-updates` | planning update | `verification.md#task-evidence` | `docs/roadmap/README.md`, `docs/backlog/README.md` | none |
| T005 | Requirement 1, Requirement 2, Requirement 3 | all acceptance criteria | `design.md#operational-considerations` | validation | `verification.md#validation-commands` | `docs/specs/012-operating-model-governance-adoption/verification.md` | none |
| T006 | Requirement 1, Requirement 2, Requirement 3 | all acceptance criteria | `design.md#operational-considerations` | close spec | `verification.md#readiness-decision` | `docs/history/spec-closure-log.md`, `docs/history/spec-archive-index.md` | none |

## Requirement To Delivery Matrix

| Requirement | Acceptance Criteria | Design Sections | Tasks | Verification | Durable Targets |
|-------------|---------------------|-----------------|-------|--------------|-----------------|
| Requirement 1 | AC1, AC2, AC3 | governance additions, design doc update, non-adopted guidance | T001, T002, T003, T004, T005, T006 | quality gates | constitution, operating model, planning docs |
| Requirement 2 | AC1, AC2, AC3 | governance additions, constitution patch | T001, T002, T005, T006 | task evidence | constitution |
| Requirement 3 | AC1, AC2, AC3 | governance additions, constitution patch | T001, T002, T005, T006 | validation commands | constitution |

## Design To Implementation Matrix

| Design Section | Requirements | Tasks | Interfaces Or Files | Verification |
|----------------|--------------|-------|---------------------|--------------|
| `design.md#overview` | Requirement 1 | T001 | spec package | spec lint |
| `design.md#governance-additions` | Requirement 1, Requirement 2, Requirement 3 | T002 | constitution | task evidence |
| `design.md#design-doc-update` | Requirement 1 | T003 | operating-model design | task evidence |
| `design.md#planning-updates` | Requirement 1 | T004 | backlog, roadmap | task evidence |
| `design.md#constitution-patch` | Requirement 2, Requirement 3 | T002 | constitution | task evidence |
| `design.md#non-adopted-guidance` | Requirement 1 | T003 | operating-model design | task evidence |
| `design.md#operational-considerations` | Requirement 1, Requirement 2, Requirement 3 | T005, T006 | verification, closure log, archive index | validation commands |

## Open Decision Impact

| Decision ID | Blocks | Affected Requirements | Affected Tasks | Resolution Needed |
|-------------|--------|-----------------------|----------------|-------------------|
| none | none | none | none | none |
