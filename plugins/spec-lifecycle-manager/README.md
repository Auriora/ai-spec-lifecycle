# Spec Lifecycle Manager Codex Plugin

This plugin bundles the `spec-lifecycle-manager` skill, read-only MCP runtime,
prompt definitions, templates, and advisory lifecycle hook.

It packages:

- Full skill and runtime under `skills/spec-lifecycle-manager/`.
- Plugin-scoped MCP server configuration in `.mcp.json`.
- Advisory lifecycle hook configuration in `hooks/hooks.json`.

The plugin is self-contained. The bundled MCP server runs from the installed
plugin cache and delegates to:

```text
skills/spec-lifecycle-manager/scripts/spec_mcp_server.py
```

The MCP runtime is read-only. Hooks are advisory and require the normal Codex
plugin hook trust flow before they run.

Use `scripts/install-spec-lifecycle-manager-package.sh` from this repository to
install or refresh the package for the current user.
