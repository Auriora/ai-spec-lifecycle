---
title: Spec lifecycle manager skill tasks
doc_type: spec
status: archived
owner: platform
last_reviewed: 2026-06-01
---

# Tasks

**Input**: Design documents from `docs/specs/001-spec-lifecycle-manager-skill/`.

**Prerequisites**: `spec.md`, `design.md`, `plan.md`, [spec lifecycle management](../../design/spec-lifecycle-management.md), and [document routing and expert review matrix](../../reference/document-routing-and-expert-review-matrix.md).

**Tests**: Validation may include manual review and realistic prompt/fixture checks because this is a process skill rather than runtime code.

## Phase 1: Documentation Baseline

**Purpose**: Capture the intended lifecycle and review guidance in durable docs.

- [x] T001 Create `docs/README.md` with entry points and active spec convention.
- [x] T002 Create `docs/design/spec-lifecycle-management.md`.
- [x] T003 Create `docs/reference/document-routing-and-expert-review-matrix.md`.
- [x] T004 Create initial spec package under `docs/specs/001-spec-lifecycle-manager-skill/`.

**Checkpoint**: The skill implementation has documented requirements and review guidance.

## Phase 2: Skill Packaging Decision

**Purpose**: Decide where the skill should live and how it should be installed.

- [x] T005 Decide whether the skill is a personal Codex skill, repository-managed skill, plugin skill, or staged in repo before install. Decision: keep the canonical skill source under `skills/spec-lifecycle-manager/` in this repository and install a working copy under `$CODEX_HOME/skills/spec-lifecycle-manager/`, falling back to `~/.codex/skills/spec-lifecycle-manager/` when `$CODEX_HOME` is unset.
- [x] T006 Identify required skill files and optional references. Decision: create `SKILL.md` and `references/document-routing-and-expert-review.md`. Validation target details remain only in this archived implementation spec, not in the reusable skill package.
- [x] T007 Confirm whether `agents/openai.yaml` metadata is required for this skill. Decision: include `agents/openai.yaml` as recommended UI metadata; it is not required for runtime behavior.

**Checkpoint**: The target skill structure is known.

## Phase 3: Skill Draft

**Purpose**: Implement the first usable skill.

- [x] T008 Create `SKILL.md` with metadata and trigger description.
- [x] T009 Add the five-phase lifecycle workflow.
- [x] T010 Add reconciliation rules and drift classifications.
- [x] T011 Add task completion and alternate verification guidance.
- [x] T012 Add promotion and closure rules.
- [x] T013 Add expert review routing guidance or link to a supporting reference.
- [x] T013A Add review-evidence guidance so the skill records document/package reviewed, expert role, date, findings or sign-off, follow-up, and whether follow-up blocks implementation, release, or closure.

**Checkpoint**: The skill can guide a real spec lifecycle task.

## Phase 4: Validation

**Purpose**: Test whether the skill gives useful, concise, and correct guidance.

- [x] T014 Validate the skill against a mature documentation repository. Evidence: read-only sub-agent validation recorded in [validation-evidence.md](validation-evidence.md).
- [x] T015 Validate the skill against a smaller agent-runtime repository. Evidence: read-only sub-agent validation recorded in [validation-evidence.md](validation-evidence.md).
- [x] T016 Verify it handles a fresh small spec without unnecessary ceremony. Evidence: pass with notes in [validation-evidence.md](validation-evidence.md).
- [x] T017 Verify it handles a partially completed stale spec with reconciliation. Evidence: pass in [validation-evidence.md](validation-evidence.md).
- [x] T017A Verify it routes durable docs and expert review roles correctly. Evidence: pass in [validation-evidence.md](validation-evidence.md).

**Checkpoint**: The skill behavior is validated enough for local use.

## Phase 5: Install And Close

**Purpose**: Make the skill available and close the implementation spec.

- [x] T018 Install or publish the skill to the chosen location. Canonical source is tracked at `skills/spec-lifecycle-manager/`; installed working copy is at `~/.codex/skills/spec-lifecycle-manager/`.
- [x] T019 Update docs with the final usage location and invocation guidance.
- [x] T020 Run final documentation review for links, status, and closure criteria. Review result: links, installed files, and Phase 4 validation evidence are present; non-blocking wording improvements are recorded as follow-up in [validation-evidence.md](validation-evidence.md).
- [x] T021 Close, archive, or keep this spec active according to the documented lifecycle. Decision: keep this package as archived validation and decision history; durable current-state guidance lives in `docs/design/`, `docs/reference/`, `docs/README.md`, and the tracked skill source at `skills/spec-lifecycle-manager/`.

## Dependencies And Execution Order

- Phase 1 must complete before drafting the skill.
- Phase 2 must complete before installation.
- Phase 3 can begin once the packaging decision identifies a working location.
- Phase 4 must complete before marking the skill ready for routine use.
- Phase 5 closes the spec only after durable docs describe the implemented behavior.
