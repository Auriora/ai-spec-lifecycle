---
title: Spec archive index runtime traceability
doc_type: spec
artifact_type: traceability
status: draft
owner: platform
last_reviewed: 2026-06-06
---

# Traceability Matrix

## Task To Context Matrix

| Task ID | Requirements | Acceptance Criteria | Design Sections | Change Impact | Verification | Durable Targets | Open Decisions |
|---------|--------------|---------------------|-----------------|---------------|--------------|-----------------|----------------|
| T001 | Requirement 1, Requirement 2, Requirement 3, Requirement 4 | all acceptance criteria | `design.md#overview`, `design.md#high-level-design` | none | `verification.md#quality-gates` | `docs/specs/011-spec-archive-index-runtime/` | none |
| T002 | Requirement 1, Requirement 4 | Requirement 1 AC1, AC2; Requirement 4 AC1, AC2, AC3 | `design.md#data-model`, `design.md#operational-considerations` | add archive index durable doc | `verification.md#durable-promotion-and-cleanup` | `docs/history/spec-archive-index.md`, `docs/design/spec-lifecycle-management.md`, `docs/README.md` | Git validation depth |
| T003 | Requirement 1, Requirement 2 | Requirement 1 AC3; Requirement 2 AC1, AC2, AC3 | `design.md#archive-index-parser`, `design.md#validation-rules` | add runtime parser | `verification.md#validation-commands` | `docs/reference/spec-lifecycle-runtime.md` | Git validation depth |
| T004 | Requirement 2, Requirement 3 | Requirement 2 AC1, AC2; Requirement 3 AC1, AC2 | `design.md#cli-shape`, `design.md#validation-rules` | add runtime command | `verification.md#validation-commands` | `docs/reference/spec-lifecycle-runtime.md` | none |
| T005 | Requirement 3 | Requirement 3 AC1, AC2, AC3 | `design.md#mcp-shape` | add MCP read surface | `verification.md#validation-commands` | `docs/reference/spec-lifecycle-runtime.md` | none |
| T006 | Requirement 1, Requirement 2, Requirement 4 | Requirement 1 AC1, AC2, AC3; Requirement 2 AC1, AC2, AC3; Requirement 4 AC1, AC2, AC3 | `design.md#validation-rules`, `design.md#operational-considerations` | populate archive index | `verification.md#evidence-log` | `docs/history/spec-archive-index.md` | cleanup timing |
| T007 | Requirement 4 | Requirement 4 AC1, AC2, AC3 | `design.md#operational-considerations` | update planning docs | `verification.md#task-evidence` | `docs/backlog/README.md`, `docs/roadmap/README.md` | none |
| T008 | Requirement 1, Requirement 2, Requirement 4 | all acceptance criteria | `design.md#operational-considerations` | close spec | `verification.md#readiness-decision` | `docs/history/spec-closure-log.md` | cleanup timing |

## Requirement To Delivery Matrix

| Requirement | Acceptance Criteria | Design Sections | Tasks | Verification | Durable Targets |
|-------------|---------------------|-----------------|-------|--------------|-----------------|
| Requirement 1 | AC1, AC2, AC3 | data model, parser, validation rules | T001, T002, T003, T006, T008 | quality gates, evidence log | archive index |
| Requirement 2 | AC1, AC2, AC3 | validation rules, CLI shape | T001, T003, T004, T006, T008 | validation commands | runtime docs |
| Requirement 3 | AC1, AC2, AC3 | CLI shape, MCP shape | T001, T004, T005 | validation commands | runtime docs, MCP server |
| Requirement 4 | AC1, AC2, AC3 | operational considerations | T001, T002, T006, T007, T008 | durable promotion and cleanup | lifecycle docs, roadmap, backlog |

## Design To Implementation Matrix

| Design Section | Requirements | Tasks | Interfaces Or Files | Verification |
|----------------|--------------|-------|---------------------|--------------|
| `design.md#overview` | Requirement 1, Requirement 2, Requirement 3, Requirement 4 | T001 | spec package | spec lint |
| `design.md#high-level-design` | Requirement 1, Requirement 2, Requirement 4 | T001, T002 | archive index and lifecycle docs | quality gates |
| `design.md#data-model` | Requirement 1, Requirement 4 | T002, T006 | `docs/history/spec-archive-index.md` | durable promotion |
| `design.md#archive-index-parser` | Requirement 1, Requirement 2 | T003 | `spec_runtime.py` | runtime tests |
| `design.md#validation-rules` | Requirement 1, Requirement 2, Requirement 4 | T003, T004, T006 | `spec_runtime.py`, archive index | validation commands |
| `design.md#cli-shape` | Requirement 2, Requirement 3 | T004 | `spec_runtime.py` CLI | runtime tests |
| `design.md#mcp-shape` | Requirement 3 | T005 | `spec_mcp_server.py` | MCP tests |
| `design.md#operational-considerations` | Requirement 4 | T002, T006, T007, T008 | durable docs and closure log | readiness decision |

## Open Decision Impact

| Decision ID | Blocks | Affected Requirements | Affected Tasks | Resolution Needed |
|-------------|--------|-----------------------|----------------|-------------------|
| Git validation depth | T003 strictness | Requirement 1, Requirement 2 | T002, T003 | Decide whether first implementation validates commit syntax only or calls Git. |
| Cleanup timing | T008 cleanup action | Requirement 4 | T006, T008 | Decide whether this spec only indexes retained packages or also removes old packages later. |
