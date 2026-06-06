---
title: Agent-backed lifecycle tools change impact
doc_type: spec
artifact_type: change-impact
status: draft
owner: platform
last_reviewed: 2026-06-06
---

# Change Impact

## Durable Source Mapping

| Source | Change Type | Proposed Impact | Promotion Target |
|--------|-------------|-----------------|------------------|
| `docs/reference/spec-lifecycle-runtime.md` | modify | Document agent-backed advisory tools, result schemas, disabled behavior, and MCP exposure. | Same file |
| `docs/design/spec-lifecycle-management.md` | modify | Add design-level explanation of low-cost agent offload boundaries if implementation changes lifecycle architecture. | Same file |
| `skills/spec-lifecycle-manager/SKILL.md` | modify | Add usage guidance for when to call agent-backed tools and how to treat results. | Same file |
| `AGENTS.md` | modify | Add repository-specific lifecycle preflight guidance only if the workflow changes for contributors. | Same file |
| `docs/backlog/README.md` | modify | Route deferred tool types or write-capable future work. | Same file |
| `docs/roadmap/README.md` | modify | Add adoption sequencing if multiple tool phases remain after the first implementation. | Same file |

## Proposed Changes

| Area | Change |
|------|--------|
| Runtime | Add packet building, agent-runner abstraction, result validation, and one initial command/tool. |
| MCP | Expose selected advisory agent-backed tool with read-only schema and clean unavailable behavior. |
| Tests | Cover schema validation, disabled runner behavior, removed spec handling, nested spec handling where relevant, and no mutation. |
| Prompts/Schemas | Add strict task instructions and result schema for the selected tool. |

## Promotion Targets

| Target | Promotion Trigger |
|--------|-------------------|
| `docs/reference/spec-lifecycle-runtime.md` | Runtime and MCP behavior implemented. |
| `docs/design/spec-lifecycle-management.md` | Architecture or lifecycle model changes accepted. |
| `skills/spec-lifecycle-manager/SKILL.md` | Agent-backed usage guidance accepted. |
| `docs/backlog/README.md` | Deferred tool types or future write-capable work identified. |
| `docs/roadmap/README.md` | Multi-phase adoption remains after first implementation. |

## Deferred Changes

- Write-capable agent-backed tools.
- Blocking hooks.
- Provider-specific model API integration unless selected explicitly during
  implementation.
- Persistent review-result archive beyond normal closure evidence.
