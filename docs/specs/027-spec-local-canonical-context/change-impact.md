---
title: Spec-local canonical context change impact
doc_type: spec
artifact_type: change-impact
status: active
owner: platform
last_reviewed: 2026-06-19
---

# Change Impact

## Purpose

Describe how the spec-local canonical context model changes lifecycle behavior
and which durable docs, templates, and runtime surfaces must be updated.

## Durable Source Mapping

| Source | Current behavior relied on | Confidence | Notes |
|--------|----------------------------|------------|-------|
| `docs/design/spec-lifecycle-management.md` | Active specs coordinate work and durable docs are promoted before closure. | high | Needs explicit active-slice canonical context rule. |
| `docs/design/coding-agent-operating-model.md` | Agents follow a quality spine and governance gates. | high | Needs a concise working-context authority rule. |
| `docs/governance/constitution.md` | Governance constraints outrank ordinary spec work. | high | Unchanged; must be listed as external authority. |
| `skills/spec-lifecycle-manager/SKILL.md` | Agent-facing lifecycle process and implementation guidance. | high | Primary guidance target. |
| `skills/spec-lifecycle-manager/references/spec-package/` | Fallback templates for package authoring. | high | Needs canonical context template support. |
| `skills/spec-lifecycle-manager/prompts/` | Prompt definitions shape how agents create, resume, reconcile, and validate specs. | high | Needs proactive canonical-context import or import-plan behavior. |
| `docs/reference/spec-lifecycle-runtime.md` | Documents runtime and MCP behavior. | high | Update if lint/readiness/closure diagnostics are added. |

## Change Type

- **Primary type:** clarification
- **Breaking change:** no
- **Durable docs required:** yes
- **External behavior affected:** no

## Proposed Changes

| Change | Type | Source of truth | New durable destination | Promotion required |
|--------|------|-----------------|-------------------------|-------------------|
| Define spec-local canonical context and authority hierarchy. | add | `docs/design/spec-lifecycle-management.md` | `docs/design/spec-lifecycle-management.md` | yes |
| Add coding-agent rule for canonical working context. | clarify | `docs/design/coding-agent-operating-model.md` | `docs/design/coding-agent-operating-model.md` | yes |
| Add skill workflow guidance for discovery, implementation, readiness, promotion, and closure. | modify | `skills/spec-lifecycle-manager/SKILL.md` | `skills/spec-lifecycle-manager/SKILL.md` | yes |
| Add fallback template support for `canonical-context.md` or equivalent embedded sections. | add | `skills/spec-lifecycle-manager/references/spec-package/` | `skills/spec-lifecycle-manager/references/spec-package/` | yes |
| Update spec creation and resume prompts so agents create canonical context or return an import plan without a second user prompt. | modify | `skills/spec-lifecycle-manager/prompts/` | `skills/spec-lifecycle-manager/prompts/` | yes |
| Add advisory runtime diagnostics for missing or incomplete canonical context where risk warrants it. | add | `skills/spec-lifecycle-manager/scripts/spec_runtime.py` | `docs/reference/spec-lifecycle-runtime.md` | yes if implemented |
| Add tests and fixtures for lint/readiness/closure behavior. | add | `tests/` | `tests/` | no durable-doc promotion beyond evidence |

## Promotion Targets

| Spec content | Durable destination | Promotion status | Notes |
|--------------|---------------------|------------------|-------|
| Authority hierarchy and caveats | `docs/design/spec-lifecycle-management.md` | pending | Must preserve governance and policy exceptions. |
| Agent operating rule | `docs/design/coding-agent-operating-model.md` | pending | Should be concise and point to lifecycle design. |
| Authoring and implementation workflow | `skills/spec-lifecycle-manager/SKILL.md` | pending | Agent-facing source. |
| Canonical context template | `skills/spec-lifecycle-manager/references/spec-package/canonical-context.md` or embedded sections | pending | Design decision D001. |
| Creation/resume prompt behavior | `skills/spec-lifecycle-manager/prompts/` | pending | Must create/propose context during spec creation and resumption. |
| Runtime diagnostic behavior | `docs/reference/spec-lifecycle-runtime.md` | pending | Required only after runtime changes land. |
| Migration guidance | `skills/spec-lifecycle-manager/references/migration-guide.md` | pending | Required if artifact rules or diagnostics change. |

## Unchanged Durable Areas

| Durable area | Reviewed source | Reason unchanged |
|--------------|-----------------|------------------|
| governance | `docs/governance/constitution.md` | This spec clarifies workflow and does not change governance authority. |
| archive history | `docs/history/spec-archive-index.md` | No closed-spec metadata changes until this spec closes. |
| backlog | `docs/backlog/README.md` | This spec is active work, not backlog routing yet. |

## Bug Fix Details

- **Observed behavior:** Agents may treat stale durable docs or legacy reviews
  as current authority while implementing an active spec.
- **Expected behavior:** Agents should use the active spec's declared canonical
  working context and treat unlisted conflicting docs as background or drift
  evidence.
- **Root cause evidence:** Current lifecycle guidance requires durable-source
  baselines but does not provide a strict enough working-context authority rule.
- **Regression risk:** Overly broad diagnostics could add ceremony to small
  specs; under-specified guidance could leave stale-doc behavior unchanged.
- **Durable doc update needed:** Yes.

## Open Questions

- D001: Separate `canonical-context.md` template vs embedded sections only.
- D002: Diagnostic severity for missing promotion target metadata before
  closure.

## Related Artifacts

- Requirements:
  `docs/specs/027-spec-local-canonical-context/requirements.md`
- Design: `docs/specs/027-spec-local-canonical-context/design.md`
- Tasks: `docs/specs/027-spec-local-canonical-context/tasks.md`
- Verification:
  `docs/specs/027-spec-local-canonical-context/verification.md`
