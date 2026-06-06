---
title: Spec lifecycle validation tasks
doc_type: tasks
artifact_type: tasks
status: archived
owner: platform
last_reviewed: 2026-06-06
---

# Tasks

**Input**: `docs/specs/002-spec-lifecycle-validation/`
**Prerequisites**: `requirements.md` and `design.md`

## Task Dependency Graph

```text
T001 -> T002 -> T003 -> T004 -> T006 -> T008
T001 -> T005 -> T006
T006 -> T007 -> T008
T008 -> T009
T009 -> T010
```

## Phase 1: Spec Package Setup

- [x] T001 Create validation spec package.
  - Depends on: none
  - Files: `docs/specs/002-spec-lifecycle-validation/`
  - Acceptance: Validation package exists and all requested validation-plan
    steps are represented.
  - Evidence: Created `requirements.md`, `design.md`, `tasks.md`, and
    `verification.md`.

## Phase 2: Fixtures And Static Checks

- [x] T002 Create scenario fixtures.
  - Depends on: T001
  - Files: `tests/fixtures/skill-validation/`
  - Acceptance: Six fixture directories exist with enough docs for prompt
    trials.
  - Evidence: Created six fixture directories under
    `tests/fixtures/skill-validation/`.

- [x] T003 Run static consistency checks.
  - Depends on: T002
  - Files: `skills/spec-lifecycle-manager/`,
    `.codex/skills/spec-lifecycle-manager/`, `docs/`
  - Acceptance: Static check results are recorded in validation evidence with
    pass/fail status.
  - Evidence: Static checks passed: no duplicate docs spec-package templates,
    repo-local skill matched source, Markdown links resolved, and required
    fields were found.

## Phase 3: Agent Trials

- [x] T004 Run prompt trial agents.
  - Depends on: T003
  - Files: `docs/specs/002-spec-lifecycle-validation/validation-evidence.md`
  - Acceptance: Prompt-trial evidence covers bug fix, old-format resume,
    completed close, external partition, fresh feature, and governance conflict.
  - Evidence: Linnaeus and Mendel sub-agents completed six prompt trials with
    pass results.

- [x] T005 Run review matrix agents.
  - Depends on: T001
  - Files: `docs/specs/002-spec-lifecycle-validation/validation-evidence.md`
  - Acceptance: Review findings are recorded with severity, evidence, and
    follow-up.
  - Evidence: Aristotle and Descartes sub-agents completed four review
    perspectives; non-blocking findings were fixed.

## Phase 4: Evidence And Closure

- [x] T006 Record validation evidence.
  - Depends on: T004, T005
  - Files: `docs/specs/002-spec-lifecycle-validation/validation-evidence.md`,
    `docs/specs/002-spec-lifecycle-validation/verification.md`
  - Acceptance: Evidence includes results, residual risk, and follow-up tasks
    or decisions.
  - Evidence: Recorded static checks, fixture inventory, prompt trials, review
    matrix, fixes, and residual risks in `validation-evidence.md`.

- [x] T007 Dogfood old-format archived spec.
  - Depends on: T006
  - Files: `docs/specs/001-spec-lifecycle-manager-skill/`,
    `docs/specs/002-spec-lifecycle-validation/validation-evidence.md`
  - Acceptance: Evidence shows whether to continue old format, migrate, or
    create a follow-up migration task.
  - Evidence: Recorded old-format archived spec trial in
    `validation-evidence.md`; selected continue old format/no migration.

- [x] T008 Review dogfood friction.
  - Depends on: T007
  - Files: `docs/specs/002-spec-lifecycle-validation/verification.md`
  - Acceptance: Dogfood assessment is recorded with keep/change
    recommendations.
  - Evidence: Dogfood assessment recorded in `validation-evidence.md`; artifact
    overhead noted as residual process cost.

- [x] T009 Final validation readiness.
  - Depends on: T008
  - Files: `docs/specs/002-spec-lifecycle-validation/tasks.md`,
    `docs/specs/002-spec-lifecycle-validation/verification.md`
  - Acceptance: Validation plan is complete or remaining risk is explicitly
    deferred.
  - Evidence: Task statuses updated; verification record updated with pass
    status and residual risks.

- [x] T010 Normalize package to current lint expectations.
  - Depends on: T009
  - Files: `docs/specs/002-spec-lifecycle-validation/requirements.md`,
    `docs/specs/002-spec-lifecycle-validation/design.md`,
    `docs/specs/002-spec-lifecycle-validation/tasks.md`,
    `docs/specs/002-spec-lifecycle-validation/verification.md`,
    `docs/specs/002-spec-lifecycle-validation/traceability.md`
  - Acceptance: Package metadata, durable baseline, task checklist shape, and
    evidence log satisfy the current runtime lint profile.
  - Evidence: Package normalized before closure; lint and closure-check
    commands recorded in `verification.md`.

## Status Legend

| Status | Meaning |
|--------|---------|
| pending | Not yet started |
| in_progress | Currently being worked on |
| done | Complete and verified |
| skipped | Intentionally deferred with documented reason |

## Related Artifacts

- Requirements: requirements.md
- Design: design.md
- Verification: verification.md
