---
title: Canonical context warning noise tasks
doc_type: spec
artifact_type: tasks
status: draft
owner: platform
last_reviewed: 2026-07-05
---

# Tasks

**Input**: `requirements.md`, `design.md`, `traceability.md`
**Prerequisites**: Requirements and design accepted for implementation
planning.

## Task Dependency Graph

```text
T001 -> T013
T002 -> T013
T003 -> T013
T004 -> T013
T005 -> T013
T006 -> T013
T007 -> T013
T008 -> T013
T009 -> T013
T010 -> T013
T011 -> T013
T012 -> T013
T013 -> T014
T014 -> T015
T015 -> T016
T016 -> T017
T017 -> T018
T018 -> T019
T019 -> T020
T020 -> T021
T021 -> T022
T022 -> T023
T023 -> T024
T024 -> T025
T025 -> T026
T026 -> T027
T027 -> T028
T028 -> T029
T029 -> T030
T030 -> T031
T031 -> T032
```

## Phase 1: Runtime Test Contract

**Purpose**: Define the expected behavior before changing runtime logic.

- [x] T001 Add advisory metadata test for `CANONICAL_CONTEXT_MISSING`.
  - Depends on: none
  - Requirement: Requirement 1
  - Properties: CP-001
  - Files: `tests/runtime/test_spec_runtime.py`
  - Acceptance: A runtime test asserts the diagnostic is warning-level,
    advisory, and non-blocking.
  - Evidence mode: implementation
  - Evidence: Added `test_canonical_context_missing_diagnostic_is_advisory_and_non_blocking`.

- [x] T002 Add import-plan advisory test.
  - Depends on: none
  - Requirement: Requirement 1, Requirement 2
  - Properties: CP-001
  - Files: `tests/runtime/test_spec_runtime.py`
  - Acceptance: A runtime test asserts `import_plan` is present when useful but
    does not imply mandatory artifact creation.
  - Evidence mode: implementation
  - Evidence: Added `test_canonical_context_import_plan_remains_advisory`.

- [x] T003 Add small-spec no-backfill test.
  - Depends on: none
  - Requirement: Requirement 2
  - Properties: CP-001
  - Files: `tests/runtime/test_spec_runtime.py`
  - Acceptance: A runtime test asserts a low-risk spec fixture proceeds without
    a separate `canonical-context.md`.
  - Evidence mode: implementation
  - Evidence: Added `test_low_risk_spec_does_not_require_canonical_context_backfill`; focused run covers the low-risk no-backfill fixture.

- [x] T004 Add promotion-only false-positive test.
  - Depends on: none
  - Requirement: Requirement 3
  - Properties: CP-003
  - Files: `tests/runtime/test_spec_runtime.py`
  - Acceptance: A runtime test asserts promotion-only wording does not emit
    `imported-source-risk`.
  - Evidence mode: implementation
  - Evidence: Added `test_promotion_only_wording_does_not_emit_imported_source_risk`.

- [x] T005 Add closure/archive false-positive test.
  - Depends on: none
  - Requirement: Requirement 3
  - Properties: CP-002, CP-003
  - Files: `tests/runtime/test_spec_runtime.py`
  - Acceptance: A runtime test asserts historical package reference wording does
    not produce artifact-add guidance.
  - Evidence mode: implementation
  - Evidence: Added `test_historical_package_reference_does_not_emit_artifact_add_guidance`; focused run covers historical package reference wording.

- [x] T006 Add imported/adapted source positive test.
  - Depends on: none
  - Requirement: Requirement 3
  - Properties: CP-004
  - Files: `tests/runtime/test_spec_runtime.py`
  - Acceptance: A runtime test asserts copied, adapted, imported, or
    superseded source authority emits `imported-source-risk`.
  - Evidence mode: implementation
  - Evidence: Added `test_imported_or_adapted_source_authority_emits_imported_source_risk`; focused run covers imported/adapted positive detection.

- [x] T007 Add stale-doc positive test.
  - Depends on: none
  - Requirement: Requirement 3
  - Properties: CP-004
  - Files: `tests/runtime/test_spec_runtime.py`
  - Acceptance: A runtime test asserts stale durable-doc authority emits
    `stale-doc-risk`.
  - Evidence mode: implementation
  - Evidence: Added `test_stale_durable_doc_authority_emits_stale_doc_risk`; focused run covers stale-doc positive detection.

