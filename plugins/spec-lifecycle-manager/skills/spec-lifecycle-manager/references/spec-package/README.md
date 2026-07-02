---
title: Spec package templates
doc_type: reference
status: active
owner: platform
last_reviewed: 2026-06-13
---

# Spec Package Templates

Use these templates only when the target repository does not provide its own
spec-package templates or explicit documentation direction.

Default package path:

```text
[docs-root]/specs/[###-slug]/
```

Use `docs/` as the default docs root for owned repositories. Use a partition
such as `docs/<name>/` when the target repository has its own documentation
system and lifecycle material should stay separate.

## Artifact Relationship

Use the artifacts as a progressive chain:

1. `requirements.md`: stable statement of problem, goals, non-goals, user
   stories with EARS-format acceptance criteria, correctness properties,
   technical context, and success criteria.
2. `design.md`: implementation approach that satisfies the requirements,
   including high-level design (architecture, components, data models, data
   flow) and low-level design (algorithms, interfaces, error handling),
   operational considerations, and open questions.
3. `tasks.md`: Kiro-style phased checklist of independently verifiable tasks and
   subtasks, with dependency notes, affected files, acceptance criteria, and
   verification evidence where they add execution clarity.

### Optional Artifacts

4. `change-impact.md`: optional OpenSpec-style delta record for changes to
   existing durable behavior, including bug fixes, modifications, removals,
   clarifications, and promotion targets.
5. `verification.md`: validation plan, quality gates, evidence log, residual
   risks, and release or closure readiness checks.
6. `research.md`: optional investigation of unknowns, alternatives, constraints,
   prior art, and recommendations. Use for complex features where decisions need
   documented evidence.
7. `quickstart.md`: temporary setup, demo, validation, rollout, or operator
   notes that may later be promoted into durable docs. Use for developer
   onboarding or operational hand-off.
8. `open-decisions.md`: unresolved decisions that block stable requirements,
   design, implementation, verification, promotion, or closure.
9. `traceability.md`: optional bidirectional matrix that maps task IDs to
   requirements, acceptance criteria, design sections, change impact,
   verification, durable targets, and open decisions. Use it for larger specs
   or when agents need a task-ID lookup surface before implementation.
10. `canonical-context.md`: optional working-context map for specs that import
    or adapt durable docs, have broad durable-doc impact, name stale-doc risk,
    or resume work where older docs could be mistaken for current authority.

Small, low-risk work can use a smaller package. Create only the files that help
coordinate implementation, validation, or future promotion.

Required intent is broader than required files. Even when a supporting artifact
is not created, the package should still answer the relevant lifecycle
questions somewhere in the core files:

- What durable current-state sources does this change rely on?
- Which durable docs or contracts does this spec add to, modify, clarify,
  supersede, or leave unchanged?
- What validation is expected, waived, not applicable, or deferred?
- Which task IDs map to requirements, acceptance criteria, design sections, and
  durable promotion targets?
- Which decisions are open, who owns them, and whether they block
  implementation, verification, or closure?
- What content must be promoted to durable docs before the spec is closed?
- Which sources are spec-canonical for this slice, which external sources
  remain always-canonical, and which stale or historical docs are only
  background?

Create separate artifacts only when they reduce ambiguity or make large work
easier to resume. Do not create them only to satisfy ceremony.

`spec.md` is not part of the current fallback package. Existing projects may
still have old-format `spec.md` files; treat them as compatibility inputs that
must be classified as feature brief, migration input, or deprecated duplicate
before relying on them for implementation.

## Spec Package Metadata

Spec package files are temporary delivery artifacts. Use `doc_type: spec` for
all package files, then use `artifact_type` to identify the artifact:

```yaml
---
title: Feature requirements title
doc_type: spec
artifact_type: requirements
status: draft
owner: team-or-person
last_reviewed: YYYY-MM-DD
---
```

Recommended `artifact_type` values:

- `requirements`
- `design`
- `tasks`
- `change-impact`
- `verification`
- `research`
- `quickstart`
- `open-decisions`
- `traceability`

Durable docs use durable document classes such as `requirements`, `design`,
`architecture`, `runbook`, `adr`, `reference`, or `checklist`. Do not treat a
spec-package `requirements.md` or `design.md` as a durable source of truth after
closure; promote accepted content into the durable documentation set.

Durable docs describe current accepted state unless explicitly labeled as
proposed, planned, deferred, or historical. Active specs describe intended
changes. Keep that boundary visible so tools and agents do not surface future
intent as current implementation guidance.

## Template Files

### Core (always created)

- `requirements.md`
- `design.md`
- `tasks.md`

### Optional (created when they add value)

- `research.md`
- `change-impact.md`
- `verification.md`
- `quickstart.md`
- `open-decisions.md`
- `traceability.md`
- `canonical-context.md`

## Acceptance Criteria Format

Requirements use EARS (Easy Approach to Requirements Syntax) keywords:

- **GIVEN/WHEN/THEN**: Behavioral scenarios
- **WHERE**: Context-dependent behavior
- **WHILE**: State-dependent behavior
- **IF/THEN**: Conditional behavior
- **SHALL**: Unconditional requirements

## Task Checklist And Evidence

Use checkboxes as the visible task status:

- `- [ ] T001 ...`: pending or not started.
- `- [~] T001 ...`: in progress. Mark the selected task this way before
  starting work.
- `- [/] T001 ...`: partial. Some work is complete, but acceptance criteria are
  not fully met.
- `- [>] T001 ...`: follow-up or routed. Work moved to another task, spec,
  backlog item, issue, or owner; record `Destination:`.
- `- [-] T001 ...`: no-op or deferred. Work is intentionally unnecessary, not
  applicable, superseded, raw-only, or deferred from this spec.
- `- [?] T001 ...`: review or decision needed. Record `Decision owner:` when
  known.
- `- [!] T001 ...`: attention needed. A blocker, error, or intervention needs
  diagnosis; record the diagnostic state and next step.
- `- [x] T001 ...`: complete and verified.

Legacy markers remain readable during migration: `[Y]` maps to `partial`;
`[*]` and `[e]` map to `attention`. Do not use legacy markers in new package
templates or new task updates.

Use nested subtasks for the natural Kiro task shape. Add `Depends on:`, `Files:`,
`Acceptance:`, and `Evidence:` bullets under parent tasks when they help an
agent choose the next safe slice or verify completion.

Check off subtasks as work progresses, but check off the parent task only after
its acceptance criteria are met and evidence is recorded. Evidence can be a
command, test result, review note, screenshot, log, commit, or manual
verification note. Partial, follow-up, no-op, review-needed, and attention
states should include the remaining work, destination, decision owner, blocker,
error, or deferral reason in `Evidence:` or a `Status:` note.

Tasks are an execution index, not a standalone specification. Before
implementing a task, agents should review the relevant `requirements.md`,
`design.md`, `change-impact.md`, `verification.md`, `open-decisions.md`, and
durable-source baseline. If a task line is vague but the package provides
implementation detail elsewhere, use the fuller package context instead of
treating the task as non-implementable.

For larger packages, add `traceability.md` so agents can look up a task ID and
see the related requirements, acceptance criteria, design sections,
verification gates, durable-doc targets, and open decisions before coding.

## Lifecycle Phases

The spec lifecycle extends beyond the core artifacts:

1. **Create**: Generate requirements, design, and tasks.
2. **Implement**: Execute tasks in dependency order.
3. **Reconcile** (on resume): Detect drift between spec, code, and durable docs.
4. **Verify**: Record evidence, quality gates, residual risks, and readiness.
5. **Promote** (post-completion): Route accepted spec content into durable docs.
6. **Review** (optional): Role-based expert review per document class.
7. **Close**: Verify all content is promoted or deferred, remove the spec from
   active indexes, and archive or remove the package according to the
   repository's document lifecycle.
