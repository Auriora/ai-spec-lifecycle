---
title: Task state management tools requirements
doc_type: spec
artifact_type: requirements
status: active
owner: platform
last_reviewed: 2026-06-13
---

# Requirements

## Durable Source Baseline

- `skills/spec-lifecycle-manager/SKILL.md` defines task checklist conventions,
  evidence expectations, and the rule to mark selected work in progress before
  implementation.
- `skills/spec-lifecycle-manager/scripts/spec_runtime.py` parses task markers
  and exposes `next_task`, `spec_summary`, hook checks, and closure checks.
- `skills/spec-lifecycle-manager/scripts/traceability_lookup.py` resolves task
  context from `traceability.md`.
- `docs/reference/spec-lifecycle-runtime.md` documents the runtime, MCP tools,
  and advisory hooks.
- Spec 065 in the aws-datalake repository exposed a process gap: broad
  verification tasks were marked complete after classification or documentation
  updates while follow-up implementation, staging validation, or no-op routing
  still needed explicit task ownership.
- Specs 023 and 048 in the aws-datalake repository exposed a second gap:
  unchecked tasks already had implementation evidence, downstream specs depended
  on that stale state, and later tasks could be marked complete for
  plan-only/blocked-output behavior unless the task acceptance clearly scoped
  completion to a non-mutating contract.

## Goals

- Keep task markers simple enough for developers to type in Markdown.
- Prefer symbols over new letter markers where the state is commonly edited by
  developers.
- Add task-management tools that list open work, show traceability-backed task
  detail, audit suspicious completion states, and update task state with
  evidence.
- Add low-noise hook guidance that catches stale or contradictory task state
  without nagging on every tool call.
- Strengthen skill guidance so broad verification tasks are split into Kiro-style
  subtasks before they hide multiple outcomes behind one checkbox.

## Non-Goals

- Do not replace Markdown `tasks.md` as the source task artifact.
- Do not create a full issue tracker, assignment system, or scheduling system.
- Do not require blocking hooks by default.
- Do not require non-keyboard glyphs for developer-authored task state.
- Do not expose general-purpose file editing through task-management tools.
  Write-capable tools are limited to spec packages and, if later accepted,
  documented durable-doc evidence fields.

## Requirements

### Requirement 1: Symbol-Based Task States

**User Story:** As a developer, I want task states that fit normal keyboard
entry, so that I can record progress, blockers, follow-up routing, and no-op
classification without inventing prose conventions.

#### Acceptance Criteria

1. GIVEN a task checklist item, WHEN the runtime parses it, THEN the system
   SHALL recognize the existing `[ ]`, `[~]`, `[Y]`, `[*]`, `[e]`, and `[x]`
   markers during migration.
2. WHERE new developer-authored states are added, THE SYSTEM SHALL prefer
   keyboard symbols and document each marker's meaning.
3. IF a task represents follow-up work created or needed outside the current
   acceptance scope, THEN THE SYSTEM SHALL support a distinct follow-up/routed
   state.
4. IF a task is intentionally no-op, raw-only, not applicable, superseded, or
   deferred from the current spec, THEN THE SYSTEM SHALL support a distinct
   no-op/deferred state with evidence.
5. IF a task is awaiting review, decision, or domain sign-off, THEN THE SYSTEM
   SHALL support a distinct review/decision state.
6. IF a task has an error, blocked condition, or intervention requirement, THEN
   THE SYSTEM SHALL support a distinct attention/intervention state.

### Requirement 2: Task Listing And Detail Tools

**User Story:** As an agent resuming a spec, I want a concise open-task view and
traceability-backed task detail, so that I do not infer status from stale
checkboxes or prose.

#### Acceptance Criteria

1. GIVEN a spec package, WHEN task listing runs, THEN the system SHALL return
   tasks grouped by phase and normalized state.
2. WHERE a task has dependencies, evidence, files, acceptance, or subtasks, THE
   SYSTEM SHALL include those fields in structured output.
3. WHEN task detail is requested for a task ID, THEN the system SHALL include the
   parsed task, parent/subtask relationships, dependency state, traceability row,
   linked requirements, verification references, durable targets, and gaps.
4. IF a task is broad enough to hide multiple outcomes, THEN the system SHALL
   report a broad-task warning with suggested subtask splits.
5. WHERE a task or traceability row references another spec, THE SYSTEM SHALL
   include cross-spec dependency health when that spec is available locally.
6. IF files, tests, or evidence indicate that a pending task may already be
   implemented, THEN THE SYSTEM SHALL report a candidate-complete finding without
   changing the marker automatically.
7. WHERE task metadata includes evidence mode, follow-up destination, decision
   owner, or upstream/downstream spec references, THE SYSTEM SHALL parse and
   return those fields in structured output.

### Requirement 3: Safe Task State Updates

**User Story:** As a maintainer, I want task state updates to preserve evidence,
so that agents cannot mark incomplete or routed work as complete by accident.

#### Acceptance Criteria

1. GIVEN a task ID, target state, and evidence text, WHEN state update runs,
   THEN the system SHALL update only that task marker and associated evidence or
   status text.
2. WHERE the target state is complete, THE SYSTEM SHALL reject the update unless
   acceptance evidence is concrete and does not contain unresolved terms such as
   pending, partial, follow-up, blocked, future, review, or not verified.
