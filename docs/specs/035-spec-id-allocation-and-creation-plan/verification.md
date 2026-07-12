---
title: Spec ID allocation and creation plan verification
doc_type: spec
artifact_type: verification
status: active
lifecycle_stage: tasks
owner: platform
last_reviewed: 2026-07-12
---

# Verification Plan

## Numbering Inventory

- **V001:** an empty selected scope returns provisional `000`.
- **V002:** active package prefixes participate in the maximum.
- **V003:** removed archive-index IDs participate in the maximum.
- **V004:** closure-log-only historical IDs participate with reduced confidence.
- **V005:** retained archive paths participate in the selected scope.
- **V006:** explicit legacy upper bounds participate without gap reuse.
- **V007:** duplicate prefixes are deterministic diagnostics.
- **V008:** malformed IDs remain visible but do not become valid prefixes.
- **V009:** missing selected-root history reduces confidence.
- **V010:** ambiguous history ownership fails closed.
- **V011:** one docs root never borrows another root's evidence.
- **V012:** equivalent evidence ordering produces identical inventory results.

## Creation Planning And Safety

- **V013:** valid ASCII lower-kebab slugs produce padded IDs and repo-relative paths.
- **V014:** separators, dot segments, controls, empty segments, repeated or edge
  hyphens, and non-ASCII slugs are rejected before path construction.
- **V015:** normalized proposed paths remain beneath the selected specs root.
- **V016:** an existing proposed path reports collision and a fresh proposal.
- **V017:** an already-used numeric prefix cannot be proposed.
- **V018:** selected-root templates outrank repository-root and skill fallback.
- **V019:** artifact inventory and required user values are deterministic.
- **V020:** the plan is labeled provisional and not reserved.
- **V021:** repeated planning does not mutate any file.
- **V022:** unchanged evidence confirms an expected fingerprint.
- **V023:** changed numbering evidence returns stale with refreshed arguments.
- **V024:** changed template authority invalidates the fingerprint.
- **V025:** changed scope, slug, or proposed-path state invalidates the fingerprint.
- **V026:** timestamps, absolute paths, wording, and invocation metadata do not
  affect evidence identity or leak into normal output.

## Integration And Adapters

- **V027:** bootstrap uses the shared allocator and preserves empty-scope `000`.
- **V028:** established repositories can plan without blank classification.
- **V029:** scan adds the next provisional number without changing existing fields.
- **V030:** no-active context adds the next number and creation-plan action.
- **V031:** ambiguous/unusable allocation does not advertise unsafe creation.
- **V032:** orientation fields match standalone inventory decisions.
- **V033-V036:** retained CLI argument, output, provenance, privacy, and error
  behavior pass.
- **V037-V044:** MCP discovery/schema validation, compact/stale/collision shapes,
  provenance, privacy, and MCP/CLI parity pass.
- **V045-V048:** source/Codex/Claude parity, package contract, sync guard, npm
  dry-pack, and full repository validation pass.
- **V049-V052:** durable design/reference/skill guidance, B061, roadmap, and
  closure evidence reconcile.

## Quality Gates

- Focused inventory fixtures pass before creation planning starts.
- Focused path/fingerprint/read-only fixtures pass before adapter work.
- Existing scan, bootstrap, no-active, template, and archive tests remain green.
- MCP and CLI decisions match after transport metadata removal.
- Full Python and Node suites, package contract, bundle parity, npm dry-pack,
  prompt/archive validation, and `git diff --check` pass before promotion.

## Evidence Log

- **2026-07-12 — T001:** Added caller-agnostic, docs-root-scoped numbering
  inventory with deterministic active/archive/closure/retained/legacy evidence,
  monotonic allocation, confidence, and malformed/duplicate/missing/ambiguous
  history diagnostics. V001-V012 pass with six focused fixtures; the complete
  Python suite passes 284 tests, source/Codex/Claude parity is synchronized,
  and `git diff --check` passes.
- **2026-07-12 — T002:** Added strict slug validation and preview-only creation
  planning with safe repo-relative paths, deterministic template/artifact
  planning, required values, explicit provisional/non-reservation semantics,
  stale fingerprints, collision diagnostics, and fresh fallback proposals.
  V013-V026 pass with 11 focused fixtures; the complete Python suite passes 289
  tests, bundle parity is synchronized, and `git diff --check` passes.
- Pending implementation evidence for T003-T007.

## Residual Risks

- Historical gaps can lower confidence but cannot be reconstructed reliably
  without explicit repository evidence.
- V1 remains advisory and read-only; concurrent safety belongs to a separately
  specified atomic writer.
