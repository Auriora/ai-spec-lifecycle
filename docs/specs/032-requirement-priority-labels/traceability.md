---
title: Requirement priority labels traceability
doc_type: spec
artifact_type: traceability
status: draft
authoring_mode: wizard
lifecycle_stage: tasks
owner: platform
last_reviewed: 2026-07-06
backlog_item: B057
---

# Traceability Matrix

## Purpose

Map implementation tasks for spec 032 back to requirements, acceptance
criteria, design sections, correctness properties, validation, and durable
promotion targets. Use this matrix before implementing a task; if it drifts
from `requirements.md`, `design.md`, or `tasks.md`, reconcile it before coding.

## Task To Context Matrix

| Task ID | Requirements | Acceptance Criteria | Design Sections | Change Impact | Verification | Durable Targets | Open Decisions |
|---------|--------------|---------------------|-----------------|---------------|--------------|-----------------|----------------|
| T001 | Requirement 1, Requirement 2 | Requirement 1 AC1, AC2, AC3, AC4, AC5, AC6; Requirement 2 AC1, AC3 | `design.md#validation-strategy`, `design.md#error-handling` | embedded in `requirements.md#durable-impact` | `verification.md#quality-gates` | `tests/runtime/test_spec_runtime.py`, `tests/fixtures/requirement-priority-labels/` | none |
| T002 | Requirement 1, Requirement 3, Requirement 4 | Requirement 1 AC1, AC2, AC3, AC5, AC6; Requirement 3 AC4; Requirement 4 AC2 | `design.md#system-architecture`, `design.md#components-and-changes`, `design.md#function-signatures-and-interfaces` | embedded in `requirements.md#durable-impact` | `verification.md#quality-gates` | `skills/spec-lifecycle-manager/scripts/lifecycle/requirements.py`, `skills/spec-lifecycle-manager/scripts/lifecycle/core.py`, `skills/spec-lifecycle-manager/scripts/lifecycle/traceability.py` | none |
| T003 | Requirement 1, Requirement 2, Requirement 4 | Requirement 1 AC4, AC5; Requirement 2 AC1, AC3; Requirement 4 AC2 | `design.md#error-handling`, `design.md#algorithms-and-logic` | embedded in `requirements.md#durable-impact` | `verification.md#quality-gates` | `skills/spec-lifecycle-manager/scripts/lifecycle/core.py`, `tests/runtime/test_spec_runtime.py` | none |
| T004 | Requirement 1, Requirement 2 | Requirement 1 AC1-AC6; Requirement 2 AC1, AC3 | `design.md#validation-strategy` | embedded in `requirements.md#durable-impact` | `verification.md#evidence-log` | `verification.md` | none |
| T005 | Requirement 3 | Requirement 3 AC1, AC2, AC3, AC5 | `design.md#correctness-property-coverage`, `design.md#validation-strategy` | embedded in `requirements.md#durable-impact` | `verification.md#quality-gates` | `tests/runtime/test_spec_runtime.py`, `tests/fixtures/requirement-priority-labels/` | none |
| T006 | Requirement 3 | Requirement 3 AC1, AC2, AC3, AC5 | `design.md#algorithms-and-logic`, `design.md#function-signatures-and-interfaces` | embedded in `requirements.md#durable-impact` | `verification.md#quality-gates` | `skills/spec-lifecycle-manager/scripts/lifecycle/core.py` | none |
| T007 | Requirement 3, Requirement 4 | Requirement 3 AC1, AC2, AC3, AC4, AC5; Requirement 4 AC2 | `design.md#data-flow`, `design.md#function-signatures-and-interfaces` | embedded in `requirements.md#durable-impact` | `verification.md#quality-gates` | `skills/spec-lifecycle-manager/scripts/lifecycle/core.py`, `tests/runtime/test_spec_runtime.py` | none |
| T008 | Requirement 3 | Requirement 3 AC1, AC2, AC3, AC5 | `design.md#validation-strategy` | embedded in `requirements.md#durable-impact` | `verification.md#evidence-log` | `verification.md` | none |
| T009 | Requirement 3, Requirement 4 | Requirement 3 AC4; Requirement 4 AC2, AC4 | `design.md#validation-strategy`, `design.md#data-flow` | embedded in `requirements.md#durable-impact` | `verification.md#quality-gates` | `tests/runtime/test_spec_runtime.py`, `tests/runtime/test_spec_mcp_server.py`, `tests/fixtures/requirement-priority-labels/` | none |
| T010 | Requirement 3, Requirement 4 | Requirement 3 AC4; Requirement 4 AC2 | `design.md#components-and-changes`, `design.md#security-trust-and-access` | embedded in `requirements.md#durable-impact` | `verification.md#quality-gates` | `skills/spec-lifecycle-manager/scripts/lifecycle/traceability.py`, `skills/spec-lifecycle-manager/scripts/lifecycle/core.py`, `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py` | none |
| T011 | Requirement 3, Requirement 4 | Requirement 3 AC4; Requirement 4 AC2, AC4 | `design.md#validation-strategy` | embedded in `requirements.md#durable-impact` | `verification.md#evidence-log` | `verification.md` | none |
| T012 | Requirement 1, Requirement 2, Requirement 4 | Requirement 1 AC1-AC6; Requirement 2 AC2; Requirement 4 AC1 | `design.md#components-and-changes`, `design.md#migration-and-compatibility` | embedded in `requirements.md#durable-impact` | `verification.md#quality-gates` | `skills/spec-lifecycle-manager/references/spec-package/requirements.md`, `skills/spec-lifecycle-manager/references/spec-package/traceability.md` | none |
| T013 | Requirement 4 | Requirement 4 AC1, AC3 | `design.md#components-and-changes`, `design.md#migration-and-compatibility` | embedded in `requirements.md#durable-impact` | `verification.md#quality-gates` | `skills/spec-lifecycle-manager/prompts/documentation-wizard.json`, `skills/spec-lifecycle-manager/prompts/lint-spec.json`, `skills/spec-lifecycle-manager/SKILL.md` | none |
| T014 | Requirement 3, Requirement 4 | Requirement 3 AC1-AC5; Requirement 4 AC2 | `design.md#components-and-changes`, `design.md#operational-considerations` | embedded in `requirements.md#durable-impact` | `verification.md#quality-gates` | `docs/design/spec-lifecycle-management.md`, `docs/reference/spec-lifecycle-runtime.md` | none |
| T015 | Requirement 4 | Requirement 4 AC3 | `design.md#migration-and-compatibility`, `design.md#operational-considerations` | embedded in `requirements.md#durable-impact` | `verification.md#quality-gates` | `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/`, `plugins/spec-lifecycle-manager/claude-plugin/skills/spec-lifecycle-manager/` | none |
| T016 | Requirement 1, Requirement 2, Requirement 3, Requirement 4 | all acceptance criteria | `design.md#validation-strategy`, `design.md#downstream-task-guidance` | embedded in `requirements.md#durable-impact` | `verification.md#quality-gates`, `verification.md#evidence-log`, `verification.md#residual-risks` | `verification.md` | none |
| T017 | Requirement 4 | Requirement 4 AC3, AC4 | `design.md#validation-strategy`, `design.md#operational-considerations` | embedded in `requirements.md#durable-impact` | `verification.md#evidence-log` | `tests/`, `verification.md` | none |
| T018 | Requirement 1, Requirement 2, Requirement 3, Requirement 4 | all acceptance criteria | `design.md#slice-boundary-and-residual-architecture`, `design.md#operational-considerations` | embedded in `requirements.md#durable-impact` | `verification.md#residual-risks`, `verification.md#readiness-decision` | `docs/backlog/README.md`, durable docs listed in `requirements.md#durable-impact` | none |

