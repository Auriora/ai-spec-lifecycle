---
title: Feature tasks title
doc_type: tasks
status: draft
owner: team-or-person
last_reviewed: YYYY-MM-DD
---

# Tasks

**Input**: Design documents from `docs/specs/[###-feature-name]/`
**Prerequisites**: `requirements.md` and `design.md`

## Task Dependency Graph

```text
T001 → T002 → T004
T001 → T003 → T004
T004 → T005
T004 → T006 (parallel)
T005 → T007
T006 → T007
```

## Phase 1: Setup

**Purpose**: Project initialization and shared preparation.

### Task 1: Title

- **ID:** T001
- **Status:** pending
- **Depends on:** []
- **Parallel:** no
- **Story:** —
- **Files:** `path/to/file`
- **Description:** What needs to be done.
- **Acceptance:** How to verify this task is complete.
- **Evidence:** Pending.

### Task 2: Title

- **ID:** T002
- **Status:** pending
- **Depends on:** [T001]
- **Parallel:** no
- **Story:** —
- **Files:** `path/to/file`
- **Description:** What needs to be done.
- **Acceptance:** How to verify this task is complete.
- **Evidence:** Pending.

## Phase 2: Foundation

**Purpose**: Shared work that must be complete before user-story implementation.

### Task 3: Title

- **ID:** T003
- **Status:** pending
- **Depends on:** [T001]
- **Parallel:** yes
- **Story:** —
- **Files:** `path/to/file`
- **Description:** What needs to be done.
- **Acceptance:** How to verify this task is complete.
- **Evidence:** Pending.

**Checkpoint**: Foundation ready; user-story work can proceed.

## Phase 3: User Story 1 - Title (Priority: P1)

**Goal**: Brief description of what this story delivers.

**Independent Test**: How to verify this story works on its own.

### Task 4: Tests for User Story 1

- **ID:** T004
- **Status:** pending
- **Depends on:** [T002, T003]
- **Parallel:** yes
- **Story:** US1
- **Files:** `tests/path/to/test`
- **Description:** Add unit and integration test coverage.
- **Acceptance:** Tests exist and define expected behavior before implementation.
- **Evidence:** Pending.

### Task 5: Implementation for User Story 1

- **ID:** T005
- **Status:** pending
- **Depends on:** [T004]
- **Parallel:** no
- **Story:** US1
- **Files:** `src/path/to/file`
- **Description:** Implement the feature behavior.
- **Acceptance:** Tests pass and behavior matches acceptance criteria.
- **Evidence:** Pending.

**Checkpoint**: User Story 1 is independently functional and testable.

## Phase 4: User Story 2 - Title (Priority: P2)

**Goal**: Brief description of what this story delivers.

**Independent Test**: How to verify this story works on its own.

### Task 6: Tests for User Story 2

- **ID:** T006
- **Status:** pending
- **Depends on:** [T004]
- **Parallel:** yes
- **Story:** US2
- **Files:** `tests/path/to/test`
- **Description:** Add unit and integration test coverage.
- **Acceptance:** Tests exist and define expected behavior before implementation.
- **Evidence:** Pending.

### Task 7: Implementation for User Story 2

- **ID:** T007
- **Status:** pending
- **Depends on:** [T005, T006]
- **Parallel:** no
- **Story:** US2
- **Files:** `src/path/to/file`
- **Description:** Implement the feature behavior.
- **Acceptance:** Tests pass and behavior matches acceptance criteria.
- **Evidence:** Pending.

**Checkpoint**: User Stories 1 and 2 both work independently.

## Phase 5: Polish and Cross-Cutting Concerns

**Purpose**: Final quality pass and documentation.

### Task 8: Documentation and Cleanup

- **ID:** T008
- **Status:** pending
- **Depends on:** [T007]
- **Parallel:** no
- **Story:** —
- **Files:** `docs/path/to/file`
- **Description:** Update durable docs, clean up code, verify performance budget.
- **Acceptance:** Docs reflect current behavior, no dead code, performance targets met.
- **Evidence:** Pending.

## Dependencies and Execution Order

- Setup starts first.
- Foundation blocks user-story work.
- User stories proceed in priority order unless dependencies allow parallel work.
- Polish and promotion happen after selected user stories are complete.
- Tests for a user story should be written before implementation where practical.
- Move tasks to `done` only after filling `Evidence` with the command, test
  result, review note, screenshot, log, commit, or manual verification note.

## Status Legend

| Status | Meaning |
|--------|---------|
| pending | Not yet started |
| in_progress | Currently being worked on |
| done | Complete and verified |
| skipped | Intentionally deferred with documented reason |

## Related Artifacts

- Requirements:
- Change Impact:
- Design:
- Verification:
