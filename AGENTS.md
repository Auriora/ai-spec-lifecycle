# Repository Guidelines

## Project Structure & Module Organization

This repository maintains the `spec-lifecycle-manager` skill and supporting
documentation. Durable project docs live under `docs/`: `design/`,
`governance/`, `reference/`, `history/`, `backlog/`, and `roadmap/`. Active
implementation specs, when present, live in `docs/specs/`; closed spec history
is recorded in `docs/history/spec-closure-log.md` and
`docs/history/spec-archive-index.md`. Skill source lives in
`skills/spec-lifecycle-manager/`, with Python runtime helpers in
`skills/spec-lifecycle-manager/scripts/`, MCP prompt definitions in
`skills/spec-lifecycle-manager/prompts/`, and fallback templates in
`skills/spec-lifecycle-manager/references/`. Tests live in `tests/`, with
fixtures under `tests/fixtures/`.

## Build, Test, and Development Commands

In Codex sessions where the `spec-lifecycle-manager` MCP server is available,
prefer MCP tools for lifecycle context (`scan_specs`, `active_spec_preflight`,
`task_context`, `traceability_lookup`, `closure_check`, `archive_index`, and
`prompts_validate`). The direct Python commands below are for validation, CI,
explicit recovery when MCP is unavailable, and runtime debugging.

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'`:
  run the full test suite.
- `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py scan .`:
  inspect spec inventory and active health.
- `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py archive-index .`:
  validate closed-spec archive metadata.
- `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py prompts`:
  validate MCP prompt definitions.
- `git diff --check`: catch whitespace issues before commit.

## Coding Style & Naming Conventions

Use Python 3 standard-library code unless a dependency is already established.
Keep files ASCII unless existing content requires otherwise. Prefer clear
functions, deterministic JSON output for runtime tools, and concise Markdown
frontmatter for docs. Active spec package names use
`docs/specs/[###-slug]/`; task IDs use stable forms such as `T001` and
`T001.1`.

## Testing Guidelines

Tests use `unittest`. Name test files `test_*.py` and place runtime tests under
`tests/runtime/` or focused helpers under `tests/traceability/`. Add fixtures
under `tests/fixtures/` when validating spec-package edge cases. Run the full
suite plus relevant `spec_runtime.py` checks before marking lifecycle work
complete.

## Commit & Pull Request Guidelines

Recent commit messages are short, imperative summaries such as
`Implement spec archive index runtime` or `Close operating model governance adoption spec`.
Keep commits scoped: implementation, closure, and evidence updates may be
separate when lifecycle state changes. PRs should describe changed docs or
runtime behavior, list validation commands, and call out residual risks or
follow-up backlog items.

## Agent-Specific Instructions

Review this file and any deeper `AGENTS.md` before changing files. For lifecycle
work, use the `spec-lifecycle-manager` skill and do not implement from
`tasks.md` alone; review relevant requirements, design, traceability,
verification, and governance first. Use MCP `scan_specs` or
`active_spec_preflight` before lifecycle work when the MCP server is available;
only run `spec_runtime.py scan .` directly when MCP is unavailable or being
debugged. If there are no active specs, use durable docs, backlog, roadmap, the
closure log, and the archive index instead of deleted packages.
If a session lacks repository instructions, ask the user to run `/init` once
rather than repeating the reminder.
