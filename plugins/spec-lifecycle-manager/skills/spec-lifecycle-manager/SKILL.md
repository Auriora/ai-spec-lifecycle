---
name: spec-lifecycle-manager
description: Manage AI-assisted implementation specs from intake through reconciliation, implementation, durable documentation promotion, expert review, and closure.
---

# Spec Lifecycle Manager

This plugin wrapper exposes the installed `spec-lifecycle-manager` skill in
Codex plugin discovery. The package installer syncs the full skill runtime to:

```text
~/.codex/skills/spec-lifecycle-manager/
```

When lifecycle work is requested, use that installed skill copy as the
authoritative workflow source. The host-level MCP server configured by the
installer runs:

```text
~/.codex/skills/spec-lifecycle-manager/scripts/spec_mcp_server.py
```

The runtime is advisory and read-only. It does not create specs, edit task
evidence, update durable docs, close packages, remove files, or commit changes.
When the MCP tools are visible in Codex, use them for lifecycle context and
deterministic checks. Run the underlying Python scripts directly only for
implementation validation, CI, MCP debugging, or explicit no-MCP recovery.
