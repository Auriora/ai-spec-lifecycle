from __future__ import annotations

import sys
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


if __name__ == "__main__":
    unittest.main()
