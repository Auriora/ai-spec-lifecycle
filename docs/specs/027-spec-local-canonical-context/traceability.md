---
title: Spec-local canonical context traceability
doc_type: spec
artifact_type: traceability
status: active
owner: platform
last_reviewed: 2026-06-19
---

# Traceability Matrix

## Purpose

Map requirements, design sections, tasks, verification evidence, durable-doc
targets, and open decisions for the spec-local canonical context work.

## Task To Context Matrix

| Task ID | Requirements | Acceptance Criteria | Design Sections | Change Impact | Verification | Durable Targets | Open Decisions |
|---------|--------------|---------------------|-----------------|---------------|--------------|-----------------|----------------|
| T001 | Requirement 1, Requirement 2, Requirement 3, Requirement 6 | R1 AC1-AC4, R2 AC1-AC4, R3 AC1-AC4, R6 AC1-AC4 | `design.md#data-models`, `design.md#open-questions` | `change-impact.md#open-questions` | `verification.md#quality-gates` | `skills/spec-lifecycle-manager/references/spec-package/` | D001 resolved 2026-07-02; D002 resolved 2026-07-02 |
| T002 | Requirement 1, Requirement 2, Requirement 4, Requirement 5 | R1 AC1-AC4, R2 AC1-AC4, R4 AC1-AC4, R5 AC1-AC4 | `design.md#system-architecture`, `design.md#components-and-changes` | `change-impact.md#proposed-changes` | `verification.md#validation-commands` | `docs/design/spec-lifecycle-management.md`, `docs/design/coding-agent-operating-model.md` | D001 |
| T003 | Requirement 1, Requirement 2, Requirement 3, Requirement 4, Requirement 5 | R1 AC1-AC4, R2 AC1-AC4, R3 AC1-AC4, R4 AC1-AC4, R5 AC1-AC4 | `design.md#low-level-design`, `design.md#security-trust-and-access` | `change-impact.md#proposed-changes` | `verification.md#validation-commands` | `skills/spec-lifecycle-manager/SKILL.md` | D001, D002 |
| T004 | Requirement 1, Requirement 2, Requirement 3, Requirement 6 | R1 AC1-AC4, R2 AC1-AC2, R3 AC1-AC4, R6 AC1-AC2, R6 AC4 | `design.md#data-models`, `design.md#migration-and-compatibility` | `change-impact.md#promotion-targets` | `verification.md#validation-commands` | `skills/spec-lifecycle-manager/references/spec-package/` | D001 |
| T005 | Requirement 1, Requirement 3, Requirement 4, Requirement 6, Requirement 7 | R1 AC1-AC4, R3 AC1-AC4, R4 AC1-AC4, R6 AC1-AC4, R7 AC1-AC4 | `design.md#components-and-changes`, `design.md#data-flow`, `design.md#downstream-task-guidance` | `change-impact.md#proposed-changes` | `verification.md#validation-commands`, `verification.md#correctness-property-coverage` | `skills/spec-lifecycle-manager/prompts/`, `skills/spec-lifecycle-manager/SKILL.md` | D001 |
| T006 | Requirement 1, Requirement 3, Requirement 4, Requirement 5, Requirement 6, Requirement 7 | R1 AC4, R3 AC1-AC4, R4 AC1-AC4, R5 AC1-AC4, R6 AC3-AC4, R7 AC1-AC4 | `design.md#algorithms-and-logic`, `design.md#function-signatures-and-interfaces`, `design.md#error-handling` | `change-impact.md#proposed-changes` | `verification.md#validation-commands`, `verification.md#correctness-property-coverage` | `skills/spec-lifecycle-manager/scripts/spec_runtime.py`, `tests/runtime/`, `tests/fixtures/` | D002 |
| T007 | Requirement 4, Requirement 5, Requirement 6, Requirement 7 | R4 AC1-AC4, R5 AC1-AC4, R6 AC1-AC4, R7 AC1-AC4 | `design.md#migration-and-compatibility`, `design.md#validation-strategy` | `change-impact.md#promotion-targets` | `verification.md#durable-promotion-and-cleanup` | `docs/reference/spec-lifecycle-runtime.md`, `skills/spec-lifecycle-manager/references/migration-guide.md` | D001, D002 |
| T008 | Requirement 7 | R7 AC1-AC4 | `design.md#data-flow`, `design.md#validation-strategy` | `change-impact.md#bug-fix-details` | `verification.md#manual-or-external-verification` | `docs/specs/027-spec-local-canonical-context/verification.md` | none |
| T009 | Requirement 1, Requirement 2, Requirement 3, Requirement 4, Requirement 5, Requirement 6, Requirement 7 | all acceptance criteria | `design.md#validation-strategy`, `design.md#operational-considerations` | `change-impact.md#promotion-targets` | `verification.md#readiness-decision` | `docs/history/spec-closure-log.md`, `docs/history/spec-archive-index.md` | none |

## Requirement To Delivery Matrix

