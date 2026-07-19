---
title: Lifecycle adoption workflow change impact
doc_type: spec
artifact_type: change-impact
status: draft
owner: platform
last_reviewed: 2026-07-19
---

# Lifecycle Adoption Workflow Change Impact

## Purpose

Map the proposed adoption workflow, routing, skill-entrypoint, advisory-hook,
and external dogfood-consumption changes to their durable authorities and
closure destinations.

## Durable Source Mapping

| Source | Current behavior relied on | Confidence | Notes |
|--------|----------------------------|------------|-------|
| `docs/design/spec-lifecycle-management.md` | Defines staged delivery, readiness, context budgets, promotion, and closure. | high | Composition must not replace these authorities. |
| `docs/reference/spec-lifecycle-runtime.md` | Defines MCP-first access and current runtime and hook tools. | high | CLI remains hook/validation/recovery infrastructure. |
| `docs/reference/spec-lifecycle-dogfood-evaluation.md` | Owns current dogfood conclusions and hook policy. | high | Receives qualified external evidence and delivered hook behavior. |
| `skills/spec-lifecycle-manager/SKILL.md` | Current full agent workflow instruction source. | high | Mandatory rules must remain authoritative. |
| `docs/backlog/README.md` | Owns deferred workflow-friction and telemetry items. | high | Avoid duplicating B025 and Spec 034. |

## Change Type

- **Primary type:** feature and documentation
- **Breaking change:** no
- **Durable docs required:** yes
- **External behavior affected:** yes, agent-facing prompt, next-action, and
  advisory-hook output

## Proposed Changes

| Change | Type | Source of truth | New durable destination | Promotion required |
|--------|------|-----------------|-------------------------|-------------------|
| Implementation-start composition | add | existing lifecycle source tools | runtime reference and lifecycle design | yes |
| Evidence/promotion next-action ordering | modify | shared lifecycle actions | runtime reference and lifecycle design | yes |
| MCP-primary recovery separation | clarify | MCP-first runtime contract | runtime reference and skill | yes |
| Capability readiness and bounded client observation | clarify | MCP initialization and capability contract | runtime reference | yes |
| Concise skill entrypoint | modify | source skill and references | source skill and plugin bundles | yes |
| Explicit ordinary-write versus lifecycle-boundary hook guidance | modify | hook runtime and lifecycle state | runtime reference and dogfood evaluation | yes, after T009 validation |
| Quiet cache-safe hook launcher and repository-local development | modify | packaged hooks, project config, and installer | install and runtime references | yes, after T013 validation |
| Qualified external adoption finding | consume | reviewed external report | dogfood evaluation | yes |

## Promotion Targets

| Spec content | Durable destination | Promotion status | Notes |
|--------------|---------------------|------------------|-------|
| Accepted workflow and action ordering | `docs/design/spec-lifecycle-management.md` | promoted | Current implementation-start composition and evidence-before-promotion ordering documented. |
| Runtime, prompt, hook, and capability contract | `docs/reference/spec-lifecycle-runtime.md` | promoted | MCP/CLI boundary, bounded client observation, narrow hooks, and quiet removed-cache behavior documented. |
| Development/package isolation | `docs/reference/spec-lifecycle-manager-mcp-install.md`, `README.md` | promoted | Source testing and packaged user deployment are separated. |
| Qualified external finding and hook outcome | `docs/reference/spec-lifecycle-dogfood-evaluation.md` | promoted | Producer scope, revision, incomplete bounds, unavailable counts, limitations, and ownership are explicit. |
| Delivery status and residuals | `docs/backlog/README.md`, `docs/roadmap/README.md` | promoted | B064 and R014 are done; residuals remain with B014, B015, B025, Spec 034, Chat Analyser, or the documented development launcher. |

## Unchanged Durable Areas

| Durable area | Reviewed source | Reason unchanged |
|--------------|-----------------|------------------|
| governance | `docs/governance/constitution.md` | Existing full-context, evidence, and promotion rules remain sufficient. |
| phase completion mutation | `docs/specs/034-phase-completion-helper/requirements.md` | Separate writer scope. |
| emitted telemetry | B025 in `docs/backlog/README.md` | Explicitly excluded. |
| hook blocking policy | `docs/reference/spec-lifecycle-dogfood-evaluation.md` | Hooks remain advisory-only. |
| Chat Analyser analysis methods | Chat Analyser project backlog | Import, extraction, origin classification, attribution, reconciliation, and report confidence remain external. |

## Resolved Decisions And Deferred Disposition

- DR-001 through DR-003 in `design.md` resolve prompt composition, measurable
  skill concision, and the ordinary-write versus explicit-boundary hook policy.
- B014 and B015 remain candidate owners for future bounded history discovery
  and workflow-friction reports. The qualified study consumed by this spec is
  one input and does not complete their broader contracts.
- B025 remains the sole owner of emitted telemetry and remote observability.
- Spec 034 remains the sole owner of phase-completion mutation.
- Chat Analyser owns session import, attribution, reconciliation, bounded
  analysis performance, and report-confidence behavior.
- Automatic project-scoped enablement of one packaged Codex plugin is not an
  available client surface; the checked-in source development launcher is the
  single operational destination for this limitation.

## Related Artifacts

- Requirements: `requirements.md`
- Research: `research.md`
- Design: `design.md`
- Tasks: `tasks.md`
- Verification: `verification.md`
