---
title: Guided documentation wizard verification
doc_type: spec
artifact_type: verification
status: active
owner: platform
last_reviewed: 2026-07-04
---

# Verification

## Scope

This verification record covers the guided documentation wizard spec package and
future implementation tasks T001-T007.

## Quality Gates

| Gate | Required? | Status | Evidence |
|------|-----------|--------|----------|
| Requirements acceptance criteria reviewed | yes | passed | 2026-07-04: R1-R7 reviewed against prompt content, durable docs, and focused tests. |
| Task evidence complete | yes | passed | 2026-07-04: T001-T007 marked complete or no-op with evidence in `tasks.md`. |
| Automated tests pass or alternate verification recorded | yes | passed | 2026-07-04: focused prompt tests passed; full validation passed. |
| Durable documentation updates identified | yes | passed | 2026-07-04: design, runtime reference, backlog, and skill guidance updated. |
| Durable documentation promoted or explicitly deferred | yes | passed | 2026-07-04: prompt-only wizard behavior promoted to durable docs. |
| Spec cleanup decision recorded | yes | passed | 2026-07-04: cleanup action is removal after final spec commit. |
| Governance or policy conflicts resolved | yes | passed | 2026-07-04: v1 remains prompt-only, read-only, and preview-first. |
| Prompt definitions validate when changed | yes | passed | 2026-07-04: `spec_runtime.py prompts .` returned zero diagnostics with 10 prompts. |
| Source and bundle parity checked when skill files change | yes | passed | 2026-07-04: `package-contract` passed with source, Codex bundle, and Claude bundle parity in sync. |

## Validation Commands

