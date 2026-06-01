---
title: Spec lifecycle manager skill validation evidence
doc_type: review
status: archived
owner: platform
last_reviewed: 2026-06-01
---

# Validation Evidence

## Summary

Phase 4 validation used sub-agents to apply the installed
`spec-lifecycle-manager` skill to the two identified target repositories and to
synthetic lifecycle scenarios in this repository. The skill is available in this
session as `spec-lifecycle-manager`, and sub-agents received it as an attached
skill item during validation.

Validation result: pass with follow-up wording improvements. The skill produced
useful guidance for active spec detection, reconciliation, coherent task
selection, durable documentation promotion, expert review roles, and closure
blockers. The validation did not modify either target repository.

## Validation Targets

| Target | Result | Evidence source |
| --- | --- | --- |
| Mature documentation repository | Pass with notes | Read-only sub-agent validation against mature docs and multiple active specs. |
| Smaller agent-runtime repository | Pass with notes | Read-only sub-agent validation against a single active runtime spec. |
| Local synthetic checks | Pass with notes | Read-only sub-agent validation against the installed skill, references, and this spec package. |

## Mature Documentation Repository Evidence

The validation found multiple candidate spec packages under `docs/specs/`.
`docs/README.md` identifies active implementation or stabilization packages,
while `docs/specs/implementation-sequencing.md` expands the active platform set
and gives dependency order. The skill correctly needs to avoid choosing the
highest numbered package by default; it should select by user goal or by the
first blocking slice in sequencing guidance.

Repository-specific instructions and durable docs were identified:

- `AGENTS.md` defines repo scripts, validation expectations, containerized
  deployment checks, and configuration-family conventions.
- `docs/README.md` maps durable doc classes including architecture,
  requirements, design, API contracts, data-flow docs, runbooks, ADRs,
  references, backlog, and reviews.
- `docs/templates/README.md` reinforces that current-state content belongs in
  durable docs rather than active specs.

Reconciliation was required because the repository has multiple active specs,
checked and unchecked tasks, cross-spec dependencies, and frontmatter/status
signals that do not fully describe implementation state.

Sample drift classifications from the validation:

- `implemented but unverified`: spec `044` has many completed phases, but a
  manual backfill lock-conflict verification task remains open.
- `code incomplete`: spec `044` still has open dispatch/runtime execution work.
- `decision unresolved`: spec `042` has source-owner and business semantics
  decisions still open.
- `intentionally deferred`: spec `043` defers production coverage audit until
  deployment, replay, or backfill creates new curated outputs.
- `durable docs stale`: completed spec content must be promoted before closure;
  the repository already documents this pattern for closed packages.

The next coherent slice identified by the validation was spec `044` Phase 5,
especially dispatching queued refresh requests through the correct runtime and
adding PostgreSQL, failure, and correlation tests. Durable promotion targets
included analytics ETL configuration docs, curated-to-processed data-flow docs,
processed refresh docs, analytics processing placement references, and
deployment/runbook docs.

Relevant expert review roles were data and integration architecture, API and
contract, operations/SRE, security/compliance, QA/test strategy, documentation
architecture, and software architecture. Repository-specific stakeholder labels
also exist in its review matrix, but the skill's generic role-based routing
still mapped cleanly.

Closure blockers were correctly identified for specs `044`, `023`, and `038`:
open implementation tasks, unverified runtime behavior, incomplete durable docs,
and active index/sequencing references.

## Smaller Agent-Runtime Repository Evidence

The validation found a single active package:
`docs/specs/001-agent-ide-runtime/`, with the expected `spec.md`, `plan.md`,
`design.md`, `research.md`, `quickstart.md`, and `tasks.md` artifacts.

Repository-specific instructions and durable docs were identified:

- `AGENTS.md` defines TypeScript source and Vitest test locations, current docs
  under `docs/design/`, MVP spec package guidance, `.cache/` exclusion, and
  rules for preserving draft, accepted, and open-question distinctions.
- `docs/reference/documentation-map.md` maps durable docs.
- Durable promotion targets include runtime requirements, system architecture,
  runtime contracts, MVP proof matrix, MCP surface design, runtime operations
  design, observability/debugging design, coding-agent integration design, and
  native dependency runbooks.

