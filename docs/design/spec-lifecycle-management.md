---
title: Spec lifecycle management
doc_type: design
status: active
owner: platform
last_reviewed: 2026-07-19
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

Durable docs are also the shared development interface between human developers
and coding agents. They should combine human-readable rationale with
agent-usable structure: stable metadata, current-state labels, invariants,
interfaces, validation signals, change rules, and links to related code, tests,
contracts, backlog, roadmap, and specs.

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
  with optional requirement-level MoSCoW priority, EARS acceptance criteria,
  correctness properties, technical context, and success criteria.
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
- `traceability.md`: optional bidirectional matrix for task, requirement,
  acceptance-criteria, design, durable target, verification, open-decision, and
  correctness-property coverage when task text alone is not enough.
- `canonical-context.md`: optional working-context map for broad or
  durable-doc-impacting specs, imported durable sources, stale-doc risk, or
  resumed specs where older docs may otherwise be mistaken for implementation
  authority. Missing canonical context is advisory unless a repository policy
  makes it blocking; small packages can embed equivalent durable-source and
  promotion context in core artifacts.

The core package files are required because their intent is required, not
because every concern deserves its own file. A small package should embed
durable-source baseline, durable-document impact, verification expectations,
traceability links, open decisions, and promotion targets inside
`requirements.md`, `design.md`, or `tasks.md` when separate supporting files
would add ceremony without reducing risk.

Separate supporting artifacts are justified when they reduce ambiguity:

- create `canonical-context.md` when the active package imports, adapts,
  supersedes, or classifies durable docs for the implementation slice and that
  context materially reduces current implementation ambiguity;
- create `change-impact.md` when existing durable behavior changes across
  several documents, contracts, or migration paths;
- create `verification.md` when validation has multiple gates, environments,
  residual risks, waivers, or release/closure evidence;
- create `traceability.md` when task text alone is not enough to map work back
  to requirements, acceptance criteria, design, durable docs, and decisions;
- create `open-decisions.md` when unresolved decisions need ownership and
  blocking status outside a single design section;
- create `research.md` or `quickstart.md` only when investigation or temporary
  operator/developer instructions need a clear home before promotion or
  discard.

`spec.md` is an old-format compatibility artifact, not a current core file. An
existing `spec.md` may be useful as a feature brief or migration input, but it
should not duplicate current `requirements.md`, `design.md`, or durable docs.
When an active package contains `spec.md`, reconciliation should classify it as
feature brief, migration input, or deprecated duplicate before implementation
continues.

## Staged Flow And Readiness

The default flow is staged: discover repository context, write or update
requirements, draft design, create traceable tasks, implement one coherent task
slice, validate, promote accepted behavior to durable docs, and close the spec.
Design-first work is allowed only as an explicit exception: record partial
requirements and require a later requirements completion step before
implementation readiness.

For an already selected active-spec task, the declarative
`implementation-start` MCP prompt is the concise entry point. It composes
active preflight, task context, traceability, agent and stage readiness, and
validation planning from their existing authoritative tools. It is read-only:
it preserves every source blocker, does not change task state, and does not
treat planned validation as completed evidence. `developer-start` remains the
first-run repository-orientation prompt.

First-run guidance starts with `lifecycle_guide` through MCP or the
`lifecycle-guide` CLI command. It reports repository classification, docs
readiness, template authority, available lifecycle tooling, active-spec
readiness, bootstrap guidance, and next actions. When a repository is blank or
near blank, `bootstrap_plan` previews minimal lifecycle docs and an optional
first spec package. Bootstrap planning is preview-only and must not invent
architecture, coding patterns, or agent directives for a repository that lacks
evidence or user-confirmed principles.

`stage_readiness` is the stage gate before implementation. It reports required
artifact state, optional traceability and verification artifacts, downstream
review needs, context-budget gaps, correctness-property mappings, acceptance
criteria coverage, and Agent Readiness Contract status. Requirements changed
after design or tasks, or design changed after tasks, should trigger downstream
review rather than silent artifact rewriting.

`phase_gate_check` is the read-only decision facade across the full delivery
lifecycle. It reports one of eight public phases: `requirements`, `design`,
`tasks`, `implementation`, `verification`, `promotion`, `closure`, or
`unknown`. The shared core remains caller-agnostic; MCP and CLI adapters add
invocation provenance without changing the lifecycle decision. Existing lint,
task, validation, promotion, and closure tools remain the authoritative
diagnostic and expansion surfaces.

Advancement is conservative. Missing or stale upstream review, unresolved
blocking decisions, missing verification or promotion proof, and runnable
implementation tasks keep `ready_to_advance` false. In particular, a runnable
task produces `PHASE_GATE_TASK_REMAINS` and a `continue_task` action rather than
allowing the presence of implementation evidence to imply readiness.

Downstream artifacts may carry an `Upstream Fingerprints` table that records
normalized content fingerprints for requirements or design inputs. The gate
reports `current` when recorded and observed fingerprints match, `stale` when
they differ, `review_required` when no usable record exists, and
`not_applicable` before the downstream artifact is relevant. Modification time
is never proof of semantic currency or staleness, and v1 does not write these
records.

The aggregate supports compact, full, and closed-section views plus
fingerprint-guarded expansion. It orders mandatory blockers before advisory
findings while bounding compact output to 20 findings, 10 actions, and a 32 KiB
target; explicit truncation state and expansion expose omitted detail. An
expansion whose expected fingerprint no longer matches returns a stale response
with refreshed arguments instead of presenting new evidence as the referenced
result.

Shared next-action presentation follows the lifecycle order rather than
inferring completion from implementation evidence: plan and execute validation,
review evidence quality, route durable promotion, then run closure checks.
Agent-facing actions name MCP tools first. Direct runtime commands are kept in
a separately labelled validation-or-recovery branch for CI, hooks, debugging,
or explicit recovery when MCP is unavailable.

Capability reporting describes server availability independently from optional
client observation. A server with its stable tool surface available reports
`ready`; absent client identity is informational and has no lifecycle impact.
When supplied during MCP initialization, only the standard client name,
version, negotiated protocol, and allowlisted structural capabilities are held
in process memory. Client identity is neither persisted nor used to select
lifecycle actions.

`spec_creation_plan` uses the same aggregate contract for provisional creation
decisions. Its compact default preserves allocation status, confidence, proposed
ID and path, collision blockers, bounds, and deterministic expansion. Callers
can request bounded `full` output or the closed `numbering`, `template`, and
`validation` sections. MCP and CLI adapters attach their own invocation
metadata while the shared allocation and creation logic remains caller-agnostic.

Spec numbering is runtime-owned rather than agent arithmetic. The read-only
`spec_id_inventory` surface selects one docs root and combines active,
archive-index, closure-log, retained, and explicit legacy-range evidence. It
returns a provisional number above the greatest valid prefix or range upper
bound, never fills lower gaps, and reports reduced or low confidence for
malformed, duplicate, missing, or ambiguous history. Empty scopes return the
bootstrap-compatible `000`.

`spec_creation_plan` composes that allocation with a caller-supplied ASCII
lower-kebab slug, path-ancestry proof, selected-root/repository/skill template
precedence, artifact inventory, required values, validation commands, and a
`spec-creation-plan-v1` fingerprint. It is preview-only and does not reserve an
ID. Stale evidence or collision returns refreshed arguments and a fresh
proposal; a future writer must atomically claim the directory.

Correctness properties and acceptance criteria are part of readiness, not
closure-only paperwork. Each stable correctness property should map to design
behavior and at least one task plus automated or documented manual
verification. Acceptance criteria should be mapped explicitly in
`traceability.md` or equivalent task/verification evidence. Repositories do not
need to add a new property-test dependency just to satisfy the lifecycle; use
the project’s accepted test framework or documented manual verification when
that is the right validation path.

