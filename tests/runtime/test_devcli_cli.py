from __future__ import annotations

import sys
import subprocess
import tempfile
import unittest
from pathlib import Path

from typer.testing import CliRunner


REPO_ROOT = Path(__file__).resolve().parents[2]
DEVCLI_SRC = REPO_ROOT / "tools" / "devcli" / "src"
if str(DEVCLI_SRC) not in sys.path:
    sys.path.insert(0, str(DEVCLI_SRC))

from auriora_dev.cli import app
from auriora_dev.commands.check import build_check_plan
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
    install_command,
    tarball_name,
)
from auriora_dev.commands.release_notes import collect_release_notes_evidence, render_release_notes
from auriora_dev.commands.spec import build_spec_plan
from auriora_dev.commands.sync import build_bundles_plan, build_guard_plan


class DevCliSurfaceTests(unittest.TestCase):
    def test_help_exposes_real_command_groups_without_template_commands(self) -> None:
        result = CliRunner().invoke(app, ["--help"])

        self.assertEqual(result.exit_code, 0, result.output)
        self.assertIn("package", result.output)
        self.assertIn("plugin", result.output)
        self.assertIn("release", result.output)
        self.assertIn("spec", result.output)
        self.assertIn("sync", result.output)
        self.assertNotIn("scaffold-split", result.output)
        self.assertNotIn("new-task", result.output)
        self.assertNotIn("proj", result.output)

    def test_check_dry_run_renders_default_validation_plan(self) -> None:
        result = CliRunner().invoke(
            app,
            ["check", "--repo-root", str(REPO_ROOT), "--dry-run"],
        )

        self.assertEqual(result.exit_code, 0, result.output)
        self.assertIn("python unit tests", result.output)
        self.assertIn("spec_runtime scan .", result.output)
        self.assertIn("spec_runtime archive-index .", result.output)
        self.assertIn("spec_runtime prompts", result.output)
        self.assertIn("spec_runtime package-contract .", result.output)
        self.assertIn("npm pack --dry-run --json", result.output)
        self.assertIn("git diff --check", result.output)


