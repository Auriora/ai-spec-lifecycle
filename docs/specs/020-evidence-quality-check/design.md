---
title: Evidence quality check design
doc_type: spec
artifact_type: design
status: active
owner: platform
last_reviewed: 2026-06-11
---

# Design

## Overview

Add an advisory `evidence_quality_check` helper that reviews task evidence and
verification evidence without running commands or checking implementation code.

## High-Level Design

- Parse tasks with the existing task parser.
- Extract evidence bullets and verification evidence rows/lines.
- Classify evidence with simple deterministic heuristics.
- Return summary counts and diagnostics for weak or missing evidence.

## Low-Level Design

- Concrete signals include shell commands, MCP tool names, file paths, commit
  hashes, review paths, package names, or explicit test counts.
- Vague signals include standalone "done", "complete", "implemented", or
  similar claims without references.
- Pending/missing signals include empty evidence, `Pending`, or absent evidence
  bullets on completed tasks.
- Waived/deferred signals require explicit waiver/defer wording and a reason.

## Operational Considerations

- This is advisory by default because evidence language varies across projects.
- B037 may later add implementation-file inspection for task completion claims.

## Open Questions

- None.
