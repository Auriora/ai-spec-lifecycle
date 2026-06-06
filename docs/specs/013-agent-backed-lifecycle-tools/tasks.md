---
title: Agent-backed lifecycle tools tasks
doc_type: spec
artifact_type: tasks
status: draft
owner: platform
last_reviewed: 2026-06-06
---

# Tasks

## Task Dependency Graph

```text
T001 -> T002 -> T003 -> T005 -> T006
T004 -> T006
T007 depends on T005
T008 depends on T004-T007
```

## Phase 1: Scope and Contract

- [x] T001 Select the first foundation tools for implementation.
  - Depends on: none
  - Files: `docs/specs/013-agent-backed-lifecycle-tools/design.md`, `docs/specs/013-agent-backed-lifecycle-tools/open-decisions.md`
  - Acceptance: Decision records whether the first tool is `closure_risk_review`, `draft_traceability_matrix`, `promotion_draft`, `agent_readiness_packet`, or a deterministic foundation tool, with rationale.
  - Evidence: D001 accepted deterministic `active_spec_preflight`, `agent_readiness_packet`, and `no_active_spec_context` as the first implementation slice.

- [x] T002 Define deterministic workflow payload schemas.
  - Depends on: T001
  - Files: `skills/spec-lifecycle-manager/scripts/spec_runtime.py`
  - Acceptance: Payloads capture status, selected spec, next task, readiness context, no-active context, guidance, gaps, and validation commands.
  - Evidence: Implemented deterministic payload builders in `spec_runtime.py` for active preflight, readiness packets, and no-active-spec context.

## Phase 2: Runtime and MCP

- [x] T003 Implement bounded packet generation for deterministic foundation tools.
  - Depends on: T002
  - Files: `skills/spec-lifecycle-manager/scripts/spec_runtime.py`
  - Acceptance: Packet includes only relevant spec/durable context and treats reviewed documents as data.
  - Evidence: `agent_readiness_packet` returns task-specific requirements, design, verification, durable targets, open decisions, guardrails, and validation commands; `no_active_spec_context` returns durable docs/history context.

- [x] T004 Implement disabled/unavailable agent-runner behavior.
  - Depends on: T003
  - Files: `skills/spec-lifecycle-manager/scripts/spec_runtime.py`, `skills/spec-lifecycle-manager/scripts/spec_agent_schemas.py`
  - Acceptance: Tool returns structured `unavailable` output without mutation when no runner is configured, uses a separate Python schema module, and leaves local Codex CLI runner support deferred.
  - Evidence: Added `spec_agent_schemas.py`, `agent_backed_tool`, `agent-backed-tool` CLI, and MCP `agent_backed_tool`; targeted runtime and MCP tests passed on 2026-06-06.

- [x] T005 Expose foundation tools through MCP.
  - Depends on: T003
  - Files: `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`, `docs/reference/spec-lifecycle-runtime.md`
  - Acceptance: MCP tool schema marks the tool advisory/read-only and accepts needed inputs such as `spec_path`, `review_type`, and `model_class`.
  - Evidence: MCP now exposes `active_spec_preflight`, `agent_readiness_packet`, and `no_active_spec_context` as read-only deterministic tools.

## Phase 3: Validation and Guidance

- [x] T006 Add deterministic validation and tests.
  - Depends on: T003, T005
  - Files: `tests/runtime/`, `skills/spec-lifecycle-manager/scripts/spec_runtime.py`
  - Acceptance: Tests cover valid payloads, no-active behavior, MCP exposure, and no mutation for deterministic foundation tools.
  - Evidence: Added runtime and MCP tests for active preflight, agent readiness packet, and no-active-spec context.

- [x] T007 Update durable docs and skill guidance.
  - Depends on: T005
  - Files: `docs/reference/spec-lifecycle-runtime.md`, `docs/design/spec-lifecycle-management.md`, `docs/reviews/spec-lifecycle-manager/`, `skills/spec-lifecycle-manager/SKILL.md`, optional `AGENTS.md`
  - Acceptance: Docs explain usage, guardrails, advisory limits, persisted review locations, and future write-capable deferral.
  - Evidence: Updated runtime reference, lifecycle design, skill guidance, and `docs/reviews/spec-lifecycle-manager/README.md`; lifecycle lint and full test suite passed on 2026-06-06.

## Phase 4: Closure

- [x] T008 Reconcile, validate, promote, and close the spec.
  - Depends on: T006, T007
  - Files: `docs/specs/013-agent-backed-lifecycle-tools/verification.md`, `docs/history/spec-closure-log.md`, `docs/history/spec-archive-index.md`
  - Acceptance: Runtime checks, tests, prompts/archive validation, durable promotion, closure log, archive index, and package removal are complete.
  - Evidence: Final validation passed on 2026-06-06; durable promotion completed in runtime docs, lifecycle design, skill guidance, review docs, runtime code, MCP adapter, and tests. Closure log, archive index, and package removal are handled by the cleanup commit after this final spec state is committed.
