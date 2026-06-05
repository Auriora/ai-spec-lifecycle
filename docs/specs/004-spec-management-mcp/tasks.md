---
title: Spec management MCP tasks
doc_type: spec
artifact_type: tasks
status: draft
owner: platform
last_reviewed: 2026-06-05
---

# Tasks

**Input**: `requirements.md`, `design.md`, `research.md`,
`docs/design/spec-lifecycle-management.md`, and
`skills/spec-lifecycle-manager/`.

## Task Dependency Graph

```text
T001 -> T002 -> T003
T003 -> T004
T003 -> T005
T003 -> T012
T004 + T005 -> T006
T006 -> T008
T006 + T012 -> T007
T008 -> T009
T007 + T009 -> T010
T010 -> T011
```

## Phase 1: Baseline And Decisions

- [x] T001 Capture MCP prompt versus Skill tradeoff.
  - Depends on: none
  - Files: `docs/specs/004-spec-management-mcp/research.md`,
    `docs/specs/004-spec-management-mcp/design.md`
  - Acceptance: Spec records current MCP prompt semantics, Skill role, and the
    recommended split of responsibilities.
  - Evidence: Research and design artifacts created.

- [x] T002 Create detailed spec package.
  - Depends on: T001
  - Files: `docs/specs/004-spec-management-mcp/`
  - Acceptance: Package includes requirements, design, tasks, and research.
  - Evidence: This spec package created.

- [x] T003 Decide implementation home and packaging.
  - Depends on: T002
  - Files: `docs/specs/004-spec-management-mcp/design.md`,
    `skills/spec-lifecycle-manager/scripts/traceability_lookup.py`
  - Acceptance: Decision identifies whether the MCP server lives in this repo,
    a plugin package, or a separate reusable repository.
  - Evidence: Design records that deterministic helpers can live in the skill
    scripts first and be wrapped by a future MCP adapter.

## Phase 2: Deterministic Runtime MVP

- [x] T004 Implement spec scanner and resources.
  - Depends on: T003
  - Files: `skills/spec-lifecycle-manager/scripts/spec_runtime.py`,
    `tests/runtime/test_spec_runtime.py`
  - Acceptance: `scan_specs`, `specs://active`, `specs://{spec_id}/summary`,
    and template resources return structured data for current and fixture
    specs.
  - Evidence: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'`;
    `skills/spec-lifecycle-manager/scripts/spec_runtime.py scan .`;
    `skills/spec-lifecycle-manager/scripts/spec_runtime.py summary docs/specs/004-spec-management-mcp`.
  - [x] T004.1 Discover active spec packages.
  - [x] T004.2 Classify current versus old-format packages.
  - [x] T004.3 Resolve effective templates.
  - [x] T004.4 Expose MCP-resource-shaped JSON payloads.

- [x] T005 Implement artifact linters.
  - Depends on: T003
  - Files: `skills/spec-lifecycle-manager/scripts/spec_runtime.py`,
    `tests/runtime/test_spec_runtime.py`
  - Acceptance: `lint_doc` and `lint_spec_package` validate frontmatter,
    required sections, task evidence, dependency IDs, and optional artifact
    rules.
  - Evidence: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'`;
    `skills/spec-lifecycle-manager/scripts/spec_runtime.py lint docs/specs/004-spec-management-mcp`.
    Explicit `spec-lint-waive: CODE - reason` markers are parsed and reported
    as waived diagnostics.
  - [x] T005.1 Implement frontmatter and heading checks.
  - [x] T005.2 Implement requirements checks.
  - [x] T005.3 Implement design checks.
  - [x] T005.4 Implement tasks checks.
  - [x] T005.5 Implement optional artifact checks.
  - [x] T005.6 Implement waiver parsing and reporting.

- [x] T006 Implement next-task and closure checks.
  - Depends on: T004, T005
  - Files: `skills/spec-lifecycle-manager/scripts/spec_runtime.py`,
    `tests/runtime/test_spec_runtime.py`
  - Acceptance: `next_task` respects dependencies and evidence and returns
    traceability context; `closure_check` reports verification, promotion,
    open-decision, and active-index blockers.
  - Evidence: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'`;
    `skills/spec-lifecycle-manager/scripts/spec_runtime.py next-task docs/specs/004-spec-management-mcp`;
    `skills/spec-lifecycle-manager/scripts/spec_runtime.py closure-check docs/specs/004-spec-management-mcp`
    returns blockers for the still-active spec.

- [x] T012 Implement traceability lookup.
  - Depends on: T003 for the standalone CLI; T006 remains the dependency for
    wiring this behavior into future MCP task-selection surfaces.
  - Files: `skills/spec-lifecycle-manager/scripts/traceability_lookup.py`,
    `tests/traceability/test_traceability_lookup.py`,
    `docs/specs/004-spec-management-mcp/traceability.md`,
    `skills/spec-lifecycle-manager/SKILL.md`,
    `skills/spec-lifecycle-manager/references/spec-package/traceability.md`
  - Acceptance: `task_context` and `traceability_lookup` return forward and
    reverse mappings across requirements, acceptance criteria, design sections,
    tasks, verification, durable targets, and open decisions; stale or missing
    matrix rows are reported as gaps.
  - Evidence: `python3 -m unittest discover -s tests -p 'test_*.py'`;
    `skills/spec-lifecycle-manager/scripts/traceability_lookup.py docs/specs/004-spec-management-mcp --task T012`;
    missing task lookup returns exit code 1 with
    `TRACEABILITY_TASK_ROW_MISSING`.

## Phase 3: Prompt And Hook Surfaces

