---
title: Developer CLI workflow tools traceability
doc_type: spec
artifact_type: traceability
status: active
owner: platform
last_reviewed: 2026-06-14
---

# Traceability

## Requirement To Delivery Matrix

| Requirement | Acceptance focus | Design sections | Tasks | Verification target |
|-------------|------------------|-----------------|-------|---------------------|
| R1 Project-Specific CLI Identity | command name, metadata, no template help | Package Identity, Command Groups | T001, T003 | CLI help and metadata tests |
| R2 Shared Command Runner | command plan, dry-run, failures | Shared Runner, Error Handling | T002 | Runner tests |
| R3 Local Validation Wrapper | full validation command plan | `adl check` | T004 | Command plan tests and validation evidence |
| R4 Bundle Sync Wrapper | source-to-bundle sync and guard | `adl sync` | T005 | Sync command tests and package-contract |
| R5 Package And Install Wrappers | package check, pack dry-run, install pass-through | `adl package` | T006 | Package command tests and install dry-run |
| R6 Plugin Status And Doctor | Codex availability, local toolchain | `adl plugin status`, `adl doctor` | T007 | Mocked optional-tool tests |
| R7 Spec Lifecycle Wrappers | scan, archive, prompts, summary, lint wrappers | `adl spec` | T008 | Spec wrapper tests |
| R8 Release Preflight | no external mutation, dirty tree, package checks | `adl release preflight` | T009 | Release preflight tests |
| R9 Documentation And Mutation Boundaries | docs and runbook updates | Operational Considerations | T001, T012 | Documentation review |
| R10 Tests And CI Safety | safe tests and validation integration | Test Strategy | T010, T011 | CLI tests and full validation |

## Task To Context Matrix

| Task | Requirements | Primary files | Evidence expected |
|------|--------------|---------------|-------------------|
| T001 | R1, R9 | `tools/devcli/pyproject.toml`, `tools/README.md`, `tools/devcli/README.md` | Metadata diff and help/install docs |
| T002 | R2, CP-001, CP-002, CP-003, CP-004 | `runner.py`, `repo.py`, tests | Runner and repo utility tests |
| T003 | R1 | `cli.py`, `commands/`, tests | Help output shows `adl` groups |
| T004 | R3 | `commands/check.py`, tests | Command plan/failure tests |
| T005 | R4 | `commands/sync.py`, tests | Dry-run/copy plan and sync guard tests |
| T006 | R5 | `commands/package.py`, tests | Package plan and installer pass-through tests |
| T007 | R6 | `commands/plugin.py`, `commands/doctor.py`, tests | Missing-tool and status tests |
| T008 | R7, CP-005 | `commands/spec.py`, tests | Spec wrapper command tests |
| T009 | R8 | `commands/release.py`, tests | No-publish preflight tests |
| T010 | R10 | `pyproject.toml`, `package.json`, tests | Safe CLI test command |
| T011 | R10 | `verification.md` | Validation evidence |
| T012 | R9 | READMEs and durable reference docs | Promotion map and docs review |

## Design To Implementation Matrix

| Design section | Implementation tasks | Validation signal |
|----------------|----------------------|-------------------|
| Package Identity | T001 | Metadata and CLI help tests |
| Shared Runner | T002 | Runner tests |
| Repository Root Discovery | T002 | Root override and path handling tests |
| Command Groups | T003 | CLI help tests |
| `adl check` | T004 | Command plan tests |
| `adl sync` | T005 | Sync command tests |
| `adl package` | T006 | Package command tests |
| `adl plugin status` and `doctor` | T007 | Mocked optional-tool tests |
| `adl spec` | T008 | Spec wrapper tests |
| `adl release preflight` | T009 | Release preflight tests |
| Validation Strategy | T010, T011 | CLI and repository validation |
| Operational Considerations | T012 | Durable docs updated |

## Open Decision Impact

| Decision | Affected requirements | Affected tasks | Blocking? |
|----------|-----------------------|----------------|-----------|
| Primary CLI name: confirm `adl` or choose another name | R1, R9 | T001, T003, T012 | Resolved 2026-06-17: `adl`, no `proj` alias retained (see design.md Package Identity). |
| Real tarball behavior for `adl package pack` | R5, R8 | T006, T009 | Blocks non-dry-run package command behavior |
| Full skill-tree sync versus allowlist for `adl sync bundles` | R4, R10 | T005 | Blocks sync implementation details |
| Test framework: pytest/Typer runner versus unittest-only | R10 | T002, T010 | Blocks test harness setup |
| How `adl release preflight` coordinates with active spec `022` | R8, R9 | T009, T012 | Blocks release-preflight scope |
