#!/usr/bin/env sh
# Spec 028: the installer logic now lives in a single cross-platform Node module
# (packaging/spec-lifecycle-manager/installer.mjs). This script is retained only
# as a thin delegator for existing Unix workflows so it cannot diverge from the
# canonical implementation. All options are forwarded unchanged.
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
INSTALLER="$SCRIPT_DIR/../packaging/spec-lifecycle-manager/installer.mjs"
DEFAULT_SOURCE="$(cd "$SCRIPT_DIR/.." && pwd)"

if ! command -v node >/dev/null 2>&1; then
  echo "Missing required dependency: node. Install Node.js 18+ to run the installer." >&2
  exit 1
fi

# Preserve the legacy default source (the checkout root); any --source the
# caller passes appears later in "$@" and wins (last --source takes effect).
exec node "$INSTALLER" --source "$DEFAULT_SOURCE" "$@"
