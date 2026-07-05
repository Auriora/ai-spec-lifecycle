---
title: Spec closure helper
doc_type: spec
artifact_type: requirements
status: draft
authoring_mode: wizard
lifecycle_stage: tasks
owner: platform
last_reviewed: 2026-07-05
---

# Requirements

## Problem Context

Closing completed specs still requires several ordered steps that are easy for
agents to blur together: confirm durable promotion, identify the final spec
commit, remove or archive the temporary package, update closure history, update
archive index metadata, route follow-up work, prove the package is no longer
active, and rerun validation. Recent closures have succeeded, but the workflow
still depends on agent memory and manual sequencing.

The closure of `030-mcp-first-runtime-migration` on 2026-07-05 exposed several
specific failure modes this helper should address: the final spec commit and
cleanup commit were separate, closure metadata needed a temporary
cleanup-commit placeholder before being resolved in a later metadata commit,
active backlog wording had to be changed from active to done, active-spec scans
had to prove the package was removed, archive-index test expectations changed,
and residual risks such as plugin reload requirements had to be captured before
closure was complete.

Several of those steps are deterministic enough to script. The helper should
reduce the number of separate actions an agent must remember by discovering the
highest-confidence complete package commit, generating closure-log and
archive-index entries, preparing package-removal edits, replacing pending
cleanup hashes, and returning validation commands as one guided sequence. Human
review remains required for judgment calls such as whether durable promotion is
sufficient, whether residual risks are acceptable, and whether package removal
should proceed.

Backlog item B056 proposes a structured helper for this closure workflow. This
artifact captures the accepted requirements for the design-stage closure-helper
work; tasks, traceability, and verification remain deferred until design review
is accepted.

## Durable Source Baseline

- `docs/backlog/README.md` B056.
- `docs/history/spec-closure-log.md`.
- `docs/history/spec-archive-index.md`.
- `docs/reference/spec-lifecycle-runtime.md`.
- `skills/spec-lifecycle-manager/SKILL.md`.
- Closure record for `030-mcp-first-runtime-migration` in
  `docs/history/spec-closure-log.md`.
- Archive index entry for `030-mcp-first-runtime-migration` in
  `docs/history/spec-archive-index.md`.

## Canonical Context

- Always-canonical sources: system, developer, user, and repository
  instructions; current Git state; current tests; current runtime behavior.
- Spec-canonical working sources: `requirements.md`, `design.md`, `tasks.md`,
  and `traceability.md` in this package while spec 029 is active.
- Imported durable sources:
  - `docs/backlog/README.md` B056 is the planning source for the closure-helper
    backlog item and its current active status.
  - `docs/history/spec-closure-log.md` is the narrative history source for
    closed spec records and verification summaries.
  - `docs/history/spec-archive-index.md` is the compact machine-verifiable
    closed-spec lookup source.
  - `docs/reference/spec-lifecycle-runtime.md` is the durable source for current
    runtime, MCP, and CLI behavior.
  - `skills/spec-lifecycle-manager/SKILL.md` is the durable source for agent
    lifecycle workflow rules.
- Historical evidence: the spec 030 closure records are evidence for the
  failure modes this helper must address, not current implementation authority
  for spec 029.
- Promotion targets: accepted behavior from this spec should be promoted to the
  runtime reference, skill guidance, lifecycle design docs, backlog status, and
  closure/archive history as applicable before closure.

## Goals

- Provide a structured closure helper for the "make durable, cleanup, remove"
  workflow.
- Preserve the current policy that specs are temporary delivery scaffolding and
  accepted behavior must be promoted to durable docs before closure.
- Keep human closure review explicit; the helper should organize and check the
  workflow, not silently close specs.
- Return concrete validation and recovery commands for the closure sequence.
- Automate deterministic closure mechanics where safe: final-spec commit lookup,
  closure-history entry generation, archive-index row generation, pending
  cleanup-hash replacement, and exact cleanup edit planning.
- Make the lifecycle tooling responsible for generating and maintaining the
  closure metadata fields it owns, while preserving durable Markdown records as
  the human-readable source of truth.
- Distinguish final-spec evidence from cleanup evidence so archive entries can
  reference the correct commits.
- Prove the removed or archived package no longer appears in active lifecycle
  inventory or active planning references.
- Capture residual risks, reload/adoption notes, and follow-up destinations as
  first-class closure metadata.

## Non-Goals

- Do not replace `closure_check`, `promotion_plan`, `archive_index`, or
  `sync_guard`; compose or extend existing lifecycle surfaces where possible.
- Do not make advisory hooks blocking.
- Do not close or remove any active spec automatically without an explicit user
  request.