Requirement priority is optional requirement-level metadata. New specs may use
`**Priority:** must-have`, `**Priority:** should-have`, or
`**Priority:** could-have` directly under the user story. Acceptance criteria
inherit their parent requirement priority; the lifecycle does not require
duplicate criterion-level labels. Missing priority remains compatible for
existing specs. Excluded scope belongs in non-goals, out-of-scope text,
rejected decisions, or routed residuals rather than a persisted `won't-have`
accepted requirement. When priority is present, readiness and closure
reconciliation preserve the scope semantics: uncovered `must-have`
requirements block unless explicitly rejected or human-superseded,
`should-have` gaps need route or residual-risk rationale, and `could-have` gaps
may close only when routed, rejected, or marked out of current scope.

The Agent Readiness Contract is distinct from `ready_to_implement`. It gives a
worker agent bounded context: selected task or requirement, likely affected
files, out-of-scope files, must-read context, optional context, durable sources
of truth, stale documents to avoid, permission boundaries, validation commands,
review expectations, and closure impact. A package can be `ready_for_agent`
while still not `ready_to_implement` if lead-agent work remains, such as
traceability repair, downstream review, or durable-doc promotion planning.

Context-budget discipline keeps implementation slices small. Prefer
`task_context`, `traceability_lookup`, and `agent_readiness_packet` over loading
every spec and durable document. Avoid archived specs unless doing a historical
audit, and refresh context at phase boundaries: after requirements changes,
after design changes, before implementation, and before closure.

For broad or durable-doc-impacting work, the active spec may define
spec-local canonical context. That context is the package-local set of working
sources agents should read first for the implementation slice. It can be a
separate `canonical-context.md` artifact or clearly labeled embedded sections
in core artifacts for small packages. Spec-local context does not override
system, developer, or user instructions, `AGENTS.md`, governance, policy,
security, generated contracts, source-code contracts, tests, or live/system
evidence. Durable docs not imported, adapted, or explicitly referenced by the
active spec remain background or drift evidence when they conflict with the
declared working context.

Optional repository-evidence providers such as Agent Workbench can contribute
freshness, diagnostics, impact, and validation-plan signals. Their output is
routing evidence only; it is not lifecycle authority, proof of task completion,
durable-doc promotion, spec closure, or governance override.

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
| `docs/roadmap/` | Sequenced lifecycle work, milestones, adoption stages, and multi-spec dependencies. |
| `docs/reviews/` | Analysis snapshots and evidence that may feed specs or durable docs. |
| `docs/specs/` | Temporary active delivery packages and optional documented subsystem spec locations. |

Repositories may use different folder names. The lifecycle still applies: identify each repository's durable doc classes before implementing from a spec.

Durable docs describe current accepted state by default. Intended future state
belongs in active specs, backlog, roadmap, ADR proposals, or explicitly marked
proposed/deferred sections. If a durable document intentionally contains future
intent, it must be labeled so agents and tools do not treat it as current
implementation guidance.

Use the Durable Document Contract in
`skills/spec-lifecycle-manager/references/durable-document-contract.md` when a
repository lacks its own durable-doc template system or when reviewing whether a
document is usable by both humans and agents. The contract is guidance for
quality and routing; it does not require every project to create every durable
doc class.

## Durable Source And Delta Rules

The durable source of truth should always be referenced from an active spec. If
the change modifies existing behavior, the spec should identify the current
durable docs, contracts, schemas, runbooks, or code-derived references that
describe that behavior.

An active spec should also state its durable-document impact: which durable
requirements, design, architecture, API/contract, data-flow, runbook,
verification, reference, ADR, backlog, or roadmap documents it adds to,
modifies, clarifies, supersedes, or leaves unchanged. This mapping may live in
`requirements.md` for small work or in `change-impact.md` when the impact spans
several durable docs or behavior classes.

Use `change-impact.md` when the work changes existing behavior, including bug
fixes. The change-impact record should classify each delta as add, modify,
remove, rename, bug fix, or clarify, and map each delta to the durable document
that must be updated before closure.

If no durable source exists for behavior that should be stable, record that as
a documentation gap and assign a durable promotion target.

Before implementing non-trivial work, perform a durable-doc readiness check:
identify authoritative docs, whether they describe current or planned state,
which code-derived contracts override prose, which durable docs must be updated
if the change succeeds, and which docs are explicitly out of scope.

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

