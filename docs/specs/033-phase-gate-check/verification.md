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

No implementation evidence recorded yet.

## Quality Gates

- Focused phase/fingerprint tests pass before adapter work.
- Full Python and Node tests pass before promotion.
- Package contract, bundle parity, npm pack, and `git diff --check` pass.

## Residual Risks

- Legacy specs without fingerprints report review_required.
- Promotion inference intentionally prefers false-negative advancement over false
  closure readiness.
