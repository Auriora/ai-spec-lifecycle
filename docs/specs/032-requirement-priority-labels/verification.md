---
title: Requirement priority labels verification
doc_type: spec
artifact_type: verification
status: draft
authoring_mode: wizard
lifecycle_stage: verify
owner: platform
last_reviewed: 2026-07-06
backlog_item: B057
---

# Verification

## Scope

This verification record covers spec 032, Requirement priority labels. It maps
the quality gates, correctness properties, task checkpoints, residual risks,
and closure readiness checks needed before implementation can be accepted and
the temporary spec package can close.

## Quality Gates

| Gate | Required? | Status | Evidence |
|------|-----------|--------|----------|
| Parser and lint behavior covers Requirement 1, Requirement 2, CP-001, and CP-005 | yes | passed | T004 evidence: focused parser/lint and traceability regression tests passed on 2026-07-05. |
| Readiness and closure semantics cover Requirement 3, CP-002, CP-003, and CP-004 | yes | passed | T008 evidence: focused runtime tests, stage readiness, package lint, full unittest discovery, and source/bundle parity checks passed on 2026-07-06. |
| Traceability and MCP propagation cover Requirement 3 AC4, Requirement 4 AC2, CP-004, and CP-005 | yes | passed | T011 evidence: runtime and MCP tests passed on 2026-07-06. |
| Prompt, template, source-skill, and bundled-plugin parity cover Requirement 4 AC1 and AC3 | yes | passed | T015 evidence: prompt validation, package-contract, source-to-bundle parity, and source-to-Claude parity passed on 2026-07-06; sync-guard reported installed-cache drift warnings only. |
| Full repository validation covers Requirement 4 AC3 and AC4 | yes | passed | T017 evidence: `SPEC_LIFECYCLE_PYTHON=python3 npm run validate` passed on 2026-07-06. |
| Closure readiness covers all requirements and correctness properties | yes | passed with closure-prep advisory | T018 evidence: lint, promotion-plan, implementation review packet generation, archive-index, and closure-check were run. Closure cleanup still requires the final spec commit and closeout workflow. |

## Validation Commands

