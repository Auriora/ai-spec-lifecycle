---
title: Lifecycle adoption workflow verification
doc_type: spec
artifact_type: verification
status: draft
owner: platform
last_reviewed: 2026-07-19
---

# Lifecycle Adoption Workflow Verification

## Scope

Verify Requirements 1-6, Success Criteria SC-001 through SC-006, and Tasks
T001-T012: declarative implementation-start composition, next-action ordering,
MCP-first recovery presentation, measurable skill concision, package parity,
the explicit ordinary-write versus lifecycle-boundary hook contract, and
consumption of a qualified external dogfood report.

## Quality Gates

| Gate | Required? | Status | Evidence |
|------|-----------|--------|----------|
| Requirements, design, traceability, and success criteria reviewed | yes | passed | 2026-07-18 findings reconciliation; DR-001 through DR-003 resolved |
| Spec 034, B025, and Chat Analyser boundaries preserved | yes | passed | Requirements non-goals, slice boundary, and change impact |
| Explicit task-context lookup has no requirement or AC gaps | yes | passed | 2026-07-18 T002 and T006 runtime lookups returned linked requirements with no gaps |
| Stage readiness has no contract or downstream-review gaps | yes | passed | 2026-07-18 runtime reported `ready_for_agent=true`, `ready_to_implement=true`, and zero summarized gaps |
| Prompt/runtime tests pass | yes | passed | Five Phase 2 prompt checks and four Phase 3 routing contracts passed; supporting runtime/MCP/module checks also passed |
| Ordinary-write and lifecycle-boundary hook fixtures pass | yes | passed | 18 focused runtime/wrapper checks: ordinary writes exclude full lint, verification uses its narrow hook, resume/closure retain full checks, debounce/quiet/advisory/no-mutation behavior preserved |
| Mandatory skill-rule inventory and 37,399-byte ceiling pass | yes | passed | 2026-07-19 entrypoint is 16,452 bytes (69.2% below the 53,427-byte baseline); focused contract covers all eight categories and named expansions |
| Source and plugin bundles synchronized | yes | passed | 2026-07-19 package contract reported source/Codex and source/Claude parity in sync at 62 files each |
| Qualified external dogfood evidence reviewed | yes | passed | 2026-07-19 metadata-only receipt reviewed against Chat Analyser revision `9db3f5f7cbdbfd01ecd1a6d23d50cb8714339ea5`; analysis implementation remains external |
| Durable documentation promoted after validation | yes | pending | T011 depends on T009 and T010 |
| Closure risk and closure checks pass | yes | pending | |

## Validation Commands

| Command | Purpose | Result | Evidence |
|---------|---------|--------|----------|
| MCP `lint_spec_package` for Spec 038 | Validate package structure | passed via CLI recovery | Zero diagnostics; explicit package validation, not an ordinary write hook |
| MCP `task_context` for the selected task | Prove explicit requirement and AC mapping | passed via CLI recovery | T004 preflight resolved R3/R4 and all linked ACs with zero gaps; MCP unavailable in this session |
| MCP `stage_readiness` for Spec 038 | Check implementation readiness | passed via CLI recovery | `ready_for_agent=true`, `ready_to_implement=true`, zero summarized gaps; T004 selected |
| MCP `prompts_validate` | Validate prompt definitions | passed via CLI recovery | `spec_runtime.py prompts .` returned 11 prompts and zero diagnostics; MCP was unavailable in this session |
| Focused prompt and routing tests in `tests/runtime/test_spec_runtime.py` and `tests/runtime/test_spec_mcp_server.py` | Validate SC-001 through SC-003 | passed | Phase 2 prompt checks and four Phase 3 routing contracts passed, including ordering, blocker bounds/expansion, MCP-primary identity, CLI recovery, and provenance preservation |
| Focused hook tests in `tests/runtime/test_spec_runtime.py` and `tests/runtime/test_codex_spec_lifecycle_hook.py` | Validate SC-005 and CP-003 | passed | 18 focused checks passed on 2026-07-19 |
| `wc -c skills/spec-lifecycle-manager/SKILL.md` plus mandatory-rule inventory review | Validate SC-004 and CP-005 | passed | 16,452 bytes; all eight categories and five required named expansion families are enforced by a focused test |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'` | Full regression suite | passed | All 317 tests passed after the archive inventory fixture was reconciled with closed Spec 037 |
| `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py package-contract .` | Validate distribution contract | passed | Zero diagnostics; source/Codex and source/Claude mirrors in sync |
| `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py sync-guard .` | Validate source, bundles, installed cache, and reload evidence | passed | Installed and enabled version 0.3.0; 138-file cache matches the bundle with zero findings |
| `git diff --check` | Validate whitespace | passed | 2026-07-19 integrated worktree check returned no findings |
| Review bounded external Chat Analyser report | Validate SC-006 and CP-004 | passed | Receipt records producer revision `9db3f5f7...`, bounds, incomplete attempts, unavailable exact distribution, limitations, and no causal claim |