3. IF the target state is follow-up, no-op, review, or attention/intervention,
   THEN THE SYSTEM SHALL require a reason and a destination, decision owner, or
   next diagnostic step where applicable.
4. THE SYSTEM SHALL support dry-run output before writing changes.
5. WHERE the evidence is plan-only, dry-run-only, routed, blocked-output, or
   contract-only, THE SYSTEM SHALL reject direct completion unless the task
   acceptance explicitly says that evidence mode is sufficient.
6. WHERE a task-state update is invoked through MCP, THE SYSTEM SHALL require an
   explicit write intent, default to preview/dry-run, limit writes to the
   selected spec package task block, and return a before/after patch summary.
7. WHERE a write-capable tool receives a path outside an active spec package,
   THEN THE SYSTEM SHALL reject the update unless a future documented durable-doc
   evidence mode explicitly allows that document class.
8. THE SYSTEM SHALL record enough update provenance for review, including tool
   name, task ID, target state, evidence mode, changed fields, and validation
   status.

### Requirement 4: Task State Reconciliation

**User Story:** As a maintainer reviewing a resumed spec, I want task state
audited against evidence depth and upstream dependencies, so that stale
checkboxes and plan-only completions do not mislead downstream implementation.

#### Acceptance Criteria

1. GIVEN an unchecked task with concrete evidence, WHEN audit runs, THEN the
   system SHALL classify it as `stale_open` or `candidate_complete` and report
   the evidence source.
2. GIVEN a complete task whose evidence describes only a planner, dry-run,
   blocked output, or deferred path, WHEN acceptance implies implemented
   behavior, THEN the system SHALL flag a `plan_only_completion` or
   `blocked_output` warning.
3. GIVEN a task that depends on another spec, WHEN the upstream spec has stale,
   unchecked, attention, or partial tasks in the referenced area, THEN the
   system SHALL report `cross_spec_dependency_untrusted`.
4. WHERE an implementation already exists outside task evidence, THE SYSTEM
   SHALL surface discovered code/test/doc evidence separately from task state.
5. IF a task mixes multiple profiles, source families, validation surfaces,
   blocked outputs, or cross-spec alignment, THEN the system SHALL suggest
   subtasks before implementation continues.
6. THE SYSTEM SHALL expose broad-task findings through a `split_task_suggestions`
   field that agents can apply manually or route to a follow-up task.

### Requirement 5: Completion Audit And Hooks

**User Story:** As an agent, I want lifecycle hooks to catch contradictory task
state without noisy reminders, so that task evidence stays accurate during
implementation.

#### Acceptance Criteria

1. WHEN a changed `tasks.md` marks a task complete, THEN advisory checks SHALL
   flag evidence that still reads as pending, partial, follow-up, blocked,
   future, review, no-op, or not verified.
2. WHEN a session resumes or active preflight runs, THEN it SHALL summarize
   existing in-progress, review, follow-up, attention, stale-open, plan-only,
   and validation-needed tasks once.
3. IF an agent starts a new implementation task while another task is still in
   progress in the same spec, THEN the advisory hook SHALL report the existing
   in-progress task without blocking by default.
4. Hooks SHALL stay quiet when task state and evidence are consistent.
5. WHERE a preflight or resume summary includes reconciliation findings, THE
   SYSTEM SHALL collapse repeated findings by task ID and classification.

### Requirement 6: Skill And Template Guidance

**User Story:** As a spec author, I want broad task guidance and examples, so
that verification tasks are decomposed before they become ambiguous.

#### Acceptance Criteria

1. The skill SHALL say broad tasks must be split when they cover multiple source
   families, evidence types, implementation outcomes, or validation surfaces.
2. The task template SHALL show Kiro-style subtasks with mixed states for
   implementation, validation, follow-up, and no-op routing.
3. The runtime docs SHALL document the task state contract, tool commands, MCP
   surface, hook behavior, and noise policy.
4. The skill SHALL distinguish implementation completion from planning,
   contract, dry-run, classification, no-op, and blocked-output evidence.
5. The task template SHALL document optional metadata fields: `Evidence mode:`,
   `Follow-up:`, `Destination:`, `Decision owner:`, `Upstream specs:`, and
   `Downstream specs:`.

## Correctness Properties

- CP-001: Task parsing SHALL remain deterministic for the same `tasks.md`.
- CP-002: Read-only task tools SHALL never mutate spec files.
- CP-003: State updates SHALL be limited to the selected task and its evidence or
  status fields.
- CP-004: Completion audit SHALL prefer false-positive advisory warnings over
  allowing unresolved evidence to pass as complete.
- CP-005: Existing `[Y]` and `[e]` markers SHALL remain readable during migration
  even if the preferred symbols change.
- CP-006: Audit tools SHALL never silently promote stale-open or
  candidate-complete tasks to complete.
- CP-007: Write-capable task tools SHALL never modify files outside their
  declared spec/documentation boundary.
- CP-008: MCP write tools SHALL be preview-first and reject ambiguous write
  targets.

## Success Criteria

- Runtime tests cover parsing, listing, detail, broad-task audit, dry-run update,
  guarded completion, and hook diagnostics.
- MCP tests expose task listing, task detail, task audit, and task-state update
  tools.
- Skill, template, runtime docs, and bundled plugin copies are aligned.
