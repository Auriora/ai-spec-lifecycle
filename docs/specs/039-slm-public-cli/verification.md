---
title: Public slm CLI verification
doc_type: spec
artifact_type: verification
status: draft
owner: platform
last_reviewed: 2026-07-19
---

# Verification

## Scope

Verify the full Spec 039 slice: shared lifecycle projections, the read-only
Python CLI, sole `slm` package bin, retained `slm install`, source/bundle parity,
cross-platform process behavior, built-tarball operation, durable documentation,
and removal of unused executable aliases.

## Quality Gates

| Gate | Required? | Status | Evidence |
|------|-----------|--------|----------|
| Requirements acceptance criteria reviewed | yes | passed | 2026-07-19 lifecycle review packet and traceability lookup; compatible-filter ambiguity resolved before commit. |
| Shared public-view checkpoint passes | yes | passed | 2026-07-19: 22 focused public-view and shared-core regression tests passed; `git diff --check` and module compilation passed. |
| Task evidence complete | yes | pending | |
| Public CLI focused tests pass | yes | passed | 2026-07-19: 14 CLI tests and 17 shared-view tests passed; live checkout table/JSON smokes passed for all five query commands. |
| Node dispatcher and Python resolver tests pass | yes | passed | 2026-07-19: 31 Node tests passed, including shell-free query dispatch, install routing, resolver behavior, child exits, and signals. |
| Read-only worktree preservation passes | yes | passed | Source fixture fingerprint passed and isolated installed-tarball `slm specs --json` completed without repository mutation. |
| Source/Codex/Claude bundle parity passes | yes | passed | Source-to-Codex and source-to-Claude trees each contain 65 equivalent files. User-wide installed cache remains intentionally unchanged during checkout testing. |
| Package contract and tarball smoke pass | yes | passed | Package contract has zero findings; 158-file dry-run contains all dispatcher/runtime files; isolated npm install passed `slm --help`, `slm specs --json`, and `slm install --help`. |
| Windows, macOS, and Linux CI paths pass | yes | pending | |
| Durable documentation promoted | yes | pending | |
| Breaking executable rename reviewed and documented | yes | pending | |
| Full repository validation passes | yes | pending | |
| Spec cleanup decision recorded | yes | pending | |

## Validation Commands

| Command | Purpose | Result | Evidence |
|---------|---------|--------|----------|
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_public_views` | Shared view records, selection, filters, history, priority diagnostics, and read-only semantics | passed | 2026-07-19: 17 tests passed. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_public_cli tests.runtime.test_public_views` | Public parsing, table/JSON parity, roots, errors, sanitization, read-only behavior, and shared record semantics | passed | 2026-07-19: 31 tests passed. |
| Focused shared-core regression selection recorded in T003 evidence | Resolver, archive, priority, next-task, and grouped-task compatibility | passed | 2026-07-19: combined run passed 22 tests. |
| `node --test tests/runtime/*.test.mjs` | Dispatcher, interpreter resolution, installer routing, build identity, and MCP launch behavior | passed | 2026-07-19: 31 tests passed. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'` | Full Python regression suite | pending | |
| `npm run validate` | Full combined lifecycle, Node, package, sync, and whitespace validation | pending | |
| `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py package-contract .` | Package files and bin contract | passed | Sole `slm` bin and source/Codex/Claude parity passed with zero findings. |
| `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py sync-guard . --commits 0` | Source/bundle parity plus installed-cache advisory | passed for repository bundle scope | Both bundle trees are in sync; the unchanged user-wide 0.4.0 cache is correctly reported as drift and is not a checkout-test deployment target. |
| `npm_config_cache=/tmp/spec-lifecycle-npm-cache npm pack --dry-run --json` | Packed file inventory and bin metadata | passed | 158 files; every dispatcher and Codex/Claude runtime file present. |
| `node tests/runtime/slm_package_smoke.mjs` | Verify `slm --help`, `slm specs --json`, and `slm install --help` from an isolated installed tarball | passed | npm-created `slm` shim present; legacy bin shims absent; all three commands passed. |
| `git diff --check` | Whitespace and patch integrity | passed through Phase 3 | 2026-07-19 checkpoints. |

## Requirement Coverage

