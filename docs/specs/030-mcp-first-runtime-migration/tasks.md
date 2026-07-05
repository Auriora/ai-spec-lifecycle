---
title: MCP-first runtime migration tasks
doc_type: spec
artifact_type: tasks
status: draft
authoring_mode: wizard
lifecycle_stage: tasks
owner: platform
last_reviewed: 2026-07-05
---

# Tasks

**Input**: `docs/specs/030-mcp-first-runtime-migration/requirements.md`,
`design.md`, and `canonical-context.md`
**Prerequisites**: Requirements and design accepted for v1 stable MCP tool
surface, single public tool ownership, and `traceability_lookup.py` migration.

## Task Dependency Graph

```text
T001 -> T002
T002 -> T003
T003 -> T004
T004 -> T005
T005 -> T006
T006 -> T007
T007 -> T008
T008 -> T009
T009 -> T010
T010 -> T011
T011 -> T012
T012 -> T013
T013 -> T014
```

## Phase 1: Planning Contracts

**Purpose**: Lock the migration boundaries before implementation changes.

- [x] T001 Confirm implementation scope and public tool ownership.
  - Depends on: none
  - Requirement: Requirement 1, Requirement 5, Requirement 9
  - Files: `docs/specs/030-mcp-first-runtime-migration/design.md`, `docs/specs/030-mcp-first-runtime-migration/traceability.md`
  - Acceptance: The accepted plan names MCP as the public owner for agent-facing lifecycle tools, confirms `traceability_lookup.py` as the only v1 migrated executable script, and confirms retained runtime commands are validation, packaging, install, hook, or emergency recovery only.
  - Evidence mode: planner
  - Evidence: Completed 2026-07-05. `verification.md#task-evidence` records MCP as the public owner for agent-facing lifecycle tools, `traceability_lookup.py` as the only v1 migrated executable script, and retained runtime commands as validation, packaging, install, hook, or emergency recovery surfaces.

- [x] T002 Finalize compatibility evidence and dynamic-tool decision.
  - Depends on: T001
  - Requirement: Requirement 2, Requirement 3, Requirement 4
  - Files: `docs/specs/030-mcp-first-runtime-migration/verification.md`, `docs/reference/spec-lifecycle-runtime.md`
  - Acceptance: The compatibility matrix format is accepted, Codex and Claude plugin environments are listed as initial targets, dated Codex and Claude evidence or documented unavailable evidence is recorded, manual checker steps or checker output are captured, and v1 keeps `tools.listChanged: False` with stable MCP tools plus `available_next_actions`.
  - Evidence mode: planner
  - Evidence: Completed 2026-07-05. `verification.md#compatibility-matrix` records Codex `0.142.5`, Claude Code `2.1.201`, local plugin/config evidence, unavailable client refresh observations, and the accepted `stable_tool_surface` decision.
  - [x] T002.1 Record dated Codex compatibility evidence or an explicit unavailable-evidence note.
    - Evidence: Completed 2026-07-05. `verification.md#compatibility-matrix` records `codex-cli 0.142.5`, enabled `spec-lifecycle-manager@auriora-local` plugin evidence, and unavailable client refresh observation.
  - [x] T002.2 Record dated Claude plugin compatibility evidence or an explicit unavailable-evidence note.
    - Evidence: Completed 2026-07-05. `verification.md#compatibility-matrix` records `2.1.201 (Claude Code)`, Claude plugin MCP config evidence, and unavailable live Claude refresh observation.
  - [x] T002.3 Record manual checker steps or checker output for protocol visibility, tool-list refresh behavior, structured output handling, and fallback behavior.
    - Evidence: Completed 2026-07-05. `verification.md#manual-checker-notes` records local checker steps and observed/unavailable signals.
  - [x] T002.4 Record the v1 stable-tool decision from the evidence rather than client-name assumptions.
    - Evidence: Completed 2026-07-05. `verification.md#compatibility-evidence-notes` records stable MCP tools plus `available_next_actions`; dynamic tools are not approved.

- [x] T003 Accept script migration inventory and replacement contract before implementation.
  - Depends on: T002
  - Requirement: Requirement 5, Requirement 6, Requirement 9
  - Files: `docs/specs/030-mcp-first-runtime-migration/design.md`, `docs/specs/030-mcp-first-runtime-migration/verification.md`, `docs/specs/030-mcp-first-runtime-migration/traceability.md`
  - Acceptance: The planning evidence classifies relevant scripts as `migrate_to_mcp`, `retain_internal`, `retain_recovery`, or `out_of_scope`; accepts `traceability_lookup.py` as the only v1 `migrate_to_mcp` script; records its old entrypoint, replacement MCP tool, no replacement CLI command, docs updates, tests to port, source removal paths, bundle removal paths, and installed-cache validation.
  - Evidence mode: planner
  - Evidence: Completed 2026-07-05. `verification.md` sections "Script Migration Inventory" and "Replacement Contract: `traceability_lookup.py`" classify retained and migrated scripts and accept the `traceability_lookup.py` replacement contract before implementation.

