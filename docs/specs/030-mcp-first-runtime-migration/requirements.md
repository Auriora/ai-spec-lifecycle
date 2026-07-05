---
title:           MCP-first runtime migration
doc_type:        spec
artifact_type:   requirements
status:          draft
authoring_mode:  wizard
lifecycle_stage: tasks
owner:           platform
last_reviewed:   2026-07-05
---

# Requirements

## Problem Context

The lifecycle manager currently exposes many deterministic behaviors through
runtime scripts and then wraps selected behavior through MCP tools. That made
early development easy, but it leaves agents with two overlapping contracts:
script commands that can be anything, and MCP tools that are the better defined
agent-facing interface.

The desired direction is MCP-first. Agents should primarily interact with a
defined MCP interface, including state-aware lifecycle tools and capability
reporting. Runtime scripts selected for migration should not remain as parallel
user-facing surfaces after the spec closes. If a script's behavior has moved
into the MCP implementation, the migrated script should be removed by closure.

This requirements-stage artifact captures the MCP migration direction only.
Design, task breakdown, traceability, and verification are intentionally
deferred until these requirements are reviewed.

## Durable Source Baseline

- `docs/backlog/README.md` B055.
- `docs/reference/spec-lifecycle-runtime.md`.
- `docs/reference/spec-lifecycle-manager-mcp-install.md`.
- `skills/spec-lifecycle-manager/scripts/spec_runtime.py`.
- `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`.
- `skills/spec-lifecycle-manager/scripts/codex_spec_lifecycle_hook.py`.
- `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/`.
- `plugins/spec-lifecycle-manager/claude-plugin/skills/spec-lifecycle-manager/`.
- MCP lifecycle initialization, protocol-version negotiation, and capability
  negotiation.
- MCP tools listing, `tools.listChanged`, structured content, and output
  schemas.

## Goals

- Make MCP tools the primary defined interface between agents and lifecycle
  tooling.
- Add an MCP capability/introspection surface that reports protocol version,
  client information when available, server capabilities, dynamic-tool support,
  and observed tool-list refresh behavior.
- Support state-aware lifecycle tools without assuming every MCP client handles
  dynamic tool-list refresh correctly.
- Investigate and test MCP capability detection before committing to coded
  runtime checks, so the design does not add complex compatibility logic that
  fails to improve real agent behavior.
- Migrate selected runtime script behaviors into shared lifecycle modules that
  are surfaced through MCP-owned tools.
- Remove migrated runtime scripts by spec closure so agents do not keep using
  stale parallel script interfaces.
- Preserve deterministic validation, packaging parity, and recovery evidence
  during the migration.

## Non-Goals

- Do not remove scripts that are explicitly retained as packaging, hook,
  installer, or CI internals unless the design selects them for migration.
- Do not rely solely on client name or version hard-coding to decide MCP
  behavior.
- Do not rely on undocumented, experimental, or framework-private agent
  internals for compatibility detection.
- Do not add coded runtime compatibility checks whose behavior cannot be proven
  against supported agents in a development environment.
- Do not require dynamic tool-list support for clients that do not reliably
  process `notifications/tools/list_changed`.
- Do not make lifecycle hooks blocking as part of this migration.
- Do not silently drop CLI recovery paths without a documented replacement for
  CI, package validation, and no-MCP recovery.
- Do not expose the same agent-facing lifecycle tool through both MCP and a
  runtime/CLI command; each tool must have one public owner.

## Requirements

### Requirement 1: MCP-First Agent Interface

**Priority:** Must

**User Story:** As a lifecycle-tool maintainer, I want agents to use MCP tools
as the primary interface, so that lifecycle behavior is exposed through defined
schemas instead of ad hoc script commands.

#### Acceptance Criteria

1. GIVEN lifecycle functionality is available through MCP, WHEN agent-facing
   guidance is updated, THEN THE SYSTEM SHALL present MCP tools as the primary
   interface and script commands as recovery, CI, or debugging paths only.
2. GIVEN a lifecycle behavior is migrated into MCP, WHEN the migrated behavior
   is documented, THEN THE SYSTEM SHALL document the MCP tool contract, input
   schema, output shape, and fallback path.

### Requirement 2: Capability And Client Compatibility Introspection

**Priority:** Should

**User Story:** As a maintainer, I want the MCP server to report negotiated and
observed client capabilities, so that dynamic tool behavior is used only when
the connected agent can actually handle it.

#### Acceptance Criteria

