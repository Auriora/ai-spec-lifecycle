---
title: MCP-first runtime migration verification
doc_type: spec
artifact_type: verification
status: draft
authoring_mode: wizard
lifecycle_stage: tasks
owner: platform
last_reviewed: 2026-07-05
---

# Verification

## Scope

This verification record currently covers Phase 1 planning contracts and Phase
2 shared internal modules for `docs/specs/030-mcp-first-runtime-migration/`:
T001-T005. Implementation tasks T006-T014 remain pending.

## Quality Gates

| Gate | Required? | Status | Evidence |
|------|-----------|--------|----------|
| Requirements acceptance criteria reviewed | yes | pass | `requirements.md`, `design.md`, and `traceability.md` reviewed on 2026-07-05 before completing T001-T003. |
| Phase 1 task evidence complete | yes | pass | T001-T003 evidence recorded in `tasks.md` and this file. |
| Automated tests pass or alternate verification recorded | yes | pass | Structural validation commands in Evidence Log pass. |
| Compatibility matrix recorded | yes | pass | Compatibility Matrix section below. |
| Migration inventory and replacement contract accepted | yes | pass | Script Migration Inventory and Replacement Contract sections below. |
| Implementation readiness | yes | partial | Phase 1 and Phase 2 are complete; T006-T014 remain pending before closure or release. |
| Durable documentation updates identified | yes | pass | Durable targets listed in `canonical-context.md` and task T013. |
| Durable documentation promoted or explicitly deferred | yes | pending | Promotion is deferred to T013. |
| Spec cleanup decision recorded | yes | pending | Closure decision is deferred to T014 and final closure workflow. |

## Compatibility Matrix

| Agent | Agent version or date | Transport | Visible protocol version | `tools/list_changed` behavior | Structured output behavior | Fallback behavior | Evidence source | Result | Decision |
|-------|-----------------------|-----------|--------------------------|-------------------------------|----------------------------|-------------------|-----------------|--------|----------|
| Codex | `codex-cli 0.142.5`, observed 2026-07-05 | stdio MCP plugin | Server returns requested initialize protocol version or server default; exact client initialize payload not exposed to this session. | Server declares `tools.listChanged: False`; no client refresh observation is exposed. | MCP server wraps dictionary results as `structuredContent`; representative structured behavior is implemented in `tool_result`. | Stable tool list is available; state-specific fallback will be `available_next_actions` in selected tool results. | `codex --version`; `codex plugin list`; `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`; current Codex session tool availability; official MCP 2025-06-18 lifecycle/tools specification checked 2026-07-05. | warn | `stable_tool_surface` |
| Claude Code | `2.1.201 (Claude Code)`, observed 2026-07-05 | stdio MCP plugin | Server returns requested initialize protocol version or server default; no live Claude MCP session initialize payload was available in this Codex run. | Server declares `tools.listChanged: False`; no live Claude refresh observation was available. | MCP server supports `structuredContent`; live Claude structured-output behavior was not observed in this run. | Stable tool list is configured in `plugins/spec-lifecycle-manager/claude-plugin/.mcp.json`; state-specific fallback will be `available_next_actions`. | `claude --version`; `plugins/spec-lifecycle-manager/claude-plugin/.mcp.json`; `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`; official MCP 2025-06-18 lifecycle/tools specification checked 2026-07-05. | warn | `stable_tool_surface` |

### Compatibility Evidence Notes

- The local Codex plugin list shows `spec-lifecycle-manager@auriora-local`
  installed and enabled at version `0.2.1`.
- The local Claude binary reports `2.1.201 (Claude Code)`, and the Claude
  plugin MCP config points at `spec_mcp_server.py`.
- The current MCP server initialize response declares
  `tools.listChanged: False`, `resources.listChanged: False`, and
  `prompts.listChanged: False`.
- Official MCP 2025-06-18 documentation checked on 2026-07-05 confirms
  initialize/version/capability negotiation, `tools.listChanged` as the signal
  for tool-list-change notifications, and `structuredContent` plus optional
  output schemas for tool results.
- No reliable client-side `notifications/tools/list_changed` refresh behavior
  was observable from this Codex run. Per Requirement 3 and CP-005, that
  absence is recorded as unavailable evidence rather than inferred support.
- Phase 1 accepts the v1 decision to use a stable MCP tool surface with
  `available_next_actions`, not dynamic tool-list changes.

## Manual Checker Notes

The Phase 1 compatibility check used local observable evidence only:

1. Confirm the agent versions:
   - `codex --version`
   - `claude --version`
2. Confirm the Codex plugin installation:
   - `codex plugin list`
3. Confirm MCP server advertised capabilities:
   - inspect `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`
     initialize handling.
4. Confirm plugin MCP transport configuration:
   - inspect `plugins/spec-lifecycle-manager/.mcp.json`
   - inspect `plugins/spec-lifecycle-manager/claude-plugin/.mcp.json`
5. Record unobserved client refresh behavior as unknown/unavailable.

This is sufficient for the v1 decision because v1 does not enable dynamic
tool-list behavior. It is not sufficient to approve dynamic tools in a future
spec.

## Script Migration Inventory

| Script | Classification | Public owner | Rationale | Phase 1 decision |
|--------|----------------|--------------|-----------|------------------|
| `spec_mcp_server.py` | `retain_internal` | MCP server entrypoint | Required adapter for the public MCP tool surface. | Accepted as retained internal entrypoint. |
| `spec_runtime.py` | `retain_recovery` | Retained validation/recovery/admin surface | Required for CI, package validation, install checks, hooks, and emergency no-MCP recovery. It must not expose duplicate agent-facing lifecycle tools for migrated behavior. | Accepted as retained recovery surface. |
| `codex_spec_lifecycle_hook.py` | `retain_internal` | Hook adapter | Required advisory hook entrypoint; hook behavior remains advisory. | Accepted as retained internal entrypoint. |
| `spec_agent_schemas.py` | `retain_internal` | Internal schema helper | Supports MCP structured output schemas and is not an agent-facing runtime tool. | Accepted as retained internal helper. |
| `traceability_lookup.py` | `migrate_to_mcp` | MCP `traceability_lookup` tool | Agent-facing lookup behavior already has an MCP replacement and should not remain as a parallel executable script after migration. | Accepted as the only v1 migrated executable script. |

## Replacement Contract: `traceability_lookup.py`

| Field | Value |
|-------|-------|
| Old executable entrypoint | `python3 skills/spec-lifecycle-manager/scripts/traceability_lookup.py` |
| Replacement public tool | MCP `traceability_lookup` |
| Replacement CLI command | None. Do not add a normal agent-facing CLI replacement. |
| Shared logic destination | `skills/spec-lifecycle-manager/scripts/lifecycle/traceability.py` |
| Source removal path | `skills/spec-lifecycle-manager/scripts/traceability_lookup.py` |
| Codex bundle removal path | `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/scripts/traceability_lookup.py` |
| Claude bundle removal path | `plugins/spec-lifecycle-manager/claude-plugin/skills/spec-lifecycle-manager/scripts/traceability_lookup.py` |
| Docs to update | `docs/reference/spec-lifecycle-runtime.md`; MCP/package guidance as needed. |
| Tests to port | `tests/traceability/test_traceability_lookup.py`; relevant MCP server tests. |
| Installed-cache validation | Install refresh followed by `sync-guard .`. |
| Closure blocker | The spec cannot close if any selected source, bundle, or installed-cache migrated executable path remains without a recorded deferral. |

## Requirement Coverage

| Requirement | Acceptance criteria covered | Evidence | Residual risk |
|-------------|-----------------------------|----------|---------------|
| Requirement 1 | AC1-AC2 | T001 accepted MCP as public owner for agent-facing lifecycle tools and retained scripts as recovery/internal surfaces. | Docs are updated later in T013. |
| Requirement 2 | AC1-AC5 | Compatibility matrix records known server capability data and unknown/unavailable client observations. | Client refresh observations are unavailable in this Codex run. |
| Requirement 3 | AC1-AC7 | Matrix lists Codex and Claude environments, manual checker steps, dated evidence, and stable fallback decision. | Future dynamic tools need fresh evidence. |
| Requirement 4 | AC2-AC4 | V1 accepts stable tools plus `available_next_actions`; dynamic tool-list behavior is not enabled. | Available-next-actions implementation remains pending in T007. |
| Requirement 5 | AC1, AC4-AC5 | Script inventory and replacement contract recorded. | Implementation and removal remain pending. |
| Requirement 6 | AC1, AC4 | Closure blocker expectation recorded for migrated script paths. | Closure-check implementation remains pending. |
| Requirement 9 | AC1-AC5 | Public ownership, retained recovery boundaries, and shared-module direction accepted. | Shared module extraction remains pending. |

## Correctness Property Coverage

| Property | Covered by | Evidence | Residual risk |
|----------|------------|----------|---------------|
| CP-001 | T002 | Stable-tool decision accepted because dynamic refresh behavior was not observed. | Future dynamic tools require new evidence. |
| CP-002 | T003 | Migrated script source and bundle paths are listed as closure blockers. | Enforcement remains pending in T011-T012. |
| CP-005 | T002 | Unknown/unavailable client capability data is recorded without guessed runtime gating. | Client behavior may change. |
| CP-006 | T003 | Replacement contract is recorded before implementation. | Satisfaction remains pending. |
| CP-007 | T001 and T003 | MCP owns agent-facing lifecycle tools; retained scripts are internal/recovery only. | Command inventory review remains pending. |
| CP-007 | T004-T005 | Shared modules are importable internals and tested without becoming public tool surfaces. | Entrypoints are wired in later phases. |

## Task Evidence

| Task ID | Status | Evidence | Notes |
|---------|--------|----------|-------|
| T001 | complete | Phase 1 accepted MCP as the public owner for agent-facing lifecycle tools, `traceability_lookup.py` as the only v1 migrated executable, and retained scripts as validation/recovery/internal surfaces. | Implementation still pending. |
| T002 | complete | Compatibility matrix and manual checker notes recorded in this file on 2026-07-05. | Dynamic tools are not approved. |
| T003 | complete | Script migration inventory and `traceability_lookup.py` replacement contract recorded in this file on 2026-07-05. | Removal and closure checks remain pending. |
| T004 | complete | Added `lifecycle/__init__.py`, `actions.py`, `capabilities.py`, `migration.py`, and `traceability.py` to source skill, Codex bundle, and Claude bundle. | MCP/runtime wiring remains pending. |
| T005 | complete | Added `tests/runtime/test_lifecycle_modules.py`; focused and full Python test runs passed. | Does not yet prove MCP transport contracts. |

## Evidence Log

| Date | Evidence | Result | Notes |
|------|----------|--------|-------|
| 2026-07-05 | `git status --short` | pass | Clean before Phase 1 edits. |
| 2026-07-05 | `codex --version` | pass | Reported `codex-cli 0.142.5`; PATH alias warning is unrelated to version evidence. |
| 2026-07-05 | `claude --version` | pass | Reported `2.1.201 (Claude Code)`. |
| 2026-07-05 | `codex plugin list` | pass | `spec-lifecycle-manager@auriora-local` installed and enabled at `0.2.1`. |
| 2026-07-05 | Official MCP 2025-06-18 lifecycle and tools documentation | pass | Confirmed protocol-version negotiation, capability negotiation, `tools.listChanged`, `notifications/tools/list_changed`, `structuredContent`, and output schema semantics. |
| 2026-07-05 | `rg` over `spec_mcp_server.py`, MCP configs, and runtime docs | pass | Confirmed current MCP tools, `structuredContent`, `tools.listChanged: False`, and existing traceability script references. |
| 2026-07-05 | `ls -l` for traceability executable paths | pass | Confirmed source, Codex bundle, and Claude bundle migrated executable paths currently exist before implementation. |
| 2026-07-05 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_lifecycle_modules` | pass | 6 focused shared-module tests passed. |
| 2026-07-05 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'` | pass | 178 Python tests passed. |
| 2026-07-05 | `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py package-contract .` | pass | Source skill, Codex bundle, and Claude bundle are in sync with 57 files each. |
| 2026-07-05 | `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py scan .` | pass | 2 active specs, both pass. |
| 2026-07-05 | `git diff --check` | pass | No whitespace errors. |

## Manual Or External Verification

Official MCP documentation was checked for protocol semantics, while current
agent behavior was derived from local executable versions, plugin installation
evidence, MCP server source, and plugin MCP configuration. This is deliberate:
the accepted v1 behavior is the conservative stable-tool fallback, and dynamic
tool-list behavior remains out of scope until a future spec or later task
records stronger observed client evidence.

## Residual Risks

- Live Claude MCP refresh behavior was not observed in this Codex run.
- Live client refresh behavior for `notifications/tools/list_changed` was not
  observable from the current session.
- `traceability_lookup.py` still exists in source and bundle paths until T012.
- Runtime docs still contain public script references until T013.
- The new `lifecycle.traceability` module delegates to the existing executable
  module until T010 moves the implementation fully behind shared internals.
- The new shared modules are not wired into MCP or retained runtime entrypoints
  until T006-T011.

## Durable Promotion And Cleanup

| Spec content | Durable destination or deferral | Status | Evidence |
|--------------|---------------------------------|--------|----------|
| MCP-first public tool ownership | `docs/reference/spec-lifecycle-runtime.md`; MCP install docs if needed | deferred | T013 |
| Compatibility matrix and stable fallback decision | `docs/reference/spec-lifecycle-runtime.md` or durable MCP behavior docs | deferred | T013 |
| Script migration inventory and replacement contract | Runtime docs and closure evidence | deferred | T013-T014 |
| Traceability executable removal | Source, bundle, installed cache, closure evidence | pending | T010-T014 |
| Shared lifecycle module architecture | Source skill, bundled plugin copies, tests, runtime docs | partial | T004-T005 complete; durable docs deferred to T013 |

### Spec Cleanup Decision

- **Cleanup action:** keep active
- **Reason:** Phase 1 planning contracts and Phase 2 shared modules are complete; MCP contract implementation remains.
- **Final spec commit:** pending
- **Closure log path:** `docs/history/spec-closure-log.md`
- **Closure log entry updated:** no
- **Closure cleanup commit:** pending
- **Active indexes updated:** no
- **Durable docs linked back to evidence where useful:** no
- **Residual spec-only content:** compatibility and migration planning evidence
  remains spec-local until T013 promotion.

## Ship Or Closure Risk

- **Risk level:** medium
- **Breaking change:** yes, once `traceability_lookup.py` is removed
- **Blast radius checked:** partial
- **Rollback path:** not required for Phase 1; implementation rollback to be
  defined during T010-T014 if needed
- **Requires human review:** yes
- **Release notes needed:** likely, if public script removal is released
- **Follow-up issue or spec needed:** no for Phase 1

### Risk Rationale

Phase 2 adds internal modules and tests but does not change public MCP or CLI
behavior. The overall spec remains medium risk because later phases will remove
an executable script and shift public agent-facing behavior to MCP-only
ownership.

## Readiness Decision

- **Ready for Phase 3 implementation:** yes, for T006 only
- **Ready for promotion:** no
- **Ready for release:** no
- **Ready for closure:** no

## Related Artifacts

- Requirements: `requirements.md`
- Canonical context: `canonical-context.md`
- Design: `design.md`
- Tasks: `tasks.md`
- Traceability: `traceability.md`
