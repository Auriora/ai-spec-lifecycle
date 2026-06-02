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

Specs are delivery scaffolding. They guide implementation while work is active, but completed behavior must be promoted into the repository's durable documentation.

The only default path this skill assumes is the active spec package location:
`docs/specs/[###-slug]/`. For durable docs, templates, and review records, use
the target repository's documented structure.

## Start

1. Read applicable repo instructions such as `AGENTS.md`.
2. Inspect repository documentation direction such as `docs/README.md`, `docs/templates/`, document lifecycle notes, indexes, and existing docs.
3. Locate the active spec package under `docs/specs/[###-slug]/`.
4. Read available spec artifacts: `research.md`, `spec.md`, `design.md`, `plan.md`, `tasks.md`, `quickstart.md`, plus `open-decisions.md`, contracts, and sequencing docs when present.
5. Identify the repository's durable documentation targets from its own docs structure and templates before assuming document classes or folder names.

If no active package exists and the user asks to start one, create the smallest useful `docs/specs/[###-slug]/` package for the risk level. Use repository templates such as `docs/templates/spec-package/` when present. If no repository template exists, use `references/spec-package/` as the fallback package template.

If several active packages exist, read repository indexes such as `docs/README.md` and any sequencing docs. Ask the user to choose, or select the first blocking slice from documented sequencing guidance when the next step is clear.

## Spec Package Flow

Use spec artifacts as a chain, not interchangeable notes:

- `research.md`: bounded investigation, tradeoffs, unknowns, and recommendations that inform the spec or design.
- `spec.md`: what problem is being solved, goals, non-goals, requirements, acceptance criteria, and success criteria.
- `design.md`: how the accepted requirements will be implemented, including components, contracts, data, operations, and open questions.
- `plan.md`: execution context, constraints, sequencing, validation strategy, affected areas, and risk controls.
- `tasks.md`: executable checklist sliced by independently verifiable work, mapped back to requirements, design, and validation.
- `quickstart.md`: temporary validation, demo, setup, rollout, or operator notes that may later be promoted into durable docs.

Not every task needs every artifact. For small, low-risk work, create only the files that add clear value.

## Reconcile

Produce a concise reconciliation summary when it adds clear value. Reconciliation is required when:

- resuming an existing or partially completed spec;
- tasks are already checked, dates are old, or open decisions exist;
- code or docs appear to have changed outside the task list;
- durable docs disagree with the spec;
- the change affects API contracts, data flow, architecture, operations, security, or cross-module behavior.

Do not trust frontmatter status alone. Reconcile it against repository indexes, sequencing docs, task state, code, tests, config, and durable-doc evidence sections.

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

Before closing or claiming durable completion, route accepted spec content into the repository's current-state docs.

Common routing:

- requirements, non-goals, and acceptance criteria -> the repo's accepted requirements, product, contract, test, or reference docs;
- technical design -> the repo's durable design, architecture, decision, or reference docs;
- rollout and operational steps -> the repo's runbook, getting-started, deployment, or support docs;
- data, schema, API, config, or integration behavior -> the repo's contract, data-flow, schema, config, or integration docs;
- lasting decision rationale -> the repo's decision record or durable history format;
- temporary research -> durable decision, reference, review, or discard when no longer useful;
- deferred work -> backlog, roadmap, issue tracker, or a smaller follow-up spec.

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
- contract, data, operations, reference, and decision-record updates are complete where relevant according to the repository's docs structure;
- task state is accurate;
- unresolved work is moved to backlog or a follow-up spec;
- indexes no longer present the package as active implementation work.

Do not leave completed behavior documented only in `docs/specs/`.
