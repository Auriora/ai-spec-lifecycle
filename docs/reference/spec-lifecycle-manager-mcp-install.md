---
title: Spec lifecycle manager plugin install
doc_type: reference
status: active
owner: platform
last_reviewed: 2026-06-11
---

# Spec Lifecycle Manager Plugin Install

## Purpose

Record how the `spec-lifecycle-manager` Codex plugin is packaged, installed,
and validated for this repository.

## Supported Model

Use the spec lifecycle runtime as a self-contained Codex plugin. The plugin
bundles the skill, MCP server definition, prompt definitions, templates,
runtime scripts, and advisory hooks under:

```text
plugins/spec-lifecycle-manager/
```

Supported boundaries:

| Surface | Role | Install path |
|---------|------|--------------|
| Agent Workbench MCP | Repo context, coding-agent runtime support, validation planning, and workspace-aware guidance. | Host-level `mcp_servers.agent-workbench` entry. |
| Spec lifecycle plugin | Spec lifecycle skill, read-only MCP tools, prompt definitions, templates, and advisory hooks. | Plugin cache under `~/.codex/plugins/cache/<marketplace>/spec-lifecycle-manager/<version>/`. |
| Spec lifecycle MCP | Spec inventory, linting, traceability context, prompt definitions, promotion planning, and closure checks. | Plugin-scoped `.mcp.json`, not a host-level `mcp_servers` entry. |
| Spec lifecycle hooks | Advisory lifecycle checks after write tools. | Plugin-scoped `hooks/hooks.json`, subject to normal Codex plugin hook trust. |

Do not install a separate `~/.codex/skills/spec-lifecycle-manager/` copy for
normal operation. Do not add a host-level
`[mcp_servers.spec-lifecycle-manager]` block unless debugging a local runtime
outside the plugin. The package installer removes the old managed global skill,
MCP, and hook entries before installing the plugin bundle.

## Plugin Layout

```text
plugins/spec-lifecycle-manager/
  .codex-plugin/plugin.json
  .mcp.json
  hooks/hooks.json
  skills/spec-lifecycle-manager/
    SKILL.md
    agents/
    prompts/
    references/
    scripts/
```

The manifest points to bundled components with plugin-root-relative paths:

- `skills`: `./skills/`
- `mcpServers`: `./.mcp.json`
- `hooks`: `./hooks/hooks.json`

## Install Flow

Use the package installer from this repository:

```bash
scripts/install-spec-lifecycle-manager-package.sh
```

The installer:

- removes the old managed standalone skill copy at
  `~/.codex/skills/spec-lifecycle-manager/`;
- removes the old managed host-level MCP config block when present;
- removes the old managed global advisory hook when present;
- copies the self-contained plugin to the local marketplace plugin directory;
- updates the local marketplace entry; and
- runs `codex plugin add spec-lifecycle-manager@<marketplace-name>`.

The plugin has no third-party runtime dependencies. It requires Python 3.9 or
newer and otherwise uses the Python standard library.

## Hook Policy

Spec lifecycle hooks are advisory-only. The bundled hook file is:

```text
plugins/spec-lifecycle-manager/hooks/hooks.json
```

The hook runs:

```text
python3 "${PLUGIN_ROOT}/skills/spec-lifecycle-manager/scripts/codex_spec_lifecycle_hook.py"
```

Plugin-bundled hooks follow Codex's plugin hook trust flow. They should stay
quiet on pass and emit additional context only for advisory lifecycle
diagnostics. Future blocking behavior requires a focused spec or backlog item
that defines event source, payload, command, timeout, severity profile,
false-positive handling, rollback path, and validation evidence.

## Validation Checklist

Use this checklist in this repository after install, sync, or reload:

| Check | Expected evidence |
|-------|-------------------|
| Plugin validates | `plugin-creator` validation passes for `plugins/spec-lifecycle-manager`. |
| Plugin is self-contained | `skills/`, `.mcp.json`, `hooks/hooks.json`, scripts, prompts, and references exist under the plugin root. |
| MCP tools visible after reload | Codex exposes plugin-scoped `spec-lifecycle-manager` MCP tools. |
| Server starts | `initialize` returns server name `spec-lifecycle-manager`. |
| Spec scan works | `scan_specs` returns repo-relative paths and the expected active-spec count when `repo_root` is supplied or inferred. |
| Resource scan works | `specs://active` returns repo-relative paths for the target workspace and does not expose the plugin cache or load path. |
| Archive index works | `archive_index` returns no diagnostics for removed package history. |
| Prompt definitions validate | `prompts_validate` returns no diagnostics. |
| Package tools resolve live specs | `closure_check`, `task_context`, or `traceability_lookup` work when an active spec exists. |
| Sync guard is reviewed | In this repository, `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py sync-guard .` reports source/bundle parity, installed cache state, reload advisory, and recent commit evidence. |
| No old standalone skill remains | `~/.codex/skills/spec-lifecycle-manager/` is absent after installer cleanup. |
| No old managed host MCP remains | `~/.codex/config.toml` does not contain the old installer-managed `mcp_servers.spec-lifecycle-manager` block. |

## Troubleshooting

If the tools are not visible after reload:

1. Confirm the plugin appears in `codex plugin list`.
2. Confirm the installed plugin cache contains `.mcp.json`.
3. Confirm the plugin is enabled.
4. Confirm no old host-level `mcp_servers.spec-lifecycle-manager` entry is
   shadowing the plugin-provided server.
5. Run `sync-guard` to compare source, bundled plugin, installed cache, and
   reload advisory state.
6. Restart Codex after plugin reinstall, hook trust changes, or a sync guard
   reload advisory.

## Related Artifacts

- `docs/reference/spec-lifecycle-runtime.md`
- `docs/history/spec-archive-index.md`
- `plugins/spec-lifecycle-manager/.codex-plugin/plugin.json`
- `plugins/spec-lifecycle-manager/.mcp.json`
