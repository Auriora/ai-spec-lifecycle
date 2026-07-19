---
title: Lifecycle adoption workflow traceability
doc_type: spec
artifact_type: traceability
status: draft
owner: platform
last_reviewed: 2026-07-19
---

# Lifecycle Adoption Workflow Traceability

## Task To Context Matrix

| Task ID | Requirements | Acceptance Criteria | Design Sections | Change Impact | Verification | Durable Targets | Open Decisions |
|---------|--------------|---------------------|-----------------|---------------|--------------|-----------------|----------------|
| T001 | Requirement 1; Requirement 2; Requirement 3; Requirement 4; Requirement 5; Requirement 6 | Requirement 1 AC1; Requirement 1 AC2; Requirement 1 AC3; Requirement 2 AC1; Requirement 2 AC2; Requirement 2 AC3; Requirement 2 AC4; Requirement 3 AC1; Requirement 3 AC2; Requirement 3 AC3; Requirement 3 AC4; Requirement 4 AC1; Requirement 4 AC2; Requirement 4 AC3; Requirement 4 AC4; Requirement 5 AC1; Requirement 5 AC2; Requirement 5 AC3; Requirement 5 AC4; Requirement 5 AC5; Requirement 6 AC1; Requirement 6 AC2; Requirement 6 AC3; Requirement 6 AC4 | Resolved decisions; slice boundary | All proposed changes and unchanged areas | Quality gates | backlog, roadmap | none |
| T002 | Requirement 2; Requirement 4 | Requirement 2 AC1; Requirement 2 AC2; Requirement 2 AC3; Requirement 2 AC4; Requirement 4 AC1; Requirement 4 AC2; Requirement 4 AC3; Requirement 4 AC4 | Implementation-start prompt; composition contract | Implementation-start composition; MCP recovery | Prompt/runtime tests | none | none |
| T003 | Requirement 2; Requirement 4 | Requirement 2 AC1; Requirement 2 AC2; Requirement 2 AC3; Requirement 2 AC4; Requirement 4 AC1; Requirement 4 AC2; Requirement 4 AC3; Requirement 4 AC4 | Implementation-start prompt; composition contract; compatibility | Implementation-start composition; MCP recovery | Prompt/runtime tests | lifecycle design, runtime reference | none |
| T004 | Requirement 3; Requirement 4 | Requirement 3 AC1; Requirement 3 AC2; Requirement 3 AC3; Requirement 3 AC4; Requirement 4 AC1; Requirement 4 AC2; Requirement 4 AC3; Requirement 4 AC4 | Shared next-action routing; interface presentation; next-action ordering | Evidence/promotion ordering; MCP recovery | Runtime/MCP tests | none | none |
| T005 | Requirement 3; Requirement 4 | Requirement 3 AC1; Requirement 3 AC2; Requirement 3 AC3; Requirement 3 AC4; Requirement 4 AC1; Requirement 4 AC2; Requirement 4 AC3; Requirement 4 AC4 | Shared next-action routing; interface presentation; next-action ordering | Evidence/promotion ordering; MCP recovery | Runtime/MCP tests | lifecycle design, runtime reference | none |
| T006 | Requirement 6 | Requirement 6 AC1; Requirement 6 AC2; Requirement 6 AC3; Requirement 6 AC4 | Advisory hook routing; advisory hook contract | State-specific advisory hook guidance | Hook runtime and wrapper tests | none | none |
| T007 | Requirement 6 | Requirement 6 AC1; Requirement 6 AC2; Requirement 6 AC3; Requirement 6 AC4 | Advisory hook routing; advisory hook contract | State-specific advisory hook guidance | Hook runtime and wrapper tests | runtime reference | none |
| T008 | Requirement 5 | Requirement 5 AC1; Requirement 5 AC2; Requirement 5 AC3; Requirement 5 AC4; Requirement 5 AC5 | Skill and capability guidance; mandatory skill rule inventory; compatibility | Concise skill entrypoint | Inventory, byte, skill, and parity checks | skill, references, plugin bundles | none |
| T009 | Requirement 2; Requirement 3; Requirement 4; Requirement 5; Requirement 6 | Requirement 2 AC1; Requirement 2 AC2; Requirement 2 AC3; Requirement 2 AC4; Requirement 3 AC1; Requirement 3 AC2; Requirement 3 AC3; Requirement 3 AC4; Requirement 4 AC1; Requirement 4 AC2; Requirement 4 AC3; Requirement 4 AC4; Requirement 5 AC1; Requirement 5 AC2; Requirement 5 AC3; Requirement 5 AC4; Requirement 5 AC5; Requirement 6 AC1; Requirement 6 AC2; Requirement 6 AC3; Requirement 6 AC4 | Validation strategy; compatibility | All implementation changes | Validation commands and quality gates | verification record | none |
| T010 | Requirement 1 | Requirement 1 AC1; Requirement 1 AC2; Requirement 1 AC3 | External dogfood evidence; security, trust, and privacy | Qualified external adoption finding | External report review | dogfood evaluation | none |
| T009.1 | Requirement 4; Requirement 5 | Requirement 4 AC1; Requirement 4 AC2; Requirement 4 AC3; Requirement 5 AC2; Requirement 5 AC3; Requirement 5 AC4 | Interface presentation; skill and capability guidance; compatibility | Capability status and bounded client metadata | Focused runtime/MCP/schema tests; full regression; package and sync checks | runtime reference and skill bundles | none |
| T011 | Requirement 1; Requirement 2; Requirement 3; Requirement 4; Requirement 5; Requirement 6 | Requirement 1 AC1; Requirement 1 AC2; Requirement 1 AC3; Requirement 2 AC1; Requirement 2 AC2; Requirement 2 AC3; Requirement 2 AC4; Requirement 3 AC1; Requirement 3 AC2; Requirement 3 AC3; Requirement 3 AC4; Requirement 4 AC1; Requirement 4 AC2; Requirement 4 AC3; Requirement 4 AC4; Requirement 5 AC1; Requirement 5 AC2; Requirement 5 AC3; Requirement 5 AC4; Requirement 5 AC5; Requirement 6 AC1; Requirement 6 AC2; Requirement 6 AC3; Requirement 6 AC4 | Slice boundary; operational considerations | Promotion targets and unchanged areas | Durable promotion checks | design, runtime, dogfood, backlog, roadmap | none |
| T012 | Requirement 1; Requirement 2; Requirement 3; Requirement 4; Requirement 5; Requirement 6 | Requirement-level closure reconciliation | Entire accepted design | Promotion targets and unchanged areas | Closure and cleanup | closure log, archive index | none |

