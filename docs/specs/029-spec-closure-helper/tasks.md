---
title: Spec closure helper tasks
doc_type: spec
artifact_type: tasks
status: draft
authoring_mode: wizard
lifecycle_stage: tasks
owner: platform
last_reviewed: 2026-07-05
---

# Tasks

**Input**: `requirements.md`, `design.md`, and `traceability.md` in
`docs/specs/029-spec-closure-helper/`.

**Prerequisites**: Requirements and design reviewed; resolved design questions
recorded; MCP-first/runtime-recovery boundary accepted.

## Task Dependency Graph

```text
T001 -> T002
T002 -> T003
T002 -> T004
T002 -> T005
T003 + T004 + T005 -> T006
T006 -> T007
T007 -> T008
T008 -> T009
T008 -> T010
T009 + T010 -> T011
T011 -> T012
T012 -> T014
T014 -> T013
T013 -> T015
T015 -> T016
```

## Phase 1: Readiness And Baseline

**Purpose**: Freeze the implementation contract and build fixtures before
changing runtime behavior.

- [x] T001 Confirm task-stage readiness and implementation baseline.
  - Depends on: none
  - Requirements: Requirement 1, Requirement 2, Requirement 3, Requirement 4,
    Requirement 5, Requirement 6, Requirement 7, Requirement 8, Requirement 9,
    Requirement 10
  - Design: Overview, Components and Changes, Downstream Task Guidance
  - Files: `docs/specs/029-spec-closure-helper/requirements.md`,
    `docs/specs/029-spec-closure-helper/design.md`,
    `docs/specs/029-spec-closure-helper/tasks.md`,
    `docs/specs/029-spec-closure-helper/traceability.md`
  - Acceptance: Requirements, design, tasks, and traceability are internally
    consistent; no unresolved design question blocks implementation;
    verification planning is represented in task acceptance until
    `verification.md` is created during the validation checkpoint; the selected
    first implementation slice has Agent Readiness Contract coverage.
  - Validation: `mcp__spec_lifecycle_manager.lint_spec_package`;
    `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py lint docs/specs/029-spec-closure-helper`.
  - Evidence mode: contract
  - Evidence: MCP task_context for T001/T002 returned no traceability gaps; mcp__spec_lifecycle_manager.lint_spec_package reported 0 diagnostics; spec_runtime.py lint docs/specs/029-spec-closure-helper reported 0 diagnostics; Agent Readiness Contract for phase 1 recorded in session update before edits.

- [x] T002 Build spec 030 closure fixtures and expected durable-record samples.
  - Depends on: T001
  - Requirements: Requirement 1, Requirement 3, Requirement 6, Requirement 7,
    Requirement 9, Requirement 10
  - Design: Validation Strategy; Final Spec Commit Discovery; Metadata
    Rendering; Durable Record Ownership
  - Files: `tests/fixtures/`, `tests/runtime/test_spec_runtime.py`
  - Acceptance: Tests can exercise a completed-spec closure sequence with
    separate final spec commit, cleanup commit, pending cleanup placeholder,
    closure-log entry, archive-index row, stale active backlog wording, and
    historical references without mutating real repository history.
  - Validation: Focused fixture/unit tests are present and fail before the
    implementation where practical.
  - Evidence mode: implementation
  - Evidence: Added tests/fixtures/spec-closure-helper/spec-030-closure-scenario with pre-cleanup, placeholder-cleanup-hash, and resolved-cleanup-hash samples; added focused fixture integrity tests in tests/runtime/test_spec_runtime.py; PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_spec_runtime.SpecRuntimeTests.test_spec_030_closure_fixture_contains_required_closure_sequence tests.runtime.test_spec_runtime.SpecRuntimeTests.test_spec_030_closure_fixture_separates_pending_and_resolved_cleanup_metadata passed.

## Phase 2: Shared Closure Core

**Purpose**: Put all closure behavior behind one import-only implementation
path before exposing MCP or runtime entrypoints.