| Requirement | Acceptance criteria covered | Evidence | Residual risk |
|-------------|-----------------------------|----------|---------------|
| Requirement 1 | AC1-AC4 | Phase 3 package contract passed; docs pending | Public executable breaking change requires T008 release communication. |
| Requirement 2 | AC1-AC5 | Source and packaged local paths passed; docs pending | View reuses scan health and avoids repeated full lint through `spec_summary`. |
| Requirement 3 | AC1-AC4 | Source and packaged local paths passed; docs pending | Ambiguity messages list sorted candidates. |
| Requirement 4 | AC1-AC7 | Source and packaged local paths passed; docs pending | Open-state membership must remain aligned with future markers. |
| Requirement 5 | AC1-AC5 | Source and packaged local paths passed; docs pending | Traceability may be absent in compatibility specs. |
| Requirement 6 | AC1-AC5 | Source and packaged local paths passed; docs pending | Limit semantics follow newest-first durable archive order. |
| Requirement 7 | AC1-AC5 | Source and packaged local paths passed | Human table width varies across terminals. |
| Requirement 8 | AC1-AC4 | Local packaged paths passed; matrix CI pending | Windows, macOS, and Linux workflow paths include the public packaged smoke. |
| Requirement 9 | AC1-AC4 | Source/bundle/tarball paths passed | User-wide installation remains release-owned, not checkout-owned. |

## Correctness Property Coverage

| Property | Covered by | Evidence | Residual risk |
|----------|------------|----------|---------------|
| CP-001 | T001-T005 marker/filter tests | passed | none after exhaustive marker coverage |
| CP-002 | T001-T005 next equivalence tests | passed | none after blocked/runnable fixtures |
| CP-003 | T001, T004, T005 renderer parity tests | passed | source and installed-tarball JSON paths passed |
| CP-004 | T001, T004, T005, T007 worktree fingerprint tests | passed | install intentionally mutates only when explicitly selected |
| CP-005 | T001-T005 ambiguity tests | passed | none |
| CP-006 | T001-T005 removed/malformed history tests | passed | none |
| CP-007 | T001-T005 priority parser/projection tests | passed | compatibility inputs remain allowed |

## Scope Reconciliation Before Closure

| Broad requirement, design target, or review finding | Implemented in this spec | Coverage state | Deferred or rejected work | Destination | Blocks closure? | Evidence |
|-----------------------------------------------------|--------------------------|----------------|---------------------------|-------------|-----------------|----------|
| Sole public `slm` executable and retained installer | implemented and packaged | partial | Durable migration and release communication remain. | T008 | yes | sole-bin contract and installed-tarball smoke |
| Active, task, requirement, and history views | source and bundles implemented | partial | Durable runtime documentation remains. | T008 | yes | T004-T007 evidence |
| Stable table/JSON output and selection semantics | source and packaged local paths implemented | partial | Durable interface documentation remains. | T008 | yes | focused tests and installed-tarball smoke |
| Read-only packaged cross-platform operation | local package proof and matrix workflow implemented | partial | Matrix CI run and final full validation remain. | T009 | yes | source fingerprint, dispatcher tests, tarball smoke, workflow test |
| Compatibility aliases | intentionally excluded | out-of-scope | Explicitly rejected; prior long executables are unused. | none | no | user decision, 2026-07-19 |
| Write-capable lifecycle commands | intentionally excluded | out-of-scope | Future work requires a focused spec and explicit approval. | future backlog/spec if requested | no | Requirements non-goals |
| Interactive TUI, colour, paging, and themes | intentionally excluded | out-of-scope | No demonstrated need in this slice. | backlog only if requested | no | Requirements non-goals |

## Agent Readiness Evidence

| Field | Evidence | Residual risk |
|-------|----------|---------------|
| Scope and out-of-scope files | `requirements.md`, `design.md`, `change-impact.md`; reconciled implementation files in T002/T004/T006/T007 | Durable promotion files remain T008. |
| Must-read and optional context | `canonical-context.md`, all spec artifacts, package/runtime source | Source may evolve before implementation. |
| Permissions and approval points | Read-only CLI; package bin removal approved; release/publish remains separately authorized | Publishing is not authorized merely by implementing this spec. |
| Validation commands and expected signals | This file and task checkpoints | Focused command names finalized in T001. |
| Review needs | Package/release and public-interface review at T009 | Cross-platform CI evidence required. |
| Durable-doc or closure impact | `change-impact.md` promotion targets | Spec cannot close with behavior documented only here. |
| Optional repo-evidence provider caveats | MCP/runtime evidence supports context but is not implementation proof | Direct tests and tarball smoke remain required. |

## Task Evidence

| Task ID | Status | Evidence | Notes |
|---------|--------|----------|-------|
| T001 | pending | | Contract tests not started. |
| T002 | pending | | Shared projections not started. |
| T003 | pending | | Shared-record checkpoint not run. |
| T004 | pending | | Public Python CLI not started. |
| T005 | pending | | Public-command checkpoint not run. |
| T006 | pending | | Package dispatcher/bin work not started. |
| T007 | pending | | Bundle and tarball validation not started. |
| T008 | pending | | Durable promotion not started. |
| T009 | pending | | Full validation and review not started. |

## Evidence Log

| Date | Evidence | Result | Notes |
|------|----------|--------|-------|
| 2026-07-19 | MCP `spec_creation_plan` for `slm-public-cli` | passed | Allocated provisional Spec 039 with high confidence and revalidated fingerprint immediately before authoring. |
| 2026-07-19 | User decision record | passed | Approved `slm`, plural commands, literal pending plus open, both next surfaces, read-only scope, and no compatibility alias. |
| 2026-07-19 | MCP design/requirements/trace review plus targeted Requirement 4 and Requirement 6 traceability lookups | passed after revision | Resolved compatible task/history filter combination semantics as deterministic unions; lint then reported zero findings and acceptance/context gaps were zero. |

## Manual Or External Verification

- Verify help/table readability in a real terminal after automated output tests
  pass.
- Confirm the packaged executable on Windows, macOS, and Linux through CI or
  recorded platform runs.
- Publishing and user-wide installation are release activities outside the
  authorization granted by spec creation.

## Residual Risks

- Removing the existing executable names is intentionally breaking even if
  usage is believed absent; release notes must make the rename visible.
- Table rendering can become noisy for long titles or paths; record identity
  and JSON must remain complete even if human summaries are bounded.
- Repositories with many active specs could make per-spec task aggregation
  expensive; implementation should measure and avoid repeated scans/lints.
- Future task markers must update the shared state map and open-state tests.

## Durable Promotion And Cleanup

| Spec content | Durable destination or deferral | Status | Evidence |
|--------------|---------------------------------|--------|----------|
| Public command and examples | `README.md` | pending | |
| CLI architecture and shared-core boundary | `docs/design/spec-lifecycle-management.md` | pending | |
| Commands, filters, output, states, and exit behavior | `docs/reference/spec-lifecycle-runtime.md` | pending | |
| Bin migration, interpreter, and package verification | `docs/reference/spec-lifecycle-manager-mcp-install.md` | pending | |
| Breaking rename and delivered features | next release notes | pending | |
| Follow-up work | backlog only if implementation/review identifies residuals | pending | |

### Spec Cleanup Decision

- **Cleanup action:** remove after promotion and closure evidence
- **Reason:** Active implementation scaffolding should not remain a parallel
  source of truth after the public CLI is documented durably.
- **Final spec commit:** pending
- **Closure log path:** `docs/history/spec-closure-log.md`
- **Closure log entry updated:** no
- **Closure cleanup commit:** pending
- **Active indexes updated:** no
- **Durable docs linked back to evidence where useful:** no
- **Residual spec-only content:** none expected

## Ship Or Closure Risk

- **Risk level:** medium
- **Breaking change:** yes
- **Blast radius checked:** no
- **Rollback path:** restore prior bin map and package dispatcher in a follow-up release
- **Requires human review:** yes - package/public-interface review
- **Release notes needed:** yes
- **Follow-up issue or spec needed:** no unless review identifies residual work

### Risk Rationale

The inspection behavior is read-only, but the package executable rename and
cross-platform process boundary are externally visible. Shared-core reuse and
artifact-based tests limit semantic drift; tarball and platform validation are
required before release.

## Readiness Decision

- **Ready for implementation:** yes, after package lint and T001 selection
- **Ready for promotion:** no
- **Ready for release:** no
- **Ready for closure:** no

## Related Artifacts

- Requirements: `requirements.md`
- Change Impact: `change-impact.md`
- Design: `design.md`
- Tasks: `tasks.md`
- Traceability: `traceability.md`
- Quickstart: `quickstart.md`
