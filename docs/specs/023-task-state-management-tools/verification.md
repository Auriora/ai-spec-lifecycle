---
title: Task state management tools verification
doc_type: spec
artifact_type: verification
status: active
owner: platform
last_reviewed: 2026-06-13
---

# Verification

## Quality Gates

| Gate | Scope | Required Evidence | Status |
| --- | --- | --- | --- |
| VG-001 | Marker contract | Parser tests cover preferred symbols and compatibility markers. | Pending |
| VG-002 | Task query tools | Runtime and MCP tests cover list/detail output, traceability context, dependencies, and subtasks. | Pending |
| VG-003 | Task audit | Runtime/hook tests catch contradictory completion, broad tasks, and follow-up prose without state. | Pending |
| VG-004 | State update | Dry-run and write tests prove scoped edits, explicit write intent, before/after patch summaries, guarded completion, and rejection of paths outside active spec package `tasks.md`. | Pending |
| VG-005 | Guidance and bundle parity | Source docs/templates and bundled plugin copies match; full repo validation passes. | Pending |
| VG-006 | Reconciliation depth | Fixtures cover stale-open tasks with evidence, candidate-complete findings, plan-only completion warnings, blocked-output warnings, `split_task_suggestions`, and cross-spec dependency health. | Pending |
| VG-007 | Metadata contract | Parser/query/update tests cover `Evidence mode:`, `Destination:`, `Decision owner:`, `Upstream specs:`, and `Downstream specs:` fields. | Pending |
| VG-008 | MCP write boundary | MCP tests prove write tools are preview-first, spec-only, task-block-scoped, and reject ambiguous or out-of-bound targets. | Pending |

## Evidence Log

| Date | Evidence | Covers | Result |
| --- | --- | --- | --- |
| 2026-06-13 | Spec created from Spec 065 task-state discussion. | Requirements and design scope. | Pending implementation. |
| 2026-06-13 | Reviewed local Codex session `019ebd51-67ed-72f0-a994-cc1cef4acf6d` for aws-datalake Specs 023 and 048. | Added stale-open, plan-only completion, blocked-output, cross-spec dependency, and evidence-depth requirements. | Pending implementation. |
| 2026-06-13 | Reviewed task-state spec against current read-only MCP boundary and accepted guarded spec/documentation write direction. | Added preview-first MCP write boundary, metadata fields, and split-task suggestion requirements. | Pending implementation. |

## Validation Commands

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'`
- `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py scan .`
- `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py prompts`
- `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py archive-index .`
- `git diff --check`

## Residual Risks

- Symbol markers may still be less obvious than letter markers for occasional
  users. Documentation and tool output must always include normalized names.
- A Markdown write tool can damage formatting if implemented too broadly. The
  update helper must preserve unrelated text and default to dry-run.
- Hooks can become noisy if they report the same in-progress task after every
  edit. Hook output should be tied to state contradictions or preflight
  summaries, not every normal write.
- Evidence-depth detection can be approximate when task acceptance is vague.
  Audit output should report the evidence and classification clearly instead of
  pretending to make a final project-management decision.
- MCP write support changes the existing read-only trust model. Initial
  implementation must keep writes spec-only, preview-first, task-block-scoped,
  and easy to disable if dogfooding shows the noise or risk is too high.
