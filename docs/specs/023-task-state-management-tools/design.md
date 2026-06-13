---
title: Task state management tools design
doc_type: spec
artifact_type: design
status: active
owner: platform
last_reviewed: 2026-06-13
---

# Design

## Overview

Extend the spec lifecycle runtime from checkbox parsing into lightweight task
management. Markdown remains the durable source. Runtime and MCP tools provide
structured views, guarded updates, and advisory checks that prevent broad or
contradictory task state from hiding unfinished work.

## High-Level Design

The implementation has four parts:

- Task state contract: normalize legacy letter markers and preferred symbolic
  markers into stable states.
- Task query tools: list tasks, return task detail with traceability context,
  and audit suspicious completion or broad task shape.
- Reconciliation checks: compare task state with evidence depth, discovered
  implementation signals, and cross-spec dependency health.
- Task update tool: perform a dry-run or scoped marker/evidence edit with guard
  rails for completion.
- Guidance and hooks: update skill/template/docs and add low-noise advisory
  checks.

## Task State Contract

Preferred developer-authored markers:

| Marker | Normalized state | Meaning |
| --- | --- | --- |
| `[ ]` | `pending` | Not started. |
| `[~]` | `in_progress` | Selected work is actively being handled. |
| `[/]` | `partial` | Some work is done, but acceptance is not met. |
| `[>]` | `follow_up` | Work is routed to a linked task, spec, backlog item, or external owner. |
| `[-]` | `no_op` | Intentionally not implemented in this spec: no-op, raw-only, not applicable, superseded, or deferred. |
| `[?]` | `review_needed` | Needs decision, domain review, or sign-off before implementation or closure. |
| `[!]` | `attention` | Blocked, errored, or needs intervention/diagnosis. |
| `[x]` | `complete` | Acceptance met and evidence recorded. |

Compatibility markers:

- `[Y]` maps to `partial`.
- `[*]` maps to `attention`.
- `[e]` maps to `attention` with `legacy_marker: error`.

The design intentionally does not add a separate validation-needed marker.
Validation-only gaps should be represented as either a validation subtask or a
`partial` parent task with explicit evidence. This keeps the marker set smaller
and avoids a second form of in-progress work.

Optional non-keyboard display glyphs may be added later in UIs, but Markdown
source should use the keyboard markers above.

## Low-Level Design

### Runtime Parsing

Update the task regex and parser to accept preferred markers and compatibility
markers. Extend the `Task` model with:

- `marker`
- `status`
- `legacy_marker` when applicable
- `parent_id` for subtasks
- `children` in task-list/detail payloads
- `status_note` extracted from `Status:`

The parser should keep existing fields: dependencies, files, acceptance,
evidence, line number, and source block.

### Task List Tool

Add `task_list(spec_path, include_subtasks=True, status=None)` to
`spec_runtime.py`.

Output:

- summary counts by state
- phases with task IDs
- task records with parent/subtask structure
- dependency readiness
- evidence summary
- broad-task warnings

MCP tool: `list_tasks`.

### Task Detail Tool

Add `task_details(spec_path, task_id)` as the primary structured wrapper around
the existing traceability lookup.

Output:

- parsed task record
- parent task and child subtasks
- dependency state
- traceability lookup payload
- linked requirements
- verification and durable target references
- gaps and broad-task warnings

MCP tool: `task_details`.

### Task Audit Tool

Add `task_state_audit(spec_path)` to identify:

- complete tasks whose evidence contains unresolved language;
- unchecked tasks whose evidence or linked files indicate existing
  implementation;
- complete tasks whose evidence is plan-only, dry-run-only, contract-only, or a
  blocked output while acceptance implies implemented behavior;
- cross-spec dependencies whose upstream task state is stale or untrusted;
- parent tasks marked complete while child tasks are not complete/no-op/follow-up;
- broad tasks with multiple source families, many acceptance clauses, or
  multiple outcome verbs;
- tasks with follow-up language but no follow-up state or linked task;
- tasks with pending evidence but non-pending markers.

MCP tool: `task_state_audit`.

### Reconciliation Classifications

The audit output should include stable machine-readable classifications:

| Classification | Meaning |
| --- | --- |
| `stale_open` | Task is pending or unchecked but has concrete implementation/evidence notes. |
| `candidate_complete` | Evidence appears sufficient for completion, but the marker has not been updated. |
| `plan_only_completion` | Task is complete, but evidence only proves a planner, contract, or dry run while acceptance implies behavior. |
| `blocked_output` | Task is complete, but the delivered behavior intentionally emits blocked/deferred output. |
| `cross_spec_dependency_untrusted` | Referenced upstream spec/task has stale, partial, attention, or unchecked state. |
| `existing_functionality_found` | Code/tests/docs already implement some acceptance before the task is worked. |

These classifications are advisory. They should make stale state visible without
auto-changing task markers.

### Evidence Depth

Task records and audit findings should distinguish evidence mode:

- `implementation`: runtime behavior or docs changed and verified.
- `validation`: tests, checks, or live evidence prove existing behavior.
- `planner`: a plan, preview, or generated contract exists, but no mutation or
  execution path was implemented.
- `dry_run`: execution was intentionally non-mutating.
- `routing`: work was moved to another task, spec, backlog item, or owner.
- `no_op`: task was intentionally unnecessary or superseded.
- `blocked_output`: implementation returns a blocked/deferred result by design.

`set_task_state` should accept evidence mode metadata. Completion is allowed for
planner, dry-run, routing, no-op, or blocked-output evidence only when the task
acceptance explicitly says that mode satisfies the task.

### Task State Update Tool

Add `set_task_state(spec_path, task_id, state, evidence, status_note=None,
dry_run=True)`.

Behavior:

- Default to dry-run.
- Preserve unrelated task text.
- Change only the selected marker and the selected task's `Evidence:` or
  `Status:` field.
- Reject `complete` when evidence contains unresolved language or no concrete
  evidence signal.
- Reject `complete` when evidence mode is planner, dry-run, routing, no-op, or
  blocked-output unless the acceptance text explicitly scopes completion to that
  evidence mode.
- Require reason/destination metadata for `follow_up`, `no_op`,
  `review_needed`, and `attention`.

MCP tool: `set_task_state`.

### Hook Behavior

Extend existing advisory hooks:

- `task-checkbox-changed`: run completion audit on changed `tasks.md`.
- `agent-slice-start`: report existing in-progress tasks in the selected spec.
- `spec-resumed` or `active_spec_preflight`: summarize non-final task states
  and reconciliation warnings once per preflight response.

Noise policy:

- No warning when state and evidence agree.
- No repeated reminders on every write.
- Advisory by default; blocking remains an explicit adoption choice.

## Operational Considerations

- The task-state update tool writes Markdown and should be heavily tested with
  fixtures before broad adoption.
- Repositories may still choose a smaller marker set; compatibility parsing lets
  old specs remain readable.
- The skill guidance should emphasize subtasks before status proliferation.
- Broad verification tasks should be split before implementation starts, not
  only after a user notices hidden follow-up work.

## Open Questions

- Should `[?]` represent both review and decision, or should domain review and
  implementation review be separate metadata under `Status:`?
- Should `[-]` include deferred work, or should deferred work always use `[>]`
  with a backlog/spec destination?
- Should `set_task_state` be exposed in MCP immediately or kept CLI-only until
  write-tool guardrails have enough dogfood evidence?
