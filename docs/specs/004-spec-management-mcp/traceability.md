---
title: Spec management MCP traceability
doc_type: spec
artifact_type: traceability
status: draft
owner: platform
last_reviewed: 2026-06-05
---

# Traceability Matrix

## Purpose

Map MCP runtime requirements, design sections, tasks, verification evidence,
durable-doc targets, and open decisions in both directions. Agents must use this
matrix as the first lookup point before implementing a task, then verify the
referenced source artifacts.

## Task To Context Matrix

| Task ID | Requirements | Acceptance Criteria | Design Sections | Change Impact | Verification | Durable Targets | Open Decisions |
|---------|--------------|---------------------|-----------------|---------------|--------------|-----------------|----------------|
| T004 | Requirement 3 | Requirement 3 AC1, AC2, AC3, AC4 | `design.md#mcp-resources`, `design.md#resource-payload-shape`, `design.md#implementation-packaging-decision` | none | CLI `scan` and `summary`; unit tests for current and old-format specs | `skills/spec-lifecycle-manager/SKILL.md` | none |
| T005 | Requirement 4 | Requirement 4 AC1, AC2, AC3, AC4, AC5 | `design.md#mcp-tools`, `design.md#linter-design`, `design.md#artifact-rules` | none | CLI `lint`; unit tests for task evidence diagnostics and package summaries | `skills/spec-lifecycle-manager/SKILL.md` | none |
| T006 | Requirement 6 | Requirement 6 AC1, AC2, AC3, AC4, AC5, AC6 | `design.md#mcp-tools`, `design.md#task-planner-and-closure-checks` | none | CLI `next-task` and `closure-check`; unit tests for selected tasks and closure blockers | `skills/spec-lifecycle-manager/SKILL.md` | none |
| T007 | Requirement 2 | Requirement 2 AC1, AC2, AC3, AC4 | `design.md#mcp-prompts`, `design.md#prompt-template-pattern`, `design.md#client-support-fallback` | none | Prompt definitions are discoverable or documented as client fallback | `skills/spec-lifecycle-manager/SKILL.md` | none |
| T008 | Requirement 8 | Requirement 8 AC1, AC2, AC4, AC5 | `design.md#hook-design`, `design.md#phase-1-advisory-hooks`, `design.md#recommended-hook-adoption-order` | none | CLI `hook spec-file-changed`; CLI `hook task-checkbox-changed`; unit tests for advisory and blocking modes | `skills/spec-lifecycle-manager/SKILL.md` | none |
| T009 | Requirement 8 | Requirement 8 AC2, AC3, AC5 | `design.md#phase-2-completion-gates`, `design.md#phase-3-lifecycle-gates` | none | Completion, verification, resume, and closure hook checks with clear blocking/advisory behavior | `skills/spec-lifecycle-manager/SKILL.md` | none |
| T010 | Requirement 5, Requirement 7 | Requirement 5 AC1, AC2, AC3, AC4; Requirement 7 AC1, AC2, AC3, AC4 | `design.md#reconciliation-design`, `design.md#review-packet-design`, `design.md#packet-output-schema` | none | CLI reconciliation, promotion planning, review packet, review-result disposition, and agent-hook smoke checks with unit coverage | `skills/spec-lifecycle-manager/SKILL.md` | none |
| T011 | Requirement 9, Requirement 10 | Requirement 9 AC1, AC2, AC3, AC4; Requirement 10 AC1, AC2, AC3 | `design.md#security`, `design.md#operational-considerations`, `design.md#mvp` | none | Dogfood runtime on this spec, record findings and overhead, then promote durable docs | `docs/design/spec-lifecycle-management.md`, `docs/reference/` | none |
| T012 | Requirement 6A | Requirement 6A AC1, AC2, AC3, AC4 | `design.md#mcp-tools`, `design.md#mcp-resources` | none | CLI lookup for task, requirement, design, and missing-row cases; unit tests for matrix parsing and gap reporting | `skills/spec-lifecycle-manager/SKILL.md`, `skills/spec-lifecycle-manager/references/spec-package/traceability.md` | none |

## Requirement To Delivery Matrix

| Requirement | Acceptance Criteria | Design Sections | Tasks | Verification | Durable Targets |
|-------------|---------------------|-----------------|-------|--------------|-----------------|
| Requirement 2 | AC1, AC2, AC3, AC4 | `design.md#mcp-prompts`, `design.md#prompt-template-pattern`, `design.md#client-support-fallback` | T007 | Prompt definition validation and client fallback review | `skills/spec-lifecycle-manager/SKILL.md` |
| Requirement 3 | AC1, AC2, AC3, AC4 | `design.md#mcp-resources`, `design.md#resource-payload-shape`, `design.md#implementation-packaging-decision` | T004 | CLI `scan` and `summary`; unit tests | `skills/spec-lifecycle-manager/SKILL.md` |
| Requirement 4 | AC1, AC2, AC3, AC4, AC5 | `design.md#mcp-tools`, `design.md#linter-design`, `design.md#artifact-rules` | T005 | CLI `lint`; unit tests | `skills/spec-lifecycle-manager/SKILL.md` |
| Requirement 6 | AC1, AC2, AC3, AC4, AC5, AC6 | `design.md#mcp-tools`, `design.md#task-planner-and-closure-checks` | T006 | CLI `next-task` and `closure-check`; unit tests | `skills/spec-lifecycle-manager/SKILL.md` |
| Requirement 6A | AC1, AC2, AC3, AC4 | `design.md#mcp-tools`, `design.md#mcp-resources` | T012 | CLI lookup for task, requirement, design, and missing-row cases; unit tests | `skills/spec-lifecycle-manager/SKILL.md`, `skills/spec-lifecycle-manager/references/spec-package/traceability.md` |
| Requirement 7 | AC1, AC2, AC3, AC4 | `design.md#review-packet-design`, `design.md#packet-output-schema` | T010 | Review packet smoke checks and unit tests | `skills/spec-lifecycle-manager/SKILL.md` |
| Requirement 8 | AC1, AC2, AC3, AC4, AC5 | `design.md#hook-design`, `design.md#phase-1-advisory-hooks`, `design.md#phase-2-completion-gates`, `design.md#phase-3-lifecycle-gates`, `design.md#recommended-hook-adoption-order` | T008, T009 | CLI hook smoke checks and unit tests | `skills/spec-lifecycle-manager/SKILL.md` |
| Requirement 9 | AC1, AC2, AC3, AC4 | `design.md#security`, `design.md#operational-considerations` | T011 | Dogfood prompt/resource/tool trust boundaries | `docs/design/spec-lifecycle-management.md`, `docs/reference/` |
| Requirement 10 | AC1, AC2, AC3 | `design.md#operational-considerations`, `design.md#mvp` | T011 | Dogfood metrics and usefulness review | `docs/design/spec-lifecycle-management.md`, `docs/reference/` |

