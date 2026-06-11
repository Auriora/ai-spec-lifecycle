---
title: Commit sync guard tasks
doc_type: tasks
artifact_type: tasks
status: active
owner: platform
last_reviewed: 2026-06-11
---

# Commit Sync Guard Tasks

## Task Dependency Graph

```text
T001 -> T002 -> T003 -> T004
```

## Tasks

- [x] T001 Define focused spec scope for B016/R005.
  - Files: `docs/specs/016-commit-sync-guard/`
  - Requirement: Requirements 1-4, Requirement 1A
  - Acceptance: Requirements, design, tasks, change impact, and verification
    describe package-repo applicability, source/bundle parity, bundle/cache
    parity, MCP reload advisory, commit evidence, and read-only behavior.
  - Evidence: Created this spec package.

- [x] T002 Implement read-only sync guard runtime command.
  - Depends on: T001
  - Requirement: Requirements 1-4, Requirement 1A
  - Files: `skills/spec-lifecycle-manager/scripts/spec_runtime.py`
  - Acceptance: `sync-guard` returns deterministic JSON for parity, cache,
    applicability, reload advisory, commit evidence, findings, summary, and
    recommendations.
  - Evidence: `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py sync-guard . --commits 5` returned applicability `applicable`, source/bundle parity `in_sync`, installed cache drift warning, reload advisory, and recent commit evidence.

- [x] T003 Add focused runtime tests.
  - Depends on: T002
  - Requirement: Requirements 1-4, Requirement 1A
  - Files: `tests/runtime/test_spec_runtime.py` or focused runtime tests
  - Acceptance: Tests cover in-sync fixtures, source/bundle drift,
    not-applicable target repos, bundle/cache drift or missing cache, and
    commit evidence checks.
  - Evidence: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_spec_runtime tests.runtime.test_spec_plugin_package` passed 47 tests; full `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'` passed 73 tests.

- [x] T004 Promote validation and install docs.
  - Depends on: T002
  - Requirement: Requirements 1-4, Requirement 1A
  - Files: `docs/reference/spec-lifecycle-runtime.md`,
    `docs/reference/spec-lifecycle-manager-mcp-install.md`,
    `docs/backlog/README.md`, `docs/roadmap/README.md`
  - Acceptance: Docs list `sync-guard` as a validation/install check and route
    B016/R005 state accurately.
  - Evidence: Updated `docs/reference/spec-lifecycle-runtime.md`, `docs/reference/spec-lifecycle-manager-mcp-install.md`, `docs/backlog/README.md`, and `docs/roadmap/README.md`; `git diff --check` passed.
