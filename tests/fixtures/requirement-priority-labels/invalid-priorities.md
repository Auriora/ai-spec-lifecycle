---
title: Invalid requirement priority fixture
doc_type: spec
artifact_type: requirements
status: draft
owner: platform
last_reviewed: 2026-07-05
---

# Requirements

## Durable Source Baseline

- Fixture baseline.

## Goals

- Exercise invalid priority diagnostics.

## Non-Goals

- Do not exercise closure semantics.

## Requirements

### Requirement 1: Duplicate Fixture

**Priority:** must-have
**Priority:** should-have

#### Acceptance Criteria

1. GIVEN context, WHEN duplicate priority is parsed, THEN THE SYSTEM SHALL report it.

### Requirement 2: Shorthand Fixture

**Priority:** must

#### Acceptance Criteria

1. GIVEN context, WHEN shorthand priority is parsed, THEN THE SYSTEM SHALL report it.

### Requirement 3: Unknown Fixture

**Priority:** urgent

#### Acceptance Criteria

1. GIVEN context, WHEN unknown priority is parsed, THEN THE SYSTEM SHALL report it.

### Requirement 4: Exclusion Fixture

**Priority:** won't-have

#### Acceptance Criteria

1. GIVEN context, WHEN exclusion priority is parsed, THEN THE SYSTEM SHALL report it.

## Correctness Properties

- CP-001: Fixture diagnostics parse.

## Success Criteria

- Parser returns invalid priority diagnostics.
