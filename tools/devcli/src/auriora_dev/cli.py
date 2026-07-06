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
from auriora_dev.commands.release import (
    build_github_release_plan,
    build_release_tag_plan,
    bump_semver,
    current_package_version,
    git_status_short,
    normalize_version,
    update_release_version,
    verify_release_artifacts,
)
from auriora_dev.commands.release_notes import (
    ReleaseNotesError,
    collect_release_notes_evidence,
    evidence_to_json,
    render_agent_instructions,
    render_release_notes,
    write_text_output,
)
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


@release_app.command("bump-version")
def release_bump_version(
    version: str | None = typer.Argument(None, help="Target version, for example 0.2.2 or v0.2.2."),
    part: str | None = typer.Option(None, "--part", help="Semver part to bump: major, minor, or patch."),
    repo_root: Path | None = RepoRootOption,
    dry_run: bool = DryRunOption,
) -> None:
    """Update release version metadata and current install docs."""
    root = _root(repo_root)
    if version is None:
        if part is None:
            typer.secho("Pass a target version or --part major|minor|patch.", fg=typer.colors.RED)
            raise typer.Exit(code=2)
        version = bump_semver(current_package_version(root), part)
    elif part is not None:
        typer.secho("Pass either a target version or --part, not both.", fg=typer.colors.RED)
        raise typer.Exit(code=2)
    normalized = normalize_version(version)
    typer.echo(f"target version: {normalized}")
    if dry_run:
        typer.echo("dry-run: would update release metadata and current install docs")
        return
    changed = update_release_version(root, normalized)
    if not changed:
        typer.echo("Version metadata already matches.")
        return
    typer.secho("Updated release version metadata:", fg=typer.colors.GREEN)
    for path in changed:
        typer.echo(f"- {path.relative_to(root)}")


@release_app.command("tag")
def release_tag(
    version: str | None = typer.Argument(None, help="Release version. Defaults to package.json#/version."),
    remote: str = typer.Option("origin", "--remote", help="Git remote to push the tag to."),
    no_push: bool = typer.Option(False, "--no-push", help="Create the local tag without pushing it."),
    force: bool = typer.Option(False, "--force", help="Allow a dirty working tree and replace an existing tag."),
    repo_root: Path | None = RepoRootOption,
    dry_run: bool = DryRunOption,
) -> None:
    """Create and optionally push an annotated release tag."""
    root = _root(repo_root)
    normalized = normalize_version(version or current_package_version(root))
    try:
        notes_path = verify_release_artifacts(root, normalized)
        if not force and git_status_short(root).strip():
            typer.secho("Working tree is dirty; pass --force to continue.", fg=typer.colors.RED)
            raise typer.Exit(code=1)
    except ValueError as exc:
        typer.secho(str(exc), fg=typer.colors.RED)
        raise typer.Exit(code=1) from exc
    typer.echo(f"release tag: v{normalized}")
    typer.echo(f"release notes: {notes_path.relative_to(root)}")
    print_or_run(
        build_release_tag_plan(root, version=normalized, remote=remote, push=not no_push, force=force),
        repo_root=root,
        dry_run=dry_run,
    )


@release_app.command("github")
def release_github(
    version: str | None = typer.Argument(None, help="Release version. Defaults to package.json#/version."),
    notes_file: Path | None = typer.Option(None, "--notes-file", help="Release notes file for gh release create."),
    title: str | None = typer.Option(None, "--title", help="Release title. Defaults to v<version>."),
    draft: bool = typer.Option(False, "--draft", help="Create the GitHub release as a draft."),
    prerelease: bool = typer.Option(False, "--prerelease", help="Mark the GitHub release as a prerelease."),
    existing: bool = typer.Option(False, "--existing", help="Upload the tarball to an existing GitHub release."),
    no_tag: bool = typer.Option(False, "--no-tag", help="Do not create a local git tag."),
    no_push_tag: bool = typer.Option(False, "--no-push-tag", help="Do not push the git tag before creating the release."),
    skip_preflight: bool = typer.Option(False, "--skip-preflight", help="Skip release preflight checks."),
    repo_root: Path | None = RepoRootOption,
    dry_run: bool = DryRunOption,
) -> None:
    """Build a tarball and create or update a GitHub release."""
    root = _root(repo_root)
    normalized = normalize_version(version or current_package_version(root))
    print_or_run(
        build_github_release_plan(
            root,
            version=normalized,
            notes_file=notes_file,
            title=title,
            draft=draft,
            prerelease=prerelease,
            existing=existing,
            create_tag=not no_tag and not existing,
            push_tag=not no_push_tag and not existing,
            preflight=not skip_preflight,
        ),
        repo_root=root,
        dry_run=dry_run,
    )