## Phase 2: Shared Internal Modules

**Purpose**: Introduce shared implementation internals without creating new public tool surfaces.

- [x] T004 Create shared lifecycle module structure.
  - Depends on: T003
  - Requirement: Requirement 9
  - Files: `skills/spec-lifecycle-manager/scripts/lifecycle/`, bundled plugin copies, tests
  - Acceptance: The package contains importable shared lifecycle modules for touched behavior, and existing entrypoints can import them without circular imports or path hacks beyond the current script bootstrap pattern.
  - Evidence mode: implementation
  - Evidence: Completed 2026-07-05. Added importable `lifecycle/` modules to the source skill and both bundled plugin copies. `package-contract .` reports source, Codex bundle, and Claude bundle parity with 57 files per skill copy.
  - [x] T004.1 Add `lifecycle/__init__.py`.
    - Evidence: Completed 2026-07-05 in source, Codex bundle, and Claude bundle.
  - [x] T004.2 Add `lifecycle/actions.py` for `available_next_actions`.
    - Evidence: Completed 2026-07-05 with deterministic `lifecycle_next_actions` helper.
  - [x] T004.3 Add `lifecycle/capabilities.py` for capability report construction.
    - Evidence: Completed 2026-07-05 with advisory `lifecycle_capabilities` report helper that preserves unknown client fields.
  - [x] T004.4 Add `lifecycle/migration.py` for script inventory and removal checks.
    - Evidence: Completed 2026-07-05 with accepted v1 inventory and migrated-script closure blocker helper.
  - [x] T004.5 Add `lifecycle/traceability.py` for moved traceability lookup logic.
    - Evidence: Completed 2026-07-05 as the internal import target for traceability lookup delegation ahead of T010 migration.

- [x] T005 Add shared-module tests.
  - Depends on: T004
  - Requirement: Requirement 7, Requirement 8, Requirement 9
  - Files: `tests/runtime/`, `tests/traceability/`
  - Acceptance: Tests cover shared module behavior independently of MCP transport and prove representative shared functions are not implemented only in entrypoint handlers.
  - Evidence mode: validation
  - Evidence: Completed 2026-07-05. Added `tests/runtime/test_lifecycle_modules.py`; focused run passed 6 tests, and full Python unittest discovery passed 178 tests.

## Phase 3: MCP Tool Contracts

**Purpose**: Make MCP the public interface for touched lifecycle tools.

- [x] T006 Add `lifecycle_capabilities` MCP tool.
  - Depends on: T005
  - Requirement: Requirement 2, Requirement 3, Requirement 7
  - Files: `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`, `skills/spec-lifecycle-manager/scripts/lifecycle/capabilities.py`, bundled plugin copies, tests
  - Acceptance: The MCP tool reports known server fields, documented initialize session fields when available, `unknown` for unavailable client fields, `tools.listChanged: False`, and `dynamic_tools.decision: stable_tool_surface`.
  - Evidence mode: implementation
  - Evidence: Completed 2026-07-05. Added MCP `lifecycle_capabilities` tool backed by `lifecycle/capabilities.py`, with output schema advertised in `tools/list`; MCP tests verify unknown client fields, `tools.listChanged: False`, and `dynamic_tools.decision: stable_tool_surface`.

- [x] T007 Add `available_next_actions` to selected MCP results.
  - Depends on: T006
  - Requirement: Requirement 1, Requirement 4, Requirement 7
  - Files: `skills/spec-lifecycle-manager/scripts/lifecycle/actions.py`, `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`, tests
  - Acceptance: `active_spec_preflight`, `stage_readiness`, `lifecycle_guide`, and `no_active_spec_context` MCP outputs include deterministic `available_next_actions`; no dynamic tool-list behavior is enabled in v1.
  - Evidence mode: implementation
  - Evidence: Completed 2026-07-05. `active_spec_preflight`, `stage_readiness`, `lifecycle_guide`, and `no_active_spec_context` MCP outputs are enriched through `lifecycle/actions.py`; tests cover selected active-spec and no-active-spec outputs. Dynamic tool-list behavior remains disabled.

- [x] T008 Add `script_migration_inventory` MCP tool.
  - Depends on: T007
  - Requirement: Requirement 5, Requirement 6, Requirement 7, Requirement 9
  - Files: `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`, `skills/spec-lifecycle-manager/scripts/lifecycle/migration.py`, bundled plugin copies, tests
  - Acceptance: The MCP `script_migration_inventory` tool returns script classifications, replacement contracts, source and bundle removal paths, installed-cache validation expectations, and closure-blocker status without exposing a duplicate runtime/CLI agent-facing inventory command.
  - Evidence mode: implementation
  - Evidence: Completed 2026-07-05. Added MCP `script_migration_inventory` tool backed by `lifecycle/migration.py`, returning retained and migrated script classifications, replacement contracts, removal paths, installed-cache validation expectation, and closure blockers without adding a duplicate runtime CLI command.