## Requirement To Delivery Matrix

| Requirement | Priority | Acceptance Criteria | Design Sections | Tasks | Verification | Durable Targets | Coverage State | Residual Destination |
|-------------|----------|---------------------|-----------------|-------|--------------|-----------------|----------------|----------------------|
| Requirement 1 | must-have | Requirement 1 AC1; Requirement 1 AC2; Requirement 1 AC3 | External dogfood evidence; security, trust, and privacy | T001, T010, T011, T012 | Qualified external report review | dogfood evaluation | covered | none |
| Requirement 2 | must-have | Requirement 2 AC1; Requirement 2 AC2; Requirement 2 AC3; Requirement 2 AC4 | Implementation-start prompt; composition contract | T001, T002, T003, T009, T011, T012 | Prompt/runtime fixtures | lifecycle design, runtime reference | covered | none |
| Requirement 3 | must-have | Requirement 3 AC1; Requirement 3 AC2; Requirement 3 AC3; Requirement 3 AC4 | Shared next-action routing; next-action ordering | T001, T004, T005, T009, T011, T012 | Transition fixtures | lifecycle design, runtime reference | covered | none |
| Requirement 4 | must-have | Requirement 4 AC1; Requirement 4 AC2; Requirement 4 AC3; Requirement 4 AC4 | Interface presentation; error handling | T001, T002, T003, T004, T005, T009, T009.1, T011, T012 | MCP-visible/no-MCP tests | runtime reference, skill | covered | none |
| Requirement 5 | must-have | Requirement 5 AC1; Requirement 5 AC2; Requirement 5 AC3; Requirement 5 AC4; Requirement 5 AC5 | Skill/capability guidance; mandatory skill rule inventory; compatibility | T001, T008, T009, T009.1, T011, T012 | Inventory, byte, skill, capability-status, and parity checks | skill, references, plugin bundles | covered | none |
| Requirement 6 | must-have | Requirement 6 AC1; Requirement 6 AC2; Requirement 6 AC3; Requirement 6 AC4 | Advisory hook routing; advisory hook contract | T001, T006, T007, T009, T011, T012 | Hook-state fixtures | runtime reference, hook runtime | covered | none |

## Correctness Property Coverage

| Property | Requirements | Design Sections | Tasks | Tests Or Verification | Residual Risk |
|----------|--------------|-----------------|-------|-----------------------|---------------|
| CP-001 | Requirement 2; Requirement 3 | Composition contract; next-action ordering | T002, T004, T009 | Table-driven blocking fixtures | Semantic correctness remains reviewed |
| CP-002 | Requirement 4 | Interface presentation | T002, T004, T009, T009.1 | MCP-visible/no-MCP and initialization-metadata assertions | Host configuration may differ |
| CP-003 | Requirement 6 | Advisory hook contract | T006, T007, T009 | Ordinary-write, resume, closure, debounce, and quiet-state fixtures | Client hook delivery may differ |
| CP-004 | Requirement 1 | External dogfood evidence | T010, T011 | External qualification and claim review | Exact findings may remain provisional |
| CP-005 | Requirement 5 | Mandatory skill rule inventory | T008, T009, T009.1 | Inventory, byte ceiling, skill validation, capability status, and bundle parity | Client loader behavior varies |
| CP-006 | Requirement 2 | Composition contract | T002, T003, T009 | Repeatability and unchanged-worktree checks | External tools may change evidence |

