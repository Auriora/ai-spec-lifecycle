---
title: Closure Response Contract
doc_type: spec
artifact_type: requirements
status: active
owner: maintainers
last_reviewed: 2026-07-12
backlog: B063
---

# Requirements

## Context

Closure planning and apply responses exposed complete generated replacements for
history files. Those bodies were not useful to an agent and could consume a
large fraction of its context. The durable runtime contract is
`docs/reference/spec-lifecycle-runtime.md`.

## Durable Source Baseline

- `docs/reference/spec-lifecycle-runtime.md#closure-helper-tools` defines the
  existing closure MCP and retained CLI behavior.
- `docs/backlog/README.md` owns improvement status and routing.

## Goals

- Return only actionable closure information to agents.
- Make sequential closure actions restart-safe and duplicate-free.
- Prevent generated and non-text repository state from becoming scan evidence.

### Requirement 1: Relevant responses only

**User Story:** As a coding agent, I want closure calls to return only data I
can act on, so that lifecycle operations do not displace implementation context.

**Priority:** must-have

#### Acceptance Criteria

1. WHEN `closure_plan` returns, THEN THE SYSTEM SHALL omit complete replacement bodies and return decisions, findings, action handles, paths, hashes, sizes, and short previews only.
2. WHEN more detail is needed, THEN THE SYSTEM SHALL expand one closed section without returning executable replacement content.
3. THE SYSTEM SHALL keep every normal or expanded closure manifest at or below 32 KiB by construction.
4. WHEN an MCP result includes `structuredContent`, THEN THE SYSTEM SHALL provide only a short text summary in `content` rather than serializing the structured payload again.

### Requirement 2: Restart-safe action execution

**User Story:** As an operator, I want closure actions to survive MCP restarts,
so that correctness does not depend on hidden process memory.

**Priority:** must-have

#### Acceptance Criteria

1. WHEN `closure_apply` receives closure inputs and a `plan_id`, THEN THE SYSTEM SHALL regenerate the executable plan from repository state.
2. IF the spec package changed after planning, THEN THE SYSTEM SHALL reject the stale fingerprint.
3. WHEN record rendering is repeated, THEN THE SYSTEM SHALL not create duplicate spec records.
4. WHEN cleanup is requested before matching records exist, THEN THE SYSTEM SHALL reject cleanup.
5. WHEN cleanup follows record rendering, THEN THE SYSTEM SHALL change only the package disposition and SHALL NOT re-render records.

### Requirement 3: Relevant reference discovery

**User Story:** As a coding agent, I want reference scans to ignore generated
and non-text state, so that findings represent sources I can review or edit.

**Priority:** must-have

#### Acceptance Criteria

1. THE SYSTEM SHALL honor repository-root `.gitignore` and `.aiignore` rules.
2. THE SYSTEM SHALL exclude `.git`, `.cache`, databases, WAL/SHM files, Python caches, and binary files.
3. THE SYSTEM SHALL return bounded counts and actionable samples rather than every match.

## Correctness Properties

- P001: No agent-facing edit summary contains a `content` field.
- P002: Repeating `render_records` leaves one closure-log entry and one archive row for the spec ID.
- P003: A spec-package content change changes the plan fingerprint.
- P004: The serialized manifest never exceeds 32 KiB.
- P005: MCP tool `content` remains below 512 bytes and does not repeat structured payload collections.

## Non-goals

- Persisting full plans in MCP process memory or on disk.
- Allowing the response ceiling to hide omitted required actions or blockers.
- Replacing the retained full-plan CLI recovery format in this slice.

## Success Criteria

- MCP responses contain no replacement bodies and serialize below 32 KiB.
- The same manifest can render records and clean up after an MCP restart.
- Full repository validation and bundle parity pass.
