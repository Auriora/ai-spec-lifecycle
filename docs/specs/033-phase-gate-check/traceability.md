---
title: Phase gate check traceability
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
| T001 | Requirement 1, Requirement 3, Requirement 4 | CP-001, CP-002, CP-005 | Public Phase Model; Inference Order; Source Composition | V001-V010 |
| T002 | Requirement 2 | CP-001, CP-004 | Staleness Contract | V011-V015 |
| T003 | Requirement 2, Requirement 3 | CP-001, CP-002, CP-005, CP-006 | Compact And Expansion Contract; Evidence Fingerprint | V016-V023 |
| T004 | Requirement 3 | CP-003, CP-004 | Core Interface; Compatibility | V024-V028 |
| T005 | Requirement 3 | CP-003 | Operational Considerations | V029-V031 |
| T006 | all | all | Durable Promotion Targets | V032-V034 |

## Requirement To Delivery Matrix

| Requirement | Tasks | Verification |
|-------------|-------|--------------|
| Requirement 1: Phase Detection | T001 | V001-V008 |
| Requirement 2: Advancement Readiness | T001-T003 | V009-V023 |
| Requirement 3: Composition With Existing Checks | T001, T003-T005 | V005, V016-V031 |
| Requirement 4: Advisory Boundary | T001, T003 | V006, V020-V023 |

## Design To Implementation Matrix

| Design section | Tasks | Primary target |
|----------------|-------|----------------|
| Public Phase Model and Inference Order | T001 | shared lifecycle core |
| Staleness Contract | T002 | shared lifecycle core/fixtures |
| Compact And Expansion Contract | T003 | core renderer/schema composition |
| Core Interface and Compatibility | T004 | MCP/CLI adapters |
| Durable Promotion Targets | T006 | durable docs/backlog/history |

## Open Decision Impact

No blocking open decisions remain. Accepted phase, tool-shape, staleness, and
promotion-conservatism decisions are recorded in requirements and design.