- [x] T007 Add MCP prompt definitions.
  - Depends on: T006, T012
  - Files: `skills/spec-lifecycle-manager/prompts/`,
    `skills/spec-lifecycle-manager/scripts/spec_runtime.py`,
    `tests/runtime/test_spec_runtime.py`
  - Acceptance: `reconcile-spec`, `choose-next-task`, `task-context`, and
    `lint-spec` prompts are discoverable where client support exists and
    include clear arguments.
  - Evidence: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'`;
    `skills/spec-lifecycle-manager/scripts/spec_runtime.py prompts .`.

- [x] T008 Add hook runner MVP.
  - Depends on: T006
  - Files: `skills/spec-lifecycle-manager/scripts/spec_runtime.py`,
    `tests/runtime/test_spec_runtime.py`
  - Acceptance: `spec-file-changed` and `task-checkbox-changed` can lint
    affected spec packages, detect completed tasks without evidence, and emit
    JSON plus human-readable output.
  - Evidence: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'`;
    `skills/spec-lifecycle-manager/scripts/spec_runtime.py hook spec-file-changed --changed-files docs/specs/004-spec-management-mcp/tasks.md`;
    `skills/spec-lifecycle-manager/scripts/spec_runtime.py hook task-checkbox-changed --severity-profile blocking --changed-files docs/specs/004-spec-management-mcp/tasks.md`.
  - [x] T008.1 Implement changed-spec artifact lint.
  - [x] T008.2 Implement task checkbox evidence detection.
  - [x] T008.3 Implement advisory versus blocking severity profiles.
  - [x] T008.4 Add fixture coverage for changed files and task completion.

## Phase 4: Lifecycle Hook Gates

- [x] T009 Add completion, verification, resume, and closure hooks.
  - Depends on: T008
  - Files: `skills/spec-lifecycle-manager/scripts/spec_runtime.py`,
    `tests/runtime/test_spec_runtime.py`
  - Acceptance: Hooks can check implementation task completion,
    verification-evidence updates, spec resume reconciliation, and spec closure
    readiness with clear blocking versus advisory behavior.
  - Evidence: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'`;
    `skills/spec-lifecycle-manager/scripts/spec_runtime.py hook implementation-task-complete --spec-path docs/specs/004-spec-management-mcp --task-id T009`;
    `skills/spec-lifecycle-manager/scripts/spec_runtime.py hook verification-updated --spec-path docs/specs/004-spec-management-mcp`;
    `skills/spec-lifecycle-manager/scripts/spec_runtime.py hook spec-resumed --spec-path docs/specs/004-spec-management-mcp`;
    `skills/spec-lifecycle-manager/scripts/spec_runtime.py hook spec-close-check --spec-path docs/specs/004-spec-management-mcp --severity-profile blocking`
    returns blockers for the still-active spec.
  - [x] T009.1 Implement implementation task completion checks.
  - [x] T009.2 Implement verification evidence mapping checks.
  - [x] T009.3 Implement resume reconciliation hook.
  - [x] T009.4 Implement closure readiness hook.

## Phase 5: Semantic Review And Promotion Planning

- [x] T010 Add reconciliation, promotion planning, and review packets.
  - Depends on: T007, T009
  - Files: `skills/spec-lifecycle-manager/scripts/spec_runtime.py`,
    `tests/runtime/test_spec_runtime.py`
  - Acceptance: Tools generate classified drift reports, durable promotion
    targets, and bounded cheap-agent review packets.
  - Evidence: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'`;
    `skills/spec-lifecycle-manager/scripts/spec_runtime.py reconcile docs/specs/004-spec-management-mcp`;
    `skills/spec-lifecycle-manager/scripts/spec_runtime.py promotion-plan docs/specs/004-spec-management-mcp`;
    `skills/spec-lifecycle-manager/scripts/spec_runtime.py review-packet docs/specs/004-spec-management-mcp --review-type design_requirements_trace`;
    `skills/spec-lifecycle-manager/scripts/spec_runtime.py hook agent-slice-start --spec-path docs/specs/004-spec-management-mcp --task-id T010 --severity-profile blocking`;
    `skills/spec-lifecycle-manager/scripts/spec_runtime.py hook review-packet-dispatch --spec-path docs/specs/004-spec-management-mcp`.
  - [x] T010.1 Implement `reconcile_spec`.
  - [x] T010.2 Implement `promotion_plan`.
  - [x] T010.3 Implement `generate_review_packet`.
  - [x] T010.4 Record review-packet result disposition format.
  - [x] T010.5 Implement agent-oriented hook candidates for
    `agent-slice-start`, `agent-response-check`, `review-packet-dispatch`, and
    `review-result-recorded`.

## Phase 6: Metrics, Governance, Dogfood, And Promote

- [x] T011 Dogfood the MCP runtime on this spec and promote durable docs.
  - Depends on: T010
  - Files: `docs/specs/004-spec-management-mcp/`,
    `docs/reference/spec-lifecycle-runtime.md`,
    `docs/design/spec-lifecycle-management.md`,
    `docs/README.md`
  - Acceptance: Dogfood evidence records useful findings, overhead, prompt
    support limits, hook value, repeated waivers, governance-sensitive changes,
    and durable doc promotion targets.
  - Evidence: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'`;
    runtime dogfood commands recorded in `verification.md`; durable runtime
    docs promoted to `docs/reference/spec-lifecycle-runtime.md` and linked from
    `docs/design/spec-lifecycle-management.md`.

## Related Artifacts

- Requirements: [requirements.md](requirements.md)
- Design: [design.md](design.md)
- Research: [research.md](research.md)
- Traceability: [traceability.md](traceability.md)
