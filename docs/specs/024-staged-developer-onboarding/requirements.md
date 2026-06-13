---
title: Staged developer onboarding requirements
doc_type: spec
artifact_type: requirements
status: active
owner: platform
last_reviewed: 2026-06-13
---

# Requirements

## Durable Source Baseline

- `skills/spec-lifecycle-manager/SKILL.md` defines the current lifecycle as
  durable docs -> active spec -> code/tests/config -> durable docs -> close
  spec, with `requirements.md`, `design.md`, and `tasks.md` as core artifacts.
- `skills/spec-lifecycle-manager/scripts/spec_runtime.py` and
  `skills/spec-lifecycle-manager/scripts/spec_mcp_server.py` provide the
  current tooling strength: deterministic scan, lint, preflight, summary,
  traceability, closure, prompt validation, review packets, and advisory hook
  support.
- `skills/spec-lifecycle-manager/prompts/` exposes lifecycle prompts, but there
  is no single first-run developer entry point that guides a new user through
  blank-repo bootstrapping, repository readiness, staged artifact creation, and
  next-action selection.
- CLU exploration identified useful workflow patterns to adapt, not packaging
  changes: staged requirements -> design -> task execution, foundation
  readiness, agent-facing pattern directives, sharper execution state,
  properties-to-tests traceability, numbered audit findings, separate history
  and release workflows, and a persistent starting point for first-time users.
- Packaging and discovery are out of scope because the current
  `spec-lifecycle-manager` packaging approach is accepted.

## Goals

- Add a clear first-run developer starting point for using the lifecycle skill
  and MCP tooling in an unfamiliar repository.
- Improve blank-repo bootstrap so the tool can create the minimum useful
  lifecycle/documentation foundation without assuming an architecture document
  must come first.
- Make staged artifact progression explicit: discover/readiness -> requirements
  -> design -> tasks -> implementation -> verification/promotion -> closure.
- Preserve and extend the current tooling-first strength instead of replacing it
  with prompt-only workflow instructions.
- Adopt all eight accepted CLU-inspired ideas in a repo-generic,
  lifecycle-manager-shaped way.
- Keep artifact creation demand-driven. The tool should recommend or create the
  next useful artifact, not generate every possible file up front.

## Non-Goals

- Do not change plugin packaging, install layout, repo-local discovery, or
  release packaging behavior.
- Do not make architecture the mandatory first step for every repository or
  every spec.
- Do not copy CLU's `.fndry/` folder model, fixed foundation file list, or
  old path assumptions.
- Do not weaken existing MCP/runtime validation, prompt validation, hook checks,
  traceability lookup, or closure tooling.
- Do not create write-capable tools outside the explicitly scoped lifecycle
  bootstrap/spec-edit surfaces designed by this spec.
- Do not force blank repositories into the full durable docs taxonomy before
  the user has confirmed the project shape.

## Accepted Ideas To Borrow

1. **Staged lifecycle flow:** requirements, design, tasks, implementation, and
   release/closure should be distinct stages with explicit readiness checks.
2. **First-run developer entry point:** a new user should have one obvious
   starting command/prompt/tool path that explains current repo readiness and
   next actions.
3. **Blank-repo bootstrap:** empty or near-empty repos need a lightweight
   bootstrap path before normal lifecycle scans can be useful.
4. **Foundation/readiness dashboard:** readiness should be deterministic,
   structured, and low-noise.
5. **Agent directives in durable docs:** durable guidance should include concise
   "before coding here" directives when the repo has enough evidence to support
   them.
6. **Execution state discipline:** selected work should be marked in progress,
   blockers should be explicit, one recovery attempt should be recorded, and
   completion should require evidence.
7. **Properties-to-tests traceability:** correctness properties and acceptance
   criteria should flow into test/validation tasks.
8. **Numbered audit/review findings:** review findings should have stable IDs,
   status, impact/effort, and extension behavior when they become durable work.

## Requirements

### Requirement 1: First-Run Lifecycle Entry Point

**User Story:** As a developer using the skill for the first time, I want one
entry point that tells me where I am and what to do next, so that I do not need
to understand every lifecycle artifact before getting useful guidance.

#### Acceptance Criteria

1. GIVEN a repository with existing docs and specs, WHEN first-run guidance is
   requested, THEN the system SHALL return current lifecycle readiness, active
   specs, missing or stale durable docs, available MCP/runtime tools, and the
   next recommended actions.
