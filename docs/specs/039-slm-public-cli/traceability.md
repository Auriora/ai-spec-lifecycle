---
title: Public slm CLI traceability matrix
doc_type: spec
artifact_type: traceability
status: draft
owner: platform
last_reviewed: 2026-07-19
---

# Traceability Matrix

## Purpose

Connect the public CLI contract to shared lifecycle ownership, implementation
tasks, package validation, and durable promotion. Before implementing a task,
review its row and the linked requirement/design sections; do not infer the
public contract from `tasks.md` alone.

## Task To Context Matrix

| Task ID | Requirements | Acceptance Criteria | Design Sections | Change Impact | Verification | Durable Targets | Open Decisions |
|---------|--------------|---------------------|-----------------|---------------|--------------|-----------------|----------------|
| T001 | Requirement 1, Requirement 2, Requirement 3, Requirement 4, Requirement 5, Requirement 6, Requirement 7, Requirement 8, Requirement 9 | all contract criteria | `design.md#requirement-coverage`, `design.md#data-models` | all proposed changes | Contract, filter, output, packaging, and read-only gates | none yet | none |
| T002 | Requirement 2, Requirement 3, Requirement 4, Requirement 5, Requirement 6 | R2 AC1-AC5; R3 AC1-AC4; R4 AC1-AC7; R5 AC1-AC5; R6 AC1-AC5 | `design.md#components-and-changes`, `design.md#algorithms-and-logic` | Active/task/requirement/history views | Shared core and parser gates | runtime/design references | none |
| T003 | Requirement 2, Requirement 3, Requirement 4, Requirement 5, Requirement 6 | same as T002 | `design.md#correctness-property-coverage` | View semantics | Focused shared-record gate | none | none |
| T004 | Requirement 2, Requirement 3, Requirement 4, Requirement 5, Requirement 6, Requirement 7, Requirement 8, Requirement 9 | R2-R9 CLI criteria | `design.md#data-flow`, `design.md#function-signatures-and-interfaces`, `design.md#error-handling` | Public inspection commands and output | CLI, output parity, root, and read-only gates | runtime reference | none |
| T005 | Requirement 2, Requirement 3, Requirement 4, Requirement 5, Requirement 6, Requirement 7, Requirement 8, Requirement 9 | R2-R9 CLI criteria | `design.md#validation-strategy` | Public inspection commands and output | Focused public CLI gate | none | none |
| T006 | Requirement 1, Requirement 8, Requirement 9 | R1 AC1-AC4; R8 AC3-AC4; R9 AC2-AC4 | `design.md#system-architecture`, `design.md#migration-and-compatibility` | Bin rename and install routing | Dispatcher, bin, interpreter, and package-contract gates | README and install reference | none |
| T007 | Requirement 1, Requirement 7, Requirement 8, Requirement 9 | R1 AC1-AC4; R7 AC1-AC5; R8 AC1-AC4; R9 AC1-AC4 | `design.md#operational-considerations` | Packaged cross-platform operation | Bundle, dry-run, tarball, and CI gates | install/runtime references | none |
| T008 | Requirement 1, Requirement 2, Requirement 3, Requirement 4, Requirement 5, Requirement 6, Requirement 7, Requirement 8, Requirement 9 | durable promotion criteria | `design.md#slice-boundary-and-residual-architecture` | All promotion targets | Durable-doc review gate | README, design, runtime, install, release notes | none |
| T009 | Requirement 1, Requirement 2, Requirement 3, Requirement 4, Requirement 5, Requirement 6, Requirement 7, Requirement 8, Requirement 9 | all | `design.md#validation-strategy` | All proposed changes | Full validation and semantic closure gates | closure log/archive index after delivery | none |

## Requirement To Delivery Matrix

