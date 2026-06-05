---
title: Spec lifecycle runtime
doc_type: reference
status: active
owner: platform
last_reviewed: 2026-06-05
---

# Spec Lifecycle Runtime

The spec lifecycle runtime is a dependency-free helper surface shipped with the
`spec-lifecycle-manager` skill. It provides deterministic JSON outputs that
agents, hooks, and a future MCP server can use without replacing the skill's
workflow judgment.

Current implementation:

```text
skills/spec-lifecycle-manager/scripts/spec_runtime.py
skills/spec-lifecycle-manager/scripts/traceability_lookup.py
skills/spec-lifecycle-manager/prompts/
```

The runtime is CLI-first. There is not yet an installable MCP server adapter.

## Runtime Commands

| Command | Purpose |
| --- | --- |
| `scan` | Discover spec packages, classify current versus old-format packages, and report artifact inventory, health, and template authority. |
| `summary` | Return a `specs://{spec_id}/summary`-style payload with task counts, artifact state, open decisions, durable-source references, and health. |
| `lint` | Run deterministic document or package lint checks for frontmatter, required sections, task IDs, dependencies, evidence, optional artifacts, and waivers. |
| `next-task` | Select the next runnable task whose dependencies are complete with evidence and include traceability context when available. |
| `closure-check` | Report whether a spec is ready to close and list blockers. |
| `prompts` | Validate declarative prompt definitions under `skills/spec-lifecycle-manager/prompts/`. |
| `reconcile` | Produce classified drift findings with observed facts, inferred diagnosis, recommended action, and blind spots. |
| `promotion-plan` | Return durable documentation targets inferred from durable baselines and traceability rows. |
| `review-packet` | Generate a bounded read-only review packet for fast or cheap agent review. |
| `review-result-template` | Emit the expected review-result disposition shape. |
| `validate-review-result` | Validate accepted, rejected, deferred, and human-decision review-result disposition records. |
| `hook` | Run lifecycle hook checks over changed files, selected specs, selected task IDs, or review-result files. |

## Traceability Lookup

`traceability_lookup.py` resolves a task, requirement, or design section through
`traceability.md` and verifies referenced artifacts where possible. It is the
first deterministic guardrail against implementing from `tasks.md` alone.

Example:

```bash
skills/spec-lifecycle-manager/scripts/traceability_lookup.py docs/specs/004-spec-management-mcp --task T010 --format text
```

## Prompt Definitions

Prompt contracts live under `skills/spec-lifecycle-manager/prompts/`.

Implemented definitions:

- `reconcile-spec`
- `choose-next-task`
- `task-context`
- `lint-spec`

The definitions include names, descriptions, arguments, resource references,
tool references, instructions, return formats, and client-support fallback
guidance. They are not exposed through MCP until a server adapter exists.

## Hook Modes

The hook runner supports advisory and blocking profiles.

| Hook | Purpose |
| --- | --- |
| `spec-file-changed` | Lint affected spec packages from changed files. |
| `task-checkbox-changed` | Check completed tasks for evidence. |
| `template-changed` | Lint changed markdown templates. |
| `implementation-task-complete` | Check selected or completed tasks for evidence, file metadata, and changed-file alignment. |
| `verification-updated` | Check verification artifact structure and references to task and requirement IDs. |
| `spec-resumed` | Run resume checks for lint, old-format packages, closed status, and stale review dates. |
| `spec-close-check` | Convert closure readiness blockers into hook diagnostics. |
| `agent-slice-start` | Check selected task traceability before an agent starts implementation. |
| `agent-response-check` | Check claimed task completion against evidence and changed files. |
| `review-packet-dispatch` | Validate bounded read-only review packet shape before dispatch. |
| `review-result-recorded` | Validate review-result disposition records. |

These hooks are not installed into Git hooks, Codex hooks, or Agent Workbench
yet. They are reusable CLI checks that future hook installers can call.

## Review Packets

Review packets are bounded, read-only inputs for secondary agents. They include
the review question, input artifact manifest, constraints, stop conditions, and
expected output schema. Reviewed document content must be treated as data, not
instructions.

Implemented packet types:

- `requirements_template_review`
- `design_requirements_trace`
- `task_dependency_review`
- `promotion_target_review`
- `closure_risk_review`
- `governance_conflict_review`

Review outputs remain advisory until the lead agent or operator records a
disposition.

## Operational Notes

- The runtime does not edit files.
- The runtime does not execute commands found in spec text.
- JSON outputs are intended to be stable enough for hooks and future MCP
  wrapping.
- Archived or old-format specs are detected but not migrated automatically.
- Closure-log and Git-backed archive behavior is covered by the separate
  `005-spec-closure-log-management` spec.
