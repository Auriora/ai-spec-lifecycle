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
T004 + T005 -> T006
T006 -> T007
T006 -> T008
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

- [ ] T003 Decide implementation home and packaging.
  - Depends on: T002
  - Files: `docs/specs/004-spec-management-mcp/design.md`,
    future implementation paths
  - Acceptance: Decision identifies whether the MCP server lives in this repo,
    a plugin package, or a separate reusable repository.
  - Evidence: Pending.

## Phase 2: Deterministic Runtime MVP

- [ ] T004 Implement spec scanner and resources.
  - Depends on: T003
  - Files: implementation path TBD, `tests/`
  - Acceptance: `scan_specs`, `specs://active`, `specs://{spec_id}/summary`,
    and template resources return structured data for current and fixture
    specs.
  - Evidence: Pending.
  - [ ] T004.1 Discover active spec packages.
  - [ ] T004.2 Classify current versus old-format packages.
  - [ ] T004.3 Resolve effective templates.
  - [ ] T004.4 Expose MCP resources.

- [ ] T005 Implement artifact linters.
  - Depends on: T003
  - Files: implementation path TBD, `tests/`
  - Acceptance: `lint_doc` and `lint_spec_package` validate frontmatter,
    required sections, task evidence, dependency IDs, and optional artifact
    rules.
  - Evidence: Pending.
  - [ ] T005.1 Implement frontmatter and heading checks.
  - [ ] T005.2 Implement requirements checks.
  - [ ] T005.3 Implement design checks.
  - [ ] T005.4 Implement tasks checks.
  - [ ] T005.5 Implement optional artifact checks.
  - [ ] T005.6 Implement waiver parsing and reporting.

- [ ] T006 Implement next-task and closure checks.
  - Depends on: T004, T005
  - Files: implementation path TBD, `tests/`
  - Acceptance: `next_task` respects dependencies and evidence; `closure_check`
    reports verification, promotion, open-decision, and active-index blockers.
  - Evidence: Pending.

## Phase 3: Prompt And Hook Surfaces

- [ ] T007 Add MCP prompt definitions.
  - Depends on: T006
  - Files: implementation path TBD, prompt definition files TBD
  - Acceptance: `reconcile-spec`, `choose-next-task`, and `lint-spec` prompts
    are discoverable where client support exists and include clear arguments.
  - Evidence: Pending.

- [ ] T008 Add hook runner MVP.
  - Depends on: T006
  - Files: implementation path TBD, hook config path TBD, `tests/`
  - Acceptance: `spec-file-changed` and `task-checkbox-changed` can lint
    affected spec packages, detect completed tasks without evidence, and emit
    JSON plus human-readable output.
  - Evidence: Pending.
  - [ ] T008.1 Implement changed-spec artifact lint.
  - [ ] T008.2 Implement task checkbox evidence detection.
  - [ ] T008.3 Implement advisory versus blocking severity profiles.
  - [ ] T008.4 Add fixture coverage for changed files and task completion.

## Phase 4: Lifecycle Hook Gates

- [ ] T009 Add completion, verification, resume, and closure hooks.
  - Depends on: T008
  - Files: implementation path TBD, hook config path TBD, `tests/`
  - Acceptance: Hooks can check implementation task completion,
    verification-evidence updates, spec resume reconciliation, and spec closure
    readiness with clear blocking versus advisory behavior.
  - Evidence: Pending.
  - [ ] T009.1 Implement implementation task completion checks.
  - [ ] T009.2 Implement verification evidence mapping checks.
  - [ ] T009.3 Implement resume reconciliation hook.
  - [ ] T009.4 Implement closure readiness hook.

## Phase 5: Semantic Review And Promotion Planning

- [ ] T010 Add reconciliation, promotion planning, and review packets.
  - Depends on: T007, T009
  - Files: implementation path TBD, `tests/`
  - Acceptance: Tools generate classified drift reports, durable promotion
    targets, and bounded cheap-agent review packets.
  - Evidence: Pending.
  - [ ] T010.1 Implement `reconcile_spec`.
  - [ ] T010.2 Implement `promotion_plan`.
  - [ ] T010.3 Implement `generate_review_packet`.
  - [ ] T010.4 Record review-packet result disposition format.
  - [ ] T010.5 Implement agent-oriented hook candidates for
    `agent-slice-start`, `agent-response-check`, `review-packet-dispatch`, and
    `review-result-recorded`.

## Phase 6: Metrics, Governance, Dogfood, And Promote

- [ ] T011 Dogfood the MCP runtime on this spec and promote durable docs.
  - Depends on: T010
  - Files: `docs/specs/004-spec-management-mcp/`, durable docs TBD
  - Acceptance: Dogfood evidence records useful findings, overhead, prompt
    support limits, hook value, repeated waivers, governance-sensitive changes,
    and durable doc promotion targets.
  - Evidence: Pending.

## Related Artifacts

- Requirements: [requirements.md](requirements.md)
- Design: [design.md](design.md)
- Research: [research.md](research.md)
