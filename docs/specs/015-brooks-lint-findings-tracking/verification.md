---
title: Brooks-Lint findings tracking verification
doc_type: spec
artifact_type: verification
status: draft
owner: platform
last_reviewed: 2026-06-09
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
| 2026-06-06 | Spec authoring | Initial spec package created. | superseded by final validation |
| 2026-06-06 | Brooks-Debt check | Tech Debt Assessment completed with score 84/100, 3 warnings, 1 suggestion; findings added to research and design seed lists. | captured as seed input |
| 2026-06-06 | Brooks-Health check | Health Dashboard completed with composite score 93/100; dimension scores and `BL-HEALTH-001` through `BL-HEALTH-005` added to research and design seed lists. | captured as seed input |
| 2026-06-06 | Brooks-Test check | Test Quality Review completed with score 89/100, 2 warnings, 1 suggestion; suite map and `BL-TEST-001` through `BL-TEST-003` added to research and design seed lists. | captured as seed input |
| 2026-06-09 | T001 | Added durable Brooks-Lint register schema in `docs/reviews/brooks-lint/README.md`; accepted D004 mode-specific ID namespace. | pass |
| 2026-06-09 | T002 | Accepted D002: `.brooks-lint-history.json` is optional supporting score-history evidence, while the Markdown register remains the durable finding source of truth. | pass |
| 2026-06-09 | T003 | Seeded `docs/reviews/brooks-lint/README.md` with `BL-ARCH-001` through `BL-ARCH-004`, `BL-DEBT-001` through `BL-DEBT-004`, `BL-HEALTH-001` through `BL-HEALTH-005`, and `BL-TEST-001` through `BL-TEST-003`; all seed findings preserve required fields. | pass |
| 2026-06-11 | T004 | Accepted D001 as Markdown-only first and documented maintenance rules in `docs/reviews/brooks-lint/README.md`; no runtime validation was added. | pass |
| 2026-06-11 | T005 | Triaged all seed findings into accepted, deferred, or dismissed states with rationales in `docs/reviews/brooks-lint/README.md`. | pass |
| 2026-06-11 | T006 | Accepted D003 and routed accepted/deferred findings to B016/R005, B026, B042, B043, or explicit no-action decisions. | pass |
| 2026-06-11 | T007 | Full validation commands passed before final spec commit. | pass |
| 2026-06-11 | T008 | Durable register, backlog, roadmap linkage, and closure targets prepared for final spec commit and cleanup. | pass |

## Residual Risks

| Risk | Status | Mitigation |
|------|--------|------------|
| Register may become stale after future Brooks runs. | mitigated | T004 defines append/reconcile rules and keeps validation Markdown-only until drift appears. |
| History file may be local telemetry rather than durable source. | mitigated | D002 treats score history as optional supporting evidence. |
| Findings may duplicate backlog items. | mitigated | T006 links duplicated findings to existing backlog/roadmap items or explicit no-action decisions. |

## Closure Readiness

This spec is ready for closure only when:

- The durable register exists or an explicit alternate location is accepted.
- Seed findings are recorded and triaged.
- Deferred or unresolved findings are promoted to backlog, roadmap, or a
  durable review register.
- Required validation commands pass and evidence is recorded.