| Command | Purpose | Result | Evidence |
|---------|---------|--------|----------|
| MCP `scan_specs` | Confirm active spec inventory and package health. | passed | 2026-06-14: reported 3 active specs with 3 active pass, including `026-guided-documentation-wizard`. |
| MCP `lint_spec_package` for `docs/specs/026-guided-documentation-wizard` | Validate package structure. | passed | 2026-06-14: no diagnostics. |
| MCP `prompts_validate` | Validate prompt definitions when prompt files change. | passed | 2026-06-14: no diagnostics; no prompt files changed in initial package creation. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'` | Run full unit suite after implementation. | passed | 2026-06-14: 144 tests passed. |
| `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py scan .` | CLI recovery scan. | passed | 2026-06-14: reported 3 active specs with 3 active pass. |
| `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py prompts .` | CLI prompt validation. | passed | 2026-06-14: no diagnostics. |
| `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py package-contract .` | Package parity when bundles change. | passed | 2026-07-04: source, Codex bundle, and Claude bundle parity in sync. |
| `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py sync-guard .` | Source/bundle/install drift check when skill or plugin files change. | warning | 2026-07-04: source and bundles are in sync; installed cache drift remains until install/reload. |
| `git diff --check` | Whitespace validation. | passed | 2026-06-14: no whitespace errors. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_spec_runtime.SpecRuntimeTests.test_prompt_definitions_are_discoverable_and_valid tests.runtime.test_spec_runtime.SpecRuntimeTests.test_documentation_wizard_prompt_covers_guided_workflow_contract tests.runtime.test_spec_runtime.SpecRuntimeTests.test_cli_prompts_outputs_json` | Focused prompt regression coverage. | passed | 2026-07-04: 3 tests passed. |
| `SPEC_LIFECYCLE_PYTHON=python3 npm run validate` | Full repository validation. | passed | 2026-07-04: Python unittest, Node tests, scan, archive-index, prompts, package-contract, sync-guard, npm pack dry-run, and `git diff --check` passed; sync-guard retained the accepted installed-cache reload warning. |

## Requirement Coverage

| Requirement | Acceptance criteria covered | Evidence | Residual risk |
|-------------|-----------------------------|----------|---------------|
| R1 Stage-Aware Wizard Entry Point | AC1-AC4 | `documentation-wizard` prompt instructs agents to use scan/preflight/no-active/blank-repo context and ask for selection when needed. | Prompt-only enforcement depends on agent compliance. |
| R2 Step-By-Step Documentation Flow | AC1-AC4 | Prompt records stage order and one-question-default requirements/design/tasks guidance. | Checklist mode remains allowed only on request. |
| R3 Open-Question Guidance | AC1-AC4 | Prompt requires why-it-matters, affected stage, answer format, blocking status, artifact destination, and implementation-readiness impact. | Semantic quality needs dogfood. |
| R4 Feedback Disposition Workflow | AC1-AC4 | Prompt requires exactly one disposition: accept, revise, defer, reject, or human decision required. | Disposition wording may need refinement after use. |
| R5 Preview-First Edit Plan | AC1-AC4 | Prompt requires repo-relative path, target section, change type, and rationale before file edits. | Manual edits remain outside a wizard tool. |
| R6 Existing Tool Composition | AC1-AC4 | Prompt composes existing read-only lifecycle tools and `prompts` validation passed. | No deterministic wizard payload exists by design. |
| R7 Durable Promotion And Closure Awareness | AC1-AC4 | Prompt and durable docs require durable destinations, unresolved spec-only content, validation evidence, and closure blockers at promotion/closure. | Closure records still require normal lifecycle process. |

## Correctness Property Coverage

| Property | Covered by | Evidence | Residual risk |
|----------|------------|----------|---------------|
| CP-001 | Prompt content review (no runtime code; D001 resolved prompt-only) | 2026-07-04 focused prompt test asserts readiness is blocked by open questions/review/stale dependencies. | Agent compliance remains residual risk. |
| CP-002 | Prompt content review | 2026-07-04 focused prompt test asserts full stage order and explicit exception handling. | |
| CP-003 | Prompt content review | 2026-07-04 focused prompt test asserts feedback dispositions are enumerated. | |
| CP-004 | Prompt content review | 2026-07-04 focused prompt test asserts preview plan fields. | |
| CP-005 | Prompt content review or manual review | 2026-07-04 focused prompt test asserts removed packages are historical evidence only. | |

## Agent Readiness Evidence

| Field | Evidence | Residual risk |
|-------|----------|---------------|
| Scope and out-of-scope files | Prompt-only changes touch prompts, skill guidance, durable docs, plugin bundles, tests, and spec evidence. No runtime/MCP tool added. | |
| Must-read and optional context | Requirements, design, change impact, traceability, verification, existing prompt schema, and durable runtime/design docs reviewed. | |
| Permissions and approval points | No write-capable wizard tool added; ordinary approved file edits only. | |
| Validation commands and expected signals | Prompt validation, focused tests, package-contract, sync-guard, full validation, and whitespace checks recorded. | |
| Review needs | Human dogfood recommended because conversational guidance quality cannot be fully proven by tests. | |
| Durable-doc or closure impact | Durable docs and bundle copies updated; closure action is removal after final spec commit. | |
| Optional repo-evidence provider caveats | Sync-guard installed-cache drift remains until local install/reload. | |

## Task Evidence

| Task ID | Status | Evidence | Notes |
|---------|--------|----------|-------|
| T001 | complete | D001-D004 resolved 2026-06-17; see design.md Open Questions and traceability.md Open Decision Impact. | |
| T002 | complete | `documentation-wizard` prompt, prompt README, skill guidance, and prompt tests added 2026-07-04. | |
| T003 | no_op | Not building per D001 (resolved 2026-06-17: v1 is prompt-only). | |
| T004 | complete | Wizard behavior promoted to design doc, runtime reference, backlog, and skill guidance 2026-07-04. | |
| T005 | complete | Source prompt/skill changes mirrored to Codex and Claude plugin bundles; package-contract passed. | Installed cache needs install/reload. |
| T006 | complete | Prompt validation, focused tests, package-contract, and sync-guard completed 2026-07-04. | Sync-guard warning accepted as install/reload residual. |
| T007 | complete | Final evidence and cleanup decision recorded 2026-07-04. | Closure log/archive update occurs after final spec commit. |

## Evidence Log

| Date | Evidence | Result | Notes |
|------|----------|--------|-------|
| 2026-06-14 | Initial package creation | passed | Created from user request to add a wizard-like guided documentation workflow. MCP lint/scan, prompt validation, CLI scan/lint/prompts, full unit suite, and `git diff --check` passed. |
| 2026-07-04 | `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py prompts .` | passed | 10 prompt definitions, zero diagnostics. |
| 2026-07-04 | Focused prompt regression tests | passed | 3 tests passed, including wizard semantic contract coverage. |
| 2026-07-04 | `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py package-contract .` | passed | Source, Codex bundle, and Claude bundle parity in sync. |
| 2026-07-04 | `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py sync-guard .` | warning | Source and bundles in sync; installed cache drift expected until install/reload. |
| 2026-07-04 | `SPEC_LIFECYCLE_PYTHON=python3 npm run validate` | passed | Full validation passed, including 168 Python tests, 17 Node tests, active scan pass, archive-index pass, prompt validation, package-contract, sync-guard, npm pack dry-run, and `git diff --check`. |
| 2026-07-04 | `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py scan .` | passed | One active spec, `026-guided-documentation-wizard`, with pass health and zero diagnostics. |

## Manual Or External Verification

Manual semantic review was performed by comparing the prompt content against
R1-R7 and CP-001 through CP-005. No external publish, install, or runtime reload
was performed.

## Residual Risks

- The wizard could duplicate existing `developer-start`, `lifecycle-triage`,
  and `stage-readiness` behavior unless implementation stays compositional.
- Semantic guidance quality will need dogfood beyond deterministic schema tests.
- Already-running MCP sessions need package install/reload before the installed
  plugin cache exposes the new prompt.

## Durable Promotion And Cleanup

| Spec content | Durable destination or deferral | Status | Evidence |
|--------------|---------------------------------|--------|----------|
| Wizard staged workflow | `docs/design/spec-lifecycle-management.md` | promoted | 2026-07-04 prompt-only wizard section added. |
| Runtime/MCP/prompt surface | `docs/reference/spec-lifecycle-runtime.md` | promoted | 2026-07-04 `documentation-wizard` prompt documented. |
| Open-question and feedback guidance | `skills/spec-lifecycle-manager/SKILL.md` | promoted | 2026-07-04 guidance added and mirrored to plugin bundles. |
| Backlog overlap | `docs/backlog/README.md` | promoted | 2026-07-04 B049 clarified as prompt-only v1 while active. |
| Follow-up write-capable behavior, if rejected for v1 | backlog or follow-up spec | not needed | D004 records write-capable helper out of scope; existing B050/B056 cover related helper ideas. |

### Spec Cleanup Decision

- **Cleanup action:** remove after final spec commit
- **Reason:** Prompt-only wizard behavior has been promoted into durable docs,
  source prompt definitions, bundle copies, and tests.
- **Final spec commit:** pending final commit
- **Closure log path:** `docs/history/spec-closure-log.md`
- **Closure log entry updated:** no
- **Closure cleanup commit:** pending
- **Active indexes updated:** pending removal commit
- **Durable docs linked back to evidence where useful:** yes
- **Residual spec-only content:** none identified yet

Residual spec-only content:

- None. Prompt-only behavior is promoted to durable docs and prompt source.

## Ship Or Closure Risk

- **Risk level:** low
- **Breaking change:** no
- **Blast radius checked:** yes
- **Rollback path:** not required
- **Requires human review:** optional dogfood review
- **Release notes needed:** yes, prompt/plugin behavior changes
- **Follow-up issue or spec needed:** no, unless write-capable wizard behavior is
  deferred

### Risk Rationale

The package changes user-facing lifecycle guidance by adding a prompt-only
surface. It does not add runtime parsing, write-capable MCP tools, or breaking
behavior. Remaining risk is semantic prompt quality and installed-cache reload.

## Readiness Decision

- **Ready for promotion:** yes
- **Ready for release:** yes
- **Ready for closure:** yes, after final spec commit

## Related Artifacts

- Requirements: [requirements.md](requirements.md)
- Change Impact: [change-impact.md](change-impact.md)
- Design: [design.md](design.md)
- Tasks: [tasks.md](tasks.md)
- Traceability: [traceability.md](traceability.md)
