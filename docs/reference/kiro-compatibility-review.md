---
title: Kiro compatibility review — spec-lifecycle-manager skill
doc_type: reference
status: active
owner: platform
last_reviewed: 2026-06-02
---

# Kiro Compatibility Review

Review of the `spec-lifecycle-manager` skill and its templates against Kiro's
native spec format. Conducted 2026-06-02. Documents findings, decisions, and
resulting changes.

## Context

Kiro is an AI-powered development environment that uses a structured spec-driven
development workflow. The goal of this review was to align the
`spec-lifecycle-manager` skill's templates with Kiro's spec format while
preserving the skill's unique value-adds (reconciliation, promotion, expert
review).

## Comparison: Existing Skill vs Kiro Native

### Structure and File Naming

| Aspect | Existing skill | Kiro native |
|--------|---------------|-------------|
| Location | `docs/specs/[###-slug]/` | `.kiro/specs/{feature-name}/` |
| Naming | Numbered prefix (`001-slug`) | Kebab-case only (`user-auth`) |
| Core files | `spec.md`, `design.md`, `plan.md`, `tasks.md` | `requirements.md`, `design.md`, `tasks.md` |
| Optional files | `research.md`, `quickstart.md` | None |
| Config | Frontmatter metadata per file | `.config.kiro` per spec folder |

### Content Model

| Aspect | Existing skill | Kiro native |
|--------|---------------|-------------|
| Requirements | FR-001 bullet style in `spec.md` | User stories with EARS-format acceptance criteria in `requirements.md` |
| Design | Lightweight (overview, components, data, operations) | Rich (high-level: architecture, data models, data flow; low-level: algorithms, signatures, error handling) |
| Tasks | Phased checklist with `[P]` markers and `T001` IDs | Task Dependency Graph (DAG) with per-task status tracking |
| Research | Dedicated `research.md` | No equivalent (conversational) |
| Plan | Dedicated `plan.md` (governance, risks, phases) | No equivalent (folded into design and tasks) |
| Quickstart | Dedicated `quickstart.md` | No equivalent |
| Correctness | Success criteria (technology-agnostic outcomes) | Property-based testing with formal correctness properties |

### Workflow Philosophy

| Aspect | Existing skill | Kiro native |
|--------|---------------|-------------|
| Lifecycle | Intake → Reconcile → Implement → Promote → Review → Close | Requirements → Design → Tasks → Execute |
| Promotion | Explicit routing to durable docs | No promotion; specs are source of truth during feature work |
| Expert review | Role-based review matrix | No review concept |
| Reconciliation | Drift detection when resuming | No reconciliation; specs are living documents |

## Decisions

### Selected Changes

The following alignment changes were selected:

1. **A. Consolidate spec.md + plan.md → requirements.md**
   - Merge problem/goals/requirements/acceptance criteria from `spec.md` and
     execution context from `plan.md` into a single `requirements.md`
   - User stories with EARS-format acceptance criteria as the primary structure
   - Add correctness properties section for property-based testing
   - Retain goals/non-goals/technical context as hybrid additions

2. **B. Enrich design.md**
   - Add High-Level Design section (system architecture, components, data
     models, data flow)
   - Add Low-Level Design section (algorithms, function signatures, error
     handling)
   - Retain operational considerations (value-add not in Kiro)

3. **C. Restructure tasks.md to use a dependency graph**
   - Task Dependency Graph (DAG) at the top of the file
   - Per-task `Depends on` field with explicit task ID references
   - Status tracking (pending/in_progress/done/skipped) replaces checkboxes
   - Keep phased grouping as visual organizer alongside DAG
   - Per-task acceptance criteria for reconciliation verification

4. **F. Keep promotion/review/reconciliation as value-adds**
   - Reconciliation: automatic on resume, separate output (not persisted in spec
     files)
   - Promotion: post-tasks phase after all tasks reach done
   - Expert review: optional per-spec (opt-in via frontmatter or config)

