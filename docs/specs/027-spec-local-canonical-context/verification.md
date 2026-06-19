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
| Requirements acceptance criteria reviewed | yes | pending | Review after package lint. |
| Task evidence complete | yes | pending | Tasks are not implemented yet. |
| Automated tests pass or alternate verification recorded | yes | pending | Required after runtime/template changes. |
| Durable documentation updates identified | yes | pending | See `change-impact.md`. |
| Durable documentation promoted or explicitly deferred | yes | pending | Required before closure. |
| Spec cleanup decision recorded | yes | pending | Required before closure. |
| Governance or policy conflicts resolved | yes | pending | No conflict known; verify during implementation. |

## Validation Commands

| Command | Purpose | Result | Evidence |
|---------|---------|--------|----------|
| `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py lint docs/specs/027-spec-local-canonical-context` | Validate this spec package structure. | pending | |
| `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py scan .` | Validate active spec inventory and health. | pending | |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'` | Validate runtime behavior after implementation. | pending | |
| `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py prompts .` | Validate prompt definitions if prompts change. | pending | Not required unless prompts are modified. |
| `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py archive-index .` | Validate closure/archive metadata before closure. | pending | Required at closure. |
| `git diff --check` | Catch whitespace issues. | pending | |

## Requirement Coverage

| Requirement | Acceptance criteria covered | Evidence | Residual risk |
|-------------|-----------------------------|----------|---------------|
| Requirement 1 | AC1-AC4 | Pending T002-T005 implementation and validation. | Diagnostics must avoid false positives for small specs. |
| Requirement 2 | AC1-AC4 | Pending durable docs and skill guidance review. | Runtime cannot prove every governance conflict. |
| Requirement 3 | AC1-AC4 | Pending template and runtime fixture. | Source revision/date may be unavailable in some repos. |
| Requirement 4 | AC1-AC4 | Pending readiness/task-context integration. | MCP output shape may need compatibility care. |
| Requirement 5 | AC1-AC4 | Pending closure-check or promotion-plan validation. | Initial severity policy needs D002. |
| Requirement 6 | AC1-AC4 | Pending template/runtime tests. | Existing specs should not be forced to migrate. |

## Correctness Property Coverage

| Property | Covered by | Evidence | Residual risk |
|----------|------------|----------|---------------|
| CP-001 | T002, T003, T005 docs/runtime review | Pending. | Needs explicit wording in durable docs and skill guidance. |
| CP-002 | T004, T005 template/runtime checks | Pending. | Table parsing may be incremental. |
| CP-003 | T005, T006, T007 closure guidance | Pending. | Severity depends on D002. |
| CP-004 | T003, T005 readiness/task-context output | Pending. | Requires careful context-budget guidance. |

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
| T001 | pending | | |
| T002 | pending | | |
| T003 | pending | | |
| T004 | pending | | |
| T005 | pending | | |
| T006 | pending | | |
| T007 | pending | | |

## Evidence Log

| Date | Evidence | Result | Notes |
|------|----------|--------|-------|
| 2026-06-19 | Initial package authored from user-confirmed refinement. | pending validation | |

## Manual Or External Verification

No manual or external verification has been completed yet.

## Residual Risks

- Runtime diagnostics could become noisy if every small spec is required to add
  canonical context. Mitigation: scope initial diagnostics to broad durable
  impact, imported sources, or declared stale-doc risk.
- Spec-local context could be misunderstood as overriding governance.
  Mitigation: keep always-canonical external authority exceptions explicit in
  durable docs, templates, and skill guidance.
- Imported-source metadata could become too heavy. Mitigation: allow embedded
  sections for small specs and a separate artifact for higher-risk packages.

## Durable Promotion And Cleanup

| Spec content | Durable destination or deferral | Status | Evidence |
|--------------|---------------------------------|--------|----------|
| Spec-local canonical context model | `docs/design/spec-lifecycle-management.md` | pending | |
| Agent operating rule | `docs/design/coding-agent-operating-model.md` | pending | |
| Agent-facing workflow | `skills/spec-lifecycle-manager/SKILL.md` | pending | |
| Template guidance | `skills/spec-lifecycle-manager/references/spec-package/` | pending | |
| Runtime behavior | `docs/reference/spec-lifecycle-runtime.md` | pending | Required if runtime diagnostics are implemented. |
| Migration guidance | `skills/spec-lifecycle-manager/references/migration-guide.md` | pending | Required if artifact rules change. |

### Spec Cleanup Decision

- **Cleanup action:** keep active
- **Reason:** Implementation has not started.
- **Final spec commit:** pending
- **Closure log path:** `docs/history/spec-closure-log.md`
- **Closure log entry updated:** no
- **Closure cleanup commit:** pending
- **Active indexes updated:** no
- **Durable docs linked back to evidence where useful:** no
- **Residual spec-only content:** listed in Durable Promotion And Cleanup

Residual spec-only content:

- All accepted behavior remains spec-only until implementation and promotion.

## Ship Or Closure Risk

- **Risk level:** medium
- **Breaking change:** no
- **Blast radius checked:** no
- **Rollback path:** not required for docs-only package authoring; required
  implementation changes are reversible through Git.
- **Requires human review:** yes
- **Release notes needed:** no
- **Follow-up issue or spec needed:** no

### Risk Rationale

The change affects how agents decide documentation authority during
implementation. That is a workflow-quality improvement, but it can cause either
under-guidance or excessive ceremony if diagnostics are poorly scoped.

## Readiness Decision

- **Ready for promotion:** no
- **Ready for release:** no
- **Ready for closure:** no

## Related Artifacts

- Requirements:
  `docs/specs/027-spec-local-canonical-context/requirements.md`
- Change Impact:
  `docs/specs/027-spec-local-canonical-context/change-impact.md`
- Design: `docs/specs/027-spec-local-canonical-context/design.md`
- Tasks: `docs/specs/027-spec-local-canonical-context/tasks.md`
