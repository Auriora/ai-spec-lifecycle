import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PLUGIN = ROOT / "plugins" / "spec-lifecycle-manager"
CLAUDE_PLUGIN = PLUGIN / "claude-plugin"
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
NPM_PACKAGE = ROOT / "package.json"
SOURCE_SKILL = ROOT / "skills" / "spec-lifecycle-manager"
BUNDLED_SKILL = PLUGIN / "skills" / "spec-lifecycle-manager"
CLAUDE_SKILL = CLAUDE_PLUGIN / "skills" / "spec-lifecycle-manager"
SCRIPT_DIR = SOURCE_SKILL / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

import spec_runtime


class SpecPluginPackageTests(unittest.TestCase):
    def test_plugin_bundles_runtime_components(self):
        self.assertTrue((PLUGIN / ".codex-plugin" / "plugin.json").is_file())
        self.assertTrue((PLUGIN / ".mcp.json").is_file())
        self.assertTrue((PLUGIN / "mcp-launch.mjs").is_file())
        self.assertTrue((PLUGIN / "hooks" / "hooks.json").is_file())
        self.assertTrue((CLAUDE_PLUGIN / ".claude-plugin" / "plugin.json").is_file())
        self.assertTrue((CLAUDE_PLUGIN / ".mcp.json").is_file())
        self.assertTrue((CLAUDE_PLUGIN / "mcp-launch.mjs").is_file())
        self.assertTrue((CLAUDE_PLUGIN / "hooks" / "hooks.json").is_file())
        self.assertTrue((PLUGIN / "skills" / "spec-lifecycle-manager" / "SKILL.md").is_file())
        self.assertTrue((PLUGIN / "skills" / "spec-lifecycle-manager" / "scripts" / "spec_mcp_server.py").is_file())
        self.assertTrue((PLUGIN / "skills" / "spec-lifecycle-manager" / "scripts" / "spec_runtime.py").is_file())
        self.assertTrue((CLAUDE_PLUGIN / "skills" / "spec-lifecycle-manager" / "SKILL.md").is_file())
        self.assertTrue((CLAUDE_PLUGIN / "skills" / "spec-lifecycle-manager" / "scripts" / "spec_mcp_server.py").is_file())
        self.assertTrue((PLUGIN / "skills" / "spec-lifecycle-manager" / "prompts").is_dir())
        self.assertTrue((PLUGIN / "skills" / "spec-lifecycle-manager" / "references").is_dir())

    def test_manifest_points_to_plugin_root_components(self):
        manifest = json.loads((PLUGIN / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual("./skills/", manifest["skills"])
        self.assertEqual("./.mcp.json", manifest["mcpServers"])
        self.assertNotIn("hooks", manifest)

    def test_mcp_and_hooks_use_bundled_runtime(self):
        # Spec 028: the shipped (marketplace) default interpreter is the
        # portable name "python"; the installer pins the host-resolved
        # interpreter (py -3 / python3 / python) at install time.
        mcp = json.loads((PLUGIN / ".mcp.json").read_text(encoding="utf-8"))
        server = mcp["mcpServers"]["spec-lifecycle-manager"]
        self.assertNotIn("cwd", server)
        self.assertEqual("node", server["command"])
        self.assertEqual(["${PLUGIN_ROOT}/mcp-launch.mjs"], server["args"])

        # Codex hook keeps exec-via-shell-string form (OQ4) with the portable
        # default interpreter and the runtime-expanded ${PLUGIN_ROOT} token.
        hooks = json.loads((PLUGIN / "hooks" / "hooks.json").read_text(encoding="utf-8"))
        post_tool = hooks["hooks"]["PostToolUse"][0]["hooks"][0]
        self.assertEqual(
            'python "${PLUGIN_ROOT}/skills/spec-lifecycle-manager/scripts/codex_spec_lifecycle_hook.py"',
            post_tool["command"],
        )

    def test_claude_plugin_manifest_mcp_and_hooks_use_bundled_runtime(self):
        manifest = json.loads((CLAUDE_PLUGIN / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual("spec-lifecycle-manager", manifest["name"])
        self.assertEqual("./skills/", manifest["skills"])
        self.assertEqual("./.mcp.json", manifest["mcpServers"])
        # An explicit "hooks" key pointing at the default hooks/hooks.json path
        # makes Claude Code load it twice and fail with "Duplicate hooks file
        # detected", which disables the whole plugin's MCP server. Claude Code
        # auto-discovers hooks/hooks.json by convention, so the key must stay out.
        self.assertNotIn("hooks", manifest)

        mcp = json.loads((CLAUDE_PLUGIN / ".mcp.json").read_text(encoding="utf-8"))
        server = mcp["mcpServers"]["spec-lifecycle-manager"]
        self.assertNotIn("cwd", server)
        self.assertEqual("node", server["command"])
        self.assertEqual(["${CLAUDE_PLUGIN_ROOT}/mcp-launch.mjs"], server["args"])

        # Claude hook uses exec form (command + args array) so it is spawned
        # without a shell on every OS (Spec 028 R3/P1).
        hooks = json.loads((CLAUDE_PLUGIN / "hooks" / "hooks.json").read_text(encoding="utf-8"))
        post_tool = hooks["hooks"]["PostToolUse"][0]["hooks"][0]
        self.assertEqual("python", post_tool["command"])
        self.assertIn(
            "${CLAUDE_PLUGIN_ROOT}/skills/spec-lifecycle-manager/scripts/codex_spec_lifecycle_hook.py",
            post_tool["args"],
        )

    def test_claude_marketplace_lists_claude_plugin_source(self):
        marketplace = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
        entries = {entry["name"]: entry for entry in marketplace["plugins"]}
        self.assertIn("spec-lifecycle-manager", entries)
        self.assertEqual(
            "./plugins/spec-lifecycle-manager/claude-plugin",
            entries["spec-lifecycle-manager"]["source"],
        )

    def test_bundled_skill_matches_source_skill(self):
        source_files = {
            path.relative_to(SOURCE_SKILL)
            for path in SOURCE_SKILL.rglob("*")
            if path.is_file() and "__pycache__" not in path.parts
        }
        bundled_files = {
            path.relative_to(BUNDLED_SKILL)
            for path in BUNDLED_SKILL.rglob("*")
            if path.is_file() and "__pycache__" not in path.parts
        }
        claude_files = {
            path.relative_to(CLAUDE_SKILL)
            for path in CLAUDE_SKILL.rglob("*")
            if path.is_file() and "__pycache__" not in path.parts
        }
        self.assertEqual(source_files, bundled_files)
        self.assertEqual(source_files, claude_files)
        for relative in sorted(source_files):
            self.assertEqual(
                (SOURCE_SKILL / relative).read_bytes(),
                (BUNDLED_SKILL / relative).read_bytes(),
                f"Bundled skill file drifted: {relative}",
            )
            self.assertEqual(
                (SOURCE_SKILL / relative).read_bytes(),
                (CLAUDE_SKILL / relative).read_bytes(),
                f"Claude plugin skill file drifted: {relative}",
            )

    def test_skill_frontmatter_includes_agent_skills_metadata(self):
        text = (SOURCE_SKILL / "SKILL.md").read_text(encoding="utf-8")
        frontmatter = text.split("---", 2)[1]
        self.assertIn("name: spec-lifecycle-manager", frontmatter)
        self.assertIn("description:", frontmatter)
        self.assertIn("license: GPL-3.0-or-later", frontmatter)
        self.assertIn("compatibility:", frontmatter)
        self.assertIn("metadata:", frontmatter)

    def test_npm_package_exposes_installer_bin_and_payload(self):
        package = json.loads(NPM_PACKAGE.read_text(encoding="utf-8"))

        self.assertEqual("@auriora/ai-spec-lifecycle", package["name"])
        self.assertEqual(
            "packaging/spec-lifecycle-manager/npm-install.js",
            package["bin"]["ai-spec-lifecycle"],
        )
        self.assertEqual(
            "packaging/spec-lifecycle-manager/npm-install.js",
            package["bin"]["spec-lifecycle-manager"],
        )
        self.assertIn("plugins/spec-lifecycle-manager", package["files"])
        self.assertIn("scripts/install-spec-lifecycle-manager-package.sh", package["files"])
        self.assertIn("packaging/spec-lifecycle-manager/npm-package.json", package["files"])

    def test_npm_pack_dry_run_contains_distribution_payload(self):
        # shutil.which honors PATHEXT, so on Windows it resolves npm.cmd; pass the
        # resolved path to subprocess because CreateProcess does not apply PATHEXT
        # to a bare "npm" argument (would raise FileNotFoundError on Windows CI).
        npm = shutil.which("npm")
        if npm is None:
            raise unittest.SkipTest("npm is required for package dry-run validation")

        cache_dir = os.path.join(tempfile.gettempdir(), "spec-lifecycle-npm-cache")
        result = subprocess.run(
            [npm, "pack", "--dry-run", "--json"],
            cwd=ROOT,
            check=True,
            env={**os.environ, "npm_config_cache": cache_dir},
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        payload = json.loads(result.stdout)[0]
        files = {item["path"] for item in payload["files"]}

        self.assertIn("package.json", files)
        self.assertIn("packaging/spec-lifecycle-manager/npm-install.js", files)
        self.assertIn("packaging/spec-lifecycle-manager/npm-package.json", files)
        # Spec 028: the bin entrypoint imports these at install time, so the
        # GitHub-release tarball must contain them or the install ERR_MODULE.
        self.assertIn("packaging/spec-lifecycle-manager/installer.mjs", files)
        self.assertIn("packaging/spec-lifecycle-manager/resolve-python.mjs", files)
        self.assertIn("scripts/install-spec-lifecycle-manager-package.sh", files)
        self.assertIn("plugins/spec-lifecycle-manager/.codex-plugin/plugin.json", files)
        self.assertIn("plugins/spec-lifecycle-manager/claude-plugin/.claude-plugin/plugin.json", files)
        self.assertIn("plugins/spec-lifecycle-manager/claude-plugin/.mcp.json", files)
        self.assertIn("plugins/spec-lifecycle-manager/claude-plugin/mcp-launch.mjs", files)
        self.assertIn("plugins/spec-lifecycle-manager/claude-plugin/hooks/hooks.json", files)
        self.assertIn("plugins/spec-lifecycle-manager/claude-plugin/skills/spec-lifecycle-manager/SKILL.md", files)
        self.assertIn("plugins/spec-lifecycle-manager/mcp-launch.mjs", files)
        self.assertIn("plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/SKILL.md", files)
        self.assertFalse(any("__pycache__" in path for path in files))
        self.assertFalse(any(path.endswith((".pyc", ".pyo")) for path in files))

    def test_package_contract_reports_claude_parity(self):
        payload = spec_runtime.package_contract(ROOT)

        self.assertIn("source_claude_parity", payload)
        self.assertEqual("in_sync", payload["source_claude_parity"]["status"])


if __name__ == "__main__":
    unittest.main()
