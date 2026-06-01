---
name: spec-lifecycle-manager
description: Manage AI-assisted implementation specs from intake through reconciliation, implementation, durable documentation promotion, expert review, and closure. Use when creating, continuing, reconciling, reviewing, implementing from, promoting, or closing spec packages, especially under docs/specs/[###-slug]/.
---

# Spec Lifecycle Manager

Use this skill to keep temporary implementation specs, durable docs, code, tests, and config aligned.

Core rule:

```text
durable docs -> active spec -> code/tests/config -> durable docs -> close spec
```

Specs are delivery scaffolding. They guide implementation while work is active, but completed behavior must be promoted into durable repository documentation.

## Start

1. Read applicable repo instructions such as `AGENTS.md`.
2. Inspect the repository docs structure before assuming folder names.
3. Locate the active spec package. Default convention: `docs/specs/[###-slug]/`.
4. Read available spec artifacts: `spec.md`, `design.md`, `plan.md`, `tasks.md`, plus `research.md`, `quickstart.md`, `open-decisions.md`, and sequencing docs when present.
5. Identify relevant durable docs: requirements, architecture, design, data-flow, API contracts, runbooks, ADRs, reference docs, backlog, and reviews.

If the repository uses different folder names, map its equivalent durable doc classes before implementing.

If no active package exists and the user asks to start one, create the smallest useful `docs/specs/[###-slug]/` package for the risk level. Use repository templates such as `docs/templates/spec-package/` when present before inventing a package shape.

If several active packages exist, read repository indexes such as `docs/README.md` and any sequencing docs. Ask the user to choose, or select the first blocking slice from documented sequencing guidance when the next step is clear.

## Reconcile

Produce a concise reconciliation summary when it adds clear value. Reconciliation is required when:

- resuming an existing or partially completed spec;
- tasks are already checked, dates are old, or open decisions exist;
- code or docs appear to have changed outside the task list;
- durable docs disagree with the spec;
- the change affects API contracts, data flow, architecture, operations, security, or cross-module behavior.

Do not trust frontmatter status alone. Reconcile it against docs indexes, sequencing docs, task state, code, tests, config, and durable-doc evidence sections.

Classify drift as:

- `spec stale`
- `code incomplete`
- `durable docs stale`
- `decision unresolved`
- `implemented but unverified`
- `intentionally deferred`

For fresh, small, low-risk work, a one- or two-line reconciliation is enough when no conflicting durable docs or code evidence is found.

## Implement

Select one coherent implementation slice at a time, usually a phase, checkpoint, user story, or requirement group from `tasks.md`.

Before choosing the slice, compare checked and unchecked task state against actual code, tests, config, and durable-doc evidence. Call out task-state stale candidates when validation or review is the current goal.

Before editing, state:

- selected task IDs or requirement IDs;
- files or doc classes likely affected;
- validation expected;
- any unresolved decision that blocks implementation.

Task checkbox rules:

- Check a task only when its completion criteria are met.
- Prefer passing tests before checking implementation tasks complete.
- If automated tests do not apply, record the alternate verification method and residual risk.
- If validation could not run, do not hide that. Mark the task complete only when the task can be defensibly verified without that validation.

## Promote

Before closing or claiming durable completion, route accepted spec content into current-state docs.

Common routing:

- requirements and non-requirements -> requirements docs, API contracts, data-flow contracts, or reference docs;
- technical design -> design docs, architecture docs, reference docs, or ADRs;
- rollout and operational steps -> runbooks or getting-started docs;
- data lineage, fields, config routing, and processed outputs -> data-flow docs, field dictionaries, config docs, and references;
- lasting decision rationale -> ADRs;
- temporary research -> ADR, reference, review, or discard;
- deferred work -> backlog or a smaller follow-up spec.

Read `references/document-routing-and-expert-review.md` when document routing or review roles are material to the task.

## Review

Use role-based expert review guidance, not subject-matter-specific reviewers, unless the user supplies domain reviewers.

Record review evidence when review is part of the workflow:

- document or package reviewed;
- expert role;
- date;
- findings or sign-off;
- required follow-up;
- whether follow-up blocks implementation, release, or closure.

## Close

A spec can close only when:

- code, tests, config, migrations, and docs are complete or explicitly deferred;
- durable docs describe the resulting current behavior;
- API, data-flow, runbook, reference, and ADR updates are complete where relevant;
- task state is accurate;
- unresolved work is moved to backlog or a follow-up spec;
- indexes no longer present the package as active implementation work.

Do not leave completed behavior documented only in `docs/specs/`.
