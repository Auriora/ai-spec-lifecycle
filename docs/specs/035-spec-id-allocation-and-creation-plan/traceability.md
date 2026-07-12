---
title: Spec ID allocation and creation plan traceability
doc_type: spec
artifact_type: traceability
status: active
lifecycle_stage: tasks
owner: platform
last_reviewed: 2026-07-12
---

# Traceability

## Task To Context Matrix

| Task | Requirements | Correctness | Design | Verification |
|------|--------------|-------------|--------|--------------|
| T001 | Requirement 1; Requirement 2 AC1-2, AC5-6 | CP-001, CP-002, CP-003 | Numbering Scope And Evidence; `spec_id_inventory` | V001-V012 |
| T002 | Requirement 2 AC3-4, AC6; Requirement 3; Requirement 5 | CP-002, CP-003, CP-004, CP-006, CP-007 | `spec_creation_plan`; Slug And Path Safety; Template And Artifact Planning; Evidence Fingerprint; Future Writer Boundary | V013-V026 |
| T003 | Requirement 4 AC1-2, AC4 | CP-001, CP-002, CP-003 | Bootstrap And Orientation Integration | V027-V032 |
| T004 | Requirement 4 AC3 | CP-003, CP-005, CP-006 | Component Boundaries; Error Handling | V033-V036 |
| T005 | Requirement 3; Requirement 4 AC3 | CP-002, CP-003, CP-005, CP-007 | Public Contracts; Component Boundaries | V037-V044 |
| T006 | Requirement 4 AC3 | CP-005 | Component Boundaries; Verification Strategy | V045-V048 |
| T007 | all | all | Durable Promotion Targets; Residual Risks | V049-V052 |

## Requirement To Delivery Matrix

| Requirement | Tasks | Coverage State | Primary proof |
|-------------|-------|----------------|---------------|
| Requirement 1: Numbering Inventory | T001, T005 | complete | scoped evidence/diagnostic fixtures and MCP schema |
| Requirement 2: Next Spec ID | T001, T002, T004-T005 | complete | monotonic, slug, path, and parity fixtures |
| Requirement 3: Preview-Only Creation Plan | T002, T004-T005 | complete | plan, collision, template, and read-only fixtures |
| Requirement 4: Bootstrap And Existing Repo Consistency | T003-T006 | complete | additive integration and adapter/package tests |
| Requirement 5: Stale Plan Validation And Future Write Boundary | T002, T005, T007 | complete | fingerprint/staleness tests and durable contract |

## Design To Implementation Matrix

| Design section | Tasks | Primary target |
|----------------|-------|----------------|
| Numbering Scope And Evidence | T001 | shared lifecycle core |
| Slug/Path, Template, Fingerprint, Writer Boundary | T002 | shared core and provenance helper |
| Bootstrap And Orientation Integration | T003 | shared orientation/bootstrap internals |
| CLI boundary | T004 | runtime adapter |
| MCP and schema boundary | T005 | MCP server and agent schemas |
| Package compatibility | T006 | source and bundled plugin trees |
| Durable Promotion Targets | T007 | durable docs, backlog, roadmap, history |

## Open Decision Impact

No blocking decisions remain. The accepted two-tool public shape, additive
orientation fields, fingerprint domain, evidence scope, template precedence,
and future atomic-writer boundary are recorded in requirements and design.
