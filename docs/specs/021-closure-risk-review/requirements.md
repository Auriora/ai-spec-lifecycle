---
title: Closure risk review requirements
doc_type: spec
artifact_type: requirements
status: active
owner: platform
last_reviewed: 2026-06-13
---

# Requirements

## Durable Source Baseline

- Backlog item B008 requests advisory closure risk review.
- `closure_check`, `promotion_plan`, `archive_index`, `review_packet`, and
  future validation/evidence surfaces provide existing inputs.
- Closure policy requires durable promotion, evidence, residual risk, and
  cleanup records before package removal.
- Conversation review on 2026-06-13 clarified that historical Git commits lower
  recovery risk, but stale active documentation creates higher operational risk
  because tools and agents can surface obsolete guidance as if it were current.

## Goals

- Add deterministic closure risk review before active spec removal.
- Combine closure readiness, promotion targets, evidence quality, validation
  plan coverage, and archive-index readiness.
- Treat stale, superseded, or misleading active documentation as a live guidance
  risk, not merely as a recoverable archive concern.
- Keep the surface read-only and advisory.

## Non-Goals

- Do not run secondary model reviews.
- Do not remove packages or write closure records.
- Do not make closure blocking by default.

## Requirements

### Requirement 1: Risk Signal Aggregation

**User Story:** As a maintainer, I want closure risk signals in one payload, so
that I can see whether a spec is truly safe to remove.

#### Acceptance Criteria

1. GIVEN a spec path, WHEN closure risk review runs, THEN the system SHALL
   include closure readiness, lint summary, promotion target status, task
   evidence quality, validation plan coverage, and unresolved follow-up notes.
2. WHERE a required signal is unavailable, THE SYSTEM SHALL report an explicit
   blind spot instead of silently passing.
3. IF closure check is ready but evidence quality is weak, THEN the system
   SHALL still report closure risk.
4. IF stale or superseded documentation remains in active docs, THEN THE SYSTEM
   SHALL report the paths and identify the consumer risk for tools, agents, or
   maintainers that may use that content as current guidance.
5. IF removed spec content remains recoverable through closure log, archive
   index, and Git commits, THEN THE SYSTEM SHALL treat that as recovery
   evidence, not as a reason to keep obsolete active docs.

### Requirement 2: Risk Classification

**User Story:** As an agent, I want risk severity and recommended action, so
that I can decide whether to close, defer, or strengthen evidence.

#### Acceptance Criteria

1. WHEN no material risks are found, THEN the review SHALL return
   `risk_level: low`.
2. WHEN weak evidence, missing durable promotion, unresolved decisions, or
   validation gaps exist, THEN the review SHALL return `medium` or `high`
   according to severity.
3. WHEN package removal would lose the only current-state documentation, THEN
   the review SHALL return `high`.
4. WHEN stale active documentation is likely to be surfaced by lifecycle tools,
   Agent Workbench, search, or agent context assembly as current guidance, THEN
   the review SHALL return `medium` or `high` even if the old content is
   recoverable from Git history.
5. WHEN the only concern is historical recoverability and the archive index,
   closure log, and Git commit evidence are present, THEN the review SHALL
   lower that concern to `low` or an informational finding.

### Requirement 3: MCP Surface

**User Story:** As a tool-calling agent, I want closure risk exposed through
MCP, so that closure workflows can use it before cleanup.

#### Acceptance Criteria

1. WHEN MCP tools are listed, THEN `closure_risk_review` SHALL be available.
2. WHEN called, THEN it SHALL return risk level, findings, blind spots,
   recommended action, and input signal summaries.

## Correctness Properties

- CP-001: Review output SHALL be deterministic for the same repo state.
- CP-002: The tool SHALL not mutate specs, closure log, archive index, or code.
- CP-003: Findings SHALL reference concrete source artifacts or named blind
  spots.

## Success Criteria

- Runtime/MCP tests cover low-risk and risky closure examples.
- Runtime/MCP tests cover stale-active-doc risk separately from Git-history
  recoverability.
- Runtime docs publish closure risk review behavior.
