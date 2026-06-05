---
title: Spec closure log management design
doc_type: spec
artifact_type: design
status: draft
owner: platform
last_reviewed: 2026-06-05
---

# Technical Design

## Overview

Spec closure log management adds a durable breadcrumb for closed spec packages
without keeping completed implementation scaffolding in the active docs path.
The full final spec package is preserved by Git. The current docs tree keeps a
compact closure entry that points to the final spec commit and explains where
current behavior now lives.

The recommended default is a **spec closure log**, not a general changelog. A
product or release changelog may later use closure entries as input, but closure
records have a different audience: future agents, maintainers, auditors, and
reviewers reconstructing why a spec disappeared.

## Requirement Coverage

| Requirement | Design Coverage | Validation Approach |
| --- | --- | --- |
| Requirement 1 | Closure log entry schema and final spec commit workflow. | Template review and fixture close trial. |
| Requirement 2 | Separate document roles and routing rules. | Docs review and skill prompt trial. |
| Requirement 3 | Two-commit close workflow. | Manual Git workflow test in a fixture repo. |
| Requirement 4 | Skill close guidance changes. | Skill validation fixture and static checks. |
| Requirement 5 | Durable closure-log template. | Template lint and link checks. |
| Requirement 6 | Verification and promotion fields in closure entries. | Closure entry review against completed fixture. |
| Requirement 7 | Active-doc cleanup rules. | Fixture close trial checks active indexes. |

## High-Level Design

### Document Roles

| Document | Role | Default Path Candidate |
| --- | --- | --- |
| Active spec index | Lists current active specs only. | `docs/specs/README.md` or existing docs index. |
| Spec closure log | Records closed specs, final spec commits, closure actions, durable promotions, verification summary, and follow-up. | `docs/history/spec-closure-log.md` or repository equivalent. |
| Product/release changelog | Communicates product, release, or operator-facing changes. | Existing repository changelog path. |
| Full spec archive | Full closed spec package. Prefer Git history; keep in tree only when policy requires. | Git final spec commit, or `docs/archive/specs/...` if required. |

Default decision:

- Keep `docs/specs/` focused on active implementation packages.
- Use `docs/history/spec-closure-log.md` as the fallback durable closure log
  path when the repository has no authoritative closure-log or archival path.
- Use `doc_type: history` for the fallback closure log document class.
- Use Git history as the default archive for removed closed specs.

Rationale:

- `docs/history/` makes the document's historical and audit role explicit
  without overloading product or release changelogs.
- `spec-closure-log.md` distinguishes implementation lifecycle closure records
  from broader changelog entries.
- `doc_type: history` already exists in the fallback durable document classes,
  so a new durable class is unnecessary for the MVP.
- Repositories with existing changelog, archive, compliance, or issue-tracking
  conventions remain authoritative and should record a template authority
  decision before adopting this fallback.

### Closure Entry Shape

```markdown
## YYYY-MM-DD - 005-spec-closure-log-management

- **Spec:** `docs/specs/005-spec-closure-log-management/`
- **Title:** Spec closure log management
- **Final spec commit:** `abc1234`
- **Closure cleanup commit:** pending | `def5678`
- **Closure action:** removed | archived | retained-as-history
- **Closed by:** role-or-person
- **Durable docs updated:**
  - `docs/design/spec-lifecycle-management.md`
  - `skills/spec-lifecycle-manager/SKILL.md`
- **Verification summary:** command, review, or evidence summary
- **Residual risks:** none | summary
- **Follow-up:** none | issue, backlog item, roadmap item, or follow-up spec
```

`Closure cleanup commit` may be recorded as `pending` in the cleanup commit
itself, because the commit hash does not exist before committing. A later
follow-up may fill it in, or tooling may derive it from Git history.

### Two-Commit Close Flow

```text
active spec ready to close
  -> promote durable docs
  -> record verification and cleanup readiness in spec
  -> commit final spec state
  -> add closure log entry with final spec commit
  -> remove/archive/mark historical spec package
  -> update active indexes
  -> commit closure cleanup
```

The final spec commit and cleanup commit have different jobs:

- Final spec commit: preserves the full final implementation scaffold.
- Cleanup commit: removes stale active scaffolding and records the durable
  closure breadcrumb.

### Closure Actions

| Action | Meaning | Use When |
| --- | --- | --- |
| `removed` | Spec package deleted from active tree; Git final spec commit is the archive. | Durable docs and closure log preserve all current and audit needs. |
| `archived` | Spec moved to an archive/history path in the current tree. | Compliance, audit, or local policy requires visible historical docs. |
| `retained-as-history` | Spec remains in place or nearby but is marked historical. | Moving/removing would break references or current lifecycle does not yet support cleanup. |