- [x] T008 Add conflicting-authority positive test.
  - Depends on: none
  - Requirement: Requirement 3
  - Properties: CP-004
  - Files: `tests/runtime/test_spec_runtime.py`
  - Acceptance: A runtime test asserts conflicting source-of-truth wording emits
    a canonical-context risk signal.
  - Evidence mode: implementation
  - Evidence: Added `test_conflicting_authority_wording_emits_canonical_context_signal`.

- [x] T009 Add ambiguous-authority review-confidence test.
  - Depends on: none
  - Requirement: Requirement 3
  - Properties: CP-001, CP-004
  - Files: `tests/runtime/test_spec_runtime.py`
  - Acceptance: A runtime test asserts ambiguous authority wording is returned
    as review-confidence guidance rather than mandatory artifact creation.
  - Evidence mode: implementation
  - Evidence: Added `test_ambiguous_authority_wording_returns_review_confidence`.

- [x] T010 Add readiness packet advisory semantics test.
  - Depends on: none
  - Requirement: Requirement 5
  - Properties: CP-005
  - Files: `tests/runtime/test_spec_runtime.py`
  - Acceptance: A runtime test asserts `agent_readiness_packet` exposes
    canonical-context diagnostics as advisory readiness guidance.
  - Evidence mode: implementation
  - Evidence: Added `test_agent_readiness_packet_exposes_canonical_context_as_advisory_guidance`.

- [x] T011 Add closure non-blocking test for missing optional context.
  - Depends on: none
  - Requirement: Requirement 5
  - Properties: CP-001, CP-005
  - Files: `tests/runtime/test_spec_runtime.py`
  - Acceptance: A runtime test asserts `closure_check` does not block solely
    because optional `canonical-context.md` is absent.
  - Evidence mode: implementation
  - Evidence: Added `test_closure_check_does_not_block_on_missing_optional_canonical_context`; focused run covers closure non-blocking behavior.

- [x] T012 Add MCP diagnostic parity test.
  - Depends on: none
  - Requirement: Requirement 5
  - Properties: CP-005
  - Files: `tests/runtime/test_spec_mcp_server.py`
  - Acceptance: An MCP server test asserts `lint_spec_package` returns
    canonical-context diagnostic fields that match shared runtime semantics.
  - Evidence mode: implementation
  - Evidence: Added `test_lint_spec_package_returns_shared_canonical_context_diagnostic_shape`.