| Command | Purpose | Result | Evidence |
|---------|---------|--------|----------|
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_spec_runtime` | Focused parser, lint, readiness, closure, and traceability runtime checks. | passed, 140 tests | T004, T008, T011 |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.traceability.test_traceability_lookup` | Traceability lookup regression coverage for shared parser adoption. | passed, 9 tests | T004 |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'` | Full repository unittest discovery for runtime, MCP, traceability, package, and helper regressions. | passed, 223 tests | T008, T011, T015, T017 |
| MCP `lint_spec_package` for `docs/specs/032-requirement-priority-labels` | Lifecycle lint for spec 032. | passed, 0 diagnostics | T008, T015, T016 |
| MCP `stage_readiness` for `docs/specs/032-requirement-priority-labels` | Stage readiness coverage and next-task signal after phase 4. | passed, ready_to_implement true; selected next task T016 | T008, T015, T016 |
| `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py package-contract .` | Source and package contract plus bundled plugin parity. | passed, 0 diagnostics | T008, T015, T016, T017 |
| `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py sync-guard .` | Source/bundle/cache parity check after mirrored runtime, prompt, and template edits. | findings, 0 errors and 2 warnings | T008, T015, T016, T017; source-to-bundle and source-to-Claude parity passed; installed cache drift remains until install/reload. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_spec_runtime tests.runtime.test_spec_mcp_server` | Focused runtime plus MCP propagation checks. | passed, 175 tests | T011, T015, T016 |
| `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py prompts .` | Prompt definition validation. | passed, 0 diagnostics | T015, T016, T017 |
| `SPEC_LIFECYCLE_PYTHON=python3 npm run validate` | Repository validation bundle including Python unit tests, Node tests, lifecycle scan, archive-index, prompts, package-contract, sync-guard, npm pack dry-run, and whitespace. | passed | T017 |
| `git diff --check` | Whitespace validation before commit and closure. | passed | T008, T011, T015, T016, T017 |
| MCP `lint_spec_package` | Lifecycle package lint for spec 032. | passed, 0 diagnostics | T016, T018 |
| MCP `stage_readiness` | Implementation readiness check for spec 032. | passed, no blocking gaps | T016 |
| MCP `closure_check` | Closure readiness check for spec 032. | passed, ready true, 0 blockers | T018 |
| `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py promotion-plan docs/specs/032-requirement-priority-labels` | Durable promotion target reconciliation. | passed, no missing targets | T018 |
| `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py review-packet docs/specs/032-requirement-priority-labels --review-type implementation` | Implementation review packet generation. | passed, packet generated with no required artifact missing | T018 |
| `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py archive-index .` | Closed-spec archive and closure-log consistency. | passed, 0 diagnostics | T018 |

## Requirement Coverage

| Requirement | Acceptance criteria covered | Evidence | Residual risk |
|-------------|-----------------------------|----------|---------------|
| Requirement 1 | AC1, AC2, AC3, AC4, AC5, AC6 | Parser, lint, template, traceability, and final validation through T001-T004, T012, T016, and T018. | No implementation residual risk. |
| Requirement 2 | AC1, AC2, AC3 | Backward-compatibility fixtures, historical package behavior, template validation, and archive-index validation through T001, T003, T004, T012, T016, and T018. | No implementation residual risk. |
| Requirement 3 | AC1, AC2, AC3, AC4, AC5 | Coverage disposition, readiness, closure, traceability, agent-context validation, and durable docs through T005-T011, T014, T016, and T018. | No implementation residual risk. |
| Requirement 4 | AC1, AC2, AC3, AC4 | Prompt, structured-output, package parity, fixture, and full validation through T009-T017. | Installed cache and released package may lag source until install/reload or release packaging. |

## Correctness Property Coverage

| Property | Covered by | Evidence | Residual risk |
|----------|------------|----------|---------------|
| CP-001 | T001, T003, T004, T016 | Parser/lint tests for unlabeled active and historical specs. | Covered. |
| CP-002 | T005, T006, T007, T008, T016 | Runtime coverage tests for incomplete `must-have` requirements. | Covered. |
| CP-003 | T005, T006, T007, T008, T016 | Runtime coverage tests for routed `could-have` requirements. | Covered. |
| CP-004 | T002, T007, T009, T010, T011, T016 | Runtime/MCP payload tests for priority propagation. | Covered. |
| CP-005 | T001, T002, T009, T010, T016 | Parser and traceability tests showing acceptance criteria inherit parent requirement priority. | Covered. |

## Scope Reconciliation Before Closure

| Broad requirement, design target, or review finding | Implemented in this spec | Coverage state | Deferred or rejected work | Destination | Blocks closure? | Evidence |
|-----------------------------------------------------|--------------------------|----------------|---------------------------|-------------|-----------------|----------|
| Requirement-level MoSCoW metadata syntax and parser | T001-T004, T012 | complete | none | none | no | Parser, lint, and source template evidence recorded through T001-T004 and T012. |
| Priority-aware readiness and closure semantics | T005-T008, T014, T018 | complete | none | none | no | Runtime helper, readiness, closure behavior, durable documentation, and final closure-prep reconciliation are complete. |
| Priority propagation through traceability, MCP, and agent context | T009-T011 | complete | none | none | no | Runtime and MCP tests prove `traceability_lookup`, `task_context`, and `agent_readiness_packet` include priority from source requirements without task-row duplication. |
| Prompt, template, source skill, runtime docs, and bundled plugin parity | T012-T017 | complete | none | none | no | Templates, prompts, source skill, durable docs, bundled plugin copies, and full validation passed through T012-T017. |

## Agent Readiness Evidence

| Field | Evidence | Residual risk |
|-------|----------|---------------|
| Scope and out-of-scope files | Scope is limited to parser/runtime, traceability/MCP payloads, prompts/templates, durable docs, tests, and plugin bundle parity listed in `tasks.md`. New MCP tools and task-status semantic rewrites are out of scope. | None identified before implementation. |
| Must-read and optional context | Must read `requirements.md`, `design.md`, `tasks.md`, `traceability.md`, this verification record, and linked durable docs for the selected task. | Context may need refresh after upstream artifact edits. |
| Permissions and approval points | Normal repo edits are allowed for selected task files; no external services or secrets are required. Human decision required only if implementation would change accepted scope or closure semantics beyond this design. | None identified before implementation. |
| Validation commands and expected signals | Focused runtime/MCP tests, prompt validation, package-contract, sync-guard, full validation, lifecycle lint/readiness/closure checks, archive-index, and `git diff --check` passed or returned expected closure-prep blockers. | None beyond installed cache drift. |
| Review needs | Implementation review packet was generated; no missing required artifacts were reported. | Human review may still be requested before final closeout. |
| Durable-doc or closure impact | Durable docs and backlog targets are listed in `requirements.md#durable-impact` and `traceability.md#requirement-to-delivery-matrix`; promotion-plan reports no missing targets. | B057 is ready to mark done during final closure cleanup. |

