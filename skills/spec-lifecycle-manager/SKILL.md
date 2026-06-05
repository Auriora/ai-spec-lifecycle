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

The default documentation root is `docs/`, making the default active spec
package location `docs/specs/[###-slug]/`. If the target repository has its own
documentation system that should stay clean, use a named partition such as
`docs/<name>/` and place lifecycle docs under that root, for example
`docs/<name>/specs/[###-slug]/`. For durable docs, templates, and review
records, use the target repository's documented structure.

If the target repository has `docs/templates/` or another documented template
system, treat those templates as authoritative for that repository. Do not apply
this skill's fallback templates silently. When the repository templates differ
from this skill's preferred package shape, record a visible template authority
decision before creating, migrating, or reshaping docs.

This skill includes two kinds of fallback references:

- `references/spec-package/`: temporary implementation spec package templates.
- `references/durable-doc-templates/`: optional durable documentation templates
  for selected projects that do not already have an authoritative documentation
  template system.

## Start

1. Read applicable repo instructions such as `AGENTS.md`.
2. Inspect repository documentation direction such as `docs/README.md`, `docs/templates/`, governance or constitution docs, document lifecycle notes, indexes, existing docs, and whether a lifecycle partition such as `docs/<name>/` is used.
3. Locate the active spec package under the chosen docs root, defaulting to `docs/specs/[###-slug]/`.
4. Read available spec artifacts: `requirements.md`, `design.md`, `tasks.md`, plus optional `change-impact.md`, `verification.md`, `research.md`, `quickstart.md`, `open-decisions.md`, `traceability.md`, contracts, checklists, and sequencing docs when present. If `spec.md` or `plan.md` are found instead, the package uses the old format; handle that through the migration decision gate in Reconcile.
5. Identify the repository's durable documentation targets from its own docs structure and templates before assuming document classes or folder names.

If no active package exists and the user asks to start one, create the smallest useful `[docs-root]/specs/[###-slug]/` package for the risk level. Use repository-documented package templates when present. If no repository-specific package template exists, use `references/spec-package/` as the fallback package template. If both exist and differ, prefer the repository template and record the template authority decision.

If durable documentation must be created or promoted and the target repository
has no documented durable-doc template system, use
`references/durable-doc-templates/` as optional fallback guidance. Copy or adapt
only the specific document class needed, not the whole template set.

If several active packages exist, read repository indexes such as `docs/README.md` and any sequencing docs. Ask the user to choose, or select the first blocking slice from documented sequencing guidance when the next step is clear.

## Spec Package Flow

Use spec artifacts as a progressive chain, not interchangeable notes:

### Core Artifacts (always created)

- `requirements.md`: problem context, goals, non-goals, glossary, user-story-based requirements with EARS-format acceptance criteria, correctness properties for property-based testing, technical context, and success criteria.
- `design.md`: how the accepted requirements will be implemented, split into high-level design (system architecture, components, data models, data flow) and low-level design (algorithms, function signatures, error handling), plus operational considerations and open questions.
- `tasks.md`: Kiro-style checklist of tasks and subtasks, phased grouping for readability, dependency graph or explicit dependency notes, file paths, acceptance criteria, and evidence for completed work.

### Optional Artifacts (created when they add value)

- `change-impact.md`: OpenSpec-style delta record that identifies durable source-of-truth docs, proposed additions/modifications/removals, bug-fix corrections, and promotion targets.
- `verification.md`: validation plan, quality gates, evidence log, residual risks, and release or closure readiness checks.
- `research.md`: bounded investigation, tradeoffs, unknowns, and recommendations that inform the requirements or design.
- `quickstart.md`: temporary validation, demo, setup, rollout, or operator notes that may later be promoted into durable docs.
- `traceability.md`: optional bidirectional matrix that maps tasks to relevant
  requirements, acceptance criteria, design sections, change impact,
  verification, durable targets, and open decisions. Use it when the package is
  large enough that task text may not carry enough context by itself.

Not every task needs every artifact. For small, low-risk work, create only the files that add clear value.

### Requirements Format

Structure requirements as user stories with EARS acceptance criteria:

```markdown
### Requirement N: Title

**User Story:** As a [role], I want [feature], so that [benefit]

#### Acceptance Criteria

1. GIVEN [context], WHEN [action], THEN [outcome]
2. WHERE [condition], THE SYSTEM SHALL [behavior]
3. IF [condition], THEN THE SYSTEM SHALL [behavior]
```

EARS keywords: GIVEN/WHEN/THEN (behavioral), WHERE (context-dependent), WHILE (state-dependent), IF/THEN (conditional), SHALL (unconditional).

