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

Task markers:

- `[ ]`: pending or not started.
- `[~]`: in progress. Mark the selected task this way before starting work.
- `[/]`: partial. Some work is complete, but acceptance criteria are not fully met.
- `[>]`: follow-up or routed. Work moved to another task, spec, backlog item,
  issue, or owner; record `Destination:`.
- `[-]`: no-op or deferred. Work is intentionally unnecessary, not applicable,
  superseded, raw-only, or deferred from this spec.
- `[?]`: review or decision needed. Record `Decision owner:` when known.
- `[!]`: attention needed. A blocker, error, or intervention needs diagnosis.
- `[x]`: complete and verified.

Legacy markers remain readable during migration: `[Y]` maps to `partial`;
`[*]` and `[e]` map to `attention`.

Optional metadata fields:

- `Evidence mode:` one of `implementation`, `validation`, `planner`,
  `contract`, `dry_run`, `routing`, `no_op`, or `blocked_output`.
- `Follow-up:` human-readable remaining work.
- `Destination:` routed backlog item, spec, task ID, issue, or owner.
- `Decision owner:` role, person, or team responsible for review or sign-off.
- `Upstream specs:` specs or task IDs that must be trusted before completion.
- `Downstream specs:` specs or task IDs that depend on this task's state.

## Task Dependency Graph

