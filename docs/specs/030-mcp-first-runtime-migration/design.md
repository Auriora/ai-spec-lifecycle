---
title:           MCP-first runtime migration design
doc_type:        spec
artifact_type:   design
status:          draft
authoring_mode:  wizard
lifecycle_stage: tasks
owner:           platform
last_reviewed:   2026-07-05
---

# Technical Design

## Overview

Move the lifecycle manager toward an MCP-first agent contract without adding
fragile client probing or removing recovery paths prematurely. The v1 design
uses a stable MCP tool surface and adds state-specific `available_next_actions`
to relevant tool results. Dynamic tool-list changes remain out of scope for v1
unless compatibility research later proves they are reliable enough.

Script migration is explicit and narrow. The design distinguishes executable
script surfaces from reusable implementation modules:

- migrated executable scripts must be removed by closure;
- retained scripts must have a documented role, such as MCP server entrypoint,
  hook entrypoint, CI/recovery runner, or internal schema helper;
- shared logic must live in importable lifecycle modules, but those modules are
  implementation internals, not alternate public tool surfaces.

The target architecture is not "MCP calls `spec_runtime.py`." The target is
"each lifecycle tool has one public owner, with MCP owning agent-facing tools."
The implementation now moves the broad deterministic lifecycle implementation
into import-only `lifecycle/core.py`. MCP imports that shared core directly, and
`spec_runtime.py` remains as the retained runtime/recovery executable. Runtime argument parsing and dispatch live in `lifecycle/runtime_adapter.py`, a private adapter used by
`spec_runtime.py`, so shared core modules do not become parallel public command
surfaces.

For this first slice, `traceability_lookup.py` is the only executable script
selected for migration and removal. It already has an MCP-facing replacement
through the `traceability_lookup` tool and is small enough to retire safely by
moving reusable parsing logic behind the MCP/runtime implementation. Larger
runtime surfaces, especially `spec_runtime.py`, remain retained recovery
entrypoints but no longer own reusable lifecycle implementation for MCP tools.

## Requirement Coverage

| Requirement   | Acceptance Criteria | Design Coverage                                                                                                                                                                                      | Validation Approach                                                                                 |
|---------------|---------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------|
| Requirement 1 | AC1, AC2            | MCP tools become the documented agent-facing contract; direct scripts are documented as recovery, CI, hook, or package internals only.                                                               | Runtime docs review, prompt/skill docs review, MCP tool list tests.                                 |
| Requirement 2 | AC1-AC5             | Add advisory `lifecycle_capabilities` MCP output with known server capability fields and `unknown` values where session data is not exposed. No runtime gating is based on private client internals. | MCP server tests for known and unknown capability fields.                                           |
| Requirement 3 | AC1-AC7             | Add a compatibility research/checker workflow that records evidence in a matrix before dynamic tool-list behavior can be enabled.                                                                    | Manual compatibility checklist, optional checker output fixture, verification evidence.             |
| Requirement 4 | AC1-AC4             | V1 uses stable MCP tools with `available_next_actions`; dynamic `tools/list_changed` remains deferred unless compatibility evidence is accepted.                                                     | MCP contract tests for equivalent next-action semantics.                                            |
| Requirement 5 | AC1-AC5             | Add a migration inventory and replacement contract table; select only `traceability_lookup.py` for v1 migration/removal.                                                                             | Design review, traceability rows, closure check for selected removal paths.                         |
| Requirement 6 | AC1-AC4             | Add closure blocker logic or closure evidence checks that fail selected migrated scripts if they remain in source/bundle/cache paths.                                                                | Closure-check/runtime tests and package parity validation.                                          |
| Requirement 7 | AC1-AC3             | MCP tool results use stable structured fields; unsupported/degraded modes are explicit.                                                                                                              | MCP response schema tests and representative structuredContent checks.                              |
| Requirement 8 | AC1-AC3             | Port migrated script tests to MCP/runtime tests, retain `spec_runtime.py` for CI/no-MCP recovery, and require package sync validation after install.                                                 | Python unit tests, MCP server tests, package-contract, sync-guard.                                  |
| Requirement 9 | AC1-AC5             | Extract lifecycle implementation into import-only shared modules, wire MCP to `lifecycle/core.py` instead of `spec_runtime.py`, keep `spec_runtime.py` as the retained runtime/recovery executable through `lifecycle/runtime_adapter.py`, and preserve a single public owner for each agent-facing lifecycle tool. | MCP-owned tool tests, retained-entrypoint review, shared-core non-executable tests, and package/sync validation. |

## Correctness Property Coverage

| Property | Design Behavior                                                                         | Validation Direction                                             | Notes                                                    |
|----------|-----------------------------------------------------------------------------------------|------------------------------------------------------------------|----------------------------------------------------------|
| CP-001   | Dynamic tools are not implemented in v1; stable tools return next actions.              | MCP contract tests compare next actions across lifecycle states. | Future dynamic behavior requires compatibility evidence. |
| CP-002   | `migrate_to_mcp` inventory rows are checked at closure against source and bundle paths. | Closure helper/check test for selected script still present.     | Applies only to selected scripts.                        |
| CP-003   | MCP results include structured fields and JSON text fallback.                           | Existing and new MCP server tests inspect `structuredContent`.   | Keep text fallback for broad client compatibility.       |
| CP-004   | `spec_runtime.py` remains the retained recovery runner.                                 | `npm run validate`, package-contract, sync-guard.                | This is deliberate retention, not migration.             |
| CP-005   | Capability reporting uses explicit `unknown` where unavailable.                         | Tests assert no guessed client capability fields.                | No private agent internals.                              |
| CP-006   | Replacement contracts must be complete before removal is accepted.                      | Closure evidence table and tests.                                | Prevents deletion-only migration.                        |
| CP-007   | Each agent-facing lifecycle tool has one public owner.                                  | MCP tool contract tests, runtime command inventory review, and shared-core extraction tests. | Avoids parallel MCP and CLI tool surfaces while keeping retained recovery explicit. |

## High-Level Design

### System Architecture

```text
Agent
  |
  | agent-facing lifecycle tools
  v
MCP entrypoint
  |-- spec_mcp_server.py           MCP JSON-RPC adapter
  |
  | direct Python calls
  v
Shared lifecycle modules
  |-- lifecycle/core.py import-only shared deterministic implementation
  |-- lifecycle/runtime_adapter.py private runtime adapter used by spec_runtime.py
  |-- lifecycle actions and state
  |-- capability report construction
  |-- traceability lookup logic
  |-- migration inventory and closure checks
  |
  v
Filesystem, docs, package metadata, tests, installed-cache evidence

Hook / CLI / CI
  |
  | validation, packaging, install, hook, or emergency recovery only
  v
Retained non-MCP entrypoints
  |-- codex_spec_lifecycle_hook.py advisory hook adapter
  |-- spec_runtime.py              validation/recovery executable over lifecycle/runtime_adapter.py
```

The MCP server remains the primary agent-facing boundary, but it is an adapter,
not the owner of lifecycle policy. It exposes a static tool list for v1 and
returns state-specific actions from tool results. That avoids depending on
uneven client support for `notifications/tools/list_changed`.

Retained non-MCP entrypoints may call shared modules for validation, packaging,
install, hook, or emergency recovery workflows. They must not expose duplicate
agent-facing lifecycle tools that compete with the MCP surface.

### Components and Changes

- `spec_mcp_server.py`
    - Retain as the MCP server entrypoint.
    - Keep `tools.listChanged: False` for v1.
    - Add or expose `lifecycle_capabilities`.
    - Add `available_next_actions` to relevant lifecycle results through helper
      functions rather than duplicating policy in the server.
    - Stop growing direct policy logic in the server; tool handlers should
      normalize arguments, call shared modules, normalize paths, and format MCP
      responses.

- Shared lifecycle modules
    - Add focused importable modules for behavior touched by this spec.
    - Initial module candidates:
        - `lifecycle_capabilities` for server/client capability report
          construction.
        - `lifecycle_actions` for `available_next_actions`.
        - `lifecycle_traceability` for logic currently in
          `traceability_lookup.py`.
        - `lifecycle_migration` for script inventory and removal checks.
    - These modules are shared by MCP and retained non-MCP entrypoints.
    - These modules are implementation internals. MCP is the public tool path;
      retained non-MCP entrypoints may use modules only for validation,
      packaging, hook, install, or emergency recovery workflows.

- `traceability_lookup.py`
    - Classify as `migrate_to_mcp`.
    - Move reusable parsing/lookup logic into an importable MCP/runtime module.
    - Remove the executable script from source and both bundled plugin copies by
      closure.
    - Keep the MCP `traceability_lookup` tool as the replacement agent-facing
      interface.
    - Do not add a replacement CLI command that exposes the same lookup as a
      normal agent-facing tool.

- `spec_runtime.py`
    - Classify as `retain_recovery`.
    - Keep CLI validation and no-MCP recovery until a later spec replaces the
      package validation runner.
    - Remove or reduce docs that present it as the normal agent-facing surface
      when MCP is available.
    - For behavior touched by this spec, call shared lifecycle modules instead
      of keeping the only implementation inside CLI command handlers.
    - Retained commands are validation/recovery/admin commands only; they should
      not duplicate MCP-owned lifecycle tools as normal user-facing paths.

- `codex_spec_lifecycle_hook.py`
    - Classify as `retain_internal`.
    - It remains a hook entrypoint and can call retained recovery/runtime logic.
    - Hook blocking behavior is unchanged.
    - For touched behavior, delegate to shared lifecycle modules or retained
      adapter functions rather than shelling out to another entrypoint.
    - Hook outputs remain advisory hook diagnostics, not duplicate lifecycle
      tool surfaces.

- `spec_agent_schemas.py`
    - Classify as `retain_internal`.
    - It is an internal schema helper, not an agent-facing runtime script.

### Data Models

#### Capability Report

```json
{
  "status": "known|partial|unknown",
  "server": {
    "name": "spec-lifecycle-manager",
    "version": "0.1.0",
    "protocol_version": "2025-06-18",
    "capabilities": {
      "tools": {
        "listChanged": false
      },
      "resources": {
        "listChanged": false
      },
      "prompts": {
        "listChanged": false
      }
    }
  },
  "client": {
    "name": "unknown",
    "version": "unknown",
    "protocol_version": "unknown",
    "capabilities": "unknown"
  },
  "dynamic_tools": {
    "server_support": false,
    "client_refresh_observed": "unknown",
    "decision": "stable_tool_surface"
  },
  "available_next_actions": []
}
```

The server should report only fields it actually knows. If the current stdio
adapter does not retain initialize parameters by session, client fields remain
`unknown` in v1.

#### Available Next Action

```json
{
  "id": "advance_to_design",
  "label": "Create design artifact",
  "stage": "design",
  "reason": "Requirements-stage package is lint-clean.",
  "tool": "stage_readiness",
  "artifact": "design.md",
  "required": true
}
```

The same action shape can appear in `active_spec_preflight`,
`stage_readiness`, `lifecycle_guide`, `no_active_spec_context`, and future
closure tools.

#### Compatibility Matrix Row

```json
{
  "agent": "Codex",
  "agent_version_or_date": "2026-07-05",
  "transport": "stdio",
  "visible_protocol_version": "2025-06-18|unknown",
  "tools_list_changed_behavior": "not_supported|observed|unknown",
  "structured_output_behavior": "observed|unknown",
  "fallback_behavior": "observed|unknown",
  "evidence_source": "manual test, checker output, or dated official docs",
  "result": "pass|warn|fail|unknown",
  "decision": "stable_tool_surface|dynamic_tools_allowed"
}
```

Documentation claims are advisory. Live development-environment behavior wins
when it conflicts with docs.

#### Script Migration Inventory Row

```json
{
  "script": "traceability_lookup.py",
  "classification": "migrate_to_mcp",
  "old_entrypoint": "python3 skills/spec-lifecycle-manager/scripts/traceability_lookup.py",
  "replacement_mcp_tool": "traceability_lookup",
  "retained_ci_debug_command": "none; use MCP traceability_lookup for agent-facing lookup and module/unit tests for debugging",
  "shared_logic_destination": "shared lifecycle traceability module",
  "docs_to_update": [
    "docs/reference/spec-lifecycle-runtime.md"
  ],
  "tests_to_port": [
    "tests/traceability/test_traceability_lookup.py"
  ],
  "source_removal_paths": [
    "skills/spec-lifecycle-manager/scripts/traceability_lookup.py"
  ],
  "bundle_removal_paths": [
    "plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/scripts/traceability_lookup.py",
    "plugins/spec-lifecycle-manager/claude-plugin/skills/spec-lifecycle-manager/scripts/traceability_lookup.py"
  ],
  "installed_cache_validation": "sync-guard after install"
}
```

