---
title: MCP-first runtime migration traceability
doc_type: spec
artifact_type: traceability
status: draft
authoring_mode: wizard
lifecycle_stage: tasks
owner: platform
last_reviewed: 2026-07-05
---

# Traceability Matrix

## Purpose

Map the MCP-first runtime migration requirements, design decisions, tasks,
validation evidence, durable targets, and resolved decisions. Before
implementation, use this matrix to confirm each task has the relevant
requirement, design, and validation context.

## Task To Context Matrix

| Task ID | Requirements | Acceptance Criteria | Design Sections | Change Impact | Verification | Durable Targets | Open Decisions |
|---------|--------------|---------------------|-----------------|---------------|--------------|-----------------|----------------|
| T001 | Requirement 1; Requirement 5; Requirement 9 | R1 AC1-AC2; R5 AC1-AC5; R9 AC1-AC5 | `design.md#overview`; `design.md#migration-and-compatibility`; `design.md#resolved-design-decisions` | none | `verification.md#quality-gates` | `docs/specs/030-mcp-first-runtime-migration/tasks.md`; `traceability.md` | none |
| T002 | Requirement 2; Requirement 3; Requirement 4 | R2 AC1-AC5; R3 AC1-AC7; R4 AC1-AC4 | `design.md#capability-report`; `design.md#compatibility-matrix-row`; `design.md#compatibility-checker-flow` | none | `verification.md#compatibility-matrix` | `docs/reference/spec-lifecycle-runtime.md` | none |
| T003 | Requirement 5; Requirement 6; Requirement 9 | R5 AC1-AC5; R6 AC1, AC4; R9 AC1-AC5 | `design.md#script-migration-inventory-row`; `design.md#migration-and-compatibility`; `design.md#resolved-design-decisions` | none | `verification.md#migration-inventory-validation` | `design.md`; `verification.md`; `traceability.md` | none |
| T004 | Requirement 9 | R9 AC1, AC4 | `design.md#system-architecture`; `design.md#components-and-changes`; `design.md#function-signatures-and-interfaces` | none | `verification.md#shared-module-validation` | package source and bundle docs | none |
| T005 | Requirement 7; Requirement 8; Requirement 9 | R7 AC1-AC3; R8 AC1; R9 AC5 | `design.md#validation-strategy`; `design.md#function-signatures-and-interfaces` | none | `verification.md#shared-module-validation` | tests | none |
| T006 | Requirement 2; Requirement 3; Requirement 7 | R2 AC1-AC5; R3 AC5-AC7; R7 AC1-AC3 | `design.md#capability-report`; `design.md#mcp-session-state`; `design.md#mcp-tools` | none | `verification.md#mcp-contract-validation` | `docs/reference/spec-lifecycle-runtime.md` | none |
| T007 | Requirement 1; Requirement 4; Requirement 7 | R1 AC1; R4 AC2-AC4; R7 AC1 | `design.md#available-next-action`; `design.md#stable-mcp-tool-flow`; `design.md#next-action-derivation` | none | `verification.md#mcp-contract-validation` | `docs/reference/spec-lifecycle-runtime.md` | none |
| T008 | Requirement 5; Requirement 6; Requirement 7; Requirement 9 | R5 AC1-AC5; R6 AC1, AC4; R7 AC1-AC3; R9 AC1-AC5 | `design.md#script-migration-inventory-row`; `design.md#mcp-tools`; `design.md#migration-closure-check` | none | `verification.md#migration-inventory-validation`; `verification.md#mcp-contract-validation` | `docs/reference/spec-lifecycle-runtime.md` | none |
| T009 | Requirement 7 | R7 AC1-AC3 | `design.md#mcp-tools`; `design.md#validation-strategy` | none | `verification.md#schema-validation` | schema docs if promoted | none |
| T010 | Requirement 5; Requirement 6; Requirement 8; Requirement 9 | R5 AC2, AC4-AC5; R6 AC3-AC4; R8 AC1-AC2; R9 AC1-AC5 | `design.md#script-migration-inventory-row`; `design.md#script-migration-flow`; `design.md#retained-non-mcp-flow` | none | `verification.md#traceability-migration-validation` | `docs/reference/spec-lifecycle-runtime.md` | none |
| T011 | Requirement 5; Requirement 6; Requirement 9 | R5 AC1-AC5; R6 AC1-AC4; R9 AC5 | `design.md#migration-closure-check`; `design.md#migration-and-compatibility` | none | `verification.md#migration-inventory-validation` | retained validation and closure-check docs | none |
| T012 | Requirement 5; Requirement 6; Requirement 8 | R5 AC2; R6 AC1-AC4; R8 AC3 | `design.md#script-migration-flow`; `design.md#migration-and-compatibility` | none | `verification.md#package-parity-validation` | package source, bundle, installed cache | none |
| T013 | Requirement 1; Requirement 5; Requirement 6; Requirement 8; Requirement 9 | R1 AC1-AC2; R5 AC3-AC4; R6 AC3; R8 AC2; R9 AC3 | `design.md#operational-considerations`; `design.md#migration-and-compatibility` | none | `verification.md#durable-promotion-and-cleanup` | `docs/reference/spec-lifecycle-runtime.md`; `docs/reference/spec-lifecycle-manager-mcp-install.md`; `skills/spec-lifecycle-manager/SKILL.md` | none |
| T014 | Requirement 6; Requirement 7; Requirement 8 | R6 AC1-AC4; R7 AC1-AC3; R8 AC1-AC3 | `design.md#validation-strategy`; `design.md#downstream-task-guidance` | none | `verification.md#quality-gates`; `verification.md#evidence-log` | closure log and archive index after completion | none |
| T015 | Requirement 1; Requirement 8; Requirement 9 | R1 AC1-AC2; R8 AC2; R9 AC1-AC5 | `design.md#overview`; `design.md#resolved-design-decisions`; `design.md#operational-considerations` | none | `verification.md#implementation-review-remediation`; `verification.md#residual-risks`; `verification.md#durable-promotion-and-cleanup` | `docs/backlog/README.md` B059; spec closure evidence | none |
| T016 | Requirement 9; B060 | R9 AC1-AC5; B060 candidate acceptance | `design.md#overview`; `design.md#resolved-design-decisions`; `design.md#operational-considerations` | none | `verification.md#implementation-review-remediation`; `verification.md#residual-risks`; `verification.md#durable-promotion-and-cleanup` | spec-package templates; `documentation-wizard` prompt; bundled plugin copies; `docs/backlog/README.md` B060 | none |
| T017 | Requirement 9; B059 | R9 AC1-AC5; B059 candidate acceptance | `design.md#overview`; `design.md#system-architecture`; `design.md#components-and-changes`; `design.md#retained-non-mcp-flow` | none | `verification.md#implementation-review-remediation`; `verification.md#residual-risks`; `verification.md#durable-promotion-and-cleanup` | shared lifecycle modules; MCP server; retained runtime/recovery docs; `docs/backlog/README.md` B059 | none |

