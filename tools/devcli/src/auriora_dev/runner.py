from __future__ import annotations

import subprocess
import time
from collections.abc import Callable, Sequence
from dataclasses import dataclass
import os
from pathlib import Path

from .repo import repo_relative, resolve_repo_root


Runner = Callable[..., subprocess.CompletedProcess[str]]


@dataclass(frozen=True)
class CommandSpec:
    label: str
    argv: tuple[str, ...]
    cwd: Path | None = None
    mutates: bool = False
    env: dict[str, str] | None = None

    @classmethod
    def from_argv(
        cls,
        label: str,
        argv: Sequence[str],
        *,
        cwd: Path | str | None = None,
        mutates: bool = False,
        env: dict[str, str] | None = None,
    ) -> "CommandSpec":
        return cls(
            label=label,
            argv=tuple(argv),
            cwd=Path(cwd) if cwd is not None else None,
            mutates=mutates,
            env=env,
        )


@dataclass(frozen=True)
class CommandResult:
    spec: CommandSpec
    exit_code: int
    elapsed_seconds: float
    stdout: str = ""
    stderr: str = ""

    @property
    def ok(self) -> bool:
        return self.exit_code == 0


def shell_quote(argv: Sequence[str]) -> str:
    return " ".join(_quote_arg(arg) for arg in argv)


def render_plan(
    commands: Sequence[CommandSpec],
    *,
    repo_root: Path | str | None = None,
) -> list[str]:
    root = resolve_repo_root(repo_root)
    lines: list[str] = []
    for index, command in enumerate(commands, start=1):
        cwd = command.cwd or root
        mutation = "mutates" if command.mutates else "read-only"
        prefix = ""
        if command.env:
            prefix = "".join(
                f"{key}={_quote_arg(value)} " for key, value in sorted(command.env.items())
            )
        lines.append(
            f"{index}. {command.label} [{mutation}] "
            f"(cwd: {repo_relative(cwd, root)}): {prefix}{shell_quote(command.argv)}"
        )
    return lines


def run_plan(
    commands: Sequence[CommandSpec],
    *,
    repo_root: Path | str | None = None,
    dry_run: bool = False,
    runner: Runner = subprocess.run,
) -> list[CommandResult]:
    if dry_run:
        return [
            CommandResult(spec=command, exit_code=0, elapsed_seconds=0.0)
            for command in commands
        ]

    root = resolve_repo_root(repo_root)
    results: list[CommandResult] = []
    for command in commands:
        started = time.monotonic()
        env = None
        if command.env:
            env = {**os.environ, **command.env}
        try:
            completed = runner(
                list(command.argv),
                cwd=command.cwd or root,
                text=True,
                capture_output=True,
                check=False,
                env=env,
            )
        except FileNotFoundError as exc:
            result = CommandResult(
                spec=command,
                exit_code=127,
                elapsed_seconds=time.monotonic() - started,
                stderr=str(exc),
            )
            results.append(result)
            break
        result = CommandResult(
            spec=command,
            exit_code=completed.returncode,
            elapsed_seconds=time.monotonic() - started,
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
        )
        results.append(result)
        if not result.ok:
            break
    return results


def _quote_arg(arg: str) -> str:
    if arg and all(char.isalnum() or char in "-_./:=@" for char in arg):
        return arg
    return "'" + arg.replace("'", "'\"'\"'") + "'"