```text
T001 -> T002
T001 -> T003
T002 + T003 -> T004
T004 -> T005
T005 -> T006
T006 -> T007
T007 -> T008
T008 -> T009
T009 -> T010
T010 -> T011
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
    - Evidence mode: implementation
    - Evidence: Pending.
  - [/] T003.2 Add validation, logging, or operational guardrails.
    - Evidence mode: implementation
    - Evidence: Guardrail implementation started; edge-path validation remains.
  - [?] T003.3 Confirm optional integration policy.
    - Decision owner: platform-owner
    - Evidence mode: planner
    - Evidence: Awaiting decision before implementation.
  - [>] T003.4 Route out-of-scope migration cleanup.
    - Destination: `docs/backlog/README.md`
    - Evidence mode: routing
    - Follow-up: Track cleanup separately from this spec's acceptance.
    - Evidence: Migration cleanup is useful but not required for this slice.
  - [-] T003.5 Skip superseded compatibility path.
    - Evidence mode: no_op
    - Evidence: Superseded by the current compatibility contract.

- [ ] T004 Checkpoint - Foundation validation.
  - Depends on: T003
  - Files: `docs/specs/[###-feature-name]/verification.md`
  - Acceptance: Shared prerequisites are reviewed, required focused validation
    is run or explicitly waived, and any user questions are recorded before
    user-story work begins.
  - Validation: Run the focused validation command for shared contracts or
    record why no automated command applies.
  - Evidence: Pending.

## Phase 3: User Story 1 - Title (Priority: P1)

**Goal**: Brief description of what this story delivers.

**Independent Test**: How to verify this story works on its own.

- [ ] T005 [US1] Add tests for user story 1.
  - Depends on: T004
  - Files: `tests/path/to/test`
  - Acceptance: Tests define expected behavior and fail before implementation
    where practical.
  - Evidence: Pending.
  - [ ] T005.1 Cover success path.
  - [ ] T005.2 Cover validation or error path.
  - [ ] T005.3 Cover regression or edge case from requirements.
  - [ ] T005.4 Write property tests for user story 1 invariants where useful.
    - Properties: `CP-001`, `CP-002`
    - Validates: Requirement 1 acceptance criteria.
    - Framework: Use the repository's accepted property-test tool, or record the
      dependency decision before adding one.

- [ ] T006 [US1] Implement user story 1 behavior.
  - Depends on: T005
  - Files: `src/path/to/file`
  - Acceptance: User story 1 passes its independent test and satisfies linked
    acceptance criteria.
  - Evidence: Pending.
  - [ ] T006.1 Implement core behavior.
  - [ ] T006.2 Integrate with shared contracts or config.
  - [ ] T006.3 Update durable docs or mark the promotion target.

- [ ] T007 Checkpoint - User Story 1 validation.
  - Depends on: T006
  - Files: `docs/specs/[###-feature-name]/verification.md`
  - Acceptance: User Story 1 is independently functional, linked acceptance
    criteria and correctness properties are covered, and validation evidence is
    recorded before the next story starts.
  - Validation: Run the story's independent test command and any property-test
    command, or record a justified waiver.
  - Evidence: Pending.

## Phase 4: User Story 2 - Title (Priority: P2)

**Goal**: Brief description of what this story delivers.

**Independent Test**: How to verify this story works on its own.

- [ ] T008 [P] [US2] Add tests and implementation for user story 2.
  - Depends on: T007
  - Files: `src/path/to/file`, `tests/path/to/test`
  - Acceptance: User story 2 passes its independent test and does not regress
    user story 1.
  - Evidence: Pending.
  - [ ] T008.1 Add tests.
  - [ ] T008.2 Implement behavior.
  - [ ] T008.3 Run focused validation.

- [ ] T009 Checkpoint - Selected user-story validation.
  - Depends on: T008
  - Files: `docs/specs/[###-feature-name]/verification.md`
  - Acceptance: Selected user stories are independently functional and
    testable, cross-story regressions are checked, and unresolved questions are
    recorded before promotion work.
  - Validation: Run focused regression and property-test commands for the
    selected stories, or record justified waivers.
  - Evidence: Pending.

## Phase 5: Polish, Promotion, and Closure

**Purpose**: Finish quality gates, durable docs, and closure readiness.

- [ ] T010 Update durable documentation and promotion targets.
  - Depends on: T009
  - Files: `docs/...`
  - Acceptance: Durable docs describe the resulting current behavior or
    deferred follow-up is documented.
  - Evidence: Pending.

- [ ] T011 Checkpoint - Run required validation and record closure risk.
  - Depends on: T010
  - Files: `docs/specs/[###-feature-name]/verification.md`
  - Acceptance: Validation evidence, residual risk, rollback or closure notes,
    and follow-up owners are recorded.
  - Validation: Run the full validation suite required by `verification.md` or
    document each skipped command with a reason and residual risk.
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
- Split broad tasks before implementation when they cover multiple source
  families, evidence modes, implementation outcomes, validation surfaces,
  profiles, or cross-spec dependencies. Use subtasks with separate evidence
  rather than one checkbox for implementation, validation, routing, no-op, and
  blocked-output outcomes.
- Keep the checkbox/subtask structure as the default task shape.
- Before starting an implementation slice, mark the selected task or subtask as
  `[~]`.
- Use `[P]` only when a task can run in parallel without dependency or file
  conflicts.
- Use `Depends on:` for tasks whose execution order is not obvious from the
  phase order.
- Use checkpoint tasks for phase boundaries, subsystem boundaries, validation
  pauses, and human decision points. Keep checkpoints evidence-bearing and
  runnable; do not use bare prose checkpoints when a future agent must decide
  whether it is safe to proceed.
- When `requirements.md` contains Correctness Properties, add property-test
  tasks or subtasks that name the property IDs, linked requirements, framework
  choice, and validation command. Keep the framework language-appropriate and
  repository-approved.
- Check off subtasks as work progresses, but check off the parent task only when
  its acceptance criteria are met.
- A task is complete only when evidence is recorded. Evidence can be a command,
  test result, review note, screenshot, log, commit, or manual verification.
- `planner`, `contract`, `dry_run`, `routing`, `no_op`, and `blocked_output`
  evidence modes do not complete ordinary implementation tasks unless the task
  acceptance explicitly says that mode is sufficient.
- If validation cannot run, leave the task unchecked unless the acceptance
  criteria can be defensibly verified by another recorded method.
- Mark skipped work with an explicit reason, for example:
  `- [ ] T009 ...`
  `  - Status: skipped - superseded by T014.`
- Mark partial, routed, review-needed, or attention-needed work with the
  relevant marker and reason, for
  example:
  `- [/] T009 ...`
  `  - Status: partial - local validation passed; production evidence remains.`
  `- [>] T010 ...`
  `  - Destination: docs/backlog/README.md`
  `  - Evidence: routed - cleanup belongs to a follow-up backlog item.`
  `- [?] T011 ...`
  `  - Decision owner: platform-owner`
  `  - Evidence: waiting for owner decision on API shape.`
  `- [!] T012 ...`
  `  - Status: error - migration command fails with missing credential.`

## Related Artifacts

- Requirements:
- Change Impact:
- Design:
- Verification:
