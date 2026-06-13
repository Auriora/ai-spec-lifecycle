---
title: Agent development lifecycle backlog
doc_type: backlog
status: active
owner: platform
last_reviewed: 2026-06-13
---

# Backlog

Track cross-spec follow-up work that is not ready for a focused implementation
spec or that should not block the active spec currently being delivered.

## Items

| ID | Status | Topic | Source | Notes |
|----|--------|-------|--------|-------|
| B001 | done | Backlog and roadmap templates | MCP implementation discussion; archive index entry `006-backlog-roadmap-templates` | Durable templates and skill guidance added for backlog and roadmap docs, including routing deferred spec work to `docs/backlog/`, `docs/roadmap/`, issue trackers, or follow-up specs. |
| B002 | done | Agent Workbench MCP packaging and hook install | Archive index entries `007-spec-lifecycle-mcp-server` and `008-agent-workbench-spec-lifecycle-install` | Host-level companion MCP install policy, Agent Workbench reference guidance, advisory-only hook policy, and validation checklist completed. |
| B003 | done | Spec archive index and closure-log runtime support | User request for Git-backed spec archives; archive index entries `005-spec-closure-log-management` and `011-spec-archive-index-runtime` | Runtime now validates archive index and closure-log consistency and exposes read-only MCP access. |
| B004 | done | Blocking lifecycle hooks | Archive index entry `010-codex-hook-dogfood`; external verification feedback; R002 | Decision: keep lifecycle hooks advisory-only. Any future blocking hook proposal must be opened as a new focused spec with false-positive handling, rollback path, and explicit approval. |
| B005 | done | Coding agent operating model governance adoption | `docs/design/coding-agent-operating-model.md`; archive index entry `012-operating-model-governance-adoption` | Selected hard operating-model rules adopted into `docs/governance/constitution.md`; flexible workflow mechanics remain durable design guidance. |
| B006 | superseded | Archived spec audit report | Archived scan hygiene work; user decision to remove completed specs | Superseded by removal-by-default policy. Historical spec packages should not remain in the active docs tree just to support audit reports. |
| B007 | done | Agent readiness packet | Archive index entry `013-agent-backed-lifecycle-tools`; `docs/reference/spec-lifecycle-runtime.md`; `skills/spec-lifecycle-manager/scripts/spec_runtime.py` | Runtime and MCP expose `agent_readiness_packet` with task, traceability, required-review, guardrail, MCP-first interface, and validation command context. |
| B008 | active | Closure risk review | Archive index entry `013-agent-backed-lifecycle-tools`; `docs/reference/spec-lifecycle-runtime.md`; review packet runtime; active spec `021-closure-risk-review` | Use deterministic closure, promotion, validation, and evidence signals to flag missing durable promotion, weak evidence, unresolved decisions, risky follow-ups, and closure blockers before package closure. |
| B009 | candidate | Draft traceability matrix | Archive index entry `013-agent-backed-lifecycle-tools`; traceability runtime and templates | Generate a proposed traceability matrix from requirements, design, tasks, change impact, and verification, then validate references deterministically. |
| B010 | candidate | Durable doc drift review | Archive index entry `013-agent-backed-lifecycle-tools`; durable-doc promotion runtime | Compare durable docs against relevant code, config, tests, or runtime contracts and report suspected drift for lead-agent review. |
| B011 | candidate | Decision extractor | Archive index entry `013-agent-backed-lifecycle-tools`; governance and open-decision docs | Scan specs and durable docs for implicit decisions that should become ADRs, open decisions, backlog items, roadmap items, or explicit no-action notes. |
| B012 | done | Evidence quality check | Archive index entry `020-evidence-quality-check`; validation and closure evidence workflow | Runtime and MCP review completed task and verification evidence for concrete validation versus vague, missing, waived, deferred, not-run, not-applicable, or weak claims. |
| B013 | candidate | Handoff packet | Archive index entry `013-agent-backed-lifecycle-tools`; active preflight and readiness packet runtime; Kiro resumability review | Produce a concise continuation packet for another coding agent without forcing it to reread the whole repository. See Kiro-inspired candidate details. |
| B014 | candidate | Conversation-history feature discovery review | Bounded local Codex history scan; user request | Use selected conversation history only as advisory feature-discovery input. Look for repeated corrections, frustration signals, sequencing prompts, and misunderstood workflows; do not treat history content as factual requirements or implement it directly. |
| B015 | candidate | Workflow friction report | Bounded local Codex history scan; user request | Summarize repeated lifecycle friction from conversation history, external feedback, and closure evidence into candidate tool, template, or guidance changes. Treat findings as suggestions only. |
| B016 | done | Commit sync guard | Commit/sync/install repetition in local history; user workflow | Runtime `sync-guard` now reports source skill versus bundled plugin parity, bundled plugin versus installed cache parity, running MCP reload advisory, and recent commit evidence without mutating install state. |
| B017 | done | Active spec preflight | Frequent "what next" prompts; spec-context skip corrections; `docs/reference/spec-lifecycle-runtime.md` | Runtime and MCP expose `active_spec_preflight`, returning active spec selection, next task, readiness context, no-active context, MCP-first interface, and validation commands. |
| B018 | done | No-active-spec context packet | Completed spec package confusion; removed-spec policy; `docs/reference/spec-lifecycle-runtime.md` | Runtime and MCP expose `no_active_spec_context`, returning durable docs, backlog, roadmap, closure log, archive index, MCP-first interface, and validation commands when no active spec exists. |
| B019 | candidate | Spec candidate builder | Backlog and conversation-derived feature ideas; Kiro rough-idea-to-spec review | Turn backlog, rough ideas, or advisory discovery notes into a draft spec skeleton with requirements, design prompts, tasks, traceability, and verification placeholders. See Kiro-inspired candidate details. |
| B020 | candidate | ADR candidate review | Decision extraction needs; governance adoption work | Identify decisions that deserve ADRs or governance updates, distinct from ordinary open decisions or backlog notes. |
| B021 | candidate | Template gap review | Template lint and task-context correction history | Compare current spec and durable templates against observed implementation pain, then suggest precise template changes with compatibility notes. |
| B022 | candidate | Agent instruction audit | AGENTS, skill, hook, and install guidance drift | Check `AGENTS.md`, skill guidance, hooks, MCP install docs, and runtime docs for contradictions or stale workflow instructions. |
| B023 | done | Validation plan builder | Validation feedback and closure evidence needs; archive index entry `019-validation-plan-builder` | Runtime and MCP generate a focused validation plan from changed files, task context, risk level, and durable-doc impact. |
| B024 | candidate | Review result router | Expert and subagent review feedback workflow | Route review findings to accept, reject, defer, backlog, follow-up spec, or human decision with rationale and evidence links. |
| B025 | candidate | OpenTelemetry and Jaeger tracing | User request; Agent Workbench reference implementation | Add disabled-by-default OpenTelemetry tracing for MCP tools and executable runtime code, with configurable OTLP HTTP export to Jaeger or a collector. Use `../agent-workbench/docs/design/observability-debugging-design.md` and `../agent-workbench/src/infrastructure/telemetry/` as reference implementation inputs. |
| B026 | done | npm distribution packaging | User request | Added npm package metadata, an `npx @auriora/ai-spec-lifecycle install` wrapper, package-contract validation, npm pack dry-run coverage, and install docs. npm publish, registry authentication, and release automation remain future work. |
| B027 | done | Project principles template | User request; `docs/governance/project-principles.md` | Added a reusable durable-doc template and skill guidance for purpose, problem statement, VMOST, core principles, scope rules, project-fit decision questions, governance relationship, and current product signals. |
| B028 | candidate | Agent Skills reference validator integration | Agent Skills standard review; `014-plugin-comparison-improvements` | Evaluate adding `skills-ref validate` to validation commands for source and bundled skills. Decide dependency installation, offline behavior, and whether failures should block plugin packaging. |
| B029 | candidate | Workflow mode contract | Kiro Vibe/Spec review; `docs/design/coding-agent-operating-model.md`; MCP preflight surface | Make the selected workflow level explicit in spec metadata and preflight output so agents distinguish direct patch, lightweight spec, full spec, and governance-gated work before editing. See Kiro-inspired candidate details. |
| B030 | candidate | Execution approval policy | Kiro Autopilot/Supervised review; governance decision-gate policy | Add an inspectable execution policy such as autonomous, task checkpoint, file-edit review, or governance required so agents know when to proceed, pause, or request human approval. See Kiro-inspired candidate details. |
| B031 | candidate | Phase gate check | Kiro requirements-design-tasks-implementation workflow review; lifecycle runtime | Add a deterministic phase-gate check that reports whether a spec is ready to move from requirements to design, design to tasks, tasks to implementation, or implementation to promotion and closure. See Kiro-inspired candidate details. |
| B032 | candidate | Semantic requirements lint | Kiro requirements quality guardrails; EARS criteria templates | Extend linting beyond structure to flag ambiguous, untestable, compound, glossary-missing, or implementation-leaking acceptance criteria before downstream design and task work. See Kiro-inspired candidate details. |
| B033 | candidate | Steering context inventory | Kiro steering files review; `AGENTS.md`; governance and project principles docs | Return applicable project instructions, governance, principles, durable docs, and conflicts as a single steering-context packet for agents before lifecycle work. See Kiro-inspired candidate details. |
| B034 | candidate | Hook policy inventory | Kiro hooks review; Codex advisory hook dogfood; R002 | Expose available lifecycle hook events, severity profiles, advisory versus blocking readiness, false-positive risk, and current install state without changing the advisory-only default. See Kiro-inspired candidate details. |
| B035 | candidate | Package capability manifest | Kiro Powers review; plugin packaging; MCP install docs | Publish a compact capability manifest for the skill/plugin that lists skills, MCP tools, prompts, hooks, templates, install paths, validation commands, and compatibility notes. See Kiro-inspired candidate details. |
| B036 | candidate | Optional Kiro spec import support | Kiro compatibility review; `.kiro/specs/` path discussion | Evaluate read-only discovery or migration support for `.kiro/specs/{feature}` packages while keeping `docs/specs/[###-slug]/` as this repository's default source of lifecycle work. See Kiro-inspired candidate details. |
| B037 | candidate | Task completion implementation audit | Kiro task-completion hook recommendations; stub-completion problem; existing `task-checkbox-changed`, `implementation-task-complete`, and `agent-response-check` hooks | Extend task-completion checks beyond evidence presence to inspect touched files for stubs, TODO placeholders, empty tests, and placeholder config before a task is treated as complete. See hook candidate details. |
| B038 | candidate | Task context and design reload hook | Kiro preTaskExecution recommendations; existing `agent-slice-start`; traceability runtime | Before implementation starts, require agents to reload task text, linked requirements, acceptance criteria, relevant design sections, and planned verification, then state the files and logic expected for done. See hook candidate details. |
| B039 | candidate | Policy-sensitive write review | Kiro fallback discipline and secrets hook recommendations; `AGENTS.md`; governance docs | Add an advisory pre-write or post-write review that flags possible fallback-discipline violations, secret material, silent degradation paths, and policy conflicts using repository steering context. See hook candidate details. |
| B040 | candidate | Prompt scope triage hook | Kiro promptSubmit scope recommendation; workflow mode contract B029; steering context B033 | When a request spans multiple subsystem or lifecycle boundaries, return an advisory scope warning and suggest whether to narrow, open a spec, or trigger a governance gate. See hook candidate details. |
| B041 | candidate | Session handoff hook | Kiro agentStop context-preservation recommendation; handoff packet B013 | On session stop or explicit handoff, generate a concise read-only summary of completed work, pending tasks, decisions, blockers, and validation evidence for the next session. See hook candidate details. |
| B042 | candidate | Runtime modularization | Brooks-Lint findings tracking spec `015-brooks-lint-findings-tracking`; `BL-ARCH-001`, `BL-DEBT-001`, `BL-HEALTH-002` | Split `spec_runtime.py` into focused modules or facades only when adjacent runtime changes create a clear boundary; avoid speculative refactoring. |
| B043 | candidate | Shared lifecycle test fixtures | Brooks-Lint findings tracking spec `015-brooks-lint-findings-tracking`; `BL-TEST-001` | Introduce shared spec-package fixture builders when a future fixture-heavy change touches runtime, MCP, hook, and traceability suites together. |
| B044 | active | npm publish and release workflow | B026 residual risk; user request; active spec `022-npm-publish-release-workflow` | Add GitHub Actions CI/CD for validation, packaged release artifacts, guarded npm publish, GitHub release evidence, and install verification. |
| B045 | candidate | Closure artifact exception policy | User discussion about completed specs blocked by missing `verification.md` or `traceability.md`; B008, B012, B023 | Consider lifecycle rules that distinguish missing evidence from missing preferred artifact containers. Support minimal final closure artifacts, explicit waivers, or evidence consolidation when tasks and durable promotion are complete but closure checks block on absent optional package files. |
| B046 | done | Hierarchical spec authoring hook guidance | User report of noisy `PostToolUse` findings when creating spec files; advisory hook dogfood; spec `023-hierarchical-spec-authoring-hooks` | Added hierarchy-aware `spec-file-changed` guidance, concise Codex hook next-action output, runtime docs, tests, bundle mirrors, install verification, and sync-guard evidence. |
| B047 | candidate | Spec package rationalisation and durable-doc integration | User discussion on spec document proliferation, `spec.md`, durable-doc precedence, and numbering | Clarify which spec intents are always required but embedded in core files, when optional artifacts should exist, and how legacy `spec.md` packages are handled without duplication. Also define how active specs reference, add to, or modify durable current-state docs. |

