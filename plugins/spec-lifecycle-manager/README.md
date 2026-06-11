# Spec Lifecycle Manager Codex Plugin

This plugin bundles the `spec-lifecycle-manager` skill, read-only MCP runtime,
prompt definitions, templates, and advisory lifecycle hook.

It packages:

- Full skill and runtime under `skills/spec-lifecycle-manager/`.
- Plugin-scoped MCP server configuration in `.mcp.json`.
- Advisory lifecycle hook configuration in `hooks/hooks.json`.
- Claude Code plugin wrapper under `claude-plugin/`.

The plugin is self-contained. The bundled MCP server runs from the installed
plugin cache and delegates to:

```text
skills/spec-lifecycle-manager/scripts/spec_mcp_server.py
```

The MCP runtime is read-only. Hooks are advisory and require the normal Codex
plugin hook trust flow before they run.

For checkout-based development, use
`scripts/install-spec-lifecycle-manager-package.sh` from this repository to
install or refresh the package for the current user.

For npm distribution after publish, use:

```bash
npx @auriora/ai-spec-lifecycle install
```

For Claude Code, load the bundled plugin wrapper from the unpacked package:

```bash
claude --plugin-dir plugins/spec-lifecycle-manager/claude-plugin
```
