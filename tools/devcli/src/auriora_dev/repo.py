from __future__ import annotations

from pathlib import Path


ROOT_MARKERS = ("AGENTS.md", "package.json", "skills/spec-lifecycle-manager")


def discover_repo_root(start: Path | None = None) -> Path:
    """Find the repository root from a path inside the checkout."""
    current = (start or Path.cwd()).resolve()
    if current.is_file():
        current = current.parent

    for candidate in (current, *current.parents):
        if all((candidate / marker).exists() for marker in ROOT_MARKERS):
            return candidate

    marker_list = ", ".join(ROOT_MARKERS)
    raise RuntimeError(f"Could not find repository root with markers: {marker_list}")


def resolve_repo_root(repo_root: Path | str | None = None) -> Path:
    if repo_root is None:
        return discover_repo_root(Path.cwd())
    return Path(repo_root).expanduser().resolve()


def repo_relative(path: Path | str, repo_root: Path | str | None = None) -> str:
    root = resolve_repo_root(repo_root)
    target = Path(path).expanduser().resolve()
    try:
        return target.relative_to(root).as_posix()
    except ValueError:
        return str(target)
