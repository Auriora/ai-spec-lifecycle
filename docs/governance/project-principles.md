---
title: Agent development lifecycle project principles
doc_type: governance
status: active
owner: platform
last_reviewed: 2026-06-06
---

# Project Principles

## Purpose

Define why this project exists, what belongs in it, and how to decide whether
new work fits. This document guides scope decisions before backlog, roadmap,
spec, or implementation work begins.

## Problem Statement

AI coding agents can move quickly, but they often lose alignment between user
intent, requirements, design, tasks, validation, durable documentation, and
follow-up work. This project solves that coordination problem by providing a
reusable lifecycle, skill, runtime, MCP surface, templates, and governance model
for spec-driven agent implementation.

The project is not a general coding framework. It exists to make AI-assisted
implementation work more coherent, auditable, resumable, and easier to hand off
across agents and sessions.

## VMOST

### Vision

AI-assisted implementation should be disciplined enough that agents can help
with real engineering work without turning plans, specs, or conversations into
stale hidden state.

### Mission

Provide a practical lifecycle system that keeps temporary specs, code changes,
tests, durable docs, runtime checks, MCP tools, hooks, and review evidence
aligned from intake through closure.

### Objectives

- Keep implementation grounded in requirements, design, traceability,
  verification, and durable docs.
- Reduce repeated agent mistakes such as implementing from task titles alone,
  confusing removed specs with active work, or skipping closure evidence.
- Make lifecycle state discoverable through deterministic CLI/MCP tools.
- Promote completed behavior into durable docs and remove completed spec
  packages from the active docs tree.
- Support bounded secondary-agent review without giving cheap agents authority
  to mutate lifecycle state.

### Strategy

- Treat specs as temporary delivery scaffolding and durable docs as the current
  source of truth.
- Prefer deterministic runtime checks before advisory agent review.
- Keep hooks advisory until repeated evidence supports tighter enforcement.
- Add templates only when they make repeated work clearer or safer.
- Use backlog and roadmap surfaces for ideas, sequencing, and deferred work
  instead of leaving decisions buried in conversations or completed specs.
- Package and distribute the skill/MCP only after core workflows are stable
  enough to avoid churn for downstream users.

### Tactics

- Maintain `skills/spec-lifecycle-manager/` as the source skill.
- Expose stable workflows through `spec_runtime.py` and the read-only MCP
  server.
- Keep active packages under `docs/specs/[###-slug]/` and close them through
  durable promotion, closure log, archive index, and package removal.
- Use `AGENTS.md`, the constitution, this document, backlog, roadmap, and
  runtime preflight tools as first-read context.
- Validate changes with focused runtime tests, spec lint, archive validation,
  prompt validation, and `git diff --check`.

## Core Principles

### Specs Are Temporary

Specs coordinate active delivery. Completed behavior belongs in durable docs,
code, tests, closure records, and archive indexes rather than retained package
folders in the active docs tree.

### Durable Docs Are The Source Of Truth

Durable docs describe accepted current behavior. Specs, backlog items, roadmap
notes, and conversation-derived ideas must route lasting information into
durable docs before closure.

### Deterministic Checks Come First

Runtime lint, inventory scans, traceability lookup, archive validation, prompt
validation, and tests should run before advisory agent judgment.

### Advisory Agents Do Not Own Lifecycle State

Secondary or low-cost agents can review, draft, and suggest. They must not own
edits, task completion, closure, archive updates, commits, hook installation, or
release decisions.

### Friction Becomes Better Workflow

Repeated corrections, context gaps, sync mistakes, weak evidence, and "what
next" prompts should become clearer guidance, deterministic tools, backlog
items, roadmap items, or focused specs.

## Scope Rules

Include work when it:

- improves spec lifecycle quality, traceability, closure, validation, or
  durable documentation;
- helps agents decide what to read, what to implement next, or how to hand off
  work safely;
- strengthens the `spec-lifecycle-manager` skill, runtime, MCP tools, hooks,
  prompts, templates, packaging, or install workflow;
- turns repeated lifecycle friction into clearer guidance, deterministic tools,
  or backlog/roadmap items;
- supports distribution or interoperability without weakening local
  repository control.

Exclude or defer work when it:

- is a generic coding-agent feature unrelated to spec lifecycle management;
- belongs primarily in Agent Workbench, Python Agent IDE, GitHub tooling, or
  another project;
- would make cheap or secondary agents authoritative over edits, task
  completion, closure, archives, commits, or hook installation;
- adds template complexity without repeated evidence of need;
- preserves completed spec packages in the active docs tree just for
  convenience.

## Decision Questions

Before adding work, ask:

1. Does this improve the lifecycle from durable docs to active spec to
   implementation to validation to durable promotion to closure?
2. Does it reduce a repeated agent failure mode or user correction?
3. Is this repository the right owner, or should another tool/project own it?
4. Can it be validated deterministically, or is it only advisory?
5. Will it make future agents more likely to find the right context?
6. Does it keep specs temporary and durable docs current?
7. Is the change worth adding now, or should it remain backlog until the core
   workflow is stable?

## Current Product Signals

- Agents can still start from task text without enough requirements, design,
  traceability, verification, and durable-doc context.
- Removed spec packages can confuse agents unless no-active-spec guidance is
  explicit and easy to access.
- Repeated commit, sync, install, and reload steps create workflow drift when
  skill files change.
- Frequent "what next" prompts show the value of deterministic preflight and
  task-readiness tools.
- Completed task evidence quality varies; lifecycle tooling should encourage
  concrete validation evidence rather than vague claims.
- MCP and hook surfaces are growing, so tracing, packaging, install validation,
  and operational docs matter before broader distribution.

## Relationship To Governance

This document guides project fit. The constitution defines lifecycle rules and
decision gates. If they conflict, update both intentionally or treat the
constitution as the stronger rule for lifecycle behavior.