### Template Changes

Add a durable template:

```text
skills/spec-lifecycle-manager/references/durable-doc-templates/spec-closure-log.md
```

The template should use durable metadata:

```yaml
---
title: Spec closure log
doc_type: history
status: active
owner: team-or-person
last_reviewed: YYYY-MM-DD
---
```

It should explain that entries are durable breadcrumbs, not full current-state
docs and not product release notes.

### Skill Changes

Update `SKILL.md` close guidance:

- identify whether repository lifecycle uses a closure log;
- before removal, require a final spec commit hash;
- add or update closure log entry;
- remove the spec from active indexes;
- choose removal, archive, or retained-history action;
- report final spec commit and closure cleanup status.

Update promotion and verification guidance so durable promotion and closure log
entry are both checked before removal.

### Existing Template Changes

Update:

- `references/durable-doc-templates/README.md`: document the spec closure log
  class and when to use it.
- `references/durable-doc-templates/document-lifecycle.md`: describe Git-backed
  archive and two-commit close flow.
- `references/spec-package/verification.md`: add final spec commit and closure
  log fields.
- `references/document-routing-and-expert-review.md`: route closure records to
  the closure log.

## Low-Level Design

### Closure Log Fields

| Field | Required | Notes |
| --- | --- | --- |
| Date | yes | Closure date. |
| Spec ID | yes | Stable package ID such as `005-spec-closure-log-management`. |
| Spec path | yes | Original active package path. |
| Title | yes | Human-readable spec title. |
| Final spec commit | yes for removal | Commit containing final full spec state. |
| Closure cleanup commit | optional | May be pending at cleanup commit time. |
| Closure action | yes | `removed`, `archived`, or `retained-as-history`. |
| Durable docs updated | yes | Paths or explicit deferrals. |
| Verification summary | yes | Command/review/evidence summary. |
| Residual risks | yes | `none` or summary. |
| Follow-up | yes | `none` or links. |

### Final Spec Commit Detection

Manual MVP:

- operator records `git rev-parse HEAD` after committing final spec state;
- closure log stores the short or full hash;
- cleanup commit removes/archive-marks the package.

Future MCP/tooling:

- verify commit exists;
- verify the commit contains the spec path;
- verify the current cleanup diff removes or archive-marks the same path;
- warn if closure log final spec commit is missing or invalid.

### Active Index Rules

Active indexes should not become closure logs. They may include a short pointer:

```markdown
Closed specs are recorded in `docs/history/spec-closure-log.md`.
```

They should not list every closed spec unless local policy explicitly calls for
that.

### Changelog Boundary

Closure log entries are implementation-lifecycle records. They may feed:

- release notes;
- product changelogs;
- operator update notes;
- audit reports.

They do not replace those documents. A product changelog should summarize user
or operator-visible behavior, not every spec cleanup detail.

### Security And Trust

- Do not use closure log entries as instructions for current behavior.
- Treat final spec commits as historical evidence; current behavior belongs in
  durable docs and code.
- Do not remove specs unless Git history is available and the final state is
  committed.
- Repositories with compliance retention requirements may choose visible
  archives over Git-only archives.

## Validation Strategy

| Validation | Covers | Evidence Location | Residual Risk |
| --- | --- | --- | --- |
| Static template checks | Required closure log fields and metadata. | Validation evidence. | Low. |
| Fixture close trial | Two-commit removal workflow and active-index cleanup. | Validation evidence. | Medium until automated. |
| Skill prompt trial | Agent follows closure-log workflow. | Validation evidence. | Medium. |
| Link check | Closure log and durable docs links resolve. | Validation evidence. | Low. |

## Operational Considerations

- The first implementation can be documentation and skill-template only.
- Automation should come later through the spec-management MCP or hook roadmap.
- Closure logs should stay compact; full historical content belongs in Git or
  repository archives.
- Repositories may override default paths through their own docs lifecycle.

## Open Questions

- Is `doc_type: history` the best durable class for closure logs, or should
  there be a `doc_type: changelog` class?
- Should the default closure log template be generic enough for non-spec
  lifecycle records?
- Should closure entries include PR numbers, issue numbers, or implementation
  commit ranges when available?
- Should a future hook block deletion of `docs/specs/*` paths unless a closure
  log entry points at a final spec commit?