## Requirement, Property, And Success Coverage

| Contract | Planned evidence | Residual risk |
|----------|------------------|---------------|
| Requirement 1; CP-004; SC-006 | Reviewed external report receipt with preserved provisional/unavailable qualifications and durable promotion review | Producer may not supply an exact finding; observational adoption is not causal effectiveness |
| Requirement 2; CP-001; CP-006; SC-001 | Prompt composition, blocker, determinism, and unchanged-worktree fixtures | Client may choose not to follow prompt guidance |
| Requirement 3; SC-002 | Validation/evidence/promotion/closure transition fixtures | Semantic document correctness remains human-reviewed |
| Requirement 4; CP-002; SC-003 | MCP-visible and no-MCP adapter assertions | Host configuration can still force direct CLI use |
| Requirement 5; CP-005; SC-004 | Eight-category inventory, 37,399-byte ceiling, skill validation, and bundle parity | Client-owned skill loaders may still load the whole file |
| Requirement 6; CP-003; SC-005 | Ordinary-write, resume, closure, debounce, quiet-success, and no-mutation fixtures | Client hook delivery may differ |

## Agent Readiness Evidence

| Field | Evidence | Residual risk |
|-------|----------|---------------|
| Scope | Tasks T002-T010 implement and validate six bounded contracts; T011 promotes only after validation; T012 closes | T001 reconciliation validation pending |
| Context | Requirements, research, design, change impact, traceability, verification, runtime/design/dogfood durable docs | Refresh before each implementation family |
| Permissions | Repository source/docs/tests and bundle mirrors only; private histories and analyser implementation are out of scope | External report availability varies |
| Validation | Exact focused files and commands above, byte ceiling, inventory review, full tests, package contract, sync guard | Installed-client reload remains environment-dependent |
| Review | Fresh design/requirements trace review before T002; implementation review before T009; docs-promotion review before T012 | Human reviewer assignment remains external |
| Closure impact | T011 promotes design, runtime, hook, skill, dogfood, backlog, and roadmap behavior after T009/T010 | Promotion remains pending |

## Task Evidence

| Task ID | Status | Evidence | Notes |
|---------|--------|----------|-------|
| T001 | complete | 2026-07-18 package lint returned zero diagnostics; T002 and T006 task-context lookups returned no gaps; findings were converted into DR-001 through DR-003, measurable R5 acceptance, explicit hook boundaries, smaller tasks, and explicit requirement/AC/SC mappings | Final stage-readiness recheck follows this downstream review update |
| T002 | complete | Contract test added before implementation and failed only because `implementation-start` was absent and the prompt count was 10 | Covers R2, R4, CP-001, CP-002, and CP-006 |
| T003 | complete | Declarative prompt plus Codex/Claude mirrors added; five focused tests passed; prompt validation found 11 valid definitions; package source mirrors passed parity | No shared-core aggregate or mutation path added |
| T004 | complete | Three pre-implementation contracts failed only on the absent shared presentation, MCP identity, and separated recovery contract; a fourth fixture covers bounded blocker expansion | Covers R3, R4, CP-001, and CP-002 |
| T005 | complete | Shared action presentation composes existing validation, evidence, promotion, and closure authorities; four contract tests and supporting runtime/MCP/module checks passed; package mirrors are in sync | No competing readiness model added |
| T006 | complete | Five pre-implementation boundary checks preserved existing resume/closure, debounce, and advisory behavior and failed only on ordinary verification lint guidance and missing narrow wrapper dispatch | Covers R6 and CP-003 |
| T007 | complete | Ordinary verification guidance now names validation/evidence checks; wrapper dispatches `verification-updated`; 18 focused checks passed with mirrors synchronized | No persistent state, mutation, or blocking behavior added |
| T008 | complete | Source entrypoint reduced to 16,452 bytes; inventory/expansion regression contract and 11 package tests passed; package contract reports exact 62-file source/Codex/Claude parity | Entry-point reduction is 69.2%; installed-cache reload remains T009 |
| T009 | complete | 230 focused and 317 full tests passed; source/installed prompts, package, sync, archive, byte, inventory, copy, and whitespace checks passed; plugin 0.3.0 installed and enabled | Running session retained its pre-install advisory-hook path until reload; installed cache is clean |
| T010 | complete | Qualified metadata-only Chat Analyser receipt reviewed at producer revision `9db3f5f7...`; exact operation distribution remains unavailable | No analyser implementation or reconstructed count imported |
| T011-T012 | pending | | |

## Evidence Log

| Date | Evidence | Result | Notes |
|------|----------|--------|-------|
| 2026-07-18 | MCP `lint_spec_package` and `stage_readiness` before review reconciliation | superseded | Earlier authoring evidence reported no AC gaps; subsequent task/traceability review found shorthand mappings that the runtime could not resolve. |
| 2026-07-18 | Hook path and native-history provenance review | lifecycle change required | Hooks do not directly invoke MCP lint, but ordinary authoring guidance could recommend it. Spec 038 now forbids full-lint execution and advice from ordinary write hooks. |
| 2026-07-18 | Chat Analyser normalized capability inspection | routed externally | Exact normalized operation aggregates remain unavailable; repair and reconciliation belong in the Chat Analyser backlog. |
| 2026-07-18 | Design-requirements-trace review | changes addressed, validation pending | Seven findings produced explicit coverage mappings, resolved decisions, measurable skill acceptance, resliced tasks, post-validation promotion sequencing, and SC mappings. |
| 2026-07-18 | Reconciled package lint, T002/T006 task context, and stage readiness | passed for implementation planning | Lint returned zero diagnostics; task context returned explicit linked requirements with no gaps; stage readiness returned `ready_for_agent=true` and `ready_to_implement=true` with zero acceptance, blocking, context, downstream-review, property, or requirement gaps. |
| 2026-07-18 | Full repository `unittest` discovery after spec reconciliation | 306 passed, 1 unrelated baseline failure | `test_archive_index_validates_current_index` expects 36 entries while the current valid archive index contains 37; direct `archive-index .` validation returned zero errors/warnings and 37 removed entries. This existing test expectation is outside Spec 038 and remains visible for T009 regression review. |
| 2026-07-18 | T002 pre-implementation prompt contract | failed as expected | The new contract test could not find `implementation-start`; discovery and CLI count checks confirmed the baseline contained 10 prompts. |
| 2026-07-18 | T003 focused prompt validation | passed | Five runtime/MCP checks passed; CLI prompt validation returned 11 definitions and zero diagnostics; source, Codex, and Claude prompt trees were identical. |
| 2026-07-18 | Phase 2 package and regression validation | findings recorded | Package contract and whitespace passed; full discovery passed 307 of 308 tests with only the pre-existing 36-versus-37 archive-count expectation; installed 0.2.1 cache drift remains a T009 validation/install concern. |
| 2026-07-18 | Post-Phase 2 lifecycle gates | passed | Package lint and task-state audit returned zero findings; stage readiness and T004 active preflight reported ready with no context, requirement, acceptance, property, or downstream-review gaps. |
| 2026-07-18 | T004 pre-implementation routing contract | failed as expected | Shared presentation was absent, action entries lacked MCP-primary identity, and MCP responses did not separate CLI recovery. |
| 2026-07-18 | T005 focused routing and interface validation | passed | Four new contracts plus supporting runtime/MCP/module checks passed; routing orders validation, evidence quality, durable promotion, and closure, preserves blockers with bounded source expansion, keeps MCP primary, emits repo-relative recovery, and retains adapter provenance. |
| 2026-07-18 | Phase 3 package and focused regression validation | findings recorded | Package contract and whitespace passed with source/Codex/Claude parity; 210 of 211 focused module/runtime/MCP tests passed, with only the existing 36-versus-37 archive-count expectation failing. |
| 2026-07-18 | Full repository `unittest` discovery after Phase 3 | 311 passed, 1 unrelated baseline failure | The only failure remains `test_archive_index_validates_current_index`: its fixture expects 36 entries while the valid archive index contains 37. |
| 2026-07-18 | Post-Phase 3 package and lifecycle gates | passed | Package contract reported zero diagnostics and exact 62-file source/Codex/Claude parity; direct archive validation reported 37 valid entries with zero diagnostics; Spec 038 lint and task-state audit returned zero findings; stage readiness selected T006 with no gaps. |
| 2026-07-19 | T006 pre-implementation hook boundary | failed as expected | Resume/closure full validation, debounce, and advisory error handling passed; ordinary verification authoring still recommended `lint_spec_package`, and the wrapper did not dispatch `verification-updated`. |
| 2026-07-19 | T007 focused hook validation | passed | 18 runtime/wrapper checks covered ordinary spec, task, template, and verification writes; explicit resume and closure; debounce; quiet non-lifecycle writes; advisory failure behavior; and unchanged task content. |
| 2026-07-19 | Post-Phase 4 regression, package, and lifecycle gates | findings recorded | Full discovery passed 315 of 316 tests with only the existing archive-count expectation; package contract reported exact 62-file source/Codex/Claude parity; Spec 038 lint and task-state audit returned zero findings; stage readiness selected T008 with no gaps; whitespace passed. |
| 2026-07-19 | T008 concise skill entrypoint validation | passed with known unrelated regression finding | Source entrypoint reduced from 53,427 to 16,452 bytes while retaining the eight mandatory categories and direct expansions; 11 package tests passed; package contract found exact 62-file source/Codex/Claude parity; package lint and whitespace passed. Full discovery passed 316 of 317 tests, with only the existing 36-versus-37 archive-count expectation; direct archive validation returned 37 entries and zero diagnostics. |
| 2026-07-19 | T009 integrated validation and installed-package check | passed | Reconciled the archive fixture with Spec 037, then passed 230 focused and 317 full tests, source and installed prompt validation, package contract, sync guard, archive, byte, inventory, exact-copy, and whitespace checks. Codex reports plugin 0.3.0 installed and enabled; its 138-file cache is in sync. The current process retained the removed 0.2.1 advisory-hook path until session reload, without blocking writes. |
| 2026-07-19 | T010 qualified external report review | passed | Reviewed Chat Analyser revision `9db3f5f7cbdbfd01ecd1a6d23d50cb8714339ea5`; recorded the completed 22-history/174 MB bound and incomplete larger attempts, preserved exact operation distribution as unavailable, imported no semantic content, and made no correctness, preference, usefulness, or causal claim. |

