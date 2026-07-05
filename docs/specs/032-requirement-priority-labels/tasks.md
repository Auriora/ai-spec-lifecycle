---
title: Requirement priority labels tasks
doc_type: spec
artifact_type: tasks
status: draft
authoring_mode: wizard
lifecycle_stage: tasks
owner: platform
last_reviewed: 2026-07-05
backlog_item: B057
---

# Tasks

**Input**: `requirements.md`, `design.md`
**Prerequisites**: Requirements and design reviewed for MoSCoW priority labels.
**Traceability**: `traceability.md` maps every task to requirements,
acceptance criteria, correctness properties, design sections, validation, and
durable targets.

## Task Dependency Graph

```text
T001 -> T002 -> T003 -> T004
T004 -> T005 -> T006 -> T007 -> T008
T008 -> T009 -> T010 -> T011
T011 -> T012 -> T013 -> T014 -> T015
T015 -> T016 -> T017 -> T018
```

## Phase 1: Shared Parser Foundation

**Purpose**: Establish one parser and lint path before propagating priority
through readiness, traceability, and closure.

- [ ] T001 Add requirement priority parser fixtures and unit tests.
  - Depends on: none
  - Requirement: Requirement 1, Requirement 2
  - Properties: CP-001, CP-005
  - Files: `tests/runtime/test_spec_runtime.py`,
    `tests/fixtures/requirement-priority-labels/`
  - Acceptance: Tests cover unlabeled requirements, canonical `must-have`,
    `should-have`, `could-have` labels, duplicate priority lines, persisted
    shorthand labels, unknown labels, and `won't-have` as an invalid accepted
    requirement priority.
  - Evidence mode: implementation
  - Evidence: Pending.

- [ ] T002 Implement a shared requirement parser used by runtime paths.
  - Depends on: T001
  - Requirement: Requirement 1, Requirement 3
  - Properties: CP-004, CP-005
  - Files: `skills/spec-lifecycle-manager/scripts/lifecycle/requirements.py`,
    `skills/spec-lifecycle-manager/scripts/lifecycle/core.py`,
    `skills/spec-lifecycle-manager/scripts/lifecycle/traceability.py`
  - Acceptance: Requirement parsing, acceptance-criteria extraction, and
    optional priority parsing live behind one shared implementation consumed by
    `core.py` and `traceability.py`; existing requirement IDs and acceptance
    criteria remain backward compatible.
  - Evidence mode: implementation
  - Evidence: Pending.
  - [ ] T002.1 Add the shared parser module and preserve existing requirement
    block payload fields.
  - [ ] T002.2 Return optional `priority` on requirement records when present.
  - [ ] T002.3 Return structured parser diagnostics without making missing
    priority a diagnostic.
  - [ ] T002.4 Update current `core.py` callers to use the shared parser.
  - [ ] T002.5 Update `traceability.py` requirement collection to use the
    shared parser.

- [ ] T003 Integrate priority diagnostics into requirements lint.
  - Depends on: T002
  - Requirement: Requirement 1, Requirement 2, Requirement 4
  - Properties: CP-001
  - Files: `skills/spec-lifecycle-manager/scripts/lifecycle/core.py`,
    `tests/runtime/test_spec_runtime.py`
  - Acceptance: `lint_doc()` or `lint_spec_package()` reports duplicate,
    shorthand, unknown, and `won't-have` priority values in active
    `requirements.md` files; unlabeled active, closed, and removed specs are
    not failed solely for missing labels.
  - Evidence mode: implementation
  - Evidence: Pending.

