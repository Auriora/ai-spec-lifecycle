# Document Routing And Expert Review

Use this reference when a spec affects durable documentation or when review roles are needed. Map these roles onto the target repository's documented structure; do not create or require these folder names unless the repository already uses them.

Use `durable-document-contract.md` for the shared human/agent contract that
durable docs should satisfy: current-state labeling, source-of-truth metadata,
validation, change rules, AGENTS.md boundaries, and anti-patterns.

## Durable Doc Roles

| Durable doc role | Purpose |
| --- | --- |
| Requirements | Current or accepted operating requirements. |
| Architecture | Stable system shape, component boundaries, and cross-system flows. |
| Technical design | Current technical design for implemented or accepted component behavior. |
| Data flow | Source-to-output lineage, transformation behavior, config routing, field dictionaries, and processed output behavior. |
| API or contract | Canonical machine-readable contracts and companion guidance. |
| Runbook or operations | Operational procedures, rollout, validation, recovery, replay, and support steps. |
| Decision record | Durable decisions and rejected alternatives. |
| Reference | Stable factual mappings, limits, schemas, taxonomies, generated summaries, and review matrices. |
| Backlog | Proposed or deferred work not ready for a focused implementation spec. |
| Roadmap | Sequenced work, milestones, adoption stages, and multi-spec dependencies. |
| Review or audit | Analysis snapshots and evidence that may feed specs or durable docs. |
| `docs/specs/` | Temporary active delivery packages. |

## Spec-To-Doc Routing

| Spec artifact or section | Durable routing |
| --- | --- |
| Problem, goals, non-goals | Requirements or backlog, depending on whether the behavior is accepted or still planned. |
| Functional requirements | Requirements, API contracts, data-flow contracts, or reference docs. |
| Acceptance criteria | Requirements, tests, runbooks, or QA references. |
| User stories | Requirements, product notes, or backlog if not implemented. |
| Design overview and components | Technical design or architecture docs. |
| Data and contract impact | API contracts, data-flow docs, schema references, or integration guides. |
| Operational considerations | Runbooks, operations references, or architecture/design docs. |
| Governance checks | Design docs, engineering governance references, or task evidence. |
| Research decisions | ADRs, reference docs, reviews, or discard when no longer useful. |
| Quickstart validation | Runbooks, getting-started docs, or deployment validation docs. |
| Tasks and checkpoints | Remain in the spec while active; close, archive, or remove after promotion. |

## Closure Cleanup Routing

Before closing a spec, route or dispose of every lasting element:

| Lasting element | Closure action |
| --- | --- |
| Implemented requirements or accepted behavior | Promote to durable requirements, reference, contract, or test documentation. |
| Implemented design or architecture | Promote to durable design or architecture docs. |
| Operational procedures, rollout, validation, or recovery steps | Promote to runbooks, getting-started guides, checklists, or operations references. |
| Decisions and rationale | Promote to ADR, history note, or durable reference. |
| Evidence that is useful only for audit | Archive with clear historical status or retain in the repository's audit/review location. |
| Closure summary and final spec commit | Record in the repository's spec closure log, defaulting to `docs/history/spec-closure-log.md` when no authoritative closure record exists. |
| Completed task coordination with no lasting value | Remove from the active docs path after closure. |
| Unfinished or deferred work lacking scope or acceptance criteria | Move to backlog. |
| Deferred work with sequencing, milestone, adoption, or multi-spec dependency impact | Move or link to roadmap. |
| Deferred work that is ready to implement | Move to a follow-up spec or issue tracker item. |

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
| Backlog | Developer process expert, product and requirements analyst | Systems architect, documentation architect |
| Roadmap | Developer process expert, systems architect | Product and requirements analyst, operations and SRE expert |
| Review or audit report | QA and test strategy expert, relevant technical expert | Documentation architect, developer process expert |
| Spec package | Developer process expert, software architect, QA and test strategy expert | Systems architect, documentation architect, operations and SRE expert |

## Whole-Package Review

Before implementation starts, review the spec package for:

- requirement clarity and measurable acceptance criteria;
- consistency with durable docs and existing code;
- durable-doc readiness: authoritative docs, current/planned/deprecated state,
  code-derived contracts that override prose, docs to update, and docs not to
  change;
- independently validatable task slices;
- explicit open decisions and non-goals;
- validation strategy and task completion criteria;
- promotion targets for lasting requirements, designs, contracts, operations, and decisions.

Before closure, review for:

- completed or explicitly deferred tasks;
- durable docs updated and linked;
- tests, checks, or alternate verification recorded;
- stale or duplicate spec-only content removed from the active knowledge path;
- follow-up work moved to backlog, roadmap, issue tracker, or a focused spec.
- spec package disposition recorded as archived, removed, or retained as
  historical context.
- final spec commit recorded before removal when Git-backed archival is used;
- closure log entry records durable destinations, verification summary,
  residual risks, and follow-up work.
