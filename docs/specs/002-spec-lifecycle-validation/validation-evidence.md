---
title: Spec lifecycle validation evidence
doc_type: review
status: draft
owner: platform
last_reviewed: 2026-06-02
---

# Validation Evidence

## Summary

Validation is exercising the repo-local `spec-lifecycle-manager` skill against
static checks, fixture repositories, sub-agent prompt trials, review-matrix
passes, and dogfood usage.

Skill under test:

```text
.codex/skills/spec-lifecycle-manager/
```

Canonical source:

```text
skills/spec-lifecycle-manager/
```

## Static Consistency Checks

| Check | Command or Method | Result | Evidence |
|-------|-------------------|--------|----------|
| Repo-level reusable templates absent | `test ! -d docs/templates` | Pass | Reusable project templates live under skill references, not repo docs. |
| Skill-owned template references exist | `test -d skills/spec-lifecycle-manager/references/spec-package && test -d skills/spec-lifecycle-manager/references/durable-doc-templates` | Pass | Both spec-package and durable-doc template directories exist under the skill. |
| Repo-local skill matches canonical source | `diff -qr skills/spec-lifecycle-manager .codex/skills/spec-lifecycle-manager` | Pass | Command returned no differences. |
| Markdown links resolve | local Python markdown-link resolver over repo markdown excluding `.codex` | Pass | Command returned `markdown-links-ok`. |
| Required task guidance present | `rg` over `skills/spec-lifecycle-manager/references/spec-package/` | Pass | Templates include checklist tasks/subtasks, `Depends on`, `Acceptance`, `Evidence`, `change-impact.md`, `verification.md`, and ship risk guidance. |
| Spec and durable metadata separated | `rg` over skill templates | Pass | Spec-package files use `doc_type: spec` plus `artifact_type`; durable templates use durable `doc_type` classes. |
| Required skill references exist | manual check from `SKILL.md` references | Pass | `references/spec-package/`, `references/durable-doc-templates/`, `references/migration-guide.md`, and `references/document-routing-and-expert-review.md` exist. |

## Fixture Inventory

| Fixture | Scenario | Expected Behavior |
|---------|----------|-------------------|
| `fresh-feature-own-repo/` | New feature in owned repo | Skill should create minimal `[docs-root]/specs/[###-slug]/` package with `requirements.md`, `design.md`, `tasks.md`, and optional `verification.md`. |
| `bug-fix-durable-source/` | Bug fix changing durable behavior | Skill should reference durable search behavior docs and recommend `change-impact.md`. |
| `old-format-resume/` | Old-format active spec | Skill should use migration decision gate and choose next coherent task without forced migration. |
| `external-partition/` | External repo docs cleanliness | Skill should use `docs/agent-lifecycle/specs/[###-slug]/`. |
| `completed-spec-close/` | Completed spec with pending durable docs | Skill should identify promotion targets and closure blocker. |
| `governance-conflict/` | Spec conflicts with constitution | Skill should stop for a governance decision before implementation. |

## Prompt Trial Results

| Agent | Model | Fixture | Prompt | Expected | Observed | Result | Follow-up |
|-------|-------|---------|--------|----------|----------|--------|-----------|
| Linnaeus `019e8930-c737-7e72-ba58-790f990f6fb5` | `gpt-5.3-codex-spark` | `fresh-feature-own-repo/` | Create a spec for a task reminders feature. | Create `requirements.md`, `design.md`, `tasks.md` under `docs/specs/[###-slug]/`, with optional verification. | Skill reads repo instructions/docs, then creates smallest useful package with required core artifacts. | Pass | Include durable gap note from `docs/requirements/current-behavior.md`. |
| Linnaeus `019e8930-c737-7e72-ba58-790f990f6fb5` | `gpt-5.3-codex-spark` | `bug-fix-durable-source/` | Create a spec for a bug fix: search leaks cross-workspace results. | Reference durable source docs and use `change-impact.md`. | Skill requires durable source references and `change-impact.md` for bug-fix behavior changes. | Pass | Cite `docs/requirements/search-behavior.md`, `docs/design/search-pipeline.md`, and test evidence. |
| Linnaeus `019e8930-c737-7e72-ba58-790f990f6fb5` | `gpt-5.3-codex-spark` | `old-format-resume/` | Resume this old spec and pick the next task. | Detect old format and use migration decision gate, not forced migration. | Skill detects `spec.md`/`plan.md`/checkboxes and offers continue, migrate, or follow-up migration options. | Pass | Likely next task is `T002`; record chosen migration path in reconciliation. |
| Mendel `019e8930-dff6-7cf3-b4e4-85ed0db2fda7` | `gpt-5.3-codex-spark` | `external-partition/` | Work in this external repo but keep lifecycle docs under `docs/agent-lifecycle/`. | Use `docs/agent-lifecycle/specs/[###-slug]/`; avoid product docs and source tree pollution. | Skill supports named docs partitions and reads repo/user instructions first. | Pass | Create lifecycle docs only under `docs/agent-lifecycle/`. |
| Mendel `019e8930-dff6-7cf3-b4e4-85ed0db2fda7` | `gpt-5.3-codex-spark` | `completed-spec-close/` | Close this completed refresh-token spec. | Identify durable-doc promotion blockers and stop closure. | `T003` is pending and `Ready for closure: no`; close is blocked until `docs/requirements/auth.md` and `docs/runbooks/auth.md` are promoted. | Pass | Promote durable docs, record evidence, then re-run closure readiness. |
| Mendel `019e8930-dff6-7cf3-b4e4-85ed0db2fda7` | `gpt-5.3-codex-spark` | `governance-conflict/` | Implement this disable-auth-check spec. | Treat constitution conflict as blocking. | Skill treats governance as higher priority; fixture constitution blocks silent security downgrades. | Pass | Request explicit governance decision or scope change before implementation. |

