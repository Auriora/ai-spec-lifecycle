---
title: Spec lifecycle validation requirements
doc_type: requirements
status: draft
owner: platform
last_reviewed: 2026-06-02
---

# Requirements

## Introduction

Validate the `spec-lifecycle-manager` skill against realistic scenarios so the
local spec-driven environment can be trusted before wider installation.

## Goals

- Verify the skill package and docs are internally consistent.
- Validate behavior against fixture repositories that represent expected usage.
- Use sub-agents to run independent prompt trials and review passes.
- Record evidence, gaps, and follow-up decisions in a durable validation record.

## Non-Goals

- Installing the updated skill globally.
- Replacing target repositories' own documentation systems.
- Automating every validation check before the workflow shape has stabilized.

## Glossary

| Term | Definition |
|------|------------|
| Fixture repo | Small test repository under `tests/fixtures/skill-validation/` used to exercise one skill scenario. |
| Prompt trial | A sub-agent run that applies the skill to a fixture with a realistic user prompt. |
| Review pass | Independent assessment of the skill/templates from one review perspective. |

## Requirements

### Requirement 1: Static Consistency

**User Story:** As a maintainer, I want static checks over the skill package and
docs, so that broken references or duplicate templates are caught before agent
trials.

#### Acceptance Criteria

1. GIVEN the repository, WHEN static validation runs, THEN reusable project
   templates live under `skills/spec-lifecycle-manager/references/`, not
   repo-level `docs/templates/`.
2. GIVEN the skill references files, WHEN checked, THEN every referenced skill
   reference file exists.
3. GIVEN README and template links, WHEN checked, THEN links resolve or any
   exception is documented.
4. GIVEN spec-package templates, WHEN checked, THEN task templates preserve
   checklist tasks and subtasks while including evidence, acceptance, change
   impact, verification, and ship risk guidance.
5. GIVEN spec-package and durable-doc templates, WHEN checked, THEN temporary
   spec artifacts use `doc_type: spec` with `artifact_type`, while durable docs
   use durable document classes.

### Requirement 2: Fixture-Based Skill Trials

**User Story:** As a maintainer, I want fixture repositories for expected
scenarios, so that skill behavior can be tested without mutating real projects.

#### Acceptance Criteria

1. GIVEN fixture repos, WHEN reviewed, THEN they cover fresh feature, bug fix,
   old-format spec, external partition, completed spec, and governance conflict
   scenarios.
2. GIVEN each fixture, WHEN a prompt trial runs, THEN expected behavior and
   actual behavior are recorded.

### Requirement 3: Prompt Trial Evidence

**User Story:** As a maintainer, I want sub-agents to run realistic prompts, so
that the skill is validated independently of the main agent's expectations.

#### Acceptance Criteria

1. GIVEN a bug-fix prompt, THEN the result expects `change-impact.md` and a
   durable source reference.
2. GIVEN an old-format resume prompt, THEN the result uses a migration decision
   gate rather than forced migration.
3. GIVEN a completed-spec close prompt, THEN the result identifies promotion
   targets and closure blockers.
4. GIVEN an external-project prompt, THEN the result uses a docs partition such
   as `docs/agent-lifecycle/`.

### Requirement 4: Review Matrix

**User Story:** As a maintainer, I want independent review passes, so that the
skill is assessed from workflow, durable-doc, governance/evidence, and external
project cleanliness perspectives.

#### Acceptance Criteria

1. GIVEN the Kiro-style workflow review, THEN findings cover requirements,
   design, task DAG, status, and correctness properties.
2. GIVEN the durable-doc lifecycle review, THEN findings cover finite spec
   lifetime, durable source of truth, change impact, and promotion.
3. GIVEN the governance/evidence review, THEN findings cover constitution,
   migration decisions, task evidence, verification, and ship risk.
4. GIVEN the external-project cleanliness review, THEN findings cover
   docs-root partitioning and source-tree cleanliness.

### Requirement 5: Dogfood Validation

**User Story:** As a maintainer, I want this validation work to use the skill's
own package shape, so that friction in the workflow is exposed immediately.

#### Acceptance Criteria

1. GIVEN this validation package, WHEN complete, THEN it contains
   `requirements.md`, `design.md`, `tasks.md`, `verification.md`, and validation
   evidence.
2. GIVEN validation findings, WHEN follow-up is needed, THEN it is recorded in
   tasks, verification, or a follow-up spec.

## Correctness Properties

- **CP-001**: Validation evidence MUST map each fixture and review pass to an
  expected outcome and an observed outcome.
- **CP-002**: The updated skill MUST remain repo-local and MUST NOT require
  global installation for this validation.

## Technical Context

- **Language/Version:** Markdown documentation and Codex skills.
- **Primary Dependencies:** Repo-local `.codex/skills/spec-lifecycle-manager/`
  for this agent environment.
- **Target Platform:** Local repository and sub-agent validation runs.
- **Constraints:** Do not mutate global skill installation.
- **Performance Goals:** Validation should be lightweight and repeatable.

## Success Criteria

- **SC-001**: All validation-plan steps are represented by tasks and evidence.
- **SC-002**: All six fixture scenarios have expected and observed outcomes.
- **SC-003**: Review matrix findings are recorded with severity and follow-up.
- **SC-004**: Any uncovered risk is explicitly documented.

## Related Artifacts

- Change Impact:
- Design: design.md
- Tasks: tasks.md
- Verification: verification.md