- Do not let automation bypass human closure approval; write-capable actions
  must be preview-first, explicitly requested, and limited to deterministic
  closure files or package cleanup targets.
- Do not introduce broad lifecycle refactors outside the closure-helper surface.

## Requirements

### Requirement 1: Closure Workflow Checklist

**User Story:** As a maintainer, I want a closure helper to enumerate the
required closure steps, so that completed specs are closed consistently without
depending on session memory.

#### Acceptance Criteria

1. GIVEN an active spec package, WHEN the closure helper is requested, THEN THE
   SYSTEM SHALL report the ordered closure workflow: durable promotion review,
   final spec commit capture, package cleanup, closure-log update,
   archive-index update, post-cleanup metadata resolution, active-state
   verification, follow-up routing, and validation.
2. GIVEN a closure step has insufficient evidence, WHEN the helper reports the
   workflow, THEN THE SYSTEM SHALL mark that step as blocked or incomplete
   rather than treating the closure as ready.
3. GIVEN a closure step is deterministic and sufficient evidence is available,
   WHEN the helper reports the workflow, THEN THE SYSTEM SHALL identify whether
   that step can be scripted, previewed, or requires human judgment.

### Requirement 2: Durable Promotion Confirmation

**User Story:** As a maintainer, I want durable promotion targets checked before
cleanup, so that removed spec packages do not hide accepted behavior that never
landed in durable docs.

#### Acceptance Criteria

1. GIVEN a spec references durable destinations, WHEN the helper evaluates
   closure readiness, THEN THE SYSTEM SHALL identify the durable paths that need
   confirmation before cleanup.
2. GIVEN durable promotion is incomplete or unclear, WHEN closure guidance is
   returned, THEN THE SYSTEM SHALL keep the package cleanup step blocked until
   the missing durable outcome is resolved or explicitly waived.

### Requirement 3: Commit Evidence Separation

**User Story:** As a maintainer, I want final-spec and cleanup commits separated,
so that archive history points to both the completed package snapshot and the
actual package removal.

#### Acceptance Criteria

1. GIVEN a completed spec package, WHEN closure metadata is prepared, THEN THE
   SYSTEM SHALL distinguish the final spec commit from the cleanup commit.
2. GIVEN the cleanup commit is not available yet, WHEN the helper prepares
   closure guidance, THEN THE SYSTEM SHALL return a pending cleanup-commit
   placeholder instead of inventing a commit hash.
3. GIVEN a cleanup commit becomes available after package removal, WHEN closure
   metadata is reviewed, THEN THE SYSTEM SHALL identify every pending cleanup
   placeholder that must be replaced in the closure log, archive index, or other
   repository closure records.
4. GIVEN closure metadata contains a pending cleanup commit after cleanup, WHEN
   final closure validation is requested, THEN THE SYSTEM SHALL report that
   metadata resolution is incomplete.
5. GIVEN a final spec commit is required, WHEN the package exists in Git
   history, THEN THE SYSTEM SHALL discover and report the highest-confidence
   candidate commit that contains the complete active spec package before
   cleanup.
6. GIVEN multiple candidate final spec commits exist, WHEN the helper reports
   closure guidance, THEN THE SYSTEM SHALL present the candidates with evidence
   rather than choosing silently.

### Requirement 4: Follow-Up Routing

**User Story:** As a maintainer, I want unresolved work routed during closure,
so that residual risks and future work remain visible after the package is
removed.

#### Acceptance Criteria

1. GIVEN a spec has deferred work, residual risks, or rejected scope, WHEN
   closure guidance is returned, THEN THE SYSTEM SHALL route each item to a
   durable destination such as backlog, roadmap, ADR, runbook, or a follow-up
   spec recommendation.
2. GIVEN no follow-up work remains, WHEN closure guidance is returned, THEN THE
   SYSTEM SHALL state that explicitly rather than omitting the routing step.
3. GIVEN a closed spec has residual operational or adoption risks, WHEN closure
   metadata is prepared, THEN THE SYSTEM SHALL require those risks to be
   recorded in the closure record or routed to a durable follow-up destination.
4. GIVEN the closure affects installed tools, plugins, prompts, hooks, or other
   reload-sensitive surfaces, WHEN closure guidance is returned, THEN THE
   SYSTEM SHALL prompt for reload, reinstall, rollout, or adoption notes before
   closure metadata is considered complete.

### Requirement 5: Validation And Recovery Commands

**User Story:** As a maintainer, I want closure validation commands returned
with the workflow, so that a completed closure can be verified without
reconstructing the command sequence.

#### Acceptance Criteria

1. GIVEN closure guidance is returned, WHEN validation is required, THEN THE
   SYSTEM SHALL include repo-appropriate commands for scan, archive index,
   closure readiness, package contract or sync checks when applicable, and
   whitespace or test validation.
