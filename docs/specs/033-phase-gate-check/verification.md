---
title: Phase gate check verification
doc_type: spec
artifact_type: verification
status: active
lifecycle_stage: tasks
owner: platform
last_reviewed: 2026-07-12
---

# Verification Plan

## Phase And Composition

- **V001-V008:** one fixture for every public phase and unknown.
- **V009:** archived or ambiguous reference is not applicable/error, not closure.
- **V010:** unresolved decisions block only their relevant transition.
- **V011:** matching recorded upstream fingerprint reports current.
- **V012:** changed upstream content reports stale.
- **V013:** missing fingerprint reports review_required.
- **V014:** mtime-only changes do not report stale.
- **V015:** the gate never writes fingerprints or artifacts.

## Aggregate Contract

- **V016:** deterministic applicable-source ordering and maximum seven sources.
- **V017:** source severity/code/reference and proof meaning are preserved.
- **V018:** compact findings/actions respect 20/10 bounds.
- **V019:** mandatory blockers survive compaction and set limit_exceeded when needed.
- **V020:** full and closed section modes remain bounded.
- **V021:** equivalent evidence produces the same fingerprint.
- **V022:** changed decision evidence produces stale expansion with refreshed arguments.
- **V023:** timestamps, absolute paths, messages, and metadata do not affect evidence identity.

## Surfaces And Packaging

- **V024:** MCP input/output schemas publish detail and stale contracts.
- **V025:** CLI exposes equivalent detail arguments.
- **V026:** MCP and CLI lifecycle decisions match without transport metadata.
- **V027:** external invocation surface remains MCP/CLI through composition.
- **V028:** normal output contains no absolute host paths.
- **V029:** source and both bundle trees match.
- **V030:** package contract and sync guard pass.
- **V031:** full repository validation passes.
- **V032-V034:** durable docs, B031, roadmap, and closure evidence reconcile.

## Evidence Log

- **2026-07-12 — T001:** Added shared caller-agnostic phase inference and
  phase-applicable source summaries. V001-V010 pass across all public phases,
  missing and archived packages, open-decision blocker fixtures, deterministic ordering,
  severity/code/reference preservation, and lazy validation/promotion/closure
  checks. Full validation passed with 260 Python and 25 Node tests, package
  contract, bundle parity, npm pack, and diff checks.
- **2026-07-12 — T002:** Added normalized upstream artifact fingerprints and
  deterministic freshness states for design, tasks, traceability, and
  verification. V011-V015 pass: matching records are current, content changes
  are stale with reconciliation actions, absent/malformed records require
  review, mtime-only changes are ignored, and repeated calls do not mutate
  files. Full validation passed with 263 Python and 25 Node tests.
- **2026-07-12 — T003:** Added caller-agnostic compact, full, closed-section,
  and stale phase-gate rendering. V016-V023 pass for deterministic source and
  finding ordering, blocker-first bounds, overflow state, authority/proof
  preservation, cross-mode fingerprints, wording/mtime stability, freshness-
  driven stale expansion, and path/privacy exclusions. Full validation passed
  with 271 Python and 25 Node tests.
- **2026-07-12 — T004:** Added the MCP `phase_gate_check` and retained CLI
  `phase-gate-check` surfaces with closed input/output schemas and adapter-owned
  provenance. V024-V028 pass for all response modes, stale expansion, selector
  rejection, invocation metadata, exact MCP/CLI parity after metadata removal,
  established-schema compatibility, and absence of absolute host paths. Full
  validation passed with 275 Python and 25 Node tests.
- **2026-07-12 — T005:** Source, Codex, and Claude skill trees are synchronized;
  package contract, sync guard, npm pack, and diff checks pass after all phase-
  gate source and adapter slices. V029-V031 pass with the 275-Python/25-Node
  full repository validation.

## Quality Gates

- Focused phase/fingerprint tests pass before adapter work.
- Full Python and Node tests pass before promotion.
- Package contract, bundle parity, npm pack, and `git diff --check` pass.

## Residual Risks

- Legacy specs without fingerprints report review_required.
- Promotion inference intentionally prefers false-negative advancement over false
  closure readiness.
