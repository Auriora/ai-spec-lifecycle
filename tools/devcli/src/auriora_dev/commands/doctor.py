from __future__ import annotations

import shutil
from pathlib import Path

from auriora_dev.repo import repo_relative


def collect_doctor_status(repo_root: Path) -> list[tuple[str, str]]:
    checks = [
        ("python3", shutil.which("python3")),
        ("node", shutil.which("node")),
        ("npm", shutil.which("npm")),
        ("codex", shutil.which("codex")),
    ]
    status = [(name, "available" if path else "unavailable") for name, path in checks]
    for path in (
        repo_root / "package.json",
        repo_root / "tools" / "devcli" / "pyproject.toml",
        repo_root / "skills" / "spec-lifecycle-manager" / "scripts" / "spec_runtime.py",
    ):
        state = "present" if path.exists() else "missing"
        status.append((repo_relative(path, repo_root), state))
    return status