- [x] T003 Implement closure data models, parsing, validation, and status/action
  mapping.
  - Depends on: T002
  - Requirements: Requirement 7, Requirement 8, Requirement 10
  - Correctness: CP-002, CP-004, CP-006, CP-007, CP-009
  - Design: Data Models; status/action mapping; Error Handling
  - Files: `skills/spec-lifecycle-manager/scripts/lifecycle/closure.py`,
    `tests/runtime/test_spec_runtime.py`
  - Acceptance: `ClosureMetadata`, `ClosurePlan`, `ClosureAction`,
    `PlannedEdit`, `FilePrecondition`, and `ValidationCommand` are represented
    by typed internal objects or equivalent validated structures; invalid
    status/action combinations are rejected; serialized dict/JSON inputs are
    parsed before use.
  - Validation: Unit tests cover valid `removed`, `archived`, and
    `retained_as_history` mappings plus invalid combinations and pending
    cleanup metadata.
  - Evidence mode: implementation
  - Evidence: Added lifecycle/closure.py data models and parsing for ClosureMetadata, ClosurePlan, ClosureAction, PlannedEdit, FilePrecondition, and ValidationCommand; focused metadata mapping test passed; python3 -m py_compile lifecycle/closure.py passed; full Python suite passed 196 tests.

- [x] T004 Implement closure planning orchestration.
  - Depends on: T003
  - Requirements: Requirement 1, Requirement 2, Requirement 4, Requirement 7,
    Requirement 8
  - Correctness: CP-001, CP-003, CP-006
  - Design: Plan Flow; Function Signatures and Interfaces; Existing lifecycle
    module composition
  - Files: `skills/spec-lifecycle-manager/scripts/lifecycle/closure.py`,
    `skills/spec-lifecycle-manager/scripts/lifecycle/core.py`,
    `tests/runtime/test_spec_runtime.py`
  - Acceptance: `closure_plan` composes scan, closure check, promotion plan,
    durable evidence, follow-up/residual-risk checks, manual decisions,
    scriptable actions, stable plan/action/edit IDs, and file preconditions
    without mutating files.
  - Validation: Unit tests cover complete plans, blocked durable promotion,
    missing follow-up disposition, explicit `none` follow-ups, and dry-run
    default behavior.
  - Evidence mode: implementation
  - Evidence: Implemented closure_plan orchestration in lifecycle/closure.py with closure check, promotion plan, durable evidence, stable plan and action IDs, planned edits, file preconditions, and validation commands; focused closure_plan tests passed; full Python suite passed 196 tests.

- [x] T005 Implement final spec commit discovery and active-reference
  classification.
  - Depends on: T003
  - Requirements: Requirement 3, Requirement 6
  - Correctness: CP-002, CP-005, CP-008
  - Design: Final Spec Commit Discovery; Active Reference Classification
  - Files: `skills/spec-lifecycle-manager/scripts/lifecycle/closure.py`,
    `tests/runtime/test_spec_runtime.py`
  - Acceptance: Candidate commits are reported with evidence and confidence;
    the helper never invents or silently chooses between plausible commits;
    active stale references are distinguished from historical closure/archive
    references and validation fixtures.
  - Validation: Git fixture tests and reference-classifier tests cover spec 030
    style history, multiple candidate commits, missing Git evidence, active
    backlog references, and historical archive references.
  - Evidence mode: implementation
  - Evidence: Implemented final spec commit candidate discovery and active-reference classification in lifecycle/closure.py; reference classifier tests cover active backlog references and historical closure-log references; full Python suite passed 196 tests.

- [x] T006 Implement closure-log/archive-index rendering and durable record
  ownership diagnostics.
  - Depends on: T004, T005
  - Requirements: Requirement 7, Requirement 9, Requirement 10
  - Correctness: CP-004, CP-007, CP-009
  - Design: Metadata Rendering; Durable Record Ownership
  - Files: `skills/spec-lifecycle-manager/scripts/lifecycle/closure.py`,
    `tests/runtime/test_spec_runtime.py`
  - Acceptance: Closure-log sections and archive-index rows render from one
    canonical payload; owned fields are validated for missing, pending, invalid,
    or inconsistent values; arbitrary prose outside generated sections is not
    treated as helper-owned.
  - Validation: Snapshot or structured rendering tests cover closure log,
    archive index, drift detection, pending cleanup placeholders, and cleanup
    hash resolution previews.
  - Evidence mode: implementation
  - Evidence: Implemented closure-log and archive-index rendering from ClosureMetadata plus owned-field drift diagnostics; rendering and cleanup-hash placeholder fixture tests passed; full Python suite passed 196 tests.

