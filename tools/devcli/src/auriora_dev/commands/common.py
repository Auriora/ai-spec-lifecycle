from __future__ import annotations

from pathlib import Path

import typer

from auriora_dev.runner import CommandResult, CommandSpec, render_plan, run_plan


PY_ENV = {"PYTHONDONTWRITEBYTECODE": "1"}
NPM_ENV = {"npm_config_cache": "/tmp/spec-lifecycle-npm-cache"}


def spec_runtime(repo_root: Path, *args: str) -> CommandSpec:
    return CommandSpec.from_argv(
        "spec_runtime " + " ".join(args),
        ["python3", "skills/spec-lifecycle-manager/scripts/spec_runtime.py", *args],
        cwd=repo_root,
        env=PY_ENV,
    )


def print_or_run(
    commands: list[CommandSpec],
    *,
    repo_root: Path,
    dry_run: bool,
) -> list[CommandResult]:
    if dry_run:
        typer.secho("Dry run command plan", bold=True)
        for line in render_plan(commands, repo_root=repo_root):
            typer.echo(line)
        return run_plan(commands, repo_root=repo_root, dry_run=True)

    results = run_plan(commands, repo_root=repo_root)
    for result in results:
        color = typer.colors.GREEN if result.ok else typer.colors.RED
        status = "passed" if result.ok else f"failed ({result.exit_code})"
        typer.secho(f"{result.spec.label}: {status}", fg=color)
        if result.stdout:
            typer.echo(result.stdout.rstrip())
        if result.stderr:
            typer.echo(result.stderr.rstrip(), err=True)
    if results and not results[-1].ok:
        raise typer.Exit(code=results[-1].exit_code)
    return results
