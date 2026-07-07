---
title: Agent Workbench evidence boundary
doc_type: reference
status: active
owner: platform
last_reviewed: 2026-06-13
---

# Agent Workbench Evidence Boundary

Use this reference when Agent Workbench, or an equivalent repository-evidence
tool, contributes context to lifecycle work. The integration is optional and
capability-gated; repositories using this skill must not depend on Agent
Workbench being installed.

## Boundary Doctrine

```text
Specs decide intent and completion.
Durable docs define accepted truth.
Agent Workbench provides current repo evidence.
Tests and validation provide proof.
Agents may propose, implement, and review, but they must not silently upgrade routing evidence into proof.
```

Workbench-style evidence can improve context selection, impact analysis,
diagnostics, and validation planning. It cannot decide task completion, close a
spec, promote durable docs, override governance, or replace human approval
points.

## Bridge Inputs

Lifecycle guidance may pass these inputs to a repo-evidence provider:

- task or requirement ID;
- active spec path, when present;
- durable docs baseline paths;
- known affected files or subsystems;
- validation expectations;
- risk level;
- mutation permissions and forbidden paths.

## Provider Outputs

Treat provider output as evidence metadata, not lifecycle authority:

- repository status and freshness;
- relevant files, symbols, and direct-read caveats;
- impact evidence;
- diagnostics evidence;
- validation plan suggestions;
- skipped or unsupported evidence;
- confidence, freshness, and capability metadata.

## Evidence Fields

When useful, record Workbench-style evidence in task evidence,
`verification.md`, review packets, or final status using a compact shape like:

```yaml
workbench_evidence:
  provider: agent-workbench
  repo_status: fresh | stale | cold | refreshing | unknown
  context_tool: context_for_task
  context_confidence: high | medium | low | partial
  capability_level: semantic | partial_semantic | resource_backed | unsupported
  evidence_kinds:
    - parser
    - sqlite
    - docs
  changed_files:
    - <path>
  diagnostics:
    status: clean | warnings | blocked | not_run
    tool: diagnostics_for_files
  validation_plan:
    status: planned | done | blocked | needed | not_applicable
    commands: []
    blocked_reason:
  residual_risk: []
```

Equivalent tools may use the same fields with a different `provider` value.
Omit fields that are not applicable rather than fabricating confidence.

## Interpretation Rules

- Routing evidence is not proof.
- Sparse or low-signal search output is not absence evidence. Treat it as a
  query or scope limitation, then inspect repository instructions, durable
  indexes, targeted file inventories, and direct source files before claiming
  docs, code, contracts, or tests are missing.
- Planned validation is not completed validation.
- Clean diagnostics do not mean tests passed.
- Stale, cold, partial, or unsupported provider status must be refreshed or
  carried as residual risk.
- Direct-read caveats must be surfaced when the provider cannot inspect the
  authoritative source directly.
- Provider confidence must not override durable docs, executable contracts,
  tests, review findings, or governance gates.

## Recovery Pattern

When repository-evidence output is sparse, surprising, truncated, stale, or
only resource-backed:

1. Report the provider state precisely, for example "the provider query did
   not surface the expected subsystem docs."
2. Check repository instructions and durable indexes such as `AGENTS.md`,
   `README.md`, `docs/README.md`, backlog, roadmap, closure logs, and archive
   indexes.
3. Use targeted file inventory (`rg --files`, known doc classes, likely
   subsystem paths) to identify candidate authoritative files.
4. Directly read the smallest complete set of candidate docs, contracts, code,
   and tests needed for the claim.
5. Carry unresolved provider gaps as residual risk instead of converting them
   into root-cause or absence claims.

## Review Stance

Use `workbench_evidence_quality` as the review stance when repository-evidence
metadata affects implementation or closure confidence. The review should check
whether provider evidence was fresh enough, capable enough, correctly scoped,
and not over-interpreted as validation proof or lifecycle authority.
