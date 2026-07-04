---
title: Guided documentation wizard change impact
doc_type: spec
artifact_type: change-impact
status: active
owner: platform
last_reviewed: 2026-07-04
---

# Change Impact

## Purpose

Describe how the guided documentation wizard changes the skill's durable
behavior, runtime/prompt surface, and documentation workflow.

## Durable Source Mapping

| Source | Current behavior relied on | Confidence | Notes |
|--------|----------------------------|------------|-------|
| `docs/design/spec-lifecycle-management.md` | Staged flow, first-run guidance, bootstrap, stage readiness, and Agent Readiness Contract. | high | Add wizard behavior here when accepted. |
| `docs/reference/spec-lifecycle-runtime.md` | Runtime command and MCP tool inventory. | high | Add wizard command/tool/prompt after implementation. |
| `docs/reference/document-routing-and-expert-review-matrix.md` | Open decisions, expert review, feedback routing, and promotion targets. | high | Wizard should use this routing model. |
| `docs/reference/plugin-comparison-improvements.md` | Accepted prompt aliases and deferred external workflow ideas. | high | Wizard must stay consistent with rejected autonomous loops. |
| `docs/backlog/README.md` | Candidate items overlapping this work. | high | Update after implementation to mark covered/superseded scope. |
| `skills/spec-lifecycle-manager/SKILL.md` | Skill workflow guidance for staged artifacts, tasks, implementation, promotion, and closure. | high | Add user feedback and open-question guidance. |
| `skills/spec-lifecycle-manager/prompts/` | Current prompt definitions and validation contract. | high | Add or refine guided documentation prompt. |

## Change Type

- **Primary type:** feature
- **Breaking change:** no
- **Durable docs required:** yes
- **External behavior affected:** no

## Proposed Changes

| Change | Type | Source of truth | New durable destination | Promotion required |
|--------|------|-----------------|-------------------------|-------------------|
| Guided documentation wizard stage model | add | `docs/design/spec-lifecycle-management.md` | `docs/design/spec-lifecycle-management.md` | yes |
| Wizard runtime/MCP/prompt inventory | add | `docs/reference/spec-lifecycle-runtime.md` | `docs/reference/spec-lifecycle-runtime.md` | yes |
| User feedback and open-question handling guidance | clarify | `skills/spec-lifecycle-manager/SKILL.md` | `skills/spec-lifecycle-manager/SKILL.md` | yes |
| Prompt definition for guided documentation | add | `skills/spec-lifecycle-manager/prompts/` | `skills/spec-lifecycle-manager/prompts/` | yes |
| Candidate backlog overlap | clarify | `docs/backlog/README.md` | `docs/backlog/README.md` | yes |

## Promotion Targets

| Spec content | Durable destination | Promotion status | Notes |
|--------------|---------------------|------------------|-------|
| Wizard stage model and stage order | `docs/design/spec-lifecycle-management.md` | promoted | Prompt-only wizard behavior documented 2026-07-04. |
| Runtime/MCP/prompt surface | `docs/reference/spec-lifecycle-runtime.md` | promoted | `documentation-wizard` prompt documented 2026-07-04. |
| Open-question and feedback guidance | `skills/spec-lifecycle-manager/SKILL.md` | promoted | Open-question, feedback-disposition, and preview-plan guidance added 2026-07-04. |
| Prompt/tool contract | `skills/spec-lifecycle-manager/prompts/` and tests | promoted | Prompt and focused tests added 2026-07-04; `prompts` validation passed. |
| Backlog overlap | `docs/backlog/README.md` | promoted | B049 clarified as prompt-only v1 while active package remains open. |

## Unchanged Durable Areas

| Durable area | Reviewed source | Reason unchanged |
|--------------|-----------------|------------------|
| release workflow | `docs/specs/022-npm-publish-release-workflow/` | Guided documentation does not affect npm publish/release behavior. |
| developer CLI workflow | `docs/specs/025-dev-cli-workflow-tools/` | Wizard may be exposed through CLI later, but v1 should not depend on dev CLI implementation. |
| governance | `docs/governance/constitution.md` | Current preview-first and evidence rules already support this work. |
| install docs | `docs/reference/spec-lifecycle-manager-mcp-install.md` | Only needs updates if plugin packaging or install behavior changes. |

## Bug Fix Details

- **Observed behavior:** The skill can report lifecycle readiness, but does not
  guide a user step by step through documentation authoring, open questions, and
  feedback disposition.
- **Expected behavior:** A user can ask for guided documentation and receive the
  next bounded question, expected answer shape, artifact destination, and
  preview-first edit plan.
- **Root cause evidence:** Prior CLU-inspired staged onboarding work delivered
  runtime readiness surfaces but not a dedicated conversational wizard.
- **Regression risk:** Medium; prompt/runtime additions could duplicate existing
  flow if not kept as composition.
- **Durable doc update needed:** yes.

## Open Questions

- D001-D004 in [design.md](design.md#open-questions).

## Related Artifacts

- Requirements: [requirements.md](requirements.md)
- Design: [design.md](design.md)
- Tasks: [tasks.md](tasks.md)
- Verification: [verification.md](verification.md)