| Requirement | Acceptance Criteria | Design Sections | Tasks | Verification | Durable Targets |
|-------------|---------------------|-----------------|-------|--------------|-----------------|
| Requirement 1 | AC1-AC4 | `design.md#system-architecture`, `design.md#data-flow` | T001, T002, T003, T004, T005, T006, T009 | lint/readiness tests, scan, manual review | `docs/design/spec-lifecycle-management.md`, `skills/spec-lifecycle-manager/SKILL.md`, templates |
| Requirement 2 | AC1-AC4 | `design.md#system-architecture`, `design.md#security-trust-and-access` | T001, T002, T003, T004, T009 | docs review, lint/readiness tests | `docs/design/spec-lifecycle-management.md`, `docs/design/coding-agent-operating-model.md`, skill guidance |
| Requirement 3 | AC1-AC4 | `design.md#data-models`, `design.md#algorithms-and-logic` | T001, T003, T004, T005, T006, T009 | runtime fixture or manual template review | templates, runtime docs |
| Requirement 4 | AC1-AC4 | `design.md#data-flow`, `design.md#function-signatures-and-interfaces` | T002, T003, T005, T006, T007, T009 | readiness/task-context diagnostics | skill guidance, runtime reference |
| Requirement 5 | AC1-AC4 | `design.md#data-flow`, `design.md#validation-strategy` | T002, T003, T006, T007, T009 | closure-check or promotion-plan evidence | lifecycle design, skill guidance, runtime reference |
| Requirement 6 | AC1-AC4 | `design.md#components-and-changes`, `design.md#migration-and-compatibility` | T001, T004, T005, T006, T007, T009 | unit tests, scan, package lint, prompt validation if needed | templates, runtime, migration guide |
| Requirement 7 | AC1-AC4 | `design.md#data-flow`, `design.md#algorithms-and-logic`, `design.md#downstream-task-guidance` | T005, T006, T007, T008, T009 | prompt/runtime fixture and dogfood scenario | prompts, skill guidance, runtime reference |

## Correctness Property Coverage

| Property | Requirements | Design Sections | Tasks | Tests Or Verification | Residual Risk |
|----------|--------------|-----------------|-------|-----------------------|---------------|
| CP-001 | Requirement 2 | `design.md#system-architecture`, `design.md#security-trust-and-access` | T002, T003, T005 | Unit test or focused docs review | Runtime may not fully prove policy semantics. |
| CP-002 | Requirement 3 | `design.md#data-models`, `design.md#algorithms-and-logic` | T004, T005 | Runtime lint fixture or template review | Table parsing can be incremental. |
| CP-003 | Requirement 5 | `design.md#data-flow`, `design.md#validation-strategy` | T006, T007, T009 | Closure-check fixture or manual closure review | Initial severity may be warning before closure. |
| CP-004 | Requirement 1, Requirement 4 | `design.md#data-flow`, `design.md#function-signatures-and-interfaces` | T003, T005, T006, T009 | Readiness/task-context fixture or manual review | Requires careful wording to avoid overloading small specs. |
| CP-005 | Requirement 7 | `design.md#data-flow`, `design.md#algorithms-and-logic` | T005, T006, T008, T009 | Prompt/runtime fixture and dogfood scenario | Automatic copying may remain preview-first. |

## Design To Implementation Matrix

| Design Section | Requirements | Tasks | Interfaces Or Files | Verification |
|----------------|--------------|-------|---------------------|--------------|
| `design.md#system-architecture` | Requirement 1, Requirement 2 | T002, T003 | lifecycle design docs, skill guidance | docs review, package lint |
| `design.md#data-models` | Requirement 3, Requirement 6 | T001, T004, T006 | template files, runtime parser/checks | template review, runtime tests |
| `design.md#algorithms-and-logic` | Requirement 1, Requirement 3, Requirement 5, Requirement 6, Requirement 7 | T005, T006 | `spec_runtime.py`, prompts | unit tests, prompt validation |
| `design.md#security-trust-and-access` | Requirement 2 | T002, T003, T006 | design docs, skill guidance | docs review |
| `design.md#migration-and-compatibility` | Requirement 6, Requirement 7 | T004, T007 | migration guide, runtime reference | scan, lint, unit tests |

## Open Decision Impact

| Decision ID | Blocks | Affected Requirements | Affected Tasks | Resolution Needed |
|-------------|--------|-----------------------|----------------|-------------------|
| D001 | Template and creation-flow implementation | Requirement 1, Requirement 3, Requirement 6, Requirement 7 | T001, T004, T005, T007 | Resolved 2026-07-02: add optional `canonical-context.md` template and allow embedded sections for small packages. |
| D002 | Runtime severity and closure behavior | Requirement 5, Requirement 6 | T001, T006, T007 | Resolved 2026-07-02: warn during authoring/readiness and block closure for accepted required canonical content without destination, route, or discard rationale. |

## Maintenance Notes

- Update this matrix when task IDs, target files, diagnostic scope, or template
  shape changes.
- D001 and D002 were resolved before implementing T004-T007; keep future
  changes aligned with those decisions.
- Keep authority hierarchy changes aligned with `AGENTS.md` and governance
  instructions.
