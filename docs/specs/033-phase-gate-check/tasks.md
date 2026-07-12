---
title: Phase gate check tasks
doc_type: spec
artifact_type: tasks
status: active
authoring_mode: wizard
lifecycle_stage: tasks
owner: platform
last_reviewed: 2026-07-12
---

# Tasks

## Phase 1: Shared Gate Semantics

- [x] T001 Implement phase inference and source summaries
  - Files: shared lifecycle core and focused runtime tests.
  - Implement the public enum, conservative transition table, deterministic
    applicable-source list, and severity-preserving summaries.
  - Acceptance: fixtures cover all phases, unknown/not-applicable behavior,
    unresolved decisions, and source authority preservation.
  - Evidence: 2026-07-12, all eight phases, missing/archived applicability,
    open-decision blocker fixtures, deterministic max-seven source ordering, lazy late
    checks, and diagnostic meaning pass focused tests. Full `npm run validate`
    passed with 260 Python and 25 Node tests.

- [x] T002 Implement upstream fingerprint and staleness states
  - Depends on: T001
  - Files: shared lifecycle core and focused fixtures.
  - Read normalized recorded fingerprints and return current/stale/
    review_required/not_applicable without treating mtimes as proof.
  - Acceptance: content changes invalidate recorded evidence; mtime-only changes
    never produce stale or a new blocker.
  - Evidence: 2026-07-12, matching, changed, missing, mtime-only, read-only, and
    multi-upstream fixtures pass with deterministic current/stale/
    review_required/not_applicable states. Full validation passed with 263
    Python and 25 Node tests.

## Phase 2: Aggregate Contract And Surfaces

- [ ] T003 Render compact, full, section, and stale responses
  - Depends on: T001, T002, Spec 036 T005
  - Apply bounds, deterministic fingerprints, closed sections, refreshed stale
    expansion arguments, and blocker-preservation rules.
  - Acceptance: bounds and stale fixtures pass; mandatory blockers remain visible.

- [ ] T004 Add MCP and retained CLI phase-gate surfaces
  - Depends on: T003
  - Add schemas, dispatch, transport provenance, and parity tests without changing
    established tool responses.
  - Acceptance: MCP/CLI decisions match after metadata removal and normal output
    contains no absolute host paths.

## Phase 3: Packaging And Promotion

- [ ] T005 Synchronize bundles and validate package parity
  - Depends on: each source implementation slice.
  - Acceptance: source/Codex/Claude parity and package contract pass.

- [ ] T006 Promote durable documentation and close B031
  - Depends on: T001-T005.
  - Acceptance: durable design/reference/skill guidance describes shipped
    behavior, full validation passes, and closure records are reconciled.

## Dependency Summary

`T001 -> T002 -> T003 -> T004 -> T005 -> T006`.

## Agent Readiness Contract

T001 is ready. Read requirements, design, tasks, traceability, and verification.
Implement only shared inference/source-summary code and focused tests; do not add
MCP/CLI surfaces or compaction in T001.
