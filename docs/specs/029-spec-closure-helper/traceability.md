---
title: Spec closure helper traceability
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

Map spec 029 requirements, design sections, tasks, planned verification,
durable-doc targets, and resolved decisions. Before implementing a task, use
the MCP `traceability_lookup` tool when available, then read the linked source
sections directly.

## Task To Context Matrix

| Task ID | Requirements | Acceptance Criteria | Design Sections | Verification | Durable Targets | Decisions |
|---------|--------------|---------------------|-----------------|--------------|-----------------|-----------|
| T001 | Requirement 1, Requirement 2, Requirement 3, Requirement 4, Requirement 5, Requirement 6, Requirement 7, Requirement 8, Requirement 9, Requirement 10 | all acceptance criteria | Overview; Downstream Task Guidance | Package lint | none | OQ-001..OQ-006 |
| T002 | Requirement 1, Requirement 3, Requirement 6, Requirement 7, Requirement 9, Requirement 10 | Requirement 1 AC1-AC3; Requirement 3 AC1-AC6; Requirement 6 AC1-AC3; Requirement 7 AC1-AC3; Requirement 9 AC1-AC5; Requirement 10 AC1-AC4 | Validation Strategy; Final Spec Commit Discovery; Metadata Rendering; Durable Record Ownership | Fixture tests | none | OQ-003, OQ-004, OQ-006 |
| T003 | Requirement 7, Requirement 8, Requirement 10 | Requirement 7 AC1-AC3; Requirement 8 AC1-AC6; Requirement 10 AC1-AC4 | Data Models; status/action mapping; Error Handling | Metadata unit tests | none | OQ-002, OQ-006 |
| T004 | Requirement 1, Requirement 2, Requirement 4, Requirement 7, Requirement 8 | Requirement 1 AC1-AC3; Requirement 2 AC1-AC2; Requirement 4 AC1-AC4; Requirement 7 AC1-AC3; Requirement 8 AC1-AC6 | Plan Flow; Function Signatures; Components and Changes | Plan tests | none | OQ-001, OQ-002 |
| T005 | Requirement 3, Requirement 6 | Requirement 3 AC1-AC6; Requirement 6 AC1-AC3 | Final Spec Commit Discovery; Active Reference Classification | Git/reference tests | none | OQ-004 |
| T006 | Requirement 7, Requirement 9, Requirement 10 | Requirement 7 AC1-AC3; Requirement 9 AC1-AC5; Requirement 10 AC1-AC4 | Metadata Rendering; Durable Record Ownership | Rendering/drift tests | `docs/history/spec-closure-log.md`; `docs/history/spec-archive-index.md` | OQ-006 |
| T007 | Requirement 3, Requirement 8, Requirement 9 | Requirement 3 AC2-AC4; Requirement 8 AC1-AC6; Requirement 9 AC3-AC5 | Cleanup Flow; Resolve Flow; Planned Edit Application; Security | Write guard tests | closure records; selected package path; active refs | OQ-002, OQ-005 |
| T008 | Requirement 5, Requirement 8, Requirement 9 | Requirement 5 AC1-AC4; Requirement 8 AC1-AC6; Requirement 9 AC5 | Validation Planning; Validation Strategy | Validation-plan tests | none | OQ-003 |
| T009 | Requirement 5, Requirement 8, Requirement 9 | Requirement 5 AC2; Requirement 8 AC1-AC6; Requirement 9 AC1-AC5 | Runtime recovery interface; Migration and Compatibility | Runtime CLI tests | `docs/reference/spec-lifecycle-runtime.md` | OQ-005 |
| T010 | Requirement 5, Requirement 8, Requirement 9 | Requirement 5 AC1-AC4; Requirement 8 AC1-AC6; Requirement 9 AC1-AC5 | MCP tools; Function Signatures; Migration and Compatibility | MCP tests | `docs/reference/spec-lifecycle-runtime.md`; `skills/spec-lifecycle-manager/SKILL.md` | OQ-001, OQ-005 |
| T011 | Requirement 8, Requirement 9, Requirement 10 | Requirement 8 AC6; Requirement 9 AC1; Requirement 10 AC1 | System Architecture; Migration and Compatibility | Interface parity check | none | OQ-005 |
| T012 | Requirement 5, Requirement 8, Requirement 10 | Requirement 5 AC1-AC3; Requirement 8 AC5-AC6; Requirement 10 AC4 | Components and Changes; Migration and Compatibility; Operational Considerations | Docs wording check | `skills/spec-lifecycle-manager/SKILL.md`; `docs/reference/spec-lifecycle-runtime.md`; `docs/design/spec-lifecycle-management.md` | OQ-001, OQ-005 |
| T013 | Requirement 5, Requirement 8, Requirement 10 | Requirement 5 AC3; Requirement 8 AC6; Requirement 10 AC4 | Components and Changes; Operational Considerations | Sync/package checks | plugin bundle copies | OQ-005 |
| T014 | Requirement 1, Requirement 3, Requirement 4, Requirement 6, Requirement 7, Requirement 9, Requirement 10 | linked acceptance criteria | Validation Strategy; Plan/Cleanup/Resolve Flows | E2E dry-run tests | none | OQ-002, OQ-003, OQ-004, OQ-006 |
| T015 | Requirement 1, Requirement 2, Requirement 3, Requirement 4, Requirement 5, Requirement 6, Requirement 7, Requirement 8, Requirement 9, Requirement 10 | all acceptance criteria | Validation Strategy; Operational Considerations | Full validation commands; creates validation evidence artifact | planned verification artifact created by T015 | OQ-001..OQ-006 |
| T016 | Requirement 1, Requirement 2, Requirement 3, Requirement 4, Requirement 5, Requirement 6, Requirement 7, Requirement 8, Requirement 9, Requirement 10 | all acceptance criteria | Slice Boundary; Downstream Task Guidance; Operational Considerations | Closure/promotion checks | durable docs; backlog if needed | OQ-001..OQ-006 |

