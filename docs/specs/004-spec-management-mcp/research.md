---
title: Spec management MCP research
doc_type: spec
artifact_type: research
status: draft
owner: platform
last_reviewed: 2026-06-05
---

# Research

## Scope

This note records the working tradeoff between MCP prompts and Skills for spec
lifecycle management. It also identifies where MCP tools, resources, hooks, and
cheap-agent review packets fit.

## Sources

- MCP prompts specification:
  <https://modelcontextprotocol.io/specification/2024-11-05/server/prompts>
- MCP server concepts:
  <https://modelcontextprotocol.io/docs/learn/server-concepts>
- MCP agent skills guidance:
  <https://modelcontextprotocol.io/docs/develop/build-with-agent-skills>
- Local lifecycle design:
  [Spec lifecycle management](../../design/spec-lifecycle-management.md)
- Local governance:
  [Agent development lifecycle constitution](../../governance/constitution.md)

## Findings

### MCP prompts are user-invoked workflow templates

The MCP specification describes prompts as server-exposed templates that
clients can list and retrieve. They are intended to be user-controlled and
client-surfaced, commonly through slash commands or command palettes. Prompt
definitions can take arguments, return structured messages, and embed
server-managed resources.

Implication for this repository:

- MCP prompts are a good fit for explicit workflow entry points such as
  `reconcile-spec`, `choose-next-task`, `lint-spec`, and `close-spec`.
- MCP prompts should not be relied on as hidden standing policy because users
  explicitly invoke them and client support may vary.

### MCP tools and resources are better for enforceable behavior

MCP server concepts distinguish tools, resources, and prompts. Tools are
schema-defined callable operations, resources are read-oriented context, and
prompts are user-controlled templates.

Implication for this repository:

- Deterministic linting, task parsing, closure checks, and reconciliation
  classification should be MCP tools.
- Active spec inventories, parsed task graphs, template authority decisions,
  and governance summaries should be MCP resources.
- Prompts should orchestrate these resources and tools instead of duplicating
  their logic.

### Skills are better for durable agent behavior

MCP's agent skills guidance describes skills as portable instruction sets that
give coding assistants domain knowledge and workflow direction. The local
`spec-lifecycle-manager` skill already encodes the repository's lifecycle
rules, migration gates, template authority behavior, reconciliation behavior,
implementation slice selection, evidence rules, promotion, and closure.

Implication for this repository:

- The Skill should remain the authority for agent behavior.
- MCP prompts should instruct the agent to use the Skill.
- MCP tools should provide evidence the Skill can consume.

### Hooks are useful when narrow and deterministic

Hooks can catch common lifecycle mistakes at the point of change, but broad
semantic hooks would create friction and false confidence.

Implication for this repository:

- Good hook candidates: changed spec lint, completed task evidence check,
  closure readiness check, template drift warning.
- Good lifecycle candidates after the advisory phase: implementation task
  completion checks, verification evidence mapping, resume reconciliation, and
  closure gates.
- Good agent-oriented candidates after dogfooding: task-slice start checks,
  response completion checks, review-packet dispatch checks, and review-result
  disposition checks.
- Good governance and metrics candidates: phase-transition metrics, repeated
  waiver warnings, and governance-sensitive change checks.
- Poor hook candidates: broad semantic design approval, automatic durable-doc
  rewriting, autonomous task completion.

### Cheap-agent offload is useful only for bounded semantic review

Fast or cheap agents can help review requirements clarity, design traceability,
promotion targets, and closure risk. They should not independently change files
or mark tasks complete.

Implication for this repository:

- Generate review packets with explicit input artifacts, bounded questions,
  output schema, and stop conditions.
- Treat findings as advisory until reconciled by the lead agent or operator.

## Recommendation

Build a layered MCP runtime:

1. Keep `spec-lifecycle-manager` as the required standing workflow Skill.
2. Add deterministic MCP resources and tools first.
3. Add MCP prompts as discoverable user commands once the deterministic tools
   exist.
4. Add hooks that call the same deterministic linter/checker core.
5. Add cheap-agent review packets only after deterministic checks produce
   stable, low-noise outputs.
6. Promote hooks from advisory to blocking only for high-confidence lifecycle
   errors with low false-positive risk.

## Risks

| Risk | Mitigation |
| --- | --- |
| Prompt support varies by client. | Make prompts optional and keep Skill/tool workflows usable by natural language. |
| Prompt templates duplicate Skill policy and drift. | Keep prompts thin and route to Skill plus MCP tools/resources. |
| Linter becomes too rigid. | Support artifact-specific rules, severity profiles, and explicit waivers. |
| Cheap agents produce noisy findings. | Use bounded packets, schemas, and lead-agent reconciliation. |
| Hooks slow small edits. | Make most hooks advisory by default and block only clear lifecycle errors. |
| Hooks become policy before proving value. | Stage adoption, record metrics, and demote noisy hooks. |
| Tool output gets treated as semantic truth. | Separate observed facts, inferred diagnoses, and recommendations. |

## Open Questions

- Which MCP clients used locally expose prompts reliably?
- Should prompt definitions live beside code or under the skill references?
- What severity profile should block commits versus only warn?
- Should review packet execution be implemented now, or should the MCP server
  only generate packets for external dispatch?