class DevCliPlanTests(unittest.TestCase):
    def test_check_plan_can_skip_package_stages(self) -> None:
        commands = build_check_plan(REPO_ROOT, include_package=False)
        argv = [command.argv for command in commands]

        self.assertNotIn(
            ("python3", "skills/spec-lifecycle-manager/scripts/spec_runtime.py", "package-contract", "."),
            argv,
        )
        self.assertNotIn(("npm", "pack", "--dry-run", "--json"), argv)
        self.assertEqual(argv[-1], ("git", "diff", "--check"))

    def test_sync_plans_wrap_bundle_copy_and_guard(self) -> None:
        bundle_commands = build_bundles_plan(REPO_ROOT)
        guard_commands = build_guard_plan(REPO_ROOT)

        self.assertEqual(len(bundle_commands), 3)
        self.assertTrue(bundle_commands[0].mutates)
        self.assertEqual(bundle_commands[0].argv[:2], ("cp", "-a"))
        self.assertEqual(bundle_commands[-1].argv[-2:], ("package-contract", "."))
        self.assertEqual(guard_commands[0].argv[-2:], ("sync-guard", "."))

    def test_package_plans_wrap_contract_pack_guard_and_installer(self) -> None:
        check_commands = build_package_check_plan(REPO_ROOT)
        pack_commands = build_package_pack_plan(REPO_ROOT)
        install_commands = build_install_local_plan(
            REPO_ROOT,
            source=".",
            codex_home="/tmp/codex-home",
            marketplace_root="/tmp/marketplace",
            repo_root_option=".",
            skip_marketplace=True,
            skip_plugin_add=True,
            dry_run=True,
        )

        self.assertEqual(check_commands[0].argv[-2:], ("package-contract", "."))
        self.assertEqual(check_commands[1].argv, ("npm", "pack", "--dry-run", "--json"))
        self.assertEqual(check_commands[2].argv[-2:], ("sync-guard", "."))
        self.assertEqual(pack_commands[0].argv, ("npm", "pack", "--dry-run", "--json"))
        self.assertFalse(pack_commands[0].mutates)
        self.assertIn("--dry-run", install_commands[0].argv)
        self.assertIn("--skip-marketplace", install_commands[0].argv)
        self.assertIn("--skip-plugin-add", install_commands[0].argv)
        self.assertFalse(install_commands[0].mutates)

    def test_plugin_and_spec_plans_use_authoritative_commands(self) -> None:
        self.assertEqual(
            build_plugin_status_plan(REPO_ROOT)[0].argv,
            ("codex", "plugin", "list"),
        )
        self.assertEqual(build_spec_plan(REPO_ROOT, "scan")[0].argv[-2:], ("scan", "."))
        self.assertEqual(
            build_spec_plan(REPO_ROOT, "archive-index")[0].argv[-2:],
            ("archive-index", "."),
        )
        self.assertEqual(build_spec_plan(REPO_ROOT, "prompts")[0].argv[-1:], ("prompts",))
        self.assertEqual(
            build_spec_plan(REPO_ROOT, "lint", "docs/specs/025-dev-cli-workflow-tools")[0].argv[-2:],
            ("lint", "docs/specs/025-dev-cli-workflow-tools"),
        )

    def test_release_preflight_has_no_external_release_mutation(self) -> None:
        commands = build_release_preflight_plan(REPO_ROOT, allow_dirty=True)
        flattened = " ".join(" ".join(command.argv) for command in commands)

        self.assertIn("git status --short", flattened)
        self.assertIn("package-contract", flattened)
        self.assertIn("npm pack --dry-run --json", flattened)
        self.assertIn("scan .", flattened)
        self.assertNotIn("npm publish", flattened)
        self.assertNotIn("git push", flattened)
        self.assertNotIn("gh release", flattened)
        self.assertTrue(all(not command.mutates for command in commands))

    def test_release_tag_and_github_plans_are_explicitly_mutating(self) -> None:
        tag_commands = build_release_tag_plan(
            REPO_ROOT,
            version="0.2.1",
            remote="origin",
            push=True,
            force=False,
        )
        github_commands = build_github_release_plan(
            REPO_ROOT,
            version="0.2.1",
            notes_file=Path("docs/release-notes/v0.2.1.md"),
            title=None,
            draft=True,
            prerelease=False,
            existing=False,
            create_tag=False,
            push_tag=False,
            preflight=False,
        )

        self.assertEqual(tag_commands[0].argv, ("git", "tag", "-a", "v0.2.1", "-m", "Release v0.2.1"))
        self.assertEqual(tag_commands[1].argv, ("git", "push", "origin", "v0.2.1"))
        self.assertIn("gh release create v0.2.1", " ".join(" ".join(command.argv) for command in github_commands))
        self.assertIn("--notes-file docs/release-notes/v0.2.1.md", " ".join(" ".join(command.argv) for command in github_commands))
        self.assertTrue(all(command.mutates for command in tag_commands))
        self.assertTrue(all(command.mutates for command in github_commands))

    def test_release_artifact_names_match_repo_package(self) -> None:
        self.assertEqual(tarball_name("v0.2.1"), "auriora-ai-spec-lifecycle-0.2.1.tgz")
        self.assertEqual(
            install_command("0.2.1"),
            "npm install -g https://github.com/Auriora/ai-spec-lifecycle/releases/download/v0.2.1/auriora-ai-spec-lifecycle-0.2.1.tgz",
        )

    def test_release_notes_collects_git_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._git(root, "init")
            self._git(root, "config", "user.email", "release@example.com")
            self._git(root, "config", "user.name", "Release Tester")
            (root / "README.md").write_text("initial\n", encoding="utf-8")
            self._git(root, "add", "README.md")
            self._git(root, "commit", "-m", "Initial release")
            self._git(root, "tag", "v0.1.0")
            (root / "skills").mkdir()
            (root / "skills" / "feature.md").write_text("feature\n", encoding="utf-8")
            self._git(root, "add", "skills/feature.md")
            self._git(root, "commit", "-m", "Add skill feature")

            evidence = collect_release_notes_evidence(
                root,
                from_ref="v0.1.0",
                to_ref="HEAD",
                version="0.2.0",
                validation_note="unit validation passed",
                validation_file=None,
            )
            markdown = render_release_notes(
                evidence,
                release_format="draft",
                include_evidence=True,
                final=False,
            )

        self.assertEqual(evidence.version, "0.2.0")
        self.assertEqual(len(evidence.commits), 1)
        self.assertIn("skills/feature.md", evidence.areas["skill_runtime"])
        self.assertIn("Spec Lifecycle Manager v0.2.0", markdown)
        self.assertIn("unit validation passed", markdown)

    def _git(self, root: Path, *args: str) -> None:
        subprocess.run(("git", *args), cwd=root, text=True, capture_output=True, check=True)


if __name__ == "__main__":
    unittest.main()
