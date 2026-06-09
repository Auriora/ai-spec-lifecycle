---
title: Brooks-Lint findings tracking design
doc_type: spec
artifact_type: design
status: draft
owner: platform
last_reviewed: 2026-06-06
---

# Design

## Overview

Add a durable Brooks findings register that sits beside existing review docs.
Each Brooks skill run can append or reconcile findings without relying on chat
history. The register should be lightweight enough to maintain manually while
still preserving the Brooks-Lint finding structure.

## High-Level Design

```text
Brooks skill run
  -> Brooks report in Codex session
  -> durable finding register
  -> triage state
  -> spec task, backlog item, roadmap item, dismissal, or resolved evidence
```

The register does not replace `.brooks-lint-history.json`; it explains the
findings behind score movement.

## Low-Level Design

### Finding ID Format

Use `BL-<MODE>-<NNN>`:

- `BL-ARCH-001` for architecture audit findings.
- `BL-REVIEW-001` for review findings.
- `BL-DEBT-001` for technical debt findings.
- `BL-HEALTH-001` for health dashboard findings.
- `BL-TEST-001` for test-quality findings.
- Future Brooks skills can add mode prefixes when needed.

### Finding States

| State | Meaning |
|-------|---------|
| `needs-decision` | Finding has been recorded but not yet accepted, deferred, dismissed, or resolved. |
| `accepted` | Finding should be fixed or tracked through planned work. |
| `deferred` | Finding is valid but not planned now; a reason and destination are required. |
| `dismissed` | Finding is not actionable for this repository; a reason is required. |
| `resolved` | Finding has been fixed or otherwise closed with evidence. |

### Register Location

Preferred location:

```text
docs/reviews/brooks-lint/README.md
```

This location matches the repository's existing `docs/reviews/` convention and
keeps review outputs separate from active implementation specs.

### Finding Template

Each detailed finding should preserve:

- ID
- Mode
- Date first seen
- Last seen
- Scope
- Severity
- State
- Symptom
- Source
- Consequence
- Remedy
- Repository references
- Triage rationale
- Linked task, backlog, roadmap, or commit
- Verification evidence

### Seed Register Entries

The first implementation should seed the register with:

- `BL-ARCH-001`: `spec_runtime.py` is becoming the lifecycle god module.
- `BL-ARCH-002`: bundled plugin copy can drift from development skill.
- `BL-ARCH-003`: installer concentrates unrelated deployment concerns.
- `BL-ARCH-004`: hook runtime execution is hardwired to subprocess.
- `BL-DEBT-001`: `spec_runtime.py` concentrates many lifecycle responsibilities.
- `BL-DEBT-002`: development skill and bundled plugin trees can drift.
- `BL-DEBT-003`: installer changes mix package copy, Codex cleanup,
  marketplace edits, and plugin registration.
- `BL-DEBT-004`: hook checks shell out through a hardwired subprocess seam.
- `BL-HEALTH-001`: installer fan-out is the main dependency-disorder signal.
- `BL-HEALTH-002`: `spec_runtime.py` remains the top maintainability hotspot.
- `BL-HEALTH-003`: skill/plugin duplication remains a drift risk.
- `BL-HEALTH-004`: installer orchestration remains scheduled debt.
- `BL-HEALTH-005`: CLI and hook tests rely on subprocess fixtures in several
  places.
- `BL-TEST-001`: spec-package fixture builders are duplicated across runtime,
  MCP, hook, and traceability tests.
- `BL-TEST-002`: plugin package tests verify component presence but not full
  development-skill to bundled-plugin sync or installer behavior.
- `BL-TEST-003`: CLI and hook tests rely on subprocess boundaries and exact
  stdout/stderr behavior.

### Debt Priority Fields

Brooks-Debt findings should additionally preserve:

- Pain score
- Spread score
- Priority score
- Debt classification
- Debt intent

### Health Dashboard Fields

Brooks-Health findings should additionally preserve:

- Dimension
- Dimension score
- Composite score
- Whether the code-quality dimension was skipped
- Score weighting notes

### Test Quality Fields

Brooks-Test findings should additionally preserve:

- Test risk code
- Suite map
- Test layer
- Coverage area or gap
- Relevant test files

## Operational Considerations

- Repeated Brooks runs should update `last seen` and evidence rather than
  creating duplicates for the same structural issue.
- Dismissed findings should remain visible with rationale.
- Deferred findings should route to backlog or roadmap if they outlive this
  spec.
- Findings fixed during this spec should include validation commands and commit
  references before being marked `resolved`.

## Open Questions

- Should a register schema be validated by runtime code now or deferred until
  there are multiple Brooks runs?
- Should `.brooks-lint-history.json` be committed as part of the durable record
  or treated as local run telemetry?
- Should active Brooks findings become backlog entries immediately or only when
  deferred beyond this spec?
