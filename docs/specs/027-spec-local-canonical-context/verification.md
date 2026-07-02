---
title: Spec-local canonical context verification
doc_type: spec
artifact_type: verification
status: active
owner: platform
last_reviewed: 2026-06-19
---

# Verification

## Scope

This verification record covers the active spec package for adding
spec-local canonical context to the `spec-lifecycle-manager` workflow. It
currently records authoring checks for the spec package itself and the
validation gates required before implementation and closure.

## Quality Gates

| Gate | Required? | Status | Evidence |
|------|-----------|--------|----------|
| Requirements acceptance criteria reviewed | yes | passed | T009 checkpoint reviewed R1-R7 coverage against implementation, dogfood evidence, and promotion-plan output. |
| Task evidence complete | yes | passed | T001-T009 have concrete validation or implementation evidence. |
| Automated tests pass or alternate verification recorded | yes | passed | 2026-07-02: full unittest suite passed, 151 tests. |
| Durable documentation updates identified | yes | passed | See `change-impact.md` and `canonical-context.md` Promotion Map. |
| Durable documentation promoted or explicitly deferred | yes | passed | Accepted behavior is promoted to durable docs, skill guidance, templates, prompts, runtime reference, migration guide, runtime, and tests. |
| Spec cleanup decision recorded | yes | passed | Keep active until final spec commit and closure-log/archive-index cleanup. |
| Governance or policy conflicts resolved | yes | passed | No governance or policy conflict found; external authorities remain explicitly higher priority. |

## Validation Commands

| Command | Purpose | Result | Evidence |
|---------|---------|--------|----------|
| `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py lint docs/specs/027-spec-local-canonical-context` | Validate this spec package structure. | passed | 2026-07-02: zero diagnostics. |
| `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py scan .` | Validate active spec inventory and health. | passed | 2026-07-02: four active specs, four pass, zero warnings/errors. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'` | Validate runtime behavior after implementation. | passed | 2026-07-02: 150 tests passed. |
| `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py prompts .` | Validate prompt definitions if prompts change. | passed | 2026-07-02: zero diagnostics. |
| `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py archive-index .` | Validate closure/archive metadata before closure. | passed | 2026-07-02: zero diagnostics; 25 removed entries, zero legacy gaps. |
| `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py package-contract .` | Validate package source/bundle contract. | passed | 2026-07-02: source, Codex bundle, and Claude bundle in sync. |
| `git diff --check` | Catch whitespace issues. | passed | 2026-07-02: no whitespace errors. |

## Requirement Coverage

| Requirement | Acceptance criteria covered | Evidence | Residual risk |
|-------------|-----------------------------|----------|---------------|
| Requirement 1 | AC1-AC4 | T002-T006 implemented; lint, scan, prompts, and tests passed. | Diagnostics intentionally remain advisory. |
| Requirement 2 | AC1-AC4 | Durable docs, skill guidance, template, and canonical-context artifact preserve external authority exceptions. | Runtime cannot prove every governance conflict. |
| Requirement 3 | AC1-AC4 | Template and runtime fixtures cover imported-source source path, canonical scope, and promotion target metadata. | Source revision/date may be unavailable in some repos. |
| Requirement 4 | AC1-AC4 | Agent readiness now includes canonical-context artifact and guardrail when present. | MCP output shape remains additive. |
| Requirement 5 | AC1-AC4 | Promotion-plan reads canonical promotion map; closure-check blocks unresolved required canonical promotion. | Closure severity depends on accurate promotion-map rows. |
| Requirement 6 | AC1-AC4 | Fallback template added; runtime diagnostics scoped to explicit risk signals; scan stays clean for existing active specs. | Existing specs should not be forced to migrate. |
| Requirement 7 | AC1-AC4 | Prompt definitions and runtime import-plan payloads updated; deterministic dogfood test proves stale-doc risk produces a canonical-context import plan without a second prompt. | Full interactive new-spec creation remains manual workflow coverage, not automated package creation. |

## Correctness Property Coverage