## Review Reconciliation

Reviewed against the current requirements, design, tasks, and traceability on
2026-07-18. Planned validation now maps all six requirements, six correctness
properties, six success criteria, and twelve tasks; implementation evidence
remains pending from T002 onward.

## Scope Reconciliation Before Closure

| Broad target | Implemented in this spec | Coverage state | Deferred work | Destination | Blocks closure? | Evidence |
|--------------|--------------------------|----------------|---------------|-------------|-----------------|----------|
| Declarative implementation-start prompt | implemented | covered | shared-core aggregate if prompt acceptance fails | follow-up decision only if evidenced | no | T002-T003 focused tests and prompt/package validation |
| Evidence, promotion, and MCP/CLI routing | implemented | covered | remote telemetry | B025 | no | T004-T005 focused tests and package parity |
| Concise skill/capability guidance | implemented | covered pending integrated validation | client loader internals if still material | backlog or vendor | yes | T008 complete; T009 pending |
| Explicit advisory hook boundary | implemented | covered | blocking hooks or automatic ordinary-write validation | none | no | T006-T007 focused runtime and wrapper tests |
| Qualified external dogfood consumption | reviewed | covered pending promotion | extraction, attribution, reconciliation, and report generation | Chat Analyser backlog | no | T010 complete; T011 promotion pending |
| Phase-completion writer | none | out-of-scope | all mutation behavior | Spec 034 | no | requirements boundary |

## Residual Risks

- A smaller entrypoint cannot guarantee that a client will avoid rereading it.
- Hook advice may still influence agent choices at explicit lifecycle boundaries;
  this spec removes ordinary-write lint advice rather than measuring causality.
- External invocation distributions can change with client versions and
  available tools.
- The current external report has attribution gaps, so exact affected counts
  may remain provisional until Chat Analyser resolves its backlog items.
- Retained private histories are not lifecycle-manager fixtures and cannot
  become CI dependencies.

## Durable Promotion And Cleanup

| Spec content | Durable destination or deferral | Status | Evidence |
|--------------|---------------------------------|--------|----------|
| Workflow and action ordering | lifecycle design and runtime reference | pending T009/T010 validation | |
| Hook guidance behavior | runtime reference and dogfood evaluation | pending T009 validation | |
| Skill/capability behavior | source skill, references, bundle mirrors | pending T009 validation | |
| Qualified external finding | dogfood evaluation | pending T010 review | |
| Residual work and sequencing | owning backlogs and roadmap | pending T011 | |

### Spec Cleanup Decision

- **Cleanup action:** keep active
- **Reason:** implementation, validation, and promotion are pending
- **Final spec commit:** pending
- **Closure log path:** `docs/history/spec-closure-log.md`
- **Closure log entry updated:** no
- **Closure cleanup commit:** pending
- **Active indexes updated:** no
- **Residual spec-only content:** active delivery scaffolding through T012

## Ship Or Closure Risk

- **Risk level:** medium
- **Breaking change:** no
- **Blast radius checked:** no
- **Rollback path:** revert prompt, action-routing, hook-guidance, and
  skill-reference changes
- **Requires human review:** yes
- **Release notes needed:** yes
- **Follow-up issue or spec needed:** only if a resolved boundary fails
  acceptance without an in-slice solution

## Readiness Decision

- **Ready to implement:** yes; Phases 2 through 6 are complete and T011 is the
  next dependency-complete slice
- **Ready for promotion:** no
- **Ready for release:** no
- **Ready for closure:** no

## Related Artifacts

- Requirements: `requirements.md`
- Research: `research.md`
- Change Impact: `change-impact.md`
- Design: `design.md`
- Tasks: `tasks.md`
