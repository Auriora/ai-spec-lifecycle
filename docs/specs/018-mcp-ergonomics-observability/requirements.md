---
title: MCP ergonomics and observability hardening
doc_type: spec
artifact_type: requirements
status: active
owner: platform
last_reviewed: 2026-06-11
---

# Requirements

## Durable Source Baseline

- `docs/reference/spec-lifecycle-runtime.md` documents the runtime commands,
  MCP tools, resource boundaries, sync guard, and package contract.
- `skills/spec-lifecycle-manager/scripts/spec_runtime.py` is the deterministic
  runtime implementation.
- `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py` exposes the
  read-only MCP tools and resources.
- `tests/runtime/test_spec_mcp_server.py`,
  `tests/runtime/test_spec_runtime.py`, and
  `tests/runtime/test_spec_plugin_package.py` are the regression surfaces.

## Goals

- Make stale or ambiguous spec references resolvable without repeated agent
  guesswork.
- Publish agent-facing selector contracts clearly through MCP schemas.
- Keep `specs://active` and related resources scoped to the target repository,
  not the plugin load path.
- Provide deterministic MCP usage audit data for future conversation reviews.
- Extend parity checks so Codex, Claude, bundled package, and installed cache
  drift are visible before release.

## Non-Goals

- Do not add write-capable MCP tools.
- Do not create a background telemetry service.
- Do not mutate installed caches or running MCP processes from audit commands.
- Do not replace the lifecycle skill workflow with runtime automation.

## Requirements

### Requirement 1: Structured Spec Reference Resolution

**User Story:** As an implementation agent, I want to resolve a spec reference
before using task tools, so that closed, missing, or ambiguous specs produce
clear structured guidance instead of retry loops.

#### Acceptance Criteria

1. GIVEN an active spec ID, WHEN the resolver is called, THEN the system SHALL
   return `status: active` with a repo-relative path.
2. GIVEN a closed spec ID listed in the archive index, WHEN the resolver is
   called, THEN the system SHALL return `status: archived` with archive
   metadata and no active path.
3. GIVEN an unknown spec ID, WHEN the resolver is called, THEN the system SHALL
   return `status: missing` with guidance to use scan or archive history.
4. GIVEN duplicate active package names across docs partitions, WHEN the
   resolver is called by ID, THEN the system SHALL return `status: ambiguous`.

### Requirement 2: Published Selector Contracts

**User Story:** As a tool-calling agent, I want selector parameters to publish
canonical values, aliases, and fallback behavior, so that I do not guess
internal enum names.

#### Acceptance Criteria

1. WHEN `tools/list` returns `review_packet`, THEN the `review_type` schema
   SHALL include canonical review types, aliases, default, and unknown-value
   behavior.
2. WHEN `tools/list` returns `agent_backed_tool`, THEN the `tool_name` schema
   SHALL expose the same review selector contract.

### Requirement 3: Repository-Scoped Resource Payloads

**User Story:** As a user reviewing MCP output, I want resources to report the
target repository only, so that plugin cache paths do not leak into spec
inventory.

#### Acceptance Criteria

1. GIVEN the MCP server is launched from a plugin path with a workspace root
   environment variable, WHEN `specs://active` is read, THEN returned paths
   SHALL be relative to the target repo.
2. WHEN resource payloads are returned, THEN they SHALL include enough root
   binding metadata to explain the selected target repo without exposing cache
   paths as spec package paths.

### Requirement 4: Deterministic MCP Audit Summary

**User Story:** As a maintainer reviewing prior agent conversations, I want a
compact audit summary, so that MCP usage problems are easy to find without
noisy full-session grep.

#### Acceptance Criteria

1. GIVEN a directory of Codex session JSONL files, WHEN the audit command is
   run, THEN the system SHALL report matching session files, explicit
   lifecycle errors, and relevant MCP/resource mentions.
2. WHEN audit results are returned through MCP, THEN payloads SHALL be
   read-only and repo-relative where applicable.

### Requirement 5: Expanded Package Parity Evidence

**User Story:** As a package maintainer, I want parity checks to include every
distribution copy, so that a release cannot accidentally ship stale Codex or
Claude behavior.

#### Acceptance Criteria

1. WHEN `sync-guard` runs in this repository, THEN it SHALL compare source
   skill, Codex bundled skill, Claude bundled skill, installed cache, reload
   advisory, and recent commit evidence.
2. WHEN `package-contract` runs, THEN it SHALL report source-to-Codex and
   source-to-Claude parity.

## Correctness Properties

- CP-001: Resolver output SHALL never require callers to parse exception text
  to distinguish active, archived, missing, and ambiguous references.
- CP-002: MCP resource payloads SHALL not include absolute plugin cache paths
  in spec inventory.
- CP-003: Audit commands SHALL be read-only and deterministic over the supplied
  session files.
- CP-004: Distribution parity checks SHALL compare file content, not only file
  existence.

## Success Criteria

- Runtime and MCP tests cover the new resolver, schema publishing, resource
  scoping, audit summary, and parity surfaces.
- `spec_runtime.py sync-guard .` and `package-contract .` expose Claude parity.
- Runtime reference docs describe the new surfaces.