## Kiro-Inspired Candidate Details

These items come from a Kiro workflow review. They are discussion candidates,
not accepted implementation requirements. Promote one or more into a focused
spec when scope, acceptance criteria, compatibility risks, and runtime surface
changes are agreed.

### B013 Handoff Packet

- Build on `agent_readiness_packet` and `active_spec_preflight` to produce a
  concise continuation packet for another agent or a later session.
- Include selected spec, selected or next task, recent evidence, blockers, open
  decisions, validation commands, durable docs touched, and residual risk.
- Keep the packet read-only and deterministic; do not summarize unstaged local
  changes as accepted evidence without command or file references.
- Candidate MCP surface: `handoff_packet`.

### B019 Spec Candidate Builder

- Accept rough ideas, backlog items, or advisory discovery notes and generate a
  draft spec skeleton without writing files by default.
- Output draft requirements, design prompts, tasks, traceability placeholders,
  verification placeholders, open decisions, and durable-source gaps.
- Preserve source uncertainty: conversation-derived or external-review content
  should be advisory input, not factual requirements.
- Candidate MCP surface: `spec_candidate_builder` with an explicit
  `write_files: false` default if a write-capable version is later proposed.

### B029 Workflow Mode Contract

- Map Kiro's Vibe/Spec distinction to the existing operating-model levels:
  `direct_patch`, `lightweight_spec`, `full_spec`, and `governance_gate`.
