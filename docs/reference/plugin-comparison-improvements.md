---
title: Plugin comparison improvements
doc_type: reference
status: active
owner: platform
last_reviewed: 2026-06-09
---

# Plugin Comparison Improvements

## Purpose

Record the comparison inputs and adoption decisions that informed the
`spec-lifecycle-manager` improvement pass. External projects and IDE features
are advisory references only; repository governance, user instructions, Codex
plugin documentation, and the local durable-doc lifecycle remain authoritative.

## References

| Reference | Link | Relevant ideas | Routing |
|-----------|------|----------------|---------|
| Praxis | `https://github.com/ouonet/praxis` | Lightweight startup triage, compact skills, living-doc and staging-doc discipline, cross-harness packaging. | Accepted as bounded triage guidance; full staging model deferred. |
| Spec Driven | `https://github.com/Habib0x0/spec-driven-plugin` | Explicit command surface for status, validation, completion, and spec execution; EARS workflow; dependency/status concepts. | Accepted as MCP prompt aliases for status, validate, complete, and triage; autonomous execution loops rejected. |
| Superpowers | `https://github.com/obra/superpowers` | Gate discipline, verification before completion, focused skill triggers, review-oriented workflow. | Accepted as documented lifecycle gates and evidence expectations; full methodology import rejected. |
| Codex plugin build docs | `https://developers.openai.com/codex/plugins/build` | Plugin-root component packaging, bundled skills, MCP server files, hooks. | Accepted as packaging constraint; source and bundled skill copies must stay aligned. |
| Codex plugin overview docs | `https://developers.openai.com/codex/plugins` | Plugin installation and component behavior model. | Accepted as plugin behavior source of truth. |
| Kiro workflow notes | User-provided workflow preview, June 2026 | Checkpoint tasks, property-test tasks, spec phases, steering files, hooks, supervised/autopilot modes. | Accepted for checkpoint/property-test template guidance and backlog candidates; Kiro folder layout remains optional/deferred. |

## Accepted Changes

### Lifecycle Prompt Aliases

The plugin now ships MCP prompt definitions for common lifecycle intents:

- `lifecycle-status`: route "what next" and status requests to active preflight
  or no-active-spec context.
- `lifecycle-validate`: choose deterministic validation surfaces for active
  specs, prompts, archive index, and closure readiness.
- `lifecycle-complete`: guide durable promotion, closure readiness, validation,
  and package cleanup.
- `lifecycle-triage`: classify work before applying a heavier spec workflow.

These prompts are convenience entry points. They do not replace MCP tools or
the `spec-lifecycle-manager` skill.

### Lifecycle Triage

The accepted triage categories are:

| Category | Use When | Default Route |
|----------|----------|---------------|
| `trivial` | Typo, formatting, or narrow local edit with no lifecycle impact. | Edit directly and validate proportionately. |
| `small` | Bounded change with known files and low durable-doc impact. | Use lightweight context and focused validation; do not create a spec by default. |
| `spec-needed` | New behavior, cross-module work, unclear acceptance criteria, plugin packaging changes, or governance-sensitive work. | Create or continue an active spec. |
| `review` | User asks to inspect, compare, audit, or assess existing work. | Use read-only review stance and deterministic context. |
| `closure` | User asks to complete, close, archive, or reconcile lifecycle state. | Use closure readiness, durable promotion, and archive-index workflow. |

### Lifecycle Gates

The accepted gate names are documented guidance, not runtime-enforced fields in
this slice:

- `ready_to_implement`: requirements, design, traceability, open decisions, and
  validation expectations are coherent enough to start an implementation slice.
- `ready_to_validate`: implementation tasks have evidence and the validation
  plan identifies required commands or review methods.
- `ready_to_close`: tasks are complete with evidence, decisions are resolved or
  deferred, durable docs are promoted, and closure blockers are clear.
- `ready_to_archive`: closure log and archive index entries are prepared and
  the active package can be removed after a final spec commit.

Runtime fields for phase gates are deferred to backlog until a focused spec
defines compatibility, schema, and tests.

### Checkpoint and Property-Test Task Guidance

Kiro-style checkpoint tasks are accepted as evidence-bearing task-list entries
at phase boundaries, subsystem boundaries, validation pauses, and human decision
points. Correctness Properties in `requirements.md` should be carried into
property-test tasks where useful, using the target repository's accepted test
framework rather than forcing a new dependency.

## Deferred Candidates

Deferred ideas are tracked in `docs/backlog/README.md`:

- Workflow mode and approval policy: `B029`, `B030`.
- Phase gate runtime checks and semantic requirement lint: `B031`, `B032`.
- Steering context, hook inventory, and package manifest: `B033`, `B034`,
  `B035`.
- Kiro compatibility/import and hook-derived workflow checks: `B036` through
  `B041`.
- Agent Skills reference validator integration: `B028`.

## Rejected Scope

- Do not replace `docs/specs/[###-slug]/` with `.claude/specs/`,
  `.kiro/specs/`, or another tool-specific default in this repository.
- Do not import autonomous long-running execution loops into this skill.
- Do not adopt the full Praxis, Spec Driven, Superpowers, or Kiro methodology as
  this repository's lifecycle model.
- Do not add write-capable MCP tools without a separate spec that defines
  permissions, rollback, review, and evidence requirements.

## Validation

This comparison is satisfied when:

- Prompt definitions validate and are bundled into the plugin copy.
- Skill guidance documents lifecycle triage, lifecycle gates, checkpoint tasks,
  and property-test task expectations.
- Deferred and rejected ideas are visible in backlog, this reference, or closure
  evidence.
- Plugin validation, unit tests, lifecycle scan, prompt validation, archive
  index validation, and whitespace checks pass.
