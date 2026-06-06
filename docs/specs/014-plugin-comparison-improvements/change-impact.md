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
| `skills/spec-lifecycle-manager/SKILL.md` | Potentially add concise lifecycle triage and prompt alias guidance. | Reduce over-processing and improve user discoverability. | Skill guidance update. |
| `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/SKILL.md` | Mirror accepted skill changes into bundled plugin skill. | Keep plugin self-contained and current. | Plugin guidance update. |
| `skills/spec-lifecycle-manager/prompts/` | Potentially add status/validate/complete/triage prompt definitions. | Make common lifecycle intents explicit. | Prompt validation update. |
| `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/prompts/` | Mirror prompt definitions into bundled plugin. | Keep plugin self-contained. | Plugin prompt update. |
| `skills/spec-lifecycle-manager/scripts/spec_runtime.py` | Potentially add triage or lifecycle gate structured output. | Deterministic MCP-first context for agents. | Runtime and tests update. |
| `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/scripts/spec_runtime.py` | Mirror runtime changes into bundled plugin. | Keep plugin self-contained. | Plugin runtime update. |
| `docs/backlog/README.md` | Add deferred ideas that are not implemented in this spec. | Bound comparison scope. | Backlog update. |
| `docs/roadmap/README.md` | Add sequencing only if accepted work spans multiple specs. | Keep planning current. | Roadmap update if needed. |

## Proposed Changes

| Area | Proposed Change | Compatibility Notes |
|------|-----------------|---------------------|
| Comparison artifact | Create a durable reference document that analyzes Praxis, Spec Driven, Superpowers, and Codex plugin documentation. | Documentation-only and additive. |
| Lifecycle triage | Define a bounded triage flow for deciding whether external plugin ideas become accepted work, backlog entries, or rejected/no-action notes. | Can start as documentation and become runtime output only if D001 accepts that scope. |
| Prompt surface | Consider explicit lifecycle status, validate, complete, and triage prompt definitions. | Must remain MCP-first and preserve prompt validation behavior. |
| Completion gates | Consider lightweight completion gate markers inspired by external plugin review. | Must not block normal Codex use unless deliberately enabled in a later implementation. |
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