2. GIVEN MCP tools are unavailable, WHEN closure guidance is returned, THEN THE
   SYSTEM SHALL include equivalent `spec_runtime.py` recovery commands.
3. GIVEN closure metadata changes archive indexes, closure logs, package
   manifests, skill bundles, or tests, WHEN validation guidance is returned,
   THEN THE SYSTEM SHALL identify likely impacted validation surfaces rather
   than returning only generic lifecycle commands.
4. GIVEN validation commands are returned, WHEN a command can be executed
   safely as a read-only or deterministic check, THEN THE SYSTEM SHALL classify
   it as runnable by the helper or manual-only for the agent.

### Requirement 6: Active-State Removal Verification

**User Story:** As a maintainer, I want the helper to prove closed specs no
longer appear active, so that removed packages do not remain active through
backlog, indexes, or runtime inventory.

#### Acceptance Criteria

1. GIVEN a package cleanup is proposed or completed, WHEN active-state
   verification is requested, THEN THE SYSTEM SHALL check active spec inventory
   through MCP when available and through `spec_runtime.py scan` as a recovery
   path.
2. GIVEN a closed spec still appears in `docs/specs/`, backlog or roadmap
   active status, active sequencing docs, or other active lifecycle indexes,
   WHEN the helper reports closure state, THEN THE SYSTEM SHALL mark cleanup
   incomplete and name the stale active reference.
3. GIVEN only historical references remain in closure logs, archive indexes,
   tests, or durable follow-up notes, WHEN active-state verification is
   reported, THEN THE SYSTEM SHALL distinguish those historical references from
   stale active references.

### Requirement 7: Closure Metadata Completeness

**User Story:** As a maintainer, I want closure metadata checked as a complete
record, so that final reports include durable destinations, verification,
residual risks, follow-up work, and closure action consistently.

#### Acceptance Criteria

1. GIVEN closure metadata is prepared, WHEN the helper reviews it, THEN THE
   SYSTEM SHALL require spec ID, title, package path, final spec commit, cleanup
   commit or explicit pending state, closure action, durable destinations,
   verification summary, residual risks, and follow-up disposition.
2. GIVEN closure action is `removed`, `archived`, or `retained-as-history`, WHEN
   metadata is reviewed, THEN THE SYSTEM SHALL verify the package disposition
   matches that action and identify mismatches.
3. GIVEN a cleanup hash has been resolved, WHEN metadata validation is rerun,
   THEN THE SYSTEM SHALL report zero pending cleanup metadata before final
   closure is considered complete.

### Requirement 8: Preview-First Interface Boundary

**User Story:** As a maintainer, I want the helper to be preview-first by
default, so that scripted closure actions reduce toil without bypassing human
approval.

#### Acceptance Criteria

1. GIVEN the helper is used in v1, WHEN it prepares closure guidance, THEN THE
   SYSTEM SHALL return a preview of planned edits, blockers, validation
   commands, recovery commands, and any scriptable actions before mutation.
2. GIVEN a scriptable closure action is requested with explicit write intent,
   WHEN the helper performs that action, THEN THE SYSTEM SHALL limit mutation to
   declared closure targets and report the exact files changed.
3. GIVEN package deletion, archive movement, closure-log updates, archive-index
   updates, or cleanup-hash replacement are requested, WHEN the helper has
   sufficient evidence, THEN THE SYSTEM SHALL support those actions as
   scriptable candidates rather than forcing an agent to perform every edit
   manually.
4. GIVEN a closure action depends on judgment, WHEN the helper prepares a plan,
   THEN THE SYSTEM SHALL keep that action manual and explain the decision needed.
5. GIVEN future broader write-capable behavior is considered, WHEN design is
   prepared, THEN THE SYSTEM SHALL require explicit user intent, narrow file
   targets, rollback guidance, and validation evidence before that mutation mode
   is accepted.
6. GIVEN MCP tools are available, WHEN the helper is exposed to agents, THEN THE
   SYSTEM SHALL prefer an MCP-first or prompt-composed interface while keeping
   direct runtime commands as validation, CI, debugging, or no-MCP recovery
   paths only.

### Requirement 9: Scriptable Closure Mechanics

**User Story:** As a maintainer, I want repetitive closure edits generated or
performed by a helper, so that agents spend less effort on mechanical history
updates and more effort on closure judgment.

#### Acceptance Criteria

1. GIVEN closure metadata inputs are available, WHEN closure history is
   prepared, THEN THE SYSTEM SHALL generate the closure-log entry and
   archive-index row from one canonical metadata payload.
2. GIVEN the helper generates closure metadata, WHEN it reports the preview,
   THEN THE SYSTEM SHALL show the exact spec ID, title, package path, final
   spec commit, cleanup commit or pending placeholder, closure action, durable
   destinations, verification summary, residual risks, and follow-up text that
   will be written.
3. GIVEN package cleanup is approved, WHEN the helper prepares cleanup, THEN THE
   SYSTEM SHALL generate the exact package delete or archive operation and
   identify any active references that must be updated in the same closure
   slice.
4. GIVEN a cleanup commit hash is available after cleanup, WHEN metadata
   resolution is requested, THEN THE SYSTEM SHALL replace matching pending
   cleanup placeholders in the closure log and archive index from the discovered
   commit hash.
5. GIVEN generated edits are applied, WHEN validation is requested, THEN THE
   SYSTEM SHALL run or return the closure-specific validation sequence needed to
   prove the generated edits are consistent.

### Requirement 10: Durable Record Ownership

**User Story:** As a maintainer, I want lifecycle tooling to own generated
closure metadata consistently, so that closure records stay useful to humans
and machine checks without duplicate manual editing.

#### Acceptance Criteria

1. GIVEN closure metadata is generated, WHEN durable records are updated, THEN
   THE SYSTEM SHALL derive closure-log and archive-index content from one
   canonical metadata payload.
2. GIVEN the closure log and archive index both exist, WHEN the helper updates
   them, THEN THE SYSTEM SHALL treat the closure log as narrative human history
   and the archive index as the compact machine-verifiable lookup surface.
3. GIVEN a repository chooses a future single-record policy, WHEN design support
   is extended, THEN THE SYSTEM SHALL preserve the machine-verifiable fields
   currently provided by the archive index or route that policy to a follow-up
   spec.
4. GIVEN generated closure metadata is maintained by MCP/runtime tooling, WHEN
   manual edits drift from the canonical schema, THEN THE SYSTEM SHALL report
   validation diagnostics rather than silently accepting inconsistent records.

## Correctness Properties

- CP-001: The helper never reports cleanup-ready when durable promotion is
  unresolved.
- CP-002: The helper never invents a final spec commit or cleanup commit.
- CP-003: The helper preserves a durable route for every unresolved follow-up
  item before package cleanup is considered complete.
- CP-004: The helper never reports final closure complete while cleanup commit
  metadata remains pending.
- CP-005: The helper never treats historical closure/archive references as stale
  active references.
- CP-006: The helper never mutates closure files without explicit write intent
  and a previewed file target set.
- CP-007: The helper derives closure-log and archive-index updates from one
  canonical metadata payload.
- CP-008: The helper never silently chooses between multiple plausible final
  spec commits.
- CP-009: The helper keeps human narrative closure history and machine-readable
  archive lookup fields consistent when both records are present.

## Resolved Design Questions

- OQ-001: The helper should be dedicated MCP tools backed by shared helper
  logic. Prompts may guide humans, but prompts should not own closure behavior.
- OQ-002: Scriptable v1 actions are metadata rendering, package cleanup,
  pending-hash resolution, and validation planning. Durable adequacy,
  residual-risk acceptance, and final action approval remain manual judgment.
- OQ-003: Always-required validation includes scan, archive-index validation,
  relevant closure check, and `git diff --check`. Package-specific validation
  includes package contract, sync guard, npm validation, and focused MCP/runtime
  tests when touched surfaces require them.
- OQ-004: Active-reference classification should distinguish historical
  closure/archive/test references from active docs, backlog, roadmap, spec
  inventory, and sequencing references.
- OQ-005: MCP and runtime recovery surfaces may both exist, but both must call
  shared `lifecycle/closure.py` logic. MCP is preferred for agents; runtime
  commands remain validation, CI, debugging, and no-MCP recovery surfaces.
- OQ-006: Keep both the closure log and archive index in v1. The closure log is
  human narrative history; the archive index is compact machine-verifiable
  lookup. Retiring one requires a separate migration that preserves
  machine-verifiable fields.

These questions no longer block task and traceability drafting. They remain in
this artifact to preserve the requirements-to-design decision trail.

## Success Criteria

- A maintainer can request closure guidance for an active spec and receive a
  complete ordered workflow with blockers, evidence needs, follow-up routing,
  and validation commands.
- The helper keeps package cleanup blocked until durable promotion and closure
  metadata are ready.
- The helper reports post-cleanup metadata resolution, active-state removal
  verification, and residual-risk capture as explicit closure phases.
- The helper reduces manual closure actions by generating or applying
  deterministic closure-log, archive-index, cleanup, cleanup-hash, and
  validation steps from reviewed metadata.
- Requirements and design are accepted before tasks, traceability, and
  verification artifacts are created for this spec.
