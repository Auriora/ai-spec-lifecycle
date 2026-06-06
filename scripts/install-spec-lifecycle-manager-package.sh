#!/usr/bin/env bash
set -euo pipefail

SOURCE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
MARKETPLACE_ROOT="${SPEC_LIFECYCLE_MARKETPLACE_ROOT:-$HOME}"
MARKETPLACE_NAME="${SPEC_LIFECYCLE_MARKETPLACE_NAME:-auriora-local}"
REPO_ROOT=""
WRITE_CODEX_CONFIG=1
WRITE_CODEX_HOOKS=1
WRITE_MARKETPLACE=1
INSTALL_CODEX_PLUGIN=1
DRY_RUN=0

usage() {
  cat <<'USAGE'
Usage: install-spec-lifecycle-manager-package.sh [options]

Options:
  --source <path>       Package source root. Defaults to the checkout root.
  --codex-home <path>   Codex home. Defaults to $CODEX_HOME or ~/.codex.
  --marketplace-root <path>
                        Local marketplace root. Defaults to ~.
  --repo-root <path>    Repository root exposed by the MCP server. Defaults to source root.
  --skip-codex-config   Copy files without editing Codex config.toml.
  --skip-codex-hooks    Copy files without editing Codex hooks.json.
  --skip-marketplace    Copy files without editing the local marketplace.
  --skip-plugin-add     Do not run `codex plugin add` after copying files.
  --dry-run             Print planned actions without writing files.
  -h, --help            Show this help.
USAGE
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --source)
      SOURCE_ROOT="$2"
      shift 2
      ;;
    --codex-home)
      CODEX_HOME="$2"
      shift 2
      ;;
    --marketplace-root)
      MARKETPLACE_ROOT="$2"
      shift 2
      ;;
    --repo-root)
      REPO_ROOT="$2"
      shift 2
      ;;
    --skip-codex-config)
      WRITE_CODEX_CONFIG=0
      shift
      ;;
    --skip-codex-hooks)
      WRITE_CODEX_HOOKS=0
      shift
      ;;
    --skip-marketplace)
      WRITE_MARKETPLACE=0
      shift
      ;;
    --skip-plugin-add)
      INSTALL_CODEX_PLUGIN=0
      shift
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

SOURCE_ROOT="$(cd "$SOURCE_ROOT" && pwd)"
if [ -z "$REPO_ROOT" ]; then
  REPO_ROOT="$SOURCE_ROOT"
fi
REPO_ROOT="$(cd "$REPO_ROOT" && pwd)"
CODEX_HOME="$(mkdir -p "$CODEX_HOME" && cd "$CODEX_HOME" && pwd)"
MARKETPLACE_ROOT="$(mkdir -p "$MARKETPLACE_ROOT" && cd "$MARKETPLACE_ROOT" && pwd)"

SKILL_INSTALL_ROOT="$CODEX_HOME/skills/spec-lifecycle-manager"
PLUGIN_INSTALL_ROOT="$CODEX_HOME/plugins/spec-lifecycle-manager"
MARKETPLACE_PLUGIN_ROOT="$MARKETPLACE_ROOT/plugins/spec-lifecycle-manager"
MARKETPLACE_JSON="$MARKETPLACE_ROOT/.agents/plugins/marketplace.json"

required_paths=(
  "skills/spec-lifecycle-manager/SKILL.md"
  "skills/spec-lifecycle-manager/scripts/spec_runtime.py"
  "skills/spec-lifecycle-manager/scripts/spec_mcp_server.py"
  "skills/spec-lifecycle-manager/scripts/codex_spec_lifecycle_hook.py"
  "skills/spec-lifecycle-manager/scripts/traceability_lookup.py"
  "skills/spec-lifecycle-manager/prompts"
  "skills/spec-lifecycle-manager/references"
  "plugins/spec-lifecycle-manager/.codex-plugin/plugin.json"
  "plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/SKILL.md"
  "packaging/spec-lifecycle-manager/package-manifest.json"
)

