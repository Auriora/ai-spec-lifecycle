import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PLUGIN = ROOT / "plugins" / "spec-lifecycle-manager"
SOURCE_SKILL = ROOT / "skills" / "spec-lifecycle-manager"
BUNDLED_SKILL = PLUGIN / "skills" / "spec-lifecycle-manager"


class SpecPluginPackageTests(unittest.TestCase):
    def test_plugin_bundles_runtime_components(self):
        self.assertTrue((PLUGIN / ".codex-plugin" / "plugin.json").is_file())
        self.assertTrue((PLUGIN / ".mcp.json").is_file())
        self.assertTrue((PLUGIN / "hooks" / "hooks.json").is_file())
        self.assertTrue((PLUGIN / "skills" / "spec-lifecycle-manager" / "SKILL.md").is_file())
        self.assertTrue((PLUGIN / "skills" / "spec-lifecycle-manager" / "scripts" / "spec_mcp_server.py").is_file())
        self.assertTrue((PLUGIN / "skills" / "spec-lifecycle-manager" / "scripts" / "spec_runtime.py").is_file())
        self.assertTrue((PLUGIN / "skills" / "spec-lifecycle-manager" / "prompts").is_dir())
        self.assertTrue((PLUGIN / "skills" / "spec-lifecycle-manager" / "references").is_dir())

    def test_manifest_points_to_plugin_root_components(self):
        manifest = json.loads((PLUGIN / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual("./skills/", manifest["skills"])
        self.assertEqual("./.mcp.json", manifest["mcpServers"])
        self.assertNotIn("hooks", manifest)

    def test_mcp_and_hooks_use_bundled_runtime(self):
        mcp = json.loads((PLUGIN / ".mcp.json").read_text(encoding="utf-8"))
        server = mcp["mcpServers"]["spec-lifecycle-manager"]
        self.assertEqual(".", server["cwd"])
        self.assertEqual("python3", server["command"])
        self.assertIn("./skills/spec-lifecycle-manager/scripts/spec_mcp_server.py", server["args"])

        hooks = json.loads((PLUGIN / "hooks" / "hooks.json").read_text(encoding="utf-8"))
        post_tool = hooks["hooks"]["PostToolUse"][0]["hooks"][0]
        self.assertIn("${PLUGIN_ROOT}/skills/spec-lifecycle-manager/scripts/codex_spec_lifecycle_hook.py", post_tool["command"])

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
        self.assertEqual(source_files, bundled_files)
        for relative in sorted(source_files):
            self.assertEqual(
                (SOURCE_SKILL / relative).read_bytes(),
                (BUNDLED_SKILL / relative).read_bytes(),
                f"Bundled skill file drifted: {relative}",
            )

    def test_skill_frontmatter_includes_agent_skills_metadata(self):
        text = (SOURCE_SKILL / "SKILL.md").read_text(encoding="utf-8")
        frontmatter = text.split("---", 2)[1]
        self.assertIn("name: spec-lifecycle-manager", frontmatter)
        self.assertIn("description:", frontmatter)
        self.assertIn("license: MIT", frontmatter)
        self.assertIn("compatibility:", frontmatter)
        self.assertIn("metadata:", frontmatter)


if __name__ == "__main__":
    unittest.main()
