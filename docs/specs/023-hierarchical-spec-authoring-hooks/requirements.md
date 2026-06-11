---
title: Hierarchical spec authoring hooks requirements
doc_type: spec
artifact_type: requirements
status: active
owner: platform
last_reviewed: 2026-06-11
---

# Requirements

## Durable Source Baseline

- Backlog item B046 records noisy `PostToolUse` feedback while agents create
  spec packages one file at a time.
- `docs/reference/spec-lifecycle-runtime.md` documents the current hook mapping:
  any `docs/**/specs/**/*.md` write calls `spec-file-changed`, and
  `tasks.md` also calls `task-checkbox-changed`.
- `skills/spec-lifecycle-manager/scripts/spec_runtime.py` currently implements
  `spec-file-changed` by linting the whole affected package.
- `skills/spec-lifecycle-manager/scripts/codex_spec_lifecycle_hook.py` currently
  condenses runtime diagnostics into a short Codex `additionalContext` message.

## Goals

- Make spec-authoring hook feedback hierarchy-aware and action-oriented.
- Distinguish initial authoring from revision of an upstream artifact after
  downstream artifacts already exist.
- Keep full package lint and closure checks available for explicit validation,
  resume, and close events.
- Point agents to the next useful document, MCP tool, prompt, or template
  resource without flooding the turn with stale package-wide diagnostics.

## Non-Goals

- Do not make hooks blocking by default.
- Do not infer semantic downstream staleness without changed-file context or
  explicit validation evidence.
- Do not remove full package linting from explicit lint, resume, validation, or
  closure workflows.
- Do not implement auto-rewrites or create missing spec artifacts.

## Requirements

### Requirement 1: Spec Tree Context

**User Story:** As an agent authoring a spec, I want hooks to understand the
current spec tree, so that feedback matches the file I just wrote.

#### Acceptance Criteria

1. GIVEN changed spec files, WHEN hook analysis runs, THEN the system SHALL
   identify the affected spec package, changed artifact types, existing
   artifacts, missing prerequisite artifacts, and existing downstream artifacts.
2. GIVEN a changed artifact, WHEN the system evaluates hierarchy, THEN it SHALL
   classify the write as `initial_authoring`, `revision`, `task_update`,
   `verification_update`, or `closure_check` where determinable from changed
   files and hook name.
3. IF a spec package has downstream artifacts that already exist, THEN the
   system SHALL report them as downstream review candidates, not as the next
   required authoring step.

### Requirement 2: Hierarchical Authoring Guidance

**User Story:** As an agent creating a spec incrementally, I want the hook to
recommend the next useful artifact, so that I can continue in the right order.

#### Acceptance Criteria

1. GIVEN `requirements.md` is written and no `design.md` exists, THEN the
   system SHALL recommend `design.md` as the next authoring step.
2. GIVEN `design.md` is written, THEN the system SHALL check for package root,
   `requirements.md`, and referenced research context, but SHALL NOT warn about
   missing downstream `tasks.md`, `traceability.md`, or `verification.md` as
   package-health defects.
3. GIVEN `tasks.md` is written, THEN the system SHALL check task shape and
   recommend `traceability.md` or `verification.md` when appropriate.
4. GIVEN `verification.md` is written, THEN the system SHALL check validation
   structure and recommend closure checks only when task evidence indicates the
   package is near closure.

### Requirement 3: Revision-Aware Downstream Advice

**User Story:** As a maintainer revising earlier spec artifacts, I want hooks
to tell me which downstream files may need review, so that I update the spec
tree coherently without being sent to the wrong next step.

#### Acceptance Criteria

1. GIVEN `requirements.md` changes after `design.md`, `tasks.md`,
   `traceability.md`, or `verification.md` exists, THEN the system SHALL
   recommend reviewing those downstream artifacts for consistency.
2. GIVEN `design.md` changes after `tasks.md`, `traceability.md`, or
   `verification.md` exists, THEN the system SHALL recommend reviewing those
   downstream artifacts for consistency.
3. WHEN downstream artifacts are reported because of an upstream revision, THEN
   the system SHALL label them as `review_existing_downstream` and SHALL NOT
   present them as missing prerequisites or next authoring steps.

### Requirement 4: Focused Hook Diagnostics

**User Story:** As a Codex user, I want hook output to stay concise, so that
advisory diagnostics are useful instead of ignored.

#### Acceptance Criteria

1. WHEN `spec-file-changed` handles ordinary authoring or revision writes, THEN
   the system SHALL avoid full package lint diagnostics that are unrelated to
   the changed artifact.
2. WHEN `tasks.md` changes, THEN completed-task evidence diagnostics SHALL be
   scoped to changed or completion-relevant task content where feasible, or the
   output SHALL state that full task lint is being run for a task-update event.
3. WHEN a full package check is appropriate, THEN the system SHALL identify the
   mode as `package_validation`, `resume`, or `closure` rather than ordinary
   authoring.
4. WHEN diagnostics are emitted through the Codex wrapper, THEN the context
   SHALL include a concise next action, relevant files, and omitted-count
   summary only for diagnostics from the selected mode.

### Requirement 5: Helper Surfaces

**User Story:** As an agent receiving hook guidance, I want relevant tools and
resources named, so that I know how to continue without guessing.

#### Acceptance Criteria

1. WHERE a missing or next artifact is recommended, THE SYSTEM SHALL include
   relevant helper resources such as `templates://spec-package`, prompt names,
   or MCP tools.
2. WHERE package context is ambiguous, THE SYSTEM SHALL recommend
   `scan_specs`, `active_spec_preflight`, or `lint_spec_package` as appropriate.
3. WHERE task-context validation is the next useful action, THE SYSTEM SHALL
   recommend `task_context` or `traceability_lookup`.

## Correctness Properties

- CP-001: The same repo tree, hook name, and changed files SHALL produce the
  same authoring guidance.
- CP-002: Authoring guidance SHALL not mutate specs, tasks, evidence, or docs.
- CP-003: Full package diagnostics SHALL remain available through explicit
  validation, resume, and closure paths.
- CP-004: Revision guidance SHALL distinguish downstream review candidates from
  missing prerequisite artifacts.

## Success Criteria

- Runtime tests cover initial authoring, upstream revision with downstream
  artifacts, task updates, and explicit package validation.
- Codex hook wrapper tests cover concise action-oriented output.
- Runtime docs explain hook modes, hierarchy behavior, and helper surfaces.
- Bundled Codex and Claude plugin copies remain in sync after implementation.
