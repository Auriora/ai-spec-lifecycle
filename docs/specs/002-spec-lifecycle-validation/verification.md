---
title: Spec lifecycle validation verification
doc_type: verification
status: draft
owner: platform
last_reviewed: 2026-06-02
---

# Verification

## Scope

This record covers validation of the repo-local `spec-lifecycle-manager` skill
against static consistency checks, fixture-based prompt trials, review matrix
passes, and dogfood usage.

## Quality Gates

| Gate | Required? | Status | Evidence |
|------|-----------|--------|----------|
| Static consistency checks complete | yes | done | Static commands passed; see `validation-evidence.md`. |
| Six fixtures created | yes | done | `tests/fixtures/skill-validation/` contains six scenario fixtures. |
| Prompt trials complete | yes | done | Linnaeus and Mendel sub-agents reported pass results. |
| Review matrix complete | yes | done | Aristotle and Descartes sub-agents reported review results; fixes applied. |
| Dogfood assessment complete | yes | done | Dogfood assessment recorded in `validation-evidence.md`. |

## Validation Commands

| Command | Purpose | Result | Evidence |
|---------|---------|--------|----------|
| `find docs/templates/spec-package -maxdepth 1 -type f -print` | Confirm duplicate docs templates are absent | pass | Directory is absent. |
| `diff -qr skills/spec-lifecycle-manager .codex/skills/spec-lifecycle-manager` | Confirm repo-local installed skill matches source | pass | No differences returned. |
| Markdown link resolver | Confirm Markdown links resolve | pass | Returned `markdown-links-ok`. |
| `rg` static field checks | Confirm required fields and artifacts exist | pass | Found status, evidence, change-impact, verification, ship risk, durable baseline, and open decisions. |

## Requirement Coverage

| Requirement | Acceptance criteria covered | Evidence | Residual risk |
|-------------|-----------------------------|----------|---------------|
| Requirement 1 | Static consistency | Pass evidence in `validation-evidence.md` | Static checks are ad hoc shell commands, not scripted. |
| Requirement 2 | Fixture coverage | Six fixture directories created | Fixtures are minimal, not runnable apps. |
| Requirement 3 | Prompt trials | Six sub-agent prompt trials passed | Trials were mental/read-only. |
| Requirement 4 | Review matrix | Four review perspectives completed | One perspective initially failed, then fixes were applied. |
| Requirement 5 | Dogfood validation | Dogfood assessment recorded | Artifact overhead remains a process risk. |

## Task Evidence

| Task ID | Status | Evidence | Notes |
|---------|--------|----------|-------|
| T001 | done | Created validation spec package | |
| T002 | done | Created six fixtures | |
| T003 | done | Static commands passed | |
| T004 | done | Linnaeus and Mendel prompt trials passed | |
| T005 | done | Aristotle and Descartes reviews completed; findings fixed | |
| T006 | done | Evidence recorded | |
| T007 | done | Dogfood assessment recorded | |
| T008 | done | Task and verification statuses updated | |

## Manual Or External Verification

Sub-agent prompt trials and review passes are manual/agentic validation. Record
agent id, model, prompt scope, result, and residual risk in
`validation-evidence.md`.

## Residual Risks

- Prompt trials were read-only mental applications of the skill, not scripted
  fixture mutations.
- Static checks are documented commands but not yet packaged into a reusable
  test script.
- Optional artifact count may be too heavy for small work; the skill already
  permits omitting optional artifacts when they do not add value.

## Ship Or Closure Risk

- **Risk level:** low
- **Breaking change:** no
- **Blast radius checked:** yes
- **Rollback path:** not required
- **Requires human review:** yes
- **Release notes needed:** no
- **Follow-up issue or spec needed:** no

### Risk Rationale

The validation workflow changes agent process behavior rather than runtime code.
Prompt trials and review passes found no blocking defects after fixes. The main
remaining risk is workflow drift or over-heavy optional templates.

## Readiness Decision

- **Ready for promotion:** yes
- **Ready for release:** yes
- **Ready for closure:** yes

## Related Artifacts

- Requirements: requirements.md
- Change Impact:
- Design: design.md
- Tasks: tasks.md
