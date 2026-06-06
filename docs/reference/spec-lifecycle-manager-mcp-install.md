---
title: Spec lifecycle manager MCP install
doc_type: reference
status: active
owner: platform
last_reviewed: 2026-06-05
---

# Spec Lifecycle Manager MCP Install

## Purpose

Record how the `spec-lifecycle-manager` MCP server is installed and validated
alongside Agent Workbench for this repository.

## Supported Model

Use the spec lifecycle MCP server as a host-level companion server. Do not
package it inside the Agent Workbench plugin and do not copy its runtime into
Agent Workbench.

Supported boundaries:

| Surface | Role | Install path |
|---------|------|--------------|
| Agent Workbench MCP | Repo context, coding-agent runtime support, validation planning, and workspace-aware guidance. | Host-level `mcp_servers.agent-workbench` entry. |
| Spec lifecycle MCP | Spec inventory, linting, traceability context, prompt definitions, promotion planning, and closure checks for this repository. | Host-level `mcp_servers.spec-lifecycle-manager` entry. |
| Agent Workbench plugin | Skill and optional quiet hook wrapper for Agent Workbench. | Plugin install only; no executable MCP server registration. |
| Spec lifecycle skill | Workflow guidance and installed MCP server script. | `~/.codex/skills/spec-lifecycle-manager/`. |

This preserves the Agent Workbench architecture rule: executable MCP runtimes
are configured at the Codex host level, while plugins package instructions and
optional hook artifacts.

## Codex Configuration

The local host-level Codex entry is:

```toml
[mcp_servers.spec-lifecycle-manager]
command = "python3"
args = [
  "/home/bcherrington/.codex/skills/spec-lifecycle-manager/scripts/spec_mcp_server.py",
  "/home/bcherrington/Projects/Auriora/agent-dev-lifecycle"
]
startup_timeout_sec = 30.0
```

The first argument points at the installed skill server script. The second
argument fixes the server to this repository.

Do not add this server to:

- `../agent-workbench/plugins/agent-workbench/.codex-plugin/plugin.json`;
- Agent Workbench plugin cache metadata;
- Agent Workbench runtime source;
- cache-relative plugin paths.

## Skill Sync

After changes under `skills/spec-lifecycle-manager/`, sync the installed skill
before validating the MCP server:

```bash
rsync -a --delete \
  /home/bcherrington/Projects/Auriora/agent-dev-lifecycle/skills/spec-lifecycle-manager/ \
  /home/bcherrington/.codex/skills/spec-lifecycle-manager/
```

Then restart or reload Codex.

## Hook Policy

Spec lifecycle hooks are advisory-only by default. The installed skill includes
an advisory Codex `PostToolUse` wrapper:

```text
~/.codex/skills/spec-lifecycle-manager/scripts/codex_spec_lifecycle_hook.py
```

Install it by adding the command to a global Codex `PostToolUse` hook that
matches write tools:

```json
{
  "matcher": "^(apply_patch|write_file|create_file)$",
  "hooks": [
    {
      "type": "command",
      "command": "python3 /home/bcherrington/.codex/skills/spec-lifecycle-manager/scripts/codex_spec_lifecycle_hook.py",
      "statusMessage": "running spec lifecycle advisory hook"
    }
  ]
}
```

The wrapper stays quiet on pass and emits additional context only for advisory
spec lifecycle diagnostics.

Do not install blocking hooks for spec lifecycle checks until a later dogfood
pass proves low false-positive risk and records an explicit promotion decision.
If blocking behavior is proposed, create a focused spec or backlog item that
defines:

- event source and payload;
- command and timeout;
- severity profile;
- false-positive handling;
- rollback path;
- validation evidence.

Agent Workbench hooks remain governed by Agent Workbench's own hook design and
runbook. The spec lifecycle server should not silently change Agent Workbench
hook behavior.

## Validation Checklist

Use this checklist after install, sync, or reload:

| Check | Expected evidence |
|-------|-------------------|
| MCP tools visible after reload | Codex exposes `mcp__spec_lifecycle_manager` tools. |
| Server starts | `initialize` returns server name `spec-lifecycle-manager`. |
| Spec scan works | `scan_specs` returns `/home/bcherrington/Projects/Auriora/agent-dev-lifecycle`. |
| Prompt definitions validate | `prompts_validate` returns no diagnostics. |
| Closure tool works | `closure_check` returns structured readiness for a known spec. |
| Installed skill is synced | `~/.codex/skills/spec-lifecycle-manager/scripts/spec_mcp_server.py` exists and is executable. |
| No duplicate MCP instance | `~/.codex/config.toml` has one host-level `mcp_servers.spec-lifecycle-manager` entry and no plugin-provided duplicate. |

Current validation on 2026-06-05:

- `mcp__spec_lifecycle_manager.scan_specs` returned this repository's spec
  inventory.
- `mcp__spec_lifecycle_manager.prompts_validate` returned four prompts with no
  diagnostics.
- `mcp__spec_lifecycle_manager.closure_check` on spec 007 returned
  `ready: true` with no blockers.
- The installed server script is executable.
- Search found no plugin-provided spec lifecycle MCP server entry.

## Troubleshooting

If the tools are not visible after reload:

1. Confirm `~/.codex/config.toml` parses as TOML.
2. Confirm the installed server script exists and is executable.
3. Run the server command manually with an `initialize` request.
4. Confirm no duplicate plugin-provided MCP server is shadowing the host-level
   entry.
5. Restart Codex after config or skill sync changes.

## Related Artifacts

- `docs/specs/008-agent-workbench-spec-lifecycle-install/`
- `docs/reference/spec-lifecycle-runtime.md`
- `../agent-workbench/docs/runbooks/codex-agent-workbench-plugin.md`
- `../agent-workbench/docs/design/coding-agent-integration-design.md`