2. GIVEN a repository with no active specs, WHEN first-run guidance runs, THEN
   the system SHALL use durable docs, backlog, roadmap, closure log, and archive
   index instead of recreating removed packages.
3. IF the repository is blank or near blank, THEN the system SHALL enter
   bootstrap mode and propose the smallest useful foundation rather than failing
   because docs/specs do not exist.
4. WHERE MCP tools are available, THE SYSTEM SHALL use them as the primary
   readiness source and include the equivalent CLI commands for validation and
   recovery.
5. WHERE MCP tools are unavailable, THE SYSTEM SHALL provide the direct
   `spec_runtime.py` commands that recover equivalent read-only context.

### Requirement 2: Blank-Repo Bootstrap

**User Story:** As a developer starting a new repository, I want the lifecycle
manager to bootstrap only the useful initial docs and checks, so that a blank
repo can become lifecycle-ready without pretending architecture already exists.

#### Acceptance Criteria

1. GIVEN a repository with no `docs/` tree, WHEN bootstrap is requested, THEN
   the system SHALL propose a minimal docs root, an initial project summary or
   runbook target, and an optional first spec package.
2. WHERE the user has not confirmed the project purpose, THE SYSTEM SHALL ask
   for or record a project-purpose statement before generating durable
   structure.
3. IF no architecture evidence exists, THEN THE SYSTEM SHALL not require an
   architecture document before requirements work can start.
4. IF enough code or project structure exists to derive architecture or
   patterns, THEN THE SYSTEM SHALL recommend those as follow-up readiness
   artifacts rather than as mandatory first artifacts.
5. THE SYSTEM SHALL make every bootstrap write previewable before applying it.
6. THE SYSTEM SHALL keep bootstrap writes limited to documented lifecycle/docs
   paths unless the user explicitly asks for project source changes.

### Requirement 3: Staged Artifact Progression

**User Story:** As a spec author, I want each lifecycle stage to complete before
the next stage consumes it, so that requirements, design, tasks, and execution
do not blur together.

#### Acceptance Criteria

1. GIVEN a new spec request, WHEN staged flow is used, THEN the system SHALL
   create or update requirements before drafting design, and design before
   drafting tasks, unless the user explicitly chooses a design-first flow.
2. WHERE a design-first flow is chosen, THE SYSTEM SHALL record partial
   requirements and require a later requirements completion step before
   implementation readiness.
3. IF requirements change after design or tasks exist, THEN THE SYSTEM SHALL
   flag downstream review needs without silently rewriting downstream artifacts.
4. IF design changes after tasks exist, THEN THE SYSTEM SHALL flag task and
   traceability review needs before implementation continues.
5. THE SYSTEM SHALL expose stage readiness through MCP/runtime output, not only
   through prose in the skill.
6. THE SYSTEM SHALL keep optional artifacts optional and recommend them based on
   risk, durable-doc impact, or validation need.

### Requirement 4: Readiness Dashboard

**User Story:** As a maintainer, I want a deterministic readiness dashboard, so
that lifecycle health and missing foundations are visible without reading every
document manually.

#### Acceptance Criteria

1. WHEN readiness runs, THEN the system SHALL report repository docs readiness,
   active spec health, staged artifact status, durable promotion gaps, tooling
   availability, and recommended next actions.
2. WHERE a repo has established templates or governance docs, THE SYSTEM SHALL
   report template authority and governance constraints.
3. WHERE a repo lacks durable docs, THE SYSTEM SHALL distinguish missing,
   intentionally absent, optional, and not-yet-derivable docs.
4. IF active specs exist, THEN readiness SHALL summarize each spec's current
   stage, next blocking artifact, and relevant validation command.
5. IF no active specs exist, THEN readiness SHALL summarize backlog, roadmap,
   history, closure, and archive signals where present.
6. THE SYSTEM SHALL provide JSON-compatible output for MCP and CLI consumers.

### Requirement 5: Agent Directives In Durable Guidance

**User Story:** As an implementation agent, I want concise directives derived
from durable project evidence, so that I can fit the repository before writing
code.

#### Acceptance Criteria

1. WHEN a durable project guide, pattern guide, runbook, or architecture guide
   is created or promoted, THEN the system SHOULD support an optional
   agent-directives section.
2. WHERE directives are generated, THE SYSTEM SHALL derive them from actual
   repository docs, code patterns, governance, or user-confirmed project
   principles.
3. THE SYSTEM SHALL not invent architecture or coding directives for a blank
   repository.
