---
title: Cross-platform packaging design
doc_type: spec
artifact_type: design
status: active
owner: platform
last_reviewed: 2026-06-29
---

# Design

## Overview

Two changes make the plugin portable: a **Node installer** replacing the `.sh`
installer, and **explicit Python interpreter resolution** replacing the
hard-coded `python3` command name in `.mcp.json`/`hooks.json`. Both rest on
Claude Code's documented execution model:

- Hook/MCP entries in **exec form** (`"command"` + `"args"`) are spawned
  **directly, without a shell**, so no POSIX/PowerShell syntax is involved.
- Claude Code expands `${CLAUDE_PLUGIN_ROOT}` itself before invocation on every
  OS; Codex expands `${PLUGIN_ROOT}` similarly. Script paths in `args` are
  therefore portable.
- On Windows (v2.1.120+) shell form falls back to PowerShell when Git Bash is
  absent, so the current shell-form hook string is a live Windows blocker.

The remaining problem is unique to a Python plugin: **there is no single Python
command name that resolves on all three OSes.** `python3` exists on most
Linux/macOS hosts but rarely on Windows; `py` is the canonical Windows launcher
but is absent on Linux/macOS; `python` is present on some but guaranteed on
none. The design resolves the interpreter explicitly instead of assuming a name.

### Documented execution-model basis

| Concern | Documented behavior | Design consequence |
| --- | --- | --- |
| Hook/MCP exec form | spawned without a shell | Use exec form for hook + MCP |
| `${CLAUDE_PLUGIN_ROOT}` / `${PLUGIN_ROOT}` | expanded by runtime pre-invocation | Safe in `args`, all OSes |
| Shell-form on Windows | PowerShell when Git Bash absent | Current hook string breaks; avoid |
| Command resolution | PATH lookup; no `.cmd`/`.bat` in exec form | `python3` name unreliable on Windows |

## High-Level Design

```text
  npx / bin ──► packaging/.../installer.mjs  (Node installer)
                     │  1. detect interpreter: py → python3 → python
                     │     (override: SPEC_LIFECYCLE_PYTHON)
                     │  2. copy files, register plugin
                     │  3. pin the detected interpreter into the installed
                     │     .mcp.json / hooks.json (or a generated launcher)
                     ▼
        installed .mcp.json:  { "command": "<resolved>",
                                "args": ["<root>/.../spec_mcp_server.py"] }
        installed hooks.json: { "command": "<resolved>",
                                "args": ["<root>/.../codex_spec_lifecycle_hook.py"] }

  shared:  interpreter-resolver  (probe py/python3/python; honor
           SPEC_LIFECYCLE_PYTHON override; verify it runs `python --version` ≥ 3)
```

### Components

- **Cross-platform installer (`packaging/spec-lifecycle-manager/installer.mjs`).**
  Node module holding the copy/register logic from
  `install-spec-lifecycle-manager-package.sh`; `npm-install.js` calls it
  in-process instead of `spawnSync`-ing the `.sh`. The `.sh` is removed or
  reduced to a thin `node installer.mjs` delegator.
- **Interpreter resolver.** Probes, in order, `SPEC_LIFECYCLE_PYTHON`
  (override), then `py -3` on Windows / `python3` / `python`, confirming each
  candidate reports Python ≥ 3 via `--version`. Returns the resolved command (and
  args, e.g. `["py","-3"]`). Used by the installer to pin configs.
- **Pinned launch configs.** For the npm/installer distribution path the
  installed `.mcp.json` and `hooks.json` carry the resolved interpreter in exec
  form. This is the robust path because the installer runs on the target host.
- **Marketplace fallback (resolved, see Resolved Decisions §1).** When Claude
  installs the plugin directly from the marketplace, no installer runs, so the
  shipped `.mcp.json`/`hooks.json` are static. These ship a static `command` of
  `python` plus a documented "Python 3 on PATH" prerequisite; the
  installer-pinned path still writes the host-resolved interpreter.

### Data flow / data models

No persisted data. The one resolved value is the interpreter command vector
(`[cmd, ...args]`), computed once at install and written into the launch
configs.

## Low-Level Design

### Interpreter resolver

