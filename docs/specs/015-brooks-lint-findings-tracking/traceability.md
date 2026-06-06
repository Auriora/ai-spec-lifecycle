---
title: Brooks-Lint findings tracking traceability
doc_type: spec
artifact_type: traceability
status: draft
owner: platform
last_reviewed: 2026-06-06
---

# Traceability

## Task To Context Matrix

| Task ID | Requirements | Acceptance Criteria | Design Sections | Change Impact | Verification | Durable Targets | Open Decisions |
|---------|--------------|---------------------|-----------------|---------------|--------------|-----------------|----------------|
| T001 | Requirement 1, Requirement 3 | R1 AC1-AC3, R3 AC1-AC3 | `design.md#finding-id-format`, `design.md#finding-template`, `design.md#debt-priority-fields`, `design.md#health-dashboard-fields`, `design.md#test-quality-fields` | `change-impact.md#durable-source-mapping` | `verification.md#quality-gates` | docs/reviews/brooks-lint/ | D004 |
| T002 | Requirement 4 | R4 AC1-AC3 | `design.md#operational-considerations` | `change-impact.md#proposed-changes` | `verification.md#quality-gates` | `.brooks-lint-history.json`, docs/reviews/brooks-lint/ | D002 |
| T003 | Requirement 1, Requirement 2, Requirement 3 | R1 AC1-AC3, R2 AC1-AC3, R3 AC1-AC3 | `design.md#seed-register-entries`, `design.md#debt-priority-fields`, `design.md#health-dashboard-fields`, `design.md#test-quality-fields` | `change-impact.md#durable-source-mapping` | `verification.md#evidence-log` | docs/reviews/brooks-lint/ | D004 |
| T004 | Requirement 2, Requirement 3, Requirement 4 | R2 AC1-AC3, R3 AC1-AC3, R4 AC1-AC3 | `design.md#operational-considerations` | `change-impact.md#proposed-changes` | `verification.md#quality-gates` | docs/reviews/brooks-lint/, `skills/spec-lifecycle-manager/scripts/spec_runtime.py` | D001 |
| T005 | Requirement 2, Requirement 5 | R2 AC1-AC3, R5 AC1-AC3 | `design.md#finding-states` | `change-impact.md#risks` | `verification.md#evidence-log` | docs/reviews/brooks-lint/ | D003 |
| T006 | Requirement 2, Requirement 5 | R2 AC3, R5 AC1-AC3 | `design.md#operational-considerations` | `change-impact.md#promotion-targets` | `verification.md#evidence-log` | `docs/backlog/README.md`, `docs/roadmap/README.md` | D003 |
| T007 | Requirement 3, Requirement 4, Requirement 5 | R3 AC1-AC3, R4 AC1-AC3, R5 AC1-AC3 | `design.md#low-level-design` | `change-impact.md#compatibility` | `verification.md#quality-gates` | `verification.md` | D001, D002 |
| T008 | Requirement 5 | R5 AC1-AC3 | `design.md#operational-considerations` | `change-impact.md#promotion-targets` | `verification.md#closure-readiness` | `docs/history/spec-closure-log.md`, `docs/history/spec-archive-index.md` | none |

## Requirement To Delivery Matrix

| Requirement | Tasks | Validation |
|-------------|-------|------------|
| Requirement 1 | T001, T003 | Register schema review; seed finding review. |
| Requirement 2 | T003, T004, T005, T006 | Triage state and routing review. |
| Requirement 3 | T001, T003, T004, T007 | Cross-skill field review and optional validation. |
| Requirement 4 | T002, T004, T007 | History relationship review. |
| Requirement 5 | T005, T006, T007, T008 | Evidence and promotion review. |

## Design To Implementation Matrix

| Design Area | Tasks | Implementation Targets |
|-------------|-------|------------------------|
| Finding ID format | T001, T003 | `docs/reviews/brooks-lint/README.md` |
| Finding states | T005, T006 | Register triage fields and backlog/roadmap routing |
| Register location | T001, T003 | `docs/reviews/brooks-lint/README.md` |
| Finding template | T001, T004 | Register maintenance rules and optional validation |
| Debt priority fields | T001, T003 | Brooks-Debt Pain x Spread fields in the register |
| Health dashboard fields | T001, T003 | Brooks-Health dimension and composite score fields in the register |
| Test quality fields | T001, T003 | Brooks-Test suite map, risk code, and test-layer fields in the register |
| Operational considerations | T002, T004, T006, T008 | History treatment, repeated run reconciliation, closure promotion |

## Open Decision Impact

| Decision | Impacted Requirements | Impacted Tasks | Blocking Scope |
|----------|-----------------------|----------------|----------------|
| D001 | Requirement 2, Requirement 3, Requirement 4 | T004, T007 | Determines whether implementation is docs-only or includes runtime validation. |
| D002 | Requirement 4 | T002, T007 | Determines whether `.brooks-lint-history.json` becomes durable tracked state. |
| D003 | Requirement 2, Requirement 5 | T005, T006 | Determines when findings move into backlog or roadmap. |
| D004 | Requirement 1, Requirement 3 | T001, T003 | Determines final finding ID namespace. |

## Reference Matrix

| Reference | Related Requirements | Related Tasks | Notes |
|-----------|----------------------|---------------|-------|
| Brooks architecture audit output | Requirement 1, Requirement 2, Requirement 3 | T001, T003, T005 | Provides seed findings. |
| Brooks tech debt assessment output | Requirement 1, Requirement 2, Requirement 3, Requirement 4 | T001, T003, T005 | Provides debt priority scores and remediation focus. |
| Brooks health dashboard output | Requirement 1, Requirement 2, Requirement 3, Requirement 4 | T001, T003, T005 | Provides composite score and cross-dimensional priorities. |
| Brooks test quality review output | Requirement 1, Requirement 2, Requirement 3, Requirement 4 | T001, T003, T005 | Provides suite map, test-quality score, and test-specific findings. |
| `.brooks-lint-history.json` | Requirement 4 | T002, T007 | Provides score history. |
| `docs/backlog/README.md` | Requirement 2, Requirement 5 | T006, T008 | Destination for deferred findings. |
| `docs/roadmap/README.md` | Requirement 5 | T006, T008 | Destination for larger remediation sequences. |