- [x] T013 Checkpoint - runtime test contract is ready.
  - Depends on: T001, T002, T003, T004, T005, T006, T007, T008, T009, T010, T011, T012
  - Files: `tests/runtime/test_spec_runtime.py`,
    `tests/runtime/test_spec_mcp_server.py`
  - Acceptance: Focused tests exist for every correctness property.
  - Validation: Run the focused tests or record current expected failures.
  - Evidence mode: validation
  - Evidence: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_spec_runtime tests.runtime.test_spec_mcp_server` ran 165 tests and exercised the complete Phase 1 contract-test set.

## Phase 2: Shared Runtime Implementation

**Purpose**: Implement one normalized diagnostic path and consume it from the
existing lifecycle surfaces.

- [x] T014 Add normalized signal-context helper.
  - Depends on: T013
  - Requirement: Requirement 2, Requirement 3
  - Properties: CP-004
  - Files: `skills/spec-lifecycle-manager/scripts/lifecycle/core.py`
  - Acceptance: A shared helper returns canonical-context signals plus clear or
    review confidence.
  - Evidence mode: implementation
  - Evidence: Added `canonical_context_signal_context` in `core.py`; focused runtime tests pass.

- [x] T015 Keep `canonical_context_risk_signals` compatible.
  - Depends on: T014
  - Requirement: Requirement 5
  - Properties: CP-005
  - Files: `skills/spec-lifecycle-manager/scripts/lifecycle/core.py`
  - Acceptance: Existing callers that expect a signal list continue to receive
    a stable list.
  - Evidence mode: implementation
  - Evidence: `canonical_context_risk_signals` remains a signal-list compatibility wrapper over normalized signal context.

- [x] T016 Refine imported-source false-positive filtering.
  - Depends on: T015
  - Requirement: Requirement 3
  - Properties: CP-003
  - Files: `skills/spec-lifecycle-manager/scripts/lifecycle/core.py`
  - Acceptance: Promotion-only wording is not classified as imported-source
    authority by itself.
  - Evidence mode: implementation
  - Evidence: Imported-source detection excludes promotion-target-only wording; `test_promotion_only_wording_does_not_emit_imported_source_risk` passes.

- [x] T017 Add historical-reference filtering.
  - Depends on: T016
  - Requirement: Requirement 1, Requirement 3
  - Properties: CP-002
  - Files: `skills/spec-lifecycle-manager/scripts/lifecycle/core.py`
  - Acceptance: Closed, archived, removed, and historical package references do
    not produce active artifact-add guidance.
  - Evidence mode: implementation
  - Evidence: Historical package reference wording no longer produces artifact-add guidance; `test_historical_package_reference_does_not_emit_artifact_add_guidance` passes.

- [x] T018 Add ambiguous-authority review confidence.
  - Depends on: T017
  - Requirement: Requirement 3
  - Properties: CP-004
  - Files: `skills/spec-lifecycle-manager/scripts/lifecycle/core.py`
  - Acceptance: Weak authority wording without concrete source risk returns
    review confidence instead of mandatory artifact guidance.
  - Evidence mode: implementation
  - Evidence: Added uncertain authority signal handling and validated it with the focused runtime suite.

- [x] T019 Update diagnostic payload and wording.
  - Depends on: T018
  - Requirement: Requirement 1, Requirement 2
  - Properties: CP-001
  - Files: `skills/spec-lifecycle-manager/scripts/lifecycle/core.py`
  - Acceptance: `CANONICAL_CONTEXT_MISSING` returns the normalized diagnostic
    payload defined in `design.md#data-models`.
  - Evidence mode: implementation
  - Evidence: `CANONICAL_CONTEXT_MISSING` now carries advisory, blocking, confidence, recommendation, signals, and import-plan metadata; focused diagnostics tests pass.

- [x] T020 Align readiness packet consumption.
  - Depends on: T019
  - Requirement: Requirement 5
  - Properties: CP-005
  - Files: `skills/spec-lifecycle-manager/scripts/lifecycle/core.py`
  - Acceptance: `agent_readiness_packet` consumes normalized diagnostics
    without changing advisory diagnostics into implementation blockers.
  - Evidence mode: implementation
  - Evidence: `agent_readiness_packet` consumes normalized diagnostics as advisory guidance; readiness focused test passes.

- [x] T021 Confirm closure blocker separation.
  - Depends on: T020
  - Requirement: Requirement 5
  - Properties: CP-001, CP-005
  - Files: `skills/spec-lifecycle-manager/scripts/lifecycle/core.py`
  - Acceptance: `closure_check` preserves the blocker model defined in
    `design.md#algorithms-and-logic`.
  - Evidence mode: implementation
  - Evidence: `closure_check` remains separated from warning-level missing optional context; closure focused test passes.

## Phase 3: Agent Guidance, Durable Docs, and Bundles

**Purpose**: Align every user-facing surface with the accepted runtime
semantics.

- [ ] T022 Update source skill guidance.
  - Depends on: T021
  - Requirement: Requirement 4
  - Properties: CP-001, CP-002
  - Files: `skills/spec-lifecycle-manager/SKILL.md`
  - Acceptance: Skill guidance says `canonical-context.md` is optional,
    advisory, stage-aware, and triggered by concrete context risk.
  - Evidence mode: implementation
  - Evidence: Pending.

- [ ] T023 Update canonical-context prompt wording.
  - Depends on: T022
  - Requirement: Requirement 4
  - Properties: CP-001, CP-005
  - Files: `skills/spec-lifecycle-manager/prompts/`
  - Acceptance: Every prompt that mentions canonical context preserves advisory
    wording and stage order.
  - Evidence mode: implementation
  - Evidence: Pending.