Migration guidance must stay current with released lifecycle improvements. When
the skill adds new task-state markers, validation semantics, closure checks,
artifact rules, or durable-document integration rules, update the migration
guide in the same release slice so old packages can be upgraded without
guesswork.

Archived, closed, or superseded packages are historical delivery records. They
should remain visible to inventory and closure-log workflows, but default
active-health scans should not require them to satisfy newer authoring lint
templates. Agents should use explicit lint or archived scan audit mode when
reviewing historical packages, and should only modernize them after a visible
resumption, migration, or cleanup decision.

## Runtime Support

The `spec-lifecycle-manager` skill includes a dependency-free CLI runtime for
deterministic lifecycle checks:

```text
skills/spec-lifecycle-manager/scripts/spec_runtime.py
```

The runtime provides JSON outputs for spec scanning, summary resources, linting,
next-task selection, task context, traceability lookup, lifecycle guidance,
bootstrap planning, stage readiness, closure checks, prompt-definition
validation, reconciliation, promotion planning, review-packet generation,
review-result disposition validation, disabled agent-backed tool execution, and
hook checks. These outputs are advisory runtime surfaces; they do not replace
the skill, repository governance, or durable documentation. The old standalone
`traceability_lookup.py` script has been migrated into MCP and shared runtime
internals; agents should use the MCP `traceability_lookup` tool or
`spec_runtime.py` task-context/next-task outputs instead of calling a separate
script.

Closure-helper write surfaces are explicit exceptions to the read-mostly MCP
model. MCP remains the preferred agent-facing interface for `closure_plan`,
`closure_apply`, and `closure_resolve`, while retained `spec_runtime.py`
commands exist for validation, CI, debugging, and no-MCP recovery. Mutating
closure actions must be generated by a previewed plan, named by action ID,
limited to declared closure targets, and guarded by explicit write intent.
Lifecycle judgment, durable-promotion approval, residual-risk acceptance, final
closure approval, and Git commits remain outside MCP automation.

The guided documentation wizard is a prompt-based workflow layered over those
runtime surfaces. It is exposed as the `documentation-wizard` prompt rather
than as a new parser, autonomous loop, or write-capable MCP tool. The prompt
guides requirements, design, tasks, agent-readiness, verification, promotion,
and closure one bounded question at a time by default. Checklist mode is an
explicit user-requested exception.

The wizard must gather lifecycle context with existing read-only surfaces such
as lifecycle guide, active preflight, no-active-spec context, stage readiness,
task context, traceability lookup, promotion plan, and closure check. It reports
the current stage, selected spec or selection need, next bounded question,
expected answer shape, open questions, feedback dispositions, preview edit
plan, readiness signal, durable destinations, recovery commands, and residual
risk.

Open questions reported by the wizard include why the question matters,
affected stage, candidate answer format, blocking status, and artifact
destination. Feedback is routed through one primary disposition: accept,
revise, defer, reject, or human decision required. The wizard must not report a
spec ready to implement while blocking questions, missing downstream review, or
stale artifact dependencies remain.

All proposed changes remain preview-first. A preview edit plan must identify
repo-relative path, target section, change type, and rationale before ordinary
file edits are made. Removed packages remain historical evidence through the
closure log and archive index; the wizard must not present them as active
implementation targets.

Agent-backed tool execution starts with a disabled runner interface. The runtime
builds bounded packets and returns structured `unavailable` output until an
explicit runner adapter is configured. A local Codex CLI adapter is the first
deferred runner candidate, but it must remain opt-in and non-mutating when
added. Any write-capable agent-backed tool requires a separate spec that covers
sandboxing, permissions, review, rollback, and evidence.

During early dogfooding, persisted review outputs should live under
`docs/reviews/spec-lifecycle-manager/`. These records are analysis snapshots:
they can inform specs, backlog, roadmap, durable docs, or human decisions, but
they do not become source-of-truth behavior by themselves.

Scan output is active-health oriented by default. Archived packages remain in
the scan inventory with archived lifecycle metadata, while their current
authoring lint is skipped unless the caller explicitly requests archived lint
audit mode.

See [Spec lifecycle runtime](../reference/spec-lifecycle-runtime.md) for the
current command surface and hook modes.

