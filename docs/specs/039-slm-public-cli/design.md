---
title: Public slm CLI design
doc_type: spec
artifact_type: design
status: draft
owner: platform
last_reviewed: 2026-07-19
---

# Technical Design

## Overview

The package will expose one public executable, `slm`. A dependency-free Node
dispatcher will retain `install` and launch a packaged Python public-CLI
entrypoint for read-only inspection commands. The Python entrypoint will build
normalized view records by calling the shared lifecycle core, then render those
records either as plain text or stable JSON.

The existing `.venv/bin/slc` Typer application remains repository-maintenance
tooling and is neither renamed nor included in the package. The existing
JSON-oriented `spec_runtime.py` interface remains the CI, hook, debugging, and
explicit recovery surface. MCP remains the preferred agent interface.

## Requirement Coverage

| Requirement | Acceptance Criteria | Design Coverage | Validation Approach |
|-------------|---------------------|-----------------|---------------------|
| Requirement 1 | AC1-AC4 | Sole `slm` package bin, dispatcher, retained `install`, explicit `slc` boundary | Bin contract tests, help snapshots, package tarball smoke |
| Requirement 2 | AC1-AC5 | Active-spec view composer over `scan_specs`, `task_list`, and `next_task` | Core/view unit tests and CLI fixtures |
| Requirement 3 | AC1-AC4 | Shared spec resolver plus one-active default and ambiguity guard | Resolution and exit-code tests |
| Requirement 4 | AC1-AC7 | Normalized task view, named state sets, `next_task` delegation | Filter partition and equivalence tests |
| Requirement 5 | AC1-AC5 | New shared requirement-list projection over the canonical requirements parser and traceability | Parser/projection tests with priority fixtures |
| Requirement 6 | AC1-AC5 | History view over archive-index and closure-log validation | Removed/archived/malformed fixtures |
| Requirement 7 | AC1-AC5 | Shared normalized records with table and JSON renderers | Golden/structural output tests |
| Requirement 8 | AC1-AC4 | Root discovery, `-C`/`--repo`, concise error mapping | Nested-cwd and failure tests |
| Requirement 9 | AC1-AC4 | Read-only composition, interpreter resolver, tarball packaging | Worktree fingerprint and packaged smoke tests |

## Correctness Property Coverage

| Property | Design Behavior | Validation Direction | Notes |
|----------|-----------------|----------------------|-------|
| CP-001 | One marker-to-state map and explicit filter state sets | Table-driven unit tests across every current and legacy marker | Legacy markers remain readable but are not emitted by new specs. |
| CP-002 | Both next surfaces call the same view builder backed by `next_task` | Compare command JSON and core payload across runnable/blocked fixtures | No independent first-pending algorithm is permitted. |
| CP-003 | Renderers receive the same immutable normalized records | Compare parsed JSON records with table-source records in tests | Formatting may truncate display text, not record identity. |
| CP-004 | Query path contains no writer calls and worktree fingerprints remain stable | Before/after file and Git-status tests | `install` is intentionally outside the read-only query set. |
| CP-005 | Selection helper returns an ambiguity error before any spec-specific query | Multiple-active fixtures | Candidate ordering is deterministic. |
| CP-006 | History builder consumes validated closure records only | Removed-package fixture with absent spec directory | Invalid archive diagnostics produce failure. |
| CP-007 | Requirement view consumes the shared priority parser | Canonical, shorthand, invalid, and missing-priority fixtures | `unspecified` is presentation only. |

## High-Level Design

### System Architecture

```text
shell / npm / npx
        |
        v
packaging/spec-lifecycle-manager/slm-cli.js
        |-- install ----------> existing installer.mjs
        |
        `-- read commands ----> resolve-python.mjs
                                  |
                                  v
packaged slm_cli.py -> lifecycle/public_cli.py
                                  |
                                  v
        shared lifecycle core and requirements/closure modules
                                  |
                     normalized view records
                         /                 \
                  plain tables          JSON document
