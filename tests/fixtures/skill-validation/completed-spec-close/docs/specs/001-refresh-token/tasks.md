# Tasks

## Task Dependency Graph

```text
T001 -> T002 -> T003
```

### Task 1: Tests

- **ID:** T001
- **Status:** done
- **Depends on:** []
- **Parallel:** no
- **Story:** US1
- **Files:** `tests/auth-refresh.test.ts`
- **Description:** Add refresh token rotation coverage.
- **Acceptance:** Tests cover success and reuse rejection.
- **Evidence:** `npm test -- auth-refresh` passed in prior run.

### Task 2: Implementation

- **ID:** T002
- **Status:** done
- **Depends on:** [T001]
- **Parallel:** no
- **Story:** US1
- **Files:** `src/auth/refresh.ts`
- **Description:** Implement token rotation.
- **Acceptance:** Tests pass and old token reuse is rejected.
- **Evidence:** Implementation merged in fixture.

### Task 3: Durable Docs

- **ID:** T003
- **Status:** pending
- **Depends on:** [T002]
- **Parallel:** no
- **Story:** US1
- **Files:** `docs/requirements/auth.md`, `docs/runbooks/auth.md`
- **Description:** Promote refresh-token behavior into durable docs.
- **Acceptance:** Durable docs describe current behavior.
- **Evidence:** Pending.