```js
// candidates by platform; each verified to report Python >= 3 before selection
export function resolvePython(env = process.env, platform = process.platform) {
  if (env.SPEC_LIFECYCLE_PYTHON) return splitCommand(env.SPEC_LIFECYCLE_PYTHON);
  const candidates = platform === "win32"
    ? [["py", "-3"], ["python"], ["python3"]]
    : [["python3"], ["python"]];
  for (const cand of candidates) {
    if (reportsPython3(cand)) return cand;   // spawn `<cand> --version`, parse major>=3
  }
  throw new Error("Python 3 not found. Install it (Windows: python.org or 'winget install Python.Python.3'; macOS: 'brew install python'; Linux: distro package) or set SPEC_LIFECYCLE_PYTHON.");
}
```

### Pinned exec-form configs (installer output)

`.mcp.json` (installed form), interpreter resolved at install:

```json
{ "mcpServers": { "spec-lifecycle-manager": {
  "command": "py",
  "args": ["-3", "${CLAUDE_PLUGIN_ROOT}/skills/spec-lifecycle-manager/scripts/spec_mcp_server.py"],
  "startup_timeout_sec": 30.0
} } }
```

`hooks.json` (installed form) switches from shell-form string to exec form:

```json
{ "type": "command",
  "command": "py",
  "args": ["-3", "${CLAUDE_PLUGIN_ROOT}/skills/spec-lifecycle-manager/scripts/codex_spec_lifecycle_hook.py"],
  "timeout": 10 }
```

(On Linux/macOS the resolved `command` is `python3` with no extra arg.) The
Codex copy keeps its `${PLUGIN_ROOT}` token and its broader matcher; only the
interpreter and exec form change.

### Internal subprocessing (already portable — keep)

`codex_spec_lifecycle_hook.py` and `spec_runtime.py` spawn child processes with
`sys.executable`, which is the running interpreter and therefore correct on
every OS. No change needed; this spec must not regress it. The `#!/usr/bin/env
python3` shebangs are inert when the script is invoked via an explicit
interpreter, so they can stay.

### Error handling

- No interpreter at install: resolver throws the actionable message above
  (Requirement 1.4 / 2.4 / P4).
- No interpreter at launch (e.g., user removed Python post-install): the pinned
  command fails to spawn; document that re-install re-resolves. For the
  marketplace static path, the prerequisite doc covers this.

## Operational Considerations

- **Rollout.** Land installer + resolver + config changes together; ship a new
  package version. Unix installs keep working (`python3` is the resolved Unix
  command).
- **Backward compatibility.** Honor a documented `SPEC_LIFECYCLE_PYTHON`
  override. Existing Unix `.mcp.json` behavior is unchanged in practice.
- **Verification.** CI matrix on windows-latest / macos-latest / ubuntu-latest:
  install, MCP launch smoke, and hook execution with a Claude-shaped payload
  (`tool_name:"Write"`, `tool_input.file_path`) so the codex/Claude tool-name
  parity is exercised cross-OS. Record evidence in `verification.md`.

## Resolved Decisions

All four open questions were resolved on 2026-06-29 before implementation start.

1. **Marketplace static config — RESOLVED (option a).** The shipped
   `.mcp.json`/`hooks.json` default `command` is **`python`**, paired with a
   documented "Python 3 on PATH" prerequisite in the install docs. The
   installer-pinned path still writes the host-resolved interpreter; this static
   default only governs the zero-config marketplace install. Revisit if Windows
   users hit `python3`/`py`-only hosts where `python` is absent.
2. **Windows interpreter preference — RESOLVED.** Resolution order is
   **`py -3` → `python` → `python3`** (PEP 397 launcher first, as in the
   resolver above).
3. **Override variable name — RESOLVED.** Use **`SPEC_LIFECYCLE_PYTHON`**,
   documented once and honored by both the installer and any launcher.
4. **Hook exec support under Codex — RESOLVED (documented fallback).** No
   in-repo evidence confirms Codex honors exec-form hook entries with an `args`
   array; the repo's documented Codex hook format
   (`docs/reference/spec-lifecycle-runtime.md`) is shell-form only. Therefore:
   the Claude `hooks.json` converts to exec form, while the Codex `hooks.json`
   keeps a **shell-form string but with the installer-resolved interpreter
   pinned in** (e.g. `py -3 "..."`). True exec-form support is to be confirmed
   against the live Codex runtime during T009; upgrade the Codex entry to exec
   form if it passes. Either way the portability fix (explicit interpreter
   resolution) holds, so this does not block implementation.

## Open Questions

None remaining. All four open questions were resolved on 2026-06-29 before
implementation — see **Resolved Decisions** above. The only carried-forward
verification item (Codex exec-form hook support, §4) is tracked in
`verification.md`, not as an open design question.