## Task Evidence

| Task ID | Status | Evidence | Notes |
|---------|--------|----------|-------|
| T001 | complete | Parser fixtures and runtime tests cover unlabeled requirements, canonical `must-have`/`should-have`/`could-have` labels, duplicate priority lines, shorthand labels, unknown labels, and `won't-have` exclusion values. | Verified by focused runtime tests. |
| T002 | complete | `lifecycle.requirements` now provides shared requirement parsing, acceptance-criteria extraction, optional priority parsing, and parser diagnostics consumed by `core.py` and `traceability.py`. | Existing requirement IDs and acceptance-criteria payloads remain backward compatible. |
| T003 | complete | Requirements lint reports duplicate, shorthand, unknown, and `won't-have` priority values; missing priority remains non-diagnostic. | Verified by focused runtime tests and spec package lint. |
| T004 | complete | Focused parser/lint checkpoint passed; no parser compatibility risk found before coverage semantics implementation. | Runtime and traceability regression tests passed. |
| T005 | complete | Added phase 2 runtime classification tests. | Covered priority and coverage-state combinations required by the task. |
| T006 | complete | Implemented shared `requirement_coverage_disposition` helper. | Source and bundled plugin runtime copies are aligned. |
| T007 | complete | Integrated priority coverage into `stage_readiness`, `closure_check`, and closure-risk blocker flow. | Structured output includes requirement priority where requirement coverage is reported. |
| T008 | complete | Focused runtime tests, package lint, stage readiness, package contract, sync guard, full unittest discovery, and whitespace validation were run. | `sync-guard` reports installed cache drift only; source-to-bundle parity passed. |
| T009 | complete | Runtime and MCP tests cover task context, task-form traceability lookup, requirement-form traceability lookup, and agent readiness payloads. | Priority is read from source requirements even when traceability rows do not carry a `Priority` column. |
| T010 | complete | Requirement-form traceability lookup now returns parsed requirement objects with priority; existing MCP handlers expose shared payloads directly. | No new MCP tool or shell-out path was added. |
| T011 | complete | Runtime plus MCP test modules passed 175 tests; spec lint and package contract passed; sync guard source parity passed with installed-cache drift warnings only. | Installed cache still needs install/reload before plugin-scoped MCP uses the refreshed package. |
| T012 | complete | Requirements and traceability source templates now show requirement-level MoSCoW priority and a requirement-level `Priority` traceability column for closure reconciliation. | No acceptance-criterion-level priority duplication introduced. |
| T013 | complete | Documentation wizard and lint-spec prompts now normalize requirement-level priority, keep missing labels compatible, route `won't-have` to exclusions, and source skill guidance documents authoring plus closure semantics. | Prompt validation passed with 0 diagnostics. |
| T014 | complete | Durable lifecycle design and runtime reference now document accepted priority syntax, compatibility behavior, affected runtime/MCP outputs, and closure reconciliation semantics. | Durable promotion for phase 4 is complete. |
| T015 | complete | Source skill files were mirrored into Codex and Claude plugin bundles; prompt validation, package-contract, spec lint, focused runtime/MCP tests, full unittest discovery, stage-readiness, and `git diff --check` passed. | `sync-guard` reports installed-cache drift only; reinstall/reload remains needed before installed plugin cache uses these changes. |
| T016 | complete | Focused runtime/MCP tests, prompt validation, spec lint, stage readiness, package-contract, sync-guard, task-state audit, and `git diff --check` were run. | `sync-guard` reports installed cache drift only; source-to-bundle and source-to-Claude parity pass. |
| T017 | complete | `SPEC_LIFECYCLE_PYTHON=python3 npm run validate` passed. | Plain `npm run validate` fails in this shell because the installer test cannot resolve Python without `SPEC_LIFECYCLE_PYTHON`; the override points at Python 3.13.7. |
| T018 | complete | Lifecycle lint, promotion-plan, implementation packet generation, archive-index, backlog B057 reconciliation, task-state audit, and closure-check passed. | Closure cleanup still needs the final spec commit, closure-log/archive-index closeout, and package removal in the close workflow. |

## Evidence Log

