---
title: Hierarchical spec authoring hooks tasks
doc_type: spec
artifact_type: tasks
status: active
owner: platform
last_reviewed: 2026-06-11
---

# Tasks

## Task Dependency Graph

T001 -> T002 -> T003 -> T004 -> T005 -> T006 -> T007

## Tasks

- [x] T001 Add backlog framing and open the focused spec.
  - Files: `docs/backlog/README.md`, `docs/specs/023-hierarchical-spec-authoring-hooks/`
  - Acceptance: B046 points to an active spec and the spec captures hierarchy-aware hook behavior.
  - Evidence: `docs/backlog/README.md` marks B046 active and this package defines requirements, design, tasks, traceability, and verification.

- [ ] T002 Add runtime spec-tree authoring context.
  - Depends on: T001
  - Files: `skills/spec-lifecycle-manager/scripts/spec_runtime.py`
  - Acceptance: Runtime can classify changed spec artifacts, prerequisites, downstream review candidates, next authoring step, and recommended helper surfaces.
  - Evidence: Pending.

- [ ] T003 Update runtime hook behavior.
  - Depends on: T002
  - Files: `skills/spec-lifecycle-manager/scripts/spec_runtime.py`
  - Acceptance: `spec-file-changed` uses hierarchy-aware authoring guidance for ordinary writes while explicit validation/resume/closure paths retain full package checks.
  - Evidence: Pending.

- [ ] T004 Update Codex hook wrapper output.
  - Depends on: T003
  - Files: `skills/spec-lifecycle-manager/scripts/codex_spec_lifecycle_hook.py`
  - Acceptance: `PostToolUse` additional context prefers concise next-action guidance and avoids unrelated package-wide diagnostic floods.
  - Evidence: Pending.

- [ ] T005 Add runtime and wrapper tests.
  - Depends on: T002, T003, T004
  - Files: `tests/runtime/test_spec_runtime.py`, `tests/runtime/test_codex_spec_lifecycle_hook.py`
  - Acceptance: Tests cover initial authoring, upstream revisions with downstream docs, task updates, explicit package validation, and wrapper context output.
  - Evidence: Pending.

- [ ] T006 Document hook modes and hierarchy guidance.
  - Depends on: T005
  - Files: `docs/reference/spec-lifecycle-runtime.md`
  - Acceptance: Runtime docs describe authoring, task-update, package-validation, resume, and closure hook behavior with helper resources.
  - Evidence: Pending.

- [ ] T007 Mirror bundles and validate.
  - Depends on: T006
  - Files: `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/`, `plugins/spec-lifecycle-manager/claude-plugin/skills/spec-lifecycle-manager/`
  - Acceptance: Source, Codex bundle, Claude bundle, sync guard, package contract, tests, scan, archive index, prompts, and whitespace checks pass.
  - Evidence: Pending.