- [x] T007 Implement planned edit application and cleanup hash resolution.
  - Depends on: T006
  - Requirements: Requirement 3, Requirement 8, Requirement 9
  - Correctness: CP-004, CP-006, CP-007
  - Design: Cleanup Flow; Resolve Flow; Planned Edit Application; Security,
    Trust, and Access
  - Files: `skills/spec-lifecycle-manager/scripts/lifecycle/closure.py`,
    `tests/runtime/test_spec_runtime.py`
  - Acceptance: Write actions require explicit `write_intent`, stable
    `action_id`, matching file preconditions, repo-root path normalization, and
    bounded declared targets; stale plans abort before writes; partial write
    failures report changed/intended files and recovery validation commands.
  - Validation: Tests cover dry-run, missing write intent, stale plan,
    path-traversal rejection, exact target scoping, pending cleanup hash
    replacement, and selected active-reference update behavior.
  - Evidence mode: implementation
  - Evidence: Implemented guarded planned edit application and cleanup-hash resolution with write_intent checks, path normalization, file preconditions, stale-plan rejection, bounded record writes, and cleanup-hash replacement; focused write guard tests passed; full Python suite passed 196 tests.

- [x] T008 Implement closure validation command planning.
  - Depends on: T007
  - Requirements: Requirement 5, Requirement 8, Requirement 9
  - Design: Validation Planning; Validation Strategy
  - Files: `skills/spec-lifecycle-manager/scripts/lifecycle/closure.py`,
    `tests/runtime/test_spec_runtime.py`
  - Acceptance: Plans include MCP-preferred tools, `spec_runtime.py` recovery
    commands, scan/archive/closure checks, `git diff --check`, and
    package-specific commands such as `package-contract`, `sync-guard`,
    `npm run validate`, and focused MCP/runtime tests when changed files require
    them.
  - Validation: Tests cover package repo, ordinary repo, history-only changes,
    lifecycle script changes, plugin bundle changes, and manual-only command
    classification.
  - Evidence mode: implementation
  - Evidence: Implemented closure validation command planning with MCP-preferred inventory, spec_runtime recovery commands, archive-index validation, git diff check, package-contract, sync-guard, runtime tests, and history fixture checks based on changed files; focused validation-plan test passed; full Python suite passed 196 tests.

## Phase 3: Public Interfaces

**Purpose**: Expose the shared helper through MCP first and retained runtime
recovery second, without duplicating closure logic.

- [x] T009 Add retained runtime recovery commands.
  - Depends on: T008
  - Requirements: Requirement 5, Requirement 8, Requirement 9
  - Design: Function Signatures and Interfaces; Migration and Compatibility
  - Files: `skills/spec-lifecycle-manager/scripts/lifecycle/runtime_adapter.py`,
    `skills/spec-lifecycle-manager/scripts/spec_runtime.py`,
    `tests/runtime/test_spec_runtime.py`
  - Acceptance: `closure-plan`, `closure-apply`, and `closure-resolve` runtime
    commands call `lifecycle/closure.py`; default to dry-run; require explicit
    write intent for mutation; emit deterministic JSON; and preserve existing
    CLI commands.
  - Validation: Runtime tests cover command parsing, JSON shape, dry-run
    defaults, write-intent errors, and no-MCP recovery usage.
  - Evidence mode: implementation
  - Evidence: Added closure-plan, closure-apply, and closure-resolve runtime recovery commands in lifecycle/runtime_adapter.py; commands call shared closure functions, default to dry-run, require write_intent for writes, emit JSON, and focused runtime CLI tests plus runtime/MCP modules passed.

- [x] T010 Add MCP closure tools over the shared helper.
  - Depends on: T008
  - Requirements: Requirement 5, Requirement 8, Requirement 9
  - Correctness: CP-006
  - Design: MCP server architecture; Function Signatures and Interfaces;
    Migration and Compatibility
  - Files: `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`,
    `tests/runtime/test_spec_mcp_server.py`
  - Acceptance: MCP exposes `closure_plan`, `closure_apply`, and
    `closure_resolve`; schemas are preview-first; write-capable calls require
    `write_intent`; handlers call shared closure internals directly and never
    route through `spec_runtime.py`.
  - Validation: MCP tests cover tool list/schema, dry-run responses,
    write-intent guards, structured error payloads, and shared-core call path.
  - Evidence mode: implementation
  - Evidence: Added MCP closure_plan, closure_apply, and closure_resolve tools in spec_mcp_server.py with preview-first schemas and write_intent guard; handlers call lifecycle_core shared closure functions directly; focused MCP tool tests plus runtime/MCP modules passed.