Include a Correctness Properties section listing invariants that must hold for property-based testing.

Always reference durable source-of-truth documents that describe current
behavior before the change. If no durable source exists, record that gap and
create a promotion target.

### Change Impact Format

Use `change-impact.md` when a feature, bug fix, refactor, migration, or
operational change modifies existing durable behavior. Classify each change as
add, modify, remove, rename, bug fix, or clarify, and map it to durable docs
that must be updated before closure.

### Design Format

Split implementation details into two levels:

- **High-Level Design**: system architecture, component boundaries, data models, and data flow.
- **Low-Level Design**: algorithms, pseudocode, function signatures, interfaces, and error handling.

Retain operational considerations (rollout, observability, migration, failure handling) as a separate section.

### Task Format

Prefer a Kiro-style checklist over a block-heavy task form:

```markdown
- [ ] T004 [P] [US1] Add tests for user story 1.
  - Depends on: T002, T003
  - Files: `tests/path/to/test`
  - Acceptance: Tests define expected behavior and fail before implementation
    where practical.
  - Evidence: Pending.
  - [ ] T004.1 Cover success path.
  - [ ] T004.2 Cover validation or error path.
```

Task expectations:

- Use stable task IDs (`T001`, `T002`, ...) and subtask IDs (`T004.1`) when useful.
- Keep checkboxes as the visible status marker.
- Use `[P]` only for tasks that can run in parallel without dependency or file conflicts.
- Add `Depends on:`, `Files:`, `Acceptance:`, and `Evidence:` bullets where they materially improve execution or reconciliation.
- Check off subtasks as work progresses, but check off the parent task only when acceptance criteria are met and evidence is recorded.
- Record skipped work with an explicit reason instead of silently deleting it.

The Task Dependency Graph at the top of `tasks.md` is useful for non-trivial specs, but it should support the checklist rather than replace it. Phases provide visual grouping; dependency notes and the graph provide execution order.

### Spec Lifetime

Spec packages are temporary delivery scaffolding with a finite lifetime. Durable docs live with the code and describe current implementation state. Before a spec closes, accepted behavior, decisions, operations, and follow-up work must be promoted or routed into the repository's durable docs, backlog, roadmap, or follow-up specs.

The durable source of truth should always be referenced from the active spec.
For repositories that already have a documentation system, keep lifecycle docs
inside the agreed docs root or partition instead of scattering this repository's
structure across the target project.

### Local Behavior Specs

If stable behavior needs to be documented near a subsystem, avoid polluting source trees unless the target repository explicitly prefers that. Use repository documentation paths such as `docs/specs/src/[path].md`, `docs/specs/modules/[name].md`, or another documented durable location. Feature-package-local files such as `docs/specs/[###-slug]/src/[path].md` may be useful during implementation, but lasting behavior must be promoted before closure.

## Reconcile

Produce a concise reconciliation summary when it adds clear value. Reconciliation is required when:

- resuming an existing or partially completed spec;
- task statuses or checkboxes are already marked complete, dates are old, or open decisions exist;
- code or docs appear to have changed outside the task list;
- durable docs disagree with the spec;
- the change affects API contracts, data flow, architecture, operations, security, or cross-module behavior.

If the spec package uses the old format (has `spec.md` or `plan.md` instead of `requirements.md`, or `tasks.md` has ambiguous checkboxes without dependency, acceptance, or evidence guidance), read `references/migration-guide.md` and use a migration decision gate before implementation:

- continue in old format for this slice;
- migrate before implementation;
- create a follow-up migration task and proceed only if the old format is coherent enough.

Always make the package migration decision visible in the reconciliation
summary, even when the decision is to continue without migration.

When repository templates exist, also make a visible template authority
decision before changing package structure, creating new lifecycle docs, or
updating templates:

- use repository templates as-is;
- use repository templates and add only missing fields needed for this package;
- propose a selective template update for review before changing future docs;
- use this skill's fallback templates because the repository has no documented
  templates.

Do not force migration for archived specs, mid-task collaboration, or small changes where migration would create more risk than value. Do not migrate repository templates wholesale just because this skill prefers a richer package shape. Template migration must be selective: identify the specific document classes affected, the existing docs that would be impacted, required field additions, compatibility risks, and whether old packages should remain untouched.

Do not trust frontmatter status alone. Reconcile it against repository indexes, sequencing docs, task state, governance constraints, code, tests, config, and durable-doc evidence sections.

Treat governance, constitution, policy, `AGENTS.md`, and documented repository principles as higher-priority constraints. If the spec conflicts with them, stop for a decision unless the user explicitly asks to update the governance source.

Classify drift as:

- `spec stale`
- `code incomplete`
- `durable docs stale`
- `decision unresolved`
- `implemented but unverified`
- `intentionally deferred`
- `governance conflict`

For fresh, small, low-risk work, a one- or two-line reconciliation is enough when no conflicting durable docs or code evidence is found.

## Implement

Select one coherent implementation slice at a time, usually a phase, checkpoint, user story, parent task, or subtask group from `tasks.md`. Respect the dependency graph and `Depends on:` notes: only select tasks whose dependencies are complete.

Do not implement from `tasks.md` alone. Treat task text as an execution index,
not the full specification. Before implementing a task, read the relevant
requirements, acceptance criteria, design sections, change-impact entries,
verification expectations, durable-source baseline, and open decisions. If the
task wording appears broad, vague, or ambiguous, resolve it through those
artifacts before coding. Lack of detail in the task line is not a reason to
ignore the fuller spec context.

When `traceability.md` exists, use it as the first task-context lookup for the
selected task ID, then verify the referenced requirements, design sections,
verification expectations, durable targets, and open decisions against the
source artifacts. If the matrix is missing, stale, or incomplete, reconcile it
from the full package instead of proceeding from task text alone.

If this skill's `scripts/traceability_lookup.py` helper is available, prefer it
for the first lookup:

```bash
skills/spec-lifecycle-manager/scripts/traceability_lookup.py docs/specs/004-spec-management-mcp --task T012 --format text
```

Run it from the repository root or pass an absolute spec package path. The
helper returns the task row, linked requirements, acceptance criteria, design
sections, change impact, verification expectations, durable targets, open
decisions, and any gaps such as missing matrix rows, unresolved `TBD` values,
missing referenced artifacts, or missing heading anchors. Treat reported gaps
as reconciliation inputs before implementing the task.

Before choosing the slice, compare task checkboxes, subtasks, acceptance
criteria, and evidence against actual code, tests, config, and durable-doc
evidence. Call out status-stale candidates when validation or review is the
current goal.

Before editing, state:

- selected task IDs or requirement IDs;
- spec artifacts consulted and the relevant details they add;
- files or doc classes likely affected;
- validation expected;
- any unresolved decision that blocks implementation.

Task status rules:

- Check off a parent task only when its acceptance criteria are met.
- Prefer passing tests before marking implementation tasks `done`.
- If automated tests do not apply, record the alternate verification method and residual risk.
- If validation could not run, do not hide that. Check off the parent task only when it can be defensibly verified without that validation.
- Update task `Evidence` when a task is checked complete; evidence can be a command, test result, review note, screenshot, log, commit, or manual verification note.
- Mark a task or subtask as skipped only with a documented reason (intentional deferral, superseded, or out of scope).

## Verify

Before promotion, release, or closure, inspect `verification.md`, checklists, task evidence, and validation commands when present.

Verification should record:

- validation commands or review methods used;
- task IDs, requirements, and acceptance criteria covered;
- evidence for completed tasks;
- quality gates passed or intentionally waived;
- residual risks and follow-up owners;
- release or closure readiness;
- ship or closure risk level, blast radius, rollback path, human-review needs,
  and release-note requirements when applicable.

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

Promotion should produce an explicit durable-doc map before closure:

- spec content promoted;
- durable destination path or documented deferral;
- evidence that the destination now reflects current behavior;
- residual spec-only content, if any, and why it remains.

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
- verification evidence and quality gates are complete or explicitly waived with residual risk;
- durable docs describe the resulting current behavior;
- contract, data, operations, reference, and decision-record updates are complete where relevant according to the repository's docs structure;
- task state is accurate;
- unresolved work is moved to backlog or a follow-up spec;
- indexes no longer present the package as active implementation work.

Before closing, perform a final spec cleanup check:

1. Re-read `requirements.md`, `design.md`, `tasks.md`, `change-impact.md`,
   `verification.md`, `quickstart.md`, `research.md`, and `open-decisions.md`
   if present.
2. Classify each lasting element as promoted, explicitly deferred, discarded, or
   retained as history.
3. Confirm durable destinations exist and are linked from the relevant indexes.
4. Confirm active docs no longer point readers to the spec as the source of
   current behavior.
5. Decide the package disposition according to the target repository's document
   lifecycle: archive, remove, or retain as a clearly historical record.
6. Update active spec indexes, sequencing docs, task boards, or README entries
   so the package no longer appears active.
7. Record closure evidence in `verification.md` or the repository's chosen
   closure record.

Do not leave completed behavior documented only in `docs/specs/`. If durable
promotion is blocked, keep the spec open or create a follow-up with an explicit
owner, destination, and closure blocker.
