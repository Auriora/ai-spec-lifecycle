---
title: Spec closure helper design
doc_type: spec
artifact_type: design
status: draft
authoring_mode: wizard
lifecycle_stage: tasks
owner: platform
last_reviewed: 2026-07-05
---

# Technical Design

## Overview

Add a preview-first closure helper that reduces the number of mechanical steps
an agent must perform to close a completed spec. The helper does not replace
closure judgment. It separates judgment-heavy checks, such as durable promotion
adequacy and residual-risk acceptance, from deterministic closure mechanics
that can be generated, validated, or applied with explicit write intent.

The implementation should live in a shared import-only module so MCP and
retained runtime recovery use one code path:

- MCP is the preferred agent-facing surface for normal Codex/Claude sessions.
- `spec_runtime.py` may expose a retained recovery/CI command over the same
  shared implementation.
- No separate script should own different closure behavior.

The first version should support a three-phase closure flow:

1. `plan`: inspect an active spec and produce blockers, closure metadata,
   candidate commits, active references, validation commands, and scriptable
   actions.
2. `apply-cleanup`: with explicit write intent, update deterministic closure
   records with a pending cleanup hash and remove or archive the package.
3. `resolve-cleanup`: after the cleanup commit exists, replace matching pending
   cleanup hashes and rerun closure/archive validation.

The design keeps both durable records for v1. They serve different consumers:
`docs/history/spec-closure-log.md` is the narrative closure history for humans,
while `docs/history/spec-archive-index.md` is the compact lookup table used by
runtime checks. The helper owns generation and validation of the fields it
writes to both records. That does not make MCP the durable source of truth; it
makes MCP/runtime the maintained interface for producing consistent durable
records from one canonical metadata payload.

## Requirement Coverage

- Requirement 1, AC1-AC3: `closure_plan` contains ordered phases, step status,
  evidence gaps, and action classification: scriptable, preview-only, or
  manual judgment.
  - Validation: unit tests for step ordering, status, and action
    classification.
- Requirement 2, AC1-AC2: durable destinations are collected from
  `promotion_plan`, verification evidence, closure metadata, and known closure
  history fields. Cleanup remains blocked when durable evidence is missing or
  waived without rationale.
  - Validation: fixture tests for complete, missing, and waived durable
    promotion.
- Requirement 3, AC1-AC6: commit discovery reports final-spec commit
  candidates, separates cleanup commit state, writes pending placeholders only
  in cleanup preview/apply, and resolves placeholders after cleanup.
  - Validation: Git fixture tests for candidate discovery, pending
    placeholders, and resolution.
- Requirement 4, AC1-AC4: residual risks, reload/adoption notes, deferred work,
  and follow-up routes are explicit metadata fields with completeness checks.
  - Validation: metadata validation tests and closure-log rendering tests.
- Requirement 5, AC1-AC4: validation command planning returns repo-appropriate
  commands with runnable/manual classification and impacted surfaces.
  - Validation: tests for package repo, ordinary repo, MCP unavailable, and
    history-only closure changes.
- Requirement 6, AC1-AC3: active-reference scanning distinguishes active
  package references from historical references in closure logs, archive
  indexes, tests, and durable follow-up notes.
  - Validation: fixture tests for stale active backlog/docs references versus
    historical references.
- Requirement 7, AC1-AC3: `ClosureMetadata` validates required fields,
  status/action consistency, and zero pending cleanup hashes for final
  completion.
  - Validation: metadata validation tests and archive-index integration tests.
- Requirement 8, AC1-AC6: MCP tools and runtime recovery commands default to
  dry-run/preview. Mutating actions require explicit write intent and scoped
  action names.
  - Validation: MCP and runtime tests for dry-run default, write-intent guard,
    and changed-file reporting.
- Requirement 9, AC1-AC5: closure-log entry and archive-index row render from
  one canonical metadata payload; cleanup and cleanup-hash edits are generated
  from the same model.
  - Validation: snapshot-style rendering tests plus round-trip archive-index
    validation.
- Requirement 10, AC1-AC4: v1 keeps the closure log and archive index but
  defines ownership: closure log is narrative, archive index is machine lookup,
  both are generated from one metadata payload and validated for drift.
  - Validation: rendering, archive-index, and drift-detection tests.

## Correctness Property Coverage

- CP-001: `plan` marks cleanup blocked until durable promotion is complete or
  explicitly waived. Waivers must be recorded in metadata.
  - Validation: unit tests with missing promotion targets.
- CP-002: commit fields are discovered from Git or provided by the user;
  unknown cleanup hashes are represented as `pending`; multiple candidates
  remain explicit.
  - Validation: Git fixture tests and metadata validation.
- CP-003: follow-up and residual-risk fields are required for completion;
  `none` is valid only when explicit.
  - Validation: metadata completeness tests.
- CP-004: final completion requires zero pending cleanup placeholders after the
  cleanup commit exists.
  - Validation: archive-index and closure-log tests.
- CP-005: active-reference scanning classifies reference context before
  blocking; historical references do not block.
  - Validation: reference classifier fixture tests.
- CP-006: mutations require explicit action and write intent; dry-run remains
  the default.
  - Validation: MCP/runtime write guard tests.
- CP-007: closure-log and archive-index rendering use the same
  `ClosureMetadata`.
  - Validation: rendering and round-trip tests.
- CP-008: candidate final commits are reported with evidence and never chosen
  silently.
  - Validation: Git candidate tests.
- CP-009: dual durable records remain consistent when generated or validated by
  the helper.
  - Validation: closure-log/archive-index consistency tests.

## High-Level Design

### System Architecture

```text
Agent
  |
  | preferred closure interface
  v
MCP server
  |-- closure_plan
  |-- closure_apply
  |-- closure_resolve
  |
  | shared Python calls
  v
lifecycle/closure.py
  |-- plan workflow
  |-- metadata model and validation
  |-- plan and action identifiers
  |-- final spec commit discovery
  |-- closure-log/archive-index rendering
  |-- durable record drift detection
  |-- cleanup edit planning
  |-- planned-edit transaction checks
  |-- pending cleanup hash resolution
  |-- active-reference classification
  |-- validation command planning
  |
  v
Existing lifecycle modules
  |-- lifecycle/core.py scan, promotion, closure, archive, sync helpers
  |-- lifecycle/runtime_adapter.py retained runtime command adapter
  |-- docs/history/spec-closure-log.md
  |-- docs/history/spec-archive-index.md
  |-- docs/specs/[id]/

No-MCP recovery / CI
  |
  v
spec_runtime.py closure-plan / closure-apply / closure-resolve
  |
  v
same lifecycle/closure.py implementation
```

The helper should be added as a small closure-specific module rather than
expanding `lifecycle/core.py` further. `core.py` may expose compatibility
wrappers for MCP/runtime dispatch, but the closure-specific algorithms and data
models should live in `lifecycle/closure.py`. Adapter layers must not duplicate
closure planning, metadata rendering, active-reference classification, or
cleanup-hash resolution logic.

### Components and Changes

- `skills/spec-lifecycle-manager/scripts/lifecycle/closure.py`
  - New import-only module for closure helper logic.
  - Owns data models, planning, rendering, edit planning, active-reference
    classification, and cleanup-hash resolution.
  - Owns generation and validation for closure-log sections and archive-index
    rows created by the helper.
- `skills/spec-lifecycle-manager/scripts/lifecycle/core.py`
  - Adds thin wrapper functions for closure helper entrypoints if needed by
    existing MCP/runtime dispatch style.
  - Reuses existing `scan_specs`, `promotion_plan`, `closure_check`,
    `archive_index`, and `sync_guard` helpers.
- `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py`
  - Adds MCP tools for preview and guarded write actions.
  - Keeps dry-run/preview behavior as default.
