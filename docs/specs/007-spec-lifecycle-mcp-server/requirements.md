---
title: Spec lifecycle MCP server requirements
doc_type: spec
artifact_type: requirements
status: archived
owner: platform
last_reviewed: 2026-06-05
---

# Requirements

## Introduction

Spec 004 produced a dependency-free CLI runtime and declarative MCP prompt
definitions, but left the MCP server adapter as future work. This spec makes
that runtime installable as a local stdio MCP server while keeping the server
read-only and grounded in the `spec-lifecycle-manager` skill.

## Goals

- Add a dependency-free stdio MCP server adapter.
- Expose runtime helpers as MCP tools.
- Expose current spec inventory and related context as MCP resources.
- Expose existing prompt definitions through MCP prompt methods.
- Document local installation and validation.

## Non-Goals

- Add write tools that edit spec packages or durable docs.
- Add HTTP/SSE transport.
- Package a plugin installer.
- Install hooks into Git, Codex, or Agent Workbench.

## Glossary

| Term | Definition |
|------|------------|
| MCP server adapter | JSON-RPC stdio process that exposes the runtime as MCP tools, resources, and prompts. |
| Stdio transport | Local process transport where each JSON-RPC message is sent as a newline-delimited JSON object. |
| Read-only server | Server that reports context and diagnostics but does not mutate repository files. |

## Durable Source Baseline

| Source | Current behavior relied on | Confidence | Notes |
|--------|----------------------------|------------|-------|
| `docs/reference/spec-lifecycle-runtime.md` | States the runtime is CLI-first and no MCP adapter exists. | high | Must be updated after implementation. |
| `docs/specs/004-spec-management-mcp/requirements.md` | Defines MCP resources, tools, prompts, and security requirements. | high | Archived source spec; use as historical design input. |
| `docs/specs/004-spec-management-mcp/design.md` | Defines read-heavy MCP adapter design and stdio development support. | high | Archived source spec; durable docs need current-state update. |
| `skills/spec-lifecycle-manager/scripts/spec_runtime.py` | Provides tested runtime functions to wrap. | high | Adapter should reuse these functions. |
| `skills/spec-lifecycle-manager/prompts/` | Contains prompt definition JSON files. | high | Adapter should expose them through prompt methods. |

## Requirements

### Requirement 1: Stdio MCP Protocol Surface

**User Story:** As an MCP client, I want a stdio server that speaks JSON-RPC,
so that I can discover lifecycle capabilities through MCP.

#### Acceptance Criteria

1. GIVEN an MCP client sends `initialize`, WHEN the server receives it, THEN it
   SHALL return protocol version, server info, and tools/resources/prompts
   capabilities.
2. GIVEN an MCP client sends `tools/list`, `resources/list`, or `prompts/list`,
   WHEN the server receives the request, THEN it SHALL return deterministic
   lists.
3. IF the client sends an unknown method or invalid tool request, THEN the
   server SHALL return a JSON-RPC error instead of crashing.

### Requirement 2: Runtime Tool Exposure

**User Story:** As an implementation agent, I want MCP tools for deterministic
spec checks, so that I can use the same runtime evidence through MCP or CLI.

#### Acceptance Criteria

1. GIVEN a client calls `scan_specs`, WHEN the tool runs, THEN it SHALL return
   the same spec inventory shape as the CLI runtime.
2. GIVEN a client calls lint, next-task, closure, reconciliation, promotion, or
   review tools, WHEN the tool runs, THEN it SHALL delegate to the existing
   runtime helper.
3. WHERE traceability context is requested, THE SYSTEM SHALL use the existing
   traceability lookup helper.

### Requirement 3: Resource And Prompt Exposure

**User Story:** As an MCP client, I want resources and prompts to be
discoverable, so that common lifecycle workflows can be invoked without
duplicating prompt policy.

#### Acceptance Criteria

1. GIVEN a client reads `specs://active`, WHEN the resource is requested, THEN
   it SHALL return the current scan payload.
2. GIVEN a client lists prompts, WHEN prompt definitions exist, THEN the server
   SHALL expose prompt names, descriptions, and arguments from the JSON
   definitions.
3. GIVEN a client gets a prompt, WHEN the prompt exists, THEN the server SHALL
   return messages that direct the agent to use the skill and runtime tools.

### Requirement 4: Read-Only Safety

**User Story:** As a maintainer, I want the MCP server to be read-only for the
MVP, so that clients cannot silently mutate specs or durable docs.

#### Acceptance Criteria

1. GIVEN the server tool list, WHEN tools are inspected, THEN no tool SHALL
   create, update, delete, archive, or commit files.
2. WHERE tool output includes spec content, THE SYSTEM SHALL return it as data,
   not executable instructions.
3. IF future write tools are proposed, THEN they SHALL require a separate spec
   or explicit design update.

### Requirement 5: Install And Validation Guidance

**User Story:** As a local operator, I want installation guidance, so that I
can configure MCP clients to run the server from the repo or installed skill.

#### Acceptance Criteria

1. GIVEN the repository docs are consulted, WHEN MCP installation is needed,
   THEN they SHALL show the stdio command.
2. GIVEN the skill is installed, WHEN the user reloads Codex, THEN the
   installed skill SHALL include the MCP server script and guidance.
3. GIVEN tests run, WHEN validation completes, THEN unit tests and spec
   lifecycle checks SHALL pass.

## Correctness Properties

- **CP-001**: MCP tool outputs match existing runtime helper payloads.
- **CP-002**: The MCP adapter does not write repository files.
- **CP-003**: MCP prompts remain thin workflow starters and do not replace the
  skill.

## Technical Context

- **Language/Version:** Python 3, dependency-free standard library.
- **Primary Dependencies:** Existing `spec_runtime.py` and
  `traceability_lookup.py`.
- **Target Platform:** Local MCP clients using stdio.
- **Constraints:** No network service, no write tools, no external Python
  package dependency.
- **Performance Goals:** Startup and single tool calls should be fast enough
  for local interactive use.

## Success Criteria

- **SC-001**: `spec_mcp_server.py` handles initialize/list/call/read/get
  requests in tests.
- **SC-002**: Runtime unit tests pass.
- **SC-003**: Durable runtime docs no longer say an MCP adapter is missing.

## Related Artifacts

- Design: design.md
- Tasks: tasks.md
- Traceability: traceability.md
- Verification: verification.md