### Data Flow

#### Stable MCP Tool Flow

1. Agent calls an MCP tool such as `active_spec_preflight`.
2. The MCP adapter calls shared lifecycle modules directly.
3. A shared next-action helper enriches the result with
   `available_next_actions`.
4. The MCP result returns `structuredContent` plus JSON text fallback.
5. The agent selects the next tool/action from structured output instead of
   relying on a changed tool list.

#### Compatibility Checker Flow

1. Maintainer runs a dev-environment compatibility checker or documented manual
   test for a target agent.
2. The checker records observable behavior only.
3. Results populate the compatibility matrix.
4. Design/verification decide whether dynamic tools are allowed.
5. V1 default remains `stable_tool_surface` unless the matrix explicitly
   supports dynamic tools.

#### Script Migration Flow

1. Design classifies scripts in the migration inventory.
2. For `migrate_to_mcp`, implementation moves shared logic to an importable
   module and routes MCP tool calls through that module.
3. Tests are ported from direct script execution to module/MCP contract tests.
4. The executable script is removed from source and bundle paths.
5. Install refresh and `sync-guard` prove source/bundle/cache parity.

#### Retained Non-MCP Flow

1. CI, install, hook, or emergency recovery invokes a retained non-MCP
   entrypoint.
2. The entrypoint validates adapter-specific inputs and calls shared modules
   only for its retained purpose.
3. The entrypoint returns validation, package, hook, install, or recovery output.
4. It does not expose a duplicate agent-facing lifecycle tool when MCP owns
   that tool.

## Low-Level Design

### Algorithms and Logic

#### Next Action Derivation

```text
function lifecycle_next_actions(context):
    if no active specs:
        return start_spec_or_review_backlog_actions
    if selected spec has requirements but no design:
        return advance_to_design_action
    if selected spec has design but no tasks:
        return advance_to_tasks_action
    if selected spec has runnable tasks:
        return task_context_and_validation_actions
    if selected spec is complete:
        return promotion_and_closure_actions
    return diagnostics_and_recovery_actions
```

This helper should be deterministic and shared by MCP tools. It should not
inspect client identity.

#### Capability Reporting

```text
function lifecycle_capabilities(session_state):
    report server protocol and declared capabilities
    if initialize params are available:
        report client protocol, clientInfo, and capabilities
    else:
        report client fields as unknown
    report dynamic_tools.decision = stable_tool_surface
    return report with available_next_actions for compatibility research
```

No runtime behavior changes based on guessed client support.

#### MCP Session State

```text
McpSessionState:
    initialized: boolean
    protocol_version: string | unknown
    client_info: object | unknown
    client_capabilities: object | unknown
```

`spec_mcp_server.py` owns this adapter state for the lifetime of the stdio
process. It records documented `initialize` parameters when they are present and
passes the state to shared capability-report construction. If a framework or
transport does not expose these values, the shared report uses `unknown`.

#### Migration Closure Check

```text
function migrated_script_closure_check(inventory):
    for row in inventory where classification == migrate_to_mcp:
        assert replacement_mcp_tool is documented
        assert tests_to_port are complete
        assert every source_removal_path is absent
        assert every bundle_removal_path is absent
    return blockers
```

#### Entrypoint Adapter Rule

```text
function entrypoint_handler(raw_input):
    parsed = parse_interface_input(raw_input)
    result = shared_lifecycle_function(parsed)
    return format_interface_output(result)
```

Entrypoint handlers may parse, validate, normalize paths, enforce adapter-level
permissions, and format output. They should not own lifecycle policy, artifact
parsing, task selection, traceability lookup, compatibility decisions, or
migration closure logic.

### Function Signatures and Interfaces

Representative Python-level functions:

```python
def lifecycle_capabilities(repo_root: Path, session_state: dict[str, Any] | None = None) -> dict[str, Any]:
    ...


def lifecycle_next_actions(repo_root: Path, spec_path: Path | None = None) -> list[dict[str, Any]]:
    ...


def script_migration_inventory(repo_root: Path) -> dict[str, Any]:
    ...


def migrated_script_closure_check(repo_root: Path, inventory: dict[str, Any]) -> list[dict[str, Any]]:
    ...
```