| Property | Covered by | Evidence | Residual risk |
|----------|------------|----------|---------------|
| CP-001 | T002, T003, T005 docs/runtime review | Passed by docs, skill, prompts, and template wording preserving external authorities. | Runtime may not fully prove policy semantics. |
| CP-002 | T004, T005 template/runtime checks | Passed by focused runtime tests for imported-source metadata. | Table parsing is intentionally simple. |
| CP-003 | T006, T007, T009 closure guidance | Passed by focused runtime test for unresolved required canonical promotion blocker and final closure-check. | Final closure cleanup still requires a final spec commit and closure record. |
| CP-004 | T003, T005, T006 readiness/task-context output | Passed by additive readiness guardrail and prompt guidance. | Requires careful context-budget use by agents. |
| CP-005 | T005, T006, T008 creation/resume import-plan behavior | Covered by prompt guidance, runtime import-plan payload, and deterministic dogfood fixture for stale-doc risk. | Full interactive new-spec creation remains manual workflow coverage. |

## Agent Readiness Evidence

| Field | Evidence | Residual risk |
|-------|----------|---------------|
| Scope and out-of-scope files | Scope is lifecycle docs, skill guidance, templates, runtime checks, and tests listed in `tasks.md`. Out of scope: new sync engine, governance rewrite, autonomous write-capable MCP tools. | Pending implementation. |
| Must-read and optional context | Must read this spec package, `docs/design/spec-lifecycle-management.md`, `docs/design/coding-agent-operating-model.md`, `docs/governance/constitution.md`, `skills/spec-lifecycle-manager/SKILL.md`, templates, and relevant runtime sections. | None known. |
| Permissions and approval points | Normal repo edits only. Stop before changing governance authority semantics. | None known. |
| Validation commands and expected signals | Listed in Validation Commands. | Runtime command set may expand if implementation touches MCP prompts. |
| Review needs | Design/requirements/traceability review before runtime implementation; closure review before package removal. | Pending. |
| Durable-doc or closure impact | See `change-impact.md`. | Accepted content must be promoted before closure. |
| Optional repo-evidence provider caveats | Agent Workbench can support routing but does not decide lifecycle authority. | None known. |

## Task Evidence

| Task ID | Status | Evidence | Notes |
|---------|--------|----------|-------|
| T001 | complete | D001 and D002 resolved in design/change-impact/traceability/canonical-context. | |
| T002 | complete | Durable lifecycle, operating-model, and Kiro compatibility docs updated. | |
| T003 | complete | Skill guidance updated and bundled copies synced. | |
| T004 | complete | Fallback `canonical-context.md` template and README guidance added. | |
| T005 | complete | Prompt definitions updated; prompt validation passed. | |
| T006 | complete | Runtime diagnostics/import-plan behavior and focused tests added; full suite passed. | |
| T007 | complete | Runtime reference, migration guidance, traceability, and verification updated. | |
| T008 | complete | `test_stage_readiness_returns_canonical_context_import_plan_for_stale_doc_risk` added; focused canonical tests passed, 4 tests. | |
| T009 | complete | Full checkpoint validation passed: 151 unittests, package lint, scan, prompts, archive-index, package-contract, promotion-plan, closure-check, task-state-audit, and `git diff --check`. | Closure log/archive index are not updated until final closure cleanup. |

## Evidence Log

| Date | Evidence | Result | Notes |
|------|----------|--------|-------|
| 2026-06-19 | Initial package authored from user-confirmed refinement. | superseded | Replaced by 2026-07-02 T001-T009 validation evidence: 151 tests passed, zero spec lint diagnostics, zero prompt diagnostics, archive-index clean, package-contract pass, promotion-plan complete, closure-check ready. |
| 2026-07-02 | D001 and D002 resolved in design, change-impact, traceability, and canonical-context artifacts. | passed | D001: optional separate `canonical-context.md` plus embedded-section allowance. D002: authoring/readiness warnings, closure blocker for unresolved required canonical promotion. |
| 2026-07-02 | Full validation for T001-T007 implementation slice. | passed | Full unittest suite: 150 tests passed; spec lint zero diagnostics; scan four active specs all pass; prompts zero diagnostics; package-contract pass; `git diff --check` pass. |
| 2026-07-02 | T008 deterministic dogfood fixture. | passed | `test_stage_readiness_returns_canonical_context_import_plan_for_stale_doc_risk` proves a new-style spec with stale durable-doc risk and no `canonical-context.md` receives `CANONICAL_CONTEXT_MISSING` plus an import plan targeting `canonical-context.md`. |
| 2026-07-02 | T009 checkpoint validation. | passed | Full unittest suite: 151 tests passed; spec lint zero diagnostics; scan four active specs all pass; prompts zero diagnostics; archive-index zero diagnostics; package-contract pass; promotion-plan has no missing targets; task-state-audit pass; closure-check ready; `git diff --check` pass. |