```

MCP calls the same lifecycle core independently and remains the preferred
agent-facing surface. `slm` is a human and automation presentation layer, not
an MCP proxy.

### Components and Changes

- `package.json` and package manifests:
  Replace the two long bin aliases with a sole `slm` bin and include all new
  dispatcher/runtime files in the package contract.
- `packaging/spec-lifecycle-manager/slm-cli.js`:
  Parse the top-level command, route `install` in-process to `installer.mjs`,
  resolve Python for inspection commands, and forward process exit/status and
  standard streams without a shell.
- `packaging/spec-lifecycle-manager/resolve-python.mjs`:
  Remain the sole cross-platform interpreter-resolution contract.
- `skills/spec-lifecycle-manager/scripts/slm_cli.py`:
  Thin packaged Python entrypoint importing the public CLI module.
- `skills/spec-lifecycle-manager/scripts/lifecycle/public_cli.py`:
  Own argument parsing, repository selection, view composition, normalized
  command envelopes, table rendering, JSON rendering, and error-to-exit mapping.
- `skills/spec-lifecycle-manager/scripts/lifecycle/core.py` and
  `requirements.py`:
  Provide or expose shared projections needed for requirement inventory and
  reuse existing scan, task, next-task, resolution, and history semantics.
- Bundled Codex and Claude skill copies:
  Receive byte-equivalent public CLI/core changes through the normal bundle
  synchronization workflow.
- `tools/devcli/`:
  Remains unchanged except for documentation or tests that explicitly assert
  the `slc`/`slm` separation.

### Data Models

Every JSON response uses a common envelope:

```json
{
  "schema_version": "1",
  "command": "specs",
  "repo_root": ".",
  "records": [],
  "summary": {}
}
```

Minimum record shapes:

```text
SpecRecord:
  spec_id, path, status, lifecycle, health,
  tasks_total, tasks_complete, next_task

TaskRecord:
  task_id, marker, state, summary,
  dependencies[], requirements[], is_subtask

RequirementRecord:
  requirement_id, title, priority, tasks[], diagnostics[]

HistoryRecord:
  spec_id, title, disposition,
  final_spec_commit, cleanup_commit, package_path
```

Paths in records are repo-relative. `priority="unspecified"` is a view value
and is never written back to a requirement artifact.

### Data Flow

1. The Node dispatcher identifies `install`, help, or a read-only query command.
2. Query commands resolve Python without invoking a shell and launch the
   packaged Python entrypoint with unchanged arguments.
3. The Python CLI discovers or validates the repository root.
4. Spec-taking commands resolve the explicit reference or apply the exactly-one
   active-spec rule.
5. A command-specific builder calls shared lifecycle functions and produces
   normalized records.
6. Filters operate only on normalized record fields.
7. The selected renderer emits either plain text or one JSON document.
8. Errors are mapped to stderr and a non-zero process exit without partial JSON
   on stdout.

## Low-Level Design

### Algorithms and Logic

```text
function select_spec(repo, optional_reference):
    if reference exists:
        result = shared_resolve_spec(reference)
        require active unambiguous package
        return result

    active = shared_scan_specs(repo).active_specs
    if active.count == 1:
        return active[0]
    if active.count == 0:
        fail "no active specs"
    fail with sorted active candidate IDs
```

```text
function task_filter(records, flags):
    require --next is exclusive with all state filters
    selected_states = union(--state values)
    if --complete: add complete
    if --pending: add pending
    if --open: add pending, in_progress, partial, review_needed, attention
    if no selected states: return all records
    return records whose normalized state is selected
```

```text
function history_records(repo):
    validation = shared_archive_index(repo)
    if validation has error diagnostics:
        fail with concise diagnostics
    return normalized records in durable archive order
```

### Function Signatures and Interfaces

Provisional internal interfaces:

```python
def requirement_list(spec_path: Path) -> dict[str, object]: ...
def build_specs_view(repo_root: Path, *, include_history: bool) -> CommandView: ...
def build_tasks_view(spec_path: Path, filters: TaskFilters) -> CommandView: ...
def build_requirements_view(spec_path: Path, filters: RequirementFilters) -> CommandView: ...
def build_history_view(repo_root: Path, filters: HistoryFilters) -> CommandView: ...
def render_table(view: CommandView, stream: TextIO) -> None: ...
def render_json(view: CommandView, stream: TextIO) -> None: ...
```

Public commands:

```text
slm [specs] [--all] [--json] [-C PATH|--repo PATH]
slm tasks [SPEC] [--complete] [--pending] [--open] [--state STATE...] [--next] [--json]
slm next [SPEC] [--json]
slm requirements [SPEC] [--priority PRIORITY|--missing-priority] [--json]
slm history [--archived] [--removed] [--limit N] [--json]
slm install [existing installer options]
```

Compatible task-state filters form a union, as do `--archived` and `--removed`;
duplicate selectors do not duplicate records. `--next` remains exclusive with
every task-state filter, and `--missing-priority` remains exclusive with
`--priority`.

### Error Handling

- Exit `0`: successful command, including valid empty results.
- Exit `2`: usage errors, invalid filters, ambiguous selection, missing active
  selection, or invalid spec reference.
- Exit `1`: interpreter failure, repository/runtime failure, malformed durable
  history, or unexpected internal error.
- Human mode writes concise errors to stderr.
- JSON mode emits no partial success document after a fatal error. A future
  structured-error envelope is outside this slice.
- The Node dispatcher forwards signals and child exit codes and does not print
  duplicate stack traces for expected CLI errors.

### Security, Trust, and Access

- Spec contents and paths are untrusted repository input; rendering must not
  execute text extracted from Markdown.
- The dispatcher uses argument vectors and `spawnSync`/equivalent process APIs,
  never shell interpolation.
- Query commands do not require network, credentials, package registry access,
  or write permissions.
- Output excludes absolute plugin cache paths and avoids terminal control
  sequences derived from repository content.
- `install` retains its existing explicit mutation boundary and is not
  described as read-only.

### Migration and Compatibility

- This is an intentional executable rename. The package exposes only `slm`;
  no long-bin compatibility alias or deprecation window is required.
- `slm install` replaces `spec-lifecycle-manager install` in durable docs.
- `npx @auriora/ai-spec-lifecycle install` remains viable because npm can
  select the package's sole bin.
- `slc` remains available only through the repo-local development environment.
- The change is release-note-worthy and should be called out as a command-line
  breaking change even if package versioning remains pre-1.0.
- MCP names, prompt names, hooks, spec formats, and task markers are unchanged.

### Slice Boundary And Residual Architecture

| Design target | In this slice | Out of this slice | Follow-up destination | Blocks closure? |
|---------------|---------------|-------------------|-----------------------|-----------------|
| Public read-only CLI | `slm` dispatcher, views, filters, JSON, packaging, docs, tests | Write-capable lifecycle commands | Future focused spec if requested | no |
| Shared lifecycle interpretation | Reuse existing core and add requirement inventory projection | Replace MCP or make CLI an MCP client | none | no |
| Executable migration | Sole `slm` bin and updated install docs | Compatibility aliases | explicitly rejected by user | no |
| Terminal presentation | Plain dependency-free tables | Interactive TUI, paging, themes, colour system | backlog only if demanded | no |

## Validation Strategy

| Validation | Covers | Evidence Location | Residual Risk |
|------------|--------|-------------------|---------------|
| Python unit tests for views, selection, filters, and renderers | Requirements 2-8, CP-001-CP-007 | `verification.md`, `tests/runtime/` | Table width differences across terminals need bounded fixtures. |
| Node tests for dispatcher/interpreter/bin behavior | Requirements 1, 8, 9 | `verification.md`, `tests/runtime/*.test.mjs` | Platform-specific process behavior requires CI. |
| Package contract and tarball smoke | Requirements 1 and 9 | `verification.md`, npm pack metadata | Must avoid validating from a checkout-only path. |
| Existing full validation | Regression across runtime, MCP, hooks, bundles, docs, and packaging | `verification.md` | None beyond documented skipped CI platforms. |
| Read-only worktree fingerprint | Requirement 9 and CP-004 | focused integration test | Installer command is excluded by design. |

## Downstream Task Guidance

- Freeze normalized record and filter semantics in tests before implementing
  rendering.
- Keep the Python public CLI standard-library only.
- Keep Node limited to package dispatch, Python resolution, and process
  forwarding; lifecycle meaning belongs in Python shared modules.
- Verify from the built tarball in isolated package/cache roots.
- If implementation changes any record field or filter meaning, update
  requirements, traceability, quickstart, and durable docs before proceeding.
- Package/release review is required because the sole-bin change is externally
  visible.

## Operational Considerations

- Queries should work offline and should not initialize Codex or Claude plugin
  state.
- Installed packages need no additional Python dependency beyond a supported
  interpreter.
- CI should exercise POSIX and Windows process launching; local validation
  should include Linux tarball smoke.
- Release verification must inspect the packed bin map and run `slm --help`,
  `slm specs --json`, and `slm install --help` from the artifact.
- Existing Codex/Claude plugin installation remains independent of whether the
  global `slm` command is on a current session's PATH.

## Open Questions

None. The user approved the executable name, command vocabulary, filter
semantics, dual next-task surfaces, read-only boundary, and removal of unused
compatibility aliases on 2026-07-19.

## Related Artifacts

- Requirements: `requirements.md`
- Change Impact: `change-impact.md`
- Tasks: `tasks.md`
- Traceability: `traceability.md`
- Verification: `verification.md`
- Quickstart: `quickstart.md`
