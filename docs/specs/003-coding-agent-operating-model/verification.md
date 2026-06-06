---
title: Coding agent operating model verification
doc_type: spec
artifact_type: verification
status: archived
owner: platform
last_reviewed: 2026-06-06
---

# Verification

## Scope

This verification record covers operating-model tasks T001 through T006:
research, spec creation, review against real workflows, local metrics, durable
destination decision, dogfood evidence, and closure readiness.

## Quality Gates

| Gate | Required? | Status | Evidence |
|------|-----------|--------|----------|
| Requirements acceptance criteria reviewed | yes | pass | Requirements 1-5 mapped to tasks and durable design. |
| Task evidence complete | yes | pass | `tasks.md` records evidence for T001-T006. |
| Automated tests pass or alternate verification recorded | yes | pass | Full regression tests passed on 2026-06-06. |
| Durable documentation updates identified | yes | pass | Durable design destination selected. |
| Durable documentation promoted or explicitly deferred | yes | pass | Operating model promoted to `docs/design/coding-agent-operating-model.md`; governance update deferred. |
| Governance or policy conflicts resolved | yes | pass | Model is guidance, not a new mandatory governance rule. |

## Validation Commands

| Command | Purpose | Result | Evidence |
|---------|---------|--------|----------|
| `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py lint docs/specs/003-coding-agent-operating-model` | Spec package lint | pass | 0 diagnostics. |
| `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py closure-check docs/specs/003-coding-agent-operating-model` | Closure readiness | pass | Ready, no blockers. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'` | Full regression tests | pass | 41 tests passed. |
| `git diff --check` | Diff whitespace hygiene | pass | No whitespace errors. |

## Evidence Log

| Date | Evidence | Result | Notes |
|------|----------|--------|-------|
| 2026-06-02 | Research reference created | pass | `docs/reference/coding-agent-workflow-research.md` records external evidence and recommendations. |
| 2026-06-06 | Low-risk direct patch review | pass | Spec metadata and closure-log evidence edits followed direct patch path with lint/diff evidence. |
| 2026-06-06 | Medium-risk behavior change review | pass | Archived scan hygiene used full spec/runtime/tests/docs flow. |
| 2026-06-06 | Higher-risk hook installation review | pass | Codex hook installation used advisory-only behavior, tests, docs, dogfood evidence, and rollback path. |
| 2026-06-06 | Durable destination decision | pass | Operating model promoted to durable design; governance update deferred. |
| 2026-06-06 | Closure validation | pass | Spec lint, closure check, full tests, and diff whitespace check passed. |

## Requirement Coverage

| Requirement | Acceptance criteria covered | Evidence | Residual risk |
|-------------|-----------------------------|----------|---------------|
| Requirement 1 | AC1, AC2, AC3 | Workflow levels and decision gates in durable design | Risk classification still requires operator judgment. |
| Requirement 2 | AC1, AC2, AC3 | Durable documentation boundary in durable design and lifecycle docs | None known. |
| Requirement 3 | AC1, AC2, AC3 | Evidence rules and completed lifecycle task records | None known. |
| Requirement 4 | AC1, AC2, AC3 | Agent role and parallelism rules | Multi-agent write coordination remains operator-mediated. |
| Requirement 5 | AC1, AC2, AC3 | Metrics section in durable design | Metrics are manual/lightweight for now. |

## Residual Risks

- The operating model is guidance, not enforced governance.
- Metrics are intentionally lightweight and may be inconsistently recorded.
- More evidence from non-documentation code changes would improve confidence.

## Task Evidence

| Task ID | Status | Evidence | Notes |
|---------|--------|----------|-------|
| T001 | complete | Research reference created. | Current as of this spec. |
| T002 | complete | Exploration spec package created. | Requirements, design, and tasks present. |
| T003 | complete | Reviewed against low-risk, medium-risk, and higher-risk lifecycle changes. | Findings promoted to durable design. |
| T004 | complete | Metrics defined in durable design. | Lightweight metrics only. |
| T005 | complete | Durable destination selected. | `docs/design/coding-agent-operating-model.md`. |
| T006 | complete | Dogfood evidence recorded. | No immediate skill or governance change required. |

## Durable Promotion And Cleanup

| Spec content | Durable destination or deferral | Status | Evidence |
|--------------|---------------------------------|--------|----------|
| Operating model | `docs/design/coding-agent-operating-model.md` | complete | Durable design added. |
| Research evidence | `docs/reference/coding-agent-workflow-research.md` | complete | Existing reference retained. |
| Governance policy | `docs/governance/constitution.md` | deferred | No mandatory policy change yet. |

### Spec Cleanup Decision

- **Cleanup action:** retain as history note
- **Reason:** The package records exploration history and evidence for the
  durable operating model.
- **Final spec commit:** `7ee157b`
- **Closure log path:** `docs/history/spec-closure-log.md`
- **Closure log entry updated:** yes
- **Closure cleanup commit:** `a86eaec`
- **Active indexes updated:** yes
- **Durable docs linked back to evidence where useful:** yes
- **Residual spec-only content:** Exploration evidence remains in spec 003 as
  retained history after closure.

## Ship Or Closure Risk

- **Risk level:** low
- **Breaking change:** no
- **Blast radius checked:** yes
- **Rollback path:** revert durable design doc and spec evidence updates
- **Requires human review:** optional
- **Release notes needed:** no
- **Follow-up issue or spec needed:** no

## Readiness Decision

- **Ready for promotion:** yes
- **Ready for release:** yes
- **Ready for closure:** yes.

## Related Artifacts

- Requirements: requirements.md
- Design: design.md
- Tasks: tasks.md
- Traceability: traceability.md
