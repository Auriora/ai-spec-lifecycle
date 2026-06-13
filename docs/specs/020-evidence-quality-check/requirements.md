---
title: Evidence quality check requirements
doc_type: spec
artifact_type: requirements
status: active
owner: platform
last_reviewed: 2026-06-13
---

# Requirements

## Durable Source Baseline

- Backlog item B012 calls for advisory evidence review.
- `tasks.md` conventions require concrete evidence when a task is checked.
- Spec closure requires validation evidence and quality gates to be complete or
  explicitly waived.

## Goals

- Classify task and verification evidence quality deterministically.
- Distinguish concrete command/file evidence from vague completion claims.
- Distinguish intentionally not-applicable validation from missing or skipped
  validation.
- Keep output advisory and waiver-friendly.
- Build on validation plan outputs when available.

## Non-Goals

- Do not inspect implementation code for stubs; B037 covers that.
- Do not run validation commands.
- Do not block task completion by default.

## Requirements

### Requirement 1: Evidence Extraction

**User Story:** As a maintainer, I want completed-task evidence extracted from
spec artifacts, so that weak evidence is visible before closure.

#### Acceptance Criteria

1. GIVEN a spec package, WHEN evidence quality runs, THEN the system SHALL
   inspect completed tasks and verification evidence sections.
2. WHERE a task has no concrete evidence, THE SYSTEM SHALL report a diagnostic
   with task ID and source path.
3. IF evidence references a command, file, commit, review, or explicit waiver,
   THEN the system SHALL classify it separately from vague prose.

### Requirement 2: Evidence Classification

**User Story:** As an agent, I want evidence classified by quality, so that I
know what must be strengthened before closure.

#### Acceptance Criteria

1. WHEN evidence is concrete, THEN the system SHALL classify it as `concrete`.
2. WHEN evidence uses phrases such as "done" without command, file, or review
   reference, THEN the system SHALL classify it as `vague`.
3. WHEN evidence is pending, missing, or empty, THEN the system SHALL classify
   it as `missing`.
4. WHEN evidence is an explicit waiver or deferral, THEN the system SHALL
   preserve the waiver reason and classify it as `waived` or `deferred`.
5. WHEN validation evidence says checks were not run because the change was
   documentation-only, THEN THE SYSTEM SHALL classify the evidence as
   `not_applicable` only if a validation plan or task context supports that
   scope.
6. IF documentation-only wording is used to avoid a check that still applies to
   the task acceptance or changed files, THEN THE SYSTEM SHALL classify the
   evidence as `not_run` or `weak` with a residual-risk finding.

### Requirement 3: MCP Surface

**User Story:** As a tool-calling agent, I want evidence quality exposed through
MCP, so that closure and review tools can reuse the signal.

#### Acceptance Criteria

1. WHEN MCP tools are listed, THEN `evidence_quality_check` SHALL be available
   as a read-only tool.
2. WHEN called with `spec_path`, THEN it SHALL return diagnostics, summary, and
   task-level evidence records.

## Correctness Properties

- CP-001: Classification SHALL be deterministic for the same artifacts.
- CP-002: Evidence review SHALL not mutate task status or verification files.
- CP-003: Every diagnostic SHALL identify the source artifact and task or
  section where possible.
- CP-004: `not_applicable` validation SHALL not be reported as weak evidence
  when the validation plan supports it.

## Success Criteria

- Runtime and MCP tests cover concrete, vague, missing, waived,
  not-applicable, and not-run evidence.
- Runtime docs publish the evidence quality contract.
