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

- [x] T001 Review and finalize the staged lifecycle contract.
  - Files: `docs/specs/024-staged-developer-onboarding/requirements.md`, `docs/specs/024-staged-developer-onboarding/design.md`
  - Acceptance: Accepted ideas, non-goals, blank-repo behavior, staged flow, Agent Readiness Contract, optional repo-evidence boundary, context-budget rules, learning-loop taxonomy, tooling preservation, and packaging exclusion are confirmed.
  - Evidence: Confirmed on 2026-06-13: the requirements and design cover accepted CLU-inspired ideas, non-goals, blank-repo bootstrap, staged flow, Agent Readiness Contract, optional repo-evidence boundary, context-budget rules, learning-loop taxonomy, tooling preservation, and unchanged packaging scope. Traceability matrix column names were normalized for runtime lookup compatibility.

- [x] T002 Update lifecycle skill guidance for first-run and staged flow.
  - Depends on: T001
  - Files: `skills/spec-lifecycle-manager/SKILL.md`
  - Acceptance: Skill guidance covers first-run use, blank-repo bootstrap, staged artifacts, design-first exception handling, Agent Readiness Contract, optional repo-evidence boundary, context-budget rules, execution recovery, agent directives, properties-to-tests, instruction-as-code routing, numbered findings, and MCP-first tooling.
  - Evidence: Updated `skills/spec-lifecycle-manager/SKILL.md` with First Run guidance, preview-first blank-repo bootstrap, staged artifact progression, design-first exception handling, Agent Readiness Contract, optional repo-evidence boundary, context-budget rules, recovery discipline, evidence-derived agent directives, properties-to-tests guidance, instruction-as-code routing, numbered findings, and MCP-first runtime access.

- [x] T003 Update fallback spec and durable-doc templates selectively.
  - Depends on: T002
  - Files: `skills/spec-lifecycle-manager/references/spec-package/`, `skills/spec-lifecycle-manager/references/durable-doc-templates/`
  - Acceptance: Templates support staged readiness, evidence-derived agent directives, properties-to-tests traceability, checkpoint validation, and numbered findings without forcing optional artifacts up front.
  - Evidence: Updated fallback spec templates for staged readiness, property-to-design mapping, downstream task guidance, checkpoint validation, Agent Readiness Contract evidence, correctness-property coverage, and traceability gaps. Updated durable-doc templates for optional evidence-derived agent directives, numbered findings, and staged lifecycle/instruction-as-code routing without adding mandatory optional artifacts. Synced source skill changes to Codex and Claude plugin bundled copies to satisfy existing package parity tests without changing packaging behavior.

## Phase 2: Runtime Readiness And Bootstrap Tools

- [x] T004 Implement lifecycle guide runtime output.
  - Depends on: T002
  - Files: `skills/spec-lifecycle-manager/scripts/spec_runtime.py`, `skills/spec-lifecycle-manager/scripts/spec_agent_schemas.py`
  - Acceptance: Runtime reports repo classification, lifecycle tooling availability, docs readiness, spec readiness, stage status, template authority, Agent Readiness Contract gaps, optional repo-evidence caveats, and next actions as deterministic JSON-compatible output.
  - Evidence: Added `lifecycle_guide`, repository classification, docs readiness, spec readiness, prompt/tooling/hook reporting, bootstrap recommendation, and next-action JSON payloads in `spec_runtime.py`; focused runtime and CLI tests passed on 2026-06-13.

- [x] T005 Implement blank-repo bootstrap planning.
  - Depends on: T004
  - Files: `skills/spec-lifecycle-manager/scripts/spec_runtime.py`, `tests/runtime/`, `tests/fixtures/`
  - Acceptance: Runtime returns a preview-only bootstrap plan for blank and near-blank repos, including paths, template sources, required user values, validation commands, assumptions, and deferred architecture/pattern recommendations.
  - Evidence: Added preview-only `bootstrap_plan` runtime and CLI behavior for blank and near-blank repositories, including preview paths, template sources, required user values, validation commands, assumptions, and deferred architecture/pattern recommendations; focused runtime and CLI tests passed on 2026-06-13.

- [x] T006 Expose lifecycle guide and bootstrap plan through MCP.
  - Depends on: T005
  - Files: `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`
  - Acceptance: MCP exposes read-only `lifecycle_guide` and `bootstrap_plan` tools, rejects mutation, and returns the runtime payloads with repo-root handling consistent with existing tools.
  - Evidence: Added read-only MCP schemas and dispatch for `lifecycle_guide` and `bootstrap_plan`; focused MCP tests passed on 2026-06-13 and confirmed no files are written by bootstrap previews.

- [x] T007 Add prompt entry point for first-run developer guidance.
  - Depends on: T006
  - Files: `skills/spec-lifecycle-manager/prompts/`, `skills/spec-lifecycle-manager/prompts/README.md`
  - Acceptance: Prompt definitions include a first-run/developer-start flow that uses runtime-backed readiness and does not invent blank-repo architecture.
  - Evidence: Added `developer-start.json`, included it in prompt validation requirements, and updated the prompt README; `spec_runtime.py prompts .` returned 0 diagnostics on 2026-06-13.

## Phase 3: Stage Readiness And Traceability Coverage

- [x] T008 Add stage readiness and coverage checks.
  - Depends on: T005
  - Files: `skills/spec-lifecycle-manager/scripts/spec_runtime.py`, `skills/spec-lifecycle-manager/scripts/traceability_lookup.py`, `tests/runtime/`, `tests/traceability/`
  - Acceptance: Runtime reports stage readiness, downstream review needs, context-budget gaps, property-to-design mapping gaps, property-to-task/verification gaps, and acceptance-criteria coverage gaps before implementation readiness.
  - Evidence: Completed on 2026-06-13: added `stage_readiness` runtime output, `stage-readiness` CLI, and read-only MCP `stage_readiness`; focused runtime/MCP tests passed 7 tests, and `spec_runtime.py stage-readiness docs/specs/024-staged-developer-onboarding` reported 0 blocking, context, downstream, property, and acceptance gaps.

- [x] T009 Update runtime docs and design docs.
  - Depends on: T007, T008
  - Files: `docs/reference/spec-lifecycle-runtime.md`, `docs/design/spec-lifecycle-management.md`, `docs/reference/document-routing-and-expert-review-matrix.md`
  - Acceptance: Durable docs explain lifecycle guide, bootstrap planning, staged flow, readiness output, Agent Readiness Contract, optional repo-evidence boundary, context-budget rules, properties-to-tests coverage, agent directives, numbered findings, learning-loop taxonomy, and validation/recovery behavior.
  - Evidence: Completed on 2026-06-13: updated the three durable docs named by T009 with staged developer onboarding behavior; MCP `lint_doc` on each doc and MCP `lint_spec_package` returned 0 diagnostics.

## Phase 4: Bundles, Tests, And Validation

- [x] T010 Sync plugin bundle and validate.
  - Depends on: T009
  - Files: `plugins/spec-lifecycle-manager/`, `tests/`
  - Acceptance: Bundled skill/plugin copy matches source where required; unit tests, prompt validation, runtime scan, archive index, and whitespace checks pass.
  - Evidence: Completed on 2026-06-13: synced source skill to both bundled plugin copies; MCP spec lint, MCP prompts, MCP archive index, CLI scan, CLI prompts, CLI archive-index, package-contract, full unit suite with 141 tests, and `git diff --check` passed. `sync-guard` reported source bundle parity in sync and installed cache drift as an install/reload advisory.

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
