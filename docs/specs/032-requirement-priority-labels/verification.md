---
title: Requirement priority labels verification
doc_type: spec
artifact_type: verification
status: draft
authoring_mode: wizard
lifecycle_stage: verify
owner: platform
last_reviewed: 2026-07-05
backlog_item: B057
---

# Verification

## Scope

This verification record covers spec 032, Requirement priority labels. It maps
the quality gates, correctness properties, task checkpoints, residual risks,
and closure readiness checks needed before implementation can be accepted and
the temporary spec package can close.

## Quality Gates

| Gate | Required? | Status | Evidence |
|------|-----------|--------|----------|
| Parser and lint behavior covers Requirement 1, Requirement 2, CP-001, and CP-005 | yes | pending | T004 evidence after focused parser and lint tests. |
| Readiness and closure semantics cover Requirement 3, CP-002, CP-003, and CP-004 | yes | pending | T008 evidence after focused readiness and closure tests. |
| Traceability and MCP propagation cover Requirement 3 AC4, Requirement 4 AC2, CP-004, and CP-005 | yes | pending | T011 evidence after runtime and MCP tests. |
| Prompt, template, source-skill, and bundled-plugin parity cover Requirement 4 AC1 and AC3 | yes | pending | T015 and T016 evidence after prompt validation, package-contract, and sync-guard. |
| Full repository validation covers Requirement 4 AC3 and AC4 | yes | pending | T017 evidence from `npm run validate` or recorded waiver. |
| Closure readiness covers all requirements and correctness properties | yes | pending | T018 evidence from MCP `closure_check`, implementation review, promotion disposition, and archive/closure validation. |

## Validation Commands

| Command | Purpose | Result | Evidence |
|---------|---------|--------|----------|
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_spec_runtime` | Focused parser, lint, readiness, closure, and traceability runtime checks. | pending | T004, T008, T016 |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_spec_runtime tests.runtime.test_spec_mcp_server` | Focused runtime plus MCP propagation checks. | pending | T011, T016 |
| `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py prompts .` | Prompt definition validation. | pending | T015, T016 |
| `npm run validate` | Repository validation bundle including package-contract and sync-guard. | pending | T017 |
| `git diff --check` | Whitespace validation before commit and closure. | pending | T016, T017 |
| MCP `lint_spec_package` | Lifecycle package lint for spec 032. | pending | T016, T018 |
| MCP `stage_readiness` | Implementation readiness check for spec 032. | pending | T016 |
| MCP `closure_check` | Closure readiness check for spec 032. | pending | T018 |

## Requirement Coverage

| Requirement | Acceptance criteria covered | Evidence | Residual risk |
|-------------|-----------------------------|----------|---------------|
| Requirement 1 | AC1, AC2, AC3, AC4, AC5, AC6 | Parser, lint, template, and traceability validation through T001-T004, T012, T016, and T018. | Pending until parser and template evidence is recorded. |
| Requirement 2 | AC1, AC2, AC3 | Backward-compatibility fixtures, historical package behavior, and template validation through T001, T003, T004, T012, T016, and T018. | Pending until unlabeled active and historical fixtures pass. |
| Requirement 3 | AC1, AC2, AC3, AC4, AC5 | Coverage disposition, readiness, closure, traceability, and agent-context validation through T005-T011, T014, T016, and T018. | Pending until runtime/MCP coverage behavior is implemented and tested. |
| Requirement 4 | AC1, AC2, AC3, AC4 | Prompt, structured-output, package parity, fixture, and full validation through T009-T017. | Existing released package may lag source behavior until release packaging runs. |

## Correctness Property Coverage

| Property | Covered by | Evidence | Residual risk |
|----------|------------|----------|---------------|
| CP-001 | T001, T003, T004, T016 | Parser/lint tests for unlabeled active and historical specs. | Pending until T004/T016 evidence. |
| CP-002 | T005, T006, T007, T008, T016 | Runtime coverage tests for incomplete `must-have` requirements. | Pending until T008/T016 evidence. |
| CP-003 | T005, T006, T007, T008, T016 | Runtime coverage tests for routed `could-have` requirements. | Pending until T008/T016 evidence. |
| CP-004 | T002, T007, T009, T010, T011, T016 | Runtime/MCP payload tests for priority propagation. | Pending until T011/T016 evidence. |
| CP-005 | T001, T002, T009, T010, T016 | Parser and traceability tests showing acceptance criteria inherit parent requirement priority. | Pending until T010/T016 evidence. |

## Scope Reconciliation Before Closure

| Broad requirement, design target, or review finding | Implemented in this spec | Coverage state | Deferred or rejected work | Destination | Blocks closure? | Evidence |
|-----------------------------------------------------|--------------------------|----------------|---------------------------|-------------|-----------------|----------|
| Requirement-level MoSCoW metadata syntax and parser | T001-T004, T012 | not-covered | none | none | yes | Pending task evidence. |
| Priority-aware readiness and closure semantics | T005-T008, T014, T018 | not-covered | none | none | yes | Pending task evidence. |
| Priority propagation through traceability, MCP, and agent context | T009-T011 | not-covered | none | none | yes | Pending task evidence. |
| Prompt, template, source skill, runtime docs, and bundled plugin parity | T012-T017 | not-covered | none | none | yes | Pending task evidence. |

## Agent Readiness Evidence