- [ ] T004 Checkpoint - Shared parser validation.
  - Depends on: T003
  - Requirement: Requirement 1, Requirement 2
  - Files: `docs/specs/032-requirement-priority-labels/verification.md`
  - Acceptance: Focused parser and lint tests pass; any parser compatibility
    risk is recorded before coverage semantics are implemented.
  - Validation: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_spec_runtime`
  - Evidence mode: validation
  - Evidence: Pending.

## Phase 2: Readiness And Closure Semantics

**Purpose**: Make MoSCoW priority affect requirement coverage consistently
without changing task status semantics.

- [ ] T005 Add tests for priority-aware requirement coverage dispositions.
  - Depends on: T004
  - Requirement: Requirement 3
  - Properties: CP-002, CP-003, CP-004
  - Files: `tests/runtime/test_spec_runtime.py`,
    `tests/fixtures/requirement-priority-labels/`
  - Acceptance: Tests cover `must-have`, `should-have`, `could-have`, and
    unlabeled requirements across complete, partial-routed,
    partial-blocking, not-covered, out-of-scope, rejected, and
    human-superseded coverage rows.
  - Evidence mode: implementation
  - Evidence: Pending.

- [ ] T006 Implement the shared requirement coverage disposition helper.
  - Depends on: T005
  - Requirement: Requirement 3
  - Properties: CP-002, CP-003, CP-004
  - Files: `skills/spec-lifecycle-manager/scripts/lifecycle/core.py`
  - Acceptance: One helper reads parsed requirement priority and the
    Requirement To Delivery Matrix to classify coverage state, residual
    destination, blockers, and non-blocking residuals while preserving legacy
    unlabeled behavior.
  - Evidence mode: implementation
  - Evidence: Pending.
  - [ ] T006.1 Classify `must-have` incomplete coverage as blocking unless
    explicitly rejected or human-superseded.
  - [ ] T006.2 Classify `should-have` incomplete coverage as requiring route,
    rationale, or accepted residual risk.
  - [ ] T006.3 Classify `could-have` incomplete coverage as closable only when
    routed, rejected, or out of current scope.
  - [ ] T006.4 Preserve existing behavior when priority is absent.

- [ ] T007 Integrate priority coverage into readiness and closure outputs.
  - Depends on: T006
  - Requirement: Requirement 3, Requirement 4
  - Properties: CP-002, CP-003, CP-004
  - Files: `skills/spec-lifecycle-manager/scripts/lifecycle/core.py`,
    `tests/runtime/test_spec_runtime.py`
  - Acceptance: `stage_readiness`, `closure_check`, and closure-risk style
    output include requirement priority where requirement coverage is reported;
    `closure_check` includes blockers from the shared coverage helper.
  - Evidence mode: implementation
  - Evidence: Pending.

- [ ] T008 Checkpoint - Readiness and closure validation.
  - Depends on: T007
  - Requirement: Requirement 3
  - Files: `docs/specs/032-requirement-priority-labels/verification.md`
  - Acceptance: Focused runtime tests prove priority-aware readiness and
    closure behavior; legacy unlabeled fixtures still pass.
  - Validation: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_spec_runtime`
  - Evidence mode: validation
  - Evidence: Pending.

## Phase 3: Traceability, MCP, And Agent Context

**Purpose**: Ensure priority reaches the agent-facing surfaces that already
report requirements, without adding new tools or task-row duplication.

- [ ] T009 Add traceability and MCP priority propagation tests.
  - Depends on: T008
  - Requirement: Requirement 3, Requirement 4
  - Properties: CP-004, CP-005
  - Files: `tests/runtime/test_spec_runtime.py`,
    `tests/runtime/test_spec_mcp_server.py`,
    `tests/fixtures/requirement-priority-labels/`
  - Acceptance: Tests prove `traceability_lookup`, `task_context`, and
    `agent_readiness_packet` include priority on returned requirement objects
    when the source requirement has priority, even when task rows do not
    duplicate priority.
  - Evidence mode: implementation
  - Evidence: Pending.

- [ ] T010 Implement priority propagation through traceability and MCP paths.
  - Depends on: T009
  - Requirement: Requirement 3, Requirement 4
  - Properties: CP-004, CP-005
  - Files: `skills/spec-lifecycle-manager/scripts/lifecycle/traceability.py`,
    `skills/spec-lifecycle-manager/scripts/lifecycle/core.py`,
    `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`
  - Acceptance: Existing MCP handlers expose priority through shared runtime
    payloads without shelling out, adding a new MCP tool, or requiring task-row
    priority columns.
  - Evidence mode: implementation
  - Evidence: Pending.