- Add the chosen or recommended level to active preflight output and, where
  useful, active spec frontmatter.
- Report required artifacts for the level so agents do not create full-spec
  ceremony for low-risk work or skip requirements/design on cross-module work.
- Candidate MCP fields: `recommended_workflow_level`, `required_artifacts`,
  `human_gates`, and `reasoning`.

### B030 Execution Approval Policy

- Encode Kiro Autopilot/Supervised behavior as an execution policy rather than
  a broad session personality mode.
- Candidate values: `autonomous`, `task_checkpoint`, `file_edit_review`, and
  `governance_required`.
- Use the policy to tell agents when they may edit, when to pause after a task,
  when to request file-level approval, and when risky work needs a human
  decision before implementation.
- Keep policy advisory until a governance update explicitly makes any approval
  behavior mandatory.

### B031 Phase Gate Check

- Make requirements, design, tasks, implementation, promotion, and closure gates
  inspectable through the runtime instead of leaving them implicit in prose.
- Report `current_phase`, `ready_to_advance`, `missing_review`,
  `downstream_artifacts_stale`, `blocking_decisions`, and
  `next_required_action`.
- Detect common drift such as tasks written against stale requirements,
  design not covering accepted requirements, implementation evidence missing,
  or durable docs not promoted before closure.
