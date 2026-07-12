import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = ROOT / "skills/spec-lifecycle-manager/scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from lifecycle import provenance


GIT_ENV = {
    "GIT_AUTHOR_NAME": "Test User",
    "GIT_AUTHOR_EMAIL": "test@example.com",
    "GIT_COMMITTER_NAME": "Test User",
    "GIT_COMMITTER_EMAIL": "test@example.com",
}


class LifecycleProvenanceTests(unittest.TestCase):
    def test_canonical_json_and_fingerprint_are_deterministic(self):
        left = {"beta": [2, 1], "alpha": "é"}
        right = {"alpha": "é", "beta": [2, 1]}
        self.assertEqual('{"alpha":"é","beta":[2,1]}', provenance.canonical_json(left))
        self.assertEqual(
            provenance.evidence_fingerprint(left),
            provenance.evidence_fingerprint(right),
        )
        self.assertNotEqual(
            provenance.evidence_fingerprint(left),
            provenance.evidence_fingerprint({"alpha": "é", "beta": [1, 2]}),
        )
        self.assertNotEqual(
            provenance.evidence_fingerprint(left, domain="another-domain"),
            provenance.evidence_fingerprint(left),
        )

    def test_canonical_json_rejects_non_json_numbers(self):
        with self.assertRaises(ValueError):
            provenance.canonical_json({"unsafe": float("nan")})

    def test_source_package_identity(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            script = root / "skills/spec-lifecycle-manager/scripts/lifecycle/provenance.py"
            script.parent.mkdir(parents=True)
            script.touch()
            (root / "package.json").write_text(
                json.dumps({"name": "@auriora/ai-spec-lifecycle", "version": "1.2.3"}),
                encoding="utf-8",
            )
            self.assertEqual(
                {"package_version": "1.2.3", "build_identity": "unknown"},
                provenance.resolve_runtime_identity(script),
            )

    def test_plugin_and_build_identity_precedence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            script = root / "plugin/skills/spec/scripts/lifecycle/provenance.py"
            script.parent.mkdir(parents=True)
            script.touch()
            manifest_dir = root / "plugin/.codex-plugin"
            manifest_dir.mkdir()
            (manifest_dir / "plugin.json").write_text(
                json.dumps({"name": "spec-lifecycle-manager", "version": "2.0.0"}),
                encoding="utf-8",
            )
            self.assertEqual("2.0.0", provenance.resolve_runtime_identity(script)["package_version"])
            (root / "plugin/build-info.json").write_text(
                json.dumps(
                    {
                        "name": "spec-lifecycle-manager",
                        "package_version": "2.0.1",
                        "build_identity": "commit:abc123",
                    }
                ),
                encoding="utf-8",
            )
            self.assertEqual(
                {"package_version": "2.0.1", "build_identity": "commit:abc123"},
                provenance.resolve_runtime_identity(script),
            )

    def test_missing_malformed_and_unrelated_identity_are_unknown(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            script = root / "nested/provenance.py"
            script.parent.mkdir()
            script.touch()
            (root / "package.json").write_text("not-json", encoding="utf-8")
            self.assertEqual(
                {"package_version": "unknown", "build_identity": "unknown"},
                provenance.resolve_runtime_identity(script),
            )
            (root / "package.json").write_text(
                json.dumps({"name": "some-target-project", "version": "99.0.0"}),
                encoding="utf-8",
            )
            self.assertEqual("unknown", provenance.resolve_runtime_identity(script)["package_version"])

    @unittest.skipUnless(shutil.which("git"), "git is required")
    def test_repository_identity_uses_root_commit_and_not_current_head(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            self._git(repo, "init")
            (repo / "one.txt").write_text("one", encoding="utf-8")
            self._git(repo, "add", "one.txt")
            self._git(repo, "commit", "-m", "root")
            root_commit = self._git(repo, "rev-parse", "HEAD", capture=True)
            expected = "sha256:" + hashlib.sha256(
                b"spec-lifecycle-repo-v1\0" + root_commit.encode("ascii")
            ).hexdigest()
            self.assertEqual(expected, provenance.repository_identity(repo))
            (repo / "two.txt").write_text("two", encoding="utf-8")
            self._git(repo, "add", "two.txt")
            self._git(repo, "commit", "-m", "second")
            self.assertEqual(expected, provenance.repository_identity(repo))

    def test_non_git_repository_identity_is_unknown(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual("unknown", provenance.repository_identity(tmp))

    def test_metadata_validates_enums_bounds_sources_and_privacy(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            metadata = provenance.assemble_lifecycle_metadata(
                root,
                invocation_surface="mcp",
                root_source="argument",
                fallback_reason="none",
                composition_sources=[" scan ", "scan", *[f"source-{i:02}" for i in range(25)]],
                runtime_start_path=root,
            )
            self.assertEqual(".", metadata["repo_root"])
            self.assertEqual("mcp", metadata["invocation_surface"])
            self.assertEqual(20, len(metadata["composition_sources"]))
            rendered = json.dumps(metadata)
            self.assertNotIn(str(root), rendered)
            for forbidden in ("prompt", "secret", "remote_url", "user_identity"):
                self.assertNotIn(forbidden, metadata)
            for field, value in (
                ("invocation_surface", "terminal"),
                ("root_source", "config"),
                ("fallback_reason", "network_error"),
            ):
                kwargs = {field: value, "runtime_start_path": root}
                with self.assertRaises(ValueError):
                    provenance.assemble_lifecycle_metadata(root, **kwargs)

    @staticmethod
    def _git(repo: Path, *args: str, capture: bool = False) -> str:
        result = subprocess.run(
            ["git", "-c", "commit.gpgsign=false", *args],
            cwd=repo,
            check=True,
            env={**os.environ, **GIT_ENV},
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return result.stdout.strip() if capture else ""


if __name__ == "__main__":
    unittest.main()