Shared module shape:

```text
skills/spec-lifecycle-manager/scripts/
  spec_mcp_server.py              # MCP adapter
  spec_runtime.py                 # retained validation/recovery adapter
  codex_spec_lifecycle_hook.py    # hook adapter
  spec_agent_schemas.py           # retained schema helper
  lifecycle/
    __init__.py
    actions.py
    capabilities.py
    migration.py
    traceability.py
```

MCP tools:

| Tool                         | Purpose                                                               | Notes                                                 |
|------------------------------|-----------------------------------------------------------------------|-------------------------------------------------------|
| `lifecycle_capabilities`     | Report server/client capability visibility and dynamic-tool decision. | Advisory; no private probing.                         |
| `script_migration_inventory` | Return classification and replacement contracts.                      | Read-only.                                            |
| `traceability_lookup`        | Replacement interface for migrated `traceability_lookup.py`.          | Existing tool retained, backed by moved module logic. |

Output schemas:

| Tool                         | Output Schema Location                                 | Validation                                                               |
|------------------------------|--------------------------------------------------------|--------------------------------------------------------------------------|
| `lifecycle_capabilities`     | `spec_agent_schemas.py` or a new shared schema module. | Representative MCP `structuredContent` validates against schema.         |
| `script_migration_inventory` | `spec_agent_schemas.py` or a new shared schema module. | Inventory fixture validates required replacement-contract fields.        |
| `traceability_lookup`        | Existing or moved traceability schema helper.          | Existing traceability fixtures validate MCP output after script removal. |

Schemas are contracts for MCP `structuredContent`. The JSON text fallback may
remain for broad client compatibility, but tests validate the structured
payload.

### Error Handling

- Capability fields that cannot be observed return `unknown`, not guessed.
- Compatibility checker failures return `warn` or `fail` rows and do not change
  runtime behavior silently.
- Missing migrated-script replacement contracts are closure blockers.
- Missing source/bundle removal for selected migrated scripts is a closure
  blocker.
- MCP tools return structured degraded-mode payloads when a repository or
  client capability is unavailable.

### Security, Trust, and Access

- MCP client identity and capability declarations are treated as advisory.
- Tool annotations, client names, and version strings are not trusted for
  security decisions.
- Dynamic tool-list behavior is not enabled from unauthenticated or undocumented
  runtime signals.
- Shared lifecycle modules are internal package APIs, not permission boundaries
  or public tool interfaces.
- No additional write capability is introduced by this design.
- Hook behavior stays advisory-only.

### Migration and Compatibility

V1 compatibility strategy:

- Static MCP tool list.
- `tools.listChanged: False`.
- State-specific `available_next_actions`.
- `lifecycle_capabilities` reports known/unknown capability data.
- Dynamic tool lists remain a future enhancement only after compatibility
  evidence supports them.

Retained scripts:

| Script                         | Classification  | Rationale                                                                                                                                      |
|--------------------------------|-----------------|------------------------------------------------------------------------------------------------------------------------------------------------|
| `spec_mcp_server.py`           | retain_internal | Required MCP server entrypoint.                                                                                                                |
| `spec_runtime.py`              | retain_recovery | Required for CI, package validation, install checks, and emergency no-MCP recovery. It must not expose duplicate agent-facing lifecycle tools. |
| `codex_spec_lifecycle_hook.py` | retain_internal | Required advisory hook entrypoint.                                                                                                             |
| `spec_agent_schemas.py`        | retain_internal | Internal schema helper.                                                                                                                        |
| `traceability_lookup.py`       | migrate_to_mcp  | Agent-facing lookup behavior already has MCP replacement; script can be retired after module extraction and test port.                         |

## Validation Strategy