- [x] T009 Add MCP output schemas and schema validation tests.
  - Depends on: T008
  - Requirement: Requirement 7
  - Files: `skills/spec-lifecycle-manager/scripts/spec_agent_schemas.py` or shared schema module, `tests/runtime/test_spec_mcp_server.py`
  - Acceptance: `lifecycle_capabilities`, `script_migration_inventory`, and `traceability_lookup` have representative structured output schemas or schema helpers, and tests validate representative `structuredContent`.
  - Evidence mode: validation
  - Evidence: Completed 2026-07-05. Added output schema helpers for `lifecycle_capabilities`, `script_migration_inventory`, and `traceability_lookup`; MCP tests verify schemas are advertised and representative `structuredContent` payloads are returned.

## Phase 4: Script Migration And Single Public Tool Ownership

**Purpose**: Remove the selected duplicate executable while preserving the MCP-owned tool.

- [ ] T010 Move traceability lookup logic behind shared internals and MCP.
  - Depends on: T009
  - Requirement: Requirement 5, Requirement 6, Requirement 8, Requirement 9
  - Files: `skills/spec-lifecycle-manager/scripts/traceability_lookup.py`, `skills/spec-lifecycle-manager/scripts/lifecycle/traceability.py`, `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`, tests
  - Acceptance: The MCP `traceability_lookup` tool uses shared traceability logic; tests no longer depend on `traceability_lookup.py` as an executable public tool; no replacement CLI command exposes the same agent-facing lookup.
  - Evidence mode: implementation
  - Evidence: Pending.

- [ ] T011 Add script migration closure checks to retained validation surfaces.
  - Depends on: T010
  - Requirement: Requirement 5, Requirement 6, Requirement 9
  - Files: `skills/spec-lifecycle-manager/scripts/lifecycle/migration.py`, `skills/spec-lifecycle-manager/scripts/spec_runtime.py`, tests
  - Acceptance: Retained validation or closure-check surfaces call shared migration logic and report a closure blocker if selected migrated source, bundle, or installed-cache paths still exist; the validation surface remains recovery/admin only and does not become the public agent-facing inventory tool.
  - Evidence mode: implementation
  - Evidence: Pending.

- [ ] T012 Remove migrated traceability executable from source and bundles.
  - Depends on: T011
  - Requirement: Requirement 5, Requirement 6, Requirement 8
  - Files: `skills/spec-lifecycle-manager/scripts/traceability_lookup.py`, `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/scripts/traceability_lookup.py`, `plugins/spec-lifecycle-manager/claude-plugin/skills/spec-lifecycle-manager/scripts/traceability_lookup.py`
  - Acceptance: The migrated executable is absent from source and bundled plugin paths, MCP traceability tests pass, and package parity checks account for the removal.
  - Evidence mode: implementation
  - Evidence: Pending.

## Phase 5: Durable Docs, Package Parity, And Closure Readiness

**Purpose**: Promote accepted behavior and prove source/bundle/cache consistency.

- [ ] T013 Update durable docs and skill guidance.
  - Depends on: T012
  - Requirement: Requirement 1, Requirement 5, Requirement 6, Requirement 8, Requirement 9
  - Files: `docs/reference/spec-lifecycle-runtime.md`, `docs/reference/spec-lifecycle-manager-mcp-install.md`, `skills/spec-lifecycle-manager/SKILL.md`, bundled plugin copies
  - Acceptance: Durable docs present MCP as the public lifecycle tool interface, document retained runtime/CLI boundaries, remove references to `traceability_lookup.py` as a public executable helper, and explain validation/recovery surfaces without duplicate tool ownership.
  - Evidence mode: implementation
  - Evidence: Pending.

- [ ] T014 Checkpoint - validation, install refresh, and closure evidence.
  - Depends on: T013
  - Requirement: Requirement 6, Requirement 7, Requirement 8
  - Files: `docs/specs/030-mcp-first-runtime-migration/verification.md`, package and bundle paths
  - Acceptance: Focused tests, full unit tests, package contract, install refresh, sync guard, scan, archive index, and whitespace checks pass or have recorded residual risk; verification evidence records compatibility matrix outcome, migrated-script removal, retained recovery boundaries, and package parity.
  - Validation: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'`; `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py package-contract .`; `scripts/install-spec-lifecycle-manager-package.sh`; `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py sync-guard .`; `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py scan .`; `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py archive-index .`; `git diff --check`
  - Evidence mode: validation
  - Evidence: Pending.

## Execution Rules

- Do not implement from `tasks.md` alone. Review `requirements.md`,
  `design.md`, `canonical-context.md`, and `traceability.md` before starting a
  task.
- Mark the selected task `[~]` before implementation.
- Do not add runtime/CLI commands that duplicate MCP-owned agent-facing tools.
- Keep shared lifecycle modules internal; they are not public tool interfaces.
- Treat dynamic MCP tool-list behavior as out of scope for v1 unless the
  compatibility matrix is updated and accepted.
- A task is complete only when concrete evidence is recorded.