## Design To Implementation Matrix

| Design Section | Requirements | Tasks | Interfaces Or Files | Verification |
|----------------|--------------|-------|---------------------|--------------|
| `design.md#mcp-resources` | Requirement 3, Requirement 6A | T004, T012 | `skills/spec-lifecycle-manager/scripts/spec_runtime.py`, `docs/specs/004-spec-management-mcp/traceability.md` | CLI `scan`, `summary`, and traceability lookup |
| `design.md#resource-payload-shape` | Requirement 3 | T004 | `skills/spec-lifecycle-manager/scripts/spec_runtime.py` | CLI JSON schema smoke tests |
| `design.md#implementation-packaging-decision` | Requirement 3 | T004 | `skills/spec-lifecycle-manager/scripts/spec_runtime.py` | Unit tests import the helper directly |
| `design.md#linter-design` | Requirement 4 | T005 | `skills/spec-lifecycle-manager/scripts/spec_runtime.py`, `tests/runtime/test_spec_runtime.py` | CLI `lint` and unit diagnostics |
| `design.md#artifact-rules` | Requirement 4 | T005 | `skills/spec-lifecycle-manager/scripts/spec_runtime.py` | Unit tests for required fields and sections |
| `design.md#task-planner-and-closure-checks` | Requirement 6 | T006 | `skills/spec-lifecycle-manager/scripts/spec_runtime.py`, `tests/runtime/test_spec_runtime.py` | CLI `next-task` and `closure-check` |
| `design.md#mcp-prompts` | Requirement 2 | T007 | prompt definition files TBD | Prompt discovery validation TBD |
| `design.md#prompt-template-pattern` | Requirement 2 | T007 | `skills/spec-lifecycle-manager/prompts/` | Prompt output shape validation |
| `design.md#client-support-fallback` | Requirement 2 | T007 | `skills/spec-lifecycle-manager/SKILL.md` | Natural-language fallback review |
| `design.md#hook-design` | Requirement 8 | T008 | `skills/spec-lifecycle-manager/scripts/spec_runtime.py`, `tests/runtime/test_spec_runtime.py` | CLI hook smoke checks |
| `design.md#phase-1-advisory-hooks` | Requirement 8 | T008 | `skills/spec-lifecycle-manager/scripts/spec_runtime.py` | Advisory `spec-file-changed` hook |
| `design.md#phase-2-completion-gates` | Requirement 8 | T009 | `skills/spec-lifecycle-manager/scripts/spec_runtime.py` | Completion and verification hook checks |
| `design.md#phase-3-lifecycle-gates` | Requirement 8 | T009 | `skills/spec-lifecycle-manager/scripts/spec_runtime.py` | Resume and closure hook checks |
| `design.md#recommended-hook-adoption-order` | Requirement 8 | T008 | `skills/spec-lifecycle-manager/scripts/spec_runtime.py` | Hook command supports first two hook types |
| `design.md#reconciliation-design` | Requirement 5 | T010 | `skills/spec-lifecycle-manager/scripts/spec_runtime.py` | CLI reconciliation checks |
| `design.md#review-packet-design` | Requirement 7 | T010 | `skills/spec-lifecycle-manager/scripts/spec_runtime.py` | Review packet generation |
| `design.md#packet-output-schema` | Requirement 7 | T010 | `skills/spec-lifecycle-manager/scripts/spec_runtime.py` | Review packet schema and result disposition validation |
| `design.md#security` | Requirement 9 | T011 | `docs/design/spec-lifecycle-management.md`, `docs/reference/` | Dogfood trust-boundary review |
| `design.md#operational-considerations` | Requirement 9, Requirement 10 | T011 | `docs/design/spec-lifecycle-management.md`, `docs/reference/` | Dogfood overhead and usefulness review |
| `design.md#mvp` | Requirement 10 | T011 | `docs/design/spec-lifecycle-management.md`, `docs/reference/` | Runtime MVP promotion review |
| `design.md#mcp-tools` | Requirement 6A | T012 | `skills/spec-lifecycle-manager/scripts/traceability_lookup.py`, `tests/traceability/test_traceability_lookup.py` | CLI lookup for task, requirement, design, and missing-row cases; unit tests |

## Open Decision Impact

| Decision ID | Blocks | Affected Requirements | Affected Tasks | Resolution Needed |
|-------------|--------|-----------------------|----------------|-------------------|
| none | none | none | none | none |

## Maintenance Notes

- Update this matrix when requirements, design sections, task IDs, verification
  gates, durable targets, or open decisions change.
- Keep task rows specific enough that an implementation agent can retrieve the
  full spec context before coding.