- [ ] T011 Checkpoint - Agent context validation.
  - Depends on: T010
  - Requirement: Requirement 3, Requirement 4
  - Files: `docs/specs/032-requirement-priority-labels/verification.md`
  - Acceptance: Runtime and MCP tests pass for priority propagation, and the
    task context path remains backward compatible for unlabeled specs.
  - Validation: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_spec_runtime tests.runtime.test_spec_mcp_server`
  - Evidence mode: validation
  - Evidence: Pending.

## Phase 4: Authoring Surfaces And Durable Docs

**Purpose**: Make future specs and durable lifecycle docs teach the accepted
MoSCoW convention consistently.

- [ ] T012 Update source templates for MoSCoW priority labels.
  - Depends on: T011
  - Requirement: Requirement 1, Requirement 2, Requirement 4
  - Properties: CP-001, CP-005
  - Files: `skills/spec-lifecycle-manager/references/spec-package/requirements.md`,
    `skills/spec-lifecycle-manager/references/spec-package/traceability.md`
  - Acceptance: Requirements template shows `**Priority:** must-have` at
    requirement level; traceability template supports requirement-level
    `Priority` where it helps closure reconciliation; no template requires
    duplicate priority on every acceptance criterion.
  - Evidence mode: implementation
  - Evidence: Pending.

- [ ] T013 Update prompts and skill guidance.
  - Depends on: T012
  - Requirement: Requirement 4
  - Files: `skills/spec-lifecycle-manager/prompts/documentation-wizard.json`,
    `skills/spec-lifecycle-manager/prompts/lint-spec.json`,
    `skills/spec-lifecycle-manager/SKILL.md`
  - Acceptance: Wizard guidance asks for or infers priority at requirement
    level, normalizes shorthand before writing, and does not report missing
    labels as blocking by default; skill guidance describes MoSCoW semantics in
    authoring and closure review.
  - Evidence mode: implementation
  - Evidence: Pending.

- [ ] T014 Update durable runtime and lifecycle documentation.
  - Depends on: T013
  - Requirement: Requirement 3, Requirement 4
  - Files: `docs/design/spec-lifecycle-management.md`,
    `docs/reference/spec-lifecycle-runtime.md`
  - Acceptance: Durable docs explain the accepted priority syntax,
    compatibility behavior, affected runtime/MCP outputs, and closure
    reconciliation semantics.
  - Evidence mode: implementation
  - Evidence: Pending.

- [ ] T015 Sync bundled plugin copies and validate package parity.
  - Depends on: T014
  - Requirement: Requirement 4
  - Files: `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/`,
    `plugins/spec-lifecycle-manager/claude-plugin/skills/spec-lifecycle-manager/`
  - Acceptance: Source skill, prompts, templates, scripts, and bundled Codex
    and Claude plugin copies are aligned; package-contract and sync validation
    pass.
  - Validation: `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py prompts .`;
    package-contract and sync-guard commands from `npm run validate`
  - Evidence mode: validation
  - Evidence: Pending.

## Phase 5: Verification, Review, And Closure Preparation

**Purpose**: Prove the implementation, record evidence, and prepare the spec
for durable promotion and closure.

- [ ] T016 Consolidate verification evidence and run focused validation.
  - Depends on: T015
  - Requirement: Requirement 1, Requirement 2, Requirement 3, Requirement 4
  - Properties: CP-001, CP-002, CP-003, CP-004, CP-005
  - Files: `docs/specs/032-requirement-priority-labels/verification.md`
  - Acceptance: `verification.md` has updated quality gates, evidence log,
    residual risks, and focused test command results for parser, lint,
    readiness, closure, traceability, MCP, prompts, package-contract, and sync
    behavior.
  - Validation: Focused Python runtime/MCP tests, prompt validation, package
    contract, sync guard, and `git diff --check`.
  - Evidence mode: validation
  - Evidence: Pending.

- [ ] T017 Run full validation and address failures.
  - Depends on: T016
  - Requirement: Requirement 4
  - Files: `tests/`, `docs/specs/032-requirement-priority-labels/verification.md`
  - Acceptance: `npm run validate` passes or every skipped/failed command has
    a recorded reason, owner, and residual risk; verification evidence is
    updated with command output summary.
  - Validation: `npm run validate`
  - Evidence mode: validation
  - Evidence: Pending.

- [ ] T018 Review implementation, promote durable outcomes, and prepare closure.
  - Depends on: T017
  - Requirement: Requirement 1, Requirement 2, Requirement 3, Requirement 4
  - Properties: CP-001, CP-002, CP-003, CP-004, CP-005
  - Files: `docs/specs/032-requirement-priority-labels/verification.md`,
    `docs/backlog/README.md`, durable docs listed in requirements and design
  - Acceptance: Implementation review findings are fixed, rejected with
    rationale, or routed to one explicit destination; B057 is ready to mark
    done at closure; closure check is clean except for intentional final
    cleanup steps.
  - Validation: MCP `lint_spec_package`, MCP `closure_check`,
    implementation review packet, archive/closure validation during closeout.
  - Evidence mode: validation
  - Evidence: Pending.

## Execution Rules

- Do not implement from `tasks.md` alone. Before starting a task, read the
  linked requirement rows in `traceability.md`, the relevant sections of
  `requirements.md` and `design.md`, and any existing verification evidence.
- Before starting an implementation task, mark the selected task or subtask as
  `[~]`.
- Check off subtasks as work progresses, but mark the parent task `[x]` only
  when its acceptance criteria are met and concrete evidence is recorded.
- Keep parser, lint, readiness, closure, traceability, and MCP behavior on
  shared runtime logic. Do not duplicate priority semantics in MCP handlers.
- Preserve backward compatibility for unlabeled specs before adding stricter
  priority diagnostics.
- Use task-level validation evidence for focused checks, and reserve full
  validation for the final verification phase unless a broad shared change
  makes an earlier full run necessary.