- `skills/spec-lifecycle-manager/SKILL.md`
  - Updates the MCP access contract so `closure_apply` and `closure_resolve`
    are documented as narrow write-capable exceptions alongside
    `set_task_state`.
  - Keeps lifecycle judgment, durable-promotion approval, and final closure
    approval outside the MCP tool contract.
- `skills/spec-lifecycle-manager/scripts/lifecycle/runtime_adapter.py`
  - Adds retained recovery commands over the same shared helper.
- `docs/reference/spec-lifecycle-runtime.md`
  - Documents MCP-first usage, runtime recovery commands, guarded
    write-capable closure tools, and closure action phases.
- `plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/`
  - Mirrors skill, prompt, reference, runtime, and MCP changes into the bundled
    Codex plugin copy.
- `plugins/spec-lifecycle-manager/claude-plugin/skills/spec-lifecycle-manager/`
  - Mirrors the same changes into the bundled Claude plugin copy.
- `tests/runtime/test_spec_runtime.py`
  - Adds CLI/recovery coverage and shared helper unit tests.
- `tests/runtime/test_spec_mcp_server.py`
  - Adds MCP tool schema, dry-run, write-intent, and structured response tests.

### Data Models

```text
ClosureMetadata:
  spec_id: string
  title: string
  package_path: repo-relative path
  status: removed | archived | retained_as_history
  closure_action: removed | archived | retained-as-history
  final_spec_commit: string | pending
  cleanup_commit: string | pending
  durable_destinations: list[path-or-reference]
  verification_summary: string
  residual_risks: list[string]
  follow_ups: list[FollowUp]
  closed_by: string
  closed_date: ISO date

ClosurePlan:
  plan_id: stable string
  generated_at: ISO datetime
  repo_root: repo-relative root marker
  spec_path: repo-relative path
  metadata: ClosureMetadata
  steps: list[ClosureStep]
  actions: list[ClosureAction]
  planned_edits: list[PlannedEdit]
  validation_commands: list[ValidationCommand]
  preconditions: list[FilePrecondition]

ClosureStep:
  id: string
  label: string
  status: ready | blocked | complete | manual | not_applicable
  action_kind: scriptable | preview_only | manual_judgment
  blockers: list[Diagnostic]
  evidence: list[EvidenceRef]

ClosureAction:
  action_id: stable string
  action_type: render_records | cleanup_package | resolve_cleanup_hash | update_active_reference | run_validation
  mode: preview | write
  requires_write_intent: boolean
  planned_edit_ids: list[string]
  manual_decision: string | none

CandidateCommit:
  commit: string
  subject: string
  date: string
  evidence: list[string]
  confidence: high | medium | low

PlannedEdit:
  edit_id: stable string
  path: repo-relative path
  action: add | update | delete | move
  reason: string
  preview: string | structured diff summary
  precondition: FilePrecondition

FilePrecondition:
  path: repo-relative path
  exists: boolean
  content_hash: string | none
  required_snippet: string | none

ValidationCommand:
  command: string
  reason: string
  runnable_by_helper: boolean
  required: boolean
  phase: plan | cleanup | resolve | final
```

The canonical payload is `ClosureMetadata`, carried by a `ClosurePlan` with
stable action and edit IDs. Closure-log and archive-index rendering should be
derived from that payload so the two durable records cannot drift. External MCP
and runtime calls may serialize metadata as dictionaries or JSON files, but the
shared implementation must parse and validate them into typed internal objects
before planning or applying edits.

Status and action values intentionally mirror the durable archive index:

- `status=removed` maps to `closure_action=removed`; the package path no longer
  exists in the active tree after the cleanup commit.
- `status=archived` maps to `closure_action=archived`; the package has moved to
  an explicit archive/history path.
- `status=retained_as_history` maps to `closure_action=retained-as-history`;
  the package remains visible only by explicit policy exception and must be
  marked historical, archived, or superseded.

The implementation should reject any other status/action combination unless a
future spec extends the durable archive-index schema.

