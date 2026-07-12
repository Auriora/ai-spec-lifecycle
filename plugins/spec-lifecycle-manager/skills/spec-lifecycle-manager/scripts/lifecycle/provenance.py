"""Deterministic, privacy-safe provenance primitives for lifecycle adapters."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any, Iterable, Mapping


UNKNOWN = "unknown"
SCHEMA_VERSION = "1"
PACKAGE_NAMES = {"@auriora/ai-spec-lifecycle", "spec-lifecycle-manager"}
INVOCATION_SURFACES = frozenset({"mcp", "cli", "hook", "prompt", UNKNOWN})
ROOT_SOURCES = frozenset({"argument", "environment", "cwd", UNKNOWN})
FALLBACK_REASONS = frozenset(
    {
        "ci",
        "package_validation",
        "hook_execution",
        "mcp_debugging",
        "mcp_unavailable",
        "explicit_recovery",
        "other",
        "none",
    }
)


def canonical_json(value: Any) -> str:
    """Return sorted, compact UTF-8-safe JSON suitable for hashing."""

    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def evidence_fingerprint(
    decision_inputs: Any,
    *,
    domain: str = "spec-lifecycle-evidence-v1",
) -> str:
    """Fingerprint caller-selected decision inputs with domain separation."""

    if not isinstance(domain, str) or not domain:
        raise ValueError("fingerprint domain must be a non-empty string")
    payload = domain.encode("utf-8") + b"\0" + canonical_json(decision_inputs).encode("utf-8")
    return f"sha256:{hashlib.sha256(payload).hexdigest()}"


def _read_object(path: Path) -> Mapping[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def _identity_from_manifest(manifest: Mapping[str, Any]) -> dict[str, str] | None:
    if manifest.get("name") not in PACKAGE_NAMES:
        return None
    version = manifest.get("version")
    return {
        "package_version": version if isinstance(version, str) and version else UNKNOWN,
        "build_identity": UNKNOWN,
    }


def resolve_runtime_identity(start_path: Path | str | None = None) -> dict[str, str]:
    """Resolve identity from the runtime's owning package, never the target repo."""

    start = Path(start_path) if start_path is not None else Path(__file__)
    current = start.resolve()
    if current.is_file():
        current = current.parent

    for owner in (current, *current.parents):
        build_info = _read_object(owner / "build-info.json")
        if build_info is not None:
            name = build_info.get("name", "spec-lifecycle-manager")
            if name in PACKAGE_NAMES:
                version = build_info.get("package_version", build_info.get("version"))
                build = build_info.get("build_identity", build_info.get("build"))
                return {
                    "package_version": version if isinstance(version, str) and version else UNKNOWN,
                    "build_identity": build if isinstance(build, str) and build else UNKNOWN,
                }

        for relative in (
            Path(".codex-plugin/plugin.json"),
            Path(".claude-plugin/plugin.json"),
        ):
            manifest = _read_object(owner / relative)
            if manifest is not None:
                identity = _identity_from_manifest(manifest)
                if identity is not None:
                    return identity

        package = _read_object(owner / "package.json")
        if package is not None:
            identity = _identity_from_manifest(package)
            if identity is not None:
                return identity

    return {"package_version": UNKNOWN, "build_identity": UNKNOWN}


def repository_identity(repo_root: Path | str) -> str:
    """Return a path-free identity derived from the repository's root commit."""

    try:
        result = subprocess.run(
            ["git", "rev-list", "--max-parents=0", "HEAD"],
            cwd=Path(repo_root),
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return UNKNOWN
    roots = sorted(line.strip() for line in result.stdout.splitlines() if line.strip())
    if not roots:
        return UNKNOWN
    payload = b"spec-lifecycle-repo-v1\0" + "\n".join(roots).encode("ascii")
    return f"sha256:{hashlib.sha256(payload).hexdigest()}"


def _closed_enum(value: str, allowed: frozenset[str], field: str) -> str:
    if value not in allowed:
        choices = ", ".join(sorted(allowed))
        raise ValueError(f"{field} must be one of: {choices}")
    return value


def _composition_sources(values: Iterable[str]) -> list[str]:
    normalized = {value.strip() for value in values if isinstance(value, str) and value.strip()}
    return sorted(normalized)[:20]


def assemble_lifecycle_metadata(
    repo_root: Path | str,
    *,
    invocation_surface: str = UNKNOWN,
    root_source: str = UNKNOWN,
    fallback_reason: str = "none",
    composition_sources: Iterable[str] = (),
    runtime_start_path: Path | str | None = None,
) -> dict[str, Any]:
    """Assemble the v1 metadata object for an adapter response boundary."""

    identity = resolve_runtime_identity(runtime_start_path)
    return {
        "schema_version": SCHEMA_VERSION,
        **identity,
        "invocation_surface": _closed_enum(
            invocation_surface, INVOCATION_SURFACES, "invocation_surface"
        ),
        "composition_sources": _composition_sources(composition_sources),
        "repo_root": ".",
        "repo_identity": repository_identity(repo_root),
        "root_source": _closed_enum(root_source, ROOT_SOURCES, "root_source"),
        "fallback_reason": _closed_enum(
            fallback_reason, FALLBACK_REASONS, "fallback_reason"
        ),
    }
