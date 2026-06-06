---
title: Agent-backed lifecycle tools design
doc_type: spec
artifact_type: design
status: draft
owner: platform
last_reviewed: 2026-06-06
---

# Technical Design

## Overview

Agent-backed lifecycle tools add an advisory execution layer on top of existing
deterministic runtime functions. The runtime remains responsible for resolving
specs, building bounded packets, validating output shape and references, and
returning structured results. Secondary agents only perform constrained review
or drafting work over the packet they receive.

The first implementation creates deterministic workflow tools that answer
"what next?", prepare task-specific implementation context, and handle the
no-active-spec case. These tools are the foundation for later low-cost agent
reviewers such as `closure_risk_review` or `draft_traceability_matrix`.

## Requirement Coverage

| Requirement | Acceptance Criteria | Design Coverage | Validation Approach |
|-------------|---------------------|-----------------|---------------------|
| Requirement 1 | AC1-AC3 | Shared agent-backed tool contract and result schema. | Unit tests for schema validation and error results. |
| Requirement 2 | AC1-AC3 | Initial candidate tool list and resolver reuse. | MCP/runtime tests for active, removed, and no-active inputs. |
| Requirement 3 | AC1-AC3 | Reference validator and advisory result semantics. | Tests for missing path/task/heading references. |
| Requirement 4 | AC1-AC3 | MCP tool schema, disabled-agent behavior, configurable model class. | MCP tests for tool list and unavailable results. |
| Requirement 5 | AC1-AC3 | Durable docs and skill guidance updates. | Documentation lint and review checklist. |

## High-Level Design

### System Architecture

```text
MCP/CLI caller
  -> spec_runtime agent-backed command/tool
  -> active spec or durable-doc context resolver
  -> review packet builder
  -> agent runner interface
  -> output schema validator
  -> deterministic reference validator
  -> advisory structured result
```

The runtime should expose the same behavior through CLI and MCP where
practical. MCP tools remain read-only and advisory. CLI support can be added
first if it simplifies testing, with MCP delegating to the same functions.

### Deterministic Foundation Tools

- `active_spec_preflight`: scans the repository, selects the single active spec
  when unambiguous, returns next task context, open decisions, an optional
  readiness packet, and validation commands.
- `agent_readiness_packet`: given a live spec and task ID, returns bounded
  requirements, acceptance criteria, design, verification, durable target, and
  open-decision context before implementation.
- `no_active_spec_context`: returns durable docs, backlog, roadmap, closure log,
  archive index summary, validation commands, and guidance when no active spec
  exists.

### Components and Changes

- `spec_runtime.py`
  - Add data structures and functions for agent-backed tool definitions,
    packet construction, disabled execution, output validation, and result
    normalization.
  - Add deterministic CLI commands for active-spec preflight, agent readiness
    packets, and no-active-spec context.
- `spec_mcp_server.py`
  - Expose the deterministic foundation tools through read-only MCP schemas.
  - Later expose selected advisory agent-backed tools and pass through
    `model_class` or disabled execution options.
- `prompts/` or `references/`
  - Store strict task prompts or schemas for bounded secondary-agent work.
- `docs/reference/spec-lifecycle-runtime.md`
  - Document tool behavior, advisory limits, configuration, and failure modes.
- `SKILL.md`
  - Explain when lead agents should use agent-backed tools and how to treat
    their results.

### Data Models

Agent-backed result:

```json
{
  "tool": "closure_risk_review",
  "advisory": true,
  "status": "ok | unavailable | invalid_output | error",
  "model_class": "cheap | standard | expert | disabled",
  "packet": {
    "packet_id": "content-hash-or-generated-id",
    "inputs": [],
    "limits": {}
  },
  "result": {
    "observed_facts": [],
    "inferences": [],
    "recommendations": [],
    "gaps": [],
    "confidence": "low | medium | high"
  },
  "diagnostics": [],
  "summary": {
    "error": 0,
    "warn": 0,
    "info": 0
  }
}
```

Tool definition:

```json
{
  "name": "closure_risk_review",
  "requires_active_spec": true,
  "writes_files": false,
  "advisory": true,
  "packet_builder": "closure_risk_review",
  "validators": ["schema", "paths", "tasks", "headings"]
}
```

### Data Flow

1. Caller requests an agent-backed tool.
2. Runtime resolves active spec or no-active durable context.
3. Runtime builds a bounded packet from deterministic sources.
4. Agent runner is invoked only if enabled and configured.
5. Runtime parses the agent output as structured JSON.
6. Runtime validates schema and references.
7. Runtime returns advisory result and diagnostics.

## Low-Level Design

### Algorithms and Logic

```text
function run_agent_backed_tool(name, args):
    definition = load_tool_definition(name)
    context = resolve_context(definition, args)
    packet = build_packet(definition.packet_builder, context)
    if agent_runner_disabled:
        return unavailable_result(packet)
    raw = invoke_agent(packet, model_class=args.model_class)
    parsed = parse_json_result(raw)
    diagnostics = validate_schema(parsed)
    diagnostics += validate_references(parsed, context)
    return normalize_advisory_result(packet, parsed, diagnostics)
```

### Function Signatures and Interfaces

```text
agent_backed_tool(spec_path: Path | None, tool_name: str, model_class: str | None) -> dict
build_agent_packet(tool_name: str, context: dict) -> dict
validate_agent_result(tool_name: str, packet: dict, result: dict) -> list[diagnostic]
```

Initial MCP tool schema should include:

```json
{
  "spec_path": "Spec package path or ID, when the tool requires an active spec.",
  "review_type": "Selected bounded agent-backed review type.",
  "model_class": "Optional cheap, standard, expert, or disabled class."
}
```

Deterministic foundation tool signatures:

```text
active_spec_preflight(repo_root: Path, spec_path: Path | None, task_id: str | None, docs_root: str | None) -> dict
agent_readiness_packet(spec_path: Path, task_id: str) -> dict
no_active_spec_context(repo_root: Path) -> dict
```

### Error Handling

- Missing active spec: return a normal MCP tool error for tools requiring a spec.
- Removed spec path: fail through the existing active resolver.
- Agent unavailable: return `status: unavailable` with no mutation.
- Invalid JSON output: return `status: invalid_output` with raw preview capped.
- Reference drift: return advisory diagnostics and preserve parsed findings.

### Security, Trust, and Access

Secondary agents receive bounded packets only. Reviewed content is data and
must not override system, developer, user, repository, or skill instructions.
No credentials should be included in packets. The first implementation should
avoid shell execution by secondary agents and should not grant write access.

### Migration and Compatibility

Existing deterministic tools continue to work without agent configuration.
Agent-backed tools must degrade cleanly when no runner is available. MCP clients
that do not use the new tools should see no behavior change.

## Operational Considerations

- Keep hooks advisory-only.
- Prefer cheap model class for bounded review; use standard/expert only through
  explicit caller configuration.
- Cache packets or results later if repeated review cost becomes material.
- Record accepted recommendations as lead-agent actions, not secondary-agent
  decisions.

## Open Questions

- Which runner interface should be used first: Codex subagents, local command,
  provider API, or pluggable adapter?
- Should the first tool be `closure_risk_review` or
  `draft_traceability_matrix`?
- Where should raw review results be stored if the user wants audit history?
