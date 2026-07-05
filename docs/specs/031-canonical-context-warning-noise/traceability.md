---
title: Canonical context warning noise traceability
doc_type: spec
artifact_type: traceability
status: draft
owner: platform
last_reviewed: 2026-07-05
---

# Traceability Matrix

## Purpose

Map spec 031 requirements, design sections, tasks, verification evidence, and
durable targets. Before implementing a task, use MCP `traceability_lookup` when
available, then verify linked requirements and design sections directly.

## Task To Context Matrix

| Task ID | Requirements | Acceptance Criteria | Design Sections | Change Impact | Verification | Durable Targets | Open Decisions |
|---------|--------------|---------------------|-----------------|---------------|--------------|-----------------|----------------|
| T001 | Requirement 1 | R1 AC1 | `design.md#data-models`, `design.md#algorithms-and-logic` | none | Runtime test evidence | none | none |
| T002 | Requirement 1, Requirement 2 | R1 AC2; R2 AC1 | `design.md#data-models` | none | Runtime test evidence | none | none |
| T003 | Requirement 2 | R2 AC2, AC3 | `design.md#algorithms-and-logic` | none | Runtime test evidence | none | none |
| T004 | Requirement 3 | R3 AC1 | `design.md#algorithms-and-logic` | none | Risk-signal test evidence | none | none |
| T005 | Requirement 1, Requirement 3 | R1 AC3; R3 AC1 | `design.md#algorithms-and-logic` | none | Risk-signal test evidence | none | none |
| T006 | Requirement 3 | R3 AC2 | `design.md#algorithms-and-logic` | none | Risk-signal test evidence | none | none |
| T007 | Requirement 3 | R3 AC2 | `design.md#algorithms-and-logic` | none | Risk-signal test evidence | none | none |
| T008 | Requirement 3 | R3 AC2 | `design.md#algorithms-and-logic` | none | Risk-signal test evidence | none | none |
| T009 | Requirement 3 | R3 AC3 | `design.md#error-handling` | none | Risk-signal test evidence | none | none |
| T010 | Requirement 5 | R5 AC2 | `design.md#data-flow` | none | Readiness test evidence | none | none |
| T011 | Requirement 5 | R5 AC3 | `design.md#data-flow` | none | Closure test evidence | none | none |
| T012 | Requirement 5 | R5 AC4 | `design.md#system-architecture` | none | MCP parity test evidence | none | none |
| T013 | Requirements 1-5 | All tested ACs | `design.md#validation-strategy` | none | Focused test checkpoint | none | none |
| T014 | Requirement 2, Requirement 3 | R2 AC1; R3 AC2-AC3 | `design.md#function-signatures-and-interfaces` | none | Runtime tests | none | none |
| T015 | Requirement 5 | R5 AC4 | `design.md#function-signatures-and-interfaces` | none | Runtime tests | none | none |
| T016 | Requirement 3 | R3 AC1 | `design.md#algorithms-and-logic` | none | T004, T005 | none | none |
| T017 | Requirement 1, Requirement 3 | R1 AC3; R3 AC1 | `design.md#algorithms-and-logic` | none | T005 | none | none |
| T018 | Requirement 3 | R3 AC3 | `design.md#error-handling` | none | T009 | none | none |
| T019 | Requirement 1, Requirement 2 | R1 AC1-AC2; R2 AC1 | `design.md#data-models` | none | T001, T002 | none | none |
| T020 | Requirement 5 | R5 AC2 | `design.md#data-flow` | none | T010 | none | none |
| T021 | Requirement 5 | R5 AC3 | `design.md#data-flow` | none | T011 | none | none |
| T022 | Requirement 4 | R4 AC1 | `design.md#components-and-changes` | none | Text review | `skills/spec-lifecycle-manager/SKILL.md` | none |
| T023 | Requirement 4 | R4 AC1 | `design.md#components-and-changes` | none | Prompt validation | `skills/spec-lifecycle-manager/prompts/` | none |
| T024 | Requirement 4 | R4 AC2 | `design.md#components-and-changes` | none | Template review | `skills/spec-lifecycle-manager/references/spec-package/` | none |
| T025 | Requirement 4, Requirement 5 | R4 AC1; R5 AC1-AC3 | `design.md#operational-considerations` | none | Durable-doc review | `docs/design/spec-lifecycle-management.md`; `docs/reference/spec-lifecycle-runtime.md` | none |
| T026 | Requirement 4 | R4 AC3 | `design.md#operational-considerations` | none | Backlog review | `docs/backlog/README.md` | none |
| T027 | Requirement 4 | R4 AC3 | `design.md#migration-and-compatibility` | none | Package-contract and sync-guard | Codex plugin bundle | none |
| T028 | Requirement 4 | R4 AC3 | `design.md#migration-and-compatibility` | none | Package-contract and sync-guard | Claude plugin bundle | none |
| T029 | Requirement 4, Requirement 5 | R4 AC3; R5 AC4 | `design.md#validation-strategy` | none | Prompt/package checkpoint | Source and bundle paths | none |
| T030 | Requirements 1-5 | All ACs | `design.md#validation-strategy` | none | Verification artifact | `verification.md` | none |
| T031 | Requirements 1-5 | All ACs | `design.md#validation-strategy` | none | Final validation bundle | Source, tests, bundles | none |
| T032 | Requirements 1-5 | Closure readiness | `design.md#slice-boundary-and-residual-architecture` | none | Closure-check and review evidence | Spec package | none |

