---
title: Coding agent operating model
doc_type: design
status: active
owner: platform
last_reviewed: 2026-06-06
---

# Coding Agent Operating Model

## Purpose

Define the durable operating model for coding-agent work in this repository.
The model keeps the classic software quality spine intact while scaling
ceremony to risk and using agents where they improve speed, coverage, or
review quality.

## Core Model

Coding agents change cadence, not accountability. The developer operator
remains responsible for intent, constraints, acceptance, tradeoffs, and final
judgment. Agents provide fast exploration, drafting, implementation,
verification, and review support.

The quality spine is:

```text
intent -> baseline -> plan/spec -> implementation slice -> verification -> review -> durable docs -> close -> feedback
```

Use the shortest version of that spine that fits the risk.

## Workflow Levels

| Level | Use when | Required evidence |
|-------|----------|-------------------|
| Direct patch | Low-risk, local, easy-to-verify changes. | Intent, changed files, local check or reason no check applies. |
| Lightweight spec | Small behavior changes, bug fixes, or changes needing durable baseline. | Durable source baseline, focused tasks, validation evidence. |
| Full spec | Cross-module, data, integration, user-facing, or operational changes. | Requirements, design, tasks, traceability where useful, verification, durable promotion. |
| Governance gate | Security, production data, contracts, migrations, policy conflicts. | Explicit human decision before implementation. |

## Agent Roles

| Role | Responsibility |
|------|----------------|
| Lead agent | Maintains context, reconciles specs, chooses workflow level, and owns final response. |
| Explore agent | Performs bounded read-only investigation. |
| Worker agent | Implements a clearly scoped, non-overlapping slice. |
| Review agent | Reviews correctness, architecture, tests, docs, or closure risk. |
| Verification agent | Designs or runs validation and records evidence. |
| Developer operator | Sets intent, accepts tradeoffs, and makes final decisions. |

## Decision Gates

Use explicit decision gates when work affects:

- security, privacy, or credentials;
- production data, migrations, or irreversible operations;
- public API, contracts, or schemas;
- cross-module architecture or integration boundaries;
- governance, constitution, lifecycle policy, hooks, or MCP surfaces.

If the active spec conflicts with governance or durable docs, stop for a
decision unless the user explicitly asks to update the higher-priority source.

## Evidence Rules

Completed work should have evidence close to the task or in `verification.md`.
Evidence can be:

- command output summary;
- tests, lint, typecheck, or build result;
- manual verification note;
- review finding disposition;
- screenshot, trace, or log where relevant;
- explicit residual risk when validation could not run.

Agents should not mark work complete based only on assertion.

## Parallelism Rules

Use parallel agents for bounded read-only work, independent review, or
non-overlapping implementation slices. Do not split broad ambiguous work across
multiple agents without explicit ownership boundaries.

Conflicting subagent findings must be reconciled before implementation or
closure proceeds.

## Metrics

Keep metrics lightweight. Useful local measures are:

| Metric | Why it matters |
|--------|----------------|
| Cycle time | Shows whether agent assistance speeds the task class. |
| Rework | Shows whether agent output creates correction overhead. |
| Evidence quality | Shows whether review starts from useful proof. |
| Review findings | Shows where agents miss risks. |
| Hook noise | Shows whether automation adds friction. |
| Closure readiness | Shows whether specs promote durable docs and evidence cleanly. |

If a metric is not being used to change behavior, stop collecting it.

## Durable Documentation Boundary

Specs are temporary delivery scaffolding. Durable docs describe the current
system, current workflow, and accepted operating decisions. When a spec
stabilizes behavior that should outlive implementation, promote that behavior
into durable docs before closure.

For broad or durable-doc-impacting implementation work, agents should use the
active spec's declared canonical context as the first working-context surface.
That context may import, adapt, supersede, or classify durable docs for the
current slice. It narrows implementation context, but it does not override
system, developer, or user instructions, `AGENTS.md`, governance, policy,
security, generated/source-code contracts, tests, or live evidence. Conflicting
unlisted durable docs should be treated as background or drift evidence until
reconciled.

## Dogfood Decision

Recent lifecycle work validated this model across:

- low-risk documentation and metadata cleanup;
- medium-risk runtime and MCP scan behavior changes;
- higher-risk host-level Codex hook installation;
- spec closure and retained-history evidence updates.

The model is kept as durable design guidance. Selected rules have been adopted
as governance where they need to constrain future agents; the remaining
workflow mechanics stay as operating guidance until a later governance decision
promotes them.

## Governance Adoption

Selected operating-model rules are now governance in
`docs/governance/constitution.md`:

- agents must use full spec context before implementation;
- risky work requires explicit decision-gate handling;
- parallel agent work must be bounded and conflicts reconciled;
- completed work needs evidence and durable promotion before closure.

Workflow levels, agent-role descriptions, metrics, and dogfood examples remain
design guidance. They inform how agents work, but they are not mandatory policy
unless the constitution states the rule directly.
