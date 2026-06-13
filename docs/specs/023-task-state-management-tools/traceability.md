---
title: Task state management tools traceability
doc_type: spec
artifact_type: traceability
status: active
owner: platform
last_reviewed: 2026-06-13
---

# Traceability Matrix

## Task To Context Matrix

| Task ID | Requirements | Acceptance Criteria | Design Sections | Change Impact | Verification | Durable Targets | Open Decisions |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T001 | Requirement 1, Requirement 6 | All | Task State Contract, Open Questions | Skill/runtime docs | Docs review | `SKILL.md`, `spec-lifecycle-runtime.md` | Marker semantics |
| T002 | Requirement 1, Requirement 2 | 1-6, 1-3 | Runtime Parsing | Parser model | Runtime tests | `spec_runtime.py`, `traceability_lookup.py` | none |
| T003 | Requirement 1, Requirement 2 | All | Runtime Parsing | Test coverage | Unit tests | `tests/runtime/`, `tests/traceability/` | none |
| T004 | Requirement 2 | All | Task List Tool, Task Detail Tool | Runtime helpers | Unit tests | `spec_runtime.py` | none |
| T005 | Requirement 2 | All | Task List Tool, Task Detail Tool | MCP tools | MCP tests | `spec_mcp_server.py` | none |
| T006 | Requirement 3, Requirement 4, Requirement 5 | 2-5, All, 1 | Task Audit Tool, Reconciliation Classifications, Evidence Depth | Audit helper | Runtime tests | `spec_runtime.py` | none |
| T007 | Requirement 3 | All | Task State Update Tool | Write helper | Runtime tests | `spec_runtime.py` | MCP exposure timing |
| T008 | Requirement 2, Requirement 3, Requirement 4, Requirement 5 | All | Hook Behavior | MCP and hooks | Runtime/MCP/hook tests | MCP server, hook wrapper | MCP exposure timing |
| T009 | Requirement 6 | All | Operational Considerations | Docs/templates/bundles | Full validation | Skill docs, templates, plugin bundles | Marker semantics |
| T010 | Requirement 2, Requirement 4 | 5-6, All | Task Audit Tool, Reconciliation Classifications, Evidence Depth | Cross-spec/evidence-depth audit | Runtime and fixture tests | Runtime, traceability lookup, fixtures | none |

## Requirement To Delivery Matrix

| Requirement | Acceptance Criteria | Design Sections | Tasks | Verification | Durable Targets |
| --- | --- | --- | --- | --- | --- |
| Requirement 1 | 1-6 | Task State Contract, Runtime Parsing | T001, T002, T003 | Parser tests | Runtime and docs |
| Requirement 2 | 1-6 | Task List Tool, Task Detail Tool | T004, T005, T010 | Runtime and MCP tests | Runtime and MCP server |
| Requirement 3 | 1-4 | Task State Update Tool | T006, T007, T008 | Runtime and MCP tests | Runtime and MCP server |
| Requirement 4 | 1-5 | Task Audit Tool, Reconciliation Classifications, Evidence Depth | T006, T010 | Runtime fixture tests | Runtime and traceability lookup |
| Requirement 5 | 1-4 | Hook Behavior | T006, T008 | Hook tests | Runtime hooks |
| Requirement 6 | 1-4 | Operational Considerations | T001, T009 | Docs/template review | Skill docs and templates |

## Design To Implementation Matrix

| Design Section | Requirements | Tasks | Interfaces Or Files | Verification |
| --- | --- | --- | --- | --- |
| Task State Contract | Requirement 1, Requirement 6 | T001, T002, T009 | Skill docs, runtime parser | Parser and docs tests |
| Runtime Parsing | Requirement 1, Requirement 2 | T002, T003 | `spec_runtime.py`, `traceability_lookup.py` | Unit tests |
| Task List Tool | Requirement 2 | T004, T005, T010 | Runtime and MCP server | Runtime/MCP tests |
| Task Detail Tool | Requirement 2 | T004, T005, T010 | Runtime and MCP server | Runtime/MCP tests |
| Task Audit Tool | Requirement 3, Requirement 4, Requirement 5 | T006, T008, T010 | Runtime and hooks | Runtime/hook tests |
| Reconciliation Classifications | Requirement 4 | T006, T010 | Runtime and fixtures | Runtime fixture tests |
| Evidence Depth | Requirement 3, Requirement 4, Requirement 6 | T007, T009, T010 | Runtime, docs, templates | Runtime/docs tests |
| Task State Update Tool | Requirement 3 | T007, T008 | Runtime and MCP server | Runtime/MCP tests |
| Hook Behavior | Requirement 5 | T008 | Hook wrapper/runtime hook | Hook tests |
| Operational Considerations | Requirement 6 | T009 | Docs/templates/bundles | Full validation |

## Open Decision Impact

| Decision ID | Blocks | Affected Requirements | Affected Tasks | Resolution Needed |
| --- | --- | --- | --- | --- |
| D001 | Final marker contract | Requirement 1, Requirement 5 | T001, T002, T009 | Accept or adjust `[>]`, `[-]`, `[?]`, `[!]`, and `[/]` before parser implementation. |
| D002 | Write-tool exposure | Requirement 3 | T007, T008 | Decide whether `set_task_state` is MCP-exposed immediately or CLI-only for initial dogfood. |
