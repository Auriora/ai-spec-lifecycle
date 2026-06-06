---
title: Agent Workbench spec lifecycle install tasks
doc_type: spec
artifact_type: tasks
status: archived
owner: platform
last_reviewed: 2026-06-05
---

# Tasks

**Input**: `docs/backlog/README.md`,
`docs/reference/spec-lifecycle-runtime.md`,
`../agent-workbench/docs/design/coding-agent-integration-design.md`, and
`../agent-workbench/docs/runbooks/codex-agent-workbench-plugin.md`.

## Task Dependency Graph

```text
T001 -> T002
T002 -> T003
T003 -> T004
T004 -> T005
```

## Phase 1: Install Spec

- [x] T001 Create spec 008 for Agent Workbench spec lifecycle install.
  - Depends on: none
  - Files: `docs/specs/008-agent-workbench-spec-lifecycle-install/`
  - Acceptance: Spec package records requirements, design, tasks,
    traceability, and verification for the five install tasks.
  - Evidence: Spec package created.

## Phase 2: Install Model

- [x] T002 Define Agent Workbench install boundary.
  - Depends on: T001
  - Files: `docs/specs/008-agent-workbench-spec-lifecycle-install/design.md`,
    `docs/reference/spec-lifecycle-manager-mcp-install.md`
  - Acceptance: Guidance states the spec lifecycle MCP server is a separate
    host-level companion server and Agent Workbench plugin must not register or
    copy it.
  - Evidence: Design and local reference note document the boundary.

- [x] T003 Add Agent Workbench reference guidance.
  - Depends on: T002
  - Files:
    `docs/reference/spec-lifecycle-manager-mcp-install.md`
  - Acceptance: Reference note includes config snippet, install/sync path,
    validation checklist, and duplicate-instance checks.
  - Evidence: Local reference note added under `docs/reference/`.

- [x] T004 Decide hook install policy.
  - Depends on: T003
  - Files:
    `docs/reference/spec-lifecycle-manager-mcp-install.md`,
    `docs/specs/008-agent-workbench-spec-lifecycle-install/design.md`
  - Acceptance: Hooks are advisory-only by default; blocking hooks require a
    later dogfood pass and explicit promotion decision.
  - Evidence: Hook policy documented in design and external Agent Workbench
    reference note.

## Phase 3: Validation And Backlog

- [x] T005 Add validation checklist and close B002.
  - Depends on: T004
  - Files: `docs/specs/008-agent-workbench-spec-lifecycle-install/verification.md`,
    `docs/backlog/README.md`
  - Acceptance: Verification records reload/tool visibility, scan behavior,
    installed skill sync, duplicate-instance check, and docs hygiene; B002 is
    marked done or replaced by a precise follow-up.
  - Evidence: Verification records live MCP smoke checks; B002 marked done.

## Related Artifacts

- Requirements: requirements.md
- Design: design.md
- Traceability: traceability.md
- Verification: verification.md
