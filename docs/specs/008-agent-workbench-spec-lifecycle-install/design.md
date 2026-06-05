---
title: Agent Workbench spec lifecycle install design
doc_type: spec
artifact_type: design
status: draft
owner: platform
last_reviewed: 2026-06-05
---

# Technical Design

## Overview

Install and integration are documentation-governed in this slice. The
`spec-lifecycle-manager` MCP server runs as a host-level companion server next
to Agent Workbench. Agent Workbench documentation records the relationship and
the validation checklist, but Agent Workbench runtime code and plugin metadata
remain unchanged.

## Requirement Coverage

| Requirement | Acceptance Criteria | Design Coverage | Validation Approach |
|-------------|---------------------|-----------------|---------------------|
| Requirement 1 | AC1, AC2, AC3 | Host-level companion server model | Agent Workbench reference review |
| Requirement 2 | AC1, AC2, AC3 | New Agent Workbench reference note | File inspection and diff check |
| Requirement 3 | AC1, AC2, AC3 | Advisory-only hook policy | Reference note and verification |
| Requirement 4 | AC1, AC2, AC3 | Validation checklist and live MCP smoke tests | MCP tool calls and config grep |
| Requirement 5 | AC1, AC2 | Backlog B002 status and follow-up handling | Backlog review |

## High-Level Design

### System Architecture

```text
Codex host config
  -> mcp_servers.agent-workbench
       -> ../agent-workbench/src/mcp/stdio.ts
  -> mcp_servers.spec-lifecycle-manager
       -> ~/.codex/skills/spec-lifecycle-manager/scripts/spec_mcp_server.py
       -> /home/bcherrington/Projects/Auriora/agent-dev-lifecycle
```

The two MCP servers are independent. Agent Workbench remains responsible for
repo context and coding-agent runtime behavior. The spec lifecycle server is
responsible for spec inventory, lint, prompt definitions, task context,
promotion planning, and closure checks for `agent-dev-lifecycle`.

### Components and Changes

- Spec 008 package:
  Records requirements, design, five tasks, traceability, and verification.
- Agent Workbench reference note:
  Documents install boundary, config snippet, hook policy, validation
  checklist, and duplicate-instance checks.
- Backlog:
  Marks B002 done because install policy and validation guidance are complete.

### Data Models

Codex host-level MCP config shape:

```toml
[mcp_servers.spec-lifecycle-manager]
command = "python3"
args = [
  "/home/bcherrington/.codex/skills/spec-lifecycle-manager/scripts/spec_mcp_server.py",
  "/home/bcherrington/Projects/Auriora/agent-dev-lifecycle"
]
startup_timeout_sec = 30.0
```

Validation checklist items:

| Check | Expected result |
|-------|-----------------|
| Reload | `mcp__spec_lifecycle_manager` tools visible. |
| Tool discovery | `scan_specs`, `closure_check`, and prompt tools exposed. |
| Scan | `scan_specs` returns `agent-dev-lifecycle` specs. |
| Skill sync | Installed server script is executable. |
| Duplicate instance | No duplicate spec lifecycle MCP entry outside host config. |

### Data Flow

1. Repo source syncs skill to `~/.codex/skills/spec-lifecycle-manager/`.
2. Codex host config launches the installed skill MCP script with the
   `agent-dev-lifecycle` repo root.
3. After reload, Codex exposes `mcp__spec_lifecycle_manager`.
4. Agents use the spec lifecycle MCP server for spec-management checks and
   Agent Workbench for repo/workbench runtime context.

## Low-Level Design

### Algorithms and Logic

No runtime algorithm changes. The decision logic is operational:

```text
if installing executable MCP runtime:
    use host-level Codex config
if packaging Agent Workbench plugin:
    keep it skill/hook-only
if installing hooks:
    advisory only until a separate dogfood promotion decision
```

### Function Signatures and Interfaces

No code interfaces change.

### Error Handling

If the server is missing after reload, validate the host-level TOML entry,
installed script path, executable bit, and restart state before changing Agent
Workbench plugin metadata.

### Security, Trust, and Access

The spec lifecycle MCP server is read-only. Hook guidance remains advisory-only
because blocking lifecycle hooks can interrupt agent workflows and need a
separate dogfood pass.

### Migration and Compatibility

No Agent Workbench runtime migration is required. Existing Agent Workbench MCP
host-level configuration remains authoritative. The spec lifecycle server is a
companion entry.

## Validation Strategy

| Validation | Covers | Evidence Location | Residual Risk |
|------------|--------|-------------------|---------------|
| MCP `scan_specs` through reloaded tools | Requirement 4 | `verification.md` | none |
| MCP `prompts_validate` through reloaded tools | Prompt/tool visibility | `verification.md` | none |
| Config grep for duplicates | Requirement 4 | `verification.md` | limited to local files checked |
| `git diff --check` in both repos | Documentation hygiene | `verification.md` | none |
| Spec lint and closure-check | Spec package shape | `verification.md` | none |

## Operational Considerations

Reload Codex after changing host-level MCP configuration. Re-sync the installed
skill after repo skill changes and before validating the MCP server.

## Open Questions

- None for the five-task install-policy slice.

## Related Artifacts

- Requirements: requirements.md
- Tasks: tasks.md
- Traceability: traceability.md
- Verification: verification.md