## Review Matrix Results

| Agent | Model | Perspective | Result | Findings | Follow-up |
|-------|-------|-------------|--------|----------|-----------|
| Aristotle `019e8930-fae1-7d21-a863-7172a534e145` | `gpt-5.3-codex-spark` | Kiro-style spec workflow | Pass | Non-blocking findings: requirements template lacked durable-source baseline; `change-impact.md` used ambiguous `doc_type`; DAG examples used Unicode arrows. | Fixed in templates and migration guide. |
| Aristotle `019e8930-fae1-7d21-a863-7172a534e145` | `gpt-5.3-codex-spark` | Durable-doc lifecycle | Pass | Finite spec lifetime, promotion, and closure model passed. Same non-blocking improvements applied. | Fixed. |
| Descartes `019e8931-18b3-7d52-bdca-870b4ab570c7` | `gpt-5.3-codex-spark` | Governance/evidence | Pass | Constitution precedence, migration gate, task evidence, verification, and ship-risk tracking were explicit. | No blocking follow-up. |
| Descartes `019e8931-18b3-7d52-bdca-870b4ab570c7` | `gpt-5.3-codex-spark` | External-project cleanliness | Initial fail, fixed | Fallback templates embedded `docs/specs/` and skill referenced `open-decisions.md` without a template. | Replaced hard-coded paths with `[docs-root]/...` and added `open-decisions.md`. |

## Review Fixes Applied

| Finding | Fix | Verification |
|---------|-----|--------------|
| Requirements template lacked durable-source baseline. | Added `Durable Source Baseline` section to `requirements.md`. | Static search found section. |
| `change-impact.md` metadata was ambiguous. | Changed frontmatter to `doc_type: change-impact`. | Static search found specific doc type. |
| DAG examples used Unicode arrows. | Replaced machine-oriented DAG examples with ASCII `->`. | Static search no longer finds Unicode arrows in spec-package templates. |
| Fallback templates hard-coded `docs/specs/`. | Replaced fallback path examples with `[docs-root]/specs/[###-slug]/`. | Static search no longer finds hard-coded paths in fallback templates. |
| `open-decisions.md` referenced but missing. | Added fallback `open-decisions.md` template and README entry. | Static search found template and optional artifact entry. |

## Dogfood Assessment

Result: pass with moderate artifact overhead.

The package shape was useful for this validation because requirements, design,
tasks, verification, and evidence stayed separate. `change-impact.md` was not
needed for this validation because it did not change existing durable behavior.
The main cost is artifact count; small validation work should keep optional
artifacts omitted unless they add clear value.

### Old-Format Archived Spec Trial

Prompt tested:

```text
Use the skill with docs/specs/001-spec-lifecycle-manager-skill.
```

Observed package state:

- package uses old format: `spec.md`, `plan.md`, `tasks.md`, `design.md`;
- frontmatter status is `archived`;
- task list is fully checked;
- closure recommendation says durable current-state guidance lives in
  `docs/design/`, `docs/reference/`, `docs/README.md`, and tracked skill source;
- package is retained as historical validation and decision history.

Migration decision gate result:

| Option | Decision | Reason |
|--------|----------|--------|
| Continue old format for this slice | Selected | The package is archived and no implementation slice is needed. |
| Migrate before implementation | Rejected | Migration would churn historical evidence and is explicitly discouraged for archived specs. |
| Create follow-up migration task | Rejected | No future active work is currently planned for the archived package. |

Reconciliation classifications:

| Classification | Evidence |
|----------------|----------|
| intentionally deferred | Old-format package remains historical rather than migrated. |
| durable docs stale | Some older durable docs and archived evidence still mention global install paths and older package concepts; current repo-local usage is documented elsewhere and may need cleanup if promoted as current guidance. |
| implemented but unverified | Not applicable; no implementation task is active. |
| code incomplete | Not applicable. |
| governance conflict | Not applicable. |

Skill behavior result: pass. The skill correctly avoids forced migration for an
archived old-format package and uses the migration decision gate. The useful
follow-up is durable-doc cleanup, not migration of the archived spec.

## Residual Risks

- Prompt trials were mental/read-only rather than mutating fixtures.
- Validation is not yet scripted; future work can turn static checks into a
  repeatable script once the workflow stabilizes.