4. THE SYSTEM SHALL keep directives concise enough for pre-implementation
   reading and route detail to the durable source document.
5. THE SYSTEM SHALL support review/audit findings that recommend directive
   additions without mutating the durable document automatically.

### Requirement 6: Execution State And Recovery Discipline

**User Story:** As a maintainer resuming implementation, I want task state,
blockers, recovery attempts, and evidence to be explicit, so that work does not
appear complete before it is verified.

#### Acceptance Criteria

1. WHEN an implementation slice starts, THEN the selected task or subtask SHALL
   be marked in progress before code or docs are changed.
2. WHEN a task fails, THEN the system SHALL record one meaningfully different
   recovery attempt before reporting a blocker.
3. IF recovery fails, THEN the system SHALL record task state, blocker details,
   exact error evidence, and the specific decision or input needed.
4. IF recovery succeeds and the lesson is reusable, THEN the system SHALL offer
   a durable gotcha, runbook, or troubleshooting promotion target.
5. THE SYSTEM SHALL keep checkpoint validation scoped to the implementation
   slice while still recording when broader validation was not run.
6. THE SYSTEM SHALL not mark a task complete without evidence that satisfies its
   acceptance criteria.

### Requirement 7: Properties-To-Tests Traceability

**User Story:** As a reviewer, I want correctness properties and acceptance
criteria carried into task and verification evidence, so that validation
coverage can be checked before implementation and closure.

#### Acceptance Criteria

1. GIVEN requirements with correctness properties, WHEN design and tasks are
   drafted, THEN each property SHALL be mapped to design behavior and at least
   one validation task or explicit non-automated verification method.
2. WHERE acceptance criteria are not covered by tasks or verification, THE
   SYSTEM SHALL report the coverage gap before implementation readiness.
3. IF a repository lacks a property-test dependency path, THEN THE SYSTEM SHALL
   allow conventional tests or documented manual verification without requiring
   a new dependency.
4. THE SYSTEM SHALL expose coverage gaps through lint/preflight/runtime output.
5. THE SYSTEM SHALL preserve stable property IDs and traceability references
   through requirements, design, tasks, and verification.

### Requirement 8: Numbered Review Findings

**User Story:** As a maintainer turning reviews into work, I want durable
findings with stable IDs and status, so that audits can be extended and acted on
without losing references.

#### Acceptance Criteria

1. WHEN a review or audit is persisted, THEN the system SHALL support stable
   finding IDs, status, severity or impact, effort where useful, source
   evidence, and recommended routing.
2. WHEN an existing review is extended, THEN new findings SHALL receive new IDs
   without renumbering existing findings.
3. WHEN a finding is resolved or deferred, THEN the system SHALL preserve the
   original entry and add resolution or routing evidence.
4. WHERE a finding changes durable behavior, THE SYSTEM SHALL route it to a
   spec, backlog, roadmap, issue, or durable doc promotion target.
5. THE SYSTEM SHALL distinguish findings-only reviews from implementation
   tasks.

## Correctness Properties

- CP-001: Readiness output SHALL be deterministic for the same repository state.
- CP-002: First-run guidance SHALL not mutate files unless the user explicitly
  requests bootstrap or spec creation.
- CP-003: Bootstrap writes SHALL be limited to previewed lifecycle/docs paths.
- CP-004: Staged readiness SHALL never classify implementation as ready when
  requirements, design, or task traceability has unresolved blocking gaps.
- CP-005: Optional artifacts SHALL remain optional unless risk, durable-doc
  impact, or validation needs make them necessary for the current work.
- CP-006: Agent directives SHALL be evidence-derived or user-confirmed, never
  invented from a blank repository.
- CP-007: Tooling additions SHALL preserve existing MCP/CLI scan, lint,
  preflight, traceability, prompt-validation, hook, and closure behavior.
- CP-008: Packaging behavior SHALL remain unchanged by this spec.

## Success Criteria

- A first-time developer can invoke one documented entry point and receive
  repository readiness, available tooling, and next lifecycle actions.
- Blank and near-blank repositories receive preview-first bootstrap guidance
  instead of architecture-first failure.
- New and resumed specs expose staged readiness through runtime/MCP output.
- Requirements properties and acceptance criteria produce visible task or
  verification coverage before implementation readiness.
- Existing MCP/CLI validation, prompt validation, advisory hooks, closure
  checks, and bundle parity behavior continue to pass.
- No packaging, plugin discovery, or install-layout behavior changes are made.