| Requirement | Priority | Acceptance Criteria | Design Sections | Tasks | Verification | Durable Targets | Coverage State | Residual Destination |
|-------------|----------|---------------------|-----------------|-------|--------------|-----------------|----------------|----------------------|
| Requirement 1 | must-have | AC1, AC2, AC3, AC4 | Overview; System Architecture; Migration and Compatibility | T001, T006, T007, T008, T009 | Bin identity, dispatcher, package, tarball gates | README; install reference; `docs/release-notes/v0.5.0.md` | complete | none |
| Requirement 2 | must-have | AC1, AC2, AC3, AC4, AC5 | Data Models; Data Flow; Algorithms and Logic | T001-T005, T008, T009 | Spec inventory and empty-state gates | README; runtime reference | complete | none |
| Requirement 3 | must-have | AC1, AC2, AC3, AC4 | Algorithms and Logic; Error Handling | T001-T005, T008, T009 | Resolution and ambiguity gates | runtime reference | complete | none |
| Requirement 4 | must-have | AC1, AC2, AC3, AC4, AC5, AC6, AC7 | Data Models; Algorithms and Logic; Interfaces | T001-T005, T008, T009 | Task filter and next equivalence gates | README; runtime reference | complete | none |
| Requirement 5 | must-have | AC1, AC2, AC3, AC4, AC5 | Components and Changes; Data Models | T001-T005, T008, T009 | Requirement parser/projection gates | README; runtime reference | complete | none |
| Requirement 6 | must-have | AC1, AC2, AC3, AC4, AC5 | Algorithms and Logic; Error Handling | T001-T005, T008, T009 | Archive/history gates | README; runtime reference | complete | none |
| Requirement 7 | must-have | AC1, AC2, AC3, AC4, AC5 | Data Models; Data Flow; Interfaces | T001, T004-T009 | Table/JSON parity and path gates | runtime/design references | complete | none |
| Requirement 8 | should-have | AC1, AC2, AC3, AC4 | Data Flow; Error Handling | T001, T004-T009 | Root discovery, exit-code, and cross-platform CI gates | runtime/install references | complete | none |
| Requirement 9 | must-have | AC1, AC2, AC3, AC4 | Security; Migration; Operational Considerations | T001, T004-T009 | Read-only, interpreter, bundle, tarball, and installed-package matrix gates | README; install/runtime references | complete | none |

## Correctness Property Coverage

| Property | Requirements | Design Sections | Tasks | Tests Or Verification | Residual Risk |
|----------|--------------|-----------------|-------|-----------------------|---------------|
| CP-001 | Requirement 4 | Correctness Property Coverage; Algorithms and Logic | T001-T005, T009 | Marker/state table-driven tests | none after all current and legacy markers pass |
| CP-002 | Requirement 4 | Algorithms and Logic | T001-T005, T009 | Core/CLI next equivalence fixtures | none after blocked and runnable cases pass |
| CP-003 | Requirement 7 | Data Models; Data Flow | T001, T004, T005, T007, T009 | Shared-record renderer parity tests | display truncation must not change identity |
| CP-004 | Requirement 9 | Security, Trust, and Access | T001, T004, T005, T007, T009 | Worktree before/after fingerprint | installer explicitly excluded |
| CP-005 | Requirement 3 | Algorithms and Logic; Error Handling | T001-T005, T009 | Multiple-active selection tests | none |
| CP-006 | Requirement 6 | Algorithms and Logic | T001-T005, T009 | Removed package and malformed archive fixtures | none after diagnostics are fail-closed |
| CP-007 | Requirement 5 | Components and Changes; Data Models | T001-T005, T009 | Canonical/shorthand/invalid/missing priority tests | `unspecified` remains view-only |

## Design To Implementation Matrix

| Design Section | Requirements | Tasks | Interfaces Or Files | Verification | Coverage State | Residual Destination |
|----------------|--------------|-------|---------------------|--------------|----------------|----------------------|
| System Architecture | Requirements 1, 9 | T006, T007 | package dispatcher, Python entrypoint, shared lifecycle modules | Node/package/tarball gates | complete | none |
| Components and Changes | Requirements 1-9 | T002, T004, T006-T008 | package, source, bundles, tests, durable docs | focused and full suites | complete | none |
| Data Models | Requirements 2, 4-7 | T001-T005 | normalized command records and envelope | structural and parity tests | complete | none |
| Algorithms and Logic | Requirements 3-6 | T002-T005 | selection, filters, history projection | focused Python tests | complete | none |
| Error Handling | Requirements 3, 6, 8 | T001, T004, T005, T007 | CLI and dispatcher | exit/stderr tests | complete | none |
| Security, Trust, and Access | Requirement 9 | T001, T004-T007, T009 | argument-vector launch and read-only queries | injection/read-only tests and review | complete | none |
| Migration and Compatibility | Requirements 1, 9 | T006-T009 | bin map and durable docs | package metadata, release review, and green cross-platform matrix | complete | none |

## Open Decision Impact

| Decision ID | Blocks | Affected Requirements | Affected Tasks | Resolution Needed |
|-------------|--------|-----------------------|----------------|-------------------|
| none | none | all | all | User decisions are recorded as resolved in `requirements.md` and `design.md`. |

## Maintenance Notes

- Update coverage states as implementation and evidence land.
- Before closure, every `not-covered` row must become `complete`, be rejected
  with rationale, or be routed to exactly one durable destination.
- If command or output semantics change, update requirements and quickstart
  before changing this matrix.
- Use MCP `traceability_lookup` for bounded task context when available.