1. GIVEN an MCP session is initialized, WHEN capability introspection is
   requested, THEN THE SYSTEM SHALL report the negotiated protocol version,
   available client information, server capabilities, and whether server-side
   `tools.listChanged` support is enabled.
2. GIVEN the server emits a tool-list-changed notification, WHEN the client
   later requests `tools/list`, THEN THE SYSTEM SHALL record that observed
   refresh behavior for compatibility reporting when the MCP framework exposes
   enough session state.
3. GIVEN the MCP framework does not expose initialization or refresh
   observations, WHEN capability introspection is requested, THEN THE SYSTEM
   SHALL report the field as unknown rather than guessing.
4. GIVEN capability detection depends on undocumented, experimental, or
   framework-private client behavior, WHEN the design is reviewed, THEN THE
   SYSTEM SHALL reject that detection method for runtime gating.
5. GIVEN capability detection cannot be proven in a supported development
   environment, WHEN implementation is planned, THEN THE SYSTEM SHALL use a
   stable fallback tool surface rather than adding speculative runtime checks.

### Requirement 3: Capability Research And Compatibility Checker

**Priority:** Must

**User Story:** As a maintainer, I want capability detection researched and
tested before implementation, so that the migration does not add complex checks
that are unreliable or ineffective.

#### Acceptance Criteria

1. GIVEN the design phase starts, WHEN dynamic tool behavior is considered,
   THEN THE SYSTEM SHALL first document which MCP client implementations and
   agent environments are in scope for compatibility testing.
2. GIVEN an in-scope agent environment is available, WHEN compatibility is
   tested, THEN THE SYSTEM SHALL run a development-environment compatibility
   checker or documented manual test that verifies protocol version reporting,
   tool-list refresh behavior, structured output handling, and fallback
   behavior.
3. GIVEN current compliance information may have changed, WHEN compatibility
   research is performed, THEN THE SYSTEM SHALL include a prompt or documented
   research step to check latest MCP compliance for the target agents before
   enabling dynamic behavior.
4. GIVEN MCP compliance research is recorded, WHEN design decisions cite that
   research, THEN THE SYSTEM SHALL include dated source references or live test
   evidence and SHALL NOT treat documentation claims as stronger than observed
   development-environment behavior.
5. GIVEN compatibility evidence is incomplete, conflicting, or stale, WHEN
   state-aware tooling is implemented, THEN THE SYSTEM SHALL prefer a stable
   MCP tool surface with `available_next_actions` over dynamic tool-list
   changes.
6. GIVEN a compatibility checker is added, WHEN it reports results, THEN THE
   SYSTEM SHALL keep the result advisory and explicit rather than silently
   changing tool behavior based on weak signals.
7. GIVEN dynamic tool-list behavior is considered for implementation, WHEN
   compatibility evidence is reviewed, THEN THE SYSTEM SHALL record a
   compatibility matrix with agent, agent version or date, transport, visible
   protocol version, `tools/list_changed` behavior, structured output behavior,
   fallback behavior, evidence source, result, and decision.

### Requirement 4: Adaptive State-Aware Tool Surface

**Priority:** Could / Conditional

**User Story:** As an agent, I want lifecycle tools to surface the actions that
matter for the current repository/spec state, so that I do not choose from a
large undifferentiated toolbox.

#### Acceptance Criteria

1. GIVEN dynamic tool-list refresh is supported, observed, and accepted by the
   compatibility evidence, WHEN lifecycle state changes, THEN THE SYSTEM SHALL
   expose state-relevant MCP tools and notify the client that the tool list
   changed.
2. GIVEN dynamic tool-list refresh is not supported, unknown, or unobserved,
   WHEN lifecycle state changes, THEN THE SYSTEM SHALL keep a stable MCP tool
   surface and return `available_next_actions` with state-specific sub-actions
   in structured output.
3. GIVEN a client receives either dynamic tools or stable fallback tools, WHEN
   the same lifecycle state is evaluated, THEN THE SYSTEM SHALL return
   equivalent next-action semantics.
4. GIVEN compatibility research does not prove dynamic tool-list behavior is
   reliable and useful for supported agents, WHEN v1 is designed, THEN THE
   SYSTEM SHALL use the stable MCP tool surface with `available_next_actions`
   rather than implementing dynamic tool lists.

### Requirement 5: Runtime Script Migration Inventory

**Priority:** Must

