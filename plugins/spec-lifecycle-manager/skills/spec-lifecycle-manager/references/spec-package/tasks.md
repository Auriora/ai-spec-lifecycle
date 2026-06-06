---
title: Feature tasks title
doc_type: spec
artifact_type: tasks
status: draft
owner: team-or-person
last_reviewed: YYYY-MM-DD
---

# Tasks

**Input**: Design documents from `[docs-root]/specs/[###-feature-name]/`
**Prerequisites**: `requirements.md` and `design.md`

Use a Kiro-style checklist as the primary structure. Keep tasks readable and
execution-focused; add metadata only where it helps an agent choose the next
safe slice, verify completion, or promote durable docs.

## Task Dependency Graph

```text
T001 -> T002
T001 -> T003
T002 + T003 -> T004
T004 -> T005
T005 -> T006
```

## Phase 1: Setup

**Purpose**: Prepare the package and identify affected files.

- [ ] T001 Create or update the feature documentation structure under
  `[docs-root]/specs/[###-feature-name]/`.
  - Depends on: none
  - Requirement: -
  - Files: `[docs-root]/specs/[###-feature-name]/`
  - Acceptance: Package contains the required artifacts for this change.
  - Evidence: Pending.

- [ ] T002 Identify source, test, configuration, and durable-doc files affected
  by the change.
  - Depends on: T001
  - Requirement: -
  - Files: `src/...`, `tests/...`, `docs/...`
  - Acceptance: Affected file list is documented in `design.md`,
    `change-impact.md`, or this task.
  - Evidence: Pending.

## Phase 2: Foundation

**Purpose**: Complete shared prerequisites before user-story work.

- [ ] T003 Implement or update shared contracts, schemas, helpers,
  configuration, or guardrails needed by all stories.
  - Depends on: T001
  - Requirement: cross-cutting
  - Files: `path/to/file`
  - Acceptance: Shared prerequisite is implemented and covered by the relevant
    validation path.
  - Evidence: Pending.
  - [ ] T003.1 Add or update contract/schema definitions.
  - [ ] T003.2 Add validation, logging, or operational guardrails.
  - [ ] T003.3 Add focused tests for shared behavior.

**Checkpoint**: Foundation is ready; user-story work can proceed.

## Phase 3: User Story 1 - Title (Priority: P1)

**Goal**: Brief description of what this story delivers.

**Independent Test**: How to verify this story works on its own.

- [ ] T004 [US1] Add tests for user story 1.
  - Depends on: T002, T003
  - Files: `tests/path/to/test`
  - Acceptance: Tests define expected behavior and fail before implementation
    where practical.
  - Evidence: Pending.
  - [ ] T004.1 Cover success path.
  - [ ] T004.2 Cover validation or error path.
  - [ ] T004.3 Cover regression or edge case from requirements.

- [ ] T005 [US1] Implement user story 1 behavior.
  - Depends on: T004
  - Files: `src/path/to/file`
  - Acceptance: User story 1 passes its independent test and satisfies linked
    acceptance criteria.
  - Evidence: Pending.
  - [ ] T005.1 Implement core behavior.
  - [ ] T005.2 Integrate with shared contracts or config.
  - [ ] T005.3 Update durable docs or mark the promotion target.

**Checkpoint**: User Story 1 is independently functional and testable.

## Phase 4: User Story 2 - Title (Priority: P2)

**Goal**: Brief description of what this story delivers.

**Independent Test**: How to verify this story works on its own.

- [ ] T006 [P] [US2] Add tests and implementation for user story 2.
  - Depends on: T005
  - Files: `src/path/to/file`, `tests/path/to/test`
  - Acceptance: User story 2 passes its independent test and does not regress
    user story 1.
  - Evidence: Pending.
  - [ ] T006.1 Add tests.
  - [ ] T006.2 Implement behavior.
  - [ ] T006.3 Run focused validation.

**Checkpoint**: Selected user stories are independently functional and
testable.

## Phase 5: Polish, Promotion, and Closure

**Purpose**: Finish quality gates, durable docs, and closure readiness.

- [ ] T007 Update durable documentation and promotion targets.
  - Depends on: T005, T006
  - Files: `docs/...`
  - Acceptance: Durable docs describe the resulting current behavior or
    deferred follow-up is documented.
  - Evidence: Pending.

- [ ] T008 Run required validation and record closure risk.
  - Depends on: T007
  - Files: `docs/specs/[###-feature-name]/verification.md`
  - Acceptance: Validation evidence, residual risk, rollback or closure notes,
    and follow-up owners are recorded.
  - Evidence: Pending.

## Execution Rules

- Do not implement from `tasks.md` alone. Treat this file as the execution
  index for the package. Before implementing a task, review the linked
  requirements, acceptance criteria, design details, change-impact notes,
  verification expectations, durable-source baseline, and open decisions.
- If a task line is broad, vague, or sounds like planning work, resolve its
  concrete implementation meaning from `requirements.md`, `design.md`,
  `change-impact.md`, `verification.md`, and `open-decisions.md` before
  coding. Do not use vague task wording as a reason to skip implementation when
  the package contains enough detail elsewhere.
- Keep the checkbox/subtask structure as the default task shape.
- Use `[P]` only when a task can run in parallel without dependency or file
  conflicts.
- Use `Depends on:` for tasks whose execution order is not obvious from the
  phase order.
- Check off subtasks as work progresses, but check off the parent task only when
  its acceptance criteria are met.
- A task is complete only when evidence is recorded. Evidence can be a command,
  test result, review note, screenshot, log, commit, or manual verification.
- If validation cannot run, leave the task unchecked unless the acceptance
  criteria can be defensibly verified by another recorded method.
- Mark skipped work with an explicit reason, for example:
  `- [ ] T009 ...`
  `  - Status: skipped - superseded by T014.`

## Related Artifacts

- Requirements:
- Change Impact:
- Design:
- Verification:
