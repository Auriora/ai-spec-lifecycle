---
title: Brooks-Lint findings tracking verification
doc_type: spec
artifact_type: verification
status: draft
owner: platform
last_reviewed: 2026-06-06
---

# Verification

## Quality Gates

Run before implementation completion:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py scan .
PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py archive-index .
PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py prompts
PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py lint docs/specs/015-brooks-lint-findings-tracking
git diff --check
```

If runtime validation is added, include focused unit tests for the register
schema and plugin package sync if plugin runtime files change.

## Evidence Log

| Date | Task | Evidence | Result |
|------|------|----------|--------|
| 2026-06-06 | Spec authoring | Initial spec package created. | pending validation |
| 2026-06-06 | Brooks-Debt check | Tech Debt Assessment completed with score 84/100, 3 warnings, 1 suggestion; findings added to research and design seed lists. | pending validation |
| 2026-06-06 | Brooks-Health check | Health Dashboard completed with composite score 93/100; dimension scores and `BL-HEALTH-001` through `BL-HEALTH-005` added to research and design seed lists. | pending validation |
| 2026-06-06 | Brooks-Test check | Test Quality Review completed with score 89/100, 2 warnings, 1 suggestion; suite map and `BL-TEST-001` through `BL-TEST-003` added to research and design seed lists. | pending validation |
| 2026-06-09 | T001 | Added durable Brooks-Lint register schema in `docs/reviews/brooks-lint/README.md`; accepted D004 mode-specific ID namespace. | pass |
| 2026-06-09 | T002 | Accepted D002: `.brooks-lint-history.json` is optional supporting score-history evidence, while the Markdown register remains the durable finding source of truth. | pass |

## Residual Risks

| Risk | Status | Mitigation |
|------|--------|------------|
| Register may become stale after future Brooks runs. | open | T004 defines append/reconcile rules. |
| History file may be local telemetry rather than durable source. | open | D002 resolves treatment. |
| Findings may duplicate backlog items. | open | T006 requires routing or linking. |

## Closure Readiness

This spec is ready for closure only when:

- The durable register exists or an explicit alternate location is accepted.
- Seed findings are recorded and triaged.
- Deferred or unresolved findings are promoted to backlog, roadmap, or a
  durable review register.
- Required validation commands pass and evidence is recorded.
