from __future__ import annotations

from pathlib import Path

from auriora_dev.commands.common import NPM_ENV, PY_ENV, spec_runtime
from auriora_dev.runner import CommandSpec


def build_check_plan(repo_root: Path, *, include_package: bool = True) -> list[CommandSpec]:
    commands = [
        CommandSpec.from_argv(
            "python unit tests",
            ["python3", "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"],
            cwd=repo_root,
            env=PY_ENV,
        ),
        spec_runtime(repo_root, "scan", "."),
        spec_runtime(repo_root, "archive-index", "."),
        spec_runtime(repo_root, "prompts"),
    ]
    if include_package:
        commands.extend(
            [
                spec_runtime(repo_root, "package-contract", "."),
                CommandSpec.from_argv(
                    "npm pack dry-run",
                    ["npm", "pack", "--dry-run", "--json"],
                    cwd=repo_root,
                    env=NPM_ENV,
                ),
            ]
        )
    commands.append(
        CommandSpec.from_argv("whitespace check", ["git", "diff", "--check"], cwd=repo_root)
    )
    return commands
