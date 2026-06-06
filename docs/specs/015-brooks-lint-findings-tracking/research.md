---
title: Brooks-Lint findings tracking research
doc_type: spec
artifact_type: research
status: draft
owner: platform
last_reviewed: 2026-06-06
---

# Research

## Inputs

| Input | Observation | Implication |
|-------|-------------|-------------|
| Brooks-Audit output | Produces mode, scope, score, Mermaid graph, findings with Symptom/Source/Consequence/Remedy, and summary. | The durable register should preserve the same finding structure instead of inventing unrelated fields. |
| `.brooks-lint-history.json` | Stores score, finding counts, mode, date, and scope. | History is useful for trends but insufficient for detailed remediation tracking. |
| Existing backlog/roadmap docs | Already hold deferred work and sequencing. | Accepted or deferred findings should route into these documents when they outlive this spec. |
| Spec lifecycle docs | Current specs require traceability, verification, and closure promotion. | Brooks findings should follow the same lifecycle discipline as implementation work. |

## Seed Findings From First Architecture Audit

| Finding ID | Mode | Severity | Short Title | Initial State |
|------------|------|----------|-------------|---------------|
| BL-ARCH-001 | Architecture Audit | warning | `spec_runtime.py` is becoming the lifecycle god module. | needs-decision |
| BL-ARCH-002 | Architecture Audit | warning | Bundled plugin copy can drift from development skill. | needs-decision |
| BL-ARCH-003 | Architecture Audit | warning | Installer concentrates unrelated deployment concerns. | needs-decision |
| BL-ARCH-004 | Architecture Audit | suggestion | Hook runtime execution is hardwired to subprocess. | needs-decision |

## Seed Findings From First Tech Debt Assessment

| Finding ID | Mode | Risk | Severity | Pain | Spread | Priority | Classification | Intent | Short Title | Initial State |
|------------|------|------|----------|------|--------|----------|----------------|--------|-------------|---------------|
| BL-DEBT-001 | Tech Debt Assessment | Cognitive Overload | warning | 2 | 3 | 6 | Scheduled debt | accidental | `spec_runtime.py` concentrates many lifecycle responsibilities. | needs-decision |
| BL-DEBT-002 | Tech Debt Assessment | Knowledge Duplication | warning | 2 | 3 | 6 | Scheduled debt | accidental | Development skill and bundled plugin trees can drift. | needs-decision |
| BL-DEBT-003 | Tech Debt Assessment | Change Propagation | warning | 2 | 2 | 4 | Scheduled debt | accidental | Installer changes mix package copy, Codex cleanup, marketplace edits, and plugin registration. | needs-decision |
| BL-DEBT-004 | Tech Debt Assessment | Dependency Disorder | suggestion | 1 | 2 | 2 | Monitored debt | accidental | Hook checks shell out through a hardwired subprocess seam. | needs-decision |

## Tech Debt Assessment Summary

| Risk | Findings | Avg Priority | Classification | Intent |
|------|----------|--------------|----------------|--------|
| Cognitive Overload | 1 | 6.0 | Scheduled debt | accidental |
| Change Propagation | 1 | 4.0 | Scheduled debt | accidental |
| Knowledge Duplication | 1 | 6.0 | Scheduled debt | accidental |
| Accidental Complexity | 0 | 0.0 | none | none |
| Dependency Disorder | 1 | 2.0 | Monitored debt | accidental |
| Domain Model Distortion | 0 | 0.0 | none | none |

**Recommended focus:** address Cognitive Overload and Knowledge Duplication
first, because both have the highest priority and explain most future
maintenance drag.

## Seed Findings From First Health Dashboard

| Finding ID | Mode | Dimension | Severity | Short Title | Initial State |
|------------|------|-----------|----------|-------------|---------------|
| BL-HEALTH-001 | Health Dashboard | Architecture | warning | Installer fan-out is the main dependency-disorder signal. | needs-decision |
| BL-HEALTH-002 | Health Dashboard | Tech Debt | warning | `spec_runtime.py` remains the top maintainability hotspot. | needs-decision |
| BL-HEALTH-003 | Health Dashboard | Tech Debt | warning | Skill/plugin duplication remains a drift risk. | needs-decision |
| BL-HEALTH-004 | Health Dashboard | Tech Debt | warning | Installer orchestration remains scheduled debt. | needs-decision |
| BL-HEALTH-005 | Health Dashboard | Test Quality | suggestion | CLI and hook tests rely on subprocess fixtures in several places. | needs-decision |

## Health Dashboard Summary

Composite score: **93/100**.

| Dimension | Score | Top Finding |
|-----------|-------|-------------|
| Code Quality | skipped | No tracked code diff. |
| Architecture | 95/100 | Installer fan-out is the main dependency-disorder signal. |
| Tech Debt | 85/100 | `spec_runtime.py` and plugin drift are the highest debt signals. |
| Test Quality | 99/100 | Subprocess-heavy CLI/hook tests are a minor test-quality signal. |

The code-quality dimension was skipped because neither `git diff` nor
`git diff --cached` contained tracked file changes. Health score weighting was
redistributed across Architecture, Tech Debt, and Test Quality.

## Seed Findings From First Test Quality Review

| Finding ID | Mode | Risk | Severity | Short Title | Initial State |
|------------|------|------|----------|-------------|---------------|
| BL-TEST-001 | Test Quality Review | Test Duplication | warning | Spec-package fixture builders are duplicated across runtime, MCP, hook, and traceability tests. | needs-decision |
| BL-TEST-002 | Test Quality Review | Coverage Illusion | warning | Plugin package tests verify component presence but not full development-skill to bundled-plugin sync or installer behavior. | needs-decision |
| BL-TEST-003 | Test Quality Review | Test Brittleness | suggestion | CLI and hook tests rely on subprocess boundaries and exact stdout/stderr behavior. | needs-decision |

## Test Quality Review Summary

Test quality score: **89/100**.

```text
Unit tests:        5 files, 64 tests
Integration tests: 0 files, 0 tests
E2E tests:         0 files, 0 tests
Ratio:             Unit 100% : Integration 0% : E2E 0%
Coverage areas:    runtime, MCP adapter, traceability lookup, Codex hook, plugin package
Gaps:              installer behavior, full plugin/source sync, reusable fixture layer
Runtime:           about 3 seconds in current validation runs
```

The suite is fast and behavior-oriented enough for local feedback. The main
test-maintenance risk is that several tests construct similar spec packages by
hand, so lifecycle schema changes propagate through test fixtures. The main
coverage risk is that plugin packaging is checked for required files and
manifest wiring, but not for full source/bundle equality or installer cleanup
behavior.

## Candidate Durable Formats

### Option A: Markdown Register

Create `docs/reviews/brooks-lint/README.md` with a table plus per-finding
details.

- Pros: easy to review, merge-friendly, matches existing durable docs.
- Cons: harder to query without parser support.

### Option B: JSON Register

Create `docs/reviews/brooks-lint/findings.json`.

- Pros: deterministic validation and easier trend reconciliation.
- Cons: less readable for humans and more awkward for narrative evidence.

### Option C: Hybrid Register

Use Markdown as the source of truth and add optional runtime validation later.

- Pros: low ceremony now; can add validation if the register grows.
- Cons: schema consistency depends on documented sections until validation is
  added.

## Recommendation

Start with a Markdown register under `docs/reviews/brooks-lint/README.md`.
Use stable IDs and a fixed per-finding template. Defer JSON or runtime
validation until repeated Brooks runs show that manual consistency is not
enough.
