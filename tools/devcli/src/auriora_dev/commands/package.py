from __future__ import annotations

from pathlib import Path

from auriora_dev.commands.common import NPM_ENV, spec_runtime
from auriora_dev.runner import CommandSpec


def build_package_check_plan(repo_root: Path) -> list[CommandSpec]:
    return [
        spec_runtime(repo_root, "package-contract", "."),
        CommandSpec.from_argv(
            "npm pack dry-run",
            ["npm", "pack", "--dry-run", "--json"],
            cwd=repo_root,
            env=NPM_ENV,
        ),
        spec_runtime(repo_root, "sync-guard", "."),
    ]


def build_package_pack_plan(repo_root: Path, *, write: bool = False) -> list[CommandSpec]:
    argv = ["npm", "pack"]
    if not write:
        argv.extend(["--dry-run", "--json"])
    return [
        CommandSpec.from_argv(
            "npm pack" if write else "npm pack dry-run",
            argv,
            cwd=repo_root,
            env=NPM_ENV if not write else None,
            mutates=write,
        )
    ]


def build_install_local_plan(
    repo_root: Path,
    *,
    source: str | None = None,
    codex_home: str | None = None,
    marketplace_root: str | None = None,
    repo_root_option: str | None = None,
    skip_marketplace: bool = False,
    skip_plugin_add: bool = False,
    dry_run: bool = False,
) -> list[CommandSpec]:
    argv = ["scripts/install-spec-lifecycle-manager-package.sh"]
    for flag, value in (
        ("--source", source),
        ("--codex-home", codex_home),
        ("--marketplace-root", marketplace_root),
        ("--repo-root", repo_root_option),
    ):
        if value:
            argv.extend([flag, value])
    if skip_marketplace:
        argv.append("--skip-marketplace")
    if skip_plugin_add:
        argv.append("--skip-plugin-add")
    if dry_run:
        argv.append("--dry-run")
    return [
        CommandSpec.from_argv(
            "test installer in isolated roots",
            argv,
            cwd=repo_root,
            mutates=not dry_run,
        )
    ]