for relative_path in "${required_paths[@]}"; do
  if [ ! -e "$SOURCE_ROOT/$relative_path" ]; then
    echo "Missing package component: $relative_path" >&2
    exit 1
  fi
done

run() {
  if [ "$DRY_RUN" -eq 1 ]; then
    printf 'dry-run:'
    printf ' %q' "$@"
    printf '\n'
  else
    "$@"
  fi
}

require_command() {
  local command_name="$1"
  local install_hint="$2"
  if ! command -v "$command_name" >/dev/null 2>&1; then
    echo "Missing required dependency: $command_name. $install_hint" >&2
    exit 1
  fi
}

ensure_python() {
  require_command python3 "Install Python 3.9 or newer before installing Spec Lifecycle Manager."
  python3 - <<'PY'
import sys
if sys.version_info < (3, 9):
    raise SystemExit(f"Python 3.9 or newer is required; found {sys.version.split()[0]}.")
PY
}

ensure_codex() {
  require_command codex "Install Codex or pass --skip-plugin-add to copy files without registering the plugin."
}

copy_tree() {
  local source_path="$1"
  local destination_path="$2"
  run mkdir -p "$(dirname "$destination_path")"
  run rm -rf "$destination_path"
  run cp -a "$source_path" "$destination_path"
}

write_codex_config() {
  local config_path="$CODEX_HOME/config.toml"
  local server_path="$SKILL_INSTALL_ROOT/scripts/spec_mcp_server.py"
  if [ "$DRY_RUN" -eq 1 ]; then
    echo "dry-run: rewrite Spec Lifecycle Manager MCP config block in $config_path"
    return
  fi

  touch "$config_path"
  if grep -q "BEGIN Spec Lifecycle Manager package install" "$config_path"; then
    local temp_config
    temp_config="$(mktemp)"
    awk '
      /# BEGIN Spec Lifecycle Manager package install/ { skipping = 1; next }
      /# END Spec Lifecycle Manager package install/ { skipping = 0; next }
      !skipping { print }
    ' "$config_path" > "$temp_config"
    mv "$temp_config" "$config_path"
  fi

  python3 - "$config_path" "$server_path" "$REPO_ROOT" <<'PY'
from pathlib import Path
import sys

config_path = Path(sys.argv[1])
server_path = sys.argv[2]
repo_root = sys.argv[3]
text = config_path.read_text(encoding="utf-8")

marker = "[mcp_servers.spec-lifecycle-manager]"
if marker in text and "BEGIN Spec Lifecycle Manager package install" not in text:
    # Preserve an existing hand-managed entry instead of creating duplicates.
    raise SystemExit(0)

block = f"""

# BEGIN Spec Lifecycle Manager package install
[mcp_servers.spec-lifecycle-manager]
command = "python3"
args = ["{server_path}", "{repo_root}"]
startup_timeout_sec = 30.0
# END Spec Lifecycle Manager package install
"""
config_path.write_text(text.rstrip() + block + "\n", encoding="utf-8")
PY
}

write_codex_hooks_json() {
  local hooks_json="$CODEX_HOME/hooks.json"
  local hook_script="$SKILL_INSTALL_ROOT/scripts/codex_spec_lifecycle_hook.py"
  if [ "$DRY_RUN" -eq 1 ]; then
    echo "dry-run: merge Spec Lifecycle Manager hook into $hooks_json"
    return
  fi

  HOOKS_JSON="$hooks_json" HOOK_SCRIPT="$hook_script" python3 - <<'PY'
import json
import os
from pathlib import Path

hooks_json = Path(os.environ["HOOKS_JSON"])
hook_script = os.environ["HOOK_SCRIPT"]

data = {"hooks": {}}
if hooks_json.exists():
    data = json.loads(hooks_json.read_text(encoding="utf-8"))
if not isinstance(data, dict):
    data = {"hooks": {}}
hooks = data.setdefault("hooks", {})
if not isinstance(hooks, dict):
    data["hooks"] = hooks = {}

entries = hooks.get("PostToolUse")
if not isinstance(entries, list):
    entries = []

def keep_entry(entry):
    if not isinstance(entry, dict):
        return False
    entry_hooks = entry.get("hooks")
    if not isinstance(entry_hooks, list):
        return True
    entry["hooks"] = [
        hook for hook in entry_hooks
        if "/spec-lifecycle-manager/scripts/codex_spec_lifecycle_hook.py" not in str(hook.get("command", ""))
    ]
    return bool(entry["hooks"])

entries = [entry for entry in entries if keep_entry(entry)]
entries.insert(0, {
    "matcher": "^(apply_patch|write_file|create_file)$",
    "hooks": [
        {
            "type": "command",
            "command": f"python3 {hook_script}",
            "statusMessage": "running spec lifecycle advisory hook"
        }
    ]
})
hooks["PostToolUse"] = entries

hooks_json.parent.mkdir(parents=True, exist_ok=True)
hooks_json.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
PY
}

