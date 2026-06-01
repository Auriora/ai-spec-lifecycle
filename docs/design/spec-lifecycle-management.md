---
title: Spec lifecycle management
doc_type: design
status: active
owner: platform
last_reviewed: 2026-06-01
---

# Spec Lifecycle Management

## Purpose

Define a reusable lifecycle for AI-assisted implementation specs. The lifecycle keeps requirements, specs, code, tests, configuration, and durable documentation consistent while work is in progress and prevents completed behavior from living only in temporary spec packages.

## Core Model

Specs are implementation scaffolding, not the final source of truth.

```text
durable docs -> active spec -> code/tests/config -> durable docs -> close spec
```

Durable docs describe accepted requirements, current architecture, current design, operator procedures, API contracts, data-flow behavior, reference material, and lasting decisions. Specs coordinate work while a change is being designed or implemented.

## Spec Package Shape

Use `docs/specs/[###-slug]/` for active specs. The numeric prefix gives stable ordering, and the slug gives a readable feature name.

Recommended package files:

- `spec.md`: problem, goals, requirements, acceptance criteria, user stories, and success criteria.
- `design.md`: planned design while implementation is active.
- `plan.md`: technical context, governance checks, phases, dependencies, risks, and validation strategy.
- `tasks.md`: executable task checklist grouped by independently testable slices.
- `research.md`: bounded analysis and decision inputs.
- `quickstart.md`: temporary validation or rollout notes that may later become runbooks or getting-started docs.
- `open-decisions.md`: unresolved decisions that block stable implementation.

## Durable Documentation Roles

| Durable doc area | Role |
| --- | --- |
| `docs/requirements/` | Current or accepted operating requirements. |
| `docs/architecture/` | Stable system shape, component boundaries, and cross-system flows. |
| `docs/design/` | Current technical design for implemented or accepted component behavior. |
| `docs/data-flow/` | Source-to-output lineage, transformation behavior, config routing, field dictionaries, and processed output behavior. |
| `docs/api/` | Canonical machine-readable API contracts and companion API guidance. |
| `docs/runbooks/` | Operational procedures, rollout, validation, recovery, replay, and support steps. |
| `docs/adr/` | Durable decisions and rejected alternatives that future maintainers should understand. |
| `docs/reference/` | Stable factual mappings, limits, schemas, taxonomies, generated summaries, and review matrices. |
| `docs/backlog/` | Cross-spec sequencing and work not ready for a focused implementation spec. |
| `docs/reviews/` | Analysis snapshots and evidence that may feed specs or durable docs. |
| `docs/specs/` | Temporary active delivery packages. |

Repositories may use different folder names. The lifecycle still applies: identify each repository's durable doc classes before implementing from a spec.

## Reconciliation

Before implementation, the agent should reconcile the active spec against durable docs, code, tests, and configuration when doing so adds clear value. Reconciliation is required when:

- resuming an existing or partially completed spec;
- the spec has checked tasks, old dates, or open decisions;
- implementation appears to have progressed outside the task list;
- durable docs disagree with the spec;
- the task touches API contracts, data-flow behavior, architecture, operations, security, or cross-module behavior.

The reconciliation should identify whether each mismatch means the spec is stale, code is incomplete, durable docs are stale, a decision is unresolved, or work is implemented but unverified.

## Implementation Rules

- Implement one coherent task slice at a time, usually one phase or checkpoint from `tasks.md`.
- Prefer independently testable user-story slices over broad task batches.
- Map tests and validation back to requirement IDs, acceptance criteria, success criteria, or task IDs where practical.
- Update task checkboxes only when the task's completion criteria are satisfied.
- Prefer passing tests before checking implementation tasks complete.
- If a task is not testable, blocked from local validation, or verified by inspection or documentation review instead of automated tests, record the verification method and residual risk.

## Promotion Rules

When implementation stabilizes, promote accepted spec content into durable docs:

| Spec content | Durable destination |
| --- | --- |
| Requirements and non-requirements | Requirements docs, API contracts, data-flow contracts, or reference docs. |
| Technical design | Design docs, architecture docs, reference docs, or ADRs. |
| Rollout and operational steps | Runbooks or getting-started docs. |
| Data lineage, fields, config routing, and processed outputs | Data-flow docs, field dictionaries, config docs, and reference docs. |
| Lasting decision rationale | ADRs. |
| Temporary research findings | ADR, reference, review, or discard if no longer useful. |
| Deferred implementation work | Backlog or a smaller follow-up spec. |

Do not leave completed behavior documented only in `docs/specs/`.

## Closure Criteria

A spec can be closed when:

- implemented code, tests, config, and migrations are complete or explicitly deferred;
- durable docs describe the resulting current behavior;
- API, data-flow, runbook, reference, and ADR updates are complete where relevant;
- task state is accurate;
- unresolved work is moved to backlog or a follow-up spec;
- the docs index no longer presents the spec as an active implementation package.

Closure may remove the spec, move it to an archive/history area, or keep a clearly marked historical package if the repository's document lifecycle calls for that.