@release_app.command("notes")
def release_notes(
    from_ref: str | None = typer.Option(None, "--from", help="Lower bound ref. Defaults to latest reachable stable vX.Y.Z tag."),
    to_ref: str = typer.Option("HEAD", "--to", help="Upper bound ref."),
    version: str | None = typer.Option(None, "--version", help="Display version. Defaults to package.json#/version."),
    output: Path | None = typer.Option(None, "--output", help="Markdown output path."),
    release_format: str = typer.Option("draft", "--format", help="Output format: draft, github, markdown, or agent."),
    include_evidence: bool = typer.Option(False, "--include-evidence", help="Include compact evidence in Markdown output."),
    evidence_output: Path | None = typer.Option(None, "--evidence-output", help="Structured JSON evidence output path."),
    validation_note: str | None = typer.Option(None, "--validation-note", help="Manual validation summary to include."),
    validation_file: Path | None = typer.Option(None, "--validation-file", help="Local validation evidence file to include."),
    final: bool = typer.Option(False, "--final", help="Mark output as maintainer-reviewed final notes."),
    dry_run: bool = typer.Option(False, "--dry-run", help="Print generated notes without writing files."),
    agent_instructions: Path | None = typer.Option(None, "--agent-instructions", help="Write an agent-ready refinement prompt."),
    repo_root: Path | None = RepoRootOption,
) -> None:
    """Generate release-note evidence, draft notes, and optional agent instructions."""
    if release_format not in {"draft", "github", "markdown", "agent"}:
        typer.secho("--format must be one of: draft, github, markdown, agent.", fg=typer.colors.RED)
        raise typer.Exit(code=2)
    root = _root(repo_root)
    try:
        evidence = collect_release_notes_evidence(
            root,
            from_ref=from_ref,
            to_ref=to_ref,
            version=version or current_package_version(root),
            validation_note=validation_note,
            validation_file=validation_file,
        )
        markdown = render_release_notes(
            evidence,
            release_format=release_format,  # type: ignore[arg-type]
            include_evidence=include_evidence,
            final=final,
        )
        if evidence_output is not None:
            evidence_path = evidence_output if evidence_output.is_absolute() else root / evidence_output
            write_text_output(evidence_path, evidence_to_json(evidence), dry_run=dry_run)
            if not dry_run:
                typer.echo(f"Wrote evidence: {evidence_path.relative_to(root)}")
        else:
            evidence_path = None
        if agent_instructions is not None:
            agent_path = agent_instructions if agent_instructions.is_absolute() else root / agent_instructions
            write_text_output(
                agent_path,
                render_agent_instructions(evidence, evidence_output=evidence_output),
                dry_run=dry_run,
            )
            if not dry_run:
                typer.echo(f"Wrote agent instructions: {agent_path.relative_to(root)}")
        if output is not None and not dry_run:
            output_path = output if output.is_absolute() else root / output
            write_text_output(output_path, markdown, dry_run=False)
            typer.echo(f"Wrote release notes: {output_path.relative_to(root)}")
            return
        typer.echo(markdown)
    except ReleaseNotesError as exc:
        typer.secho(str(exc), fg=typer.colors.RED)
        raise typer.Exit(code=1) from exc


def main() -> None:
    app()


if __name__ == "__main__":
    main()