- Candidate MCP surface: `phase_gate_check`.

### B032 Semantic Requirements Lint

- Extend linting beyond frontmatter and required sections into requirements
  quality.
- Flag acceptance criteria that lack SHALL-style mandatory language, combine
  multiple assertions, use undefined glossary terms, describe implementation
  instead of behavior, lack measurable outcomes, or omit important negative
  requirements.
- Keep diagnostics explainable and waiver-friendly because semantic lint can be
  noisy.
- Candidate runtime modes: advisory default, blocking only after dogfood and
  explicit approval.

### B033 Steering Context Inventory

- Treat `AGENTS.md`, governance, constitution, project principles, durable docs,
  and repository-specific guidance as the portable equivalent of Kiro steering
  files.
- Return the applicable guidance set before lifecycle work, including file
  paths, scope, priority, and any detected conflicts.
- Fold into preflight or expose as a separate read-only tool when agents need
  instruction context without scanning the whole docs tree.
- Candidate MCP surface: `steering_context`.

### B034 Hook Policy Inventory

- Keep lifecycle hooks advisory by default, consistent with R002.
- Expose available hook events, configured severity profiles, install state,
  checked file patterns, known false-positive risks, and whether each hook is
  safe for advisory or blocking use.
- Use the inventory to support future blocking-hook discussions without
  silently changing edit behavior.
