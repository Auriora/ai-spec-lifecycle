---
title: Spec lifecycle manager plugin install
doc_type: reference
status: active
owner: platform
last_reviewed: 2026-06-11
copyright: Copyright 2026 Auriora
license: GPL-3.0-or-later
---

# Spec Lifecycle Manager Plugin Install

## Purpose

Record how the `spec-lifecycle-manager` Codex and Claude Code plugins are
packaged, installed, and validated for this repository.

## Supported Model

Use the spec lifecycle runtime as a self-contained Codex plugin. The plugin
bundles the skill, MCP server definition, prompt definitions, templates,
runtime scripts, and advisory hooks under:

```text
plugins/spec-lifecycle-manager/
```

Supported boundaries:

| Surface | Role | Install path |
|---------|------|--------------|
| Agent Workbench MCP | Repo context, coding-agent runtime support, validation planning, and workspace-aware guidance. | Host-level `mcp_servers.agent-workbench` entry. |
| Spec lifecycle plugin | Spec lifecycle skill, read-only MCP tools, prompt definitions, templates, and advisory hooks. | Plugin cache under `~/.codex/plugins/cache/<marketplace>/spec-lifecycle-manager/<version>/`. |
| Spec lifecycle MCP | Spec inventory, linting, traceability context, prompt definitions, promotion planning, and closure checks. | Plugin-scoped `.mcp.json`, not a host-level `mcp_servers` entry. |
| Spec lifecycle hooks | Advisory lifecycle checks after write tools. | Plugin-scoped `hooks/hooks.json`, subject to normal Codex plugin hook trust. |
| Claude Code plugin | Claude plugin wrapper with the same skill, MCP server, runtime scripts, and advisory lifecycle hook. | `plugins/spec-lifecycle-manager/claude-plugin/` from a checkout or unpacked package. |

Do not install a separate `~/.codex/skills/spec-lifecycle-manager/` copy for
normal operation. Do not add a host-level
`[mcp_servers.spec-lifecycle-manager]` block unless debugging a local runtime
outside the plugin. The package installer removes the old managed global skill,
MCP, and hook entries before installing the plugin bundle.

## Plugin Layout

```text
plugins/spec-lifecycle-manager/
  .codex-plugin/plugin.json
  .mcp.json
  hooks/hooks.json
  skills/spec-lifecycle-manager/
    SKILL.md
    agents/
    prompts/
    references/
    scripts/
  claude-plugin/
    .claude-plugin/plugin.json
    .mcp.json
    hooks/hooks.json
    skills/spec-lifecycle-manager/
      SKILL.md
      agents/
      prompts/
      references/
      scripts/
```

The manifest points to bundled components with plugin-root-relative paths:

- `skills`: `./skills/`
- `mcpServers`: `./.mcp.json`

The Claude Code plugin wrapper points to its nested bundled components with
the same plugin-root-relative paths:

- `skills`: `./skills/`
- `mcpServers`: `./.mcp.json`

Neither manifest declares a `hooks` key. Both runtimes auto-discover
`hooks/hooks.json` at its default location by convention. In Claude Code,
declaring `"hooks": "./hooks/hooks.json"` in `plugin.json` causes the file to
load twice and fail with "Duplicate hooks file detected," which disables the
whole plugin's MCP server. The `hooks` manifest key should only be used to
point at additional hook files beyond the default location.

## Cross-Platform Support and Python Interpreter

The plugin installs and runs on **Windows, macOS, and Linux**. The installer is
a shell-free Node program and the MCP server and hook are launched without a
POSIX shell, so no `bash`, Git Bash, WSL, MSYS2, or Cygwin is required on any OS.

### Supported matrix

| Item | Requirement |
|------|-------------|
| OS | Windows, macOS, Linux (CI: `windows-latest`, `macos-latest`, `ubuntu-latest`) |
| Node.js | 18 or newer (the installer/bin is Node) |
| Python | 3.10 or newer (standard library only; no third-party deps) |

### Interpreter resolution

Because no single Python command name exists on every OS (`python3` is usually
absent on Windows; `py` is absent on macOS/Linux; `python` is guaranteed
nowhere), the interpreter is resolved explicitly at install time and pinned into
the installed `.mcp.json`/`hooks.json`. Resolution order:

| Platform | Order (first that reports Python ≥ 3.10 wins) |
|----------|----------------------------------------------|
| Windows | `py -3` → `python` → `python3` |
| macOS / Linux | `python3` → `python` |