Reconciliation was required because the active package is partially completed
and some task state appears stale relative to code and tests.

Sample drift classifications from the validation:

- `spec stale`: unchecked context-tool tasks appear implemented in
  `src/application/use-cases/get-task-context.ts` and covered by MCP tests.
- `implemented but unverified`: runtime operation pieces have tests, but broader
  warm-up, degraded, and concurrency tasks remain unchecked.
- `code incomplete`: several `T204` runtime operations tasks remain open.
- `durable docs stale`: runtime requirements evidence still has placeholder
  sections despite implementation and tests.
- `intentionally deferred`: broader post-MVP semantic/runtime features are
  explicitly deferred in the task list.

The validation recommended a reconciliation/verification slice first: verify
the apparently implemented context tasks against code and tests, then update
task state if validation passes. The next implementation slice after that is
the `T204` runtime operations proof work because it gates MVP closure.

Relevant expert review roles were developer process expert, software architect,
QA/test strategy expert, operations/SRE expert, documentation architect, and API
and contract expert.

Closure blockers were correctly identified: many unchecked tasks remain,
durable requirements evidence is incomplete, and proof matrix acceptance gates
still need fixture-backed evidence.

## Fresh Small Spec Check

Result: pass with notes.

The skill explicitly allows fresh, small, low-risk work to keep reconciliation
brief and proceed. This satisfies the requirement to avoid unnecessary ceremony.
The validation noted one improvement: fresh spec creation guidance is implied by
the skill metadata but could be made more explicit in `SKILL.md`.

## Partially Completed Stale Spec Check

Result: pass.

The skill requires reconciliation when resuming existing or partially completed
specs, when tasks are already checked, when evidence is old or partial, when
code or docs changed outside the task list, or when durable docs disagree with
the spec. It also provides the required drift classifications:

- `spec stale`
- `code incomplete`
- `durable docs stale`
- `decision unresolved`
- `implemented but unverified`
- `intentionally deferred`

## Durable Doc Routing And Expert Review Check

Result: pass.

The skill routes accepted spec content into durable docs before closure and
links to `references/document-routing-and-expert-review.md` for detailed routing
and review roles. The reference covers durable doc classes, spec-to-doc routing,
expert roles, document-class review matrices, whole-package review, and review
evidence fields.

## Skill Availability Check

Result: pass.

The installed package exists at:

```text
~/.codex/skills/spec-lifecycle-manager/
```

`SKILL.md` is readable, the skill is listed in this session, and the installed
package contains `agents/openai.yaml`. Sub-agents used the skill through
attached skill items during the Phase 4 validation runs. The canonical source is
now tracked in this repository at `skills/spec-lifecycle-manager/`; the
`~/.codex` copy is an installed artifact.

## Residual Risks And Follow-Up

Validation found useful wording improvements, but no blocker to local use:

- Add explicit handling for multiple active specs: read `docs/README.md` and
  sequencing docs, then ask the user to choose or select the first blocking
  slice from sequencing guidance.
- Add guidance not to trust frontmatter status alone; reconcile status against
  docs indexes, sequencing docs, and task state.
- Add explicit guidance to compare checked and unchecked tasks against actual
  code/tests before choosing the next slice.
- Add a validation output field for task-state stale candidates.
- Add guidance to inspect durable docs' evidence sections, not only prose.
- Add a reminder that closure may require removing or demoting active-index
  references to completed specs.
- Make fresh-spec creation guidance explicit and state that a one- or two-line
  reconciliation is enough for fresh, small, low-risk work with no conflicting
  evidence.

Follow-up status: implemented in the installed skill after Phase 4 closure.
The tracked and installed `SKILL.md` copies now cover multiple active specs,
frontmatter/status reconciliation, task-state stale candidates, durable-doc
evidence sections, fresh-spec lightweight creation, and active-index cleanup.
The reusable skill package intentionally does not include the implementation
validation target repositories; those remain only in this archived validation
evidence.

## Closure Recommendation

Phase 4 is complete. The skill is validated enough for local use, with
non-blocking wording improvements recorded above. This implementation spec can
be retained with `status: archived` as validation and decision history; durable
current-state guidance now lives in `docs/design/`, `docs/reference/`,
`docs/README.md`, and the tracked skill source under
`skills/spec-lifecycle-manager/`.
