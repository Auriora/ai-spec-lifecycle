# Spec Lifecycle Manager Codex Plugin

This plugin is a Codex wrapper around the `spec-lifecycle-manager` skill and
read-only MCP runtime maintained by this repository.

It packages:

- `skills/spec-lifecycle-manager/SKILL.md` as lightweight plugin guidance.
- Host installer support for syncing the full skill runtime to
  `~/.codex/skills/spec-lifecycle-manager`.
- Host-level MCP and advisory hook configuration pointing at the installed
  skill copy.

The plugin does not use cache-relative MCP paths. The executable MCP runtime is
configured in `~/.codex/config.toml` so it can launch the installed Python
runtime directly.

Use `scripts/install-spec-lifecycle-manager-package.sh` from this repository to
install or refresh the package for the current user.
