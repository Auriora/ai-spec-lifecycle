---
title: Spec-local canonical context tasks
doc_type: spec
artifact_type: tasks
status: active
owner: platform
last_reviewed: 2026-06-19
---

# Tasks

**Input**: `docs/specs/027-spec-local-canonical-context/requirements.md` and
`docs/specs/027-spec-local-canonical-context/design.md`

## Task Dependency Graph

```text
T001 -> T002 -> T003
T003 -> T004
T003 -> T005
T004 + T005 -> T006
T006 -> T007
T006 -> T008
T007 + T008 -> T009
```

## Phase 1: Design Decisions And Durable Guidance

**Purpose**: Land the authority model before templates or runtime checks encode
it.

- [ ] T001 Resolve canonical context artifact shape.
  - Depends on: none
  - Requirement: R1, R2, R3, R6
  - Files: `docs/specs/027-spec-local-canonical-context/design.md`,
    `docs/specs/027-spec-local-canonical-context/traceability.md`
  - Acceptance: D001 and D002 are resolved or explicitly deferred with owner,
    blocking status, and artifact destination.
  - Evidence mode: planner
  - Evidence: Pending.

- [ ] T002 Update durable lifecycle and operating-model docs.
  - Depends on: T001
  - Requirement: R1, R2, R4, R5
  - Files: `docs/design/spec-lifecycle-management.md`,
    `docs/design/coding-agent-operating-model.md`
  - Acceptance: Durable docs define spec-local canonical context, authority
    exceptions, stale-doc handling, and closure promotion discipline.
  - Evidence: Pending.

- [ ] T003 Update skill guidance for active implementation.
  - Depends on: T002
  - Requirement: R1, R2, R3, R4, R5
  - Files: `skills/spec-lifecycle-manager/SKILL.md`
  - Acceptance: Skill guidance tells agents how to discover, read, apply,
    reconcile, promote, and close spec-local canonical context.
  - Evidence: Pending.

## Phase 2: Templates And Runtime Support

**Purpose**: Make the model easy to use in new specs and visible in lifecycle
checks.

- [ ] T004 Add fallback template support.
  - Depends on: T003
  - Requirement: R1, R2, R3, R6
  - Files: `skills/spec-lifecycle-manager/references/spec-package/`
  - Acceptance: Fallback templates include canonical context guidance with
    always-canonical external sources, spec-canonical working sources, imported
    sources, non-canonical background sources, and promotion map examples.
  - Evidence: Pending.

- [ ] T005 Update spec creation and resume prompts.
  - Depends on: T003
  - Requirement: R1, R3, R4, R6, R7
  - Files: `skills/spec-lifecycle-manager/prompts/`,
    `skills/spec-lifecycle-manager/SKILL.md`
  - Acceptance: New-spec and resumed-spec flows proactively create a
    canonical-context artifact or return an import plan with target spec-local
    paths, import mode, canonical scope, and promotion target.
  - Evidence: Pending.

- [ ] T006 Add advisory runtime diagnostics and import-plan support.
  - Depends on: T003
  - Requirement: R1, R3, R4, R5, R6, R7
  - Files: `skills/spec-lifecycle-manager/scripts/spec_runtime.py`,
    `tests/runtime/`, `tests/fixtures/`
  - Acceptance: Lint, readiness, promotion, or closure checks warn about
    missing/incomplete canonical context only when durable-doc impact or
    stale-doc risk warrants it, and creation/resume support can produce an
    explicit canonical-context import plan.
  - Evidence: Pending.

## Phase 3: Validation, Documentation, And Closure Readiness

**Purpose**: Verify the behavior and prepare durable promotion before closure.

- [ ] T007 Update runtime reference, migration guidance, and traceability.
  - Depends on: T004, T006
  - Requirement: R4, R5, R6, R7
  - Files: `docs/reference/spec-lifecycle-runtime.md`,
    `skills/spec-lifecycle-manager/references/migration-guide.md`,
    `docs/specs/027-spec-local-canonical-context/traceability.md`,
    `docs/specs/027-spec-local-canonical-context/verification.md`
  - Acceptance: Durable docs and migration guidance describe any new artifact
    or diagnostic behavior, and traceability remains current.
  - Evidence: Pending.

- [ ] T008 Dogfood new-spec canonical context creation.
  - Depends on: T005, T006
  - Requirement: R7
  - Files: `docs/specs/027-spec-local-canonical-context/verification.md`
  - Acceptance: A dogfood run or deterministic fixture shows that a new spec
    with durable-doc context gets a canonical-context artifact or import plan
    without a second user prompt.
  - Evidence: Pending.

- [ ] T009 Checkpoint - validate and prepare promotion.
  - Depends on: T007, T008
  - Requirement: R1, R2, R3, R4, R5, R6, R7
  - Files: `docs/specs/027-spec-local-canonical-context/verification.md`,
    `docs/history/spec-closure-log.md`,
    `docs/history/spec-archive-index.md`
  - Acceptance: Required validation commands pass or have documented waivers;
    accepted spec content is promoted or mapped for closure; residual risks and
    follow-up destinations are recorded.
  - Validation: Run full unit tests, scan, package lint, prompt validation if
    prompts changed, archive-index when preparing closure, and `git diff
    --check`.
  - Evidence: Pending.

## Execution Rules

- Do not implement from `tasks.md` alone. Review linked requirements, design,
  change impact, traceability, and verification before editing.
- Keep diagnostics advisory and scoped until tests show they do not create
  broad false positives.
- Preserve the caveat that spec-local context does not override governance,
  policy, `AGENTS.md`, generated contracts, source-code contracts, or live
  evidence.
- Use repo-relative paths in user-facing docs and diagnostics.
