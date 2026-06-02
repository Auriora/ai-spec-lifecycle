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
4. Read available spec artifacts: `requirements.md`, `design.md`, `tasks.md`, plus optional `research.md`, `quickstart.md`, `open-decisions.md`, contracts, and sequencing docs when present. If `spec.md` or `plan.md` are found instead, the package uses the old format and should be migrated (see Reconcile).
5. Identify the repository's durable documentation targets from its own docs structure and templates before assuming document classes or folder names.

If no active package exists and the user asks to start one, create the smallest useful `docs/specs/[###-slug]/` package for the risk level. Use repository templates such as `docs/templates/spec-package/` when present. If no repository template exists, use `references/spec-package/` as the fallback package template.

If several active packages exist, read repository indexes such as `docs/README.md` and any sequencing docs. Ask the user to choose, or select the first blocking slice from documented sequencing guidance when the next step is clear.

## Spec Package Flow

Use spec artifacts as a progressive chain, not interchangeable notes:

### Core Artifacts (always created)

- `requirements.md`: problem context, goals, non-goals, glossary, user-story-based requirements with EARS-format acceptance criteria, correctness properties for property-based testing, technical context, and success criteria.
- `design.md`: how the accepted requirements will be implemented, split into high-level design (system architecture, components, data models, data flow) and low-level design (algorithms, function signatures, error handling), plus operational considerations and open questions.
- `tasks.md`: task dependency graph (DAG) showing execution order, phased grouping for readability, and per-task entries with status tracking (pending/in_progress/done/skipped), explicit dependencies, file paths, and acceptance criteria.

### Optional Artifacts (created when they add value)

- `research.md`: bounded investigation, tradeoffs, unknowns, and recommendations that inform the requirements or design.
- `quickstart.md`: temporary validation, demo, setup, rollout, or operator notes that may later be promoted into durable docs.

Not every task needs every artifact. For small, low-risk work, create only the files that add clear value.

### Requirements Format

Structure requirements as user stories with EARS acceptance criteria:

```markdown
### Requirement N: Title

**User Story:** As a [role], I want [feature], so that [benefit]

#### Acceptance Criteria

1. GIVEN [context], WHEN [action], THEN [outcome]
2. WHERE [condition], THE system SHALL [behavior]
3. IF [condition], THEN THE system SHALL [behavior]
```

EARS keywords: GIVEN/WHEN/THEN (behavioral), WHERE (context-dependent), WHILE (state-dependent), IF/THEN (conditional), SHALL (unconditional).

Include a Correctness Properties section listing invariants that must hold for property-based testing.

### Design Format

Split implementation details into two levels:

- **High-Level Design**: system architecture, component boundaries, data models, and data flow.
- **Low-Level Design**: algorithms, pseudocode, function signatures, interfaces, and error handling.

Retain operational considerations (rollout, observability, migration, failure handling) as a separate section.

### Task Format

Each task entry includes:

- **ID**: unique identifier (T001, T002, ...)
- **Status**: pending | in_progress | done | skipped
- **Depends on**: list of task IDs that must complete first
- **Parallel**: whether it can run alongside other tasks in the same phase
- **Story**: user story reference (US1, US2, ...) or — if cross-cutting
- **Files**: exact file paths affected
- **Description**: what needs to be done
- **Acceptance**: how to verify the task is complete

The Task Dependency Graph at the top of `tasks.md` shows the full DAG in text form. Phases provide visual grouping; the DAG provides execution order.

## Reconcile

Produce a concise reconciliation summary when it adds clear value. Reconciliation is required when:

- resuming an existing or partially completed spec;
- tasks are already checked, dates are old, or open decisions exist;
- code or docs appear to have changed outside the task list;
- durable docs disagree with the spec;
- the change affects API contracts, data flow, architecture, operations, security, or cross-module behavior.

If the spec package uses the old format (has `spec.md` or `plan.md` instead of `requirements.md`, or `tasks.md` uses checkboxes without a Task Dependency Graph), read `references/migration-guide.md` and migrate before proceeding with implementation.

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

Select one coherent implementation slice at a time, usually a phase, checkpoint, user story, or requirement group from `tasks.md`. Respect the Task Dependency Graph: only select tasks whose dependencies are all `done`.

Before choosing the slice, compare task status fields against actual code, tests, config, and durable-doc evidence. Call out status-stale candidates when validation or review is the current goal.

Before editing, state:

- selected task IDs or requirement IDs;
- files or doc classes likely affected;
- validation expected;
- any unresolved decision that blocks implementation.

Task status rules:

- Set a task to `done` only when its acceptance criteria are met.
- Prefer passing tests before marking implementation tasks `done`.
- If automated tests do not apply, record the alternate verification method and residual risk.
- If validation could not run, do not hide that. Mark the task `done` only when it can be defensibly verified without that validation.
- Set a task to `skipped` only with a documented reason (intentional deferral, superseded, or out of scope).

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
