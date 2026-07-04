---
title: Guided documentation wizard tasks
doc_type: spec
artifact_type: tasks
status: active
owner: platform
last_reviewed: 2026-07-04
---

# Tasks

**Input**: `docs/specs/026-guided-documentation-wizard/`
**Prerequisites**: `requirements.md`, `design.md`, `change-impact.md`,
`traceability.md`, and `verification.md`

## Task Dependency Graph

```text
T001 -> T002
T002 -> T003
T003 -> T004
T004 -> T005
T005 -> T006
T006 -> T007
```

## Phase 1: Scope And Contract

**Purpose**: Make the v1 wizard boundary explicit before editing runtime or
prompt files.

- [x] T001 Decide v1 wizard surface and feedback model.
  - Depends on: none
  - Requirement: R1, R3, R4, R5
  - Files: `docs/specs/026-guided-documentation-wizard/design.md`,
    `docs/specs/026-guided-documentation-wizard/traceability.md`
  - Acceptance: D001-D004 are resolved or explicitly deferred with owner,
    blocking status, and artifact destination.
  - Evidence: D001-D004 resolved 2026-06-17 by the spec owner and recorded in design.md (Open Questions) and traceability.md (Open Decision Impact): prompt-only surface (D001), reuse of the existing accept/revise/defer/reject/human-decision disposition shape (D002), one-question-default pacing with checklist on request (D003), manual-only write boundary for v1 (D004). Downstream tasks T002 and T006 can proceed against these decisions; T003 marked no-op per D001.

## Phase 2: Prompt And Guidance

**Purpose**: Add guided user-facing behavior without creating a second lifecycle
engine.

- [x] T002 Add guided documentation prompt guidance.
  - Depends on: T001
  - Requirement: R1, R2, R3, R4, R5, R6
  - Files: `skills/spec-lifecycle-manager/prompts/`,
    `skills/spec-lifecycle-manager/SKILL.md`,
    `tests/runtime/test_spec_runtime.py`
  - Acceptance: Prompt guidance tells agents to ask one stage-specific question
    at a time, report expected answer shape, classify feedback, and keep edits
    preview-first.
  - Evidence: 2026-07-04 added
    `skills/spec-lifecycle-manager/prompts/documentation-wizard.json`,
    updated `skills/spec-lifecycle-manager/prompts/README.md`, added
    `documentation-wizard` tests in `tests/runtime/test_spec_runtime.py`, and
    updated `skills/spec-lifecycle-manager/SKILL.md` with open-question,
    feedback-disposition, stage-order, and preview-plan guidance.

- [x] T003 Implement deterministic wizard runtime if approved for v1.
  - Depends on: T001
  - Requirement: R1, R2, R3, R4, R5, R6, R7
  - Files: `skills/spec-lifecycle-manager/scripts/spec_runtime.py`,
    `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`,
    `tests/runtime/test_spec_runtime.py`,
    `tests/runtime/test_spec_mcp_server.py`
  - Acceptance: If runtime/MCP is approved for v1, runtime or MCP wizard output
    reports stage, next question, open questions, feedback dispositions, preview
    edit plan, readiness, validation commands, and residual risk. If runtime/MCP
    is not approved for v1, record the no-op decision and keep coverage in the
    prompt contract.
  - Evidence: Not building per D001 (resolved 2026-06-17: v1 is prompt-only). Runtime/MCP design removed from design.md.
  - [x] T003.1 Add read-only runtime payload and CLI command.
  - Evidence: D001 resolved v1 as prompt-only in `docs/specs/026-guided-documentation-wizard/design.md`; `skills/spec-lifecycle-manager/scripts/spec_runtime.py` has no wizard CLI change for this spec.
  - [x] T003.2 Add MCP tool only if the runtime surface is accepted for v1.
  - Evidence: D001 resolved v1 as prompt-only in `docs/specs/026-guided-documentation-wizard/design.md`; `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py` has no wizard MCP tool change for this spec.
  - [x] T003.3 Cover CP-001 through CP-005 in focused tests.
  - Evidence: CP-001 through CP-005 are covered by the prompt-contract test added 2026-07-04 in `tests/runtime/test_spec_runtime.py` for the D001 prompt-only surface.