| Field | Evidence | Residual risk |
|-------|----------|---------------|
| Scope and out-of-scope files | Scope is limited to parser/runtime, traceability/MCP payloads, prompts/templates, durable docs, tests, and plugin bundle parity listed in `tasks.md`. New MCP tools and task-status semantic rewrites are out of scope. | None identified before implementation. |
| Must-read and optional context | Must read `requirements.md`, `design.md`, `tasks.md`, `traceability.md`, this verification record, and linked durable docs for the selected task. | Context may need refresh after upstream artifact edits. |
| Permissions and approval points | Normal repo edits are allowed for selected task files; no external services or secrets are required. Human decision required only if implementation would change accepted scope or closure semantics beyond this design. | None identified before implementation. |
| Validation commands and expected signals | Focused runtime/MCP tests, prompt validation, package-contract, sync-guard, full validation, lifecycle lint/readiness/closure checks, and `git diff --check`. | Full validation may reveal unrelated existing failures that need recorded disposition. |
| Review needs | Developer review before implementation, implementation review before closure, and closure check after durable promotion. | Review findings may require task updates before closure. |
| Durable-doc or closure impact | Durable docs and backlog targets are listed in `requirements.md#durable-impact` and `traceability.md#requirement-to-delivery-matrix`. | B057 must not be marked complete until implementation and durable promotion are accepted. |

## Task Evidence

| Task ID | Status | Evidence | Notes |
|---------|--------|----------|-------|
| T001 | pending | | Parser fixture tests not started. |
| T002 | pending | | Shared parser implementation not started. |
| T003 | pending | | Requirements lint integration not started. |
| T004 | pending | | Parser checkpoint evidence not recorded. |
| T005 | pending | | Coverage disposition tests not started. |
| T006 | pending | | Coverage helper implementation not started. |
| T007 | pending | | Readiness and closure integration not started. |
| T008 | pending | | Readiness and closure checkpoint evidence not recorded. |
| T009 | pending | | Traceability/MCP tests not started. |
| T010 | pending | | Traceability/MCP propagation not started. |
| T011 | pending | | Agent-context checkpoint evidence not recorded. |
| T012 | pending | | Source template updates not started. |
| T013 | pending | | Prompt and skill guidance updates not started. |
| T014 | pending | | Durable runtime/lifecycle documentation not started. |
| T015 | pending | | Bundled plugin parity validation not started. |
| T016 | pending | | Focused validation consolidation not started. |
| T017 | pending | | Full validation not started. |
| T018 | pending | | Implementation review, promotion, and closure preparation not started. |

## Evidence Log

| Date | Evidence | Result | Notes |
|------|----------|--------|-------|
| 2026-07-05 | Verification artifact created and traceability mappings updated before implementation. | pending validation | Addresses readiness finding that CP-001 through CP-005 lacked verification mapping and checkpoint tasks referenced a missing artifact. |

## Manual Or External Verification

No manual or external verification has been performed yet.

## Residual Risks

- Existing released npm package may lag source behavior until the package
  release workflow runs. Track during T015-T017 and release/package workflow.
- Priority semantics rely on traceability coverage rows being maintained
  accurately. T018 must reconcile broad requirements against task evidence
  before closure.
- Task-state audit broad-task information may remain because parent tasks group
  subtasks and checkpoints. Split further only if implementation evidence
  becomes ambiguous.

## Durable Promotion And Cleanup

| Spec content | Durable destination or deferral | Status | Evidence |
|--------------|---------------------------------|--------|----------|
| Requirements and accepted priority behavior | `skills/spec-lifecycle-manager/references/spec-package/requirements.md`, `docs/design/spec-lifecycle-management.md` | pending | T012, T014 |
| Runtime/MCP behavior | `docs/reference/spec-lifecycle-runtime.md` | pending | T014 |
| Prompt behavior | `skills/spec-lifecycle-manager/prompts/` and bundled plugin copies | pending | T013, T015 |
| Decisions and rationale | Durable design/reference docs and closure log at closure | pending | T018 |
| Follow-up work | `docs/backlog/README.md` or follow-up spec if discovered | pending | T018 |

### Spec Cleanup Decision

- **Cleanup action:** remove after durable promotion and final spec commit
- **Reason:** Active spec packages are temporary delivery scaffolding.
- **Final spec commit:** pending
- **Closure log path:** `docs/history/spec-closure-log.md`
- **Closure log entry updated:** no
- **Closure cleanup commit:** pending
- **Active indexes updated:** no
- **Durable docs linked back to evidence where useful:** no
- **Residual spec-only content:** listed below

Residual spec-only content:

- Pending implementation evidence and closure reconciliation remain in this
  spec until T018 completes.

## Ship Or Closure Risk

- **Risk level:** medium
- **Breaking change:** no
- **Blast radius checked:** no
- **Rollback path:** not required
- **Requires human review:** yes
- **Release notes needed:** no
- **Follow-up issue or spec needed:** no

### Risk Rationale

Risk is medium because this changes shared lifecycle parsing, closure guidance,
agent-facing structured output, prompts, templates, and bundled plugin copies.
The design avoids breaking unlabeled specs and defers no accepted must-have
behavior.

## Readiness Decision

- **Ready for promotion:** no
- **Ready for release:** no
- **Ready for closure:** no

## Related Artifacts

- Requirements: `requirements.md`
- Change Impact: embedded in `requirements.md`
- Design: `design.md`
- Tasks: `tasks.md`
- Traceability: `traceability.md`