- [x] T011 Checkpoint - interface parity and no duplicate closure logic.
  - Depends on: T009, T010
  - Requirements: Requirement 8, Requirement 9, Requirement 10
  - Design: System Architecture; Migration and Compatibility
  - Files: `skills/spec-lifecycle-manager/scripts/lifecycle/closure.py`,
    `skills/spec-lifecycle-manager/scripts/lifecycle/runtime_adapter.py`,
    `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`,
    `tests/runtime/test_spec_runtime.py`,
    `tests/runtime/test_spec_mcp_server.py`
  - Acceptance: MCP and runtime surfaces expose compatible payload semantics
    while using a single shared implementation path for planning, rendering,
    classification, applying edits, and cleanup-hash resolution.
  - Validation: Focused runtime and MCP tests pass; static inspection confirms
    MCP handlers do not call `spec_runtime.py`.
  - Evidence mode: validation
  - Evidence: Confirmed runtime and MCP surfaces share lifecycle/closure.py through lifecycle_core exports; MCP handler inspection test confirms no spec_runtime.py or subprocess call in closure handlers; source, Codex plugin, and Claude plugin skill copies synced; package-contract passed.

## Phase 4: Durable Guidance, Bundles, And Packaging

**Purpose**: Keep agent-facing instructions, runtime reference docs, and plugin
copies consistent with the new write-capable MCP closure exception.

- [x] T012 Update durable MCP/write-boundary documentation.
  - Depends on: T011
  - Requirements: Requirement 5, Requirement 8, Requirement 10
  - Design: Components and Changes; Migration and Compatibility; Operational
    Considerations
  - Files: `skills/spec-lifecycle-manager/SKILL.md`,
    `docs/reference/spec-lifecycle-runtime.md`,
    `docs/design/spec-lifecycle-management.md`
  - Acceptance: Durable guidance no longer says `set_task_state` is the only
    write-capable MCP tool without qualification; closure write tools are
    documented as narrow preview-first exceptions; lifecycle judgment, durable
    promotion approval, final closure approval, and commits remain outside MCP
    automation.
  - Validation: `rg` confirms stale "only write-capable" and "MCP never edits
    durable docs/removes files" wording is updated or qualified.
  - Evidence mode: implementation
  - Evidence: Updated SKILL.md, spec-lifecycle-runtime.md, and spec-lifecycle-management.md to document closure_apply and closure_resolve as narrow preview-first write-capable exceptions; lifecycle judgment, durable-promotion approval, final closure approval, residual-risk acceptance, and commits remain outside MCP automation; stale wording rg check returned no matches.

- [x] T013 Sync plugin bundles and package surfaces.
  - Depends on: T014
  - Requirements: Requirement 5, Requirement 8, Requirement 10
  - Design: Components and Changes; Operational Considerations
  - Files: `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/`,
    `plugins/spec-lifecycle-manager/claude-plugin/skills/spec-lifecycle-manager/`,
    package manifests if generated by the sync flow
  - Acceptance: Bundled Codex and Claude plugin copies match source skill,
    runtime, MCP, prompt/reference, and tests expectations; package metadata
    remains valid.
  - Validation: `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py sync-guard . --commits 5`;
    `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py package-contract .`.
  - Evidence mode: implementation
  - Evidence: Synced updated SKILL.md into Codex and Claude plugin skill copies; package-contract passed with source bundle and source Claude parity in_sync; sync-guard confirmed source-to-bundle parity and reported only installed cache refresh advisory outside source package surfaces.

## Phase 5: End-To-End Validation And Review

**Purpose**: Prove the helper reduces closure toil without weakening closure
judgment, durable promotion, or recovery evidence.