### Public inspection CLI boundary

The release package exposes `slm` as its sole executable. The Node dispatcher
owns package-level routing: `slm install` calls the package installer in-process,
while every inspection command resolves Python through the package interpreter
contract and launches the bundled standard-library `slm_cli.py` with an argument
vector and no shell. Bare `slm` routes to `specs`.

The preferred public query vocabulary is `spec`: `slm spec` defaults to active
inventory; the `all`, `open`, and `closed` selectors choose an inventory scope;
and the `tasks`, `next`, and `requirements` actions inspect one active spec. The
plural `specs`, `tasks`, `next`, `requirements`, and `history` commands remain
compatible routes. All forms are read-only projections over the same lifecycle
parsers and selectors. The singular parser normalizes to existing builders;
shared projection functions produce normalized records first, and plain-text
tables and the versioned JSON envelope render those same records so filtering,
ordering, identity, and state cannot diverge by vocabulary or output mode.
Historic records come from the validated closure log and archive index,
including removed packages.

Active spec records also project task-backed phase progress. The public view
uses the shared task parser and task-to-phase mapping, counts a phase complete
only when all assigned tasks are complete, and selects the first incomplete
phase in document order as current. Phase state is one of the existing
normalized task states, chosen by a documented deterministic precedence; it is
not a second persisted lifecycle model. Specs without explicit task-backed
phases expose no phase progress or state.

Keep the three command boundaries distinct:

- `slm` is the public, packaged, read-only lifecycle inspection surface plus
  the explicit `install` action.
- `slc` is checkout-only maintainer orchestration for validation, bundle sync,
  package, install-test, and release workflows. It is not an npm bin.
- MCP is the preferred structured agent interface for context, lifecycle
  judgment, guarded state changes, promotion, and closure.

The public CLI must not introduce independent meanings for task markers,
requirements priorities, spec resolution, next-task selection, archive
validity, or lifecycle health. Changes to those contracts start in shared
lifecycle code and must update CLI tests, the bundled Codex and Claude copies,
the runtime reference, package contract, and installed-tarball smoke.

## Implementation Rules

- Implement one coherent task slice at a time, usually one phase or checkpoint from `tasks.md`.
- Do not implement from `tasks.md` alone. Task entries are an execution index;
  agents must review the relevant requirements, acceptance criteria, design,
  change impact, verification expectations, durable-source baseline, and open
  decisions before coding.
- If task wording is broad or vague, resolve its concrete implementation
  meaning from the full spec package before treating it as blocked or
  non-implementable.
- Prefer independently testable user-story slices over broad task batches.
- Map tests and validation back to requirement IDs, acceptance criteria, success criteria, or task IDs where practical.
- Preserve correctness-property IDs through requirements, design,
  traceability, tasks, and verification where the spec defines them.
- Update the selected task to `[~]` before starting implementation so resumed
  sessions can see what is in progress.
- Update task status only when the recorded marker matches the actual state:
  `[ ]` pending, `[~]` in progress, `[/]` partial, `[>]` follow-up or routed,
  `[-]` no-op or deferred, `[?]` review or decision needed, `[!]` attention
  needed, and `[x]` complete. Legacy `[Y]`, `[*]`, and `[e]` markers remain
  readable during migration but should not be used for new task updates.
- Prefer passing tests before marking implementation tasks `done`.
- Record task evidence before marking a task `done`.
- If a task is not testable, blocked from local validation, or verified by inspection or documentation review instead of automated tests, record the verification method and residual risk.
- Use numbered findings for reviews and audits that may become work. Preserve
  the original finding ID, status, severity or impact, evidence, routing, and
  resolution or deferral notes instead of renumbering older findings.

## Verification Rules

Before promotion, release, or closure, record validation evidence and residual
risk. Verification may live in `verification.md`, task evidence fields,
checklists, review records, or durable docs depending on the repository's
structure.

Verification should map evidence back to task IDs, requirements, acceptance
criteria, and success criteria where practical.