5. **G. Add later lifecycle extensions beyond native Kiro**
   - `change-impact.md` records durable deltas for features, bug fixes,
     refactors, migrations, operational changes, and clarifications.
   - `verification.md` records evidence, quality gates, ship or closure risk,
     blast radius, rollback, review, and release-note needs.

### Rejected / Deferred Changes

- **D. Drop research.md, plan.md, quickstart.md from core**: Not adopted.
  Research and quickstart remain as optional artifacts. Spec.md and plan.md
  remain as deprecated references for migration.
- **E. Add .config.kiro and adopt Kiro folder conventions**: Deferred. The skill
  retains `docs/specs/[###-slug]/` as its default path. A future change could
  support `.kiro/specs/` as an alternative.

## Clarifications

### requirements.md Format

- **Hybrid approach**: Keep problem/goals/non-goals context sections alongside
  Kiro-style user stories
- **EARS keywords**: GIVEN/WHEN/THEN, WHERE, WHILE, IF/THEN, SHALL
- **Edge cases**: Become acceptance criteria on relevant requirements rather than
  a standalone section
- **FR-001 IDs**: Not retained as the primary structure; replaced by numbered
  requirements with user stories

### tasks.md Format

- **Phased grouping + dependency graph**: Phases provide visual structure;
  the DAG provides machine-readable execution order
- **Status field**: Replaces checkbox convention (`- [ ]` / `- [x]`)
- **Checkpoints**: Retained between phases for reconciliation gates

### Reconciliation Output

- **Separate report**: Reconciliation produces a standalone summary, not a
  section appended to spec files
- **Trigger**: Automatic when resuming an existing or partially completed spec
- **Drift classification**: spec stale, code incomplete, durable docs stale,
  decision unresolved, implemented but unverified, intentionally deferred

## Resulting File Changes

### New Files

| File | Purpose |
|------|---------|
| `references/spec-package/requirements.md` | Core template — user stories, EARS acceptance criteria, correctness properties, technical context, success criteria |
| `references/spec-package/change-impact.md` | Optional durable-delta template for behavior changes and bug fixes |
| `references/spec-package/verification.md` | Optional verification, evidence, quality gate, and ship-risk template |

### Updated Files

| File | Changes |
|------|---------|
| `references/spec-package/design.md` | Added High-Level Design and Low-Level Design sections |
| `references/spec-package/tasks.md` | Added Task Dependency Graph, per-task Depends on/Status/Acceptance fields, status legend |
| `references/spec-package/README.md` | Reflects three-file core, EARS format reference, status values, lifecycle phases |

### Deleted Files

| File | Superseded by |
|------|---------------|
| `references/spec-package/spec.md` | `requirements.md` |
| `references/spec-package/plan.md` | `requirements.md`, `design.md`, `tasks.md` |

### Unchanged Files

| File | Reason |
|------|--------|
| `references/spec-package/research.md` | Remains as optional artifact |
| `references/spec-package/quickstart.md` | Remains as optional artifact |
| `references/document-routing-and-expert-review.md` | Unchanged; governs promotion and review phases |
| `SKILL.md` | Updated to reference the three-file core, verification support, and migration decision gate |

## Migration Strategy

**Approach**: Hybrid — migration decision gate in SKILL.md Reconcile section +
detailed `references/migration-guide.md`.

- SKILL.md Reconcile section now detects old-format specs (presence of `spec.md`
  or `plan.md`, or checkbox-style tasks without a DAG) and directs the agent to
  read the migration guide and choose whether to continue old format, migrate
  first, or create a follow-up migration task.
- `references/migration-guide.md` contains full field mappings, conversion
  rules, and a step-by-step procedure.
- Archived specs (like `001-spec-lifecycle-manager-skill`) are left as-is unless
  resumed for further work.

## Pending Work

The following updates remain to fully complete the alignment:

1. **Consider .kiro/specs/ path support** — Evaluate whether the skill should
   support `.kiro/specs/{feature-name}/` as an alternative location for
   environments where Kiro is the primary agent.