### Data Flow

#### Plan Flow

1. Resolve repo root and spec package.
2. Run or consume active-spec scan and closure check.
3. Build durable promotion evidence from `promotion_plan`, spec artifacts,
   task evidence, and existing durable references.
4. Discover final spec commit candidates from Git history.
5. Generate closure metadata with pending cleanup hash.
6. Classify active references and historical references.
7. Build closure-log and archive-index previews.
8. Build cleanup edit preview.
9. Build validation command plan.
10. Attach file-content preconditions for every planned edit.
11. Return blockers, manual decisions, scriptable actions, stable action IDs,
    plan ID, and exact edit targets.

#### Cleanup Flow

1. Require explicit action and write intent.
2. Recompute or load the referenced plan and fail if blockers remain.
3. Verify every file precondition for the selected action.
4. Build all selected edits in memory before writing.
5. Apply the bounded edit batch only after all preconditions pass.
6. Write closure-log and archive-index entries with `cleanup_commit: pending`.
7. Remove or archive the spec package according to approved action.
8. Apply deterministic active-reference updates only when explicitly requested
   and included in the preview.
9. Return changed files, next commit instruction, post-cleanup validation, and
   manual rollback guidance if an unexpected write failure occurs.

#### Resolve Flow

1. Require explicit action and write intent.
2. Discover the cleanup commit from `HEAD` or a provided commit hash.
3. Verify file preconditions for closure records.
4. Replace matching pending cleanup placeholders in closure records.
5. Update tests or known count fixtures only when they are explicit planned
   edits and validation indicates they must change.
6. Return changed files and final validation commands.

## Low-Level Design

### Algorithms and Logic

#### Final Spec Commit Discovery

```text
function discover_final_spec_commits(repo_root, spec_path):
    commits = git log --follow -- spec_path
    candidates = []
    for commit in commits newest first:
        tree_has_package = git ls-tree commit spec_path has files
        if tree_has_package:
            evidence = inspect expected artifacts at commit
            confidence = high if commit contains complete package artifacts and closure readiness evidence
            candidates.append(commit, evidence, confidence)
    return candidates
```

The helper should report the highest-confidence candidate containing the
complete package, not simply the latest commit touching the path. It must not
silently choose when multiple plausible candidates exist. A caller may provide
the final spec commit explicitly.

#### Metadata Rendering

```text
function render_closure_records(metadata):
    parse and validate ClosureMetadata
    closure_log_entry = render markdown section(metadata)
    archive_index_row = render table row(metadata)
    return planned edits for both files
```

Rendering should preserve existing closure-log and archive-index formatting.
Insertion order should put the newest closure at the top of each entries
section.

#### Durable Record Ownership

```text
function validate_owned_closure_records(metadata, closure_log, archive_index):
    compare generated closure-log fields with durable section
    compare generated archive-index row with durable row
    report missing, pending, invalid, or inconsistent owned fields
```

The helper owns the generated fields for records it creates or resolves:
spec ID, title, package path, final spec commit, cleanup commit, closure
action, durable destinations, verification pointer, residual-risk/follow-up
presence, and closure status. It should not own arbitrary prose outside the
generated closure section.

The archive index remains useful in v1 because it is compact and machine
oriented. The closure log remains useful because it captures narrative
verification summaries and residual risks. A future single-record policy can be
considered later, but it must preserve the archive index's machine-verifiable
fields before the separate index can be retired.

#### Active Reference Classification

```text
function classify_spec_references(spec_id, package_path):
    for match in rg(spec_id or package_path):
        if path is docs/history/spec-closure-log.md:
            class = historical
        elif path is docs/history/spec-archive-index.md:
            class = historical
        elif path is tests and assertion references archive history:
            class = historical_or_validation
        elif context says active, promoted, current task, next task, or docs/specs:
            class = active_stale
        else:
            class = review
    return grouped references
```

Only `active_stale` references block cleanup. Historical references remain as
closure evidence.