## Requirement To Delivery Matrix

| Requirement | Acceptance Criteria | Design Sections | Tasks | Verification | Durable Targets |
|-------------|---------------------|-----------------|-------|--------------|-----------------|
| Requirement 1 | AC1, AC2 | `design.md#overview`; `design.md#components-and-changes` | T001, T007, T013 | MCP contract tests; docs review | `docs/reference/spec-lifecycle-runtime.md`; skill guidance |
| Requirement 2 | AC1-AC5 | `design.md#capability-report`; `design.md#mcp-session-state` | T002, T006 | MCP server tests | runtime docs |
| Requirement 3 | AC1-AC7 | `design.md#compatibility-matrix-row`; `design.md#compatibility-checker-flow` | T002, T006 | compatibility matrix review | `verification.md`; runtime docs |
| Requirement 4 | AC1-AC4 | `design.md#stable-mcp-tool-flow`; `design.md#available-next-action` | T002, T007 | MCP contract tests | runtime docs |
| Requirement 5 | AC1-AC5 | `design.md#script-migration-inventory-row`; `design.md#migration-and-compatibility` | T001, T003, T008, T010, T011, T012, T013 | migration inventory tests; package parity | runtime docs; package docs |
| Requirement 6 | AC1-AC4 | `design.md#migration-closure-check`; `design.md#script-migration-flow` | T003, T008, T011, T012, T013, T014 | closure blocker tests; sync-guard | closure docs after completion |
| Requirement 7 | AC1-AC3 | `design.md#mcp-tools`; `design.md#error-handling` | T005, T006, T007, T008, T009, T014 | MCP schema and structuredContent tests | runtime docs |
| Requirement 8 | AC1-AC3 | `design.md#validation-strategy`; `design.md#retained-non-mcp-flow` | T005, T010, T012, T013, T014 | unit tests; package-contract; sync-guard | verification evidence |
| Requirement 9 | AC1-AC5 | `design.md#system-architecture`; `design.md#components-and-changes`; `design.md#retained-non-mcp-flow` | T001, T003, T004, T005, T008, T010, T011, T013, T015, T016, T017 | public tool ownership review; shared-module tests; shared-core extraction tests; prompt/template guard | runtime docs; package docs; templates/prompts |

## Correctness Property Coverage