| Validation                                                        | Covers                                                                                  | Evidence Location                                               | Residual Risk                                                   |
|-------------------------------------------------------------------|-----------------------------------------------------------------------------------------|-----------------------------------------------------------------|-----------------------------------------------------------------|
| `python3 -m unittest tests.runtime.test_spec_mcp_server`          | MCP tool contracts, structured output, lifecycle capabilities.                          | `verification.md`, task evidence.                               | Client UI behavior still needs manual compatibility checks.     |
| Public tool ownership tests/review                                | MCP owns agent-facing lifecycle tools; retained runtime commands do not duplicate them. | Runtime and MCP test evidence.                                  | Some recovery commands may look similar and need explicit docs. |
| Port traceability tests from direct script to module/MCP tests    | Migrated script replacement contract.                                                   | `tests/traceability/`, `tests/runtime/test_spec_mcp_server.py`. | May need temporary duplicate tests during migration.            |
| `spec_runtime.py lint docs/specs/030-mcp-first-runtime-migration` | Spec artifact health.                                                                   | Task evidence.                                                  | Structural lint only.                                           |
| `package-contract .`                                              | Source/bundle package contract.                                                         | Task evidence.                                                  | Does not validate installed cache alone.                        |
| Install refresh plus `sync-guard .`                               | Source, bundle, installed cache parity and removed script paths.                        | Task evidence and closure log.                                  | Requires local install environment.                             |
| Compatibility matrix review                                       | Dynamic tool-list decision.                                                             | `verification.md`.                                              | Manual checks may become stale; record dates.                   |

## Downstream Task Guidance

- Required checkpoints before implementation:
    - Requirements accepted.
    - Compatibility matrix format, dated Codex/Claude evidence or explicit
      unavailable-evidence notes, and v1 stable-tool decision accepted.
    - Script migration inventory and `traceability_lookup.py` replacement
      contract accepted.
    - Shared module boundaries accepted for touched behavior.
    - Public owner for each touched lifecycle tool accepted.
- Properties or acceptance criteria needing explicit task coverage:
    - CP-002 and CP-006 for migrated script removal.
    - CP-005 for rejecting undocumented capability probes.
    - Requirement 8 for recovery/CI preservation.
    - Requirement 9 for single public tool ownership.
- Optional artifacts needed before implementation:
    - `traceability.md` was created with `tasks.md`.
    - `verification.md` should include the compatibility matrix and closure
      removal evidence.
- Downstream review needed if this design changes after tasks are drafted:
    - Review tasks, traceability, verification, and durable-doc promotion targets.

## Operational Considerations

- The first implementation slice should not change dynamic MCP tool exposure.
- Installed Codex and Claude plugin bundles must be refreshed after script
  removal.
- Documentation should steer agents to MCP first while preserving explicit
  recovery commands for CI/debugging.
- If removing `traceability_lookup.py` breaks external users, the design should
  route that as residual risk or defer removal before implementation begins.

## Open Questions

No blocking open design questions remain for the v1 design if the resolved
decisions below are accepted. Reopen this section if task planning finds a
conflict between single public tool ownership, retained recovery commands, or
package validation needs.

## Resolved Design Decisions

| ID     | Question                                                           | Current Design Position                                                                                               | Blocks Implementation  |
|--------|--------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------|------------------------|
| OQ-001 | Which scripts are in scope for first migration?                    | Only `traceability_lookup.py`; retain the rest.                                                                       | no, if accepted        |
| OQ-002 | Rewrite or incrementally adapt MCP server?                         | Incrementally adapt; no rewrite.                                                                                      | no, if accepted        |
| OQ-003 | Retained no-MCP recovery path?                                     | `spec_runtime.py` remains retained recovery.                                                                          | no, if accepted        |
| OQ-004 | Which clients to test for dynamic tools?                           | Codex and Claude plugin environments first; dynamic tools deferred.                                                   | no for v1 stable tools |
| OQ-005 | Is dynamic tool-list behavior worth v1?                            | No. Use stable tools and `available_next_actions` for v1.                                                             | no, if accepted        |
| OQ-006 | Which `spec_runtime.py` logic should be extracted?                 | Extract reusable lifecycle implementation into import-only `lifecycle/core.py`; keep runtime argument parsing in private `lifecycle/runtime_adapter.py`; keep `spec_runtime.py` as the retained runtime/recovery executable. | no, if accepted        |
| OQ-007 | Which retained runtime commands are not duplicate lifecycle tools? | Retain validation, packaging, install, hook, and emergency recovery commands only.                                    | no, if accepted        |

## Related Artifacts

- Requirements: `requirements.md`
- Canonical context: `canonical-context.md`
- Tasks: `tasks.md`
- Traceability: `traceability.md`
- Verification: `verification.md`