Generated mutations from reference classification are narrower than detection.
The classifier may report all likely references, but write actions may update
only known structured surfaces or exact previewed replacements with matching
file preconditions. Ambiguous references remain manual review items.

#### Planned Edit Application

```text
function apply_planned_edits(plan, action_id, write_intent):
    require write_intent
    select action by stable action_id
    verify plan is fresh enough or all file preconditions match
    build every replacement in memory
    if any precondition fails:
        abort without writing
    write files in deterministic order
    return changed files and recovery notes
```

This is not a full database transaction, but it avoids partial writes caused by
known stale inputs. If the process fails during filesystem writes, the returned
recovery notes should name changed files and the validation command sequence.

#### Validation Planning

```text
function build_validation_plan(repo_root, changed_files, phase):
    always include scan and archive-index validation for closure phases
    include closure-check before cleanup while package exists
    include package-contract/sync-guard if skill or plugin files changed
    include focused runtime/MCP tests if lifecycle scripts changed
    include archive-index fixture tests if history files changed
    include git diff --check for every phase
```

Validation commands should include MCP preferred tools when available and
`spec_runtime.py` recovery commands for CI/no-MCP contexts.

### Function Signatures and Interfaces

```text
def closure_plan(
    spec_path: Path,
    *,
    repo_root: Path | None = None,
    final_spec_commit: str | None = None,
    closure_action: str = "removed",
    include_reference_scan: bool = True,
) -> dict[str, Any]

def closure_apply(
    spec_path: Path,
    *,
    repo_root: Path | None = None,
    plan: ClosurePlan | dict[str, Any],
    action_id: str,
    dry_run: bool = True,
    write_intent: bool = False,
) -> dict[str, Any]

def closure_resolve(
    repo_root: Path,
    *,
    spec_id: str,
    cleanup_commit: str | None = None,
    dry_run: bool = True,
    write_intent: bool = False,
) -> dict[str, Any]
```

The public function may accept serialized dictionaries at the boundary, but the
first internal step must parse and validate a `ClosurePlan` and
`ClosureMetadata`. The rest of the implementation should use typed internal
objects.

MCP tools should expose the same conceptual interface:

```text
closure_plan(spec_path, final_spec_commit?, closure_action?)
closure_apply(spec_path, plan, action_id, dry_run=true, write_intent=false)
closure_resolve(spec_id, cleanup_commit?, dry_run=true, write_intent=false)
```

The runtime recovery interface should mirror those names under
`spec_runtime.py`, for example:

```bash
skills/spec-lifecycle-manager/scripts/spec_runtime.py closure-plan docs/specs/029-example
skills/spec-lifecycle-manager/scripts/spec_runtime.py closure-apply docs/specs/029-example --plan-file closure-plan.json --action-id cleanup_package --write-intent
skills/spec-lifecycle-manager/scripts/spec_runtime.py closure-resolve . --spec-id 029-example --cleanup-commit HEAD --write-intent
```

### Error Handling

- Missing spec package: return an error diagnostic with no planned edits.
- Closure blockers: return `blocked` steps and no mutating actions.
- Missing final spec commit: return candidate discovery diagnostics and require
  explicit selection.
- Multiple final spec candidates: mark commit selection as manual judgment.
- Pending cleanup metadata during final validation: return an error or blocking
  diagnostic.
- Write requested without `write_intent`: return a write-intent error and do
  not mutate files.
- Planned edit conflict: return changed-file diagnostics and require a fresh
  plan.
- Stale plan: return precondition diagnostics and require `closure_plan` to be
  rerun.
- Partial write failure: return changed files, intended files, and manual
  recovery validation commands.
- Git unavailable: return recovery guidance that commit discovery must be
  supplied manually.

### Security, Trust, and Access

The helper operates on local repository files and Git history. It should not
access network services or secrets. Mutating actions are limited to declared
repo-relative closure targets:

- selected spec package path;
- `docs/history/spec-closure-log.md`;
- `docs/history/spec-archive-index.md`;
- explicitly planned active-reference files such as backlog or roadmap docs;
- explicitly planned validation fixture updates when required.

Paths must be normalized under the repository root. The helper must reject
absolute paths outside the repository and path traversal. Dry-run is the
default for MCP and runtime recovery.

Write actions must verify file preconditions from the previewed plan. They
should reject stale plans rather than merging over unexpected edits.

### Migration and Compatibility

Existing `closure_check`, `promotion_plan`, `archive_index`, and `sync_guard`
remain valid. The helper composes them and adds a higher-level orchestration
surface. Existing closure workflows continue to work manually.

The MCP tool names are additive. The runtime recovery commands are additive. No
existing CLI command is removed in this spec.

This spec intentionally changes the current MCP write-capability contract. The
implementation must update durable guidance that currently says `set_task_state`
is the only write-capable MCP tool and that MCP never edits durable docs,
archives packages, or removes files. The updated guidance should describe the
closure helper as a second narrow exception: preview-first, explicit
write-intent, limited to declared closure targets, and still unable to make
closure judgment or commit changes.

### Slice Boundary And Residual Architecture

- Preview-first closure planning:
  - In this slice: shared helper, MCP tool, runtime recovery command, and tests.
  - Out of this slice: fully autonomous closure without review.
  - Follow-up destination: none.
  - Blocks closure: yes.
- Deterministic closure metadata generation:
  - In this slice: closure-log and archive-index rendering from one payload.
  - Out of this slice: arbitrary repository-specific history formats beyond
    documented fallbacks.
  - Follow-up destination: backlog if needed.
  - Blocks closure: no.
- Package cleanup scripting:
  - In this slice: delete or archive the selected spec package with explicit
    write intent.
  - Out of this slice: remote issue tracker updates or external project-board
    changes.
  - Follow-up destination: future backlog or issue-integration spec.
  - Blocks closure: no.
- Cleanup hash resolution:
  - In this slice: replace pending cleanup hashes in the closure log and archive
    index.
  - Out of this slice: rewriting old historical closure entries except the
    selected pending entry.
  - Follow-up destination: none.
  - Blocks closure: yes.
- Active-reference classification:
  - In this slice: backlog, roadmap, `docs/specs`, history, tests, common
    lifecycle docs, and mutation only for known or exact-previewed replacements.
  - Out of this slice: semantic understanding of every project-specific planning
    system.
  - Follow-up destination: backlog if needed.
  - Blocks closure: no.
- Validation command planning:
  - In this slice: repo-local lifecycle, package, and test commands with
    runnable/manual classification.
  - Out of this slice: running expensive or external CI-only validation locally.
  - Follow-up destination: verification waiver or follow-up.
  - Blocks closure: no.
- Durable record ownership:
  - In this slice: generate and validate owned closure-log/archive-index fields
    from one payload.
  - Out of this slice: retiring the archive index or converting history to a
    single record.
  - Follow-up destination: follow-up spec if desired.
  - Blocks closure: no.

## Validation Strategy

- Unit tests for `closure_plan` with complete and blocked specs:
  - Covers: Requirements 1, 2, 4, and 7.
  - Evidence location: `tests/runtime/test_spec_runtime.py` or focused closure
    tests.
  - Residual risk: none.
- Git fixture tests for final spec commit candidates:
  - Covers: Requirement 3, CP-002, and CP-008.
  - Evidence location: runtime tests.
  - Residual risk: fixture Git history may not cover every merge pattern.
- Rendering tests for closure-log and archive-index output:
  - Covers: Requirements 7 and 9, CP-007.
  - Evidence location: runtime tests.
  - Residual risk: Markdown formatting changes need fixture refresh.
- Write-intent guard tests for MCP and runtime commands:
  - Covers: Requirement 8 and CP-006.
  - Evidence location: MCP/runtime tests.
  - Residual risk: none.
