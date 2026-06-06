---
title: Brooks-Lint findings tracking
doc_type: spec
artifact_type: overview
status: draft
owner: platform
last_reviewed: 2026-06-06
---

# Brooks-Lint Findings Tracking

## Purpose

Create a durable workflow for recording, triaging, and resolving Brooks-Lint
findings as each Brooks skill is run against this repository.

## Context

The first Brooks architecture audit recorded these seed findings:

- `spec_runtime.py` is becoming a lifecycle god module.
- The bundled plugin copy can drift from the development skill source.
- The installer concentrates unrelated deployment concerns.
- The Codex hook has a hardwired subprocess seam.

The first Brooks tech debt assessment recorded the same structural hotspots as
scheduled or monitored debt, plus Pain x Spread priority scores for remediation
planning.

The first Brooks health dashboard recorded a composite score and dimension
scores across architecture, tech debt, and test quality. The code-quality
dimension was skipped because there was no tracked code diff.

The first Brooks test quality review recorded the suite as fast and mostly
unit-level, with fixture duplication and packaging coverage gaps as the main
test-maintenance risks.

The tracking mechanism should support future runs of Brooks skills, not just
the initial architecture audit.

## Artifacts

- Requirements: [requirements.md](requirements.md)
- Research: [research.md](research.md)
- Design: [design.md](design.md)
- Change Impact: [change-impact.md](change-impact.md)
- Open Decisions: [open-decisions.md](open-decisions.md)
- Tasks: [tasks.md](tasks.md)
- Traceability: [traceability.md](traceability.md)
- Verification: [verification.md](verification.md)
