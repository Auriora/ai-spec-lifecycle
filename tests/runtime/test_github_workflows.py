import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class GitHubWorkflowTests(unittest.TestCase):
    def test_cross_platform_workflow_runs_full_validation_family(self):
        workflow = (ROOT / ".github/workflows/cross-platform.yml").read_text(encoding="utf-8")

        for expected in (
            "python -m unittest discover -s tests -p 'test_*.py'",
            "node --test tests/runtime/*.test.mjs",
            "spec_runtime.py scan .",
            "spec_runtime.py archive-index .",
            "spec_runtime.py prompts",
            "spec_runtime.py package-contract .",
            "spec_runtime.py sync-guard .",
            "npm pack --dry-run --json",
            "git diff --check",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, workflow)

    def test_release_workflow_builds_artifact_and_guards_publish(self):
        workflow = (ROOT / ".github/workflows/release.yml").read_text(encoding="utf-8")

        for expected in (
            "tags:",
            "workflow_dispatch:",
            "publish:",
            "npm pack --json > npm-pack.json",
            "release-summary.md",
            "actions/upload-artifact@v4",
            "secrets.NPM_TOKEN",
            "Publish skipped.",
            "refusing to overwrite",
            "npm publish --access public",
            "npm view",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, workflow)


if __name__ == "__main__":
    unittest.main()
