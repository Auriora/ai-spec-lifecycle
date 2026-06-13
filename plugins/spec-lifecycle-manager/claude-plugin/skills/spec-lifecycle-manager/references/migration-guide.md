# Spec Package Migration Guide

Use this guide to decide whether and how to migrate spec packages from older
formats (`spec.md`, `plan.md`, or weak checkbox-only tasks) to the current
hybrid Kiro-style format (`requirements.md`, enriched `design.md`, and
checklist tasks with subtasks, dependency notes, acceptance criteria, and
evidence).

Keep this guide current with released lifecycle improvements. When the skill
adds task-state markers, validation semantics, closure checks, artifact rules,
or durable-document integration requirements, update this guide in the same
release slice so old packages can be migrated consistently.

## Migration Decision Gate

When an active package uses the old format, choose one path before
implementation:

1. **Continue old format for this slice**: use when the change is small,
   migration would disrupt active collaboration, or the package is near closure.
2. **Migrate before implementation**: use when the package will remain active,
   the old format is already causing drift, or task status is too ambiguous to
   proceed safely.
3. **Create a follow-up migration task**: use when implementation can proceed
   safely now, but the package should be modernized before the next substantial
   slice.

Do not migrate without making the decision explicit in the reconciliation
summary.

Use this visible note format:

```markdown
Migration Decision:
- Package format: continue old format for this slice | migrate before implementation | create follow-up migration task
- Template authority: repository templates | repository templates with package-local additions | proposed selective template update | skill fallback templates
- Reason: ...
- Impact: existing docs touched? yes/no; templates touched? yes/no; durable docs affected? yes/no
- Follow-up: ...
```

Also classify any old `spec.md` file before relying on it:

```markdown
spec.md Classification:
- Role: feature brief | migration input | deprecated duplicate
- Duplicates current artifacts? yes/no
- Carries unpromoted decisions or acceptance criteria? yes/no
- Action: retain as brief | migrate content | remove after migration | leave historical
```

When a repository has its own `docs/templates/` or documented template system,
the template authority decision is required even if package migration is not
performed. Repository templates remain authoritative unless the user explicitly
asks to revise them.

## Template Authority And Selective Template Migration

Template migration is different from package migration:

- **Package migration** reshapes one active spec package.
- **Template migration** changes the future document shape for a repository and
  may affect many existing or future documents.

When repository templates exist, do not replace them wholesale with this
skill's fallback templates. Grade them first:

| Grade | Meaning | Action |
|-------|---------|--------|
| Adopt as-is | Repo templates cover the needed workflow and metadata | Use them without changes |
| Add package-local fields | Current package needs extra evidence, impact, verification, or risk fields, but repo-wide templates do not need to change yet | Add fields only to the active package |
| Selective template update | Multiple packages would benefit from a missing field or section | Propose the smallest template change and identify affected document classes |
| Defer template update | Existing docs would be disrupted or the value is unclear | Continue with current templates and record follow-up |
| Use skill fallback | No repo templates or governance are available | Use `references/spec-package/` |

Before changing repository templates, record:

- the exact templates affected;
- the missing fields or sections;
- which existing docs would become non-conforming or require migration;
- whether old packages should be grandfathered;
- whether the change affects durable docs, active specs, or both;
- review or approval needed before applying the new template.

Prefer package-local additions when only one spec needs stronger tracking.
Prefer template updates only when the repository's documented workflow should
change for future packages.

## When Migration Is Usually Worth It

Migration is usually worth it when:

- An active or in-progress spec is resumed and uses the old format.
- A spec is reopened for further implementation work.
- Reconciliation detects `spec.md` or `plan.md` files instead of
  `requirements.md`.
- Task checkboxes are stale or do not carry evidence.
- The package needs stronger dependency ordering or verification evidence.

Do not migrate automatically:

- Archived specs that will not be resumed (leave as historical records).
- Specs where migration would disrupt active collaboration mid-task.
- Small, low-risk fixes where migration would create more churn than clarity.

## Detection

Old format indicators:

- `spec.md` exists (instead of `requirements.md`)
- `plan.md` exists (content now split across requirements/design/tasks)
- `tasks.md` uses ambiguous `- [ ]` / `- [x]` checkboxes without dependency,
  acceptance, evidence, or verification guidance
- `tasks.md` lacks dependency notes or a Task Dependency Graph for non-trivial
  work
- `design.md` lacks High-Level Design / Low-Level Design sections

