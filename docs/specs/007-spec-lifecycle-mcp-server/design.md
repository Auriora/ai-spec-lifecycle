---
title: Spec lifecycle MCP server design
doc_type: spec
artifact_type: design
status: draft
owner: platform
last_reviewed: 2026-06-05
---

# Technical Design

## Overview

Add `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`, a
dependency-free JSON-RPC stdio adapter that wraps the existing runtime helpers.
The server is read-only and exposes three MCP surfaces:

- tools for deterministic runtime operations;
- resources for current spec and template context;
- prompts for the existing declarative workflow starters.

## Requirement Coverage

| Requirement | Acceptance Criteria | Design Coverage | Validation Approach |
|-------------|---------------------|-----------------|---------------------|
| Requirement 1 | AC1, AC2, AC3 | JSON-RPC request handler and stdio loop | Subprocess protocol tests |
| Requirement 2 | AC1, AC2, AC3 | Tool dispatch delegates to runtime helpers | Tool call tests and runtime regression tests |
| Requirement 3 | AC1, AC2, AC3 | Resource and prompt adapters | Resource and prompt tests |
| Requirement 4 | AC1, AC2, AC3 | Read-only tool list and no write functions | Code review and tests |
| Requirement 5 | AC1, AC2, AC3 | Docs, skill guidance, and validation evidence | Runtime docs and verification |

## High-Level Design

### System Architecture

```text
MCP client
  -> stdio JSON-RPC
  -> spec_mcp_server.py
  -> spec_runtime.py / traceability_lookup.py
  -> repo docs and skill templates
```

The server does not maintain durable state. Each request resolves the repository
root, calls runtime helpers, and returns JSON-compatible payloads.

### Components and Changes

- `spec_mcp_server.py`:
  Handles newline-delimited JSON-RPC messages, protocol discovery, tool calls,
  resources, and prompts.
- `tests/runtime/test_spec_mcp_server.py`:
  Exercises initialize, tools/list, tools/call, resources/list,
  resources/read, prompts/list, prompts/get, and error handling.
- `docs/reference/spec-lifecycle-runtime.md`:
  Documents the server command, exposed tools/resources/prompts, and remaining
  limits.
- `skills/spec-lifecycle-manager/SKILL.md` and `docs/README.md`:
  Surface install guidance.

### Data Models

Tool result shape:

```json
{
  "content": [{"type": "text", "text": "...json..."}],
  "structuredContent": {},
  "isError": false
}
```

Resource read shape:

```json
{
  "contents": [{"uri": "specs://active", "mimeType": "application/json", "text": "...json..."}]
}
```

Prompt get shape:

```json
{
  "messages": [{"role": "user", "content": {"type": "text", "text": "..."}}]
}
```

### Data Flow

1. Client sends `initialize`.
2. Server reports tools, resources, and prompts capabilities.
3. Client lists or calls a capability.
4. Server validates arguments, delegates to runtime helper, and returns JSON
   data.
5. Unknown methods or invalid arguments return JSON-RPC errors.

## Low-Level Design

### Algorithms and Logic

```text
for each stdin line:
    parse JSON
    if notification: ignore
    dispatch method
    return JSON-RPC response or error
```

Tool dispatch resolves `spec_id` to `docs/specs/{spec_id}` when a direct path
does not exist.

### Function Signatures and Interfaces

Key adapter functions:

```text
handle_request(message: dict, repo_root: Path) -> dict | None
call_tool(name: str, arguments: dict) -> dict
read_resource(uri: str, repo_root: Path) -> dict
get_prompt(name: str, arguments: dict, repo_root: Path) -> dict
serve(repo_root: Path | None) -> int
```

### Error Handling

- Invalid JSON returns JSON-RPC parse errors.
- Unknown methods return method-not-found errors.
- Invalid tool arguments return invalid-params errors.
- Notifications without `id` are ignored.

### Security, Trust, and Access

The adapter exposes no write tools. It reads local repository files through the
same helpers already used by the CLI. Prompt output treats spec and template
content as data and instructs agents to use the skill as the workflow
authority.

### Migration and Compatibility

The server is a thin adapter over current runtime payloads. Future MCP SDK or
transport changes can wrap the same functions without changing the runtime
helpers.

## Validation Strategy

| Validation | Covers | Evidence Location | Residual Risk |
|------------|--------|-------------------|---------------|
| `python3 -m unittest tests.runtime.test_spec_mcp_server` | MCP protocol behavior | `verification.md` | Minimal protocol subset only |
| `python3 -m unittest discover -s tests -p 'test_*.py'` | Full runtime regression | `verification.md` | none expected |
| `spec_runtime.py lint docs/specs/007-spec-lifecycle-mcp-server` | Spec package shape | `verification.md` | none expected |
| `spec_runtime.py closure-check docs/specs/007-spec-lifecycle-mcp-server` | Closure readiness | `verification.md` | none expected |

## Operational Considerations

Run from the repository source:

```bash
python3 skills/spec-lifecycle-manager/scripts/spec_mcp_server.py /path/to/repo
```

Run from an installed skill:

```bash
python3 ~/.codex/skills/spec-lifecycle-manager/scripts/spec_mcp_server.py /path/to/repo
```

Clients should configure this as a local stdio server with the repository root
as the first argument.

## Open Questions

- Whether to package this through the Agent Workbench plugin remains future
  work.
- Whether to add write tools remains explicitly out of scope for this MVP.

## Related Artifacts

- Requirements: requirements.md
- Tasks: tasks.md
- Traceability: traceability.md
- Verification: verification.md
