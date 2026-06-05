---
title: Spec lifecycle MCP server tasks
doc_type: spec
artifact_type: tasks
status: draft
owner: platform
last_reviewed: 2026-06-05
---

# Tasks

**Input**: `requirements.md`, `design.md`,
`docs/specs/004-spec-management-mcp/`, `docs/reference/spec-lifecycle-runtime.md`,
and `skills/spec-lifecycle-manager/scripts/`.

## Task Dependency Graph

```text
T001 -> T002
T002 -> T003
T003 -> T004
T004 -> T005
T005 -> T006
T006 -> T007
```

## Phase 1: Spec Baseline

- [x] T001 Create MCP server implementation spec.
  - Depends on: none
  - Files: `docs/specs/007-spec-lifecycle-mcp-server/`
  - Acceptance: Requirements, design, tasks, traceability, and verification
    define a read-only stdio MCP server adapter.
  - Evidence: Spec package created.

## Phase 2: Server Implementation

- [x] T002 Add dependency-free stdio MCP server.
  - Depends on: T001
  - Files: `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`
  - Acceptance: Server handles initialize, tools, resources, prompts, ping,
    JSON-RPC errors, and notifications without write tools.
  - Evidence: Server script added and focused MCP tests pass.

- [x] T003 Expose runtime helpers as MCP tools.
  - Depends on: T002
  - Files: `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`
  - Acceptance: Tools wrap scan, summary, lint, next-task, closure,
    reconciliation, promotion, review packet, traceability, and prompt
    validation helpers.
  - Evidence: `tools/list` and `tools/call scan_specs` tested; dispatch
    delegates to existing runtime helpers.

- [x] T004 Expose resources and prompts.
  - Depends on: T003
  - Files: `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`
  - Acceptance: Server lists and reads active spec resources, and lists/gets
    prompt definitions from the existing prompt JSON files.
  - Evidence: Resource and prompt subprocess tests pass.

## Phase 3: Tests And Durable Docs

- [x] T005 Add MCP server tests.
  - Depends on: T004
  - Files: `tests/runtime/test_spec_mcp_server.py`
  - Acceptance: Tests cover initialize, tools, resources, prompts, and invalid
    tool errors.
  - Evidence: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_spec_mcp_server` passed.

- [x] T006 Promote install and runtime docs.
  - Depends on: T005
  - Files: `docs/reference/spec-lifecycle-runtime.md`, `docs/README.md`,
    `skills/spec-lifecycle-manager/SKILL.md`, `docs/backlog/README.md`,
    `docs/history/spec-closure-log.md`
  - Acceptance: Durable docs describe the MCP server command, capability
    surface, read-only boundary, and installed-skill command.
  - Evidence: Runtime docs, docs index, skill guidance, closure-log residual
    status, and backlog follow-up updated.

## Phase 4: Validation

- [x] T007 Validate and record evidence.
  - Depends on: T006
  - Files: `docs/specs/007-spec-lifecycle-mcp-server/verification.md`
  - Acceptance: Focused MCP tests, full unit tests, spec lint, closure-check,
    and whitespace checks pass or record explicit residual risk.
  - Evidence: Verification records passing commands.

## Related Artifacts

- Requirements: requirements.md
- Design: design.md
- Traceability: traceability.md
- Verification: verification.md
