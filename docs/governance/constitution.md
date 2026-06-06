---
title: Agent development lifecycle constitution
doc_type: governance
status: active
owner: platform
last_reviewed: 2026-06-06
---

# Agent Development Lifecycle Constitution

## Purpose

Define the standing principles that govern AI-assisted implementation specs,
durable documentation, validation, review, and closure in this repository.

## Principles

### Specs Are Temporary

Feature specs under `docs/specs/[###-slug]/` are delivery scaffolding with a
finite lifetime. They guide active work, but they are not the long-term source
of truth for implemented behavior.

### Durable Docs Reflect Current State

Durable documentation should live with the repository, remain discoverable from
the docs index, and describe the current implementation state. When a spec
changes accepted behavior, the lasting content must be promoted into durable
docs before closure.

Active specs must reference the durable source of truth for current behavior
when one exists. If no durable source exists, the spec must record the gap and
the durable document that should become the source of truth after promotion.

### Evidence Before Completion

Tasks move to `done` only when acceptance criteria are met and evidence is
recorded. Evidence can be automated test output, validation commands, review
notes, logs, screenshots, commits, or documented manual verification with
residual risk.

### Spec Context Before Implementation

When an active spec exists, agents must not implement from `tasks.md` alone.
Task entries are execution indexes. Agents must review the relevant
requirements, acceptance criteria, design, verification expectations, durable
source baseline, traceability context when present, and open decisions before
implementation or closure.

### Risk Gates Require Decisions

Work that affects security, privacy, credentials, production data,
migrations, public contracts, schemas, governance, lifecycle policy, hooks,
MCP surfaces, or cross-module architecture requires explicit decision-gate
handling before implementation proceeds. If governance conflicts with an
active spec or durable design doc, governance takes precedence unless the user
explicitly requests a governance update.

### Parallel Agent Work Is Bounded

Parallel agents and subagents may be used for bounded read-only investigation,
independent review, validation design, or non-overlapping implementation
slices. Overlapping write scopes or conflicting findings must be reconciled by
the lead agent or developer operator before implementation or closure
continues.

### Migration Is A Decision

Older spec formats may be migrated to the current package shape, but migration
is a decision gate, not an automatic prerequisite. Completed specs should be
removed from the active docs tree after durable promotion unless an explicit
archive or retention decision is made.

### Repository Structure Wins

Agents must follow repository instructions, documented templates, governance,
and lifecycle rules before falling back to bundled skill references.

### Source Trees Stay Focused

Do not add local behavior specs inside source trees unless the target
repository explicitly asks for that pattern. Prefer documented repository paths
such as `docs/specs/src/[path].md`, `docs/specs/modules/[name].md`, or
feature-package-local notes that are promoted before closure.

### Documentation Partitions Are Allowed

When working in a repository with its own documentation approach, lifecycle docs
may live under a named partition such as `docs/<name>/`. This keeps the target
repository clean while still preserving specs, durable docs, governance, and
evidence in a discoverable structure.

### Ship Risk Is Explicit

Before release or closure, record ship or closure risk, blast radius, rollback
path, human-review needs, and release-note needs when they apply.

## Review And Updates

Update this constitution when the repository changes its spec lifecycle,
documentation structure, validation gates, or agent workflow rules. Changes
should be reflected in the `spec-lifecycle-manager` skill or its references
when they affect agent behavior.