- [x] T014 Add end-to-end dry-run coverage using the spec 030 closure scenario.
  - Depends on: T012
  - Requirements: Requirement 1, Requirement 3, Requirement 4, Requirement 6,
    Requirement 7, Requirement 9, Requirement 10
  - Correctness: CP-001, CP-002, CP-003, CP-004, CP-005, CP-007, CP-008,
    CP-009
  - Design: Validation Strategy; Plan Flow; Cleanup Flow; Resolve Flow
  - Files: `tests/runtime/test_spec_runtime.py`,
    `tests/runtime/test_spec_mcp_server.py`, `tests/fixtures/`
  - Acceptance: Dry-run coverage demonstrates plan, cleanup preview, pending
    cleanup metadata, active-reference reporting, cleanup-hash resolution, and
    final validation command planning for a spec 030-like closure without
    mutating real repository history.
  - Validation: Focused end-to-end runtime/MCP tests pass.
  - Evidence mode: validation
  - Evidence: Focused end-to-end runtime/MCP closure tests passed: plan preview, cleanup preview, cleanup placeholder metadata, active-reference classification, cleanup-hash resolution, and validation command planning for the spec 030 closure fixture.

- [x] T015 Run full package validation and record evidence.
  - Depends on: T013
  - Requirements: Requirement 1, Requirement 2, Requirement 3, Requirement 4,
    Requirement 5, Requirement 6, Requirement 7, Requirement 8, Requirement 9,
    Requirement 10
  - Design: Validation Strategy; Operational Considerations
  - Files: `docs/specs/029-spec-closure-helper/verification.md`,
    `tests/runtime/`, package/runtime docs
  - Acceptance: `verification.md` is created or updated with full validation
    evidence; failures are fixed or explicitly routed; residual reload/adoption
    risk is documented.
  - Validation:
    `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'`;
    `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py scan .`;
    `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py archive-index .`;
    `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py prompts .`;
    `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py package-contract .`;
    `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py sync-guard . --commits 5`;
    `npm run validate`;
    `git diff --check`.
  - Evidence mode: validation
  - Evidence: Created verification.md with full validation evidence; Python unittest suite passed 201 tests; scan, archive-index, prompts, package-contract, npm run validate, and git diff --check passed; sync-guard confirmed source/bundle parity with installed cache refresh advisory recorded as residual adoption risk.

- [ ] T016 Implementation review, promotion, and closure readiness checkpoint.
  - Depends on: T015
  - Requirements: Requirement 1, Requirement 2, Requirement 3, Requirement 4,
    Requirement 5, Requirement 6, Requirement 7, Requirement 8, Requirement 9,
    Requirement 10
  - Correctness: all
  - Design: Slice Boundary And Residual Architecture; Downstream Task Guidance;
    Operational Considerations
  - Files: `docs/specs/029-spec-closure-helper/verification.md`,
    durable docs updated by this spec, `docs/backlog/README.md` if follow-up
    routing is required
  - Acceptance: `verification.md` contains review findings, closure
    dispositions, and residual risks; findings are fixed, rejected with
    rationale, or routed to one durable destination; broad requirements and
    design targets have closure dispositions; durable docs describe accepted
    current behavior; unresolved work is routed before closure; active spec
    cleanup is not attempted until a final spec commit is available.
  - Validation: `mcp__spec_lifecycle_manager.lint_spec_package`;
    `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py closure-check docs/specs/029-spec-closure-helper`;
    `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py promotion-plan docs/specs/029-spec-closure-helper`.
  - Evidence mode: validation
  - Evidence: Pending.

## Execution Rules

- Do not implement from `tasks.md` alone. Start from the row for the selected
  task in `traceability.md`, then read the linked requirements, acceptance
  criteria, design sections, and verification expectations.
- Before starting a task, mark it `[~]` and preserve dependency, acceptance, and
  evidence fields.
- Check off a parent task only when all acceptance criteria are met and evidence
  is recorded.
- Keep MCP-first behavior for agent-facing lifecycle interactions. Use
  `spec_runtime.py` directly for CI, validation, MCP debugging, or no-MCP
  recovery.
- Do not add a separate closure implementation in MCP, runtime adapter, hooks,
  or docs. Shared behavior belongs in
  `skills/spec-lifecycle-manager/scripts/lifecycle/closure.py`.
- Treat `closure_apply` and `closure_resolve` as narrow write-capable
  exceptions. They must remain preview-first, explicit-write-intent, bounded to
  declared targets, and unable to approve closure judgment or commit changes.
