from __future__ import annotations

from pathlib import Path

import typer

from auriora_dev.commands.check import build_check_plan
from auriora_dev.commands.common import print_or_run
from auriora_dev.commands.doctor import collect_doctor_status
from auriora_dev.commands.package import (
    build_install_local_plan,
    build_package_check_plan,
    build_package_pack_plan,
)
from auriora_dev.commands.plugin import build_plugin_status_plan
from auriora_dev.commands.release import build_release_preflight_plan
from auriora_dev.commands.spec import build_spec_plan
from auriora_dev.commands.sync import build_bundles_plan, build_guard_plan
from auriora_dev.repo import resolve_repo_root


app = typer.Typer(
    no_args_is_help=True,
    help="Developer CLI for Spec Lifecycle Manager maintenance.",
)
package_app = typer.Typer(help="Package and local install helpers.")
plugin_app = typer.Typer(help="Read-only plugin status helpers.")
release_app = typer.Typer(help="Release preflight helpers.")
spec_app = typer.Typer(help="Spec lifecycle runtime wrappers.")
sync_app = typer.Typer(help="Source-to-bundle sync helpers.")

app.add_typer(package_app, name="package")
app.add_typer(plugin_app, name="plugin")
app.add_typer(release_app, name="release")
app.add_typer(spec_app, name="spec")
app.add_typer(sync_app, name="sync")


RepoRootOption = typer.Option(
    None,
    "--repo-root",
    help="Repository root. Defaults to upward discovery from the current directory.",
)
DryRunOption = typer.Option(False, "--dry-run", help="Print the command plan without running it.")


def _root(repo_root: Path | None) -> Path:
    return resolve_repo_root(repo_root)


@app.command()
def check(
    repo_root: Path | None = RepoRootOption,
    dry_run: bool = DryRunOption,
    skip_package: bool = typer.Option(
        False,
        "--skip-package",
        help="Run a reduced validation plan without package-contract and npm pack.",
    ),
) -> None:
    """Run the local validation plan."""
    root = _root(repo_root)
    if skip_package:
        typer.secho("Reduced scope: package validation stages are skipped.", fg=typer.colors.YELLOW)
    print_or_run(build_check_plan(root, include_package=not skip_package), repo_root=root, dry_run=dry_run)


@app.command()
def doctor(repo_root: Path | None = RepoRootOption) -> None:
    """Report local toolchain and repository metadata status."""
    root = _root(repo_root)
    for name, state in collect_doctor_status(root):
        typer.echo(f"{name}: {state}")


@sync_app.command("bundles")
def sync_bundles(
    repo_root: Path | None = RepoRootOption,
    dry_run: bool = DryRunOption,
) -> None:
    """Copy source skill files into bundled plugin copies."""
    root = _root(repo_root)
    print_or_run(build_bundles_plan(root), repo_root=root, dry_run=dry_run)


@sync_app.command("guard")
def sync_guard(
    repo_root: Path | None = RepoRootOption,
    dry_run: bool = DryRunOption,
) -> None:
    """Run the lifecycle sync guard."""
    root = _root(repo_root)
    print_or_run(build_guard_plan(root), repo_root=root, dry_run=dry_run)


@package_app.command("check")
def package_check(
    repo_root: Path | None = RepoRootOption,
    dry_run: bool = DryRunOption,
) -> None:
    """Run package contract, npm dry-run, and sync guard."""
    root = _root(repo_root)
    print_or_run(build_package_check_plan(root), repo_root=root, dry_run=dry_run)


@package_app.command("pack")
def package_pack(
    repo_root: Path | None = RepoRootOption,
    dry_run: bool = typer.Option(True, "--dry-run/--write", help="Dry-run by default; use --write to create a tarball."),
) -> None:
    """Run npm pack in dry-run mode unless --write is explicit."""
    root = _root(repo_root)
    print_or_run(build_package_pack_plan(root, write=not dry_run), repo_root=root, dry_run=False)


@package_app.command("install-local")
def package_install_local(
    repo_root: Path | None = RepoRootOption,
    source: str | None = typer.Option(None, "--source", help="Package source root."),
    codex_home: str | None = typer.Option(None, "--codex-home", help="Codex home override."),
    marketplace_root: str | None = typer.Option(None, "--marketplace-root", help="Local marketplace root."),
    installer_repo_root: str | None = typer.Option(None, "--installer-repo-root", help="Repository root passed through to the installer as --repo-root."),
    skip_marketplace: bool = typer.Option(False, "--skip-marketplace", help="Do not update the local marketplace."),
    skip_plugin_add: bool = typer.Option(False, "--skip-plugin-add", help="Do not run codex plugin add."),
    dry_run: bool = DryRunOption,
) -> None:
    """Invoke the authoritative local installer."""
    root = _root(repo_root)
    print_or_run(
        build_install_local_plan(
            root,
            source=source,
            codex_home=codex_home,
            marketplace_root=marketplace_root,
            repo_root_option=installer_repo_root,
            skip_marketplace=skip_marketplace,
            skip_plugin_add=skip_plugin_add,
            dry_run=dry_run,
        ),
        repo_root=root,
        dry_run=False,
    )
    if not dry_run:
        typer.echo("Next verification: slc sync guard")


@plugin_app.command("status")
def plugin_status(
    repo_root: Path | None = RepoRootOption,
    dry_run: bool = DryRunOption,
) -> None:
    """Run read-only Codex plugin status."""
    root = _root(repo_root)
    print_or_run(build_plugin_status_plan(root), repo_root=root, dry_run=dry_run)


@spec_app.command("scan")
def spec_scan(repo_root: Path | None = RepoRootOption, dry_run: bool = DryRunOption) -> None:
    """Run spec_runtime.py scan."""
    root = _root(repo_root)
    print_or_run(build_spec_plan(root, "scan"), repo_root=root, dry_run=dry_run)


@spec_app.command("archive-index")
def spec_archive_index(repo_root: Path | None = RepoRootOption, dry_run: bool = DryRunOption) -> None:
    """Run spec_runtime.py archive-index."""
    root = _root(repo_root)
    print_or_run(build_spec_plan(root, "archive-index"), repo_root=root, dry_run=dry_run)


@spec_app.command("prompts")
def spec_prompts(repo_root: Path | None = RepoRootOption, dry_run: bool = DryRunOption) -> None:
    """Run spec_runtime.py prompts."""
    root = _root(repo_root)
    print_or_run(build_spec_plan(root, "prompts"), repo_root=root, dry_run=dry_run)


@spec_app.command("summary")
def spec_summary(
    target: str = typer.Argument(..., help="Spec package path or ID."),
    repo_root: Path | None = RepoRootOption,
    dry_run: bool = DryRunOption,
) -> None:
    """Run spec_runtime.py summary."""
    root = _root(repo_root)
    print_or_run(build_spec_plan(root, "summary", target), repo_root=root, dry_run=dry_run)


@spec_app.command("lint")
def spec_lint(
    target: str = typer.Argument(..., help="Spec package path or ID."),
    repo_root: Path | None = RepoRootOption,
    dry_run: bool = DryRunOption,
) -> None:
    """Run spec_runtime.py lint."""
    root = _root(repo_root)
    print_or_run(build_spec_plan(root, "lint", target), repo_root=root, dry_run=dry_run)


@release_app.command("preflight")
def release_preflight(
    repo_root: Path | None = RepoRootOption,
    dry_run: bool = DryRunOption,
    allow_dirty: bool = typer.Option(
        False,
        "--allow-dirty",
        help="Continue after reporting dirty working-tree state.",
    ),
) -> None:
    """Run local release preflight without push, tag, publish, or GitHub release mutation."""
    root = _root(repo_root)
    typer.echo("Release mutation is out of scope: no push, tag, npm publish, or GitHub release command is run.")
    print_or_run(build_release_preflight_plan(root, allow_dirty=allow_dirty), repo_root=root, dry_run=dry_run)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
