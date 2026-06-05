---
title: Spec lifecycle MCP server verification
doc_type: spec
artifact_type: verification
status: draft
owner: platform
last_reviewed: 2026-06-05
---

# Verification

## Scope

This verification record covers spec 007 implementation tasks T001 through
T007: dependency-free stdio MCP server adapter, runtime tool exposure,
resources, prompts, tests, durable docs, and install guidance.

## Quality Gates

| Gate | Required? | Status | Evidence |
|------|-----------|--------|----------|
| Requirements acceptance criteria reviewed | yes | pass | Requirements 1-5 mapped to server, tests, and docs. |
| Task evidence complete | yes | pass | `tasks.md` records evidence for T001-T007. |
| Automated tests pass or alternate verification recorded | yes | pass | Focused MCP tests and full runtime tests passed. |
| Durable documentation updates identified | yes | pass | Runtime reference, docs index, skill guidance, closure log, and backlog updated. |
| Durable documentation promoted or explicitly deferred | yes | pass | Install and runtime guidance promoted. |
| Spec cleanup decision recorded | yes | pass | Spec remains active until committed and closure-log cleanup can be decided. |
| Governance or policy conflicts resolved | yes | pass | Server is read-only and does not replace skill authority. |

## Validation Commands

| Command | Purpose | Result | Evidence |
|---------|---------|--------|----------|
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_spec_mcp_server` | Focused MCP server tests | pass | 5 tests passed. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'` | Full regression tests | pass | 36 tests passed. |
| `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py lint docs/specs/007-spec-lifecycle-mcp-server` | Spec package lint | pass | No diagnostics. |
| `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py closure-check docs/specs/007-spec-lifecycle-mcp-server` | Closure readiness | pass | Ready with no blockers. |
| `git diff --check` | Diff whitespace hygiene | pass | No whitespace errors reported. |

## Evidence Log

| Date | Evidence | Result | Notes |
|------|----------|--------|-------|
| 2026-06-05 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_spec_mcp_server` | pass | 5 focused MCP protocol tests passed. |
| 2026-06-05 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'` | pass | 36 tests passed. |
| 2026-06-05 | `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py lint docs/specs/007-spec-lifecycle-mcp-server` | pass | No diagnostics. |
| 2026-06-05 | `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py closure-check docs/specs/007-spec-lifecycle-mcp-server` | pass | Ready with no blockers. |
| 2026-06-05 | `git diff --check` | pass | No whitespace errors reported. |

## Requirement Coverage

| Requirement | Acceptance criteria covered | Evidence | Residual risk |
|-------------|-----------------------------|----------|---------------|
| Requirement 1 | AC1, AC2, AC3 | `spec_mcp_server.py`; focused MCP tests | Minimal JSON-RPC subset. |
| Requirement 2 | AC1, AC2, AC3 | Tool dispatch delegates to runtime helpers | Individual helper branches not exhaustively protocol-tested. |
| Requirement 3 | AC1, AC2, AC3 | Resource and prompt tests | Client support for prompts varies by MCP client. |
| Requirement 4 | AC1, AC2, AC3 | Read-only server implementation | Future write tools require separate design. |
| Requirement 5 | AC1, AC2, AC3 | Runtime docs, skill guidance, validation, backlog B002 | Agent Workbench plugin packaging remains future work. |

## Residual Risks

- The adapter implements the local stdio JSON-RPC subset needed for tools,
  resources, and prompts; it does not use an MCP SDK.
- Hook installation into Git, Codex, or Agent Workbench is still future work
  tracked in backlog B002.
- Packaging as a reusable plugin remains future work tracked in backlog B002.

## Task Evidence

| Task ID | Status | Evidence | Notes |
|---------|--------|----------|-------|
| T001 | complete | Spec package created. | Includes requirements, design, tasks, traceability, and verification. |
| T002 | complete | `spec_mcp_server.py` added. | Handles initialize, ping, tools, resources, prompts, errors, and notifications. |
| T003 | complete | Runtime tools exposed through `tools/list` and `tools/call`. | Delegates to `spec_runtime.py` and `traceability_lookup.py`. |
| T004 | complete | Resources and prompts exposed. | Focused tests cover `specs://active` and `task-context` prompt. |
| T005 | complete | MCP server tests added. | 5 focused tests passed. |
| T006 | complete | Runtime docs, docs index, skill guidance, closure log, and backlog updated. | Install commands documented; B002 tracks packaging/hook install. |
| T007 | complete | Validation commands recorded. | Final command results updated after execution. |

## Durable Promotion And Cleanup

| Spec content | Durable destination or deferral | Status | Evidence |
|--------------|---------------------------------|--------|----------|
| MCP server command and capabilities | `docs/reference/spec-lifecycle-runtime.md` | complete | Runtime reference updated. |
| Installed skill command | `skills/spec-lifecycle-manager/SKILL.md` | complete | MCP section added. |
| User-facing install note | `docs/README.md` | complete | MCP server command documented. |
| Plugin packaging and hook install | `docs/backlog/README.md` B002 | deferred | Backlog item recorded. |

### Spec Cleanup Decision

- **Cleanup action:** retain as active until committed
- **Reason:** The package records implementation evidence for the MCP server
  adapter.
- **Final spec commit:** pending
- **Closure log path:** `docs/history/spec-closure-log.md`
- **Closure log entry updated:** no
- **Closure cleanup commit:** pending
- **Active indexes updated:** yes
- **Durable docs linked back to evidence where useful:** yes
- **Residual spec-only content:** Implementation evidence remains in spec 007
  until closure.

## Ship Or Closure Risk

- **Risk level:** medium
- **Breaking change:** no
- **Blast radius checked:** yes
- **Rollback path:** remove `spec_mcp_server.py`, tests, and docs updates
- **Requires human review:** yes before broad installation
- **Release notes needed:** no
- **Follow-up issue or spec needed:** yes, backlog B002 for plugin packaging
  and hook install

## Readiness Decision

- **Ready for promotion:** yes
- **Ready for release:** yes
- **Ready for closure:** yes.

## Related Artifacts

- Requirements: requirements.md
- Design: design.md
- Tasks: tasks.md
- Traceability: traceability.md