- Active-reference classifier tests:
  - Covers: Requirement 6 and CP-005.
  - Evidence location: runtime tests.
  - Residual risk: project-specific planning docs may need future patterns.
- Stale-plan/precondition tests:
  - Covers: Requirements 8 and 9, CP-006.
  - Evidence location: runtime and MCP tests.
  - Residual risk: none.
- Durable record ownership drift tests:
  - Covers: Requirement 10 and CP-009.
  - Evidence location: archive-index and closure-log tests.
  - Residual risk: none.
- End-to-end dry-run using spec 030 closure history fixture:
  - Covers: Requirements 1-9.
  - Evidence location: runtime test fixture based on spec 030 records.
  - Residual risk: must avoid mutating real history in tests.
- Package validation:
  - Covers: bundle/install parity with `package-contract`, `sync-guard`, and
    `npm run validate`.
  - Evidence location: verification evidence.
  - Residual risk: already-running plugin sessions may need reload.

## Downstream Task Guidance

- Draft tasks only after this design is reviewed.
- Tasks should be split by implementation layer: shared helper model, planning,
  rendering, write-intent application, MCP surface, runtime recovery surface,
  tests, docs, bundle sync, and closure evidence.
- Tasks must include fixtures for spec 030-like closure flows.
- Traceability should be created with tasks because the requirements now span
  read-only planning, guarded writes, Git history, closure metadata, validation,
  and MCP/runtime boundaries.
- Verification expectations should be represented in tasks and traceability
  during task planning. Create or update `verification.md` when implementation
  evidence exists, because closure correctness depends on staged evidence before
  cleanup, after cleanup, and after cleanup hash resolution.

## Operational Considerations

The helper should reduce closure toil but cannot remove the need for human
review. Operators must still decide whether durable promotion is complete,
whether residual risks are acceptable, and whether the package should be
removed, archived, or retained as history.

For this repository, package or skill changes require bundle sync and installed
cache refresh before already-running agents see the new behavior. Closure
metadata should continue to record that reload/adoption risk when relevant.

## Open Questions

No open questions remain for task drafting. The requirements-stage questions
are resolved by the design decisions below.

### Resolved Design Questions

- OQ-001: add dedicated MCP tools backed by shared helper logic. Prompts may
  guide humans but should not own behavior.
  - Blocks tasks: no.
- OQ-002: scriptable v1 actions are metadata rendering, package cleanup,
  pending-hash resolution, and validation planning. Durable adequacy,
  residual-risk acceptance, and final action approval remain manual judgment.
  - Blocks tasks: no.
- OQ-003: always-required validation includes scan, archive-index validation,
  relevant closure check, and `git diff --check`. Package-specific validation
  includes package contract, sync guard, npm validation, and focused MCP/runtime
  tests when touched surfaces require them.
  - Blocks tasks: no.
- OQ-004: use path and context classification. Historical closure, archive, and
  test references do not block; active docs, backlog, roadmap, and spec
  inventory references do.
  - Blocks tasks: no.
- OQ-005: MCP and runtime recovery surfaces may both exist, but both must call
  `lifecycle/closure.py`. MCP is preferred and runtime is recovery/CI.
  - Blocks tasks: no.
- OQ-006: keep both the closure log and archive index in v1. The closure log is
  human narrative history; the archive index is compact machine lookup. The
  helper owns generated fields across both. Retiring one requires a separate
  migration that preserves machine-verifiable fields.
  - Blocks tasks: no.

## Related Artifacts

- Requirements: `docs/specs/029-spec-closure-helper/requirements.md`
- Durable closure log: `docs/history/spec-closure-log.md`
- Durable archive index: `docs/history/spec-archive-index.md`
- Runtime reference: `docs/reference/spec-lifecycle-runtime.md`
- Tasks: `docs/specs/029-spec-closure-helper/tasks.md`
- Traceability: `docs/specs/029-spec-closure-helper/traceability.md`
- Verification: planned by tasks; not yet created
