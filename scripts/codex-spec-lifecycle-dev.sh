#!/usr/bin/env sh
# Launch an isolated Spec Lifecycle Manager development session. Packaged
# plugins are disabled for this process only; project skill/MCP/hook discovery
# then resolves directly from this checkout without modifying user-wide state.
set -eu

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
REPO_ROOT="$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)"

exec codex --disable plugins -C "$REPO_ROOT" "$@"