- Candidate MCP surface: `hook_policy` or `hook_inventory`.

### B035 Package Capability Manifest

- Capture the plugin's Kiro-Powers-like capabilities in a repo-owned manifest or
  generated report.
- Include skills, MCP tools, prompts, hooks, templates, install paths,
  validation commands, bundled plugin paths, compatibility notes, and
  read-only/write-capable boundaries.
- Use it for adoption, packaging, install verification, and troubleshooting
  rather than introducing a new "power" abstraction.
- Candidate outputs: markdown reference doc and machine-readable JSON manifest.

### B036 Optional Kiro Spec Import Support

- Evaluate `.kiro/specs/{feature}` discovery or migration support as an
  optional compatibility path.
- Keep `docs/specs/[###-slug]/` as the default because this repository ties
  specs to durable docs, backlog, roadmap, closure log, and archive index.
- Prefer read-only import, lint, and migration-preview behavior before any
  write-capable conversion tool.
- Candidate MCP/runtime behavior: detect `.kiro/specs/`, report compatibility,
  and suggest migration steps without treating those packages as active by
  default.

## Hook Candidate Details

These items adapt Kiro hook recommendations for this repository's
`spec-lifecycle-manager` skill and MCP runtime. AWS-datalake-specific checks,
such as SAM validation, scoped Python module tests, and SQL migration version
numbers, are intentionally excluded unless they become generic lifecycle
validation patterns.

### B037 Task Completion Implementation Audit

- Build on the existing `task-checkbox-changed`,
  `implementation-task-complete`, and `agent-response-check` hooks.
- Trigger when a task is marked complete in `tasks.md`, a task-completion hook
  is invoked, or an agent claims task completion in a response.
- Inspect files listed in task metadata, changed files passed to the hook, and
  evidence references where available.
- Flag likely incomplete implementation indicators: `pass`,
  `NotImplementedError`, TODO or placeholder comments in production paths,
  empty functions, tests with no assertions, skipped tests without reasons,
  placeholder config values, or evidence that does not mention concrete files or
  commands.
- Keep output advisory by default. A blocking profile would require dogfood
  evidence, false-positive handling, waivers, and explicit approval.
- Candidate runtime fields: `inspected_files`, `stub_indicators`,
  `evidence_gaps`, `recommended_task_status`, and `residual_risk`.

### B038 Task Context and Design Reload Hook

- Extend `agent-slice-start` so pre-task execution reloads the full task row,
  linked requirements, acceptance criteria, traceability rows, design sections,
  verification expectations, durable targets, and open decisions.
- Require the agent-facing output to state the expected file set, real logic to
  implement, non-goals, and verification before edits begin.
- Detect missing `_Requirements:` or traceability references, stale requirement
  IDs, unresolved open decisions, and design/task mismatches.
- Prefer MCP `task_context` and `traceability_lookup` as the source of truth.
- Candidate runtime fields: `task_context_loaded`, `design_alignment`,
  `missing_links`, `implementation_plan_required`, and `validation_plan`.

### B039 Policy-Sensitive Write Review

- Adapt fallback-discipline and secrets checks into a generic policy-sensitive
  lifecycle hook.
- Use steering context from `AGENTS.md`, governance, project principles, and
  durable docs to identify repository-specific constraints before or after
  writes.
- Flag likely implicit fallbacks, silent default substitution, degraded paths,
  credential material, tokens, connection strings, or policy conflicts.
- Avoid repo-specific command execution in the generic skill; projects can add
  their own validators through hook configuration or validation plans.
- Candidate runtime modes: pre-write advisory for planned edits and post-write
  advisory for changed-file review.
- Candidate runtime fields: `policy_sources`, `suspected_fallbacks`,
  `suspected_secrets`, `policy_conflicts`, and `recommended_review_gate`.

### B040 Prompt Scope Triage Hook

- Adapt Kiro's `promptSubmit` scope check into a lifecycle triage hook.
- Detect requests that appear to cross multiple subsystems, durable-doc classes,
  active specs, governance boundaries, or implementation/test/deploy phases.
