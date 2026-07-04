# Tools

Put repository-owned developer tooling here.

The repository uses a dedicated Python CLI package:

- `tools/devcli/`: the `slc` developer CLI for validation, source-to-bundle
  sync, package checks, local install, plugin status, spec wrappers, doctor,
  and release preflight helpers.

The CLI is a thin convenience layer over repository-owned scripts and runtime
helpers. Commands that can mutate files or local installation state must make
that boundary explicit and support dry-run behavior when the underlying
workflow supports it.

Keep tooling code separate from application code so the project structure stays clear.