Override the choice on any OS with the `SPEC_LIFECYCLE_PYTHON` environment
variable (honored verbatim, including arguments, e.g. `py -3` or an absolute
path). If no interpreter resolves, the installer fails with an actionable error
naming the missing prerequisite rather than installing a config that cannot
launch.

### Marketplace (no-installer) default

When the plugin is added directly from a marketplace, no installer runs, so the
shipped `.mcp.json`/`hooks.json` ship the portable default command `python`.
Ensure a **Python 3.10+ interpreter named `python` is on PATH**, or set
`SPEC_LIFECYCLE_PYTHON`, for that zero-config path. The npm/installer path does
not need this — it pins the host-resolved interpreter.

## Install Flow

Use the cross-platform installer from this repository (Node, no shell):

```bash
node packaging/spec-lifecycle-manager/installer.mjs
```

`scripts/install-spec-lifecycle-manager-package.sh` is retained for existing
Unix workflows but is now a thin delegator that `exec`s the Node installer, so
the two cannot diverge.

The installer:

- resolves the host Python interpreter (see above) and fails loudly if none
  meets the 3.10 floor;
- removes the old managed standalone skill copy at
  `~/.codex/skills/spec-lifecycle-manager/`;
- removes the old managed host-level MCP config block when present;
- removes the old managed global advisory hook when present;
- copies the self-contained plugin to the local marketplace plugin directory;
- pins the resolved interpreter into the installed `.mcp.json`/`hooks.json`;
- updates the local marketplace entry; and
- runs `codex plugin add spec-lifecycle-manager@<marketplace-name>`
  (skip with `--skip-plugin-add`).

The plugin has no third-party runtime dependencies. It requires Python 3.10 or
newer and otherwise uses the Python standard library.

### Developer CLI wrapper

For checkout-based development, `tools/devcli/` provides the `slc` convenience
CLI. It wraps the installer and package validation commands without replacing
them:

```bash
pip install --no-build-isolation -e tools/devcli
slc package check
slc package pack
slc package install-local --dry-run
slc sync guard
slc plugin status
```

`slc package install-local` invokes
`scripts/install-spec-lifecycle-manager-package.sh` and passes supported
installer options through. Use `--dry-run` first when checking local install
behavior. The authoritative install logic remains
`packaging/spec-lifecycle-manager/installer.mjs`; `slc` is only a repeatable
developer interface around that flow.

## npm Distribution Package

The repository defines an npm package contract:

```text
package.json
packaging/spec-lifecycle-manager/npm-package.json
packaging/spec-lifecycle-manager/npm-install.js
packaging/spec-lifecycle-manager/installer.mjs
packaging/spec-lifecycle-manager/resolve-python.mjs
```

The package name is `@auriora/ai-spec-lifecycle`. It packages the plugin
bundle, package metadata, and the cross-platform Node installer. It is
**marketplace-ready but not published** to the npm registry; the package is
distributed as the `npm pack` tarball attached to **GitHub releases**. Install
from a downloaded/unpacked tarball with its bin:

```bash
npx @auriora/ai-spec-lifecycle install
```

The npm bin resolves the unpacked package root and calls
`packaging/spec-lifecycle-manager/installer.mjs` in-process (no shell, no
spawned `.sh`) with `--source <package-root>`. A `prepack` step strips any
Python bytecode caches so the tarball is clean. Local marketplace install
remains supported for checkout-based development. Docker/GHCR image distribution
is not the supported package path.

## Claude Code Plugin

For a one-off or development session, load the bundled plugin wrapper from a
checkout or unpacked npm package without installing it:

```bash
claude --plugin-dir plugins/spec-lifecycle-manager/claude-plugin
```

This loads the plugin for that session only; you must pass `--plugin-dir`
every time you start `claude`.

For a persistent install that loads automatically every session, this
repository is also a Claude Code marketplace via
`.claude-plugin/marketplace.json` at the repository root, which lists the
Claude plugin wrapper under the marketplace name `ai-spec-lifecycle`. From a
local checkout:

```bash
claude plugin marketplace add /path/to/agent-dev-lifecycle
claude plugin install spec-lifecycle-manager@ai-spec-lifecycle
```

Or, for other users adding the GitHub-hosted marketplace directly:

```bash
claude plugin marketplace add Auriora/ai-spec-lifecycle
claude plugin install spec-lifecycle-manager@ai-spec-lifecycle
```

Or, from a **downloaded release tarball** (offline / version-pinned). The
unpacked tarball ships its own `.claude-plugin/marketplace.json`, so its
`package/` directory is a self-contained Claude marketplace root:

```bash
tar -xzf auriora-ai-spec-lifecycle-<version>.tgz
claude plugin marketplace add ./package
claude plugin install spec-lifecycle-manager@ai-spec-lifecycle
```

### Version-pinned remote marketplace (add by URL)

`packaging/spec-lifecycle-manager/marketplace-pinned.json` is a standalone,
URL-hostable marketplace file. Its plugin `source` is a `git-subdir` pinned to a
release tag, so it resolves even when Claude downloads only the JSON (a relative
`source` would not). Users install a pinned version without cloning or
downloading anything manually:

```bash
claude plugin marketplace add https://raw.githubusercontent.com/Auriora/ai-spec-lifecycle/main/packaging/spec-lifecycle-manager/marketplace-pinned.json
claude plugin install spec-lifecycle-manager@ai-spec-lifecycle
```

Note: a marketplace plugin `source` cannot point at a GitHub release `.tgz`
asset directly — the supported source types are local path, `github`, git
`url`, `git-subdir`, and `npm`. This file uses `git-subdir` against the release
tag; bump its `ref` (and the `version`) each release.

The git-based form uses the same relative `source` resolution and cache-copy
behavior as the local-path form above (verified end-to-end); it was not
re-verified against the live GitHub repository in this pass.

After this, the plugin loads automatically in every new Claude Code session
with no flag required. Use `claude plugin list` to confirm it is installed and
enabled, and `claude plugin uninstall spec-lifecycle-manager@ai-spec-lifecycle`
to remove it.

The Claude plugin wrapper starts the MCP server from its own plugin root in exec
form (`command` + `args`), using `${CLAUDE_PLUGIN_ROOT}` so the path resolves
correctly regardless of the caller's working directory or install location. The
shipped default `command` is `python`; the installer pins the host-resolved
interpreter (e.g. `py` with arg `-3` on Windows, `python3` on macOS/Linux):

```jsonc
// shipped default; installer pins the resolved interpreter
{ "command": "python",
  "args": ["${CLAUDE_PLUGIN_ROOT}/skills/spec-lifecycle-manager/scripts/spec_mcp_server.py"] }
```

After changing the plugin wrapper, skill, MCP config, or hooks, run
`claude plugin marketplace update ai-spec-lifecycle` (persistent install) or
`/reload-plugins` (per-session `--plugin-dir` load) to pick up the change.

### Windows quick-start

A self-contained walkthrough for installing the Claude plugin on Windows.

**Prerequisites**

