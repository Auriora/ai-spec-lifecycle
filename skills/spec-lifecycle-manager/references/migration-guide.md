# Spec Package Migration Guide

Use this guide to decide whether and how to migrate spec packages from the old
format (spec.md + plan.md + checkbox tasks) to the current format
(requirements.md + enriched design.md + DAG tasks).

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
- `tasks.md` uses `- [ ]` / `- [x]` checkboxes without Status fields
- `tasks.md` lacks a Task Dependency Graph section
- `design.md` lacks High-Level Design / Low-Level Design sections

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

### Conversion Rules

1. **FR-001 bullets → User story requirements**

   Old:
   ```markdown
   - **FR-001**: System MUST identify active spec packages using `docs/specs/[###-slug]/`.
   ```

   New:
   ```markdown
   ### Requirement 1: Active Spec Package Detection

   **User Story:** As an agent, I want to automatically identify active spec
   packages, so that I can resume work without manual navigation.

   #### Acceptance Criteria

   1. GIVEN a repository with `docs/specs/[###-slug]/` directories, WHEN the
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

## Task Migration: Checkboxes → Status + DAG

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
T001 → T002
T001 → T003 (parallel)
\```

## Phase 1: Setup

### Task 1: Create Documentation Structure

- **ID:** T001
- **Status:** pending
- **Depends on:** []
- **Parallel:** no
- **Story:** —
- **Files:** `docs/specs/[###-feature-name]/`
- **Description:** Create or update feature documentation structure.
- **Acceptance:** Directory exists with required template files.
- **Evidence:** Directory listing or diff showing created files.

### Task 2: Identify Source Files

- **ID:** T002
- **Status:** pending
- **Depends on:** [T001]
- **Parallel:** no
- **Story:** —
- **Files:** `src/`, `tests/`
- **Description:** Identify source and test files affected by the plan.
- **Acceptance:** File list documented in task or design.
- **Evidence:** Design section or search output summary.

### Task 3: Configure Helpers

- **ID:** T003
- **Status:** done
- **Depends on:** [T001]
- **Parallel:** yes
- **Story:** —
- **Files:** `scripts/`
- **Description:** Configure or update local validation helpers.
- **Acceptance:** Helpers run successfully.
- **Evidence:** Validation command output.
```

### Status Mapping

| Old | New |
|-----|-----|
| `- [ ]` (unchecked) | `pending` |
| `- [x]` (checked) | `done` |
| `[P]` marker | `Parallel: yes` |
| No explicit status | `pending` |
| No verification note | `Evidence: Pending.` |

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
2. Create `requirements.md` from `spec.md` + `plan.md` using the field mappings
   above.
3. Update `design.md` to add High-Level/Low-Level structure.
4. Rebuild `tasks.md` with DAG, status fields, and per-task acceptance criteria.
5. Create `verification.md` when the package has validation gates, evidence, or
   residual risks worth tracking separately.
6. Verify cross-references between artifacts are correct.
7. Decide whether to remove, archive, or leave `spec.md` and `plan.md` as
   historical migration inputs. Do not delete them if they carry unpromoted
   decision history.
8. Update any `Related Artifacts` links in remaining files.
9. Update repository indexes if they reference the old filenames.

## Post-Migration Verification

After migration, confirm:

- [ ] `requirements.md` exists with user stories and EARS acceptance criteria
- [ ] `design.md` has High-Level and Low-Level sections
- [ ] `tasks.md` has a Task Dependency Graph and per-task status fields
- [ ] Task entries have Evidence fields
- [ ] `verification.md` exists when quality gates or validation evidence need
      separate tracking
- [ ] No orphan references to `spec.md` or `plan.md`
- [ ] Frontmatter status and dates are accurate
- [ ] Related Artifacts links resolve correctly
