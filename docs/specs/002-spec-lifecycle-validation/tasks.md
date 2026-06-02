---
title: Spec lifecycle validation tasks
doc_type: tasks
status: draft
owner: platform
last_reviewed: 2026-06-02
---

# Tasks

**Input**: `docs/specs/002-spec-lifecycle-validation/`
**Prerequisites**: `requirements.md` and `design.md`

## Task Dependency Graph

```text
T001 -> T002 -> T003 -> T004 -> T006 -> T008
T001 -> T005 -> T006
T006 -> T007 -> T008
```

## Phase 1: Spec Package Setup

### Task 1: Create Validation Spec Package

- **ID:** T001
- **Status:** done
- **Depends on:** []
- **Parallel:** no
- **Story:** US5
- **Files:** `docs/specs/002-spec-lifecycle-validation/`
- **Description:** Create requirements, design, tasks, and verification artifacts for validation.
- **Acceptance:** Validation package exists and all requested validation-plan steps are represented.
- **Evidence:** Created `requirements.md`, `design.md`, `tasks.md`, and `verification.md`.

## Phase 2: Fixtures And Static Checks

### Task 2: Create Scenario Fixtures

- **ID:** T002
- **Status:** done
- **Depends on:** [T001]
- **Parallel:** no
- **Story:** US2
- **Files:** `tests/fixtures/skill-validation/`
- **Description:** Create fixtures for fresh feature, bug fix, old-format spec, external partition, completed spec, and governance conflict.
- **Acceptance:** Six fixture directories exist with enough docs for prompt trials.
- **Evidence:** Created six fixture directories under `tests/fixtures/skill-validation/`.

### Task 3: Run Static Consistency Checks

- **ID:** T003
- **Status:** done
- **Depends on:** [T002]
- **Parallel:** no
- **Story:** US1
- **Files:** `skills/spec-lifecycle-manager/`, `.codex/skills/spec-lifecycle-manager/`, `docs/`
- **Description:** Verify duplicate templates, referenced files, README links, and required template fields.
- **Acceptance:** Static check results are recorded in validation evidence with pass/fail status.
- **Evidence:** Static checks passed: no duplicate docs spec-package templates, repo-local skill matched source, Markdown links resolved, and required fields were found.

## Phase 3: Agent Trials

### Task 4: Run Prompt Trial Agents

- **ID:** T004
- **Status:** done
- **Depends on:** [T003]
- **Parallel:** yes
- **Story:** US3
- **Files:** `docs/specs/002-spec-lifecycle-validation/validation-evidence.md`
- **Description:** Use sub-agents with the repo-local skill to run fixture prompts and report expected vs actual behavior.
- **Acceptance:** Prompt-trial evidence covers bug fix, old-format resume, completed close, external partition, fresh feature, and governance conflict.
- **Evidence:** Linnaeus and Mendel sub-agents completed six prompt trials with pass results.

### Task 5: Run Review Matrix Agents

- **ID:** T005
- **Status:** done
- **Depends on:** [T001]
- **Parallel:** yes
- **Story:** US4
- **Files:** `docs/specs/002-spec-lifecycle-validation/validation-evidence.md`
- **Description:** Use sub-agents for Kiro workflow, durable-doc lifecycle, governance/evidence, and external-project cleanliness reviews.
- **Acceptance:** Review findings are recorded with severity, evidence, and follow-up.
- **Evidence:** Aristotle and Descartes sub-agents completed four review perspectives; non-blocking findings were fixed.

## Phase 4: Evidence And Closure

### Task 6: Record Validation Evidence

- **ID:** T006
- **Status:** done
- **Depends on:** [T004, T005]
- **Parallel:** no
- **Story:** US1-US5
- **Files:** `docs/specs/002-spec-lifecycle-validation/validation-evidence.md`, `docs/specs/002-spec-lifecycle-validation/verification.md`
- **Description:** Summarize static checks, fixture trials, prompt trials, review matrix, and dogfood findings.
- **Acceptance:** Evidence includes results, residual risk, and follow-up tasks or decisions.
- **Evidence:** Recorded static checks, fixture inventory, prompt trials, review matrix, fixes, and residual risks in `validation-evidence.md`.

### Task 7: Review Dogfood Friction

- **ID:** T007
- **Status:** done
- **Depends on:** [T006]
- **Parallel:** no
- **Story:** US5
- **Files:** `docs/specs/002-spec-lifecycle-validation/verification.md`
- **Description:** Assess whether using the new skill shape for this validation was useful or too heavy.
- **Acceptance:** Dogfood assessment is recorded with keep/change recommendations.
- **Evidence:** Dogfood assessment recorded in `validation-evidence.md`; artifact overhead noted as residual process cost.

### Task 8: Final Validation Readiness

- **ID:** T008
- **Status:** done
- **Depends on:** [T007]
- **Parallel:** no
- **Story:** US1-US5
- **Files:** `docs/specs/002-spec-lifecycle-validation/tasks.md`, `docs/specs/002-spec-lifecycle-validation/verification.md`
- **Description:** Mark accurate task statuses, record evidence, and identify any follow-up work.
- **Acceptance:** Validation plan is complete or remaining risk is explicitly deferred.
- **Evidence:** Task statuses updated; verification record updated with pass status and residual risks.

## Status Legend

| Status | Meaning |
|--------|---------|
| pending | Not yet started |
| in_progress | Currently being worked on |
| done | Complete and verified |
| skipped | Intentionally deferred with documented reason |

## Related Artifacts

- Requirements: requirements.md
- Change Impact:
- Design: design.md
- Verification: verification.md