## Phase 3: Durable Documentation

**Purpose**: Promote accepted wizard behavior into durable current-state docs.

- [x] T004 Promote wizard behavior to durable docs.
  - Depends on: T002, T003
  - Requirement: R6, R7
  - Files: `docs/design/spec-lifecycle-management.md`,
    `docs/reference/spec-lifecycle-runtime.md`,
    `docs/backlog/README.md`
  - Acceptance: Durable docs describe the accepted wizard behavior, runtime or
    prompt surface, read-only/write boundary, and overlapping backlog routing.
  - Evidence: 2026-07-04 promoted prompt-only wizard behavior to
    `docs/design/spec-lifecycle-management.md`,
    `docs/reference/spec-lifecycle-runtime.md`, and
    `docs/backlog/README.md`, including read-only composition,
    one-question-default pacing, feedback dispositions, preview-first edit
    plans, durable promotion visibility, and removed-spec handling.

- [x] T005 Mirror plugin bundles if skill, prompt, or runtime files change.
  - Depends on: T002, T003
  - Requirement: R6
  - Files: `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/`,
    `plugins/spec-lifecycle-manager/claude-plugin/skills/spec-lifecycle-manager/`
  - Acceptance: Source, Codex bundle, and Claude bundle contain equivalent
    prompt/runtime/skill changes where packaging requires parity.
  - Evidence: 2026-07-04 mirrored `SKILL.md`, prompt README, and
    `documentation-wizard.json` to both bundled plugin skill trees.
    `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py package-contract .`
    passed with source, Codex bundle, and Claude bundle parity in sync.

## Phase 4: Validation And Closure Readiness

**Purpose**: Verify the wizard package and record closure-quality evidence.

- [x] T006 Run lifecycle and runtime validation.
  - Depends on: T004, T005
  - Requirement: R1, R2, R3, R4, R5, R6, R7
  - Files: `docs/specs/026-guided-documentation-wizard/verification.md`
  - Acceptance: Required MCP/CLI validation, prompt validation, focused tests,
    sync/package checks when applicable, and `git diff --check` are recorded
    with residual risk.
  - Evidence: 2026-07-04 prompt validation passed with 10 prompts and zero
    diagnostics. Focused tests passed:
    `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_spec_runtime.SpecRuntimeTests.test_prompt_definitions_are_discoverable_and_valid tests.runtime.test_spec_runtime.SpecRuntimeTests.test_documentation_wizard_prompt_covers_guided_workflow_contract tests.runtime.test_spec_runtime.SpecRuntimeTests.test_cli_prompts_outputs_json`.
    Package-contract passed. Sync-guard reported source/bundle parity in sync
    and installed-cache drift accepted as a reload residual.

- [x] T007 Promote final evidence and prepare closure decision.
  - Depends on: T006
  - Requirement: R7
  - Files: `docs/specs/026-guided-documentation-wizard/verification.md`,
    `docs/history/spec-closure-log.md`,
    `docs/history/spec-archive-index.md`
  - Acceptance: Final promotion map, residual spec-only content, closure action,
    and follow-up destinations are recorded before any package removal.
  - Evidence: 2026-07-04 verification.md records validation evidence,
    promotion targets, residual installed-cache reload risk, and removal as
    the intended closure action after final validation and final spec commit.

## Execution Rules

- Do not implement from `tasks.md` alone. Review linked requirements,
  acceptance criteria, design details, change-impact notes, traceability rows,
  verification expectations, durable-source baseline, and open decisions before
  editing.
- Mark the selected task `[~]` before starting an implementation slice.
- Keep v1 preview-first unless T001 explicitly resolves otherwise.
