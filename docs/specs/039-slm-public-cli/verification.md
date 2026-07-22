---
title: Public slm CLI verification
doc_type: spec
artifact_type: verification
status: draft
owner: platform
last_reviewed: 2026-07-22
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
| Task evidence complete | yes | passed | T001-T011 contain concrete implementation or validation evidence. |
| Public CLI focused tests pass | yes | passed | 2026-07-19: 14 CLI tests and 17 shared-view tests passed; live checkout table/JSON smokes passed for all five query commands. |
| Node dispatcher and Python resolver tests pass | yes | passed | 2026-07-19: 32 Node tests passed, including shell-free query dispatch, install routing, resolver behavior, child exits, signals, and the repository launcher. |
| Read-only worktree preservation passes | yes | passed | Source fixture fingerprint passed and isolated installed-tarball `slm specs --json` completed without repository mutation. |
| Source/Codex/Claude bundle parity passes | yes | passed | Source-to-Codex and source-to-Claude trees each contain 65 equivalent files. User-wide installed cache remains intentionally unchanged during checkout testing. |
| Package contract and tarball smoke pass | yes | passed | Package contract has zero findings; 158-file dry-run contains all dispatcher/runtime files; isolated npm install passed `slm --help`, `slm specs --json`, and `slm install --help`. |
| Windows, macOS, and Linux CI paths pass | yes | passed | GitHub Actions run 29683557635 passed all six Linux/macOS/Windows jobs on Python 3.10 and 3.12, including installed-tarball smoke. |
| Durable documentation promoted | yes | passed | README, durable design, runtime reference, and install reference now define the accepted `slm` surface and command boundaries. |
| Breaking executable rename reviewed and documented | yes | passed | README and install/runtime references direct users from both removed aliases to the sole `slm` bin; release notes remain a release-preparation obligation. |
| Full repository validation passes | yes | passed | `npm run validate` passed after replacing two stale historic `npm-install.js` destinations with `slm-cli.js`. |
| Spec cleanup decision recorded | yes | passed | Remove after final spec commit and closure metadata; closure execution remains a separate lifecycle action. |
| Singular `spec` route extension passes | yes | passed | Focused route-equivalence tests, source/Codex/Claude bundle parity, isolated package smoke, and full validation passed on 2026-07-22. |
| Task-derived phase progress passes | yes | passed | Mixed-state precedence, progress, all-complete, no-phase, table/JSON, singular/plural, bundle, package, and full validation passed on 2026-07-22. |

## Validation Commands

| Command | Purpose | Result | Evidence |
|---------|---------|--------|----------|
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_public_views` | Shared view records, selection, filters, history, priority diagnostics, and read-only semantics | passed | 2026-07-19: 17 tests passed. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_public_cli tests.runtime.test_public_views` | Public parsing, table/JSON parity, roots, errors, sanitization, read-only behavior, and shared record semantics | passed | 2026-07-19: 31 tests passed. |
| Focused shared-core regression selection recorded in T003 evidence | Resolver, archive, priority, next-task, and grouped-task compatibility | passed | 2026-07-19: combined run passed 22 tests. |
| `node --test tests/runtime/*.test.mjs` | Dispatcher, interpreter resolution, installer routing, build identity, and MCP launch behavior | passed | 2026-07-19: 31 tests passed. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'` | Full Python regression suite | passed | 353 tests passed. The first run exposed two stale archive destinations; after the history records were corrected, the focused test and full rerun passed. |
| `npm run validate` | Full combined lifecycle, Node, package, sync, and whitespace validation | passed | 353 Python and 31 Node tests passed; scan, archive index, prompts, package contract, sync guard, 158-file npm dry-run, and `git diff --check` passed. |
| `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py package-contract .` | Package files and bin contract | passed | Sole `slm` bin and source/Codex/Claude parity passed with zero findings. |
| `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py sync-guard . --commits 0` | Source/bundle parity plus installed-cache advisory | passed for repository bundle scope | Both bundle trees are in sync; the unchanged user-wide 0.4.0 cache is correctly reported as drift and is not a checkout-test deployment target. |
| `npm_config_cache=/tmp/spec-lifecycle-npm-cache npm pack --dry-run --json` | Packed file inventory and bin metadata | passed | 158 files; every dispatcher and Codex/Claude runtime file present. |
| `node tests/runtime/slm_package_smoke.mjs` | Verify `slm --help`, `slm specs --json`, and `slm install --help` from an isolated installed tarball | passed | Repassed in Phase 4: npm-created `slm` shim present; legacy bin shims absent; all three commands passed. |
| `./slm --help` and `./slm specs --json` | Verify the repo-root source-backed developer launcher | passed | Root launcher delegates to the package dispatcher without npm or user-wide installation; focused Node regression covers help discovery. |
| `git diff --check` | Whitespace and patch integrity | passed | Phase 4 full validation. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_public_cli tests.runtime.test_public_views` | Singular inventory and per-spec routes, defaults, filters, invalid forms, and shared-view regressions | passed | 2026-07-22: 34 tests passed. |
| `node --test tests/runtime/slm-cli.test.mjs` | Singular dispatcher forwarding and existing dispatcher behavior | passed | 2026-07-22: 7 tests passed. |
| `node tests/runtime/slm_package_smoke.mjs` | Installed-tarball help and singular/plural inventory equivalence | passed | 2026-07-22: isolated package smoke passed. |
| `SPEC_LIFECYCLE_PYTHON=python3 npm run validate` | Full regression, lifecycle, package, bundle, dry-run, and whitespace validation after T010 | passed | 2026-07-22: 356 Python and 33 Node tests passed with scan, archive index, prompts, package contract, sync guard, npm dry-run, and `git diff --check`. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_public_views tests.runtime.test_public_cli` | Phase grouping, completion, precedence, no-phase behavior, table/JSON projection, and existing public CLI regressions | passed | 2026-07-22: 38 tests passed. |
| `node tests/runtime/slm_package_smoke.mjs` | Installed-tarball phase fields and singular/plural inventory equivalence | passed | 2026-07-22: isolated phased-spec package smoke passed. |
| `SPEC_LIFECYCLE_PYTHON=python3 npm run validate` | Full regression, lifecycle, package, bundle, dry-run, and whitespace validation after T011 | passed | 2026-07-22: 360 Python and 33 Node tests passed with scan, archive index, prompts, package contract, source/bundle sync, npm dry-run, and `git diff --check`. |

