from __future__ import annotations

from pathlib import Path

from auriora_dev.commands.common import spec_runtime
from auriora_dev.runner import CommandSpec


BUNDLE_TARGETS = (
    "plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/",
    "plugins/spec-lifecycle-manager/claude-plugin/skills/spec-lifecycle-manager/",
)


def build_bundles_plan(repo_root: Path) -> list[CommandSpec]:
    source = "skills/spec-lifecycle-manager/."
    commands = [
        CommandSpec.from_argv(
            f"sync source skill to {target}",
            ["cp", "-a", source, target],
            cwd=repo_root,
            mutates=True,
        )
        for target in BUNDLE_TARGETS
    ]
    commands.append(spec_runtime(repo_root, "package-contract", "."))
    return commands


def build_guard_plan(repo_root: Path) -> list[CommandSpec]:
    return [spec_runtime(repo_root, "sync-guard", ".")]