| Property | Requirements | Design Sections | Tasks | Tests Or Verification | Residual Risk |
|----------|--------------|-----------------|-------|-----------------------|---------------|
| CP-001 | Requirement 3; Requirement 4 | `design.md#compatibility-checker-flow`; `design.md#stable-mcp-tool-flow` | T002, T007 | MCP contract tests; compatibility matrix review | Dynamic tools deferred until future evidence. |
| CP-002 | Requirement 5; Requirement 6 | `design.md#migration-closure-check`; `design.md#script-migration-flow` | T003, T008, T011, T012, T014 | closure blocker tests; sync-guard | none if removal checks cover bundles and cache. |
| CP-003 | Requirement 7 | `design.md#mcp-tools`; `design.md#error-handling` | T006, T007, T008, T009 | structuredContent and schema tests | Text fallback remains for compatibility. |
| CP-004 | Requirement 8 | `design.md#retained-non-mcp-flow`; `design.md#validation-strategy` | T013, T014 | full test suite; package-contract; sync-guard | Emergency recovery docs must stay clear. |
| CP-005 | Requirement 2; Requirement 3 | `design.md#mcp-session-state`; `design.md#security-trust-and-access` | T002, T006 | tests assert `unknown` instead of guessed fields | Client behavior may change; evidence must be dated. |
| CP-006 | Requirement 5; Requirement 6 | `design.md#script-migration-inventory-row`; `design.md#migration-closure-check` | T003, T008, T010, T011, T012 | replacement contract tests/review | none if closure blocks deletion-only migration. |
| CP-007 | Requirement 9 | `design.md#system-architecture`; `design.md#retained-non-mcp-flow` | T001, T003, T004, T005, T011, T013, T015, T016, T017 | public tool ownership review; command inventory review; shared-core extraction tests; prompt/template guard | none after T016/T017 validation. |

## Design To Implementation Matrix

| Design Section | Requirements | Tasks | Interfaces Or Files | Verification |
|----------------|--------------|-------|---------------------|--------------|
| `design.md#system-architecture` | Requirement 9 | T004, T005 | `skills/spec-lifecycle-manager/scripts/lifecycle/`, entrypoint scripts | shared-module tests |
| `design.md#capability-report` | Requirement 2, Requirement 3 | T006 | `spec_mcp_server.py`, `lifecycle/capabilities.py` | MCP server tests |
| `design.md#available-next-action` | Requirement 1, Requirement 4 | T007 | `lifecycle/actions.py`, `active_spec_preflight`, `stage_readiness`, `lifecycle_guide`, `no_active_spec_context` | MCP contract tests |
| `design.md#compatibility-matrix-row` | Requirement 3, Requirement 4 | T002, T014 | `verification.md` | compatibility matrix review |
| `design.md#script-migration-inventory-row` | Requirement 5, Requirement 6 | T003, T008, T011, T012 | `lifecycle/migration.py`, traceability removal paths | migration inventory tests; sync-guard |
| `design.md#mcp-session-state` | Requirement 2 | T006 | `spec_mcp_server.py`, `lifecycle/capabilities.py` | initialize/session tests |
| `design.md#mcp-tools` | Requirement 7 | T006, T008, T009 | MCP tool definitions, schema helpers | schema validation tests |
| `design.md#retained-non-mcp-flow` | Requirement 8, Requirement 9 | T011, T013, T014 | `spec_runtime.py`, hook scripts, docs | command inventory review; validation suite |
| `design.md#overview` retained recovery debt | Requirement 9 | T015, T017 | `docs/backlog/README.md` B059; `lifecycle/core.py`; `lifecycle/runtime_adapter.py`; `spec_runtime.py`; `spec_mcp_server.py` | implementation review remediation; shared-core extraction tests |
| `design.md#overview` closure semantic coverage | Requirement 9 | T016 | spec-package templates, `documentation-wizard` prompt | prompt/template validation |
| `design.md#system-architecture` shared-core extraction | Requirement 9 | T017 | `spec_mcp_server.py`, `spec_runtime.py`, `lifecycle/core.py`, `lifecycle/runtime_adapter.py` | MCP/runtime shared-core tests; non-executable shared-core regression |

## Open Decision Impact

| Decision ID | Blocks | Affected Requirements | Affected Tasks | Resolution Needed |
|-------------|--------|-----------------------|----------------|-------------------|
| none | none | all | all | Design decisions are recorded in `design.md#resolved-design-decisions`; reopen if implementation finds a conflict. |

## Maintenance Notes

- Update this matrix when task IDs, selected migrated scripts, MCP tool names,
  shared module boundaries, validation commands, or durable targets change.
- Keep single public tool ownership explicit in task evidence and docs.
- Treat uncovered correctness properties or acceptance criteria as readiness
  gaps until mapped here.
