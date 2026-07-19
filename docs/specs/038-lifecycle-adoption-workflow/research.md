---
title: Lifecycle adoption workflow research
doc_type: spec
artifact_type: research
status: draft
owner: platform
last_reviewed: 2026-07-18
---

# Lifecycle Adoption Workflow Research

## Scope

This artifact records the product findings from a bounded external Chat
Analyser study of Codex and Claude Code use of `spec-lifecycle-manager`. It is
decision context for lifecycle improvements, not an analysis specification. It
does not judge task correctness, tool usefulness, independent preference, or
causal benefit.

## Evidence Boundary

The 2026-07-18 study used a bounded verified cohort after larger builds exceeded
available resources. It observed genuine structured lifecycle-manager use and
a provisional concentration on validation and gating operations. The external
producer later found a normalized capability-attribution defect, so exact
operation distributions remain provisional or unavailable. The producer's
scope, evidence identity, and limitations must accompany any promoted finding.

The detailed session-import, native extraction, invocation-origin,
native-to-normalized reconciliation, resource-bound, and report-confidence
contracts have been routed to the Chat Analyser project backlog. This spec does
not reproduce those contracts or attempt to repair the external dataset.

## External Report Receipt

| Field | Reviewed value |
|-------|----------------|
| Producer | Chat Analyser project |
| Analysis date | 2026-07-18 |
| Evidence identity | Producer Git revision `9db3f5f7cbdbfd01ecd1a6d23d50cb8714339ea5`, especially `docs/backlog/analysis-product.md` lines introduced by that revision |
| Bounded scope | A stratified 22-history/174 MB request completed; a 242-source/approximately 1.83 GB request ended with exit 137 and a reduced 69-source request did not complete within more than 15 minutes |
| Qualified conclusion | Genuine structured `spec-lifecycle-manager` use occurred in Codex and Claude Code histories; the observed operation mix suggested lifecycle workflow improvements |
| Count status | Exact affected operation distributions are **unavailable**, not zero: Claude normalized capability attribution was shown to misattribute operations, and unexplained native-to-normalized mismatches fail the aggregate closed |
| Known limitations | The completed cohort was bounded and stratified; invocation origin was not fully classified; incomplete larger runs do not contribute counts; the evidence does not establish necessity, preference, correctness, usefulness, outcome success, or causal improvement |
| Privacy boundary | Receipt retains metadata, bounds, status, revision, and conclusions only; it imports no semantic session content or private history |

Review disposition: accepted as qualified observational adoption evidence for
Requirement 1 and CP-004. It supports the product response in this spec but not
an exact frequency baseline or an effectiveness claim. Analysis extraction,
attribution correction, reconciliation, and report generation remain owned by
the Chat Analyser project.

## Review Findings

- Both Codex and Claude Code emitted genuine structured lifecycle-manager calls
  in the reviewed cohort.
- Provisional observations were weighted toward lint, readiness, audit, and
  closure surfaces, while implementation-start, evidence-quality, and durable
  promotion surfaces appeared less prominent.
- Direct lifecycle CLI use and repeated full skill reads suggested an
  opportunity for a clearer composed entrypoint and more compact capability
  guidance, but the study does not prove why an agent chose either behavior.
- Ordinary post-write hooks do not directly execute MCP
  `lint_spec_package`; they use narrower runtime paths.
- Advisory hook output can nevertheless recommend `lint_spec_package`.
  Immediate Claude sequences showed that such advice can precede an agent lint
  call, so a raw call count cannot be treated as independent agent preference.
- The normalized attribution defect makes exact operation-name aggregates
  unsuitable as a lifecycle-manager acceptance gate until the owning analyser
  reports a qualified result.

## Product Implications

1. Compose existing preflight, task context, traceability, readiness, and
   validation surfaces into one read-only implementation-start workflow.
2. Strengthen next-action routing from implementation through evidence quality
   and durable promotion before closure.
3. Keep MCP primary and CLI explicitly labelled for hooks, CI, validation,
   debugging, and recovery.
4. Reduce skill-entrypoint loading while retaining mandatory governance.
5. Remove full-package lint execution and advice from ordinary spec, task,
   template, and verification writes; retain package lint only at explicit
   resume, closure, or direct validation boundaries.
6. Consume only a reviewed, qualified external dogfood finding; do not import
   the analyser's method into the lifecycle runtime.

## External Ownership Routing

| Analysis concern | Owning destination |
|------------------|--------------------|
| Capability identity and operation attribution defect | Chat Analyser backlog |
| Evidence-backed invocation-origin and hook-correlation classification | Chat Analyser backlog |
| Bounded native operation distribution, reconciliation, and exact/provisional/unavailable reporting | Chat Analyser backlog |
| Lifecycle response to the qualified findings | Spec 038 |

## Options Considered

| Option | Summary | Pros | Cons | Decision |
|--------|---------|------|------|----------|
| Documentation only | Update guidance without changing workflow surfaces. | Small and low risk. | Existing guidance was still fragmented and hook advice remained too broad. | Reject as insufficient. |
| New lifecycle engine | Add one stateful workflow that replaces existing tools. | One apparent entrypoint. | Duplicates authority and increases compatibility risk. | Reject. |
| Composed start prompt and stronger next actions | Compose current authoritative tools and improve state-specific routing. | Low duplication, MCP-first, testable, client-neutral. | Still relies on clients following returned actions. | Adopt. |
| State-specific advisory hook guidance | Keep narrow checks and recommend full lint only for an explicit lifecycle need. | Reduces redundant validation advice without mutation or blocking. | Cannot guarantee how an agent responds. | Adopt. |
| Automatic blocking hooks | Force context and promotion calls. | Strong enforcement. | Conflicts with advisory-hook policy and may add noise. | Reject for this spec. |
| New telemetry system | Emit and aggregate all lifecycle events. | Better longitudinal measurement. | Duplicates B025 and expands privacy/operations scope. | Defer to B025. |

## Confidence And Unknowns

- **Confidence:** high that genuine structured use occurred and that ordinary
  hooks do not directly run MCP lint; high that hook advice can recommend lint;
  lower for exact operation distributions or causal interpretation.
- **Known unknowns:** outcome success, semantic correctness, whether each call
  was necessary, why an agent selected a surface, and the effect of
  client/plugin versions on discovery.
- **Assumptions:** the external producer owns the correctness and confidence of
  its report; this repository may preserve qualifications but must not silently
  strengthen them.
- **Evidence gaps:** no post-change report and no exact affected operation
  distribution from the current external evidence.

## Recommendation

Implement the composed start workflow, stronger evidence/promotion routing,
MCP-first presentation, compact skill entrypoint, and the explicit
ordinary-write versus lifecycle-boundary hook contract. Evaluate the result
with a reviewed external report whose
qualifications are preserved. Keep phase-completion mutation, analysis
methodology and repair, and telemetry outside this spec.

## Related Artifacts

- Requirements: `requirements.md`
- Design: `design.md`
- Tasks: `tasks.md`
- Verification: `verification.md`
