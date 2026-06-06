---
title: Codex hook dogfood verification
doc_type: spec
artifact_type: verification
status: draft
owner: platform
last_reviewed: 2026-06-06
---

# Verification

## Scope

This verification record covers dogfooding the advisory Codex spec lifecycle
hook after installation into global Codex `PostToolUse` hooks.

## Quality Gates

| Gate | Required? | Status | Evidence |
|------|-----------|--------|----------|
| Requirements acceptance criteria reviewed | yes | pass | Requirements 1-3 mapped to dogfood evidence and policy decision. |
| Task evidence complete | yes | pass | T001-T004 complete with evidence. |
| Automated tests pass or alternate verification recorded | yes | pass | Focused and full tests passed. |
| Durable documentation updates identified | yes | pass | Runtime and install docs already document advisory hook behavior. |
| Durable documentation promoted or explicitly deferred | yes | pass | No durable doc change needed beyond existing hook guidance. |
| Governance or policy conflicts resolved | yes | pass | Hook remains advisory and exits zero. |

## Validation Commands

| Command | Purpose | Result | Evidence |
|---------|---------|--------|----------|
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_codex_spec_lifecycle_hook` | Focused hook tests | pass | 2 tests passed after retargeting the advisory finding fixture to spec 003. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'` | Full regression tests | pass | 41 tests passed. |
| `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py lint docs/specs/010-codex-hook-dogfood` | Spec package lint | pass | No diagnostics. |
| `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py closure-check docs/specs/010-codex-hook-dogfood` | Closure readiness | pass | Ready with no blockers after dogfood evidence was recorded. |
| `git diff --check` | Diff whitespace hygiene | pass | No whitespace errors reported. |

## Evidence Log

| Date | Event | Outcome | Notes |
|------|-------|---------|-------|
| 2026-06-06 | Spec package creation | quiet-pass | Spec 010 created to track dogfood. |
| 2026-06-06 | Synthetic clean spec edit payload for `docs/specs/010-codex-hook-dogfood/tasks.md` | quiet-pass | Hook exited zero with no stdout/stderr. |
| 2026-06-06 | Synthetic active spec edit payload for `docs/specs/003-coding-agent-operating-model/tasks.md` | useful-finding | Hook exited zero and emitted concise advisory context for known lint findings. |
| 2026-06-06 | Synthetic non-target edit payload for `README.md` | quiet-pass | Hook exited zero and stayed quiet because no spec lifecycle target was changed. |
| 2026-06-06 | Focused and full hook tests | pass | Tests cover quiet pass and useful advisory finding paths. |

## Policy Decision

| Decision | Status | Rationale | Follow-up |
|----------|--------|-----------|-----------|
| Keep advisory hook globally enabled | accepted | The hook stayed quiet on pass/no-target payloads, produced concise useful context for a known spec finding, and exited zero in all paths. | No blocking promotion. Revisit only if repeated noise appears or a later focused spec defines blocking policy. |

## Requirement Coverage

| Requirement | Acceptance criteria covered | Evidence | Residual risk |
|-------------|-----------------------------|----------|---------------|
| Requirement 1 | AC1, AC2, AC3 | Evidence log covers quiet, useful finding, and no-target behavior. | More evidence may arrive from future real edits. |
| Requirement 2 | AC1, AC2, AC3 | Policy decision keeps advisory hook enabled and defers blocking promotion. | Blocking behavior still requires a later focused spec. |
| Requirement 3 | AC1, AC2, AC3 | Focused tests and synthetic payloads cover clean edits and known invalid spec edits; template routing is covered by wrapper tests and runtime lint. | Real template edit evidence remains opportunistic. |

## Residual Risks

- The hook is installed globally outside repository source control.
- Real-world template edit evidence remains limited; synthetic and unit-test
  coverage is sufficient for advisory dogfood but not for blocking promotion.

## Task Evidence

| Task ID | Status | Evidence | Notes |
|---------|--------|----------|-------|
| T001 | complete | Spec package created. | Includes requirements, design, tasks, traceability, and verification. |
| T002 | complete | Representative payloads recorded. | Quiet pass, useful finding, and no-target behavior covered. |
| T003 | complete | Keep advisory hook globally enabled. | Blocking promotion explicitly deferred. |
| T004 | complete | Focused tests, full tests, lint, closure-check, and diff check passed. | Ready for closure. |

## Durable Promotion And Cleanup

| Spec content | Durable destination or deferral | Status | Evidence |
|--------------|---------------------------------|--------|----------|
| Dogfood decision | Existing runtime and install reference docs | complete | Current docs already describe advisory hook behavior and no blocking promotion. |
| Follow-up work | Backlog, roadmap, or follow-up spec | deferred | No immediate follow-up needed; create one only if repeated hook noise or blocking promotion is proposed. |

### Spec Cleanup Decision

- **Cleanup action:** retain as history note
- **Reason:** The package records Codex hook dogfood evidence and policy
  decision.
- **Final spec commit:** pending
- **Closure log path:** `docs/history/spec-closure-log.md`
- **Closure log entry updated:** pending
- **Closure cleanup commit:** pending
- **Active indexes updated:** yes
- **Durable docs linked back to evidence where useful:** yes
- **Residual spec-only content:** Dogfood evidence remains in spec 010 as
  retained history after closure.

## Ship Or Closure Risk

- **Risk level:** low
- **Breaking change:** no
- **Blast radius checked:** yes
- **Rollback path:** remove the hook entry from `~/.codex/hooks.json`
- **Requires human review:** optional
- **Release notes needed:** no
- **Follow-up issue or spec needed:** no

## Readiness Decision

- **Ready for promotion:** yes
- **Ready for release:** yes
- **Ready for closure:** yes after final validation commands pass.
