---
title: Brooks-Lint findings tracking requirements
doc_type: spec
artifact_type: requirements
status: draft
owner: platform
last_reviewed: 2026-06-06
---

# Requirements

## Durable Source Baseline

- `docs/reviews/brooks-lint/README.md` is the intended durable destination
  for persisted audit findings.
- `.brooks-lint-history.json` records score history when Brooks skills run.
- The 2026-06-06 Brooks-Audit, Brooks-Debt, Brooks-Health, and Brooks-Test
  runs are seed inputs for this spec.
- Active implementation context is this spec package.
- Existing backlog and roadmap documents remain the durable planning surfaces
  for deferred remediation work.

## Goals

- Preserve Brooks-Lint findings from every skill run in a stable location.
- Track each finding from observed symptom through triage, owner decision,
  implementation task, verification evidence, and closure.
- Keep architecture, review, test-quality, and future Brooks skill outputs
  comparable without forcing every finding into immediate implementation.
- Avoid making transient chat output the only record of architectural debt.

## Non-Goals

- Do not implement all Brooks-Audit remediation in this spec.
- Do not replace `.brooks-lint-history.json` score history.
- Do not add third-party dependencies.
- Do not create a heavyweight issue tracker inside the repository.
- Do not change Brooks skill behavior outside this repository.

## Requirements

### Requirement 1: Durable Findings Register

**User Story:** As a maintainer, I want Brooks-Lint findings recorded in a
durable register, so that repeated skill runs create usable project memory.

#### Acceptance Criteria

1. GIVEN a Brooks skill produces findings, WHEN the findings are accepted for
   tracking, THEN THE SYSTEM SHALL record each finding with a stable ID.
2. GIVEN a finding is recorded, THEN THE SYSTEM SHALL preserve mode, scope,
   severity, symptom, source, consequence, and remedy fields.
3. GIVEN a finding came from a specific file or module, THEN THE SYSTEM SHALL
   include a repository-relative reference where possible.

### Requirement 2: Triage State

**User Story:** As a maintainer, I want every Brooks finding to have a clear
state, so that audits do not become unowned lists.

#### Acceptance Criteria

1. GIVEN a finding is added, THEN THE SYSTEM SHALL classify it as `accepted`,
   `deferred`, `dismissed`, or `needs-decision`.
2. GIVEN a finding is deferred or dismissed, THEN THE SYSTEM SHALL record a
   reason.
3. GIVEN a finding is accepted, THEN THE SYSTEM SHALL link it to a task,
   backlog item, roadmap item, or explicit implementation plan.

### Requirement 3: Cross-Skill Comparability

**User Story:** As a maintainer, I want findings from different Brooks skills
to share a schema, so that architecture, review, and test-quality results can
be compared.

#### Acceptance Criteria

1. GIVEN findings come from different Brooks modes, THEN THE SYSTEM SHALL
   preserve mode names without changing their meaning.
2. GIVEN a finding references a Brooks risk code, THEN THE SYSTEM SHALL retain
   that risk code or book/principle attribution.
3. GIVEN a repeated finding appears in later runs, THEN THE SYSTEM SHALL allow
   it to update existing evidence instead of creating duplicate debt.

### Requirement 4: Score History Integration

**User Story:** As a maintainer, I want score history and finding details to
support each other, so that trend changes can be explained.

#### Acceptance Criteria

1. GIVEN `.brooks-lint-history.json` exists, THEN THE SYSTEM SHALL document how
   finding records relate to history entries.
2. GIVEN a score changes between Brooks runs, THEN THE SYSTEM SHALL make it
   possible to identify which finding changes explain the movement.
3. GIVEN score history is unavailable, THEN THE SYSTEM SHALL still allow
   durable finding records to be maintained.

### Requirement 5: Closure Evidence

**User Story:** As a maintainer, I want fixed Brooks findings to include
verification evidence, so that closure is more than marking a checkbox.

#### Acceptance Criteria

1. GIVEN a finding is marked resolved, THEN THE SYSTEM SHALL include the commit,
   changed files, and validation commands where available.
2. GIVEN a finding is dismissed, THEN THE SYSTEM SHALL include a rationale and
   reviewer or maintainer decision.
3. GIVEN a finding remains open at spec closure, THEN THE SYSTEM SHALL promote
   it to backlog, roadmap, or a durable review register.

## Correctness Properties

- **CP-001**: Every tracked finding has one stable ID and one current state.
- **CP-002**: A resolved finding must have verification evidence or an explicit
  waiver rationale.
- **CP-003**: The tracking format must support findings from more than one
  Brooks skill.
- **CP-004**: No finding may be silently dropped during promotion or closure.

## Technical Context

- **Language/Version:** Markdown plus Python 3.9+ standard library if runtime
  validation is added.
- **Primary Dependencies:** Existing docs, backlog, roadmap, Brooks history
  file, spec lifecycle runtime.
- **Target Platform:** Repository-local Codex lifecycle workflow.
- **Constraints:** Keep records durable, reviewable, and merge-friendly.
- **Performance Goals:** Any validation should be fast enough to run with the
  existing lifecycle checks.

## Success Criteria

- **SC-001**: A durable Brooks findings register exists with seed findings from
  the initial architecture audit.
- **SC-002**: Each finding has a stable ID, state, severity, source, consequence,
  and remedy.
- **SC-003**: Future Brooks skill runs have clear instructions for appending or
  reconciling findings.
- **SC-004**: Lifecycle scan, lint, archive index, prompt validation, unit tests,
  and whitespace checks pass.

## Related Artifacts

- Change Impact: [change-impact.md](change-impact.md)
- Research: [research.md](research.md)
- Design: [design.md](design.md)
- Tasks: [tasks.md](tasks.md)
- Traceability: [traceability.md](traceability.md)
- Verification: [verification.md](verification.md)
- Open Decisions: [open-decisions.md](open-decisions.md)
