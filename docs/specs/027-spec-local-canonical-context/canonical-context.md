---
title: Spec-local canonical context canonical context
doc_type: spec
artifact_type: canonical-context
status: active
owner: platform
last_reviewed: 2026-07-02
---

# Canonical Context

## Purpose

This package changes how lifecycle agents decide documentation authority during
implementation. It needs explicit working-context authority because the change
touches durable lifecycle docs, skill instructions, fallback templates, MCP
prompt definitions, runtime diagnostics, tests, and migration guidance.

## Authority Hierarchy

Always-canonical external sources outrank this package: system, developer, and
user instructions; applicable `AGENTS.md`; governance; security and privacy
policy; generated contracts; source-code contracts; tests; and live/system
evidence. This package is canonical only for the active implementation slice
that adds spec-local canonical context behavior.

## Always-Canonical External Sources

| Source | Authority reason | Handling |
|--------|------------------|----------|
| `AGENTS.md` | Repository instructions | Read before changing lifecycle docs, skill files, scripts, templates, or tests. |
| `docs/governance/constitution.md` | Governance constraints | Stop for a decision if implementation would change governance authority. |
| `skills/spec-lifecycle-manager/scripts/spec_runtime.py` and tests | Runtime/source contract | Runtime behavior must match tests and deterministic CLI/MCP output. |
| Current system, developer, and user instructions | Session authority | Do not override with spec-local text. |

## Spec-Canonical Working Sources

| Source | Role | Scope | Notes |
|--------|------|-------|-------|
| `requirements.md` | accepted intent | Spec-local canonical context behavior | Defines required authority, template, prompt, and runtime outcomes. |
| `design.md` | implementation approach | Optional artifact plus advisory diagnostics | D001 and D002 resolutions are canonical for this slice. |
| `change-impact.md` | durable routing | Durable docs, skill, templates, prompts, runtime, and tests | Promotion targets must be updated before closure. |
| `tasks.md` | execution index | T001-T006 in this implementation slice | Do not implement from task text alone. |
| `traceability.md` | task context | Requirement/task/design/verification mapping | Update if task or artifact scope changes. |

## Imported Sources

| Spec path | Source path | Source revision or date | Status | Canonical scope | Promotion target |
|-----------|-------------|-------------------------|--------|-----------------|------------------|
| `canonical-context.md` | `docs/design/spec-lifecycle-management.md` | 2026-07-02 | adapted | Lifecycle model, artifact shape, context-budget guidance, task markers | `docs/design/spec-lifecycle-management.md` |
| `canonical-context.md` | `docs/design/coding-agent-operating-model.md` | 2026-07-02 | adapted | Agent working-context rule | `docs/design/coding-agent-operating-model.md` |
| `canonical-context.md` | `skills/spec-lifecycle-manager/SKILL.md` | 2026-07-02 | adapted | Agent-facing workflow and closure guidance | `skills/spec-lifecycle-manager/SKILL.md` |
| `canonical-context.md` | `skills/spec-lifecycle-manager/references/spec-package/` | 2026-07-02 | adapted | Fallback template shape and examples | `skills/spec-lifecycle-manager/references/spec-package/` |
| `canonical-context.md` | `skills/spec-lifecycle-manager/prompts/` | 2026-07-02 | adapted | Creation/resume/task-context prompt behavior | `skills/spec-lifecycle-manager/prompts/` |
| `canonical-context.md` | `skills/spec-lifecycle-manager/scripts/spec_runtime.py` | 2026-07-02 | adapted | Advisory diagnostics and import-plan payloads | `skills/spec-lifecycle-manager/scripts/spec_runtime.py` |

## Non-Canonical Background Sources

| Source | Reason non-canonical | Handling |
|--------|----------------------|----------|
| `docs/reference/kiro-compatibility-review.md` | Historical compatibility review with older marker examples | Use for history only; current marker semantics come from runtime, skill, and task template. |
| Earlier installed plugin cache under `~/.codex/plugins/cache/.../0.1.0` | Stale local install evidence | Ignore for source behavior after the 0.2.1 refresh. |
| Closed or archived specs | Historical delivery records | Do not use as current behavior unless explicitly auditing history. |

## Promotion Map

| Spec-local content | Durable destination or route | Required before closure |
|--------------------|------------------------------|-------------------------|
| Current task marker semantics | `docs/design/spec-lifecycle-management.md` | yes |
| Current task marker semantics compatibility note | `docs/reference/kiro-compatibility-review.md` | yes |
| Current task marker template guidance | `skills/spec-lifecycle-manager/references/spec-package/README.md` | yes |
| Spec-local canonical context model | `docs/design/spec-lifecycle-management.md` | yes |
| Spec-local canonical context operating rule | `docs/design/coding-agent-operating-model.md` | yes |
| Agent-facing workflow and closure rules | `skills/spec-lifecycle-manager/SKILL.md` | yes |
| Canonical context fallback template | `skills/spec-lifecycle-manager/references/spec-package/canonical-context.md` | yes |
| Canonical context template index guidance | `skills/spec-lifecycle-manager/references/spec-package/README.md` | yes |
| Creation/resume/task-context prompt behavior | `skills/spec-lifecycle-manager/prompts/` | yes |
| Runtime diagnostics, readiness, promotion, and closure behavior | `skills/spec-lifecycle-manager/scripts/spec_runtime.py` | yes |
| Runtime behavior reference | `docs/reference/spec-lifecycle-runtime.md` | yes |
| Runtime behavior tests | `tests/runtime/` | yes |
| Migration guidance | `skills/spec-lifecycle-manager/references/migration-guide.md` | yes |

## Related Artifacts

- Requirements: `requirements.md`
- Design: `design.md`
- Change impact: `change-impact.md`
- Tasks: `tasks.md`
- Traceability: `traceability.md`
- Verification: `verification.md`
