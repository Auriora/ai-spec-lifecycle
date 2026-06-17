---
title: Guided documentation wizard traceability
doc_type: spec
artifact_type: traceability
status: active
owner: platform
last_reviewed: 2026-06-17
---

# Traceability

## Task To Context Matrix

| Task ID | Requirements | Acceptance Criteria | Design Sections | Change Impact | Verification | Durable Targets | Open Decisions |
|---------|--------------|---------------------|-----------------|---------------|--------------|-----------------|----------------|
| T001 | R1, R3, R4, R5 | R1 AC1-AC4; R3 AC1-AC4; R4 AC1-AC4; R5 AC1-AC4 | Overview; Open Questions | Change Type; Open Questions | Quality Gates; Agent Readiness Evidence | `design.md`; `traceability.md` | D001-D004 resolved 2026-06-17 |
| T002 | R1, R2, R3, R4, R5, R6 | R1 AC1-AC4; R2 AC1-AC4; R3 AC1-AC4; R4 AC1-AC4; R5 AC1-AC4; R6 AC1-AC4 | System Architecture; Components and Changes; Conversation Output Shape; Prompt Behavior | Proposed Changes | Validation Commands; Requirement Coverage | `skills/spec-lifecycle-manager/prompts/`; `skills/spec-lifecycle-manager/SKILL.md` | none |
| T003 | none | none | none — runtime/MCP design removed; not building per D001 | none | none | none | D001 resolved 2026-06-17: prompt-only; T003 is no-op |
| T004 | R6, R7 | R6 AC3-AC4; R7 AC1-AC4 | Operational Considerations; Validation Strategy | Promotion Targets; Unchanged Durable Areas | Durable Promotion And Cleanup | `docs/design/spec-lifecycle-management.md`; `docs/reference/spec-lifecycle-runtime.md`; `docs/backlog/README.md` | none |
| T005 | R6 | R6 AC1-AC4 | Components and Changes; Migration and Compatibility | Promotion Targets | Validation Commands | plugin bundle skill copies | none |
| T006 | R1, R2, R3, R4, R5, R6, R7 | all listed acceptance criteria | Validation Strategy | Promotion Targets | Quality Gates; Evidence Log | `verification.md`; test files | none |
| T007 | R7 | R7 AC1-AC4 | Operational Considerations | Promotion Targets | Durable Promotion And Cleanup; Spec Cleanup Decision | closure log and archive index | none |

## Requirement To Delivery Matrix

| Requirement | Acceptance Criteria | Design Sections | Tasks | Verification | Durable Targets |
|-------------|---------------------|-----------------|-------|--------------|-----------------|
| R1 Stage-Aware Wizard Entry Point | AC1-AC4 | System Architecture; Data Flow; Error Handling | T001, T002, T006 | Prompt content review | `docs/reference/spec-lifecycle-runtime.md` |
| R2 Step-By-Step Documentation Flow | AC1-AC4 | Conversation Output Shape; Prompt Behavior | T002, T006 | Prompt content review | `docs/design/spec-lifecycle-management.md` |
| R3 Open-Question Guidance | AC1-AC4 | Conversation Output Shape; Prompt Behavior | T001, T002, T006 | Prompt content review | `skills/spec-lifecycle-manager/SKILL.md` |
| R4 Feedback Disposition Workflow | AC1-AC4 | Conversation Output Shape; Prompt Behavior | T001, T002, T006 | Prompt content review | `skills/spec-lifecycle-manager/SKILL.md` |
| R5 Preview-First Edit Plan | AC1-AC4 | Conversation Output Shape; Security, Trust, and Access | T001, T002, T006 | Prompt content review | `docs/reference/spec-lifecycle-runtime.md` |
| R6 Existing Tool Composition | AC1-AC4 | Components and Changes; Migration and Compatibility | T002, T004, T005, T006 | Prompt validation; manual tool-list cross-check | runtime reference and prompt docs |
| R7 Durable Promotion And Closure Awareness | AC1-AC4 | Operational Considerations; Validation Strategy | T004, T006, T007 | Promotion/closure review | durable docs, closure log, archive index |

## Correctness Property Coverage

| Property | Requirements | Design Sections | Tasks | Tests Or Verification | Residual Risk |
|----------|--------------|-----------------|-------|-----------------------|---------------|
| CP-001 | R1, R3, R7 | Prompt Behavior; Error Handling | T006 | Prompt content review | Enforcement depends on agent compliance, not code. |
| CP-002 | R2 | Prompt Behavior | T002, T006 | Prompt content review | Human users can still ask to skip stages; exception must be visible. |
| CP-003 | R4 | Conversation Output Shape | T002, T006 | Prompt content review | Disposition semantics may need dogfood refinement. |
| CP-004 | R5 | Conversation Output Shape; Security, Trust, and Access | T002, T006 | Prompt content review | Write application remains manual in v1. |
| CP-005 | R1, R7 | Error Handling; Migration and Compatibility | T006 | Prompt content review or manual review | Depends on archive/closure history quality. |

## Design To Implementation Matrix

| Design Section | Requirements | Tasks | Interfaces Or Files | Verification |
|----------------|--------------|-------|---------------------|--------------|
| System Architecture | R1, R6 | T002 | prompt definitions | Prompt content review |
| Conversation Output Shape | R2, R3, R4, R5 | T002 | prompt definitions | Prompt content review |
| Prompt Behavior | R1, R2, R3, R4, R7 | T002 | prompt definitions | Prompt content review |
| Security, Trust, and Access | R5 | T001, T002 | preview-first behavior | Prompt content review |
| Validation Strategy | R1-R7 | T006 | validation evidence | Full validation |
| Operational Considerations | R7 | T004, T007 | durable docs and closure records | Closure readiness review |

## Open Decision Impact

| Decision ID | Resolution | Blocks | Affected Requirements | Affected Tasks |
|-------------|------------|--------|------------------------|----------------|
| D001 | Resolved 2026-06-17: prompt-only plus durable guidance; no runtime/MCP tool built. | Implementation surface | R1, R2, R3, R6 | T001 (resolved), T003 (no-op) |
| D002 | Resolved 2026-06-17: reuse the existing review-result disposition shape. | Feedback model | R4 | T001 (resolved), T002 |
| D003 | Resolved 2026-06-17: one stage-specific question by default, explicit checklist mode on request. | User interaction pacing | R2, R3 | T001 (resolved), T002 |
| D004 | Resolved 2026-06-17: manual edit application by Codex/user in v1; future guarded-write helper, if pursued, to be routed to backlog under T004, not designed here. | Write boundary | R5 | T001 (resolved) |

## Maintenance Notes

- Update this matrix when decisions, task IDs, prompt names, or runtime
  command names change.
- Treat uncovered correctness properties or acceptance criteria as readiness
  gaps until mapped to tests or documented manual validation.
