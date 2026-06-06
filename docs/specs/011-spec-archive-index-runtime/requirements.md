---
title: Spec archive index runtime requirements
doc_type: spec
artifact_type: requirements
status: archived
owner: platform
last_reviewed: 2026-06-06
---

# Requirements

## Introduction

Spec packages are currently retained in `docs/specs/` as historical records
after closure. The closure log records final spec commits and cleanup commits,
but there is not yet a deterministic archive index or runtime check that lets a
repo safely remove retained spec packages while keeping enough Git-backed
evidence to find their final state.

This spec defines the next implementation slice for archive index and
closure-log runtime support.

## Goals

- Add a durable spec archive index that records closed spec package identity,
  final spec commit, cleanup commit, durable destinations, and retained/removed
  archive action.
- Add runtime validation for archive index and closure-log consistency.
- Preserve Git-backed recoverability before any retained spec package is
  removed.
- Keep default active scans focused on active work while keeping closed specs
  discoverable through index data.

## Non-Goals

- Removing existing archived spec packages in this first implementation slice.
- Replacing `docs/history/spec-closure-log.md`.
- Adding write-capable MCP tools.
- Making blocking hook promotion decisions.

## Durable Source Baseline

| Source | Current behavior relied on | Confidence | Notes |
|--------|----------------------------|------------|-------|
| `docs/design/spec-lifecycle-management.md` | Specs are temporary scaffolding; closure must promote or defer lasting content and record closure evidence. | high | Primary lifecycle source. |
| `docs/history/spec-closure-log.md` | Closed specs are recorded with final spec commit, cleanup commit, durable docs, verification summary, residual risks, and follow-up. | high | Current historical index, but entry shape is manually maintained. |
| `docs/reference/spec-lifecycle-runtime.md` | Runtime exposes scan, lint, closure, hook, and MCP surfaces. | high | New checks should fit this CLI-first runtime. |
| `docs/backlog/README.md` | B003 promotes archive index work into this spec. | high | Planning source for scope. |

## Requirements

### Requirement 1: Durable Archive Index

**User Story:** As a lifecycle maintainer, I want a durable archive index for
closed specs, so that retained or removed spec packages remain discoverable
through Git history.

#### Acceptance Criteria

1. GIVEN a closed spec, WHEN it is recorded in the archive index, THEN the
   index includes spec ID, title, package path, final spec commit, cleanup
   commit, closure action, durable destinations, and verification reference.
2. GIVEN a spec package may be removed after closure, WHEN the archive index is
   checked, THEN it identifies the commit that still contains the final spec
   package.
3. IF final spec commit or cleanup commit evidence is missing, THEN the runtime
   SHALL report a diagnostic instead of silently accepting the entry.

### Requirement 2: Closure Log Consistency

**User Story:** As an agent closing specs, I want runtime checks for closure-log
and archive-index consistency, so that closure evidence does not drift.

#### Acceptance Criteria

1. GIVEN a closure-log entry and archive-index entry for the same spec, WHEN
   validation runs, THEN shared fields match or differences are reported.
2. GIVEN a cleanup commit is marked pending, WHEN validation runs after a later
   cleanup commit exists, THEN the runtime reports the pending cleanup as a
   follow-up finding.
3. IF a closure-log entry references durable docs, THEN validation SHALL check
   that each referenced path exists unless explicitly marked external or
   removed.

### Requirement 3: Runtime And MCP Surface

**User Story:** As a coding agent, I want a deterministic runtime surface for
archive index checks, so that I can inspect closure state before closing or
removing specs.

#### Acceptance Criteria

1. GIVEN the runtime command is called, WHEN archive index validation succeeds,
   THEN it returns JSON with counts, entries, and zero diagnostics.
2. GIVEN inconsistencies exist, WHEN validation runs, THEN it returns JSON
   diagnostics that hooks and MCP tools can reuse.
3. WHERE MCP exposes lifecycle read tools, THE SYSTEM SHALL expose archive index
   state read-only.

### Requirement 4: Safe Cleanup Guidance

**User Story:** As a maintainer, I want cleanup rules for retained versus
removed specs, so that spec package removal is deliberate and reversible
through Git.

#### Acceptance Criteria

1. GIVEN a spec package is retained, WHEN the archive index is updated, THEN the
   action is recorded as retained-as-history.
2. GIVEN a spec package is removed, WHEN the archive index is updated, THEN the
   final spec commit must be recorded before removal.
3. IF cleanup would remove the only durable record of accepted behavior, THEN
   cleanup SHALL be blocked until promotion or deferral evidence is recorded.

## Correctness Properties

- Every removed spec package must have a final spec commit that predates
  removal and contains the package.
- Closure-log and archive-index entries for the same spec must not disagree on
  final spec commit, cleanup commit, or closure action.
- Runtime validation must be read-only and deterministic.
- Missing durable destinations must be reported unless explicitly external or
  intentionally removed.

## Success Criteria

- A spec archive index format exists in durable docs.
- Runtime validation catches missing commits, pending cleanup evidence, and
  durable destination path drift.
- MCP read tools expose archive index state or validation payloads.
- Spec 011 can close without removing historical packages in this slice.