1. **Claude Code** installed (the `claude` command works in your terminal).
2. **Python 3.10+ with `python` on PATH.** Install from
   [python.org](https://www.python.org/downloads/) and check **"Add python.exe
   to PATH"** during setup, then confirm in a *new* terminal:

   ```powershell
   python --version
   ```

   It must print `3.10` or higher. The zero-installer marketplace path uses the
   shipped static `command: python`, so a working `python` (not just the `py`
   launcher) must resolve. If `python` opens the Microsoft Store, disable
   **Settings → Apps → App execution aliases → python.exe** or reinstall Python
   with the PATH option. (Node.js is not required for the Claude path — only for
   the npm/Codex installer.)

**Install** (one command each, no manual download):

```powershell
claude plugin marketplace add Auriora/ai-spec-lifecycle
claude plugin install spec-lifecycle-manager@ai-spec-lifecycle
```

To pin to a specific release, append the tag: `Auriora/ai-spec-lifecycle@v0.2.1`.
For an offline install, download the release tarball, `tar -xzf` it, and
`claude plugin marketplace add .\package` instead of the first line.

**Confirm and use**

```powershell
claude plugin list
```

`spec-lifecycle-manager` should appear. Start `claude` in any project; the
plugin loads automatically, exposing the spec-lifecycle MCP tools and the
advisory PostToolUse hook. If the tools do not appear, it is almost always that
`python` is not a working Python 3.10+ on PATH — re-check `python --version` in a
fresh terminal.

Uninstall with `claude plugin uninstall spec-lifecycle-manager@ai-spec-lifecycle`.

## Hook Policy

Spec lifecycle hooks are advisory-only. The bundled hook file is:

```text
plugins/spec-lifecycle-manager/hooks/hooks.json
```

The Codex hook runs as a shell-form command string (the resolved interpreter is
pinned in place of the `python` default):

```text
python "${PLUGIN_ROOT}/skills/spec-lifecycle-manager/scripts/codex_spec_lifecycle_hook.py"
```

Plugin-bundled hooks follow Codex's plugin hook trust flow. They should stay
quiet on pass and emit additional context only for advisory lifecycle
diagnostics. Future blocking behavior requires a focused spec or backlog item
that defines event source, payload, command, timeout, severity profile,
false-positive handling, rollback path, and validation evidence.

The Claude Code wrapper uses the same advisory hook script from its nested
plugin root, but in **exec form** (`command` + `args`) so it is spawned without
a shell on every OS:

```jsonc
{ "command": "python",
  "args": ["${CLAUDE_PLUGIN_ROOT}/skills/spec-lifecycle-manager/scripts/codex_spec_lifecycle_hook.py"] }
```

## Validation Checklist

Use this checklist in this repository after install, sync, or reload:

| Check | Expected evidence |
|-------|-------------------|
| Plugin validates | `plugin-creator` validation passes for `plugins/spec-lifecycle-manager`. |
| Plugin is self-contained | `skills/`, `.mcp.json`, `hooks/hooks.json`, scripts, prompts, and references exist under the plugin root. |
| MCP tools visible after reload | Codex exposes plugin-scoped `spec-lifecycle-manager` MCP tools. |
| Server starts | `initialize` returns server name `spec-lifecycle-manager`. |
| Spec scan works | `scan_specs` returns repo-relative paths and the expected active-spec count when `repo_root` is supplied or inferred. |
| Resource scan works | `specs://active` returns repo-relative paths for the target workspace and does not expose the plugin cache or load path. |
| Archive index works | `archive_index` returns no diagnostics for removed package history. |
| Prompt definitions validate | `prompts_validate` returns no diagnostics. |
| Package tools resolve live specs | `closure_check`, `task_context`, or `traceability_lookup` work when an active spec exists. |
| Sync guard is reviewed | In this repository, `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py sync-guard .` reports source/bundle parity, installed cache state, reload advisory, and recent commit evidence. |
| Package contract validates | `PYTHONDONTWRITEBYTECODE=1 skills/spec-lifecycle-manager/scripts/spec_runtime.py package-contract .` returns no diagnostics for npm contract metadata, required package files, source/bundle parity, and provenance. |
| npm tarball contains payload | `npm pack --dry-run --json` includes `package.json`, the npm installer bin, npm package contract, existing installer script, and plugin bundle. |
| Claude plugin validates | Package tests confirm the Claude manifest, MCP config, hook config, skill, and runtime script are bundled under `plugins/spec-lifecycle-manager/claude-plugin/`. |
| Claude plugin is in npm payload | `npm pack --dry-run --json` includes the Claude plugin manifest, `.mcp.json`, hooks, skill, and MCP runtime script. |
| No old standalone skill remains | `~/.codex/skills/spec-lifecycle-manager/` is absent after installer cleanup. |
| No old managed host MCP remains | `~/.codex/config.toml` does not contain the old installer-managed `mcp_servers.spec-lifecycle-manager` block. |

## Troubleshooting

If the tools are not visible after reload:

1. Confirm the plugin appears in `codex plugin list`.
2. Confirm the installed plugin cache contains `.mcp.json`.
3. Confirm the plugin is enabled.
4. Confirm no old host-level `mcp_servers.spec-lifecycle-manager` entry is
   shadowing the plugin-provided server.
5. Run `sync-guard` to compare source, bundled plugin, installed cache, and
   reload advisory state.
6. Restart Codex after plugin reinstall, hook trust changes, or a sync guard
   reload advisory.

## Related Artifacts

- `docs/reference/spec-lifecycle-runtime.md`
- `docs/history/spec-archive-index.md`
- `plugins/spec-lifecycle-manager/.codex-plugin/plugin.json`
- `plugins/spec-lifecycle-manager/.mcp.json`
- `plugins/spec-lifecycle-manager/claude-plugin/.claude-plugin/plugin.json`
- `plugins/spec-lifecycle-manager/claude-plugin/.mcp.json`
- `.claude-plugin/marketplace.json`
