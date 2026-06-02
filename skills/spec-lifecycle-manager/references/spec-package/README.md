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
3. `tasks.md`: dependency graph and phased checklist of independently verifiable
   implementation slices, with explicit status tracking and traceability back to
   requirements, design, and verification evidence.

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

Small, low-risk work can use a smaller package. Create only the files that help
coordinate implementation, validation, or future promotion.

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

## Acceptance Criteria Format

Requirements use EARS (Easy Approach to Requirements Syntax) keywords:

- **GIVEN/WHEN/THEN**: Behavioral scenarios
- **WHERE**: Context-dependent behavior
- **WHILE**: State-dependent behavior
- **IF/THEN**: Conditional behavior
- **SHALL**: Unconditional requirements

## Task Status Values

| Status | Meaning |
|--------|---------|
| pending | Not yet started |
| in_progress | Currently being worked on |
| done | Complete and verified |
| skipped | Intentionally deferred with documented reason |

## Task Evidence

Every task should include an `Evidence` field. Keep it empty while pending, then
record the command, test result, review note, screenshot, log, commit, or manual
verification note that proves completion when the task moves to `done`.

## Lifecycle Phases

The spec lifecycle extends beyond the core artifacts:

1. **Create**: Generate requirements, design, and tasks.
2. **Implement**: Execute tasks in dependency order.
3. **Reconcile** (on resume): Detect drift between spec, code, and durable docs.
4. **Verify**: Record evidence, quality gates, residual risks, and readiness.
5. **Promote** (post-completion): Route accepted spec content into durable docs.
6. **Review** (optional): Role-based expert review per document class.
7. **Close**: Verify all content is promoted or deferred, close the spec.
