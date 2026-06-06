---
title: Backlog and roadmap templates traceability
doc_type: spec
artifact_type: traceability
status: archived
owner: platform
last_reviewed: 2026-06-05
---

# Traceability Matrix

## Purpose

Map backlog and roadmap template tasks to requirements, design sections,
verification evidence, durable targets, and open decisions.

## Task To Context Matrix

| Task ID | Requirements | Acceptance Criteria | Design Sections | Change Impact | Verification | Durable Targets | Open Decisions |
|---------|--------------|---------------------|-----------------|---------------|--------------|-----------------|----------------|
| T001 | Requirement 4 | Requirement 4 AC3 | `design.md#overview` | none | `verification.md#task-evidence` | `docs/specs/006-backlog-roadmap-templates/` | none |
| T002 | Requirement 1 | Requirement 1 AC1, AC2, AC3 | `design.md#data-models` | none | `verification.md#task-evidence` | `skills/spec-lifecycle-manager/references/durable-doc-templates/backlog.md` | none |
| T003 | Requirement 2 | Requirement 2 AC1, AC2, AC3 | `design.md#data-models` | none | `verification.md#task-evidence` | `skills/spec-lifecycle-manager/references/durable-doc-templates/roadmap.md` | none |
| T004 | Requirement 1, Requirement 2, Requirement 3 | Requirement 1 AC1; Requirement 2 AC1; Requirement 3 AC1, AC2, AC3 | `design.md#components-and-changes`, `design.md#data-flow` | none | `verification.md#task-evidence` | `skills/spec-lifecycle-manager/references/durable-doc-templates/README.md`, `skills/spec-lifecycle-manager/references/document-routing-and-expert-review.md` | none |
| T005 | Requirement 3, Requirement 4 | Requirement 3 AC1, AC2, AC3; Requirement 4 AC1 | `design.md#algorithms-and-logic` | none | `verification.md#task-evidence` | `skills/spec-lifecycle-manager/SKILL.md` | none |
| T006 | Requirement 3, Requirement 4 | Requirement 3 AC1, AC2, AC3; Requirement 4 AC2, AC3 | `design.md#components-and-changes`, `design.md#migration-and-compatibility` | none | `verification.md#task-evidence` | `docs/design/spec-lifecycle-management.md`, `docs/README.md`, `docs/backlog/README.md` | none |
| T007 | Requirement 4 | Requirement 4 AC1, AC2, AC3 | `design.md#validation-strategy` | none | `verification.md#evidence-log` | `docs/specs/006-backlog-roadmap-templates/verification.md` | none |

## Requirement To Delivery Matrix

| Requirement | Acceptance Criteria | Design Sections | Tasks | Verification | Durable Targets |
|-------------|---------------------|-----------------|-------|--------------|-----------------|
| Requirement 1 | AC1, AC2, AC3 | `design.md#data-models` | T002, T004 | `verification.md#requirement-coverage` | `skills/spec-lifecycle-manager/references/durable-doc-templates/backlog.md` |
| Requirement 2 | AC1, AC2, AC3 | `design.md#data-models` | T003, T004 | `verification.md#requirement-coverage` | `skills/spec-lifecycle-manager/references/durable-doc-templates/roadmap.md` |
| Requirement 3 | AC1, AC2, AC3 | `design.md#data-flow`, `design.md#algorithms-and-logic` | T004, T005, T006 | `verification.md#requirement-coverage` | `skills/spec-lifecycle-manager/SKILL.md`, `docs/design/spec-lifecycle-management.md` |
| Requirement 4 | AC1, AC2, AC3 | `design.md#components-and-changes`, `design.md#validation-strategy` | T001, T005, T006, T007 | `verification.md#requirement-coverage` | `docs/backlog/README.md`, `docs/README.md` |

## Design To Implementation Matrix

| Design Section | Requirements | Tasks | Interfaces Or Files | Verification |
|----------------|--------------|-------|---------------------|--------------|
| `design.md#overview` | Requirement 4 | T001 | `docs/specs/006-backlog-roadmap-templates/` | `verification.md#task-evidence` |
| `design.md#components-and-changes` | Requirement 1, Requirement 2, Requirement 4 | T002, T003, T004, T006 | durable template README, routing reference, lifecycle docs, docs index | `verification.md#task-evidence` |
| `design.md#data-models` | Requirement 1, Requirement 2 | T002, T003 | `backlog.md`, `roadmap.md` | `verification.md#requirement-coverage` |
| `design.md#data-flow` | Requirement 3 | T004, T005, T006 | `SKILL.md`, lifecycle design | `verification.md#requirement-coverage` |
| `design.md#algorithms-and-logic` | Requirement 3 | T005 | `SKILL.md` | `verification.md#task-evidence` |
| `design.md#validation-strategy` | Requirement 4 | T007 | `verification.md` | `verification.md#evidence-log` |

## Open Decision Impact

| Decision ID | Blocks | Affected Requirements | Affected Tasks | Resolution Needed |
|-------------|--------|-----------------------|----------------|-------------------|
| none | none | none | none | none |