## Requirement Coverage

| Requirement | Acceptance criteria covered | Evidence | Residual risk |
|-------------|-----------------------------|----------|---------------|
| Requirement 1 | AC1-AC4 | Package contract, installed-tarball smoke, README, install/runtime migration guidance, and `docs/release-notes/v0.5.0.md` passed | none |
| Requirement 2 | AC1-AC5 | Source and packaged local paths plus README/runtime docs passed | View reuses scan health and avoids repeated full lint through `spec_summary`. |
| Requirement 3 | AC1-AC4 | Source and packaged local paths plus runtime selection docs passed | Ambiguity messages list sorted candidates. |
| Requirement 4 | AC1-AC7 | Source and packaged local paths plus task-filter docs passed | Open-state membership must remain aligned with future markers. |
| Requirement 5 | AC1-AC5 | Source and packaged local paths plus priority-filter docs passed | Traceability may be absent in compatibility specs. |
| Requirement 6 | AC1-AC5 | Source and packaged local paths plus durable-history docs passed | Limit semantics follow newest-first durable archive order. |
| Requirement 7 | AC1-AC5 | Source and packaged local paths passed | Human table width varies across terminals. |
| Requirement 8 | AC1-AC4 | Local packaged paths and six-job Linux/macOS/Windows matrix passed | none |
| Requirement 9 | AC1-AC4 | Source, bundle, tarball, and cross-platform installed-tarball paths passed | User-wide installation remains release-owned, not checkout-owned. |
| Requirement 10 | AC1-AC8 | Focused parser and route-equivalence tests, live source comparisons, bundle parity, installed-package smoke, and full validation passed | Existing plural commands remain supported compatibility surfaces. |
| Requirement 11 | AC1-AC7 | Focused phase aggregation tests, live human/JSON output, source/Codex/Claude parity, installed-package smoke, durable docs, and full validation passed | Future normalized task states require explicit precedence review. |

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
| CP-008 | T010 singular/plural route equivalence tests | passed | singular routes delegate to the existing normalized view builders |
| CP-009 | T011 phase grouping, completion, precedence, no-phase, and route-equivalence tests | passed | phase fields are projections of shared task grouping and normalized task state |

## Scope Reconciliation Before Closure

