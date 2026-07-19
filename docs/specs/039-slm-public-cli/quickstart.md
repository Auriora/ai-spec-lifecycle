---
title: Public slm CLI quickstart
doc_type: spec
artifact_type: quickstart
status: draft
owner: platform
last_reviewed: 2026-07-19
---

# Quickstart

## Purpose

Define the intended user journey and packaged smoke scenarios for `slm`. These
commands are proposed behavior until the corresponding implementation tasks and
verification evidence are complete.

## Prerequisites

- Node.js 18 or newer.
- Python 3.10 or newer, or a valid `SPEC_LIFECYCLE_PYTHON` override.
- A built Spec Lifecycle Manager release tarball containing the `slm` bin.
- A repository with lifecycle docs for non-empty examples.

## Steps

1. Install a built release tarball into an isolated npm prefix or use the
   equivalent release-install command documented by the implementation.
2. Confirm command discovery:

   ```bash
   slm --help
   slm install --help
   ```

3. From a lifecycle-enabled repository, list active specs:

   ```bash
   slm specs
   slm specs --json
   ```

4. Select an active spec and inspect tasks:

   ```bash
   slm tasks 039
   slm tasks 039 --pending
   slm tasks 039 --open
   slm tasks 039 --complete
   slm tasks 039 --next
   slm next 039
   ```

5. Inspect requirements and priorities:

   ```bash
   slm requirements 039
   slm requirements 039 --priority must-have
   slm requirements 039 --missing-priority
   ```

6. Inspect durable closed-spec history:

   ```bash
   slm history
   slm history --removed --limit 10
   slm history --json
   ```

7. Verify explicit repository selection from outside the root:

   ```bash
   slm -C ../example-repository specs
   ```

## Expected Results

- `slm --help` shows `specs`, `tasks`, `next`, `requirements`, `history`, and
  `install`.
- Bare `slm` and `slm specs` show the same active-spec records.
- Human mode uses concise plain text; `--json` emits one valid versioned JSON
  document.
- `--pending` shows literal pending tasks, while `--open` includes all defined
  non-terminal task states.
- Both next-task command forms select the same dependency-aware result.
- Requirements show canonical priority or `unspecified`.
- History includes removed specs without requiring their package directories.
- None of the inspection commands modify the repository.

## Validation Evidence

| Step Or Scenario | Evidence | Result | Residual Risk |
|------------------|----------|--------|---------------|
| Help and install routing | Isolated tarball smoke | pending | Must prove sole-bin npm behavior. |
| Active spec human/JSON views | Focused CLI test and manual terminal check | pending | Table width differs by terminal. |
| Task filters and next equivalence | Table-driven tests and core comparison | pending | Future markers require test updates. |
| Requirement priorities | Canonical/missing/invalid priority fixtures | pending | Traceability may be absent. |
| Removed history | Archive fixture with absent package directory | pending | Malformed records must fail closed. |
| Explicit/nested root selection | Temporary repository fixture | pending | Cross-platform path behavior requires CI. |
| Read-only guarantee | Before/after worktree fingerprint | pending | `install` is excluded by design. |

## Cleanup

- Remove isolated npm prefixes, caches, and unpacked tarballs created by smoke
  tests.
- Do not remove or reset user repository files as part of CLI validation.
- Do not install a development checkout into user-wide Codex or Claude state.

## Promotion Or Discard Decision

- **Disposition:** promote
- **Durable destination:** `README.md` for the concise path and
  `docs/reference/spec-lifecycle-runtime.md` for complete command semantics
- **Reason:** The commands are the primary public onboarding path for the new
  executable.
- **Owner or follow-up:** platform, T008

## Related Artifacts

- Requirements: `requirements.md`
- Design: `design.md`
- Tasks: `tasks.md`
- Traceability: `traceability.md`
- Verification: `verification.md`
