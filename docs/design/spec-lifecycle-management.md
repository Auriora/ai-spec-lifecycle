---
title: Spec lifecycle management
doc_type: design
status: active
owner: platform
last_reviewed: 2026-06-02
---

# Spec Lifecycle Management

## Purpose

Define a reusable lifecycle for AI-assisted implementation specs. The lifecycle keeps requirements, specs, code, tests, configuration, and durable documentation consistent while work is in progress and prevents completed behavior from living only in temporary spec packages.

## Core Model

Specs are implementation scaffolding with a finite lifetime, not the final
source of truth.

```text
durable docs -> active spec -> code/tests/config -> durable docs -> close spec
```

Durable docs describe accepted requirements, current architecture, current
design, operator procedures, API contracts, data-flow behavior, reference
material, and lasting decisions. Specs coordinate work while a change is being
designed or implemented. Once implementation stabilizes, accepted behavior must
move into durable docs that live with the code and reflect current state.

## Spec Package Shape

Use `docs/specs/[###-slug]/` for active specs by default. The numeric prefix
gives stable ordering, and the slug gives a readable feature name.

When working in a repository with its own documentation approach, use a named
documentation partition such as `docs/<name>/` when the user wants lifecycle
material kept separate. In that case, active specs live under
`docs/<name>/specs/[###-slug]/`, and durable docs for that lifecycle partition
live under the same docs root unless the target repository documents another
location.

Current fallback package files:

- `requirements.md`: problem context, goals, non-goals, glossary, user stories
  with EARS acceptance criteria, correctness properties, technical context, and
  success criteria.
- `design.md`: high-level design, low-level design, operational
  considerations, and open questions.
- `tasks.md`: task dependency graph, phased task grouping, per-task status,
  dependencies, affected files, acceptance criteria, and evidence.
- `change-impact.md`: optional durable-delta record for changes to existing
  behavior, including features, bug fixes, removals, renames, clarifications,
  and promotion targets.
- `verification.md`: optional validation plan, quality gates, evidence log,
  residual risks, and readiness checks.
- `research.md`: optional bounded analysis and decision inputs.
- `quickstart.md`: optional temporary validation or rollout notes that may later
  become runbooks or getting-started docs.
- `open-decisions.md`: optional unresolved decisions that block stable
  implementation.

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
| `docs/specs/` | Temporary active delivery packages and optional documented subsystem spec locations. |

Repositories may use different folder names. The lifecycle still applies: identify each repository's durable doc classes before implementing from a spec.

## Durable Source And Delta Rules

The durable source of truth should always be referenced from an active spec. If
the change modifies existing behavior, the spec should identify the current
durable docs, contracts, schemas, runbooks, or code-derived references that
describe that behavior.

Use `change-impact.md` when the work changes existing behavior, including bug
fixes. The change-impact record should classify each delta as add, modify,
remove, rename, bug fix, or clarify, and map each delta to the durable document
that must be updated before closure.

If no durable source exists for behavior that should be stable, record that as
a documentation gap and assign a durable promotion target.

## Reconciliation

Before implementation, the agent should reconcile the active spec against durable docs, code, tests, and configuration when doing so adds clear value. Reconciliation is required when:

- resuming an existing or partially completed spec;
- the spec has checked tasks, old dates, or open decisions;
- implementation appears to have progressed outside the task list;
- durable docs disagree with the spec;
- the task touches API contracts, data-flow behavior, architecture, operations, security, or cross-module behavior.

The reconciliation should identify whether each mismatch means the spec is
stale, code is incomplete, durable docs are stale, a decision is unresolved,
work is implemented but unverified, work is intentionally deferred, or the spec
conflicts with governance.

If an active package uses an older `spec.md`/`plan.md`/checkbox format,
migration is a decision gate. The agent should decide whether to continue the
old format for the current slice, migrate before implementation, or create a
follow-up migration task. Archived specs should remain historical unless
resumed.

## Implementation Rules

- Implement one coherent task slice at a time, usually one phase or checkpoint from `tasks.md`.
- Prefer independently testable user-story slices over broad task batches.
- Map tests and validation back to requirement IDs, acceptance criteria, success criteria, or task IDs where practical.
- Update task status only when the task's completion criteria are satisfied.
- Prefer passing tests before marking implementation tasks `done`.
- Record task evidence before marking a task `done`.
- If a task is not testable, blocked from local validation, or verified by inspection or documentation review instead of automated tests, record the verification method and residual risk.

## Verification Rules

Before promotion, release, or closure, record validation evidence and residual
risk. Verification may live in `verification.md`, task evidence fields,
checklists, review records, or durable docs depending on the repository's
structure.

Verification should map evidence back to task IDs, requirements, acceptance
criteria, and success criteria where practical.

Before release or closure, classify ship or closure risk as low, medium, or
high. Record blast radius, rollback path, required human review, release-note
needs, and follow-up specs or issues when applicable.

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
- verification evidence and quality gates are complete or explicitly waived with residual risk;
- durable docs describe the resulting current behavior;
- API, data-flow, runbook, reference, and ADR updates are complete where relevant;
- task state is accurate;
- unresolved work is moved to backlog or a follow-up spec;
- the docs index no longer presents the spec as an active implementation package.

Closure may remove the spec, move it to an archive/history area, or keep a clearly marked historical package if the repository's document lifecycle calls for that.