write_marketplace_json() {
  if [ "$DRY_RUN" -eq 1 ]; then
    echo "dry-run: add Spec Lifecycle Manager to $MARKETPLACE_JSON"
    return
  fi

  MARKETPLACE_JSON="$MARKETPLACE_JSON" MARKETPLACE_NAME="$MARKETPLACE_NAME" python3 - <<'PY'
import json
import os
from pathlib import Path

marketplace_json = Path(os.environ["MARKETPLACE_JSON"])
marketplace_name = os.environ["MARKETPLACE_NAME"]
entry = {
    "name": "spec-lifecycle-manager",
    "source": {
        "source": "local",
        "path": "./plugins/spec-lifecycle-manager",
    },
    "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL",
    },
    "category": "Developer Tools",
}

data = {
    "name": marketplace_name,
    "interface": {"displayName": "Auriora Local Plugins"},
    "plugins": [],
}
if marketplace_json.exists():
    data = json.loads(marketplace_json.read_text(encoding="utf-8"))
if not isinstance(data, dict):
    data = {}
data.setdefault("name", marketplace_name)
data.setdefault("interface", {"displayName": "Auriora Local Plugins"})
if not isinstance(data.get("interface"), dict):
    data["interface"] = {"displayName": "Auriora Local Plugins"}
data["interface"].setdefault("displayName", "Auriora Local Plugins")
plugins = data.get("plugins")
if not isinstance(plugins, list):
    plugins = []

plugins = [plugin for plugin in plugins if plugin.get("name") != entry["name"]]
plugins.append(entry)
data["plugins"] = plugins

marketplace_json.parent.mkdir(parents=True, exist_ok=True)
marketplace_json.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
PY
}

install_codex_plugin() {
  ensure_codex
  run codex plugin add "spec-lifecycle-manager@$MARKETPLACE_NAME"
}

ensure_python
copy_tree "$SOURCE_ROOT/skills/spec-lifecycle-manager" "$SKILL_INSTALL_ROOT"
copy_tree "$SOURCE_ROOT/plugins/spec-lifecycle-manager" "$PLUGIN_INSTALL_ROOT"
copy_tree "$SOURCE_ROOT/plugins/spec-lifecycle-manager" "$MARKETPLACE_PLUGIN_ROOT"
run chmod +x "$SKILL_INSTALL_ROOT/scripts/spec_runtime.py"
run chmod +x "$SKILL_INSTALL_ROOT/scripts/spec_mcp_server.py"
run chmod +x "$SKILL_INSTALL_ROOT/scripts/codex_spec_lifecycle_hook.py"
run chmod +x "$SKILL_INSTALL_ROOT/scripts/traceability_lookup.py"

if [ "$WRITE_CODEX_CONFIG" -eq 1 ]; then
  write_codex_config
fi
if [ "$WRITE_CODEX_HOOKS" -eq 1 ]; then
  write_codex_hooks_json
fi
if [ "$WRITE_MARKETPLACE" -eq 1 ]; then
  write_marketplace_json
fi
if [ "$INSTALL_CODEX_PLUGIN" -eq 1 ]; then
  install_codex_plugin
fi

echo "Spec Lifecycle Manager installed at $CODEX_HOME"