- Return an advisory recommendation: direct patch, narrow the request, choose an
  active spec, create a lightweight/full spec, or stop for a governance gate.
- Build on B029 workflow mode contract and B033 steering context inventory.
- Candidate MCP/runtime surface: `prompt_scope_check`, usable by hooks or
  direct preflight before work begins.

### B041 Session Handoff Hook

- Adapt Kiro's `agentStop` session-context summary into a read-only lifecycle
  handoff.
- Build on B013 handoff packet rather than writing to `.kiro/steering/` or
  project instructions by default.
- Include completed tasks, changed files, validation run, validation not run,
  pending tasks, open decisions, blockers, and durable docs that may need
  promotion.
- Persisting the handoff should be explicit and repository-routed; default
  behavior should return the packet to the agent/client without mutating docs.
- Candidate hook events: `agent-stop`, explicit `handoff-requested`, or
  post-task checkpoint.

### B046 Hierarchical Spec Authoring Hook Guidance

- Implemented by spec `023-hierarchical-spec-authoring-hooks`.
- `spec-file-changed` now returns hierarchy-aware authoring context instead of
  defaulting to whole-package lint for ordinary spec authoring.
- The Codex hook wrapper now surfaces concise next-action guidance, relevant
  helper tools, and downstream review candidates.
- Full package lint remains available for explicit validation, resume, and
  closure workflows.

### B047 Spec Package Rationalisation And Durable-Doc Integration

The current package model has a good direction but needs a clearer
low-duplication contract before changing templates or runtime behavior.

Discussion baseline:

- `spec.md` was deprecated during the Kiro-style alignment work on 2026-06-02,
  especially commit `58cfb9e` (`Align skill flow with Kiro-style specs`).
  The migration decision was to consolidate `spec.md` and `plan.md` content
  into `requirements.md`, while keeping old-format packages supported through a
  visible migration decision.
- Existing `spec.md` files in downstream projects are not automatically
  useless. They often act as a feature brief, summary, or old-format
  requirements container. The risk is duplication when they restate
  requirements, durable-source baselines, or design decisions already present in
  `requirements.md`, `design.md`, or durable docs.
- Optional artifacts should stay optional as files, but their intent should not
  disappear. The required core package should embed the necessary intent:
  durable-source baseline, durable-doc impact, verification expectations,
  traceability links, open decisions, and promotion targets.
- Durable docs should describe current accepted state by default. Intended or
  proposed state belongs in an active spec, backlog, roadmap, ADR proposal, or a
  clearly marked proposed/deferred section.
- Active specs should explicitly say whether they add to, modify, clarify,
  supersede, or leave unchanged each relevant durable doc class: requirements,
  design, architecture, API/contract, data-flow, runbook, verification, and
  reference docs.
- Numbering may help agent read order and precedence, but spec numbers should
  remain distinct from durable-doc numbering. Prefer runtime/template read-order
  metadata before renaming canonical files such as `requirements.md`,
  `design.md`, and `tasks.md`.

Candidate scope for a future spec:

- Define a minimal core package contract where `requirements.md`, `design.md`,
  and `tasks.md` embed required lifecycle intents without forcing every
  supporting artifact to exist as a separate file.
- Define conditions that justify separate `change-impact.md`,
  `verification.md`, `traceability.md`, `open-decisions.md`, `research.md`, or
  `quickstart.md` files.
- Define a compatibility rule for old-format `spec.md`: feature brief only,
  migration input, or deprecated duplicate. Runtime should classify the role
  and warn when it duplicates current artifacts.
- Strengthen durable-doc mapping so every active spec records current durable
  sources, intended deltas, promotion targets, and unchanged durable areas.
- Decide whether package indexes or runtime preflight should expose artifact
  precedence/read order without changing filenames.
- Decide whether durable docs need a numbering convention that distinguishes
  durable document order from active spec IDs.

## Candidate Priorities

Priority is based on recurring friction signals from local history and project
dogfooding, not on factual claims from conversation content.

