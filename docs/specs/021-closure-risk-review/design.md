---
title: Closure risk review design
doc_type: spec
artifact_type: design
status: active
owner: platform
last_reviewed: 2026-06-11
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
- Return risk level, findings, blind spots, and recommended next action.

## Low-Level Design

- `low`: no blockers, no weak evidence, durable targets exist, validation plan
  has required checks.
- `medium`: closure technically ready but weak evidence, missing optional
  validation, or deferred follow-up needs routing.
- `high`: closure blockers, missing durable promotion, unresolved decisions, or
  package removal would orphan current behavior.

## Operational Considerations

- Closure risk review is advisory and should be run before closure records and
  package removal.
- Review packet aliases remain useful for human/model review, but this helper
  is deterministic.

## Open Questions

- None.
