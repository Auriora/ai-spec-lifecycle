---
title: Guided documentation wizard traceability
doc_type: spec
artifact_type: traceability
status: active
owner: platform
last_reviewed: 2026-06-14
---

# Traceability

## Task To Context Matrix

| Task ID | Requirements | Acceptance Criteria | Design Sections | Change Impact | Verification | Durable Targets | Open Decisions |
|---------|--------------|---------------------|-----------------|---------------|--------------|-----------------|----------------|
| T001 | R1, R3, R4, R5 | R1 AC1-AC4; R3 AC1-AC4; R4 AC1-AC4; R5 AC1-AC4 | Overview; Open Questions | Change Type; Open Questions | Quality Gates; Agent Readiness Evidence | `design.md`; `traceability.md` | D001, D002, D003, D004 |
| T002 | R1, R2, R3, R4, R5, R6 | R1 AC1-AC4; R2 AC1-AC4; R3 AC1-AC4; R4 AC1-AC4; R5 AC1-AC4; R6 AC1-AC4 | Agent-facing surface; Components and Changes | Proposed Changes | Validation Commands; Requirement Coverage | `skills/spec-lifecycle-manager/prompts/`; `skills/spec-lifecycle-manager/SKILL.md` | D001, D003 |
| T003 | R1, R2, R3, R4, R5, R6, R7 | all listed acceptance criteria | System Architecture; Data Models; Algorithms and Logic; Function Signatures and Interfaces | Proposed Changes | Correctness Property Coverage; Validation Commands | `skills/spec-lifecycle-manager/scripts/spec_runtime.py`; `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`; tests | D001, D002, D004 |
| T004 | R6, R7 | R6 AC3-AC4; R7 AC1-AC4 | Operational Considerations; Validation Strategy | Promotion Targets; Unchanged Durable Areas | Durable Promotion And Cleanup | `docs/design/spec-lifecycle-management.md`; `docs/reference/spec-lifecycle-runtime.md`; `docs/backlog/README.md` | none |
| T005 | R6 | R6 AC1-AC4 | Components and Changes; Migration and Compatibility | Promotion Targets | Validation Commands | plugin bundle skill copies | none |
| T006 | R1, R2, R3, R4, R5, R6, R7 | all listed acceptance criteria | Validation Strategy | Promotion Targets | Quality Gates; Evidence Log | `verification.md`; test files | none |
| T007 | R7 | R7 AC1-AC4 | Operational Considerations | Promotion Targets | Durable Promotion And Cleanup; Spec Cleanup Decision | closure log and archive index | none |

## Requirement To Delivery Matrix

| Requirement | Acceptance Criteria | Design Sections | Tasks | Verification | Durable Targets |
|-------------|---------------------|-----------------|-------|--------------|-----------------|
| R1 Stage-Aware Wizard Entry Point | AC1-AC4 | System Architecture; Data Flow; Error Handling | T001, T002, T003, T006 | Runtime tests; prompt review | `docs/reference/spec-lifecycle-runtime.md` |
| R2 Step-By-Step Documentation Flow | AC1-AC4 | Data Models; Algorithms and Logic | T002, T003, T006 | Stage transition tests | `docs/design/spec-lifecycle-management.md` |
| R3 Open-Question Guidance | AC1-AC4 | Data Models; Algorithms and Logic | T001, T002, T003, T006 | Open-question tests and prompt review | `skills/spec-lifecycle-manager/SKILL.md` |
| R4 Feedback Disposition Workflow | AC1-AC4 | Data Models; Algorithms and Logic | T001, T002, T003, T006 | Feedback disposition tests | `skills/spec-lifecycle-manager/SKILL.md` |
| R5 Preview-First Edit Plan | AC1-AC4 | Preview edit model; Security, Trust, and Access | T001, T002, T003, T006 | Preview schema tests | `docs/reference/spec-lifecycle-runtime.md` |
| R6 Existing Tool Composition | AC1-AC4 | Components and Changes; Migration and Compatibility | T002, T003, T004, T005, T006 | Prompt validation; runtime/MCP tests | runtime reference and prompt docs |
| R7 Durable Promotion And Closure Awareness | AC1-AC4 | Operational Considerations; Validation Strategy | T003, T004, T006, T007 | Promotion/closure review | durable docs, closure log, archive index |

## Correctness Property Coverage

| Property | Requirements | Design Sections | Tasks | Tests Or Verification | Residual Risk |
|----------|--------------|-----------------|-------|-----------------------|---------------|
| CP-001 | R1, R3, R7 | Algorithms and Logic; Error Handling | T003, T006 | Runtime readiness tests | none expected |
| CP-002 | R2 | Algorithms and Logic | T002, T003, T006 | Stage transition tests | Human users can still ask to skip stages; exception must be visible. |
| CP-003 | R4 | Data Models | T003, T006 | Feedback model tests | Disposition semantics may need dogfood refinement. |
| CP-004 | R5 | Data Models; Security, Trust, and Access | T003, T006 | Preview edit schema tests | Write application remains manual in v1. |
| CP-005 | R1, R7 | Error Handling; Migration and Compatibility | T003, T006 | Closed-spec scenario test or manual review | Depends on archive/closure history quality. |

## Design To Implementation Matrix

| Design Section | Requirements | Tasks | Interfaces Or Files | Verification |
|----------------|--------------|-------|---------------------|--------------|
| System Architecture | R1, R6 | T002, T003 | prompt definitions, runtime helper | Prompt and runtime tests |
| Data Models | R2, R3, R4, R5 | T003 | wizard payload records | Unit tests |
| Algorithms and Logic | R1, R2, R3, R4, R7 | T003 | `documentation_wizard(...)` candidate | Unit tests |
| Function Signatures and Interfaces | R6 | T003 | CLI/MCP candidate interfaces | Runtime/MCP tests |
| Security, Trust, and Access | R5 | T001, T003 | preview-first behavior | Unit tests and review |
| Validation Strategy | R1-R7 | T006 | validation evidence | Full validation |
| Operational Considerations | R7 | T004, T007 | durable docs and closure records | Closure readiness review |

## Open Decision Impact

| Decision ID | Blocks | Affected Requirements | Affected Tasks | Resolution Needed |
|-------------|--------|-----------------------|----------------|-------------------|
| D001 | Implementation surface | R1, R2, R3, R6 | T001, T002, T003 | Decide prompt-only versus runtime/MCP in v1. |
| D002 | Feedback model | R4 | T001, T003 | Choose review-result reuse or smaller wizard model. |
| D003 | User interaction pacing | R2, R3 | T001, T002 | Choose one-question default versus checklist mode. |
| D004 | Write boundary | R5 | T001, T003 | Confirm manual edit application for v1 or define guarded write follow-up. |

## Maintenance Notes

- Update this matrix when decisions, task IDs, prompt names, or runtime command
  names change.
- Treat uncovered correctness properties or acceptance criteria as readiness
  gaps until mapped to tests or documented manual validation.