## Requirement To Delivery Matrix

| Requirement | Priority | Acceptance Criteria | Design Sections | Tasks | Verification | Durable Targets | Coverage State | Residual Destination |
|-------------|----------|---------------------|-----------------|-------|--------------|-----------------|----------------|----------------------|
| Requirement 1 | must-have | AC1, AC2, AC3, AC4, AC5, AC6 | `design.md#overview`, `design.md#data-models`, `design.md#algorithms-and-logic`, `design.md#error-handling` | T001, T002, T003, T012, T016, T018 | `verification.md#quality-gates`, `verification.md#evidence-log` | requirements template, traceability template, parser tests | complete | none |
| Requirement 2 | must-have | AC1, AC2, AC3 | `design.md#migration-and-compatibility`, `design.md#error-handling` | T001, T003, T004, T012, T016, T018 | `verification.md#quality-gates`, `verification.md#evidence-log` | runtime lint, templates, historical validation behavior | complete | none |
| Requirement 3 | must-have | AC1, AC2, AC3, AC4, AC5 | `design.md#data-flow`, `design.md#algorithms-and-logic`, `design.md#function-signatures-and-interfaces`, `design.md#slice-boundary-and-residual-architecture` | T005, T006, T007, T008, T009, T010, T011, T014, T016, T018 | `verification.md#quality-gates`, `verification.md#evidence-log`, `verification.md#residual-risks` | runtime readiness, closure, traceability, agent context docs | complete | none |
| Requirement 4 | must-have | AC1, AC2, AC3, AC4 | `design.md#components-and-changes`, `design.md#validation-strategy`, `design.md#operational-considerations` | T009, T010, T011, T012, T013, T015, T016, T017, T018 | `verification.md#quality-gates`, `verification.md#evidence-log` | prompts, skill guidance, plugin bundles, package validation | complete | none |

## Correctness Property Coverage