Duplication indicators:

- `spec.md` restates requirements already present in `requirements.md`
- `spec.md` contains durable-source baselines now present in
  `requirements.md` or `change-impact.md`
- `plan.md` repeats task phases that now live in `tasks.md`
- Future/intended behavior appears in durable docs without proposed/deferred
  labeling
- Durable-doc impact is split across artifacts without a single clear source

## Field Mapping: spec.md → requirements.md

| Old location (spec.md) | New location (requirements.md) |
|------------------------|-------------------------------|
| Summary | Introduction |
| Problem | Introduction (merge with summary) |
| Goals | Goals |
| Non-Goals | Non-Goals |
| Requirements → Functional Requirements | Requirements → individual requirement sections with user stories |
| Requirements → Key Entities | Glossary |
| Acceptance Criteria | Distributed as acceptance criteria on relevant requirements |
| User Scenarios → User Story N | Requirements → Requirement N (rewrite as user story) |
| Edge Cases | Acceptance criteria on relevant requirements |
| Success Criteria | Success Criteria |
| Validation Targets | Move to verification.md or design.md operational considerations |
| Related Artifacts | Related Artifacts |

If `spec.md` is only a concise feature brief, do not expand it into duplicate
requirements. Either retain it as an explicit brief with links to current
artifacts, or replace it with a package README/index if the repository wants a
read-order surface.

### Conversion Rules

