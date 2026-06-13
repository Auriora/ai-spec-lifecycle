---
title: Validation plan builder requirements
doc_type: spec
artifact_type: requirements
status: active
owner: platform
last_reviewed: 2026-06-13
---

# Requirements

## Durable Source Baseline

- Backlog item B023 requests a focused validation plan from changed files, task
  context, risk level, and durable-doc impact.
- `docs/reference/spec-lifecycle-runtime.md` documents deterministic runtime
  and MCP validation surfaces.
- `skills/spec-lifecycle-manager/scripts/spec_runtime.py` already exposes
  scan, lint, preflight, traceability, package, archive, and sync checks.

## Goals

- Build a read-only validation planner for lifecycle work.
- Return command/tool recommendations with reasons, required inputs, and risk
  coverage.
- Support direct changed-file input and optional active spec/task context.
- Distinguish checks that are not applicable from checks that were skipped or
  not run, especially for documentation-only changes.
- Make the validation contract explicit before non-trivial implementation work
  starts, so agents know the pass/fail signal and expected evidence before
  editing.
- Keep the planner deterministic and dependency-free.

## Non-Goals

- Do not execute validation commands.
- Do not make hooks blocking.
- Do not infer external CI status.
- Do not replace project-specific validation configured by target repositories.

## Requirements

### Requirement 1: Validation Plan Inputs

**User Story:** As an implementation agent, I want to provide changed files and
optional task context, so that the validation plan matches the actual work.

#### Acceptance Criteria

1. GIVEN repo root and changed files, WHEN validation planning runs, THEN the
   system SHALL classify file groups such as runtime, MCP, hook, tests, docs,
   package, plugin bundle, and spec package.
2. GIVEN a spec path and task ID, WHEN validation planning runs, THEN the
   system SHALL include linked task, requirements, design, verification, and
   durable target context where available.
3. IF no changed files are provided, THEN the system SHALL still return baseline
   lifecycle validation for the selected repo/spec context.

### Requirement 2: Plan Output

**User Story:** As a maintainer, I want validation recommendations with
coverage reasons, so that I can understand why each check is required.

#### Acceptance Criteria

1. WHEN a plan is returned, THEN each check SHALL include a stable ID, command
   or MCP tool, reason, required flag, and covered risk.
2. WHERE package or plugin files changed, THE SYSTEM SHALL include
   `package-contract`, `sync-guard`, and package dry-run guidance.
3. WHERE specs or closure records changed, THE SYSTEM SHALL include scan,
   archive index, prompt, lint, or closure checks as appropriate.
4. WHERE changed files are documentation-only, THE SYSTEM SHALL recommend
   documentation and lifecycle checks and classify unrelated code/runtime checks
   as `not_applicable` or optional with a reason, not as noisy skipped
   validation.
5. IF a check would normally be required but cannot run because an input,
   credential, external service, or environment is unavailable, THEN THE SYSTEM
   SHALL classify it as `not_run` with the blocker and residual risk.
6. WHEN a non-trivial implementation task is selected, THEN the plan SHALL
   expose a validation contract with automated proof, manual proof, expected
   evidence location, residual risk if proof cannot run, false-positive risk,
   and false-negative risk where those fields can be derived from task,
   verification, or changed-file context.
7. IF a validation contract field cannot be derived, THEN the plan SHALL report
   the missing field as a planning gap instead of inventing proof criteria.
8. THE SYSTEM SHALL distinguish planned validation, executed validation,
   blocked validation, inspection-only validation, and not-applicable
   validation, so that a recommended proof method is not presented as completed
   evidence.
9. IF executed validation evidence is supplied through task, verification, or
   review context, THEN the plan SHALL preserve the evidence reference;
   otherwise it SHALL classify the proof as planned, needed, blocked,
   inspection-only, or not applicable.

### Requirement 3: MCP Surface

**User Story:** As a tool-calling agent, I want validation planning exposed
through MCP, so that validation guidance is available before edits or closure.

#### Acceptance Criteria

1. WHEN MCP tools are listed, THEN `validation_plan` SHALL be available as a
   read-only tool.
2. WHEN `validation_plan` is called, THEN it SHALL return the same structured
   payload as the CLI/runtime helper after path normalization.

## Correctness Properties

- CP-001: The same inputs SHALL produce the same plan.
- CP-002: The planner SHALL not mutate files, install packages, or run tests.
- CP-003: Required checks SHALL be explainable from changed files, task
  context, or baseline lifecycle policy.
- CP-004: `not_applicable` checks SHALL not be counted as missing validation.
- CP-005: Validation contract fields SHALL be derived from repository, spec, or
  task evidence and SHALL not be fabricated from generic defaults.
- CP-006: Planned validation SHALL not count as executed validation evidence.

## Success Criteria

- Runtime and MCP tests cover changed-file classification and output shape.
- Runtime and MCP output can provide a concise validation contract for
  non-trivial tasks before implementation starts.
- Runtime docs publish the command/tool and payload contract.
- Bundled Codex and Claude plugin copies remain in sync.
