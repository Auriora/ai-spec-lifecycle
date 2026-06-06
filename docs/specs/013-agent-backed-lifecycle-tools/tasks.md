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
T001 -> T002 -> T003 -> T004 -> T005 -> T006
              \-> T007
T008 depends on T004-T007
```

## Phase 1: Scope and Contract

- [ ] T001 Select the first agent-backed tool for implementation.
  - Depends on: none
  - Files: `docs/specs/013-agent-backed-lifecycle-tools/design.md`, `docs/specs/013-agent-backed-lifecycle-tools/open-decisions.md`
  - Acceptance: Decision records whether the first tool is `closure_risk_review`, `draft_traceability_matrix`, `promotion_draft`, or `agent_readiness_packet`, with rationale.
  - Evidence: Pending.

- [ ] T002 Define the shared advisory result schema and validation rules.
  - Depends on: T001
  - Files: `skills/spec-lifecycle-manager/scripts/spec_runtime.py`, selected schema or prompt files
  - Acceptance: Schema captures status, advisory flag, packet metadata, observed facts, inferences, recommendations, gaps, confidence, diagnostics, and summary.
  - Evidence: Pending.

## Phase 2: Runtime and MCP

- [ ] T003 Implement bounded packet generation for the selected tool.
  - Depends on: T002
  - Files: `skills/spec-lifecycle-manager/scripts/spec_runtime.py`
  - Acceptance: Packet includes only relevant spec/durable context and treats reviewed documents as data.
  - Evidence: Pending.

- [ ] T004 Implement disabled/unavailable agent-runner behavior.
  - Depends on: T003
  - Files: `skills/spec-lifecycle-manager/scripts/spec_runtime.py`
  - Acceptance: Tool returns structured `unavailable` output without mutation when no runner is configured.
  - Evidence: Pending.

- [ ] T005 Expose the selected tool through MCP.
  - Depends on: T004
  - Files: `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`, `docs/reference/spec-lifecycle-runtime.md`
  - Acceptance: MCP tool schema marks the tool advisory/read-only and accepts needed inputs such as `spec_path`, `review_type`, and `model_class`.
  - Evidence: Pending.

## Phase 3: Validation and Guidance

- [ ] T006 Add deterministic validation and tests.
  - Depends on: T004, T005
  - Files: `tests/runtime/`, `skills/spec-lifecycle-manager/scripts/spec_runtime.py`
  - Acceptance: Tests cover valid schema, invalid output, disabled runner, removed spec handling, and no mutation.
  - Evidence: Pending.

- [ ] T007 Update durable docs and skill guidance.
  - Depends on: T005
  - Files: `docs/reference/spec-lifecycle-runtime.md`, `docs/design/spec-lifecycle-management.md`, `skills/spec-lifecycle-manager/SKILL.md`, optional `AGENTS.md`
  - Acceptance: Docs explain usage, guardrails, advisory limits, and future write-capable deferral.
  - Evidence: Pending.

## Phase 4: Closure

- [ ] T008 Reconcile, validate, promote, and close the spec.
  - Depends on: T006, T007
  - Files: `docs/specs/013-agent-backed-lifecycle-tools/verification.md`, `docs/history/spec-closure-log.md`, `docs/history/spec-archive-index.md`
  - Acceptance: Runtime checks, tests, prompts/archive validation, durable promotion, closure log, archive index, and package removal are complete.
  - Evidence: Pending.
