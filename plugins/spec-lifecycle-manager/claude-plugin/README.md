# Spec Lifecycle Manager Claude Code Plugin

This plugin packages the Spec Lifecycle Manager skill, read-only MCP server,
and advisory spec lifecycle hook for Claude Code.

The plugin is self-contained. Its MCP configuration launches:

```text
skills/spec-lifecycle-manager/scripts/spec_mcp_server.py
```

Load it for a single session with:

```bash
claude --plugin-dir plugins/spec-lifecycle-manager/claude-plugin
```

For a persistent install that loads automatically every session, add the
repository root as a local marketplace and install from it:

```bash
claude plugin marketplace add /path/to/agent-dev-lifecycle
claude plugin install spec-lifecycle-manager@ai-spec-lifecycle
```

After plugin source changes, run `/reload-plugins` (per-session load) or
`claude plugin marketplace update ai-spec-lifecycle` (persistent install).