| Broad requirement, design target, or review finding | Implemented in this spec | Coverage state | Deferred or rejected work | Destination | Blocks closure? | Evidence |
|-----------------------------------------------------|--------------------------|----------------|---------------------------|-------------|-----------------|----------|
| Sole public `slm` executable and retained installer | implemented, packaged, and documented | complete | Release notes are routed to release preparation because no release is being prepared in this phase. | release workflow | no | sole-bin contract, installed-tarball smoke, README and install reference |
| Active, task, requirement, and history views | source, bundles, and durable docs implemented | complete | none | none | no | T004-T008 evidence |
| Stable table/JSON output and selection semantics | source, packaged local paths, and durable docs implemented | complete | none | none | no | focused tests, installed-tarball smoke, runtime reference |
| Read-only packaged cross-platform operation | local package proof, full validation, and green six-job matrix complete | complete | none | none | no | source fingerprint, dispatcher tests, tarball smoke, GitHub Actions run 29683557635 |
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
| T001 | complete | Contract fixture and red tests established the public surface before implementation. | T001 task evidence. |
| T002 | complete | Shared normalized projections and resolver extensions passed focused regressions. | T002 task evidence. |
| T003 | complete | Shared-record checkpoint passed 22 tests and lifecycle lint. | T003 task evidence. |
| T004 | complete | Standard-library public CLI and all five query views passed 31 focused tests. | T004 task evidence. |
| T005 | complete | Public-command checkpoint passed 36 focused and regression tests. | T005 task evidence. |
| T006 | complete | Node dispatcher, sole-bin contract, shell-free query routing, and installer routing passed. | T006 task evidence. |
| T007 | complete | Bundles, package contract, dry-run, CI path, and isolated tarball smoke passed. | T007 task evidence. |
| T008 | complete | Durable README, design, runtime, install, and v0.5.0 release references updated; every documented query path passed against the checkout dispatcher. | none |
| T009 | complete | Full validation passed: 353 Python tests, 32 Node tests, scan, archive, prompts, package, sync, npm dry-run, whitespace, isolated tarball smoke, MCP lint, package/public-interface review, and six-job platform matrix. | none |
| T010 | complete | Added unified singular inventory and per-spec routing, retained compatible plural commands, synchronized both bundles, promoted durable guidance, and passed focused, package, and full validation. | none |
| T011 | complete | Added task-derived phase progress/current-state fields and table columns, preserved explicit no-phase absence, synchronized both bundles, promoted durable guidance, and passed focused, package, and full validation. | Future task states require explicit precedence review. |

## Evidence Log

| Date | Evidence | Result | Notes |
|------|----------|--------|-------|
| 2026-07-19 | MCP `spec_creation_plan` for `slm-public-cli` | passed | Allocated provisional Spec 039 with high confidence and revalidated fingerprint immediately before authoring. |
| 2026-07-19 | User decision record | passed | Approved `slm`, plural commands, literal pending plus open, both next surfaces, read-only scope, and no compatibility alias. |
| 2026-07-19 | MCP design/requirements/trace review and targeted Requirement 4/6 lookups | 0 findings | MCP `lint_spec_package` reported error=0, warn=0, info=0; `task_context` reported gaps=[] after the filter unions were recorded in `requirements.md`, `design.md`, and `traceability.md`. |
| 2026-07-19 | Phase 4 full validation | passed | `npm run validate` passed 353 Python tests, 31 Node tests, lifecycle/archive/prompt/package/sync checks, 158-file npm dry-run, and whitespace checks; isolated tarball smoke passed separately. |
| 2026-07-19 | Package and public-interface semantic review | 0 implementation findings; 1 external gate routed | Inspected `package.json`, `packaging/spec-lifecycle-manager/slm-cli.js`, shared public runtime, package tests, durable docs, history migration, and `docs/release-notes/v0.5.0.md`. The release maintainer owns platform CI before publish. |
| 2026-07-19 | v0.5.0 release-candidate validation | passed | After the version bump and source launcher addition, `npm run test:devcli` passed 17 tests, `npm run validate` passed 353 Python and 32 Node tests plus all lifecycle/package checks, and the isolated installed-tarball smoke passed. |
| 2026-07-19 | GitHub Actions cross-platform run 29683557635 | passed | All six Linux, macOS, and Windows jobs passed on Python 3.10 and 3.12, including the public `slm` built-package smoke. |
| 2026-07-22 | T010 singular `spec` implementation | passed | All seven live singular/plural JSON route pairs matched exactly; 34 focused Python tests, 7 dispatcher tests, isolated tarball smoke, source/Codex/Claude parity, and durable documentation checks passed. |
| 2026-07-22 | T010 full repository validation | passed | `npm run validate` passed 356 Python tests, 33 Node tests, lifecycle/archive/prompt/package/sync checks, npm dry-run, and whitespace checks. |
| 2026-07-22 | T011 task-derived phase projection | passed | Live output showed Spec 039 at tasks 10/11, phases 5/6, state in_progress, and Spec 034 with absent phase fields; 38 focused tests and installed-tarball smoke passed. |
| 2026-07-22 | T011 full repository validation | passed | `npm run validate` passed 360 Python tests, 33 Node tests, lifecycle/archive/prompt/package checks, source/Codex/Claude parity, npm dry-run, and whitespace checks. User-wide cache drift remains expected for this unreleased checkout. |

