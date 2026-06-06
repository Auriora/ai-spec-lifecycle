---
title: Plugin comparison improvements tasks
doc_type: spec
artifact_type: tasks
status: draft
owner: platform
last_reviewed: 2026-06-06
---

# Tasks

## Phase 1: Comparative Analysis

- [ ] T001 Create durable plugin comparison artifact.
  - Requirements: Requirement 1, Requirement 5
  - Acceptance: Artifact preserves Praxis, Spec Driven, Superpowers, and Codex
    plugin docs references with accepted/deferred/rejected idea routing.
  - Evidence:

- [ ] T002 Resolve comparison scope decisions.
  - Requirements: Requirement 1, Requirement 5
  - Acceptance: D001-D005 are accepted, rejected, or deferred with rationale.
  - Depends on: T001
  - Evidence:

## Phase 2: Agent-Facing Workflow Improvements

- [ ] T003 Add lifecycle status/validate/complete prompt aliases or equivalent MCP prompt definitions.
  - Requirements: Requirement 3
  - Acceptance: Users have clear Codex-facing routes for status, validation,
    and completion workflows; prompt validation passes.
  - Depends on: T002
  - Evidence:

- [ ] T004 Add lifecycle triage guidance or prompt if accepted.
  - Requirements: Requirement 2
  - Acceptance: Triage categories and routing are visible to agents; trivial
    and small work avoid default spec creation.
  - Depends on: T002
  - Evidence:

- [ ] T005 Add lifecycle gate language or structured output if accepted.
  - Requirements: Requirement 4
  - Acceptance: Ready-to-implement, ready-to-validate, ready-to-close, and
    ready-to-archive semantics are documented or exposed in runtime output with
    blockers/evidence targets.
  - Depends on: T002
  - Evidence:

## Phase 3: Routing and Packaging Hygiene

- [ ] T006 Route deferred comparison ideas to backlog or roadmap.
  - Requirements: Requirement 5
  - Acceptance: Deferred ideas are represented in durable planning docs with
    rationale; rejected ideas are recorded in comparison artifact or decisions.
  - Depends on: T001, T002
  - Evidence:

- [ ] T007 Mirror accepted skill/runtime/prompt changes into the bundled plugin.
  - Requirements: Requirement 3, Requirement 4, Requirement 5
  - Acceptance: `plugins/spec-lifecycle-manager/` remains self-contained and
    validates after any top-level skill/runtime changes.
  - Depends on: T003, T004, T005
  - Evidence:

## Phase 4: Verification and Closure

- [ ] T008 Run validation and record evidence.
  - Requirements: Requirement 1, Requirement 2, Requirement 3, Requirement 4, Requirement 5
  - Acceptance: Required validation commands pass or residual risks are
    documented in `verification.md`.
  - Depends on: T006, T007
  - Evidence:

- [ ] T009 Promote durable docs and close package.
  - Requirements: Requirement 5
  - Acceptance: Accepted behavior is promoted to durable docs; closure log and
    archive index are ready for package removal.
  - Depends on: T008
  - Evidence:
