---
title: Closure risk review design
doc_type: spec
artifact_type: design
status: active
owner: platform
last_reviewed: 2026-06-13
---

# Design

## Overview

Add `closure_risk_review` as a deterministic aggregator over existing closure
signals. It makes closure decisions easier to review without invoking a
secondary agent.

## High-Level Design

- Call existing `closure_check` and `promotion_plan`.
- Include validation plan and evidence quality signals when those helpers are
  available.
- Inspect tasks, verification, open decisions, and durable baseline references.
- Inspect whether stale or superseded content remains in active docs where
  tools and agents may surface it as current guidance.
- Return risk level, findings, blind spots, and recommended next action.

## Low-Level Design

- `low`: no blockers, no weak evidence, durable targets exist, validation plan
  has required checks, and historical recovery evidence exists for removed
  scaffolding when needed.
- `medium`: closure technically ready but weak evidence, missing optional
  validation, deferred follow-up needs routing, or stale active docs have a
  bounded chance of being surfaced as current guidance.
- `high`: closure blockers, missing durable promotion, unresolved decisions, or
  package removal would orphan current behavior. Also high when obsolete active
  docs are likely to mislead Agent Workbench, lifecycle tooling, search, or
  future implementation agents.

Closure risk should distinguish two different concerns:

- Recoverability risk: old spec content can be recovered from Git, closure log,
  and archive index. When those breadcrumbs are present, this is usually low.
- Active guidance risk: stale docs remain in the live documentation path and
  may be selected by tools or agents as current context. This can be medium or
  high because it can cause incorrect future implementations.

## Operational Considerations

- Closure risk review is advisory and should be run before closure records and
  package removal.
- Review packet aliases remain useful for human/model review, but this helper
  is deterministic.

## Open Questions

- None.
