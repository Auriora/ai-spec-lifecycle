---
title:           MCP-first runtime migration canonical context
doc_type:        spec
artifact_type:   canonical-context
status:          draft
authoring_mode:  wizard
lifecycle_stage: tasks
owner:           platform
last_reviewed:   2026-07-05
---

# Canonical Context

## Purpose

This file identifies the working authorities for the MCP-first runtime
migration spec. The spec changes agent-facing interfaces, runtime script
status, package parity expectations, and MCP compatibility behavior, so the
requirements must distinguish current durable sources from candidate migration
decisions.

## Authority Hierarchy

The spec-local context is canonical only for this MCP-first runtime migration
slice. It does not override system, developer, or user instructions,
`AGENTS.md`, governance, policy, source-code contracts, tests, generated
contracts, package manifests, live MCP behavior, or validation evidence.

## Always-Canonical External Sources

| Source                                                            | Authority reason                           | Handling                                                     |
|-------------------------------------------------------------------|--------------------------------------------|--------------------------------------------------------------|
| active session instructions                                       | Highest-priority task and policy direction | Preserve unless superseded by newer user direction.          |
| `AGENTS.md`                                                       | Repository instructions                    | Read before changing governed paths.                         |
| `docs/governance/constitution.md`                                 | Governance policy                          | Stop for a decision if this spec conflicts with it.          |
| source code, tests, package manifests, and installed MCP behavior | Implementation truth                       | Treat conflicts as reconciliation inputs, not spec override. |
| live validation evidence                                          | Current system state                       | Prefer over stale docs when validating migration state.      |

## Spec-Canonical Working Sources

| Source                       | Role                               | Scope     | Notes                                                                                         |
|------------------------------|------------------------------------|-----------|-----------------------------------------------------------------------------------------------|
| `requirements.md`            | draft accepted intent after review | this spec | Requirements are draft until reviewed.                                                        |
| `design.md`                  | draft implementation approach      | this spec | Design chooses stable MCP tools for v1 and a narrow script migration scope.                   |
| User direction on 2026-07-05 | migration constraint               | this spec | MCP tools are preferred agent interface; migrated runtime scripts must be removed by closure. |
| User direction on 2026-07-05 | compatibility constraint           | this spec | Investigate and test capability detection first; prefer stable per-agent compatibility checks over flaky runtime checks based on undocumented agent internals. |
| Requirements review on 2026-07-05 | review constraint | this spec | Add requirement priorities, script replacement contracts, measurable compatibility evidence, and a clear distinction between removed executable scripts and retained shared internals. |
| User direction on 2026-07-05 | architecture constraint | this spec | MCP, hooks, runtime, and CLI entrypoints should be thin adapters over shared lifecycle logic; MCP should not depend on `spec_runtime.py` as its implementation facade. |
| User direction on 2026-07-05 | tool ownership constraint | this spec | Each agent-facing lifecycle tool must have one public path. MCP owns the public tool path; runtime/CLI paths are validation, packaging, install, hook, or emergency recovery only. |

## Imported Sources

| Spec path         | Source path                                                                   | Source revision or date | Status     | Canonical scope                                                                    | Promotion target                                       |
|-------------------|-------------------------------------------------------------------------------|-------------------------|------------|------------------------------------------------------------------------------------|--------------------------------------------------------|
| `requirements.md` | `docs/backlog/README.md` B055                                                 | 2026-07-05 working tree | summarized | Backlog source for MCP/runtime migration direction.                                | `docs/backlog/README.md`                               |
| `requirements.md` | `docs/reference/spec-lifecycle-runtime.md`                                    | 2026-07-05 working tree | summarized | Current runtime, MCP tool, prompt, hook, validation, and script recovery behavior. | `docs/reference/spec-lifecycle-runtime.md`             |
| `requirements.md` | `docs/reference/spec-lifecycle-manager-mcp-install.md`                        | 2026-07-05 working tree | summarized | Current MCP install and package integration behavior.                              | `docs/reference/spec-lifecycle-manager-mcp-install.md` |
| `requirements.md` | `skills/spec-lifecycle-manager/scripts/spec_runtime.py`                       | 2026-07-05 working tree | adapted    | Current deterministic runtime behavior and CLI command surface.                    | MCP implementation docs and retained recovery docs     |
| `requirements.md` | `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`                    | 2026-07-05 working tree | adapted    | Current MCP server implementation surface.                                         | MCP implementation docs                                |
| `requirements.md` | `skills/spec-lifecycle-manager/scripts/codex_spec_lifecycle_hook.py`          | 2026-07-05 working tree | background | Current hook bridge behavior; migration scope is undecided.                        | Hook docs only if design selects hook migration        |
| `requirements.md` | `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/`               | 2026-07-05 working tree | adapted    | Bundled Codex plugin copy that must mirror source changes.                         | Package parity evidence                                |
| `requirements.md` | `plugins/spec-lifecycle-manager/claude-plugin/skills/spec-lifecycle-manager/` | 2026-07-05 working tree | adapted    | Bundled Claude plugin copy that must mirror source changes.                        | Package parity evidence                                |

## Non-Canonical Background Sources

| Source                                                              | Reason non-canonical                          | Handling                                            |
|---------------------------------------------------------------------|-----------------------------------------------|-----------------------------------------------------|
| Archived spec packages referenced by closure history                | historical, not active implementation context | Use only as background or drift evidence.           |
| Conversation history not captured in this spec                      | advisory input, not requirements              | Promote only through reviewed spec edits.           |
| External MCP discussions not reflected in durable docs or this spec | not imported for this slice                   | Use only as background research if design needs it. |

## Promotion Map

| Spec-local content                                                 | Durable destination or route                                                  | Required before closure |
|--------------------------------------------------------------------|-------------------------------------------------------------------------------|-------------------------|
| MCP-first interface behavior                                       | `docs/reference/spec-lifecycle-runtime.md` and MCP install docs as applicable | yes                     |
| Runtime script migration inventory and retirement policy           | `docs/reference/spec-lifecycle-runtime.md`, package docs, and backlog updates | yes                     |
| Compatibility behavior for dynamic tools and stable fallback tools | Runtime docs and MCP tool schemas                                             | yes                     |
| Requirement priorities and script replacement contracts           | Requirements, design, traceability, and closure evidence                      | yes                     |
| Stable-tool v1 design and traceability script migration scope     | `docs/reference/spec-lifecycle-runtime.md`, MCP tool docs, package docs       | yes                     |
| Shared lifecycle module architecture and thin-entrypoint rule     | Runtime docs, MCP docs, and implementation package structure                  | yes                     |
| Single public tool ownership and retained recovery boundaries     | Runtime docs, MCP docs, validation docs, and package guidance                 | yes                     |
| Package parity and install validation evidence                     | Closure log and archive index after implementation                            | yes                     |

## Drift Risks

- Existing docs may still describe scripts as the primary recovery or agent
  interface after MCP migration.
- Plugin bundle copies may retain scripts removed from the source skill unless
  package parity is validated.
- Installed cache may remain stale after source and bundle updates unless the
  package install flow is rerun.
- Dynamic MCP tool-list support may vary by client even when the protocol
  supports `notifications/tools/list_changed`.