- [ ] T024 Update fallback spec-package template wording.
  - Depends on: T023
  - Requirement: Requirement 4
  - Properties: CP-001
  - Files: `skills/spec-lifecycle-manager/references/spec-package/`
  - Acceptance: Templates distinguish embedded durable-source baseline from a
    separate optional `canonical-context.md` artifact.
  - Evidence mode: implementation
  - Evidence: Pending.

- [ ] T025 Update durable lifecycle documentation.
  - Depends on: T024
  - Requirement: Requirement 4
  - Properties: CP-001, CP-005
  - Files: `docs/design/spec-lifecycle-management.md`,
    `docs/reference/spec-lifecycle-runtime.md`
  - Acceptance: Durable docs describe the accepted advisory runtime semantics.
  - Evidence mode: implementation
  - Evidence: Pending.

- [ ] T026 Update B058 backlog state.
  - Depends on: T025
  - Requirement: Requirement 4
  - Properties: CP-005
  - Files: `docs/backlog/README.md`
  - Acceptance: B058 records the implemented outcome or closure-ready status
    according to repository backlog conventions.
  - Evidence mode: implementation
  - Evidence: Pending.

- [ ] T027 Sync Codex plugin bundle.
  - Depends on: T026
  - Requirement: Requirement 4
  - Properties: CP-005
  - Files: `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/`
  - Acceptance: The bundled Codex skill copy matches source changes required by
    this spec.
  - Evidence mode: implementation
  - Evidence: Pending.

- [ ] T028 Sync Claude plugin bundle.
  - Depends on: T027
  - Requirement: Requirement 4
  - Properties: CP-005
  - Files: `plugins/spec-lifecycle-manager/claude-plugin/skills/spec-lifecycle-manager/`
  - Acceptance: The bundled Claude skill copy matches source changes required
    by this spec.
  - Evidence mode: implementation
  - Evidence: Pending.

- [ ] T029 Checkpoint - prompt and bundle validation.
  - Depends on: T028
  - Files: `skills/spec-lifecycle-manager/prompts/`,
    `plugins/spec-lifecycle-manager/`
  - Acceptance: Prompt and bundle parity checks pass.
  - Validation: `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py prompts`; `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py package-contract .`; `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py sync-guard .`
  - Evidence mode: validation
  - Evidence: Pending.

## Phase 4: Verification and Closure Readiness

**Purpose**: Preserve evidence and prepare for implementation review and
closure workflow.

- [ ] T030 Create verification artifact.
  - Depends on: T029
  - Requirement: all
  - Properties: CP-001, CP-002, CP-003, CP-004, CP-005
  - Files: `docs/specs/031-canonical-context-warning-noise/verification.md`
  - Acceptance: `verification.md` records focused tests, package checks, full
    validation, residual risk, and reload/install notes.
  - Evidence mode: implementation
  - Evidence: Pending.

- [ ] T031 Run final validation bundle.
  - Depends on: T030
  - Requirement: all
  - Properties: CP-001, CP-002, CP-003, CP-004, CP-005
  - Files: repository validation surfaces
  - Acceptance: The final validation commands pass.
  - Validation: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'`; `npm run validate`; `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py lint docs/specs/031-canonical-context-warning-noise`; `git diff --check`
  - Evidence mode: validation
  - Evidence: Pending.

- [ ] T032 Prepare implementation review and closure handoff.
  - Depends on: T031
  - Requirement: all
  - Properties: CP-001, CP-002, CP-003, CP-004, CP-005
  - Files: `docs/specs/031-canonical-context-warning-noise/`
  - Acceptance: The implementation review and closure-readiness disposition is
    recorded before closure starts.
  - Validation: `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py closure-check docs/specs/031-canonical-context-warning-noise`
  - Evidence mode: validation
  - Evidence: Pending.

## Execution Rules

- Do not implement from `tasks.md` alone. Use
  `docs/specs/031-canonical-context-warning-noise/traceability.md` or MCP
  `traceability_lookup` for the selected task, then read linked requirements
  and design sections.
- Before starting a task, mark it `[~]`; mark it `[x]` only after acceptance is
  met and concrete evidence is recorded.
- Keep runtime behavior in shared lifecycle internals. MCP and CLI adapters
  should handle interface concerns only.
- Do not make canonical context a hard phase gate in this spec.
- Split any task before implementation if it starts to require multiple
  independent evidence modes or file-family outcomes.
