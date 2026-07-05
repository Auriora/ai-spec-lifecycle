---
title: Spec closure helper
doc_type: spec
artifact_type: requirements
status: draft
authoring_mode: wizard
lifecycle_stage: requirements
owner: platform
last_reviewed: 2026-07-05
---

# Requirements

## Problem Context

Closing completed specs still requires several ordered steps that are easy for
agents to blur together: confirm durable promotion, identify the final spec
commit, remove or archive the temporary package, update closure history, update
archive index metadata, route follow-up work, and rerun validation. Recent
closures have succeeded, but the workflow still depends on agent memory and
manual sequencing.

Backlog item B056 proposes a structured helper for this closure workflow. This
requirements-stage artifact captures the desired behavior only; design, tasks,
traceability, and verification are intentionally deferred until the requirements
are reviewed.

## Durable Source Baseline

- `docs/backlog/README.md` B056.
- `docs/history/spec-closure-log.md`.
- `docs/history/spec-archive-index.md`.
- `docs/reference/spec-lifecycle-runtime.md`.
- `skills/spec-lifecycle-manager/SKILL.md`.

## Goals

- Provide a structured closure helper for the "make durable, cleanup, remove"
  workflow.
- Preserve the current policy that specs are temporary delivery scaffolding and
  accepted behavior must be promoted to durable docs before closure.
- Keep human closure review explicit; the helper should organize and check the
  workflow, not silently close specs.
- Return concrete validation and recovery commands for the closure sequence.
- Distinguish final-spec evidence from cleanup evidence so archive entries can
  reference the correct commits.

## Non-Goals

- Do not replace `closure_check`, `promotion_plan`, `archive_index`, or
  `sync_guard`; compose or extend existing lifecycle surfaces where possible.
- Do not make advisory hooks blocking.
- Do not close or remove any active spec automatically without an explicit user
  request.
- Do not introduce broad lifecycle refactors outside the closure-helper surface.

## Requirements

### Requirement 1: Closure Workflow Checklist

**User Story:** As a maintainer, I want a closure helper to enumerate the
required closure steps, so that completed specs are closed consistently without
depending on session memory.

#### Acceptance Criteria

1. GIVEN an active spec package, WHEN the closure helper is requested, THEN THE
   SYSTEM SHALL report the ordered closure workflow: durable promotion review,
   final spec commit capture, package cleanup, closure-log update,
   archive-index update, follow-up routing, and validation.
2. GIVEN a closure step has insufficient evidence, WHEN the helper reports the
   workflow, THEN THE SYSTEM SHALL mark that step as blocked or incomplete
   rather than treating the closure as ready.

### Requirement 2: Durable Promotion Confirmation

**User Story:** As a maintainer, I want durable promotion targets checked before
cleanup, so that removed spec packages do not hide accepted behavior that never
landed in durable docs.

#### Acceptance Criteria

1. GIVEN a spec references durable destinations, WHEN the helper evaluates
   closure readiness, THEN THE SYSTEM SHALL identify the durable paths that need
   confirmation before cleanup.
2. GIVEN durable promotion is incomplete or unclear, WHEN closure guidance is
   returned, THEN THE SYSTEM SHALL keep the package cleanup step blocked until
   the missing durable outcome is resolved or explicitly waived.

### Requirement 3: Commit Evidence Separation

**User Story:** As a maintainer, I want final-spec and cleanup commits separated,
so that archive history points to both the completed package snapshot and the
actual package removal.

#### Acceptance Criteria

1. GIVEN a completed spec package, WHEN closure metadata is prepared, THEN THE
   SYSTEM SHALL distinguish the final spec commit from the cleanup commit.
2. GIVEN the cleanup commit is not available yet, WHEN the helper prepares
   closure guidance, THEN THE SYSTEM SHALL return a pending cleanup-commit
   placeholder instead of inventing a commit hash.

### Requirement 4: Follow-Up Routing

**User Story:** As a maintainer, I want unresolved work routed during closure,
so that residual risks and future work remain visible after the package is
removed.

#### Acceptance Criteria

1. GIVEN a spec has deferred work, residual risks, or rejected scope, WHEN
   closure guidance is returned, THEN THE SYSTEM SHALL route each item to a
   durable destination such as backlog, roadmap, ADR, runbook, or a follow-up
   spec recommendation.
2. GIVEN no follow-up work remains, WHEN closure guidance is returned, THEN THE
   SYSTEM SHALL state that explicitly rather than omitting the routing step.

### Requirement 5: Validation And Recovery Commands

**User Story:** As a maintainer, I want closure validation commands returned
with the workflow, so that a completed closure can be verified without
reconstructing the command sequence.

#### Acceptance Criteria

1. GIVEN closure guidance is returned, WHEN validation is required, THEN THE
   SYSTEM SHALL include repo-appropriate commands for scan, archive index,
   closure readiness, package contract or sync checks when applicable, and
   whitespace or test validation.
2. GIVEN MCP tools are unavailable, WHEN closure guidance is returned, THEN THE
   SYSTEM SHALL include equivalent `spec_runtime.py` recovery commands.

## Correctness Properties

- CP-001: The helper never reports cleanup-ready when durable promotion is
  unresolved.
- CP-002: The helper never invents a final spec commit or cleanup commit.
- CP-003: The helper preserves a durable route for every unresolved follow-up
  item before package cleanup is considered complete.

## Open Questions

| ID | Question | Why It Matters | Blocking | Likely Destination |
|----|----------|----------------|----------|--------------------|
| OQ-001 | Should the helper be a new MCP tool, a prompt workflow, or an extension of `closure_check` / `promotion_plan` output? | Determines implementation surface and compatibility risk. | yes | `design.md` |
| OQ-002 | Should the helper update files directly in a future write-capable mode, or stay read-only and return an edit plan? | Affects approval policy and safety boundaries. | yes | `design.md` |
| OQ-003 | Which closure validation commands are always required versus package-repo-specific? | Prevents over-validating ordinary target repos while preserving package parity checks here. | yes | `verification.md` |

## Success Criteria

- A maintainer can request closure guidance for an active spec and receive a
  complete ordered workflow with blockers, evidence needs, follow-up routing,
  and validation commands.
- The helper keeps package cleanup blocked until durable promotion and closure
  metadata are ready.
- Requirements are accepted before design, tasks, traceability, and verification
  artifacts are created for this spec.