| Property | Requirements | Design Sections | Tasks | Tests Or Verification | Residual Risk |
|----------|--------------|-----------------|-------|-----------------------|---------------|
| CP-001 | Requirement 2 | `design.md#correctness-property-coverage`, `design.md#error-handling` | T001, T003, T004, T016 | `verification.md#quality-gates`, `verification.md#correctness-property-coverage` | none |
| CP-002 | Requirement 3 | `design.md#correctness-property-coverage`, `design.md#algorithms-and-logic` | T005, T006, T007, T008, T016 | `verification.md#quality-gates`, `verification.md#correctness-property-coverage` | none |
| CP-003 | Requirement 3 | `design.md#correctness-property-coverage`, `design.md#algorithms-and-logic` | T005, T006, T007, T008, T016 | `verification.md#quality-gates`, `verification.md#correctness-property-coverage` | none |
| CP-004 | Requirement 3, Requirement 4 | `design.md#data-flow`, `design.md#function-signatures-and-interfaces` | T002, T007, T009, T010, T011, T016 | `verification.md#quality-gates`, `verification.md#correctness-property-coverage` | none |
| CP-005 | Requirement 1 | `design.md#data-models`, `design.md#function-signatures-and-interfaces` | T001, T002, T009, T010, T016 | `verification.md#quality-gates`, `verification.md#correctness-property-coverage` | none |

## Design To Implementation Matrix

| Design Section | Requirements | Tasks | Interfaces Or Files | Verification | Coverage State | Residual Destination |
|----------------|--------------|-------|---------------------|--------------|----------------|----------------------|
| `design.md#overview` | Requirement 1, Requirement 2, Requirement 3, Requirement 4 | T001-T018 | full implementation slice | `verification.md#evidence-log` | complete | none |
| `design.md#system-architecture` | Requirement 3, Requirement 4 | T002, T006, T007, T010, T015 | `lifecycle/core.py`, `lifecycle/traceability.py`, MCP server, plugin bundles | `verification.md#quality-gates` | complete | none |
| `design.md#components-and-changes` | Requirement 1, Requirement 3, Requirement 4 | T002, T006, T010, T012, T013, T014, T015 | parser, templates, prompts, skill docs, runtime docs, plugin bundles | `verification.md#quality-gates` | complete | none |
| `design.md#data-models` | Requirement 1, Requirement 3, Requirement 4 | T001, T002, T007, T009, T010 | requirement payloads with optional `priority` | `verification.md#quality-gates` | complete | none |
| `design.md#data-flow` | Requirement 3, Requirement 4 | T006, T007, T009, T010 | parser to readiness, closure, traceability, MCP payloads | `verification.md#quality-gates` | complete | none |
| `design.md#algorithms-and-logic` | Requirement 1, Requirement 3 | T001, T002, T005, T006, T007 | priority parser and coverage disposition helper | `verification.md#quality-gates` | complete | none |
| `design.md#function-signatures-and-interfaces` | Requirement 1, Requirement 3, Requirement 4 | T002, T006, T007, T009, T010 | shared parser helpers and coverage helper | `verification.md#quality-gates` | complete | none |
| `design.md#error-handling` | Requirement 1, Requirement 2 | T001, T003, T004 | lint diagnostics for shorthand, unknown, duplicate, and `won't-have` labels | `verification.md#evidence-log` | complete | none |
| `design.md#security-trust-and-access` | Requirement 4 | T010, T015, T017 | MCP direct shared runtime calls, plugin bundle parity | `verification.md#quality-gates` | complete | none |
| `design.md#migration-and-compatibility` | Requirement 2, Requirement 4 | T001, T003, T012, T013, T015, T017 | legacy fixtures, templates, prompts, plugin bundles | `verification.md#quality-gates` | complete | none |
| `design.md#slice-boundary-and-residual-architecture` | Requirement 3 | T006, T007, T018 | coverage disposition and closure routing | `verification.md#readiness-decision` | complete | none |
| `design.md#validation-strategy` | Requirement 1, Requirement 2, Requirement 3, Requirement 4 | T004, T008, T011, T016, T017 | verification artifact and validation commands | `verification.md#quality-gates`, `verification.md#evidence-log` | complete | none |
| `design.md#operational-considerations` | Requirement 4 | T014, T015, T017, T018 | docs, bundle parity, validation evidence | `verification.md#evidence-log`, `verification.md#readiness-decision` | complete | none |

## Open Decision Impact

| Decision ID | Blocks | Affected Requirements | Affected Tasks | Resolution Needed |
|-------------|--------|-----------------------|----------------|-------------------|
| none | none | none | none | Design records no open decisions. |

## Maintenance Notes

- Update this matrix whenever task IDs, design sections, verification gates, or
  durable promotion targets change.
- Keep priority values in this file aligned with parsed requirement source;
  task rows should not become the source of truth for priority.
- MoE review on 2026-07-06 confirmed that the `must-have` values in this matrix
  now match requirement-level priority metadata in `requirements.md`.
- Before closure, every `not-covered` row must become `complete`,
  `partial-routed`, `out-of-scope`, or rejected with one explicit residual
  destination.
- If implementation changes the shared parser or coverage helper shape, review
  all rows that reference `lifecycle/core.py`, `lifecycle/traceability.py`, or
  MCP payloads before continuing.