## Manual Or External Verification

No external verification was required. Manual verification for T009 reviewed
promotion-plan output and confirmed no missing promotion targets remain.

## Residual Risks

- Runtime diagnostics could become noisy if every small spec is required to add
  canonical context. Mitigation: scope initial diagnostics to broad durable
  impact, imported sources, or declared stale-doc risk.
- Spec-local context could be misunderstood as overriding governance.
  Mitigation: keep always-canonical external authority exceptions explicit in
  durable docs, templates, and skill guidance.
- Imported-source metadata could become too heavy. Mitigation: allow embedded
  sections for small specs and a separate artifact for higher-risk packages.
- Full interactive new-spec creation remains a manual workflow rather than an
  automated fixture. Mitigation: deterministic stage-readiness dogfood covers
  the import-plan behavior that creation/resume prompts expose to agents.

## Durable Promotion And Cleanup

| Spec content | Durable destination or deferral | Status | Evidence |
|--------------|---------------------------------|--------|----------|
| Spec-local canonical context model | `docs/design/spec-lifecycle-management.md` | promoted | 2026-07-02 implementation slice. |
| Agent operating rule | `docs/design/coding-agent-operating-model.md` | promoted | 2026-07-02 implementation slice. |
| Agent-facing workflow | `skills/spec-lifecycle-manager/SKILL.md` | promoted | 2026-07-02 implementation slice. |
| Template guidance | `skills/spec-lifecycle-manager/references/spec-package/` | promoted | 2026-07-02 implementation slice. |
| Spec creation and resume prompt guidance | `skills/spec-lifecycle-manager/prompts/` | promoted | 2026-07-02 implementation slice. |
| Runtime behavior | `docs/reference/spec-lifecycle-runtime.md` | promoted | 2026-07-02 implementation slice. |
| Migration guidance | `skills/spec-lifecycle-manager/references/migration-guide.md` | promoted | 2026-07-02 implementation slice. |
| Dogfood validation evidence | `docs/specs/027-spec-local-canonical-context/verification.md` | retained until closure | 2026-07-02 T008/T009 checkpoint. |

### Spec Cleanup Decision

- **Cleanup action:** keep active
- **Reason:** Implementation and checkpoint validation are complete, but final
  closure cleanup requires a final spec commit plus closure-log/archive-index
  updates.
- **Final spec commit:** pending
- **Closure log path:** `docs/history/spec-closure-log.md`
- **Closure log entry updated:** no
- **Closure cleanup commit:** pending
- **Active indexes updated:** no
- **Durable docs linked back to evidence where useful:** yes
- **Residual spec-only content:** listed in Durable Promotion And Cleanup

Residual spec-only content:

- No accepted current behavior remains spec-only. Dogfood evidence and closure
  breadcrumbs remain in this active package until closure.

## Ship Or Closure Risk

- **Risk level:** low
- **Breaking change:** no
- **Blast radius checked:** yes
- **Rollback path:** not required for docs-only package authoring; required
  implementation changes are reversible through Git.
- **Requires human review:** no
- **Release notes needed:** no
- **Follow-up issue or spec needed:** no

### Risk Rationale

The change affects how agents decide documentation authority during
implementation, but diagnostics are advisory and scoped to explicit durable-doc,
stale-doc, imported-source, or canonical-context signals. Validation shows the
existing active specs stay clean.

## Readiness Decision

- **Ready for promotion:** yes
- **Ready for release:** yes
- **Ready for closure:** yes, after final spec commit and closure-log/archive-index cleanup.

## Related Artifacts

- Requirements:
  `docs/specs/027-spec-local-canonical-context/requirements.md`
- Change Impact:
  `docs/specs/027-spec-local-canonical-context/change-impact.md`
- Design: `docs/specs/027-spec-local-canonical-context/design.md`
- Tasks: `docs/specs/027-spec-local-canonical-context/tasks.md`
