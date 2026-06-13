---
title: Document routing and expert review matrix
doc_type: reference
status: active
owner: platform
last_reviewed: 2026-06-01
---

# Document Routing And Expert Review Matrix

## Purpose

Define how spec content maps to durable documentation and which role-based experts should review each document class. Expert roles are process and system roles, not subject-matter owners for a specific feature domain.

## Expert Roles

| Expert role | Review focus |
| --- | --- |
| Systems architect | End-to-end system boundaries, cross-system effects, lifecycle fit, scalability, and failure modes. |
| Software architect | Component design, module boundaries, contracts, abstractions, dependency direction, and maintainability. |
| Developer process expert | Workflow ergonomics, task slicing, handoff quality, repository conventions, and implementation traceability. |
| Senior developer | Code-level feasibility, implementation clarity, testability, refactoring risk, and local patterns. |
| QA and test strategy expert | Verification strategy, acceptance criteria, test coverage, fixtures, environments, and residual risk. |
| Operations and SRE expert | Deployment, observability, runbooks, rollback, supportability, incident response, and runtime safety. |
| Security and compliance expert | Auth, access, secrets, data handling, auditability, least privilege, and compliance-sensitive changes. |
| Documentation architect | Information architecture, document class fit, duplication control, cross-links, lifecycle state, and reader paths. |
| API and contract expert | API/schema compatibility, versioning, examples, error semantics, and contract source of truth. |
| Data and integration architecture expert | Data lineage, integration boundaries, source/target contracts, data quality, idempotency, and replay behavior. |
| Product and requirements analyst | Requirement clarity, scope, non-goals, acceptance criteria, and user-visible outcomes. |

Use only the roles relevant to the changed documents. A small local-only code task may need only senior developer and QA review; a cross-system data/API change may need most of the matrix.

## Document Class Review Matrix

| Document class | Primary reviewers | Secondary reviewers |
| --- | --- | --- |
| Requirements | Product and requirements analyst, systems architect, QA and test strategy expert | Documentation architect, security and compliance expert |
| Architecture | Systems architect, software architect | Operations and SRE expert, security and compliance expert, documentation architect |
| Technical design | Software architect, senior developer | Systems architect, QA and test strategy expert, operations and SRE expert |
| Data-flow | Data and integration architecture expert, systems architect | QA and test strategy expert, documentation architect, operations and SRE expert |
| API contract | API and contract expert, software architect | Security and compliance expert, QA and test strategy expert, documentation architect |
| Runbook | Operations and SRE expert, senior developer | QA and test strategy expert, security and compliance expert, documentation architect |
| ADR | Systems architect, software architect | Operations and SRE expert, security and compliance expert, documentation architect |
| Reference | Documentation architect, relevant technical expert | QA and test strategy expert |
| Backlog or roadmap | Developer process expert, systems architect | Product and requirements analyst, operations and SRE expert |
| Review or audit report | QA and test strategy expert, relevant technical expert | Documentation architect, developer process expert |
| Spec package | Developer process expert, software architect, QA and test strategy expert | Systems architect, documentation architect, operations and SRE expert |
| Agent directive section | Developer process expert, documentation architect | Software architect, senior developer, security and compliance expert |
| Learning-loop or recovery note | Developer process expert, senior developer | QA and test strategy expert, documentation architect |

## Whole-Package Review

Before implementation starts, review the spec package as a whole for:

- requirement clarity and measurable acceptance criteria;
- consistency with durable docs and existing code;
- task slices that can be implemented and validated independently;
- explicit open decisions and non-goals;
- validation strategy and task completion criteria;
- promotion targets for every lasting requirement, design, contract, operation, and decision.

Before spec closure, review the whole package for:

- completed or explicitly deferred tasks;
- durable docs updated and linked;
- tests, checks, or alternate verification recorded;
- stale or duplicate spec-only content removed from the active knowledge path;
- follow-up work moved to backlog or a new focused spec.

## Spec-To-Doc Routing

| Spec artifact or section | Durable routing |
| --- | --- |
| Problem, goals, non-goals | Requirements or backlog, depending on whether the behavior is accepted or still planned. |
| Functional requirements | Requirements, API contracts, data-flow contracts, or reference docs. |
| Acceptance criteria | Requirements, tests, runbooks, or QA references. |
| Correctness properties | Design behavior, traceability matrices, tests, verification plans, or documented manual validation methods. |
| User stories | Requirements, product notes, or backlog if not implemented. |
| Design overview and components | Technical design or architecture docs. |
| Data and contract impact | API contracts, data-flow docs, schema references, or integration guides. |
| Operational considerations | Runbooks, operations references, or architecture/design docs. |
| Governance checks | Design docs, engineering governance references, or task evidence. |
| Research decisions | ADRs, reference docs, reviews, or discarded when no longer useful. |
| Quickstart validation | Runbooks, getting-started docs, or deployment validation docs. |
| Tasks and checkpoints | Remain in the spec while active; close, archive, or remove after promotion. |
| Agent directives | Durable project, pattern, runbook, architecture, or governance docs only when derived from repository evidence or user-confirmed principles. |
| Numbered review findings | `docs/reviews/`, backlog, roadmap, issues, follow-up specs, or durable docs when accepted behavior changes. Preserve stable finding IDs and resolution/routing evidence. |
| Learning-loop failures | Runbooks, troubleshooting notes, backlog, roadmap, follow-up specs, or durable docs depending on whether the reusable lesson is operational, process, design, or governance guidance. |

Before implementation readiness, route coverage gaps explicitly:

- missing property-to-design mapping -> design or traceability update;
- missing property-to-task or verification mapping -> task, verification, or
  traceability update;
- missing acceptance-criteria coverage -> task, verification, QA reference, or
  traceability update;
- downstream review needs after requirements or design changes -> review the
  dependent design, tasks, traceability, and verification artifacts before
  implementation continues.

## Review Record Guidance

Review evidence should state:

- document or spec package reviewed;
- expert role used for the review;
- date;
- findings or sign-off;
- required follow-up;
- whether follow-up blocks implementation, release, or spec closure.

The review record can live in the spec package while implementation is active. Durable findings should be promoted to requirements, design, runbooks, ADRs, reference docs, backlog, or reviews as appropriate.

Numbered findings should be append-only for identity: add new IDs for new
findings, preserve old IDs, and record accepted, rejected, deferred, or
human-decision dispositions. A finding is not implementation evidence until the
accepted change has its own task, validation, and durable destination.
