---
title: Durable document contract
doc_type: reference
status: active
owner: platform
last_reviewed: 2026-06-13
---

# Durable Document Contract

Durable docs are the persistent, reviewed, version-controlled source of truth
used by human developers and coding agents to understand, change, validate, and
operate a system.

Temporary specs coordinate active delivery. Durable docs describe accepted
current state. If a fact affects future implementation, validation, operation,
architecture, user-visible behavior, or change control, it belongs in a durable
document, code-derived contract, or explicitly tracked backlog or roadmap item.
It should not live only in an active spec.

## Shared Development Interface

A durable document should serve both humans and agents:

- Orientation:
  Humans need narrative overview, purpose, and tradeoffs. Agents need entry
  points, scope, stable IDs, and links.
- Decision-making:
  Humans need rationale and alternatives. Agents need constraints, invariants,
  and current-state labels.
- Implementation:
  Humans need design intent and examples. Agents need affected paths,
  contracts, commands, and patterns.
- Validation:
  Humans need test strategy and risk. Agents need exact validation commands and
  expected signals.
- Maintenance:
  Humans need ownership and history. Agents need review dates, supersession
  links, and status fields.
- Change control:
  Humans need review process and rationale. Agents need change rules and
  closure gates.

Narrative-only docs leave agents guessing. Structure-only docs lose human
judgment. Durable docs need both.

## Metadata

Use the repository's documented frontmatter first. When a repository does not
define a durable-doc template, prefer these fields for new durable docs:

```yaml
---
id: stable-doc-id
title: Document title
doc_type: requirements|architecture|design|api|data-flow|runbook|adr|reference|backlog|roadmap|review|governance|history
status: draft|active|code-derived|superseded|deprecated|archived
owner: team-or-person
audience:
  - human-developer
  - ai-developer
last_reviewed: YYYY-MM-DD
applies_to:
  - path/or/subsystem
source_of_truth: true
related_code: []
related_tests: []
related_specs: []
validation: []
supersedes: []
superseded_by: []
---
```

Minimum fallback metadata remains `title`, `doc_type`, `status`, `owner`, and
`last_reviewed`. Add richer fields when they improve routing, review, or agent
readiness; do not require every small document to carry empty metadata that
nobody maintains.

## Current-State Labels

Durable docs describe current accepted state by default. If they contain other
states, label them clearly:

- `current`: implemented and accepted now.
- `planned`: intended but not yet implemented.
- `deprecated`: still present but should not be extended.
- `removed`: no longer true.
- `experimental`: exists but is unstable.
- `decision`: rationale, not direct implementation instruction.
- `constraint`: must be preserved.
- `example`: illustrative only.

Roadmap, backlog, and ADR proposal language must not be presented as current
behavior unless the document explicitly says it is implemented and accepted.

## Baseline Sections

Use the repository's template first. When no template exists, a durable
current-state document should usually include:

- `Purpose`: what the document is for.
- `Current State`: what is true now.
- `Scope`: what this document covers.
- `Out of Scope`: what it does not cover.
- `Invariants`: rules that must remain true.
- `Behaviour / Design`: accepted behavior, design, or workflow.
- `Interfaces / Contracts`: APIs, schemas, commands, files, events, or
  protocol boundaries.
- `Operational Notes`: deployment, validation, recovery, or support guidance.
- `Validation`: commands, checks, expected signals, evidence, and residual risk.
- `Change Rules`: what must be updated when this area changes.
- `Related Documents`: requirements, ADRs, specs, runbooks, backlog, roadmap,
  code, tests, and contracts.

The most important agent-facing sections are `Current State`, `Invariants`,
`Interfaces / Contracts`, `Validation`, `Change Rules`, and `Related
Documents`.

## Durable Doc Readiness

Before implementing from a non-trivial spec, identify:

- authoritative durable docs for the area;
- whether each document is current enough to use;
- whether it describes current, planned, deprecated, removed, experimental, or
  example behavior;
- which code, tests, schemas, or generated contracts are more authoritative
  than prose;
- which durable docs must be updated if the change succeeds;
- which durable docs must not be changed.

Before closing a spec, verify:

- accepted behavior moved to durable docs or code-derived contracts;
- validation commands and evidence are linked;
- lasting decisions are captured in ADRs, governance, or durable design docs;
- deferred items are routed to backlog, roadmap, issue tracker, or follow-up
  spec;
- active docs no longer present the spec as current behavior.

## AGENTS.md Boundary

`AGENTS.md` is an agent entry point, not the durable source of truth. It should
point agents to authoritative docs and constraints, not duplicate architecture,
requirements, design, API contracts, or runbooks.

Use `AGENTS.md` for operational agent instructions such as build/test commands,
repository-specific workflow constraints, and where durable truth lives. Use
durable docs for system behavior, rationale, interfaces, operations, and
accepted change rules.

## Reviews And Specs

Review records are analysis snapshots. They can feed backlog, roadmap, specs,
durable docs, or human decisions, but they are not authoritative current
behavior by themselves.

Active specs are temporary delivery scaffolding. They may reference durable
sources and define intended deltas, but completed behavior must be promoted or
routed before closure.

## Anti-Patterns

- Retaining completed specs as current docs.
- Mixing roadmap intent with current behavior without labels.
- Duplicating requirements across several durable docs.
- Omitting validation or change rules for behavior that agents will edit.
- Leaving stale owner or review metadata.
- Treating generated docs as hand-authored source.
- Treating closed reviews as requirements.
- Expanding `AGENTS.md` into a duplicate architecture or design manual.
