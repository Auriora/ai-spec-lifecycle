---
title: Task state management tools tasks
doc_type: spec
artifact_type: tasks
status: active
owner: platform
last_reviewed: 2026-06-13
---

# Tasks

## Task Dependency Graph

T001 -> T002 -> T003
T002 -> T004 -> T005
T002 -> T006
T005 + T006 -> T010
T010 -> T007
T003 + T007 + T010 -> T008
T008 -> T009

## Phase 1: Contract And Parser

- [ ] T001 Finalize the symbolic task-state contract.
  - Files: `skills/spec-lifecycle-manager/SKILL.md`, `docs/reference/spec-lifecycle-runtime.md`
  - Acceptance: Preferred keyboard markers, compatibility markers, normalized states, and unresolved open decisions are documented.
  - Evidence: Pending.

- [ ] T002 Update task parsing and payloads.
  - Depends on: T001
  - Files: `skills/spec-lifecycle-manager/scripts/spec_runtime.py`, `skills/spec-lifecycle-manager/scripts/traceability_lookup.py`
  - Acceptance: Runtime parses preferred symbolic markers and legacy markers, returns normalized state, legacy marker where applicable, subtask relationships, status notes, evidence mode, destination, decision owner, and upstream/downstream spec references.
  - Evidence: Pending.

- [ ] T003 Add parser and summary tests.
  - Depends on: T002
  - Files: `tests/runtime/test_spec_runtime.py`, `tests/traceability/test_traceability_lookup.py`
  - Acceptance: Tests cover preferred markers, legacy `[Y]` and `[e]`, parent/subtask status, metadata fields, and summary counts.
  - Evidence: Pending.

## Phase 2: Task Query Tools

- [ ] T004 Implement task listing and task detail helpers.
  - Depends on: T002
  - Files: `skills/spec-lifecycle-manager/scripts/spec_runtime.py`
  - Acceptance: Helpers return grouped tasks, dependency readiness, evidence summaries, parent/subtask detail, cross-spec references, and traceability-backed task context.
  - Evidence: Pending.

- [ ] T005 Expose task query tools through MCP.
  - Depends on: T004
  - Files: `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`
  - Acceptance: `list_tasks` and `task_details` appear in MCP `tools/list` and return structured output.
  - Evidence: Pending.

## Phase 3: Audit And State Updates

- [ ] T006 Implement task-state audit.
  - Depends on: T002
  - Files: `skills/spec-lifecycle-manager/scripts/spec_runtime.py`
  - Acceptance: Audit flags local contradictory completion evidence, broad tasks, incomplete child tasks under complete parents, follow-up prose without follow-up state, routed/review/attention states without required metadata, and non-pending markers with pending evidence.
  - Evidence: Pending.

- [ ] T010 Add cross-spec and evidence-depth reconciliation.
  - Depends on: T005, T006
  - Files: `skills/spec-lifecycle-manager/scripts/spec_runtime.py`, `skills/spec-lifecycle-manager/scripts/traceability_lookup.py`, `tests/runtime/test_spec_runtime.py`, `tests/fixtures/`
  - Acceptance: Runtime reports cross-spec dependency health when local specs are available, classifies stale-open/candidate-complete/plan-only/blocked-output findings, and returns `split_task_suggestions` for broad profile-style work.
  - Evidence: Pending.

- [ ] T007 Implement guarded task-state updates.
  - Depends on: T010
  - Files: `skills/spec-lifecycle-manager/scripts/spec_runtime.py`
  - Acceptance: Dry-run and write modes update only the selected task marker/evidence/status note and optional metadata fields, reject unsafe completion, reject unsupported plan-only/dry-run/blocked-output completion, reject paths outside active spec package `tasks.md`, require explicit write intent, return a before/after patch summary, and require destination/decision metadata for non-final routed or attention states.
  - Evidence: Pending.

- [ ] T008 Expose audit/update tools and hook checks.
  - Depends on: T003, T007, T010
  - Files: `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`, `skills/spec-lifecycle-manager/scripts/codex_spec_lifecycle_hook.py`, `plugins/spec-lifecycle-manager/hooks/hooks.json`
  - Acceptance: MCP exposes `task_state_audit` and guarded `set_task_state`; existing advisory hooks report contradictory completion, stale-open tasks, plan-only completion candidates, and existing in-progress tasks without repeated noise.
  - Evidence: Pending.

## Phase 4: Guidance, Bundles, And Validation

- [ ] T009 Update skill guidance, templates, docs, bundles, and validation.
  - Depends on: T008
  - Files: `skills/spec-lifecycle-manager/SKILL.md`, `skills/spec-lifecycle-manager/references/spec-package/`, `docs/reference/spec-lifecycle-runtime.md`, `plugins/spec-lifecycle-manager/`
  - Acceptance: Source skill, fallback templates, runtime docs, plugin bundle, Claude plugin bundle, and tests are aligned; validation commands pass.
  - Evidence: Pending.

## Execution Notes

- Before implementing a task, mark it `[~]`.
- Split any implementation task further if it starts to mix runtime behavior,
  MCP exposure, hook behavior, docs, and bundle sync in one change.
- Use subtasks rather than additional markers when a task has separate
  implementation and validation slices.
- Use `Evidence mode:`, `Destination:`, `Decision owner:`, `Upstream specs:`,
  and `Downstream specs:` metadata when plain evidence text would otherwise hide
  routed work, review ownership, or cross-spec dependency trust.
