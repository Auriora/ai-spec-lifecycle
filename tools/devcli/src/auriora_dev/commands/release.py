from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Any

from auriora_dev.commands.common import NPM_ENV, spec_runtime
from auriora_dev.runner import CommandSpec


SEMVER_RE = re.compile(
    r"^(?P<major>0|[1-9]\d*)\."
    r"(?P<minor>0|[1-9]\d*)\."
    r"(?P<patch>0|[1-9]\d*)"
    r"(?P<suffix>[-+][0-9A-Za-z.-]+)?$"
)

VERSION_JSON_POINTERS = (
    ("package.json", ("version",)),
    ("plugins/spec-lifecycle-manager/.codex-plugin/plugin.json", ("version",)),
    ("plugins/spec-lifecycle-manager/claude-plugin/.claude-plugin/plugin.json", ("version",)),
)

CURRENT_DOC_PATHS = (
    "README.md",
    "packaging/spec-lifecycle-manager/npm-package.json",
    "packaging/spec-lifecycle-manager/marketplace-pinned.json",
)


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


def build_release_tag_plan(
    repo_root: Path,
    *,
    version: str,
    remote: str,
    push: bool,
    force: bool,
) -> list[CommandSpec]:
    tag = release_tag(version)
    tag_argv = ["git", "tag"]
    if force:
        tag_argv.append("-f")
    tag_argv.extend(["-a", tag, "-m", f"Release {tag}"])
    commands = [
        CommandSpec.from_argv("Create annotated release tag", tag_argv, cwd=repo_root, mutates=True)
    ]
    if push:
        push_argv = ["git", "push"]
        if force:
            push_argv.append("--force")
        push_argv.extend([remote, tag])
        commands.append(
            CommandSpec.from_argv("Push release tag", push_argv, cwd=repo_root, mutates=True)
        )
    return commands


def build_github_release_plan(
    repo_root: Path,
    *,
    version: str,
    notes_file: Path | None,
    title: str | None,
    draft: bool,
    prerelease: bool,
    existing: bool,
    create_tag: bool,
    push_tag: bool,
    preflight: bool,
) -> list[CommandSpec]:
    normalized = normalize_version(version)
    tag = release_tag(normalized)
    tarball = tarball_name(normalized)
    commands: list[CommandSpec] = []
    if preflight:
        commands.extend(build_release_preflight_plan(repo_root, allow_dirty=True))
    commands.append(
        CommandSpec.from_argv(
            "Create GitHub release tarball",
            ["env", "npm_config_cache=/tmp/spec-lifecycle-npm-cache", "npm", "pack"],
            cwd=repo_root,
            mutates=True,
        )
    )
    if existing:
        commands.append(
            CommandSpec.from_argv(
                "Upload tarball to existing GitHub release",
                ["gh", "release", "upload", tag, tarball, "--clobber"],
                cwd=repo_root,
                mutates=True,
            )
        )
        return commands
    if create_tag:
        commands.append(
            CommandSpec.from_argv(
                "Create release tag",
                ["git", "tag", "-a", tag, "-m", f"Release {tag}"],
                cwd=repo_root,
                mutates=True,
            )
        )
    if push_tag:
        commands.append(
            CommandSpec.from_argv(
                "Push release tag",
                ["git", "push", "origin", tag],
                cwd=repo_root,
                mutates=True,
            )
        )
    argv = ["gh", "release", "create", tag, tarball, "--title", title or tag]
    if notes_file is None:
        argv.append("--generate-notes")
    else:
        argv.extend(["--notes-file", str(notes_file)])
    if draft:
        argv.append("--draft")
    if prerelease:
        argv.append("--prerelease")
    commands.append(CommandSpec.from_argv("Create GitHub release", argv, cwd=repo_root, mutates=True))
    return commands


def release_tag(version: str) -> str:
    return f"v{normalize_version(version)}"


def tarball_name(version: str) -> str:
    return f"auriora-ai-spec-lifecycle-{normalize_version(version)}.tgz"


