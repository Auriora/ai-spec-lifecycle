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
| Requirements acceptance criteria reviewed | yes | pending | Pending dogfood decision. |
| Task evidence complete | yes | pending | T001 complete; T002-T004 pending. |
| Automated tests pass or alternate verification recorded | yes | pending | Pending final dogfood validation. |
| Durable documentation updates identified | yes | pending | Pending decision. |
| Durable documentation promoted or explicitly deferred | yes | pending | Pending decision. |
| Governance or policy conflicts resolved | yes | pass | Hook remains advisory and exits zero. |

## Validation Commands

| Command | Purpose | Result | Evidence |
|---------|---------|--------|----------|
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.runtime.test_codex_spec_lifecycle_hook` | Focused hook tests | pending | Pending dogfood run. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'` | Full regression tests | pending | Pending dogfood run. |
| `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py lint docs/specs/010-codex-hook-dogfood` | Spec package lint | pending | Pending dogfood run. |
| `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py closure-check docs/specs/010-codex-hook-dogfood` | Closure readiness | pending | Pending dogfood run. |
| `git diff --check` | Diff whitespace hygiene | pending | Pending dogfood run. |

## Evidence Log

| Date | Event | Outcome | Notes |
|------|-------|---------|-------|
| 2026-06-06 | Spec package creation | quiet-pass | Spec 010 created to track dogfood. |

## Policy Decision

| Decision | Status | Rationale | Follow-up |
|----------|--------|-----------|-----------|
| Keep advisory hook globally enabled | pending | Dogfood evidence pending. | Pending. |

## Requirement Coverage

| Requirement | Acceptance criteria covered | Evidence | Residual risk |
|-------------|-----------------------------|----------|---------------|
| Requirement 1 | pending | Evidence log pending | Hook may be noisy until evaluated. |
| Requirement 2 | pending | Policy decision pending | Blocking promotion remains out of scope. |
| Requirement 3 | pending | Validation commands pending | Template edit evidence pending. |

## Residual Risks

- The hook is installed globally outside repository source control.
- This dogfood spec depends on observing representative Codex hook behavior.

## Task Evidence

| Task ID | Status | Evidence | Notes |
|---------|--------|----------|-------|
| T001 | complete | Spec package created. | Includes requirements, design, tasks, traceability, and verification. |
| T002 | pending | Pending. | Needs representative hook events. |
| T003 | pending | Pending. | Needs policy decision. |
| T004 | pending | Pending. | Needs validation evidence. |

## Durable Promotion And Cleanup

| Spec content | Durable destination or deferral | Status | Evidence |
|--------------|---------------------------------|--------|----------|
| Dogfood decision | Runtime or install reference docs, if needed | pending | Pending policy decision. |
| Follow-up work | Backlog, roadmap, or follow-up spec | pending | Pending dogfood result. |

