"""Internal traceability lookup helpers.

The executable ``traceability_lookup.py`` is migrated later in spec 030. This
module provides the internal import location that MCP and retained adapters can
target as the migration progresses.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import traceability_lookup


def task_lookup(spec_path: Path, task_id: str) -> dict[str, Any]:
    return traceability_lookup.task_lookup(spec_path, task_id)


def reverse_lookup(spec_path: Path, lookup_type: str, value: str) -> dict[str, Any]:
    return traceability_lookup.reverse_lookup(spec_path, lookup_type, value)