def install_command(version: str) -> str:
    normalized = normalize_version(version)
    return (
        "npm install -g "
        f"https://github.com/Auriora/ai-spec-lifecycle/releases/download/v{normalized}/"
        f"auriora-ai-spec-lifecycle-{normalized}.tgz"
    )


def normalize_version(version: str) -> str:
    normalized = version.removeprefix("v")
    if SEMVER_RE.match(normalized) is None:
        raise ValueError(f"Expected a semantic version like 0.2.1, got {version!r}.")
    return normalized


def bump_semver(version: str, part: str) -> str:
    match = SEMVER_RE.match(normalize_version(version))
    if match is None:
        raise ValueError(f"Cannot bump non-semver version {version!r}.")
    major = int(match.group("major"))
    minor = int(match.group("minor"))
    patch = int(match.group("patch"))
    if part == "major":
        return f"{major + 1}.0.0"
    if part == "minor":
        return f"{major}.{minor + 1}.0"
    if part == "patch":
        return f"{major}.{minor}.{patch + 1}"
    raise ValueError(f"Unsupported version part {part!r}.")


def current_package_version(repo_root: Path) -> str:
    package = json.loads((repo_root / "package.json").read_text(encoding="utf-8"))
    version = package.get("version")
    if not isinstance(version, str):
        raise ValueError("package.json#/version is missing or is not a string.")
    return normalize_version(version)


def verify_release_artifacts(repo_root: Path, version: str) -> Path:
    normalized = normalize_version(version)
    failures: list[str] = []
    for relative, pointer in VERSION_JSON_POINTERS:
        path = repo_root / relative
        value = _get_json_pointer(_read_json(path), pointer)
        if value != normalized:
            failures.append(
                f"{relative}#/{'/'.join(pointer)} is {value!r}; expected {normalized!r}."
            )

    notes_path = repo_root / "docs" / "release-notes" / f"v{normalized}.md"
    if not notes_path.exists():
        failures.append(f"Missing release notes: {notes_path.relative_to(repo_root)}.")

    if failures:
        raise ValueError("Release artifact checks failed:\n- " + "\n- ".join(failures))
    return notes_path


def update_release_version(repo_root: Path, version: str) -> list[Path]:
    normalized = normalize_version(version)
    changed: list[Path] = []
    replacements = {
        re.compile(r"v\d+\.\d+\.\d+"): f"v{normalized}",
        re.compile(r"auriora-ai-spec-lifecycle-\d+\.\d+\.\d+\.tgz"): tarball_name(normalized),
    }
    for relative, pointer in VERSION_JSON_POINTERS:
        path = repo_root / relative
        data = _read_json(path)
        if _set_json_pointer(data, pointer, normalized):
            _write_json(path, data)
            changed.append(path)

    for relative in CURRENT_DOC_PATHS:
        path = repo_root / relative
        text = path.read_text(encoding="utf-8")
        updated = text
        for pattern, replacement in replacements.items():
            updated = pattern.sub(replacement, updated)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            changed.append(path)

    return sorted(set(changed))


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object.")
    return value


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def _set_json_pointer(data: dict[str, Any], pointer: tuple[str, ...], value: str) -> bool:
    current: Any = data
    for key in pointer[:-1]:
        if not isinstance(current, dict) or key not in current:
            raise ValueError(f"Missing JSON object path: {'/'.join(pointer)}")
        current = current[key]
    if not isinstance(current, dict):
        raise ValueError(f"Missing JSON object path: {'/'.join(pointer)}")
    final_key = pointer[-1]
    if current.get(final_key) == value:
        return False
    current[final_key] = value
    return True


def _get_json_pointer(data: dict[str, Any], pointer: tuple[str, ...]) -> Any:
    current: Any = data
    for key in pointer:
        if not isinstance(current, dict) or key not in current:
            raise ValueError(f"Missing JSON object path: {'/'.join(pointer)}")
        current = current[key]
    return current


def git_status_short(repo_root: Path) -> str:
    status = subprocess.run(
        ("git", "status", "--short"),
        cwd=repo_root,
        check=False,
        text=True,
        capture_output=True,
    )
    if status.returncode != 0:
        raise RuntimeError("git status --short failed.")
    return status.stdout