## Requirement To Delivery Matrix

| Requirement | Acceptance Criteria | Design Sections | Tasks | Verification | Durable Targets | Coverage State | Residual Destination |
|-------------|---------------------|-----------------|-------|--------------|-----------------|----------------|----------------------|
| Requirement 1: Advisory Diagnostic Wording | AC1, AC2, AC3 | `design.md#data-models`, `design.md#algorithms-and-logic` | T001, T002, T005, T017, T019, T030, T031, T032 | Runtime tests and verification artifact | Runtime reference, skill, prompts | complete | none |
| Requirement 2: Canonical Context Creation Conditions | AC1, AC2, AC3 | `design.md#data-models`, `design.md#algorithms-and-logic` | T002, T003, T014, T019, T030, T031, T032 | Runtime tests and verification artifact | Skill and templates | complete | none |
| Requirement 3: Risk Signal Precision | AC1, AC2, AC3 | `design.md#algorithms-and-logic`, `design.md#error-handling` | T004, T005, T006, T007, T008, T009, T014, T016, T017, T018, T030, T031, T032 | Risk-signal tests and verification artifact | Runtime reference | complete | none |
| Requirement 4: Prompt And Template Alignment | AC1, AC2, AC3 | `design.md#components-and-changes`, `design.md#migration-and-compatibility` | T022, T023, T024, T025, T026, T027, T028, T029, T030, T031, T032 | Prompt validation, package-contract, sync-guard | Skill, prompts, templates, durable docs, bundles | complete | none |
| Requirement 5: Runtime Surface Alignment | AC1, AC2, AC3, AC4 | `design.md#system-architecture`, `design.md#data-flow`, `design.md#function-signatures-and-interfaces` | T010, T011, T012, T015, T020, T021, T025, T029, T030, T031, T032 | Readiness, closure, MCP parity, package checks | Runtime reference and bundles | complete | none |

## Correctness Property Coverage

