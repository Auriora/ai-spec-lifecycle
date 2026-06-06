---
title: Codex hook dogfood requirements
doc_type: spec
artifact_type: requirements
status: archived
owner: platform
last_reviewed: 2026-06-06
---

# Requirements

## Introduction

The spec lifecycle Codex `PostToolUse` hook is installed as an advisory
guardrail. It needs dogfooding on real spec and template edits before any
expansion or blocking behavior is considered.

## Goals

- Measure advisory hook usefulness and noise during real lifecycle edits.
- Record false positives, missed findings, runtime overhead, and operator
  friction.
- Decide whether to keep, refine, expand, or remove the hook.
- Keep blocking hook promotion out of scope until evidence supports it.

## Non-Goals

- Install blocking Codex hooks.
- Change Agent Workbench hook policy.
- Add semantic review hooks that require model judgment.
- Replace MCP tools or the spec lifecycle skill.

## Glossary

| Term | Definition |
|------|------------|
| Advisory hook | Hook that exits zero and provides additional context only when useful. |
| False positive | Hook diagnostic that does not represent useful lifecycle feedback. |
| Dogfood window | A bounded set of real edits used to evaluate the hook before expanding it. |

## Durable Source Baseline

| Source | Current behavior relied on | Confidence | Notes |
|--------|----------------------------|------------|-------|
| `docs/reference/spec-lifecycle-runtime.md` | Documents the Codex hook wrapper and runtime hook modes. | high | Dogfood should validate this guidance. |
| `docs/reference/spec-lifecycle-manager-mcp-install.md` | Documents advisory-only hook policy. | high | Blocking promotion remains deferred. |
| `~/.codex/hooks.json` | Global Codex hook config contains the installed advisory wrapper. | high | Host-level config is outside repo source. |

## Requirements

### Requirement 1: Dogfood Evidence

**User Story:** As a maintainer, I want evidence from real Codex hook runs, so
that hook policy is based on observed behavior rather than assumptions.

#### Acceptance Criteria

1. GIVEN the hook is installed, WHEN real spec or template edits occur, THEN
   the dogfood record SHALL capture whether the hook was quiet, useful, noisy,
   or unavailable.
2. WHERE diagnostics are emitted, THE SYSTEM SHALL record whether they were
   actionable, false positive, or duplicate feedback.
3. IF runtime or output friction appears, THEN the dogfood record SHALL capture
   the observed impact and candidate mitigation.

### Requirement 2: Hook Policy Decision

**User Story:** As a process owner, I want a clear decision after dogfooding,
so that Codex hooks do not grow without evidence.

#### Acceptance Criteria

1. GIVEN dogfood evidence exists, WHEN the evaluation completes, THEN it SHALL
   decide whether to keep, refine, expand, remove, or defer the hook.
2. IF blocking behavior is proposed, THEN the decision SHALL require a
   follow-up spec with event payloads, timeout, severity profile, false-positive
   handling, rollback path, and validation evidence.
3. WHERE the hook remains advisory, THE SYSTEM SHALL document any recommended
   refinements or no-op decision.

### Requirement 3: Validation Coverage

**User Story:** As a maintainer, I want dogfood validation to include both pass
and finding paths, so that the hook remains quiet when useful and visible when
needed.

#### Acceptance Criteria

1. GIVEN clean spec edits occur, WHEN the hook runs, THEN it SHOULD stay quiet.
2. GIVEN known invalid spec edits occur, WHEN the hook runs, THEN it SHALL emit
   concise advisory context.
3. GIVEN template edits occur, WHEN the hook runs, THEN it SHALL route them to
   template lint checks.

## Correctness Properties

- The hook remains advisory and exits zero during dogfooding.
- Hook evidence distinguishes useful findings from false positives.
- Blocking promotion requires a later explicit decision.

## Technical Context

Relevant implementation lives in
`skills/spec-lifecycle-manager/scripts/codex_spec_lifecycle_hook.py`, runtime
hook checks in `skills/spec-lifecycle-manager/scripts/spec_runtime.py`, and
tests in `tests/runtime/test_codex_spec_lifecycle_hook.py`.

## Success Criteria

- Dogfood evidence covers at least three real or representative hook events.
- A keep/refine/expand/remove/defer decision is recorded.
- Any follow-up work is routed to backlog, roadmap, or a focused spec.
