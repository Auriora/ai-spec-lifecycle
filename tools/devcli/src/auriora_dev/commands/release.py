from __future__ import annotations

from pathlib import Path

from auriora_dev.commands.common import NPM_ENV, spec_runtime
from auriora_dev.runner import CommandSpec


def build_release_preflight_plan(repo_root: Path, *, allow_dirty: bool = False) -> list[CommandSpec]:
    commands = [
        CommandSpec.from_argv(
            "working tree status",
            ["git", "status", "--short"],
            cwd=repo_root,
        )
    ]
    if not allow_dirty:
        commands.append(
            CommandSpec.from_argv(
                "require clean working tree",
                ["git", "diff", "--quiet"],
                cwd=repo_root,
            )
        )
    commands.extend(
        [
            spec_runtime(repo_root, "package-contract", "."),
            CommandSpec.from_argv(
                "npm pack dry-run",
                ["npm", "pack", "--dry-run", "--json"],
                cwd=repo_root,
                env=NPM_ENV,
            ),
            spec_runtime(repo_root, "scan", "."),
        ]
    )
    return commands
