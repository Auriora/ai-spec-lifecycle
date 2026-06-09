---
title: Plugin comparison improvements change impact
doc_type: spec
artifact_type: change-impact
status: draft
owner: platform
last_reviewed: 2026-06-06
---

# Change Impact

## Durable Source Mapping

| Source | Proposed Change | Reason | Impact |
|--------|-----------------|--------|--------|
| `docs/reference/` | Add durable plugin comparison analysis document. | Preserve external references and accepted/deferred/rejected ideas. | New reference doc. |
| `skills/spec-lifecycle-manager/SKILL.md` | Add concise lifecycle triage and lifecycle gate guidance. | Reduce over-processing and improve user discoverability. | Skill guidance update. |
| `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/SKILL.md` | Mirror accepted skill changes into bundled plugin skill. | Keep plugin self-contained and current. | Plugin guidance update. |
| `skills/spec-lifecycle-manager/prompts/` | Add status/validate/complete/triage prompt definitions. | Make common lifecycle intents explicit. | Prompt validation update. |
| `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/prompts/` | Mirror prompt definitions into bundled plugin. | Keep plugin self-contained. | Plugin prompt update. |
| `skills/spec-lifecycle-manager/scripts/spec_runtime.py` | No runtime change in this spec. | Runtime gate fields and deterministic triage are deferred. | No implementation impact. |
| `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/scripts/spec_runtime.py` | No runtime change in this spec. | Bundled runtime remains unchanged. | No implementation impact. |
| `docs/backlog/README.md` | Add deferred ideas that are not implemented in this spec. | Bound comparison scope. | Backlog update completed before this closure slice. |
| `docs/roadmap/README.md` | Add sequencing only if accepted work spans multiple specs. | Keep planning current. | Roadmap update if needed. |

## Proposed Changes

| Area | Proposed Change | Compatibility Notes |
|------|-----------------|---------------------|
| Comparison artifact | Create a durable reference document that analyzes Praxis, Spec Driven, Superpowers, and Codex plugin documentation. | Documentation-only and additive. |
| Lifecycle triage | Define a bounded triage flow for deciding whether work is trivial, small, spec-needed, review, or closure. | Implemented as skill guidance and MCP prompt, not runtime classification. |
| Prompt surface | Add explicit lifecycle status, validate, complete, and triage prompt definitions. | MCP-first and prompt-validation compatible. |
| Completion gates | Add lightweight completion gate vocabulary inspired by external plugin review. | Documented guidance only; no blocking behavior. |
| Plugin bundle | Mirror accepted skill, prompt, and runtime changes into the self-contained plugin package. | Required to keep installed plugin behavior aligned with repository development sources. |

## Compatibility

- Runtime changes should be additive.
- Prompt changes must preserve `client_support_recovery`.
- Plugin validation must continue to pass.
- No new third-party dependencies are expected.

## Risks

| Risk | Mitigation |
|------|------------|
| External plugin ideas create scope creep. | Route each finding to accepted, deferred, rejected, or no-action. |
| Duplicating Superpowers/Praxis workflows makes this plugin too heavy. | Adopt only lifecycle-specific, bounded ideas. |
| Bundled plugin skill drifts from top-level development skill. | Include mirror/update task and validation. |
| Prompt aliases become vague or overlapping. | Keep aliases tied to existing MCP tools and validation tests. |

## Promotion Targets

- Durable comparison artifact under `docs/reference/`.
- Runtime reference updates in `docs/reference/spec-lifecycle-runtime.md` if
  runtime or prompt behavior changes.
- Backlog/roadmap updates for deferred ideas.
- No runtime reference update is required for new runtime fields because runtime
  behavior did not change.
