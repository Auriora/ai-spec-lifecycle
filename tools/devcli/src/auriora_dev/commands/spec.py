from __future__ import annotations

from pathlib import Path

from auriora_dev.commands.common import spec_runtime
from auriora_dev.runner import CommandSpec


def build_spec_plan(repo_root: Path, command: str, target: str | None = None) -> list[CommandSpec]:
    if command in {"scan", "archive-index"}:
        return [spec_runtime(repo_root, command, ".")]
    if command == "prompts":
        return [spec_runtime(repo_root, "prompts")]
    if command in {"summary", "lint"}:
        if not target:
            raise ValueError(f"{command} requires a target path or spec id")
        return [spec_runtime(repo_root, command, target)]
    raise ValueError(f"Unsupported spec command: {command}")
