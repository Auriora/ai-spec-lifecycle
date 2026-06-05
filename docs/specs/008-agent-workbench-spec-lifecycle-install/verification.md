---
title: Agent Workbench spec lifecycle install verification
doc_type: spec
artifact_type: verification
status: draft
owner: platform
last_reviewed: 2026-06-05
---

# Verification

## Scope

This verification record covers spec 008 tasks T001 through T005: install
policy, Agent Workbench reference guidance, advisory hook policy, validation
checklist, and B002 backlog closure.

## Quality Gates

| Gate | Required? | Status | Evidence |
|------|-----------|--------|----------|
| Requirements acceptance criteria reviewed | yes | pass | Requirements 1-5 mapped to tasks and durable targets. |
| Task evidence complete | yes | pass | `tasks.md` records evidence for T001-T005. |
| Automated tests pass or alternate verification recorded | yes | pass | Live MCP smoke checks and docs hygiene checks recorded. |
| Durable documentation updates identified | yes | pass | Agent Workbench reference note and backlog update. |
| Durable documentation promoted or explicitly deferred | yes | pass | Install guidance promoted to Agent Workbench reference docs. |
| Spec cleanup decision recorded | yes | pass | Spec remains active until committed and closure-log cleanup can be decided. |
| Governance or policy conflicts resolved | yes | pass | Agent Workbench host-level MCP architecture preserved. |

## Validation Commands

| Command | Purpose | Result | Evidence |
|---------|---------|--------|----------|
| MCP `scan_specs` via `mcp__spec_lifecycle_manager.scan_specs` | Reload and scan smoke test | pass | Tool namespace visible; scan returned `agent-dev-lifecycle` inventory. |
| MCP `prompts_validate` via `mcp__spec_lifecycle_manager.prompts_validate` | Prompt/tool surface smoke test | pass | Four prompts returned with no diagnostics. |
| MCP `closure_check` on spec 007 | Closure tool smoke test | pass | Ready with no blockers. |
| `test -x ~/.codex/skills/spec-lifecycle-manager/scripts/spec_mcp_server.py` | Installed skill sync/executable check | pass | Installed server script executable. |
| `rg -n "spec-lifecycle-manager" ~/.codex/config.toml ~/.codex/plugins ../agent-workbench ...` | Duplicate-instance check | pass | Only host-level config, docs, and references found; no plugin-provided MCP server entry. |
| `git diff --check` in `agent-dev-lifecycle` | Docs hygiene | pass | No whitespace errors reported. |
| `git diff --check` in `agent-workbench` | Cross-repo docs hygiene | pass | No whitespace errors reported. |
| `mcp__spec_lifecycle_manager.lint_spec_package` on spec 008 | Spec package lint | pass | No diagnostics. |
| `mcp__spec_lifecycle_manager.closure_check` on spec 008 | Closure readiness | pass | Ready with no blockers. |

## Evidence Log

| Date | Evidence | Result | Notes |
|------|----------|--------|-------|
| 2026-06-05 | `mcp__spec_lifecycle_manager.scan_specs` | pass | Returned spec inventory for `/home/bcherrington/Projects/Auriora/agent-dev-lifecycle`. |
| 2026-06-05 | `mcp__spec_lifecycle_manager.prompts_validate` | pass | Returned four prompts and no diagnostics. |
| 2026-06-05 | `mcp__spec_lifecycle_manager.closure_check` on spec 007 | pass | Ready with no blockers. |
| 2026-06-05 | TOML parse and server lookup for `~/.codex/config.toml` | pass | Exactly one matching host-level server: `spec-lifecycle-manager`. |
| 2026-06-05 | Duplicate search across `~/.codex/config.toml`, `~/.codex/plugins`, and Agent Workbench plugin/config paths | pass | Found only host config plus documentation references. |
| 2026-06-05 | `test -x ~/.codex/skills/spec-lifecycle-manager/scripts/spec_mcp_server.py` | pass | Installed skill server script is executable. |
| 2026-06-05 | Manual stdio `initialize` request to installed server script | pass | Returned server name `spec-lifecycle-manager`. |
| 2026-06-05 | `git diff --check` in both repos | pass | No whitespace errors reported. |
| 2026-06-05 | MCP lint and closure-check for spec 008 | pass | No diagnostics and ready with no blockers. |

## Requirement Coverage

| Requirement | Acceptance criteria covered | Evidence | Residual risk |
|-------------|-----------------------------|----------|---------------|
| Requirement 1 | AC1, AC2, AC3 | Agent Workbench reference note and design | none |
| Requirement 2 | AC1, AC2, AC3 | `../agent-workbench/docs/reference/agent-dev-lifecycle/spec-lifecycle-manager-mcp-install.md` | none |
| Requirement 3 | AC1, AC2, AC3 | Advisory-only hook policy in Agent Workbench reference note | Blocking hook promotion remains future work by design. |
| Requirement 4 | AC1, AC2, AC3 | MCP smoke checks and duplicate-instance checks | Duplicate check is local to known config/plugin paths. |
| Requirement 5 | AC1, AC2 | `docs/backlog/README.md` B002 status | none |

## Residual Risks

- Blocking spec lifecycle hooks are not installed; they require a later
  dogfood pass and explicit promotion decision.
- The install guidance targets the local Codex host configuration. Other MCP
  clients may need equivalent host-level configuration.

## Task Evidence

| Task ID | Status | Evidence | Notes |
|---------|--------|----------|-------|
| T001 | complete | Spec package created. | Five-task package created. |
| T002 | complete | Install boundary documented. | Host-level companion server model recorded. |
| T003 | complete | Agent Workbench reference guidance added. | Config snippet and validation checklist included. |
| T004 | complete | Hook policy documented. | Advisory-only by default; blocking requires later decision. |
| T005 | complete | Validation evidence recorded; B002 marked done. | Final command results updated after execution. |

## Durable Promotion And Cleanup

| Spec content | Durable destination or deferral | Status | Evidence |
|--------------|---------------------------------|--------|----------|
| Agent Workbench install guidance | `../agent-workbench/docs/reference/agent-dev-lifecycle/spec-lifecycle-manager-mcp-install.md` | complete | Reference note added. |
| Hook install policy | Agent Workbench reference note | complete | Advisory-only policy documented. |
| Backlog B002 | `docs/backlog/README.md` | complete | Item marked done. |
| Blocking hook promotion | future spec or backlog item | deferred | Residual risk recorded. |

### Spec Cleanup Decision

- **Cleanup action:** retain as active until committed
- **Reason:** The package records the cross-repo install-policy evidence.
- **Final spec commit:** pending
- **Closure log path:** `docs/history/spec-closure-log.md`
- **Closure log entry updated:** no
- **Closure cleanup commit:** pending
- **Active indexes updated:** yes
- **Durable docs linked back to evidence where useful:** yes
- **Residual spec-only content:** Implementation evidence remains in spec 008
  until closure.

## Ship Or Closure Risk

- **Risk level:** low
- **Breaking change:** no
- **Blast radius checked:** yes
- **Rollback path:** revert documentation and backlog changes
- **Requires human review:** optional
- **Release notes needed:** no
- **Follow-up issue or spec needed:** yes, only if blocking hooks are promoted

## Readiness Decision

- **Ready for promotion:** yes
- **Ready for release:** yes
- **Ready for closure:** yes.

## Related Artifacts

- Requirements: requirements.md
- Design: design.md
- Tasks: tasks.md
- Traceability: traceability.md