| Property | Requirements | Design Sections | Tasks | Tests Or Verification | Residual Risk |
|----------|--------------|-----------------|-------|-----------------------|---------------|
| CP-001 | Requirement 1, Requirement 4 | `design.md#data-models`, `design.md#algorithms-and-logic` | T001, T002, T003, T009, T011, T019, T022, T023, T024, T030, T031 | Runtime tests assert warning/advisory/non-blocking metadata; prompt/template checks verify wording. | none |
| CP-002 | Requirement 1, Requirement 3 | `design.md#algorithms-and-logic` | T005, T017, T030, T031 | Historical-reference regression tests. | Archived inventory-specific behavior may need MCP coverage if runtime fixtures are insufficient. |
| CP-003 | Requirement 3 | `design.md#algorithms-and-logic` | T004, T005, T016, T030, T031 | Promotion, closure, and archive false-positive tests. | none |
| CP-004 | Requirement 2, Requirement 3 | `design.md#algorithms-and-logic`, `design.md#error-handling` | T006, T007, T008, T009, T014, T018, T030, T031 | Positive detection and ambiguous review-confidence tests. | Heuristics may still miss novel phrasing; record in verification if observed. |
| CP-005 | Requirement 4, Requirement 5 | `design.md#system-architecture`, `design.md#data-flow`, `design.md#migration-and-compatibility` | T010, T011, T012, T015, T020, T021, T025, T027, T028, T029, T030, T031, T032 | Readiness, closure, MCP parity, package-contract, and sync-guard checks. | Installed cache reload is outside source/bundle proof unless explicitly performed. |

## Design To Implementation Matrix

| Design Section | Requirements | Tasks | Interfaces Or Files | Verification | Coverage State | Residual Destination |
|----------------|--------------|-------|---------------------|--------------|----------------|----------------------|
| `design.md#overview` | Requirements 1-5 | T013, T030, T032 | Spec package artifacts | Review and lifecycle lint | complete | none |
| `design.md#system-architecture` | Requirement 5 | T012, T015, T020, T021 | `core.py`, `spec_mcp_server.py`, `runtime_adapter.py` | Runtime and MCP tests | complete | none |
| `design.md#components-and-changes` | Requirement 4 | T022, T023, T024, T025, T026, T027, T028 | Skill, prompts, templates, docs, bundles | Prompts, package-contract, sync-guard | complete | none |
| `design.md#data-models` | Requirement 1, Requirement 2 | T001, T002, T019 | Diagnostic dictionaries in `core.py` | Runtime tests | complete | none |
| `design.md#data-flow` | Requirement 5 | T010, T011, T020, T021 | `lint_spec_package`, `agent_readiness_packet`, `closure_check` | Readiness and closure tests | complete | none |
| `design.md#algorithms-and-logic` | Requirement 2, Requirement 3 | T003, T004, T005, T006, T007, T008, T014, T016, T017 | Canonical-context helpers in `core.py` | Risk-signal tests | complete | none |
| `design.md#function-signatures-and-interfaces` | Requirement 5 | T014, T015 | Runtime helper interfaces | Unit tests and MCP handler tests | complete | none |
| `design.md#error-handling` | Requirement 3 | T009, T018 | Diagnostic warning metadata | Ambiguous-match tests | complete | none |
| `design.md#migration-and-compatibility` | Requirement 4, Requirement 5 | T027, T028, T029 | Bundle paths and adapters | Package-contract and sync-guard | complete | none |
| `design.md#validation-strategy` | Requirements 1-5 | T013, T029, T030, T031, T032 | Tests, lifecycle commands, validation evidence | Focused and full validation | complete | none |
| `design.md#operational-considerations` | Requirement 4 | T025, T026, T030, T032 | Durable docs and verification notes | Review and closure-check | complete | none |

## Open Decision Impact

| Decision ID | Blocks | Affected Requirements | Affected Tasks | Resolution Needed |
|-------------|--------|-----------------------|----------------|-------------------|
| none | none | none | none | Requirements-stage design questions are resolved in `requirements.md#resolved-design-questions` and `design.md#overview`. |

## Maintenance Notes

- Update this matrix whenever task IDs, runtime surfaces, design sections, or
  durable targets change.
- Before closure, every `complete` coverage state must be supported by task
  evidence or changed to a partial state with one explicit destination.
- Treat installed runtime reload as operational evidence, not source or bundle
  parity proof.
