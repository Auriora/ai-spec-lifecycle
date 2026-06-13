---
title: Staged developer onboarding tasks
doc_type: spec
artifact_type: tasks
status: active
owner: platform
last_reviewed: 2026-06-13
---

# Tasks

## Task Dependency Graph

T001 -> T002 -> T003
T002 -> T004
T003 + T004 -> T005
T005 -> T006 -> T007
T005 -> T008
T007 + T008 -> T009
T009 -> T010

## Phase 1: Requirements And Stage Contract

- [ ] T001 Review and finalize the staged lifecycle contract.
  - Files: `docs/specs/024-staged-developer-onboarding/requirements.md`, `docs/specs/024-staged-developer-onboarding/design.md`
  - Acceptance: Accepted ideas, non-goals, blank-repo behavior, staged flow, Agent Readiness Contract, optional repo-evidence boundary, context-budget rules, learning-loop taxonomy, tooling preservation, and packaging exclusion are confirmed.
  - Evidence: Pending.

- [ ] T002 Update lifecycle skill guidance for first-run and staged flow.
  - Depends on: T001
  - Files: `skills/spec-lifecycle-manager/SKILL.md`
  - Acceptance: Skill guidance covers first-run use, blank-repo bootstrap, staged artifacts, design-first exception handling, Agent Readiness Contract, optional repo-evidence boundary, context-budget rules, execution recovery, agent directives, properties-to-tests, instruction-as-code routing, numbered findings, and MCP-first tooling.
  - Evidence: Pending.

- [ ] T003 Update fallback spec and durable-doc templates selectively.
  - Depends on: T002
  - Files: `skills/spec-lifecycle-manager/references/spec-package/`, `skills/spec-lifecycle-manager/references/durable-doc-templates/`
  - Acceptance: Templates support staged readiness, evidence-derived agent directives, properties-to-tests traceability, checkpoint validation, and numbered findings without forcing optional artifacts up front.
  - Evidence: Pending.

## Phase 2: Runtime Readiness And Bootstrap Tools

- [ ] T004 Implement lifecycle guide runtime output.
  - Depends on: T002
  - Files: `skills/spec-lifecycle-manager/scripts/spec_runtime.py`, `skills/spec-lifecycle-manager/scripts/spec_agent_schemas.py`
  - Acceptance: Runtime reports repo classification, lifecycle tooling availability, docs readiness, spec readiness, stage status, template authority, Agent Readiness Contract gaps, optional repo-evidence caveats, and next actions as deterministic JSON-compatible output.
  - Evidence: Pending.

- [ ] T005 Implement blank-repo bootstrap planning.
  - Depends on: T004
  - Files: `skills/spec-lifecycle-manager/scripts/spec_runtime.py`, `tests/runtime/`, `tests/fixtures/`
  - Acceptance: Runtime returns a preview-only bootstrap plan for blank and near-blank repos, including paths, template sources, required user values, validation commands, assumptions, and deferred architecture/pattern recommendations.
  - Evidence: Pending.

- [ ] T006 Expose lifecycle guide and bootstrap plan through MCP.
  - Depends on: T005
  - Files: `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`
  - Acceptance: MCP exposes read-only `lifecycle_guide` and `bootstrap_plan` tools, rejects mutation, and returns the runtime payloads with repo-root handling consistent with existing tools.
  - Evidence: Pending.

- [ ] T007 Add prompt entry point for first-run developer guidance.
  - Depends on: T006
  - Files: `skills/spec-lifecycle-manager/prompts/`, `skills/spec-lifecycle-manager/prompts/README.md`
  - Acceptance: Prompt definitions include a first-run/developer-start flow that uses runtime-backed readiness and does not invent blank-repo architecture.
  - Evidence: Pending.

## Phase 3: Stage Readiness And Traceability Coverage

- [ ] T008 Add stage readiness and coverage checks.
  - Depends on: T005
  - Files: `skills/spec-lifecycle-manager/scripts/spec_runtime.py`, `skills/spec-lifecycle-manager/scripts/traceability_lookup.py`, `tests/runtime/`, `tests/traceability/`
  - Acceptance: Runtime reports stage readiness, downstream review needs, context-budget gaps, property-to-design mapping gaps, property-to-task/verification gaps, and acceptance-criteria coverage gaps before implementation readiness.
  - Evidence: Pending.

- [ ] T009 Update runtime docs and design docs.
  - Depends on: T007, T008
  - Files: `docs/reference/spec-lifecycle-runtime.md`, `docs/design/spec-lifecycle-management.md`, `docs/reference/document-routing-and-expert-review-matrix.md`
  - Acceptance: Durable docs explain lifecycle guide, bootstrap planning, staged flow, readiness output, Agent Readiness Contract, optional repo-evidence boundary, context-budget rules, properties-to-tests coverage, agent directives, numbered findings, learning-loop taxonomy, and validation/recovery behavior.
  - Evidence: Pending.

## Phase 4: Bundles, Tests, And Validation

- [ ] T010 Sync plugin bundle and validate.
  - Depends on: T009
  - Files: `plugins/spec-lifecycle-manager/`, `tests/`
  - Acceptance: Bundled skill/plugin copy matches source where required; unit tests, prompt validation, runtime scan, archive index, and whitespace checks pass.
  - Evidence: Pending.

## Execution Notes

- Before implementing a task, mark it `[~]`.
- Do not implement from this task list alone; read requirements, design,
  traceability, and verification for the selected task.
- Keep packaging changes out of scope except bundle parity required by existing
  repository tests.
- If a task starts mixing prompt guidance, runtime behavior, MCP exposure, docs,
  and tests in one change, split it into subtasks before marking it in progress.
- Use checkpoint validation after runtime/MCP changes before updating docs that
  claim the tool behavior exists.
