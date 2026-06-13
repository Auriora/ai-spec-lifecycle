---
title: Validation plan builder design
doc_type: spec
artifact_type: design
status: active
owner: platform
last_reviewed: 2026-06-13
---

# Design

## Overview

Add a deterministic `validation_plan` runtime/MCP surface. The planner maps
changed files and optional task context to checks already supported by this
repository.

## High-Level Design

- Add `validation_plan(repo_root, changed_files, spec_path, task_id, risk_level)`.
- Classify changed files by repo-relative path prefixes and suffixes.
- Compose recommendations from existing commands and MCP tools.
- Include baseline checks for lifecycle, package, plugin, and docs contexts.
- Classify each check as required, recommended, optional, not applicable, or
  not run so doc-only changes do not create false validation noise.

## Low-Level Design

- File classification stays table-driven inside `spec_runtime.py`.
- Plan items use stable IDs such as `unit-tests`, `scan`, `archive-index`,
  `prompts`, `package-contract`, `sync-guard`, `npm-pack-dry-run`, and
  `git-diff-check`.
- Each item includes `required`, `reason`, `covers`, `command`, and optional
  `mcp_tool`.
- Each item also includes a normalized `status` or `applicability` field:
  `required`, `recommended`, `optional`, `not_applicable`, or `not_run`.
- `not_applicable` means the changed-file/task context does not require the
  check. `not_run` means the check applies but has not executed or is blocked by
  missing inputs, credentials, tools, or environment.
- If `task_id` is supplied, the planner uses existing traceability lookup and
  reports gaps instead of failing.

Documentation-only changes should normally require `scan`, relevant package
lint, archive or prompt checks when those documents changed, and
`git-diff-check`. They should not require code unit tests unless the changed
docs are validation evidence for code behavior or the selected task acceptance
requires code validation.

## Operational Considerations

- The planner is advisory; users decide which commands to run.
- Target repositories can extend validation manually until project-specific
  validator configuration exists.

## Open Questions

- Future work can add repo-local validation profiles once this generic planner
  proves useful.
