---
title: Agent Workbench spec lifecycle install requirements
doc_type: spec
artifact_type: requirements
status: archived
owner: platform
last_reviewed: 2026-06-05
---

# Requirements

## Introduction

The read-only `spec-lifecycle-manager` MCP server is installed at the Codex
host level and is visible after reload. This spec records the cross-repository
installation guidance for using that server alongside Agent Workbench without
violating Agent Workbench's architecture rule that executable MCP runtimes stay
host-level.

## Goals

- Record the spec lifecycle MCP install model for Agent Workbench users.
- Keep executable MCP server paths out of the Agent Workbench plugin.
- Add Agent Workbench reference guidance under
  `docs/reference/agent-dev-lifecycle/`.
- Decide hook install policy for spec lifecycle checks.
- Capture validation evidence for reload, tool discovery, scan behavior, skill
  sync, and duplicate-instance checks.

## Non-Goals

- Add Agent Workbench plugin code.
- Add a plugin-provided `spec-lifecycle-manager` MCP server.
- Install blocking hooks.
- Change Agent Workbench runtime architecture.

## Glossary

| Term | Definition |
|------|------------|
| Host-level MCP | MCP server configured directly in `~/.codex/config.toml`. |
| Skill sync | Copying `skills/spec-lifecycle-manager/` into `~/.codex/skills/spec-lifecycle-manager/`. |
| Companion server | Separate MCP server used alongside Agent Workbench, not inside its plugin. |

## Durable Source Baseline

| Source | Current behavior relied on | Confidence | Notes |
|--------|----------------------------|------------|-------|
| `docs/backlog/README.md` | B002 tracks Agent Workbench MCP packaging and hook install. | high | This spec promotes B002 into a focused package. |
| `docs/reference/spec-lifecycle-runtime.md` | Documents the read-only stdio MCP server command. | high | Existing current-state runtime guidance. |
| `../agent-workbench/docs/design/coding-agent-integration-design.md` | Requires Agent Workbench executable MCP runtime to be host-level; plugin is skill/hook-only. | high | Governs Agent Workbench side. |
| `../agent-workbench/docs/runbooks/codex-agent-workbench-plugin.md` | Documents host-level MCP setup for Agent Workbench. | high | Companion guidance should align with this model. |

## Requirements

### Requirement 1: Host-Level Install Boundary

**User Story:** As an Agent Workbench operator, I want the spec lifecycle MCP
server installed as a separate host-level server, so that Agent Workbench does
not gain a second executable runtime path.

#### Acceptance Criteria

1. GIVEN Agent Workbench plugin guidance, WHEN spec lifecycle MCP installation
   is documented, THEN it SHALL keep executable MCP configuration at host
   level.
2. WHERE Agent Workbench plugin packaging is discussed, THE SYSTEM SHALL state
   that the plugin must not register or copy the spec lifecycle MCP server.
3. IF both servers are enabled, THEN the guidance SHALL describe them as
   independent companion MCP servers.

### Requirement 2: Agent Workbench Reference Guidance

**User Story:** As a maintainer, I want Agent Workbench to contain a reference
note for the spec lifecycle server, so that future agents can find the install
policy from that repo.

#### Acceptance Criteria

1. GIVEN `../agent-workbench/docs/reference/agent-dev-lifecycle/`, WHEN this
   spec is complete, THEN it SHALL contain a reference note for the
   `spec-lifecycle-manager` MCP install model.
2. GIVEN the note is read, WHEN a user configures Codex, THEN it SHALL show
   the host-level `mcp_servers.spec-lifecycle-manager` entry.
3. GIVEN the note discusses validation, THEN it SHALL include reload, tool
   visibility, scan, skill sync, and duplicate-instance checks.

### Requirement 3: Hook Policy

**User Story:** As a process owner, I want a clear hook install policy, so that
spec lifecycle hooks do not create premature blocking behavior.

#### Acceptance Criteria

1. GIVEN spec lifecycle hooks are discussed, WHEN they are installed or
   recommended, THEN they SHALL be advisory only by default.
2. IF a hook would block agent work, THEN the guidance SHALL require a later
   dogfood pass and explicit promotion decision.
3. WHERE hook ownership is unclear, THE SYSTEM SHALL route follow-up work to
   backlog or a later focused spec rather than silently installing hooks.

### Requirement 4: Validation Evidence

**User Story:** As a local operator, I want validation evidence for the
installed MCP server, so that I know the reload worked.

#### Acceptance Criteria

1. GIVEN Codex was reloaded, WHEN tools are inspected, THEN the
   `mcp__spec_lifecycle_manager` namespace SHALL be visible.
2. GIVEN the server is visible, WHEN `scan_specs` runs, THEN it SHALL return
   the `agent-dev-lifecycle` inventory.
3. GIVEN the install is complete, WHEN duplicate-instance checks run, THEN no
   plugin-provided or duplicate spec lifecycle MCP entry SHALL be found.

### Requirement 5: Backlog Closure

**User Story:** As a maintainer, I want B002 updated, so that completed
install-policy work does not remain proposed.

#### Acceptance Criteria

1. GIVEN B002 is promoted to spec 008, WHEN the tasks complete, THEN B002 SHALL
   be marked done.
2. GIVEN future hook or packaging work remains, WHEN it is not implemented in
   this slice, THEN it SHALL be recorded as a new backlog item or explicit
   residual risk.

## Correctness Properties

- **CP-001**: There is exactly one executable spec lifecycle MCP server entry in
  host-level Codex config.
- **CP-002**: Agent Workbench plugin remains skill/hook-only for its own
  package and does not launch copied spec lifecycle runtime code.
- **CP-003**: Spec lifecycle hooks remain advisory until separately dogfooded.

## Technical Context

- **Language/Version:** Markdown documentation and Codex TOML configuration.
- **Primary Dependencies:** Installed `spec-lifecycle-manager` skill and MCP
  server.
- **Target Platform:** Codex with Agent Workbench and spec lifecycle MCP
  servers enabled.
- **Constraints:** Do not mutate Agent Workbench runtime code.
- **Performance Goals:** Not applicable.

## Success Criteria

- **SC-001**: Agent Workbench reference guidance exists.
- **SC-002**: Validation checklist records live MCP tool evidence.
- **SC-003**: B002 is marked done or replaced by a precise follow-up item.

## Related Artifacts

- Design: design.md
- Tasks: tasks.md
- Traceability: traceability.md
- Verification: verification.md