| Priority | Backlog ID | Rationale |
|----------|------------|-----------|
| P1 | B016 | Reduces repeated commit/sync/install drift after skill changes by checking installed/source parity and making sync status explicit. |
| P1 | B026 | Makes the skill/MCP easier to install and update outside this repository through a useful npm package shape before broader adoption. |
| P1 | B023 | Improves evidence quality by deriving validation plans from actual task, file, and documentation-only context while avoiding skipped-check noise. |
| P1 | B037 | Directly targets stub-completion and weak task completion claims by checking implementation files and evidence together. |
| P1 | B038 | Reduces context-loss errors before implementation by forcing task, requirement, design, and verification reloads through existing traceability surfaces. |
| P1 | B012 | Helps distinguish real task evidence from vague, not-run, and genuinely not-applicable validation claims. |
| P1 | B008 | Improves closure quality by separating historical recoverability from stale-active-document guidance risk. |
| P2 | B029 | Makes workflow level explicit before agents choose whether to patch directly, open a spec, or stop for governance review. |
| P2 | B031 | Turns lifecycle phase transitions into deterministic checks that can prevent stale requirements, incomplete design, or premature implementation. |
| P2 | B033 | Gives agents a portable steering context without adopting Kiro-specific `.kiro/steering/` paths. |
| P2 | B044 | Turns the pack-ready npm package into a governed CI/CD release path with validation, provenance, and guarded publish behavior. |
| P2 | B025 | Adds operational visibility for MCP tools and runtime executables as the tool surface grows; should stay disabled by default and export to Jaeger only when configured. |
| P2 | B028 | Gives an official standard conformance check once dependency and offline behavior are agreed. |
| P2 | B030 | Clarifies autonomy and approval expectations before edits, especially for task checkpoints and governance-sensitive work. |
| P2 | B032 | Improves requirement quality before design and implementation amplify ambiguous acceptance criteria. |
| P2 | B039 | Generalizes fallback-discipline and secrets concerns into a repository-policy review without hard-coding AWS-datalake behavior. |
| P2 | B040 | Helps route broad prompts into direct patch, spec, or governance paths before agents start broad work. |
| P2 | B045 | Clarifies how closure should handle functionally complete specs that lack preferred artifact files, reducing unnecessary retroactive documentation while preserving evidence quality. |
| P2 | B047 | Reduces spec document proliferation and duplication while strengthening the tie between active specs and durable current-state docs. |
| P2 | B015 | Converts repeated corrections and workflow friction into candidate improvements without treating history as authoritative. |
| P2 | B014 | Supports bounded feature discovery from selected history as advisory input only. |
| P3 | B009 | Useful for richer specs, but lower priority than preflight because traceability can already be hand-authored. |
| P3 | B013 | Helps continuation between agents now that the preflight/context model exists. |
| P3 | B022 | Valuable hygiene once agent instructions and MCP docs change more often. |
| P3 | B042 | Useful when runtime changes reveal stable module boundaries; should not lead with speculative refactoring. |
| P3 | B043 | Reduces fixture drift once enough related test changes justify a shared helper. |
| P3 | B011 | Useful for governance hygiene, but can be noisy without strong routing rules. |
| P3 | B020 | Builds on decision extraction and should follow clearer ADR guidance. |
| P3 | B021 | Best after several more template pain points accumulate. |
| P3 | B010 | Higher semantic risk because durable-code drift review can produce plausible but weak findings. |
| P3 | B019 | Useful once backlog prioritization and tool scope are stable. |
| P3 | B024 | Best after expert/subagent review result formats are more settled. |
| P3 | B034 | Useful for hook governance and troubleshooting, but should follow more advisory-hook dogfood data. |
| P3 | B035 | Supports packaging and adoption once the plugin distribution shape is clearer. |
| P3 | B036 | Valuable for Kiro interoperability, but lower priority than improving this repository's native `docs/specs/` lifecycle. |
| P3 | B041 | Useful for resumability, but should build on B013 and remain non-mutating by default. |

## Advisory Discovery Notes

The 2026-06-06 local Codex history scan sampled user-message text from
`~/.codex/history.jsonl` and `~/.codex/sessions/**/*.jsonl`. The scan suggested
recurring areas to consider, not factual requirements: agents skipping full spec
context, commit/sync/install repetition, completed spec packages confusing
agents, MCP/hook/tool validation, frequent "what next" sequencing needs, and
correction or frustration language around misunderstood scope.

## Maintenance

- Promote an item into a focused spec when scope, owner, and acceptance
  criteria are clear.
- Promote or link an item to roadmap when sequencing, milestone, adoption, or
  multi-spec dependency tracking matters.
- Link closed specs to backlog items when follow-up work is intentionally
  deferred.
- Keep backlog items concise; detailed requirements belong in a spec package.
