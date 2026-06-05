---
title: Documentation templates
doc_type: reference
status: active
owner: platform
last_reviewed: 2026-06-02
---

# Durable Documentation Templates

This directory provides optional durable documentation templates for projects
using the `spec-lifecycle-manager` skill. Use them only when the target project
does not already have an authoritative `docs/templates/` system, or when the
project explicitly chooses to adopt or adapt these templates.

These templates describe current-state documentation that should live with code
and reflect implemented or accepted behavior. They are not active spec-package
templates; temporary implementation specs use `../spec-package/`.

When a spec package closes, durable docs should contain the current-state
requirements, design, contract, operations, decision, and reference material
needed by future readers. The closed spec may be archived or removed according
to the repository lifecycle, but it should not remain the active source of truth
for implemented behavior.

## Core Rules

1. Every new document should use one primary document class.
2. If a document mixes multiple classes, split it instead of stretching one template too far.
3. Current-state operator guidance belongs in active docs folders such as `getting-started/`, `runbooks/`, `architecture/`, `integrations/`, `api/`, and `reference/`.
4. Historical rationale, superseded material, and design history should be captured in ADRs, current-state docs, active specs, or archived docs only when the context is still useful.
5. Runtime contracts should remain in machine-readable formats where possible, with companion prose only when needed.
6. Generated documents may use a simplified structure when a script owns most of their content, but they should still be clearly identified as generated and linked from the appropriate class folder.

## Required Metadata

Use this frontmatter on new markdown documents unless a template says otherwise or the document is generated:

```yaml
---
title: Short descriptive title
doc_type: guide|runbook|architecture|design|requirements|adr|integration|reference|checklist|history|governance
status: draft|active|code-derived|deprecated|superseded|archived
owner: team-or-person
last_reviewed: YYYY-MM-DD
---
```

Use `doc_type: spec` only for temporary spec-package files. Durable documents
should use the specific durable class that best describes their role.

Use `status: code-derived` only for documentation generated or assembled from
implemented code, repository config, and existing docs that is intended to
describe current behavior but is still awaiting stakeholder sign-off.

Additional ADR fields:

```yaml
decision_date: YYYY-MM-DD
deciders:
  - name-or-role
supersedes:
superseded_by:
```

For ADRs, the body `## Status` records the decision state, while frontmatter
`status` records the document lifecycle state. Keep them aligned where
practical: proposed decisions usually use `status: draft`, accepted decisions
usually use `status: active`, superseded decisions should set `superseded_by`,
and deprecated decisions should point readers to current guidance.

## Document Classes

### ADR

Use [adr.md](adr.md) for a durable architectural or technical decision that should remain understandable after implementation details change.

Store ADRs under `docs/adr/` using `NNNN-short-title.md`.

### Generic Document

Use [generic.md](generic.md) when none of the specific document classes below
fit cleanly. Prefer a specific template when the document is an operational
procedure, integration guide, architecture overview, ADR, reference, checklist,
history note, or feature spec.

### Architecture Overview

Use [architecture-overview.md](architecture-overview.md) for stable explanations of system shape, component responsibilities, and key flows.
Architecture overviews should link important code, config, contracts, and
validation evidence so future readers can check whether the architecture still
matches implementation.
Store architecture overviews under `docs/architecture/`.

### Requirements

Use [requirements.md](requirements.md) for current-state requirements that
describe implemented or accepted behavior without organizing the content as an
implementation backlog. Requirements should link to source code, config,
schemas, tests, runbooks, technical designs, and ADRs as evidence.
Store requirements under `docs/requirements/`.

### Technical Design

Use [technical-design.md](technical-design.md) for current-state design details
that are more specific than an architecture overview but should not be kept as
a feature implementation spec. Technical designs should explain components,
data/control flow, contracts, configuration, validation, security, and
operations.
Store technical designs under `docs/design/`.

### Getting Started Guide

Use [getting-started-guide.md](getting-started-guide.md) for setup and onboarding material aimed at developers or operators starting a task for the first time.

### Runbook

Use [runbook.md](runbook.md) for operational procedures with clear triggers, steps, validation, and escalation.
Runbooks that change or investigate implementation behavior should include linked docs and config/code touchpoints so the procedure stays traceable to schemas, runtime settings, code paths, and validation evidence.

### Integration Guide

Use [integration-guide.md](integration-guide.md) for MCP surface, language
adapter, parser/LSP, validation tool, plugin, or local runtime integration
behavior, contracts, configuration, and failure handling.

### API Contract Guide

Use [api-contract-guide.md](api-contract-guide.md) for prose that explains how
to read or apply a machine-readable contract such as an MCP tool schema,
resource schema, JSON schema, or API definition.
The machine-readable contract remains the source of truth; the guide should
record ownership, compatibility, error behavior, migration expectations, tests,
and related integration docs.

### Reference

Use [reference.md](reference.md) for factual reference material, assumptions,
limits, naming rules, capability matrices, or runtime dictionaries.

### Checklist

Use [checklist.md](checklist.md) for bounded review or rollout checklists with
explicit scope, completion criteria, owners, evidence, results, and follow-up
items.

### History Note

Use [history-note.md](history-note.md) for retained historical context that should not be mistaken for current guidance.

### Document Lifecycle

Use [document-lifecycle.md](document-lifecycle.md) for rules on when to keep a doc active, move it to history, or remove it.

### Governance Constitution

Use [governance-constitution.md](governance-constitution.md) for repository
principles, non-negotiable quality bars, validation rules, and decision gates
that agents must treat as authoritative.
Store governance docs under `docs/governance/`.

### Feature Spec Package

Feature spec packages are temporary delivery scaffolding, not durable
current-state documentation. Their canonical fallback templates live with the
`spec-lifecycle-manager` skill under:

```text
skills/spec-lifecycle-manager/references/spec-package/
```

Use those skill templates for structured work that needs requirements, design,
tasks, verification, change impact, and optional research or quickstart notes
tracked together. Spec packages can describe features, bug fixes, refactors,
migrations, operational changes, or documentation-only changes.

This directory is reserved for durable document classes that should live with
the code and reflect current implementation state. Copy or adapt only the
document classes needed for a selected project.

## When To Split A Document

Split a document when it combines:

- current-state requirements and detailed technical design
- accepted decision rationale and current architecture explanation
- integration overview and step-by-step incident handling
- reference data and operational procedure
- history or backlog notes and current operator guidance

## Naming Guidance

- Use kebab-case file names.
- Prefer role-based names such as `system-architecture.md` or `deployment-runbook.md`.
- Use `NNNN-short-title.md` for ADRs.
- Avoid vague names such as `notes.md`, `misc.md`, or `design-v2.md`.