## Requirement To Delivery Matrix

| Requirement | Acceptance Criteria | Design Sections | Tasks | Verification | Durable Targets | Coverage State | Residual Destination |
|-------------|---------------------|-----------------|-------|--------------|-----------------|----------------|----------------------|
| Requirement 1 Closure Workflow Checklist | AC1-AC3 | Plan Flow; Downstream Task Guidance | T004, T014, T015, T016 | Plan tests; E2E dry-run | runtime reference if behavior accepted | complete | none |
| Requirement 2 Durable Promotion Confirmation | AC1-AC2 | Plan Flow; Components and Changes | T004, T015, T016 | Plan tests; promotion-plan check | durable docs updated by implementation | complete | none |
| Requirement 3 Commit Evidence Separation | AC1-AC6 | Final Spec Commit Discovery; Cleanup Flow; Resolve Flow | T002, T005, T007, T014 | Git fixture and E2E tests | closure log and archive index behavior | complete | none |
| Requirement 4 Follow-Up Routing | AC1-AC4 | Plan Flow; Data Models | T004, T014, T016 | Metadata and E2E tests | backlog/roadmap/follow-up when needed | complete | none |
| Requirement 5 Validation And Recovery Commands | AC1-AC4 | Validation Planning; runtime/MCP interfaces | T008, T009, T010, T012, T013, T015 | Validation-plan, runtime, MCP, package checks | runtime reference | complete | none |
| Requirement 6 Active-State Removal Verification | AC1-AC3 | Active Reference Classification | T002, T005, T014 | Reference classifier and E2E tests | active docs/backlog if stale refs found | complete | none |
| Requirement 7 Closure Metadata Completeness | AC1-AC3 | Data Models; Metadata Rendering | T003, T004, T006, T014 | Metadata/rendering tests | closure log and archive index | complete | none |
| Requirement 8 Preview-First Interface Boundary | AC1-AC6 | Planned Edit Application; MCP/runtime interfaces; Security | T003, T004, T007, T009, T010, T011, T012 | Write-intent and interface tests | skill/runtime docs | complete | none |
| Requirement 9 Scriptable Closure Mechanics | AC1-AC5 | Metadata Rendering; Cleanup Flow; Resolve Flow | T006, T007, T008, T009, T010, T014 | Rendering, apply, resolve, E2E tests | closure log and archive index | complete | none |
| Requirement 10 Durable Record Ownership | AC1-AC4 | Durable Record Ownership; Migration and Compatibility | T003, T006, T011, T012, T013, T014 | Drift tests; docs and sync checks | closure log, archive index, skill/runtime docs | complete | none |

## Correctness Property Coverage

| Property | Requirements | Design Sections | Tasks | Tests Or Verification | Residual Risk |
|----------|--------------|-----------------|-------|-----------------------|---------------|
| CP-001 | Requirement 2 | Plan Flow | T004, T014 | Missing promotion target tests; E2E dry-run | none |
| CP-002 | Requirement 3 | Data Models; Final Spec Commit Discovery | T003, T005, T014 | Metadata and Git fixture tests | none |
| CP-003 | Requirement 4 | Plan Flow; Data Models | T004, T014 | Follow-up/residual-risk tests | none |
| CP-004 | Requirement 3, Requirement 7 | Data Models; Resolve Flow | T003, T006, T007, T014 | Pending cleanup tests | none |
| CP-005 | Requirement 6 | Active Reference Classification | T005, T014 | Reference classifier tests | Project-specific planning formats may need future patterns. |
| CP-006 | Requirement 8 | Planned Edit Application; Security; MCP/runtime interfaces | T003, T007, T009, T010, T011 | Write-intent and stale-plan tests | none |
| CP-007 | Requirement 9, Requirement 10 | Metadata Rendering; Durable Record Ownership | T006, T014 | Rendering and drift tests | none |
| CP-008 | Requirement 3 | Final Spec Commit Discovery | T005, T014 | Multiple-candidate Git tests | Merge history may need future fixture expansion. |
| CP-009 | Requirement 10 | Durable Record Ownership | T006, T011, T014 | Closure-log/archive-index consistency tests | none |

## Design To Implementation Matrix

| Design Section | Requirements | Tasks | Interfaces Or Files | Verification | Coverage State | Residual Destination |
|----------------|--------------|-------|---------------------|--------------|----------------|----------------------|
| Components and Changes | Requirement 5, Requirement 8, Requirement 10 | T009-T014 | `closure.py`, `core.py`, `runtime_adapter.py`, `spec_mcp_server.py`, docs, plugin copies | Runtime/MCP/package/E2E tests | complete | none |
| Data Models | Requirement 7, Requirement 8, Requirement 10 | T003 | `lifecycle/closure.py` | Metadata unit tests | complete | none |
| Plan Flow | Requirement 1, Requirement 2, Requirement 4, Requirement 7, Requirement 8 | T004 | `closure_plan` | Plan tests | complete | none |
| Cleanup Flow | Requirement 3, Requirement 8, Requirement 9 | T007 | `closure_apply` | Write guard tests | complete | none |
| Resolve Flow | Requirement 3, Requirement 9 | T007 | `closure_resolve` | Resolve tests | complete | none |
| Final Spec Commit Discovery | Requirement 3 | T005 | Git helpers in `closure.py` | Git fixture tests | complete | none |
| Metadata Rendering | Requirement 7, Requirement 9, Requirement 10 | T006 | closure-log/archive-index renderers | Rendering tests | complete | none |
| Durable Record Ownership | Requirement 10 | T006, T012 | owned-field validators; docs | Drift/docs checks | complete | none |
| Active Reference Classification | Requirement 6 | T005 | reference classifier | Classifier tests | complete | none |
| Planned Edit Application | Requirement 8, Requirement 9 | T007 | apply helpers | Stale-plan/write tests | complete | none |
| Validation Planning | Requirement 5 | T008, T015 | validation command planner | Validation-plan tests; full suite | complete | none |
| Function Signatures and Interfaces | Requirement 5, Requirement 8, Requirement 9 | T009-T011 | runtime and MCP entrypoints | CLI/MCP parity tests | complete | none |
| Migration and Compatibility | Requirement 5, Requirement 8, Requirement 10 | T012, T013 | durable docs and plugin bundles | sync/package checks | complete | none |
| Slice Boundary And Residual Architecture | Requirement 1, Requirement 2, Requirement 3, Requirement 4, Requirement 5, Requirement 6, Requirement 7, Requirement 8, Requirement 9, Requirement 10 | T016 | verification and closure evidence | review and closure checks | complete | none |

## Open Decision Impact

| Decision ID | Blocks | Affected Requirements | Affected Tasks | Resolution |
|-------------|--------|-----------------------|----------------|------------|
| OQ-001 | none | Requirement 8, Requirement 9 | T010, T012 | Dedicated MCP tools backed by shared helper logic. |
| OQ-002 | none | Requirement 1, Requirement 8, Requirement 9 | T004, T007, T014 | Script deterministic mechanics; keep judgment manual. |
| OQ-003 | none | Requirement 5 | T008, T015 | Always include scan/archive/closure/diff checks, with package-specific additions. |
| OQ-004 | none | Requirement 6 | T005, T014 | Path/context classification distinguishes historical from stale active refs. |
| OQ-005 | none | Requirement 5, Requirement 8, Requirement 9 | T009-T012 | MCP preferred; runtime retained for recovery/CI; both call `closure.py`. |
| OQ-006 | none | Requirement 10 | T006, T012, T016 | Keep closure log and archive index in v1; future retirement needs a separate migration. |

## Maintenance Notes

- Update this matrix whenever task IDs, design sections, file targets, or
  validation expectations change.
- Before closure, every `partial-blocking` or `not-covered` coverage state must
  be completed, rejected with rationale, or routed to one durable destination.
- If MCP `traceability_lookup` disagrees with this file, reconcile the matrix
  against requirements, design, tasks, and verification before implementing.
- `verification.md` is intentionally not created at task planning time in
  wizard mode. T015 creates or updates it when implementation evidence exists.