**User Story:** As a maintainer, I want an explicit migration inventory for
runtime scripts, so that closure can prove which scripts moved to MCP and which
scripts intentionally remain.

#### Acceptance Criteria

1. GIVEN runtime scripts exist under `skills/spec-lifecycle-manager/scripts/`,
   WHEN the migration design is prepared, THEN THE SYSTEM SHALL classify each
   relevant script as `migrate_to_mcp`, `retain_internal`, `retain_recovery`,
   or `out_of_scope`.
2. GIVEN a script is classified as `migrate_to_mcp`, WHEN implementation is
   complete, THEN THE SYSTEM SHALL remove that script from the source skill and
   bundled plugin copies before closure.
3. GIVEN a script is retained, WHEN closure evidence is prepared, THEN THE
   SYSTEM SHALL record why the script remains and which contract keeps it from
   being a migrated runtime script.
4. GIVEN a script is classified as `migrate_to_mcp`, WHEN the migration design
   is prepared, THEN THE SYSTEM SHALL record a replacement contract for that
   script including old command or entrypoint, replacement MCP tool, retained
   CI/debug command if any, documentation updates, tests to port, source removal
   paths, bundle removal paths, and installed-cache validation.
5. GIVEN shared implementation logic remains necessary after a script is
   removed, WHEN the design classifies the script, THEN THE SYSTEM SHALL
   distinguish removed executable script surfaces from retained shared modules
   or package internals.

### Requirement 6: Migrated Script Removal By Closure

**Priority:** Must

**User Story:** As a maintainer, I want migrated runtime scripts removed by spec
closure, so that agents cannot keep using obsolete parallel script interfaces.

#### Acceptance Criteria

1. GIVEN a runtime script behavior has been migrated to MCP, WHEN closure check
   runs for this spec, THEN THE SYSTEM SHALL fail or report a blocker if the
   migrated script still exists in source or bundled plugin paths.
2. GIVEN migrated scripts are removed, WHEN package parity validation runs,
   THEN THE SYSTEM SHALL confirm source skill, Codex bundle, Claude bundle, and
   installed cache agree on the removals.
3. GIVEN documentation references a removed migrated script, WHEN closure
   evidence is prepared, THEN THE SYSTEM SHALL update the reference to the MCP
   tool or retained recovery path.
4. GIVEN a migrated script is removed, WHEN closure evidence is prepared, THEN
   THE SYSTEM SHALL verify the script's replacement contract has been satisfied
   rather than relying on deletion alone.

### Requirement 7: MCP Implementation Contract

**Priority:** Must

**User Story:** As an agent or maintainer, I want the MCP implementation to
provide structured outputs and explicit schemas, so that behavior remains
inspectable even when scripts are hidden or removed.

#### Acceptance Criteria

1. GIVEN an MCP tool replaces a runtime script behavior, WHEN the tool returns
   results, THEN THE SYSTEM SHALL provide structured content with stable fields
   for status, diagnostics, affected specs, available next actions, validation
   commands, and residual risk where relevant.
2. GIVEN an MCP tool has an output schema, WHEN validation runs, THEN THE
   SYSTEM SHALL verify representative responses conform to that schema.
3. GIVEN a tool cannot complete because required client or repository
   capabilities are unavailable, WHEN it returns, THEN THE SYSTEM SHALL return
   a structured unsupported or degraded-mode result rather than silently falling
   back.

### Requirement 8: Validation And Recovery During Migration

**Priority:** Must

**User Story:** As a maintainer, I want validation to prove that MCP behavior
replaces the migrated scripts without losing CI or no-MCP recovery, so that the
migration does not strand users or package checks.

#### Acceptance Criteria

1. GIVEN a migrated behavior previously had script tests, WHEN the MCP behavior
   is implemented, THEN THE SYSTEM SHALL move or replace those tests with MCP
   contract tests and parity tests.
2. GIVEN package validation still needs command-line execution, WHEN a script
   is removed, THEN THE SYSTEM SHALL provide a retained runner, package command,
   or documented test harness that is not the migrated runtime script.
3. GIVEN the package is installed locally after migration, WHEN `sync-guard`
   runs, THEN THE SYSTEM SHALL report source, bundle, and installed cache
   parity without migrated-script drift.

### Requirement 9: Single Tool Ownership And Thin Entrypoints

**Priority:** Must

**User Story:** As a lifecycle-tool maintainer, I want each lifecycle tool to
have one public entrypoint with shared implementation internals, so that agents
do not choose between competing MCP and runtime paths for the same behavior.