## Success Criterion Coverage

| Success Criterion | Requirements | Tasks | Verification |
|-------------------|--------------|-------|--------------|
| SC-001 | Requirement 2 | T002, T003, T009 | Prompt composition and routing fixtures |
| SC-002 | Requirement 3 | T004, T005, T009 | Evidence/promotion/closure transition fixtures |
| SC-003 | Requirement 4 | T002, T003, T004, T005, T009, T009.1 | MCP-visible, no-MCP, and initialization-state adapter assertions |
| SC-004 | Requirement 5 | T008, T009, T009.1 | Mandatory inventory, `wc -c`, capability-status, skill validation, and bundle parity |
| SC-005 | Requirement 6 | T006, T007, T009 | Ordinary-write, resume, closure, debounce, and quiet-hook fixtures |
| SC-006 | Requirement 1 | T010, T011 | External report qualification and durable dogfood review |

## Design To Implementation Matrix

| Design Section | Requirements | Tasks | Interfaces Or Files | Verification | Coverage State | Residual Destination |
|----------------|--------------|-------|---------------------|--------------|----------------|----------------------|
| Implementation-start prompt and composition | Requirement 2; Requirement 4 | T002, T003, T009 | prompt definitions and mirrors | Prompt and runtime tests | implemented; integrated validation pending T009 | Spec 038 |
| Shared next-action routing | Requirement 3; Requirement 4 | T004, T005, T009 | lifecycle action builder, adapters, fixtures | Transition and interface fixtures | implemented; integrated validation pending T009 | Spec 038 |
| Skill and capability guidance | Requirement 5 | T008, T009, T009.1 | skill, references, capability output, bundle mirrors | Inventory, byte, capability-status, skill, and parity checks | implemented; promotion pending T011 | Spec 038 |
| Capability status and client observation | Requirement 4; Requirement 5 | T009.1 | capability core, MCP session adapter, schema, mirrors | Initialization retention, missing-client, action-authority, and recovery-label tests | implemented; promotion pending T011 | Spec 038 |
| Advisory hook routing | Requirement 6 | T006, T007, T009 | hook runtime, wrapper, and fixtures | Hook-state tests | implemented; integrated validation pending T009 | Spec 038 |
| External dogfood evidence | Requirement 1 | T010, T011 | reviewed report receipt and durable dogfood doc | Qualification review | reviewed; durable promotion pending T011 | Spec 038 |
| Durable promotion | Requirement 1; Requirement 2; Requirement 3; Requirement 4; Requirement 5; Requirement 6 | T011, T012 | design, runtime, dogfood, backlog, roadmap | Promotion and closure checks | planned | Spec 038 |

## Open Decision Impact

| Decision ID | Status | Affected Requirements | Affected Tasks | Resolution |
|-------------|--------|-----------------------|----------------|------------|
| DR-001 | resolved | Requirement 2; Requirement 4 | T002, T003 | Use a declarative `implementation-start` prompt over existing tools; no shared-core aggregate in this slice. |
| DR-002 | resolved | Requirement 5 | T008, T009 | Preserve eight mandatory-rule categories and reduce source `SKILL.md` to no more than 37,399 bytes from the 53,427-byte baseline. |
| DR-003 | resolved | Requirement 6 | T006, T007, T009 | Ordinary write hooks never execute or recommend full lint; only explicit resume, closure, or direct validation boundaries may run it. |

## Durable Promotion Matrix

| Spec content | Current source | Promotion destination | Task | Status |
|--------------|----------------|-----------------------|------|--------|
| Implementation-start and action ordering | requirements/design | `docs/design/spec-lifecycle-management.md` | T011 | pending validation |
| MCP/CLI, hook, and capability contract | requirements/design | `docs/reference/spec-lifecycle-runtime.md` | T011 | pending validation |
| Qualified external findings | research/verification | `docs/reference/spec-lifecycle-dogfood-evaluation.md` | T010, T011 | reviewed; promotion pending T011 |
| Delivery and residual routing | change impact/verification | `docs/backlog/README.md`, `docs/roadmap/README.md` | T011 | pending validation |
| Mandatory skill behavior | requirements/design | source skill, references, Codex and Claude bundles | T008, T009 | implemented; integrated validation pending T009 |

## Review Reconciliation

Reviewed against the current requirements, resolved design decisions, resliced
tasks, and verification plan on 2026-07-18. Explicit identifiers resolve through
runtime task context, all must-have requirements are covered by planned
delivery, and SC-001 through SC-006 have direct task and verification mappings.

## Related Artifacts

- Requirements: `requirements.md`
- Research: `research.md`
- Design: `design.md`
- Change Impact: `change-impact.md`
- Tasks: `tasks.md`
- Verification: `verification.md`
