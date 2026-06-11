# Spec Lifecycle Manager Claude Code Plugin

This plugin packages the Spec Lifecycle Manager skill, read-only MCP server,
and advisory spec lifecycle hook for Claude Code.

The plugin is self-contained. Its MCP configuration launches:

```text
skills/spec-lifecycle-manager/scripts/spec_mcp_server.py
```

Load it locally with:

```bash
claude --plugin-dir plugins/spec-lifecycle-manager/claude-plugin
```

After plugin source changes, run `/reload-plugins` in Claude Code.
