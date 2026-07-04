from __future__ import annotations

from pathlib import Path

from auriora_dev.runner import CommandSpec


def build_plugin_status_plan(repo_root: Path) -> list[CommandSpec]:
    return [
        CommandSpec.from_argv(
            "codex plugin list",
            ["codex", "plugin", "list"],
            cwd=repo_root,
        )
    ]
