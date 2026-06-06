---
title: Spec closure log management research
doc_type: spec
artifact_type: research
status: archived
owner: platform
last_reviewed: 2026-06-05
---

# Research

## Scope

This note records the local decision framing for Git-backed spec archival and
closure logs. It does not choose the final default path; that remains an
implementation task.

## Question

Should closed spec packages be retained in the current docs tree, removed and
recovered from Git, or summarized in a changelog-like durable document?

## Options Considered

| Option | Summary | Pros | Cons | Notes |
| --- | --- | --- | --- | --- |
| Keep full closed specs in tree | Move or mark closed packages as archived. | Easy browsing, no Git command needed. | Stale-doc risk, active docs clutter, duplicate current truth. | Useful for compliance-heavy repos. |
| Remove specs and rely only on Git | Delete closed packages after promotion. | Clean active docs, no duplicate scaffolding. | Harder discovery; requires knowing commit hash. | Needs durable breadcrumb. |
| Closure log plus Git final spec commit | Record compact closure entry and final spec commit, then remove/archive spec based on policy. | Clean docs plus audit path. | Requires disciplined two-commit workflow. | Recommended default. |
| Full product changelog | Fold spec closure into release/user changelog. | User-facing summary potential. | Mixes implementation scaffolding with product changes. | Better as downstream output, not primary record. |

## Findings

- The existing lifecycle already says specs are temporary and durable docs must
  become the source of truth.
- Git can preserve final full spec state if the workflow commits the spec before
  deletion.
- A compact closure log solves discoverability without keeping stale
  implementation scaffolding active.
- Product changelogs and closure logs have different audiences and should not
  be collapsed by default.

## Tradeoffs

The two-commit workflow adds ceremony at closure time, but it makes deletion
auditable and keeps current docs clean. Keeping full archived specs visible is
simpler for browsing but increases the chance that future agents read stale
scaffolding as current behavior.

## Sources

- Local lifecycle design: [Spec lifecycle management](../../design/spec-lifecycle-management.md)
- Local skill close guidance:
  [SKILL.md](../../../skills/spec-lifecycle-manager/SKILL.md)
- Local document lifecycle template:
  [document-lifecycle.md](../../../skills/spec-lifecycle-manager/references/durable-doc-templates/document-lifecycle.md)

## Confidence And Unknowns

- **Confidence:** medium
- **Known unknowns:** best default path; whether `doc_type: history` is enough;
  how much automation should be in hooks versus MCP tools.
- **Assumptions:** Git history is available to future maintainers; repositories
  can override defaults when compliance requires visible archives.
- **Evidence gaps:** no dogfood close trial yet.

## Recommendation

Add closure-log management to the skill as a documented close workflow. Use a
spec closure log as the durable breadcrumb and Git as the default full archive
for removed specs. Keep product changelogs separate.

## Decision Impact

- Requirements: closure requires final spec commit when removing a spec.
- Design: active indexes, closure logs, and product changelogs get distinct
  roles.
- Tasks: implementation needs a closure-log template, skill guidance updates,
  and validation coverage.
- Verification: closure checks must verify final spec commit and closure entry.

## Related Artifacts

- Requirements: [requirements.md](requirements.md)
- Design: [design.md](design.md)
- Tasks: [tasks.md](tasks.md)
