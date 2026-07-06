---
name: spec-lifecycle-manager
description: Manage AI-assisted implementation specs from intake through reconciliation, implementation, durable documentation promotion, expert review, and closure. Use when creating, continuing, reconciling, reviewing, implementing from, promoting, or closing spec packages, especially under docs/specs/[###-slug]/.
copyright: Copyright 2026 Auriora
license: GPL-3.0-or-later
compatibility: Requires Codex with Agent Skills support, Python 3.9+, and repository docs using AGENTS.md or equivalent instructions; MCP and hooks are optional but supported.
metadata:
  author: Auriora
  version: "0.1.0"
  bundled_in_plugin: spec-lifecycle-manager
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
system, treat those templates as authoritative for durable repository
documentation. Do not apply this skill's durable-doc fallback templates
silently. For temporary implementation spec packages, treat
`docs/templates/spec-package/` as the repository override only when that
directory exists. A durable-doc template directory by itself does not override
this skill's spec-package fallback templates.

This skill includes two kinds of fallback references:

- `references/spec-package/`: temporary implementation spec package templates.
- `references/durable-doc-templates/`: optional durable documentation templates
  for selected projects that do not already have an authoritative documentation
  template system.

## Start

1. Read applicable repo instructions before changing files. Start with root
   `AGENTS.md` when present, then read any deeper `AGENTS.md` files that govern
   the target paths. If no repository instructions are available in the session,
   give the user one short hint to run `/init` so future agents can discover
   repository guidance; do not repeat that hint after it has been given in the
   same session.
2. Inspect repository documentation direction such as `docs/README.md`, `docs/templates/`, governance or constitution docs, document lifecycle notes, indexes, existing docs, and whether a lifecycle partition such as `docs/<name>/` is used.
3. Locate the active spec package under the chosen docs root, defaulting to `docs/specs/[###-slug]/`.
4. Read available spec artifacts: `requirements.md`, `design.md`, `tasks.md`, plus optional `change-impact.md`, `verification.md`, `research.md`, `quickstart.md`, `open-decisions.md`, `traceability.md`, contracts, checklists, and sequencing docs when present. If `spec.md` or `plan.md` are found instead, the package uses the old format; handle that through the migration decision gate in Reconcile.
5. Identify the repository's durable documentation targets from its own docs structure and templates before assuming document classes or folder names.

If no active package exists and the user asks to start one, create the smallest useful `[docs-root]/specs/[###-slug]/` package for the risk level. Use repository-documented spec-package templates when `docs/templates/spec-package/` or an equivalent explicit spec-package template location exists. If no repository-specific spec-package template exists, use `references/spec-package/` as the fallback package template. If both exist and differ, prefer the repository template and record the template authority decision.

If no active package exists and the user is not asking to start one, do not
recreate or browse removed spec packages as if they are current work. Use
durable docs, `docs/backlog/`, `docs/roadmap/`, the closure log, and the spec
archive index as the current context. Removed package paths in history records
are evidence pointers to Git history, not active implementation targets, unless
the user explicitly asks for historical audit or restoration.

If durable documentation must be created or promoted and the target repository
has no documented durable-doc template system, use
`references/durable-doc-templates/` as optional fallback guidance. Copy or adapt
only the specific document class needed, not the whole template set.
Use `references/durable-doc-templates/project-principles.md` when a repository
needs a project-fit guide that explains purpose, problem, VMOST, scope
boundaries, decision questions, governance relationship, and current product
signals.

If several active packages exist, read repository indexes such as `docs/README.md` and any sequencing docs. Ask the user to choose, or select the first blocking slice from documented sequencing guidance when the next step is clear.

## First Run

When entering an unfamiliar repository, start with a runtime-backed orientation
before creating docs or specs. Use `lifecycle_guide` when available; otherwise
use `active_spec_preflight`, `scan_specs`, repository instructions, durable
indexes, backlog, roadmap, closure logs, and archive indexes to answer three
questions:

- What lifecycle state is this repository in?
- What tools, docs, templates, governance constraints, and active specs are
  available?
- What is the smallest useful next action?

First-run guidance should report MCP tools when they are available and include
equivalent CLI commands for validation, CI, and recovery. If MCP tools are not
available, provide the direct `spec_runtime.py` commands needed to recover the
same read-only context.

If the repository is blank or near blank, enter bootstrap mode instead of
failing because `docs/`, `docs/specs/`, architecture docs, or durable lifecycle
indexes are absent. Bootstrap mode is preview-first:

- classify the repository evidence as `blank` or `near_blank`;
- ask for or record a project-purpose statement before durable structure is
  generated;
- propose only the minimum useful docs foundation, such as a docs root,
  lifecycle index, project summary, runbook target, or optional first spec;
- do not require an architecture document before requirements work can start;
- recommend architecture or pattern docs only when code, project structure, or
  user-confirmed purpose provides evidence for them;
- keep proposed writes limited to lifecycle/docs paths unless the user
  explicitly asks for source changes.

Do not recreate deleted spec packages when first-run guidance finds no active
specs. Use durable docs, backlog, roadmap, closure logs, and archive indexes as
the current source of truth.

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
- `canonical-context.md`: optional working-context map that identifies
  always-canonical external sources, spec-canonical working sources, imported
  durable sources, non-canonical background sources, and promotion routes. Use
  it for broad or durable-doc-impacting specs, imported or adapted durable
  sources, stale-doc risk, or resumed specs where older docs may otherwise be
  mistaken for implementation authority. Small specs may embed equivalent
  `## Canonical Context` sections in core artifacts when a separate file would
  add ceremony.

Not every task needs every artifact. For small, low-risk work, create only the
files that add clear value, but do not drop the underlying intent. Embed the
needed durable-source baseline, durable-document impact, verification
expectations, traceability links, open decisions, and promotion targets in
`requirements.md`, `design.md`, or `tasks.md` when separate files would only
duplicate content.

Spec-local canonical context narrows implementation context for an active
slice, but it never overrides always-canonical external authorities: system,
developer, and user instructions, applicable `AGENTS.md`, governance, policy,
security, privacy or compliance rules, generated contracts, source-code
contracts, tests, and live/system evidence. When a spec imports, adapts, or
supersedes durable docs, record source path, source revision or date when
available, import mode, canonical scope, and promotion target. Durable or
historical docs not listed as canonical, imported, or explicitly referenced by
the active spec are background or drift evidence when they conflict with the
declared working context.

Use staged artifact progression for new or resumed specs:

1. `discover`: inspect repo state, instructions, durable docs, tooling, and
   template authority.
2. `bootstrap`: preview the minimum lifecycle foundation for blank or near
   blank repositories.
3. `requirements`: capture goals, non-goals, user stories, acceptance
   criteria, correctness properties, durable-source baseline, and durable-doc
   impact.
4. `design`: map accepted requirements and correctness properties to concrete
   components, interfaces, operational behavior, and validation strategy.
5. `tasks`: define ordered, traceable work with dependencies, evidence, and
   checkpoints.
6. `agent_ready`: provide a bounded Agent Readiness Contract before a worker
   agent edits files.
7. `implement`: execute one coherent task slice and record evidence.
8. `verify`: record validation evidence, waivers, residual risk, and review
   outcomes.
9. `promote`: move accepted behavior to durable docs, backlog, roadmap, ADRs,
   runbooks, or follow-up specs.
10. `close`: preserve closure breadcrumbs and remove or archive temporary spec
    scaffolding according to repository policy.

For user-facing guided documentation work, use the `documentation-wizard`
prompt when available. The wizard is prompt-only in v1: it composes existing
read-only tools and asks one bounded stage-specific question at a time by
default. Use checklist mode only when the user asks for a compact or fast pass.
It must preserve stage order unless an explicit exception is requested and
recorded, and it must not report implementation readiness while blocking open
questions, missing downstream review, or stale artifact dependencies remain.
Wizard mode is the default for creating or continuing specs, including
backlog-to-spec work. Disable wizard mode only when the user explicitly asks to
scaffold all artifacts, create the full package, or batch-generate
requirements, design, and tasks.

In wizard mode, do not create downstream artifacts before the current stage is
accepted. Some artifacts may be created together when they belong to the same
stage:

- `canonical-context.md` during discover when durable-doc drift, imported
  sources, confusing history, or multiple authorities exist.
- `requirements.md` plus `change-impact.md` when durable behavior or durable
  documentation is affected.
- `tasks.md` plus `traceability.md`; tasks without traceability are too easy to
  implement from checklist text alone.
- `verification.md` plus `quickstart.md` only when temporary validation, demo,
  or operator steps need a runnable guide.

`open-decisions.md` is optional. Create it only when decisions are numerous,
cross-cutting, owned by different people, or block multiple downstream tasks.
For small specs, keep open questions in `requirements.md` or `design.md`.

When reporting open questions, include why the question matters, affected
stage, expected answer shape, blocking status, likely artifact destination, and
whether the answer blocks implementation readiness. When handling feedback,
classify each item with exactly one primary disposition: accept, revise, defer,
reject, or human decision required. Accepted feedback should identify affected
artifact sections and validation impact; deferred feedback should identify one
destination and residual risk; rejected feedback should preserve rationale
without becoming a requirement.

Before editing files during guided documentation, provide a preview edit plan
with repo-relative path, target section, change type, and rationale. The wizard
does not add a write-capable MCP tool; approved edits still use ordinary file
edits under the repository's normal lifecycle and permission rules.

Default to requirements before design and design before tasks. If the user
explicitly chooses a design-first flow, record partial requirements, label the
exception, and require a later requirements-completion step before
implementation readiness. When requirements change after design or tasks exist,
flag downstream review instead of silently rewriting later artifacts. When
design changes after tasks exist, flag task and traceability review before
implementation continues.

Optional artifacts remain optional. Recommend or create them only when risk,
durable-doc impact, validation needs, open decisions, or traceability size make
them useful for the current work.

`spec.md` is an old-format compatibility artifact, not a current core artifact.
If an active package contains `spec.md`, classify it during reconciliation as:

- `feature brief`: concise package overview that does not duplicate current
  requirements or design;
- `migration input`: old-format requirements or acceptance content that still
  needs to be migrated;
- `deprecated duplicate`: content already represented in current artifacts or
  durable docs and likely to go stale.

Do not create new `spec.md` files from the fallback templates.

### Requirements Format

Structure requirements as user stories with EARS acceptance criteria:

```markdown
### Requirement N: Title

**User Story:** As a [role], I want [feature], so that [benefit]

**Priority:** must-have

#### Acceptance Criteria

1. GIVEN [context], WHEN [action], THEN [outcome]
2. WHERE [condition], THE SYSTEM SHALL [behavior]
3. IF [condition], THEN THE SYSTEM SHALL [behavior]
```

EARS keywords: GIVEN/WHEN/THEN (behavioral), WHERE (context-dependent), WHILE (state-dependent), IF/THEN (conditional), SHALL (unconditional).

Use optional requirement-level MoSCoW priority when it clarifies scope:
`must-have`, `should-have`, or `could-have`. Place the line after the user
story and before acceptance criteria. Missing priority remains compatible.
Acceptance criteria inherit the parent requirement priority; do not require
duplicate priority labels on every criterion. Excluded work belongs in
non-goals, out-of-scope text, rejected decisions, or routed residuals rather
than a persisted `won't-have` accepted requirement priority.

Include a Correctness Properties section listing invariants that must hold for
property-based testing. Keep the property IDs stable enough to reference from
test tasks. The skill is language-neutral: use the target repository's normal
property-test tool when one exists, such as Hypothesis for Python, fast-check
for TypeScript, proptest or quickcheck for Rust, Go fuzzing, or FsCheck for
.NET.

Always reference durable source-of-truth documents that describe current
behavior before the change. If no durable source exists, record that gap and
create a promotion target.

Durable docs should describe current accepted state by default. Intended future
state belongs in active specs, backlog, roadmap, ADR proposals, or explicitly
marked proposed/deferred sections. An active spec must state whether it adds to,
modifies, clarifies, supersedes, or leaves unchanged relevant durable
requirements, design, architecture, API/contract, data-flow, runbook,
verification, reference, ADR, backlog, or roadmap documents.

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
- Use task markers consistently:
  - `[ ]`: pending or not started.
  - `[~]`: in progress. Update the selected task to `[~]` before starting work.
  - `[/]`: partial. Use when part of the task was completed but acceptance
    criteria are not fully met; record what remains in `Evidence:` or a status note.
  - `[>]`: follow-up or routed. Use when work is moved to another task, spec,
    backlog item, issue, or owner; record `Destination:` and remaining work.
  - `[-]`: no-op or deferred. Use when work is intentionally unnecessary,
    raw-only, not applicable, superseded, or deferred from the current spec;
    record the reason and evidence.
  - `[?]`: review or decision needed. Use when the task awaits review,
    sign-off, or a decision; record `Decision owner:` when known.
  - `[!]`: attention needed. Use when execution failed, a blocker exists, or
    intervention is required; record the diagnostic state and next step.
  - `[x]`: complete and verified.
- Legacy markers remain readable during migration: `[Y]` maps to `partial`,
  while `[*]` and `[e]` map to `attention` and preserve their legacy marker in
  runtime payloads.
- Use optional metadata fields when they clarify non-final states:
  `Evidence mode:`, `Follow-up:`, `Destination:`, `Decision owner:`,
  `Upstream specs:`, and `Downstream specs:`.
- Treat `Evidence mode:` as part of the completion contract, not decorative
  prose. `implementation` and `validation` evidence can complete ordinary
  implementation tasks when acceptance is met. `planner`, `contract`,
  `dry_run`, `routing`, `no_op`, and `blocked_output` evidence must not be used
  to mark implementation complete unless the task acceptance explicitly says
  that mode satisfies the task.
- Split broad tasks before implementation when they span multiple source
  families, evidence modes, implementation outcomes, validation surfaces,
  profiles, or cross-spec dependencies. Prefer Kiro-style subtasks with their
  own evidence over one checkbox that hides routing, no-op, blocked output, or
  validation-only work.
- Use `[P]` only for tasks that can run in parallel without dependency or file conflicts.
- Add `Depends on:`, `Files:`, `Acceptance:`, and `Evidence:` bullets where they materially improve execution or reconciliation.
- Check off subtasks as work progresses, but check off the parent task only when acceptance criteria are met and evidence is recorded.
- Record skipped work with an explicit reason instead of silently deleting it.
- Use explicit checkpoint tasks when a phase boundary, subsystem boundary,
  validation pause, or human decision point needs evidence before proceeding.
  A checkpoint task should list the validation commands or reviews to run and
  record whether any user question, residual risk, or follow-up remains.
- When requirements define Correctness Properties, carry them into property-test
  tasks or subtasks. Name the linked properties, requirements, expected
  invariants, test framework if known, and evidence required. Do not require a
  third-party property-test dependency when the target repository has no accepted
  dependency path; route that decision through design or open decisions.

The Task Dependency Graph at the top of `tasks.md` is useful for non-trivial specs, but it should support the checklist rather than replace it. Phases provide visual grouping; dependency notes and the graph provide execution order.

### Lifecycle Triage

Use the lightest lifecycle path that fits the risk:

- `trivial`: typo, formatting, or narrow local edit with no lifecycle impact.
  Follow repository instructions, edit directly, and validate proportionately.
- `small`: bounded change with known files and low durable-doc impact. Use
  focused context and validation; do not create a spec by default.
- `spec-needed`: behavior change, cross-module change, plugin packaging change,
  governance-sensitive work, unclear acceptance criteria, migration, or
  operational risk. Create or continue an active spec.
- `review`: read-only audit, comparison, investigation, or code review. Use the
  relevant review stance and deterministic context before suggesting changes.
- `closure`: request to complete, close, archive, or reconcile lifecycle state.
  Use closure readiness, durable promotion, and archive-index workflow.

The `lifecycle-triage` prompt is a convenience entry point for this routing
model. It is advisory and does not replace user instructions or repository
governance.

### Lifecycle Gates

Use these gate names when reporting readiness:

- `ready_to_implement`: requirements, design, traceability, open decisions, and
  validation expectations are coherent enough to start an implementation slice.
- `ready_to_validate`: implementation tasks have evidence and the validation
  plan identifies required commands or review methods.
- `ready_to_close`: tasks are complete with evidence, decisions are resolved or
  deferred, durable docs are promoted, and closure blockers are clear.
- `ready_to_archive`: closure log and archive index entries are prepared and
  the active package can be removed after a final spec commit.

If a gate is not ready, report concrete blockers and the evidence needed to
clear them. Runtime-enforced gate fields are intentionally deferred until a
focused spec defines schema and compatibility behavior.

### Spec Lifetime

Spec packages are temporary delivery scaffolding with a finite lifetime. Durable docs live with the code and describe current implementation state. Before a spec closes, accepted behavior, decisions, operations, and follow-up work must be promoted or routed into the repository's durable docs, backlog, roadmap, or follow-up specs. After closure, remove the completed spec package from the active docs tree unless explicit repository policy requires a visible historical package.

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

Keep `references/migration-guide.md` current with lifecycle improvements. When
this skill changes task states, validation semantics, closure checks, artifact
rules, or durable-document integration, update the migration guide and bundled
copies in the same release slice.

When repository spec-package templates exist, also make a visible template
authority decision before changing package structure, creating new lifecycle
docs, or updating templates:

- use repository templates as-is;
- use repository templates and add only missing fields needed for this package;
- propose a selective template update for review before changing future docs;
- use this skill's fallback templates because the repository has no documented
  spec-package templates.

Do not force migration for archived specs, mid-task collaboration, or small changes where migration would create more risk than value. Do not migrate repository templates wholesale just because this skill prefers a richer package shape. Template migration must be selective: identify the specific document classes affected, the existing docs that would be impacted, required field additions, compatibility risks, and whether old packages should remain untouched.

When broad durable-doc impact, stale-doc risk, imported durable sources, or
resumed-spec drift are present and no canonical context exists, treat missing
canonical context as advisory unless repository policy explicitly says
otherwise. Inspect the concrete context risk before adding artifacts. Create
`canonical-context.md`, embed `## Canonical Context` sections in the active
package, or return an explicit import plan only when the risk affects current
implementation authority. The import plan should name the source path, target
spec-local path, import mode, canonical scope, and promotion target. If the
package uses repository templates, follow their documented canonical-context
location. Do not recreate, modernize, or add artifacts to closed, archived,
removed, or otherwise historical spec packages because of canonical-context
diagnostics.

Archived, closed, or superseded specs are historical delivery records. Default
runtime scans keep them visible in inventory but exclude them from active
authoring lint health. Use explicit lint or scan audit mode only when
intentionally reviewing old records, and make a visible resumption, migration,
or cleanup decision before modernizing archived packages.

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

When `canonical-context.md` exists, read it before broader durable-doc scans for
the selected slice. Treat its spec-canonical working sources and imported
sources as the first working context, while preserving always-canonical external
authorities. If a durable doc conflicts with declared canonical context and is
not listed as always-canonical, imported, or explicitly referenced, classify the
conflict as drift and reconcile before using that doc as implementation
authority.

### Runtime Access Order

When MCP tools are available in the current Codex session, use them before
shelling out to this skill's Python runtime scripts. The MCP server is the
primary agent-facing surface for lifecycle context and deterministic checks:

- `scan_specs` or `active_spec_preflight` before lifecycle work.
- `task_context` and `traceability_lookup` before implementing a selected task.
- `spec_summary`, `lint_spec_package`, `next_task`, `closure_check`,
  `archive_index`, `reconcile_spec`, `promotion_plan`, `review_packet`,
  `agent_backed_tool`, and `prompts_validate` for their matching workflows.

Use the repo-local helpers under `skills/spec-lifecycle-manager/scripts/`
directly as implementation, CI, validation, and recovery interfaces only: MCP
unavailable, installed-runtime validation, MCP adapter debugging, or a
repository validation checklist that explicitly requires the CLI command.

If MCP tools are unavailable, use `spec_runtime.py` for retained validation and
recovery checks, then read `traceability.md` and linked source artifacts
directly for task context. Do not call a separate traceability lookup script;
the public agent-facing lookup surface is the MCP `traceability_lookup` tool.
Treat missing matrix rows, unresolved `TBD` values, missing referenced
artifacts, or missing heading anchors as reconciliation inputs before
implementing the task.

When MCP tools are unavailable or CLI validation is explicitly required, the
repo-local `skills/spec-lifecycle-manager/scripts/spec_runtime.py` helper is a
retained recovery and validation adapter. Normal agent-facing lifecycle
commands have MCP owners:

- `scan_specs` for inventory and health.
- `spec_summary` for spec summaries.
- `lint_spec_package` and `lint_doc` for lint checks.
- `next_task` for task selection.
- `closure_check` for closure readiness.
- `reconcile_spec`, `promotion_plan`, `review_packet`, and
  `agent_backed_tool` for their matching workflows.

Use direct script commands only for no-MCP recovery, hooks, CI, package or
prompt validation, and MCP debugging:

```bash
skills/spec-lifecycle-manager/scripts/spec_runtime.py scan .
skills/spec-lifecycle-manager/scripts/spec_runtime.py scan . --include-archived-lint
skills/spec-lifecycle-manager/scripts/spec_runtime.py prompts .
skills/spec-lifecycle-manager/scripts/spec_runtime.py hook spec-file-changed --changed-files docs/specs/013-example-active-spec/tasks.md
skills/spec-lifecycle-manager/scripts/spec_runtime.py hook implementation-task-complete --spec-path docs/specs/013-example-active-spec --task-id T009
skills/spec-lifecycle-manager/scripts/spec_runtime.py hook spec-close-check --spec-path docs/specs/013-example-active-spec --severity-profile blocking
```

Review packet type values are canonical packet IDs, not free-form workflow
phases. If omitted, `review_type` defaults to `design_requirements_trace`.
Implementation-style aliases such as `implementation` and
`implementation-readiness` map to `implementation_review`; unknown non-empty
values map to `generic_review` and are preserved in the returned packet as
`requested_review_type`.

Only run package-specific commands against an active package returned by
`scan`. If scan reports no active specs, use durable docs and history indexes
for context instead of substituting a removed package path.

The MCP tools and CLI helpers are advisory runtime surfaces, not replacements
for lifecycle judgment. Use their structured results as evidence for
reconciliation, task selection, lint findings, and closure blockers.

Use an Agent Readiness Contract before handing work to a worker agent or
starting a non-trivial implementation slice. The contract is distinct from
`ready_to_implement`: a task can be logically implementable but still not
`ready_for_agent` if context, permissions, validation, review, or durable-doc
impact are unclear. The contract should name:

- scope: selected task or requirement, risk level, likely affected files, and
  explicit out-of-scope files;
- context: must-read artifacts, optional artifacts, durable sources of truth,
  historical or stale documents not to treat as current, and refresh points;
- validation: required commands, expected pass/fail signal, manual proof,
  evidence location, and residual risk;
- permissions: allowed edits, forbidden edits, external services, secrets, and
  human approval points;
- review: required packet type, fresh-context review need, and
  security/privacy review need;
- closure impact: durable docs affected, backlog/roadmap/issue routing, and
  release-note expectation;
- optional repo evidence: provider name, freshness, confidence, capability,
  evidence kinds, diagnostics status, validation-plan status, skipped evidence,
  and residual risk when Agent Workbench or an equivalent provider is used.

Missing contract fields are readiness gaps. Do not pad them with generic
advice.

Apply context-budget rules when building readiness packets or implementing
tasks:

- prefer `task_context`, `traceability_lookup`, and linked sections over
  loading every artifact;
- read the smallest complete set of source artifacts needed for the selected
  slice;
- avoid archived specs unless the user asks for historical audit or
  restoration;
- refresh context at phase boundaries, after upstream artifact changes, and
  before validation or closure claims;
- keep optional repo-evidence providers advisory. They can guide routing and
  validation planning, but cannot prove completion, promotion, closure, or
  governance override.

Agent Workbench, when present, is also an optional repository-evidence provider,
not a lifecycle authority or required dependency. Use Workbench-style evidence
for repo freshness, context routing, impact analysis, diagnostics, and
validation-plan suggestions only when available and relevant. Do not let
Workbench decide completion, durable-doc promotion, spec closure, governance
overrides, or human approval points. When Workbench or an equivalent tool
affects confidence, record freshness, capability, skipped evidence, diagnostics
status, validation-plan status, and residual risk using
`references/agent-workbench-evidence-boundary.md`.

Sparse or surprising Workbench search output is inconclusive. Do not report
that authoritative docs, code, or contracts are absent just because
`docs_search`, `context_for_task`, symbol search, or another ranked routing
surface missed them. State that the provider query was sparse or partial, then
pivot to repository instructions, durable indexes, targeted file inventory, and
direct reads of likely source files before making absence, implementation,
drift, or root-cause claims.

`agent-backed-tool` is also advisory and read-only. The current runner
implementation is a disabled stub: it builds the bounded review packet and
returns a structured `unavailable` result instead of invoking a secondary
process. Treat that result as confirmation that the packet and runner contract
are available, not as a completed review. A local Codex CLI adapter is a
deferred future runner candidate and must remain opt-in when added.

When an agent-backed review result is produced or manually recorded during
dogfooding, persist it under the repository's review documentation area. For
this repository, use `docs/reviews/spec-lifecycle-manager/`. Keep accepted
recommendations as lead-agent actions with evidence; route incomplete or risky
findings to backlog, roadmap, a follow-up spec, or human decision instead of
silently accepting them.

Do not add write-capable agent-backed tools inside an active implementation
slice unless a separate explicit spec defines sandboxing, permissions, review,
rollback, and evidence requirements.

When this skill's `scripts/spec_mcp_server.py` helper is available, configure
it as a local stdio MCP server for clients that support MCP:

```bash
python3 skills/spec-lifecycle-manager/scripts/spec_mcp_server.py /path/to/repo
python3 plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/scripts/spec_mcp_server.py /path/to/repo
```

The MCP server exposes shared lifecycle internals as resources, tools, and
prompts. Most tools are read-only. Write-capable tools are narrow,
preview-first exceptions: `set_task_state` is limited to one selected task block
in an active spec package `tasks.md`, while `closure_apply` and
`closure_resolve` are limited to previewed closure-record, package-cleanup, and
cleanup-hash resolution actions. These tools default to dry-run and require
explicit write intent for mutation. Do not expect the MCP server to create
specs, approve durable promotion, accept residual risk, make final closure
decisions, or commit. Use the Skill for lifecycle judgment and the MCP server,
when visible, for structured context and deterministic checks.

When this skill's `scripts/codex_spec_lifecycle_hook.py` helper is installed
as a Codex `PostToolUse` hook, it provides advisory checks for changed spec
packages, task evidence, and templates after write tools. It should stay
advisory-only during dogfooding: quiet on pass, additional context on findings,
and no blocking behavior.

Before choosing the slice, compare task checkboxes, subtasks, acceptance
criteria, and evidence against actual code, tests, config, and durable-doc
evidence. Call out status-stale candidates when validation or review is the
current goal.

For non-trivial implementation, also check durable-doc readiness before editing:
identify the authoritative durable docs for the area, whether they describe
current or planned behavior, any code-derived contracts that override prose,
which docs must be updated if the change succeeds, and which docs are out of
scope. Use `references/durable-document-contract.md` when the repository lacks
its own durable-doc contract or when durable docs are ambiguous.

Before editing, state:

- selected task IDs or requirement IDs;
- spec artifacts consulted and the relevant details they add;
- files or doc classes likely affected;
- validation expected;
- any unresolved decision that blocks implementation.

Task status rules:

- Before starting an implementation slice, mark the selected task or subtask
  `[~]` and preserve any dependency, acceptance, and evidence fields.
- Check off a parent task only when its acceptance criteria are met.
- Prefer passing tests before marking implementation tasks `done`.
- If automated tests do not apply, record the alternate verification method and residual risk.
- If validation could not run, do not hide that. Check off the parent task only when it can be defensibly verified without that validation.
- Update task `Evidence` when a task is checked complete; evidence can be a command, test result, review note, screenshot, log, commit, or manual verification note.
- Mark a task or subtask as partial, on hold, error, or skipped only with a
  documented reason (remaining work, blocker, error needing intervention,
  intentional deferral, superseded, or out of scope).

If an implementation slice fails, make one meaningfully different recovery
attempt when that is safe and in scope. If recovery also fails, stop and record
the task state, blocker, exact error evidence, attempted recovery, and the
specific decision or input needed. If the recovery produces a reusable lesson,
offer a durable gotcha, runbook, troubleshooting note, backlog item, roadmap
item, or follow-up spec destination.

When stale, missing, ambiguous, or conflicting instructions cause repeated
agent failure or user correction, treat that as instruction-as-code evidence.
Classify the failure before routing it, using stable categories such as
misunderstood requirement, missed durable source, stale spec followed,
insufficient validation, over-broad implementation, invented behavior,
dependency or environment failure, context overflow or noise, unsafe tool use,
review missed defect, documentation promotion missed, routing evidence treated
as proof, or planned validation treated as completed validation. Do not mutate
`AGENTS.md`, durable docs, backlog, roadmap, or specs automatically; route the
candidate change for lead-agent or human acceptance.

Durable agent directives, when created or promoted, must be derived from actual
repository docs, code patterns, governance, or user-confirmed principles. Keep
directives concise and route details to the durable source document. Do not
invent architecture, conventions, or coding directives for a blank repository.

Persisted review or audit findings should use stable finding IDs and preserve
history. A finding record should keep status, severity or impact, effort where
useful, source evidence, recommended routing, resolution or deferral evidence,
and whether it is findings-only or implementation work. When extending a
review, append new IDs without renumbering existing findings.

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

Durable docs are the shared source of truth for human and AI developers. They
should be readable by humans and usable by agents: current-state labels,
invariants, interfaces or contracts, validation signals, change rules, and
links to related code, tests, specs, backlog, roadmap, or ADRs. `AGENTS.md`
should point agents to these sources and workflow constraints; it should not
duplicate durable architecture, requirements, design, API contracts, or
runbooks.

Common routing:

- requirements, non-goals, and acceptance criteria -> the repo's accepted requirements, product, contract, test, or reference docs;
- technical design -> the repo's durable design, architecture, decision, or reference docs;
- rollout and operational steps -> the repo's runbook, getting-started, deployment, or support docs;
- data, schema, API, config, or integration behavior -> the repo's contract, data-flow, schema, config, or integration docs;
- lasting decision rationale -> the repo's decision record or durable history format;
- temporary research -> durable decision, reference, review, or discard when no longer useful;
- deferred work -> backlog, roadmap, issue tracker, or a smaller follow-up spec.

Route deferred work by readiness:

- use backlog when work is useful but lacks enough scope, acceptance criteria,
  owner, or timing to become active implementation work;
- use roadmap when work affects sequencing, milestones, adoption stages, or
  dependencies across specs, repositories, or releases;
- use the repository's issue tracker when issues are the authoritative planning
  system or when the work needs external assignment, labels, or project-board
  tracking;
- create a smaller follow-up spec when the work is ready to implement and has
  clear requirements, design direction, acceptance criteria, and validation
  expectations.

Record one primary destination for each deferred item. Add cross-links where
useful, but do not leave the same work ambiguously active in multiple places.

Promotion should produce an explicit durable-doc map before closure:

- spec content promoted;
- durable destination path or documented deferral;
- evidence that the destination now reflects current behavior;
- residual spec-only content, if any, and why it remains.

Read `references/document-routing-and-expert-review.md` when document routing or review roles are material to the task.
Read `references/durable-document-contract.md` when creating, promoting, or
reviewing durable docs, especially when a repository has no authoritative
template system or when current and planned behavior are mixed.

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
- unresolved work is moved to backlog, roadmap, issue tracker, or a follow-up
  spec;
- indexes no longer present the package as active implementation work.

When requirement priorities are present, closure review must preserve their
scope semantics. Accepted `must-have` requirements with missing coverage block
closure unless explicitly rejected or superseded by a human decision.
Unimplemented `should-have` requirements need a route, rationale, or accepted
residual risk. Unimplemented `could-have` requirements may close only when
routed, rejected, or marked out of current scope. Missing priority uses legacy
compatibility behavior and is not a blocker by itself.

If the repository uses a spec closure log, or no repository-specific closure
record exists and this skill's fallback lifecycle is being used, closing must
also preserve a durable closure breadcrumb. The fallback closure log path is
`docs/history/spec-closure-log.md` with `doc_type: history`.

Before closing, perform a final spec cleanup check:

1. Re-read `requirements.md`, `design.md`, `tasks.md`, `change-impact.md`,
   `verification.md`, `quickstart.md`, `research.md`, and `open-decisions.md`
   if present.
2. Classify each lasting element as promoted, explicitly deferred, discarded, or
   retained as history.
3. Confirm any spec-local canonical context has been promoted, routed to
   backlog/roadmap/follow-up spec, or discarded with rationale.
4. Confirm durable destinations exist and are linked from the relevant indexes.
5. Confirm active docs no longer point readers to the spec as the source of
   current behavior.
6. Decide the package disposition according to the target repository's document
   lifecycle. Prefer `removed` after durable promotion; use `archived` or
   `retained-as-history` only when explicit repository policy requires visible
   historical spec packages.
7. Update active spec indexes, sequencing docs, task boards, or README entries
   so the package no longer appears active.
8. Require a final spec commit hash that contains the complete final package
   before removal. Do not remove the package when that commit is missing.
9. Add or update the repository's closure record with spec ID, title, closed
   date, final spec commit, closure action, durable destinations,
   verification summary, residual risks, and follow-up work.
10. Record closure evidence in `verification.md`, the closure log, or the
   repository's chosen closure record.

Use these closure actions consistently:

- `removed`: deleted from the active tree after the final spec commit records
  the full package;
- `archived`: moved to an archive/history path because explicit repository
  policy requires visible historical docs;
- `retained-as-history`: kept in place or nearby by explicit exception and
  clearly marked historical, archived, or superseded.

When reporting closure, include the final spec commit, closure cleanup commit
if known, durable docs updated, closure action, residual risks, and follow-up
destinations.

Do not leave completed behavior documented only in `docs/specs/`. If durable
promotion is blocked, keep the spec open or create a follow-up with an explicit
owner, destination, and closure blocker.
