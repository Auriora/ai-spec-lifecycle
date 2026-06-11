---
title: Spec closure log
doc_type: history
status: active
owner: team-or-person
last_reviewed: YYYY-MM-DD
---

# Spec Closure Log

Use this durable log to record compact closure entries for completed spec
packages when the full final spec state is preserved by Git or an approved
archive path. This log is implementation-lifecycle history, not a product or
release changelog.

Default path when the repository has no authoritative lifecycle history path:

```text
docs/history/spec-closure-log.md
```

## Purpose

- Keep `docs/specs/` focused on active implementation packages.
- Preserve discoverability for removed specs and for archived or retained
  historical specs only when explicit repository policy requires them.
- Record the final spec commit that contains the complete final package before
  removal or cleanup.
- Point future readers to durable current-state docs rather than temporary
  implementation scaffolding.

## Entries

Add one entry per closed spec. Use reverse chronological order unless the
repository documents another order.

### YYYY-MM-DD - 000-spec-slug

- **Spec:** `docs/specs/000-spec-slug/`
- **Title:** Human-readable spec title
- **Final spec commit:** `required-before-removal`
- **Closure cleanup commit:** pending
- **Closure action:** removed | archived | retained-as-history
- **Closed by:** role-or-person
- **Durable docs updated:**
  - `docs/path.md`
  - deferred: reason and follow-up link
- **Verification summary:** command, review, or evidence summary
- **Residual risks:** none | summary
- **Follow-up:** none | backlog item, roadmap item, issue, or follow-up spec

## Closure Actions

| Action | Meaning |
| --- | --- |
| `removed` | Spec package was deleted from the active tree after the final spec commit recorded the full package. |
| `archived` | Spec package was moved to an archive/history path because repository policy requires visible historical docs. |
| `retained-as-history` | Spec package remains in place or nearby by explicit exception and is clearly marked historical, archived, or superseded. |

## Required Checks

Before recording `removed`:

- The final spec state is committed.
- The final spec commit contains the spec package path.
- Durable docs describe accepted current behavior.
- Verification and residual risk are summarized.
- Follow-up work is linked or recorded as `none`.

If the final spec commit is missing, do not remove the spec package. Record the
blocker in the active spec or closure checklist instead.

## Changelog Boundary

This log may feed product changelogs, release notes, operator updates, or audit
reports, but it does not replace those documents. Product and release
changelogs should summarize user- or operator-visible changes rather than every
spec lifecycle cleanup detail.
