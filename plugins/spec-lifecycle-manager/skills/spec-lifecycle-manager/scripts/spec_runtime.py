#!/usr/bin/env python3
"""Retained runtime/recovery adapter for shared lifecycle internals.

Agent-facing lifecycle tools are owned by the MCP server. This script remains
for validation, package checks, hooks, and no-MCP recovery; reusable behavior
lives in ``lifecycle.core``.
"""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from lifecycle.core import *  # noqa: F401,F403 - compatibility adapter
from lifecycle.runtime_adapter import main


if __name__ == "__main__":
    raise SystemExit(main())