1. **FR-001 bullets → User story requirements**

   Old:
   ```markdown
   - **FR-001**: System MUST identify active spec packages using `[docs-root]/specs/[###-slug]/`.
   ```

   New:
   ```markdown
   ### Requirement 1: Active Spec Package Detection

   **User Story:** As an agent, I want to automatically identify active spec
   packages, so that I can resume work without manual navigation.

   #### Acceptance Criteria

   1. GIVEN a repository with `[docs-root]/specs/[###-slug]/` directories, WHEN the
      skill is invoked, THEN it identifies all active spec packages.
   2. WHERE a spec package has status `active` or `draft` in frontmatter, THE
      system SHALL treat it as an active package.
   ```

2. **User Scenarios → Requirements with acceptance criteria**

   Old:
   ```markdown
   ### User Story 1 - Continue An Active Spec (Priority: P1)
   An agent needs to continue implementation from an existing spec package...
   **Acceptance Scenarios**:
   1. **Given** state, **When** action, **Then** outcome.
   ```

   New:
   ```markdown
   ### Requirement 1: Continue Active Spec

   **User Story:** As an agent, I want to continue implementation from an
   existing spec package, so that I do not lose track of code/doc drift.

   #### Acceptance Criteria

   1. GIVEN an existing partially completed spec, WHEN implementation resumes,
      THEN a reconciliation summary is produced before selecting work.
   ```

3. **Edge Cases → Acceptance criteria**

   Distribute edge cases as additional acceptance criteria on the most relevant
   requirement. Use IF/THEN format:

   ```markdown
   3. IF no `docs/` folder exists yet, THEN THE SYSTEM SHALL create the
      minimum required directory structure.
   ```

## Field Mapping: plan.md → requirements.md + design.md + tasks.md

| Old location (plan.md) | New location |
|------------------------|-------------|
| Technical Context | requirements.md → Technical Context |
| Governance Check | design.md (incorporate into design decisions) |
| Project Structure | tasks.md (file paths in task entries) |
| Phases | tasks.md (phase grouping) |
| Dependencies | tasks.md → Task Dependency Graph |
| Risks | design.md → Open Questions or Operational Considerations |
| Validation Strategy | verification.md, plus requirements.md → Success Criteria when it describes desired outcomes |
| Complexity Tracking | Remove (governance is a design concern now) |

## Task Migration: Weak Checklists -> Enhanced Kiro-Style Tasks

### Old format

```markdown
## Phase 1: Setup
- [ ] T001 Create documentation structure
- [ ] T002 Identify source files
- [x] T003 [P] Configure helpers
```

### New format

```markdown
## Task Dependency Graph

\```text
T001 -> T002
T001 -> T003 (parallel)
\```

## Phase 1: Setup

- [ ] T001 Create or update feature documentation structure.
  - Depends on: none
  - Files: `[docs-root]/specs/[###-feature-name]/`
  - Acceptance: Required package files exist.
  - Evidence: Pending.

- [ ] T002 Identify source and test files.
  - Depends on: T001
  - Files: `src/`, `tests/`
  - Acceptance: File list is documented in task, design, or change-impact.
  - Evidence: Pending.

- [x] T003 [P] Configure helpers.
  - Depends on: T001
  - Files: `scripts/`
  - Acceptance: Helpers run successfully.
  - Evidence: Validation command output.
  - [x] T003.1 Add helper command.
  - [x] T003.2 Run helper once.
```

### Checklist Enhancement Rules

- Keep `- [ ]` and `- [x]` checkboxes as the primary status marker.
- Preserve `[P]` markers for parallel-safe tasks.
- Add nested subtasks when the parent task has natural implementation steps.
- Add `Depends on:` when dependency order is not obvious from the phase.
- Add `Files:` when file ownership or conflict avoidance matters.
- Add `Acceptance:` to make completion defensible.
- Add `Evidence:` and leave it as `Pending.` until completion is verified.
- Use `Status: skipped - reason` only for intentionally skipped work.

### Dependency Inference

When migrating, infer dependencies from:

- Phase ordering (earlier phases block later phases)
- Explicit notes like "blocks user-story work"
- `[P]` markers indicate tasks that can run alongside others in the same phase
- Checkpoint statements indicate dependency gates

## Design Migration

### Old format

```markdown
# Design
## Overview
## Components And Changes
## Data And Contract Impact
## Operational Considerations
## Open Questions
```

### New format

```markdown
# Technical Design
## Overview
## High-Level Design
### System Architecture
### Components and Changes
### Data Models
### Data Flow
## Low-Level Design
### Algorithms and Logic
### Function Signatures and Interfaces
### Error Handling
## Operational Considerations
## Open Questions
## Related Artifacts
```

### Mapping

| Old section | New section |
|-------------|-------------|
| Overview | Overview |
| Components And Changes | High-Level Design → Components and Changes |
| Data And Contract Impact | High-Level Design → Data Models + Data Flow |
| Operational Considerations | Operational Considerations (unchanged) |
| Open Questions | Open Questions (unchanged) |
| — | Low-Level Design (add if implementation details exist) |

## Migration Procedure

1. Read the existing spec package fully.
2. Classify `spec.md` and `plan.md` as feature brief, migration input, or
   deprecated duplicate.
3. Create or update `requirements.md` from unpromoted `spec.md` + `plan.md`
   content using the field mappings above.
4. Add or update the durable source and durable impact mapping. State which
   durable requirements, design, architecture, API/contract, data-flow, runbook,
   verification, reference, ADR, backlog, or roadmap docs are added, modified,
   clarified, superseded, or unchanged.
5. Update `design.md` to add High-Level/Low-Level structure.
6. Rebuild or enhance `tasks.md` with Kiro-style checklist tasks, useful
   subtasks, dependency notes or a DAG, affected files, per-task acceptance
   criteria, and evidence.
7. Create `change-impact.md`, `verification.md`, `traceability.md`,
   `open-decisions.md`, `research.md`, or `quickstart.md` only when separate
   files reduce ambiguity. Otherwise embed the intent in the core artifacts.
8. Verify cross-references between artifacts are correct.
9. Decide whether to remove, archive, or leave `spec.md` and `plan.md` as
   historical migration inputs. Do not delete them if they carry unpromoted
   decision history.
10. Update any `Related Artifacts` links in remaining files.
11. Update repository indexes if they reference the old filenames.

## Post-Migration Verification

After migration, confirm:

- [ ] `requirements.md` exists with user stories and EARS acceptance criteria
- [ ] `requirements.md` records durable sources and durable impact, or links to
      `change-impact.md`
- [ ] `design.md` has High-Level and Low-Level sections
- [ ] `tasks.md` uses checklist tasks and subtasks as the primary structure
- [ ] Non-trivial dependencies are captured through `Depends on:` notes or a
      Task Dependency Graph
- [ ] Parent tasks have acceptance criteria and evidence fields where needed
- [ ] `verification.md` exists when quality gates or validation evidence need
      separate tracking
- [ ] `spec.md` and `plan.md` are classified as retained brief, migrated input,
      deprecated duplicate, or historical record
- [ ] No orphan references to `spec.md` or `plan.md`
- [ ] Duplicated requirements, design decisions, and durable-source baselines
      have one current source
- [ ] Durable docs touched by the spec are current-state docs or clearly marked
      proposed/deferred/historical where applicable
- [ ] Frontmatter status and dates are accurate
- [ ] Related Artifacts links resolve correctly