## Package And Public Interface Review

| Review target | Disposition | Evidence or owner |
|---------------|-------------|-------------------|
| Sole public executable and migration | passed | Package contract and tarball install expose only `slm`; durable docs name both removed aliases. |
| Installer/query boundary | passed | `install` remains in-process; query commands use the packaged interpreter resolver and an argument-vector spawn with no shell. |
| Shared lifecycle semantics | passed | Table and JSON render the same normalized records; selectors reuse shared resolver, next-task, priority, marker, and archive contracts. |
| Read-only and path safety | passed | Fixture fingerprints, repo-relative output tests, control-sequence sanitization, and isolated smoke passed. |
| Package contents and bundle parity | passed | Package contract, 158-file dry-run, source/Codex/Claude parity, and installed-tarball smoke passed. |
| Cross-platform release proof | passed | GitHub Actions run 29683557635 passed all six configured platform/interpreter jobs. |
| Breaking-change release communication | passed | `docs/release-notes/v0.5.0.md` names the sole `slm` bin, both removed aliases, and the required script migration. |

## Manual Or External Verification

- Verify help/table readability in a real terminal after automated output tests
  pass.
- The packaged executable was confirmed on Windows, macOS, and Linux through
  GitHub Actions run 29683557635 before publish.
- Publishing and user-wide installation are release activities outside the
  authorization granted by spec creation.

## Residual Risks

- Removing the existing executable names is intentionally breaking even if
  usage is believed absent; the v0.5.0 release notes make the rename visible.
- Table rendering can become noisy for long titles or paths; record identity
  and JSON must remain complete even if human summaries are bounded.
- Repositories with many active specs could make per-spec task aggregation
  expensive; implementation should measure and avoid repeated scans/lints.
- Future task markers must update the shared state map and open-state tests.

## Durable Promotion And Cleanup

| Spec content | Durable destination or deferral | Status | Evidence |
|--------------|---------------------------------|--------|----------|
| Public command and examples | `README.md` | complete | All documented inspection paths passed against the checkout dispatcher. |
| CLI architecture and shared-core boundary | `docs/design/spec-lifecycle-management.md` | complete | Public `slm`, maintainer `slc`, and agent MCP boundaries documented. |
| Commands, filters, output, states, and exit behavior | `docs/reference/spec-lifecycle-runtime.md` | complete | Shared selection, state, output, root, and failure semantics documented. |
| Bin migration, interpreter, and package verification | `docs/reference/spec-lifecycle-manager-mcp-install.md` | complete | Sole-bin migration and isolated tarball smoke documented. |
| Breaking rename and delivered features | `docs/release-notes/v0.5.0.md` | complete | Sole-bin migration and removed aliases documented. |
| Follow-up work | none | complete | Platform CI passed; review identified no new implementation backlog. |

### Spec Cleanup Decision

- **Cleanup action:** remove after promotion and closure evidence
- **Reason:** Active implementation scaffolding should not remain a parallel
  source of truth after the public CLI is documented durably.
- **Final spec commit:** pending
- **Closure log path:** `docs/history/spec-closure-log.md`
- **Closure log entry updated:** no
- **Closure cleanup commit:** pending
- **Active indexes updated:** no
- **Durable docs linked back to evidence where useful:** yes
- **Residual spec-only content:** none expected

## Ship Or Closure Risk

- **Risk level:** medium
- **Breaking change:** yes
- **Blast radius checked:** yes - npm bin, installer, bundle, docs, history, and CI paths reviewed
- **Rollback path:** restore prior bin map and package dispatcher in a follow-up release
- **Requires human review:** satisfied by the approved public contract; package/public-interface semantic review passed
- **Release notes needed:** yes
- **Follow-up issue or spec needed:** no unless review identifies residual work

### Risk Rationale

The inspection behavior is read-only, but the package executable rename and
cross-platform process boundary are externally visible. Shared-core reuse and
artifact-based tests limit semantic drift; tarball and platform validation are
required before release.

## Readiness Decision

- **Ready for implementation:** yes, after package lint and T001 selection
- **Ready for promotion:** yes - phase progress/state semantics are present in all durable targets
- **Ready for release:** yes - focused, bundle, installed-package, and full validation passed
- **Ready for closure:** yes - T001-T011 are complete; closure remains a separately authorized lifecycle action

## Related Artifacts

- Requirements: `requirements.md`
- Change Impact: `change-impact.md`
- Design: `design.md`
- Tasks: `tasks.md`
- Traceability: `traceability.md`
- Quickstart: `quickstart.md`
