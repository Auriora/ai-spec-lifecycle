---
title: Developer CLI workflow tools traceability
doc_type: spec
artifact_type: traceability
status: active
owner: platform
last_reviewed: 2026-07-04
---

# Traceability

## Requirement To Delivery Matrix

| Requirement | Acceptance focus | Design sections | Tasks | Verification target |
|-------------|------------------|-----------------|-------|---------------------|
| Requirement 1: Project-Specific CLI Identity | command name, metadata, no template help | Package Identity, Command Groups | T001, T003 | CLI help and metadata tests |
| Requirement 2: Shared Command Runner | command plan, dry-run, failures | Shared Runner, Error Handling | T002 | Runner tests |
| Requirement 3: Local Validation Wrapper | full validation command plan | `slc check` | T004 | Command plan tests and validation evidence |
| Requirement 4: Bundle Sync Wrapper | source-to-bundle sync and guard | `slc sync` | T005 | Sync command tests and package-contract |
| Requirement 5: Package And Install Wrappers | package check, pack dry-run, install pass-through | `slc package` | T006 | Package command tests and install dry-run |
| Requirement 6: Plugin Status And Doctor | Codex availability, local toolchain | `slc plugin status`, `slc doctor` | T007 | Mocked optional-tool tests |
| Requirement 7: Spec Lifecycle Wrappers | scan, archive, prompts, summary, lint wrappers | `slc spec` | T008 | Spec wrapper tests |
| Requirement 8: Release Preflight | no external mutation, dirty tree, package checks | `slc release preflight` | T009 | Release preflight tests |
| Requirement 9: Documentation And Mutation Boundaries | docs and runbook updates | Operational Considerations | T001, T012 | Documentation review |
| Requirement 10: Tests And CI Safety | safe tests and validation integration | Test Strategy | T010, T011 | CLI tests and full validation |

## Task To Context Matrix

| Task | Requirements | Primary files | Durable Targets | Evidence expected |
|------|--------------|---------------|-----------------|-------------------|
| T001 | Requirement 1, Requirement 9 | `tools/devcli/pyproject.toml`, `tools/README.md`, `tools/devcli/README.md` | `tools/README.md`, `tools/devcli/README.md` | Metadata diff and help/install docs |
| T002 | Requirement 2, CP-001, CP-002, CP-003, CP-004 | `runner.py`, `repo.py`, `tests/runtime/test_devcli_runner.py` | `tools/devcli/README.md` | Runner and repo utility tests |
| T003 | Requirement 1 | `cli.py`, `commands/`, `tests/runtime/test_devcli_cli.py` | `tools/devcli/README.md` | Help output shows `slc` groups |
| T004 | Requirement 3 | `commands/check.py`, `tests/runtime/test_devcli_check.py` | `tools/devcli/README.md`, `docs/reference/spec-lifecycle-runtime.md` | Command plan/failure tests |
| T005 | Requirement 4 | `commands/sync.py`, `tests/runtime/test_devcli_sync.py` | `tools/devcli/README.md`, `docs/reference/spec-lifecycle-runtime.md` | Dry-run/copy plan and sync guard tests |
| T006 | Requirement 5 | `commands/package.py`, `tests/runtime/test_devcli_package.py` | `tools/devcli/README.md`, `docs/reference/spec-lifecycle-manager-mcp-install.md` | Package plan and installer pass-through tests |
| T007 | Requirement 6 | `commands/plugin.py`, `commands/doctor.py`, `tests/runtime/test_devcli_plugin.py` | `tools/devcli/README.md`, `docs/reference/spec-lifecycle-manager-mcp-install.md` | Missing-tool and status tests |
| T008 | Requirement 7, CP-005 | `commands/spec.py`, `tests/runtime/test_devcli_spec.py` | `tools/devcli/README.md`, `docs/reference/spec-lifecycle-runtime.md` | Spec wrapper command tests |
| T009 | Requirement 8 | `commands/release.py`, `tests/runtime/test_devcli_release.py` | `tools/devcli/README.md`, `docs/reference/spec-lifecycle-manager-mcp-install.md` | No-publish preflight tests |
| T010 | Requirement 10 | `pyproject.toml`, `package.json`, `tests/runtime/test_devcli_*.py` | `package.json`, `tools/devcli/README.md` | Safe CLI test command |
| T011 | Requirement 10 | `verification.md` | `docs/specs/025-dev-cli-workflow-tools/verification.md` | Validation evidence |
| T012 | Requirement 9 | READMEs and durable reference docs | `tools/README.md`, `tools/devcli/README.md`, `docs/reference/spec-lifecycle-manager-mcp-install.md`, `docs/reference/spec-lifecycle-runtime.md` | Promotion map and docs review |

## Design To Implementation Matrix

| Design section | Implementation tasks | Validation signal |
|----------------|----------------------|-------------------|
| Package Identity | T001 | Metadata and CLI help tests |
| Shared Runner | T002 | Runner tests |
| Repository Root Discovery | T002 | Root override and path handling tests |
| Command Groups | T003 | CLI help tests |
| `slc check` | T004 | Command plan tests |
| `slc sync` | T005 | Sync command tests |
| `slc package` | T006 | Package command tests |
| `slc plugin status` and `doctor` | T007 | Mocked optional-tool tests |
| `slc spec` | T008 | Spec wrapper tests |
| `slc release preflight` | T009 | Release preflight tests |
| Validation Strategy | T010, T011 | CLI and repository validation |
| Operational Considerations | T012 | Durable docs updated |

## Open Decision Impact

| Decision | Affected requirements | Affected tasks | Blocking? |
|----------|-----------------------|----------------|-----------|
| Primary CLI name: confirm `slc` or choose another name | Requirement 1, Requirement 9 | T001, T003, T012 | Resolved 2026-07-04: `slc`, no `proj` alias retained (see design.md Package Identity). |
| Real tarball behavior for `slc package pack` | Requirement 5, Requirement 8 | T006, T009 | Blocks non-dry-run package command behavior |
| Full skill-tree sync versus allowlist for `slc sync bundles` | Requirement 4, Requirement 10 | T005 | Blocks sync implementation details |
| Test framework: pytest/Typer runner versus unittest-only | Requirement 10 | T010 | Unblocked for T002 by using standard-library `unittest`; final CLI command integration remains T010 scope. |
| How `slc release preflight` coordinates with active spec `022` | Requirement 8, Requirement 9 | T009, T012 | Blocks release-preflight scope |
