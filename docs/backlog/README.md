---
title: Agent development lifecycle backlog
doc_type: backlog
status: active
owner: platform
last_reviewed: 2026-06-06
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
| B008 | candidate | Closure risk review | Archive index entry `013-agent-backed-lifecycle-tools`; `docs/reference/spec-lifecycle-runtime.md`; review packet runtime | Use advisory review packets or a future configured runner to flag missing durable promotion, weak evidence, unresolved decisions, risky follow-ups, and closure blockers before package closure. |
| B009 | candidate | Draft traceability matrix | Archive index entry `013-agent-backed-lifecycle-tools`; traceability runtime and templates | Generate a proposed traceability matrix from requirements, design, tasks, change impact, and verification, then validate references deterministically. |
| B010 | candidate | Durable doc drift review | Archive index entry `013-agent-backed-lifecycle-tools`; durable-doc promotion runtime | Compare durable docs against relevant code, config, tests, or runtime contracts and report suspected drift for lead-agent review. |
| B011 | candidate | Decision extractor | Archive index entry `013-agent-backed-lifecycle-tools`; governance and open-decision docs | Scan specs and durable docs for implicit decisions that should become ADRs, open decisions, backlog items, roadmap items, or explicit no-action notes. |
| B012 | candidate | Evidence quality check | Archive index entry `013-agent-backed-lifecycle-tools`; validation and closure evidence workflow | Review completed task evidence for concrete validation versus vague claims; keep output advisory and require deterministic evidence references where possible. |
| B013 | candidate | Handoff packet | Archive index entry `013-agent-backed-lifecycle-tools`; active preflight and readiness packet runtime | Produce a concise continuation packet for another coding agent without forcing it to reread the whole repository. |
| B014 | candidate | Conversation-history feature discovery review | Bounded local Codex history scan; user request | Use selected conversation history only as advisory feature-discovery input. Look for repeated corrections, frustration signals, sequencing prompts, and misunderstood workflows; do not treat history content as factual requirements or implement it directly. |
| B015 | candidate | Workflow friction report | Bounded local Codex history scan; user request | Summarize repeated lifecycle friction from conversation history, external feedback, and closure evidence into candidate tool, template, or guidance changes. Treat findings as suggestions only. |
| B016 | candidate | Commit sync guard | Commit/sync/install repetition in local history; user workflow | Detect commits or working-tree changes that touch `skills/spec-lifecycle-manager/`, compare source against the installed `~/.codex/skills/spec-lifecycle-manager/` copy, and remind or automate the installer when drift exists. |
| B017 | done | Active spec preflight | Frequent "what next" prompts; spec-context skip corrections; `docs/reference/spec-lifecycle-runtime.md` | Runtime and MCP expose `active_spec_preflight`, returning active spec selection, next task, readiness context, no-active context, MCP-first interface, and validation commands. |
| B018 | done | No-active-spec context packet | Completed spec package confusion; removed-spec policy; `docs/reference/spec-lifecycle-runtime.md` | Runtime and MCP expose `no_active_spec_context`, returning durable docs, backlog, roadmap, closure log, archive index, MCP-first interface, and validation commands when no active spec exists. |
| B019 | candidate | Spec candidate builder | Backlog and conversation-derived feature ideas | Turn backlog or advisory discovery ideas into a draft spec skeleton with requirements, design prompts, tasks, traceability, and verification placeholders. |
| B020 | candidate | ADR candidate review | Decision extraction needs; governance adoption work | Identify decisions that deserve ADRs or governance updates, distinct from ordinary open decisions or backlog notes. |
| B021 | candidate | Template gap review | Template lint and task-context correction history | Compare current spec and durable templates against observed implementation pain, then suggest precise template changes with compatibility notes. |
| B022 | candidate | Agent instruction audit | AGENTS, skill, hook, and install guidance drift | Check `AGENTS.md`, skill guidance, hooks, MCP install docs, and runtime docs for contradictions or stale workflow instructions. |
| B023 | candidate | Validation plan builder | Validation feedback and closure evidence needs | Generate a focused validation plan from changed files, task context, risk level, and durable-doc impact. |
| B024 | candidate | Review result router | Expert and subagent review feedback workflow | Route review findings to accept, reject, defer, backlog, follow-up spec, or human decision with rationale and evidence links. |
| B025 | candidate | OpenTelemetry and Jaeger tracing | User request; Agent Workbench reference implementation | Add disabled-by-default OpenTelemetry tracing for MCP tools and executable runtime code, with configurable OTLP HTTP export to Jaeger or a collector. Use `../agent-workbench/docs/design/observability-debugging-design.md` and `../agent-workbench/src/infrastructure/telemetry/` as reference implementation inputs. |
| B026 | candidate | Distribution packaging for GHCR | User request | Package the skill, MCP server, scripts, prompts, and install metadata for distribution through GitHub Container Registry. Define versioning, image/package layout, install or sync commands, provenance, and compatibility checks. |
| B027 | done | Project principles template | User request; `docs/governance/project-principles.md` | Added a reusable durable-doc template and skill guidance for purpose, problem statement, VMOST, core principles, scope rules, project-fit decision questions, governance relationship, and current product signals. |
| B028 | candidate | Agent Skills reference validator integration | Agent Skills standard review; `014-plugin-comparison-improvements` | Evaluate adding `skills-ref validate` to validation commands for source and bundled skills. Decide dependency installation, offline behavior, and whether failures should block plugin packaging. |

## Candidate Priorities

Priority is based on recurring friction signals from local history and project
dogfooding, not on factual claims from conversation content.

| Priority | Backlog ID | Rationale |
|----------|------------|-----------|
| P1 | B016 | Reduces repeated commit/sync/install drift after skill changes by checking installed/source parity and making sync status explicit. |
| P1 | B026 | Makes the skill/MCP easier to install and update outside this repository; should define GHCR package shape before broader adoption. |
| P2 | B015 | Converts repeated corrections and workflow friction into candidate improvements without treating history as authoritative. |
| P2 | B014 | Supports bounded feature discovery from selected history as advisory input only. |
| P2 | B023 | Improves evidence quality by deriving validation plans from actual task and file context. |
| P2 | B012 | Helps distinguish real task evidence from vague completion claims. |
| P2 | B008 | Improves closure quality and durable-promotion confidence. |
| P2 | B025 | Adds operational visibility for MCP tools and runtime executables as the tool surface grows; should stay disabled by default and export to Jaeger only when configured. |
| P2 | B028 | Gives an official standard conformance check once dependency and offline behavior are agreed. |
| P3 | B009 | Useful for richer specs, but lower priority than preflight because traceability can already be hand-authored. |
| P3 | B013 | Helps continuation between agents now that the preflight/context model exists. |
| P3 | B022 | Valuable hygiene once agent instructions and MCP docs change more often. |
| P3 | B011 | Useful for governance hygiene, but can be noisy without strong routing rules. |
| P3 | B020 | Builds on decision extraction and should follow clearer ADR guidance. |
| P3 | B021 | Best after several more template pain points accumulate. |
| P3 | B010 | Higher semantic risk because durable-code drift review can produce plausible but weak findings. |
| P3 | B019 | Useful once backlog prioritization and tool scope are stable. |
| P3 | B024 | Best after expert/subagent review result formats are more settled. |

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
