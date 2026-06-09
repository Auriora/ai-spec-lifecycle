---
title: Feature requirements title
doc_type: spec
artifact_type: requirements
status: draft
owner: team-or-person
last_reviewed: YYYY-MM-DD
---

# Requirements

## Introduction

Brief description of the change. What problem is being solved and why it matters.

## Goals

- Goal

## Non-Goals

- Non-goal

## Glossary

| Term | Definition |
|------|-----------|
| Term | Definition |

## Durable Source Baseline

Reference durable source-of-truth docs, contracts, schemas, runbooks,
governance files, or code-derived references that describe current behavior
before this change.

| Source | Current behavior relied on | Confidence | Notes |
|--------|----------------------------|------------|-------|
| `docs/path/to/doc.md` | Current behavior summary | high | |
| none found | Documentation gap summary | low | Promote accepted behavior to `docs/path/to/new-doc.md`. |

If no durable source exists, record the gap and the durable document that should
become the source of truth after promotion.

## Requirements

### Requirement 1: Title

**User Story:** As a [role], I want [feature], so that [benefit]

#### Acceptance Criteria

1. GIVEN [context], WHEN [action], THEN [outcome]
2. WHERE [condition applies], THE SYSTEM SHALL [behavior]

### Requirement 2: Title

**User Story:** As a [role], I want [feature], so that [benefit]

#### Acceptance Criteria

1. IF [condition], THEN THE SYSTEM SHALL [behavior]
2. WHILE [state], THE SYSTEM SHALL [behavior]

## Correctness Properties

Properties that must hold for the system to be considered correct. These inform
property-based testing and should be referenced from task-level test work when
they apply. Use the target repository's normal property-test tool when one is
already accepted; otherwise record the dependency decision in `design.md` or
`open-decisions.md`.

- **CP-001**: [Invariant or property description]
- **CP-002**: [Invariant or property description]

## Technical Context

- **Language/Version:**
- **Primary Dependencies:**
- **Target Platform:**
- **Constraints:**
- **Performance Goals:**

## Success Criteria

- **SC-001**: [Measurable outcome]
- **SC-002**: [Measurable outcome]

## Related Artifacts

- Change Impact:
- Design:
- Tasks:
- Verification:
