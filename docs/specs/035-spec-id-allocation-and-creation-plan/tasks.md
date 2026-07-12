---
title: Spec ID allocation and creation plan tasks
doc_type: spec
artifact_type: tasks
status: active
authoring_mode: wizard
lifecycle_stage: tasks
owner: platform
last_reviewed: 2026-07-12
---

# Tasks

## Phase 1: Numbering Evidence

- [x] T001 Implement docs-root-scoped numbering inventory
  - Contract input: the accepted Spec 036 T005 envelope, fingerprint, schema,
    and provenance primitives are already delivered.
  - Files: shared lifecycle core and focused runtime fixtures.
  - Parse active, archive-index, closure-log, retained-archive, and explicit
    legacy-range evidence without crossing the selected docs-root boundary.
  - Acceptance: empty and populated scopes return deterministic evidence,
    monotonic next numbers, confidence, and diagnostics for malformed,
    duplicate, missing-history, and ambiguous-history cases.
  - Evidence: 2026-07-12, shared inventory covers empty/bootstrap, active,
    removed, retained, closure-log-only, explicit legacy-range, duplicate,
    malformed, missing-history, ambiguous-history, multi-root, path-escape,
    deterministic ordering, monotonic allocation, confidence, and read-only
    behavior. Six focused fixtures and the 284-test full Python suite pass;
    source/Codex/Claude parity and `git diff --check` pass.

- [ ] T002 Implement slug validation and provisional creation planning
  - Depends on: T001.
  - Files: shared lifecycle core, provenance helper, and focused fixtures.
  - Compose safe proposed paths, template authority, artifact sets,
    preconditions, validation commands, and stale-plan fingerprints.
  - Acceptance: valid ASCII lower-kebab slugs produce repo-relative plans;
    invalid/traversal/confusable values produce no path; collisions and changed
    inputs return fresh proposals; repeated calls are read-only and stable.
  - Evidence: Pending.

## Phase 2: Existing Workflow Integration

- [ ] T003 Reuse allocation in bootstrap, scan, and no-active orientation
  - Depends on: T001, T002.
  - Files: shared lifecycle core and orientation/bootstrap fixtures.
  - Replace hard-coded bootstrap numbering and add next-number/action fields to
    established orientation payloads without changing existing fields.
  - Acceptance: blank scopes still propose `000`; established repositories use
    the same allocator; scan and no-active results expose the provisional next
    number without agent-side arithmetic.
  - Evidence: Pending.

- [ ] T004 Add retained CLI inventory and creation-plan surfaces
  - Depends on: T003.
  - Files: runtime adapter and CLI tests.
  - Add validation/recovery commands with docs-root, slug, and expected-
    fingerprint arguments using caller-agnostic core results.
  - Acceptance: commands validate inputs, return repo-relative deterministic
    JSON, attach CLI provenance, and never mutate files.
  - Evidence: Pending.

- [ ] T005 Add MCP tools, schemas, and MCP/CLI parity coverage
  - Depends on: T004.
  - Files: MCP server, shared schemas, and MCP tests.
  - Expose `spec_id_inventory` and `spec_creation_plan` with closed schemas and
    adapter-owned provenance.
  - Acceptance: tool discovery, schema rejection, compact contract,
    stale/collision responses, privacy, and exact decision parity after
    transport metadata removal pass.
  - Evidence: Pending.

## Phase 3: Packaging And Promotion

- [ ] T006 Synchronize package bundles and validate compatibility
  - Depends on: T001-T005.
  - Acceptance: source/Codex/Claude parity, package contract, sync guard, npm
    dry-pack, and full validation pass without changing established schemas.
  - Evidence: Pending.

- [ ] T007 Promote durable documentation and close B061
  - Depends on: T006.
  - Acceptance: durable design/reference/skill guidance describes provisional
    allocation and the future atomic-writer boundary; backlog/roadmap and
    closure records reconcile.
  - Evidence: Pending.

## Dependency Summary

`Spec 036 T005 -> T001 -> T002 -> T003 -> T004 -> T005 -> T006 -> T007`.

## Agent Readiness Contract

T001 is the first runnable slice. Read requirements, design, traceability, and
the accepted Spec 036 envelope/provenance contract. Limit edits to shared
inventory/allocation internals and focused fixtures; do not add creation-plan,
orientation, CLI, or MCP surfaces in T001. Validate focused tests, full Python
tests, package parity after source slices, and `git diff --check`. Preserve
repo-relative output, explicit docs-root ownership, standard-library-only
runtime code, and read-only behavior.