| Date | Evidence | Result | Notes |
|------|----------|--------|-------|
| 2026-07-05 | Verification artifact created and traceability mappings updated before implementation. | pending validation | Addresses readiness finding that CP-001 through CP-005 lacked verification mapping and checkpoint tasks referenced a missing artifact. |
| 2026-07-05 | Phase 1 parser foundation implemented and validated. | passed | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_spec_runtime` passed 135 tests; `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.traceability.test_traceability_lookup` passed 9 tests; package lint reported 0 diagnostics; `git diff --check` passed. |
| 2026-07-06 | Phase 2 readiness and closure semantics implemented and validated. | passed with advisory | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_spec_runtime` passed 139 tests; full unittest discovery passed 221 tests; spec lint, stage readiness, package contract, and `git diff --check` passed. `sync-guard` reported installed cache drift warnings only. |
| 2026-07-06 | Phase 3 traceability, MCP, and agent-context priority propagation implemented and validated. | passed with advisory | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_spec_runtime tests.runtime.test_spec_mcp_server` passed 175 tests; full unittest discovery passed 223 tests; spec lint, stage readiness, package contract, and `git diff --check` passed. `sync-guard` reported installed cache drift warnings only. |
| 2026-07-06 | Phase 4 authoring surfaces, durable docs, and bundled plugin copies implemented and validated. | passed with advisory | Prompt validation, spec lint, package-contract, focused runtime/MCP tests, full unittest discovery, stage-readiness, task-state audit, and `git diff --check` passed. `sync-guard` reported installed cache drift warnings only while source-to-bundle and source-to-Claude parity passed. |
| 2026-07-06 | Phase 5 verification, full validation, and closure preparation completed. | passed with advisory | Focused runtime/MCP tests passed 175 tests; full validation passed with `SPEC_LIFECYCLE_PYTHON=python3 npm run validate`; package-contract, prompts, lint, stage-readiness, promotion-plan, archive-index, and `git diff --check` passed. `sync-guard` reports installed-cache drift until install/reload. |

## Manual Or External Verification

No manual or external verification beyond local command execution has been
performed. Final human review remains optional before closure.

## Residual Risks

- Installed plugin cache and any released npm package may lag source behavior
  until local install/reload or release packaging runs.
- Final closure still needs a final spec commit hash, closure-log/archive-index
  records, B057 status update, and active package removal or cleanup action.
- Plain `npm run validate` fails in this shell unless
  `SPEC_LIFECYCLE_PYTHON=python3` is supplied for installer tests; the validated
  override resolves to Python 3.13.7.

## Durable Promotion And Cleanup

| Spec content | Durable destination or deferral | Status | Evidence |
|--------------|---------------------------------|--------|----------|
| Requirements and accepted priority behavior | `skills/spec-lifecycle-manager/references/spec-package/requirements.md`, `docs/design/spec-lifecycle-management.md` | complete | T012, T014 |
| Runtime/MCP behavior | `docs/reference/spec-lifecycle-runtime.md` | complete | T014 |
| Prompt behavior | `skills/spec-lifecycle-manager/prompts/` and bundled plugin copies | complete | T013, T015 |
| Decisions and rationale | Durable design/reference docs and closure log at closure | ready for closure | T018 |
| Follow-up work | `docs/backlog/README.md` B057 status update during closure | ready for closure | T018 |

### Spec Cleanup Decision

- **Cleanup action:** remove after durable promotion and final spec commit
- **Reason:** Active spec packages are temporary delivery scaffolding.
- **Final spec commit:** pending; use the next commit that records completed T016-T018 evidence.
- **Closure log path:** `docs/history/spec-closure-log.md`
- **Closure log entry updated:** no
- **Closure cleanup commit:** pending
- **Active indexes updated:** no
- **Durable docs linked back to evidence where useful:** yes
- **Residual spec-only content:** listed below

Residual spec-only content:

- Final closure log, archive index, and active-package cleanup remain outside
  this phase until the close workflow runs.

## Ship Or Closure Risk

- **Risk level:** low
- **Breaking change:** no
- **Blast radius checked:** yes
- **Rollback path:** not required
- **Requires human review:** optional
- **Release notes needed:** no
- **Follow-up issue or spec needed:** no

### Risk Rationale

Risk is low after validation because parser, closure, traceability, MCP,
prompt, package, and full validation checks passed. Remaining risk is
operational: installed cache/released package drift until install/reload or
release packaging, and final closure bookkeeping still needs the close workflow.

## Readiness Decision

- **Ready for promotion:** yes
- **Ready for release:** source-ready; install/release packaging still required
- **Ready for closure:** yes, after committing final spec evidence

## Related Artifacts

- Requirements: `requirements.md`
- Change Impact: embedded in `requirements.md`
- Design: `design.md`
- Tasks: `tasks.md`
- Traceability: `traceability.md`