Recovery evidence is part of verification. When a task fails, record the exact
error and at least one meaningfully different recovery attempt before declaring
a blocker. If recovery succeeds and the lesson is reusable, route it to a
durable gotcha, runbook, troubleshooting note, backlog item, roadmap item, or
follow-up spec. Learning-loop findings should classify the failure, for example
misunderstood requirement, missed durable source, stale spec followed,
insufficient validation, over-broad implementation, invented behavior,
environment failure, context noise, unsafe tool use, review missed defect,
documentation promotion missed, routing evidence treated as proof, or planned
validation treated as completed validation.

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
| Deferred implementation work lacking scope or acceptance criteria | Backlog. |
| Deferred sequencing, adoption, milestone, or multi-spec dependency work | Roadmap. |
| Deferred work ready for implementation | Issue tracker item or smaller follow-up spec. |

Do not leave completed behavior documented only in `docs/specs/`.

Durable promotion should also check that lasting facts have a source of truth:
current behavior in durable docs or code-derived contracts, intended future
work in backlog/roadmap/issues/follow-up specs, and historical evidence in
closure logs, reviews, or archive indexes.

## Backlog And Roadmap Routing

Backlog and roadmap documents are durable planning surfaces, not active
implementation specs and not product changelogs. Use them to keep deferred
work visible without treating every idea as ready-to-build work.

Use backlog for proposed, accepted, deferred, or dropped work that needs
clarification before implementation. Backlog entries should stay concise and
link to their primary destination when promoted.

Use roadmap for sequencing, milestones, adoption stages, or dependencies that
span multiple specs, backlog items, repositories, releases, or operational
rollouts. Roadmap items should include exit criteria and evidence links.

Use a follow-up spec or issue tracker item when deferred work has clear scope,
acceptance criteria, and validation expectations. Repository-specific planning
systems remain authoritative; the fallback durable templates are optional when
no project template exists.

## Closure Criteria

A spec can be closed when:

- implemented code, tests, config, and migrations are complete or explicitly deferred;
- verification evidence and quality gates are complete or explicitly waived with residual risk;
- durable docs describe the resulting current behavior;
- API, data-flow, runbook, reference, and ADR updates are complete where relevant;
- task state is accurate;
- unresolved work is moved to backlog, roadmap, issue tracker, or a follow-up
  spec;
- the docs index no longer presents the spec package as current behavior or
  active implementation work.

Closure should remove the completed spec package from the active docs tree
after durable promotion. Moving or retaining a visible historical package is an
exception that requires repository-specific archive policy or an explicit
decision.

## Closure Log And Git-Backed Archive

Use a durable spec closure log as the breadcrumb to Git history for completed
spec packages removed from the active docs tree. The fallback closure log path
is:

```text
docs/history/spec-closure-log.md
```

Use `doc_type: history` for the fallback closure log. Repositories with their
own changelog, archive, compliance, or issue-tracking records remain
authoritative; record that template authority decision before adopting the
fallback.

Use this two-commit close flow when removing a spec package:

1. Complete durable promotion and verification.
2. Commit the final spec state while the full package is still present.
3. Record that final spec commit in the closure log.
4. Remove the package, or archive/retain it only when explicit policy requires
   visible historical docs.
5. Update active indexes so the package is no longer presented as current work.
6. Commit the cleanup separately.

When archive-index support is available, also record closed spec package state
in:

```text
docs/history/spec-archive-index.md
```

The closure log is the narrative history. The archive index is the compact
lookup surface for package path, final spec commit, cleanup commit, closure
action, durable destinations, and verification reference. If a package is
removed, the final spec commit must identify a commit that still contains the
completed package before removal.

Closure actions:

| Action | Meaning |
| --- | --- |
| `removed` | Spec package was deleted from the active tree after the final spec commit recorded the full package. |
| `archived` | Spec package was moved to an archive/history path because explicit policy requires visible historical docs. |
| `retained-as-history` | Spec remains in place or nearby by explicit exception and is clearly marked historical, archived, or superseded. |

Active indexes should list active specs only. They may point readers to the
closure log or archive index, but they should not list completed spec packages
as current work or become a complete closed-spec history.

Spec closure logs are implementation-lifecycle records. Product or release
changelogs may use them as input, but changelogs do not replace closure
records because they serve a different audience.
