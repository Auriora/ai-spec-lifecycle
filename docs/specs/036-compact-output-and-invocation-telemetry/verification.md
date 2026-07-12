---
title: Compact lifecycle output and invocation provenance verification
doc_type: spec
artifact_type: verification
status: active
lifecycle_stage: tasks
owner: platform
last_reviewed: 2026-07-12
---

# Verification Plan

## Contract Foundation

- **V001:** Canonical JSON is stable across input mapping order.
- **V002:** Fingerprints change when decision inputs change and exclude volatile fields by caller selection.
- **V003:** Owning-package version resolves in source and plugin layouts.
- **V004:** Missing/malformed identity evidence returns `unknown` without failing lifecycle calls.
- **V005:** Repository identity is stable across commits in one repository and differs across unrelated root histories.
- **V006:** Non-Git/unborn repositories return `unknown`.
- **V007:** MCP initialize reports the authoritative package version.
- **V008:** Lifecycle capabilities reports the same version.
- **V009:** Established initialize/capabilities fields remain present.

## Provenance And Compatibility

- **V010:** MCP, CLI, and hook surfaces are reported correctly.
- **V011:** Root-source precedence is argument, environment, then cwd.
- **V012:** Internal composition does not replace external surface.
- **V013:** Metadata contains no absolute path, prompt, source content, secret, user, or remote URL.
- **V014:** MCP/CLI lifecycle decisions remain equivalent ignoring transport metadata.
- **V015:** Packaged build identity matches release inputs.
- **V016:** Package and plugin versions agree.
- **V017:** Missing legacy build identity remains `unknown`.

## Compact Envelope And Packaging

- **V018:** Compact summaries cap findings at 20 and actions at 10.
- **V019:** Mandatory blockers survive compaction and set `limit_exceeded` when necessary.
- **V020:** Detail modes validate and preserve decision semantics.
- **V021:** Fingerprint mismatch returns `stale` with refreshed follow-up arguments.
- **V022-V025:** Spec 033/035 aggregate contract and MCP/CLI parity fixtures.
- **V026:** `slc sync bundles` succeeds.
- **V027:** package contract and sync guard pass.
- **V028:** source and both bundled trees match.
- **V029:** full Python test suite passes.
- **V030:** `npm run validate` passes.
- **V031:** durable docs, backlog, roadmap, and closure records are reconciled.

## Evidence Log

- **2026-07-12 — T001:** Added deterministic canonical JSON, evidence
  fingerprints, owning-runtime identity resolution, root-commit repository
  identity, closed provenance enums, bounded composition sources, and metadata
  assembly. V001-V006 passed in 8 focused unit tests; `git diff --check` passed.
- **2026-07-12 — T002:** Replaced the MCP server and capabilities stale
  `0.1.0` defaults with owning-runtime identity resolution. V007-V009 passed in
  a 51-test focused provenance/module/MCP run; explicit overrides remain
  supported and target-repository manifests cannot contaminate runtime identity.
- **2026-07-12 — bundle validation:** Repository-owned bundle sync and package
  contract passed; source, Codex, and Claude trees are in sync. Sync guard
  reports only installed-cache drift and reload advisories. The full Python
  suite passed 245 tests and `git diff --check` passed.
- **2026-07-12 — T003:** Added lifecycle capabilities as the additive provenance
  canary for MCP and the retained CLI. V010-V014 passed: external surfaces,
  argument/environment/cwd root precedence, privacy, strict metadata schema,
  and MCP/CLI decision parity were covered by 200 focused tests. Bundle sync,
  package contract, 248 full tests, direct CLI smoke, and `git diff --check`
  passed. Hook provenance remains inapplicable because capabilities is not a
  hook-routable operation.
- **2026-07-12 — T004:** Added deterministic Codex/Claude build-info baselines,
  prepack Git identity generation, postpack reset, and strict package validation
  across root package, legacy package manifest, both plugin manifests, and both
  build-info files. V015-V017 passed: actual npm content carried the full commit
  identity, ordinary checkout/legacy identity remains explicitly `unknown`, and
  mismatch/malformed fixtures fail closed. `npm run validate` passed with 250
  Python and 25 Node tests, package contract, parity, dry-run pack, and diff checks.

## Quality Gates

- Focused tests pass for each task before bundle synchronization.
- Source, Codex, and Claude plugin trees pass package contract and sync guard.
- Full Python tests and `npm run validate` pass before promotion or closure.
- `git diff --check` remains clean for every implementation slice.

## Residual Risks

- Repository identity is correlatable with known Git history and requires
  explicit durable documentation.
- Legacy installations without generated build identity report `unknown`.
- Established-tool compaction remains out of scope until representative payload
  measurements justify a separately compatible migration.