#### Acceptance Criteria

1. GIVEN an agent-facing lifecycle behavior is exposed as a tool, WHEN the
   behavior is implemented, THEN THE SYSTEM SHALL expose that tool through one
   public owner, with MCP as the default owner for agent-facing lifecycle tools.
2. GIVEN the MCP server exposes a tool, WHEN the tool invokes lifecycle
   behavior, THEN THE SYSTEM SHALL call shared lifecycle functions or services
   directly rather than shelling out to or depending on `spec_runtime.py` as a
   monolithic runtime facade.
3. GIVEN CLI, hook, or recovery entrypoints need related behavior, WHEN they
   execute, THEN THE SYSTEM SHALL keep those entrypoints scoped to validation,
   packaging, install, hook, or emergency recovery workflows and SHALL NOT expose
   duplicate agent-facing lifecycle tools that compete with MCP.
4. GIVEN a retained script contains both entrypoint handling and reusable
   lifecycle logic, WHEN it is touched by this migration, THEN THE SYSTEM SHALL
   either extract the reusable logic to a shared module or record why extraction
   is out of scope for this slice.
5. GIVEN shared logic is extracted, WHEN validation runs, THEN THE SYSTEM SHALL
   prove the MCP-owned tool path uses the shared logic and SHALL separately
   prove retained non-MCP entrypoints do not expose duplicate tool contracts.

## Correctness Properties

- CP-001: Dynamic tool exposure is used only when support is negotiated or
  observed and compatibility evidence is strong enough; otherwise stable
  fallback tools return equivalent next actions.
- CP-002: A script classified as `migrate_to_mcp` cannot remain in source or
  bundle paths at spec closure.
- CP-003: MCP tool outputs remain structured enough for agents to inspect the
  workflow without reading removed scripts.
- CP-004: Package validation remains runnable after migrated scripts are
  removed.
- CP-005: Compatibility detection cannot rely on undocumented agent internals or
  unproven runtime probes.
- CP-006: Each migrated script has a satisfied replacement contract before the
  script removal is accepted as complete.
- CP-007: Each agent-facing lifecycle tool has one public owner; shared modules
  do not become competing public entrypoints.

## Open Questions

| ID     | Question                                                                                                 | Why It Matters                                                                      | Blocking | Likely Destination |
|--------|----------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------|----------|--------------------|
| OQ-001 | Which existing scripts are in scope for migration in the first MCP-first slice?                          | Determines blast radius and closure removal checks.                                 | yes      | `design.md`        |
| OQ-002 | Should the MCP server be rewritten or incrementally adapted before script retirement?                    | Determines whether this spec is a direct migration or a staged architecture change. | yes      | `design.md`        |
| OQ-003 | What is the retained no-MCP recovery path after migrated runtime scripts are removed?                    | Prevents losing CI/debug support while eliminating agent-facing script contracts.   | yes      | `design.md`        |
| OQ-004 | Which clients should be tested for dynamic tool-list behavior before enabling state-specific tool lists? | Avoids relying on spec support that client implementations may not expose well.     | yes      | `verification.md`  |
| OQ-005 | Is dynamic tool-list behavior worth implementing after compatibility research, or should v1 choose a stable per-agent/tool-surface approach? | Prevents overbuilding runtime checks that do not work reliably in real agents. | yes | `design.md` |
| OQ-006 | Which `spec_runtime.py` logic should be extracted into shared modules before or alongside `traceability_lookup.py` migration? | Prevents preserving the current MCP-to-runtime coupling as the long-term architecture. | yes | `design.md` |
| OQ-007 | Which retained runtime commands are validation or recovery commands rather than duplicate lifecycle tools? | Prevents reintroducing parallel MCP and CLI tool surfaces. | yes | `design.md` |

## Success Criteria

- Agents have a clearly documented MCP-first lifecycle interface.
- The MCP server reports compatibility information for dynamic-tool behavior
  where the framework makes it available and the behavior is proven in a
  supported development environment.
- State-aware lifecycle behavior works through dynamic tools only when supported
  and proven; otherwise stable fallback tools return equivalent next actions.
- Every runtime script selected for MCP migration is removed from source,
  bundled plugin copies, documentation, and installed cache by spec closure.
- Agent-facing lifecycle tools have one public MCP-owned path, with retained
  runtime/CLI paths limited to validation, packaging, hooks, install, or
  emergency recovery.
- Validation proves MCP contracts, package parity, and retained recovery paths.
