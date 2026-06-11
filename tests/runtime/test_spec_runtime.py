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
SCRIPT = SCRIPT_DIR / "spec_runtime.py"
sys.path.insert(0, str(SCRIPT_DIR))

import spec_runtime


GIT_ENV = {
    "GIT_AUTHOR_NAME": "Test User",
    "GIT_AUTHOR_EMAIL": "test@example.com",
    "GIT_COMMITTER_NAME": "Test User",
    "GIT_COMMITTER_EMAIL": "test@example.com",
}


def run_git(repo: Path, *args: str) -> None:
    if shutil.which("git") is None:
        raise unittest.SkipTest("git is required for sync guard tests")
    subprocess.run(
        ["git", "-c", "commit.gpgsign=false", *args],
        cwd=repo,
        check=True,
        env={**os.environ, **GIT_ENV},
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def write_sync_guard_repo(repo: Path, codex_home: Path, include_cache: bool = True) -> None:
    source = repo / "skills/spec-lifecycle-manager"
    bundled = repo / "plugins/spec-lifecycle-manager"
    bundled_skill = bundled / "skills/spec-lifecycle-manager"
    claude_skill = bundled / "claude-plugin/skills/spec-lifecycle-manager"
    source.mkdir(parents=True)
    bundled_skill.mkdir(parents=True)
    claude_skill.mkdir(parents=True)
    (bundled / ".codex-plugin").mkdir(parents=True)
    (repo / "scripts").mkdir()
    (repo / "packaging/spec-lifecycle-manager").mkdir(parents=True)
    (source / "SKILL.md").write_text("name: spec-lifecycle-manager\n", encoding="utf-8")
    (source / "scripts").mkdir()
    (source / "scripts/spec_runtime.py").write_text("print('runtime')\n", encoding="utf-8")
    shutil.copytree(source, bundled_skill, dirs_exist_ok=True)
    shutil.copytree(source, claude_skill, dirs_exist_ok=True)
    (bundled / ".codex-plugin/plugin.json").write_text(
        '{"name": "spec-lifecycle-manager", "version": "0.1.0+test"}\n',
        encoding="utf-8",
    )
    (repo / "scripts/install-spec-lifecycle-manager-package.sh").write_text("#!/usr/bin/env bash\n", encoding="utf-8")
    (repo / "package.json").write_text(
        json.dumps(
            {
                "name": "@auriora/ai-spec-lifecycle",
                "version": "0.1.0-test",
                "bin": {
                    "ai-spec-lifecycle": "packaging/spec-lifecycle-manager/npm-install.js",
                    "spec-lifecycle-manager": "packaging/spec-lifecycle-manager/npm-install.js",
                },
                "files": [
                    "packaging/spec-lifecycle-manager/npm-package.json",
                    "packaging/spec-lifecycle-manager/npm-install.js",
                    "plugins/spec-lifecycle-manager",
                    "scripts/install-spec-lifecycle-manager-package.sh",
                ],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (repo / "packaging/spec-lifecycle-manager/package-manifest.json").write_text(
        '{"name": "spec-lifecycle-manager", "version": "0.1.0+test"}\n',
        encoding="utf-8",
    )
    (repo / "packaging/spec-lifecycle-manager/npm-install.js").write_text("#!/usr/bin/env node\n", encoding="utf-8")
    (repo / "packaging/spec-lifecycle-manager/npm-package.json").write_text(
        json.dumps(
            {
                "package_name": "@auriora/ai-spec-lifecycle",
                "registry": "npm",
                "publish_status": "pack-ready-not-published",
                "version_source": "package.json#/version",
                "install_command": "npx @auriora/ai-spec-lifecycle install",
                "payload_root": "plugins/spec-lifecycle-manager",
                "bin": "packaging/spec-lifecycle-manager/npm-install.js",
                "required_paths": [
                    "package.json",
                    "packaging/spec-lifecycle-manager/npm-package.json",
                    "packaging/spec-lifecycle-manager/npm-install.js",
                    "plugins/spec-lifecycle-manager/.codex-plugin/plugin.json",
                    "plugins/spec-lifecycle-manager/.mcp.json",
                    "plugins/spec-lifecycle-manager/hooks/hooks.json",
                    "plugins/spec-lifecycle-manager/claude-plugin/skills/spec-lifecycle-manager/SKILL.md",
                    "plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/SKILL.md",
                    "scripts/install-spec-lifecycle-manager-package.sh",
                ],
                "provenance": {
                    "source_repository": "https://example.invalid/repo",
                    "source_path": "plugins/spec-lifecycle-manager",
                },
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (bundled / ".mcp.json").write_text('{"mcpServers": {}}\n', encoding="utf-8")
    (bundled / "hooks").mkdir()
    (bundled / "hooks/hooks.json").write_text('{"hooks": {}}\n', encoding="utf-8")
    if include_cache:
        cache = codex_home / "plugins/cache/auriora-local/spec-lifecycle-manager/0.1.0+test"
        shutil.copytree(bundled, cache, dirs_exist_ok=True)


def commit_all(repo: Path, message: str) -> None:
    run_git(repo, "add", ".")
    run_git(repo, "commit", "-m", message)


def write_archived_old_format_spec(repo: Path) -> Path:
    spec = repo / "docs/specs/001-old-format"
    spec.mkdir(parents=True)
    frontmatter = "\n".join(
        [
            "---",
            "title: Old format",
            "doc_type: spec",
            "status: archived",
            "owner: platform",
            "last_reviewed: 2026-06-06",
            "---",
            "",
        ]
    )
    (spec / "spec.md").write_text(frontmatter + "# Spec\n", encoding="utf-8")
    (spec / "plan.md").write_text(frontmatter + "# Plan\n", encoding="utf-8")
    (spec / "tasks.md").write_text(frontmatter + "# Tasks\n\n- [ ] T001 Do work.\n", encoding="utf-8")
    return spec


def write_complete_spec(repo: Path, status: str = "draft") -> Path:
    (repo / ".git").mkdir(exist_ok=True)
    spec = repo / "docs/specs/001-current"
    durable = repo / "docs/reference"
    spec.mkdir(parents=True)
    durable.mkdir(parents=True)
    (durable / "current.md").write_text("# Current Behavior\n", encoding="utf-8")
    frontmatter = "\n".join(
        [
            "---",
            "title: Current format",
            "doc_type: spec",
            "artifact_type: {artifact}",
            f"status: {status}",
            "owner: platform",
            "last_reviewed: 2026-06-06",
            "---",
            "",
        ]
    )
    (spec / "requirements.md").write_text(
        frontmatter.format(artifact="requirements")
        + "\n".join(
            [
                "# Requirements",
                "",
                "## Problem Context",
                "",
                "## Durable Source Baseline",
                "",
                "- `docs/reference/current.md`",
                "",
                "## Goals",
                "",
                "## Non-Goals",
                "",
                "## Requirements",
                "",
                "### Requirement 1: Current Behavior",
                "",
                "**User Story:** As an agent, I want durable context, so that implementation is grounded.",
                "",
                "#### Acceptance Criteria",
                "",
                "1. GIVEN a task, WHEN context is requested, THEN THE SYSTEM SHALL return durable targets.",
                "",
                "## Correctness Properties",
                "",
                "- CP-001: Durable target references resolve.",
                "",
                "## Success Criteria",
                "",
                "- Context lookup succeeds.",
            ]
        ),
        encoding="utf-8",
    )
    (spec / "design.md").write_text(
        frontmatter.format(artifact="design")
        + "\n".join(
            [
                "# Design",
                "",
                "## Overview",
                "",
                "Provide task context from durable docs.",
                "",
                "## High-Level Design",
                "",
                "### Current Context",
                "",
                "Use durable docs as the source of truth.",
                "",
                "## Low-Level Design",
                "",
                "### Task Context",
                "",
                "Return requirement, design, verification, and durable target links.",
                "",
                "## Operational Considerations",
                "",
                "## Open Questions",
            ]
        ),
        encoding="utf-8",
    )
    (spec / "tasks.md").write_text(
        frontmatter.format(artifact="tasks")
        + "# Tasks\n\n- [x] T001 Do work.\n  - Depends on: none\n  - Files: `docs/reference/current.md`\n  - Acceptance: Done.\n  - Evidence: Done.\n",
        encoding="utf-8",
    )
    (spec / "traceability.md").write_text(
        frontmatter.format(artifact="traceability")
        + "\n".join(
            [
                "# Traceability",
                "",
                "## Task To Context Matrix",
                "",
                "| Task ID | Requirements | Acceptance Criteria | Design Sections | Change Impact | Verification | Durable Targets | Open Decisions |",
                "|---------|--------------|---------------------|-----------------|---------------|--------------|-----------------|----------------|",
                "| T001 | Requirement 1 | AC1 | `design.md#task-context` | none | `verification.md#quality-gates` | `docs/reference/current.md` | none |",
                "",
                "## Requirement To Delivery Matrix",
                "",
                "| Requirement | Acceptance Criteria | Design Sections | Tasks | Verification | Durable Targets |",
                "|-------------|---------------------|-----------------|-------|--------------|-----------------|",
                "| Requirement 1 | AC1 | `design.md#task-context` | T001 | `verification.md#quality-gates` | `docs/reference/current.md` |",
                "",
                "## Design To Implementation Matrix",
                "",
                "| Design Section | Requirements | Tasks | Implementation Targets | Verification |",
                "|----------------|--------------|-------|------------------------|--------------|",
                "| `design.md#task-context` | Requirement 1 | T001 | `docs/reference/current.md` | `verification.md#quality-gates` |",
                "",
                "## Open Decision Impact",
                "",
                "| Decision | Area | Requirement | Task | Status |",
                "|----------|------|-------------|------|--------|",
                "| none | none | Requirement 1 | T001 | none |",
            ]
        ),
        encoding="utf-8",
    )
    (spec / "verification.md").write_text(
        frontmatter.format(artifact="verification")
        + "\n".join(
            [
                "# Verification",
                "",
                "## Quality Gates",
                "",
                "| Gate | Required | Status | Evidence |",
                "|------|----------|--------|----------|",
                "| Durable docs updated | yes | pass | `docs/reference/current.md` |",
                "",
                "## Evidence Log",
                "",
                "| Date | Check | Result | Notes |",
                "|------|-------|--------|-------|",
                "| 2026-06-06 | Fixture check | pass | T001 Requirement 1 |",
                "",
                "## Residual Risks",
                "",
                "None.",
            ]
        ),
        encoding="utf-8",
    )
    return spec


class SpecRuntimeTests(unittest.TestCase):
    def test_package_contract_validates_required_shape(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            codex_home = Path(tmp) / "codex"
            repo.mkdir()
            write_sync_guard_repo(repo, codex_home)
            run_git(repo, "init")
            commit_all(repo, "initial package")

            payload = spec_runtime.package_contract(repo)

        self.assertEqual("pass", payload["status"])
        self.assertEqual("@auriora/ai-spec-lifecycle", payload["package"]["name"])
        self.assertEqual("npm", payload["package"]["primary"])
        self.assertEqual("pack-ready-not-published", payload["package"]["npm"]["publish_status"])
        self.assertEqual("in_sync", payload["source_bundle_parity"]["status"])
        self.assertEqual("in_sync", payload["source_claude_parity"]["status"])
        self.assertTrue(all(item["exists"] for item in payload["required_paths"]))
        self.assertEqual(0, payload["summary"]["error"])

    def test_package_contract_reports_missing_required_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            codex_home = Path(tmp) / "codex"
            repo.mkdir()
            write_sync_guard_repo(repo, codex_home)
            (repo / "plugins/spec-lifecycle-manager/.mcp.json").unlink()

            payload = spec_runtime.package_contract(repo)

        self.assertEqual("findings", payload["status"])
        self.assertGreater(payload["summary"]["error"], 0)
        self.assertTrue(any(item["code"] == "PACKAGE_REQUIRED_PATH_MISSING" for item in payload["diagnostics"]))

    def test_sync_guard_reports_clean_source_bundle_and_cache_parity(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            codex_home = Path(tmp) / "codex"
            repo.mkdir()
            write_sync_guard_repo(repo, codex_home)
            run_git(repo, "init")
            commit_all(repo, "initial package")

            payload = spec_runtime.sync_guard(repo, codex_home, commit_count=1)

        self.assertEqual("in_sync", payload["source_bundle_parity"]["status"])
        self.assertEqual("in_sync", payload["source_claude_parity"]["status"])
        self.assertEqual("in_sync", payload["bundle_cache_parity"]["status"])
        self.assertEqual("ok", payload["commit_evidence"]["status"])
        self.assertEqual(0, payload["summary"]["error"])

    def test_sync_guard_is_not_applicable_outside_package_repo(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "target-repo"
            codex_home = Path(tmp) / "codex"
            repo.mkdir()
            (repo / ".git").mkdir()
            (repo / "docs").mkdir()

            payload = spec_runtime.sync_guard(repo, codex_home, commit_count=1)

        self.assertEqual("not_applicable", payload["status"])
        self.assertEqual("not_applicable", payload["applicability"]["status"])
        self.assertEqual([], payload["findings"])
        self.assertIn("plugins/spec-lifecycle-manager/.codex-plugin/plugin.json", payload["applicability"]["missing_paths"])

    def test_sync_guard_reports_source_bundle_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            codex_home = Path(tmp) / "codex"
            repo.mkdir()
            write_sync_guard_repo(repo, codex_home)
            run_git(repo, "init")
            commit_all(repo, "initial package")
            (repo / "skills/spec-lifecycle-manager/SKILL.md").write_text("name: changed\n", encoding="utf-8")

            payload = spec_runtime.sync_guard(repo, codex_home, commit_count=1)

        self.assertEqual("drift", payload["source_bundle_parity"]["status"])
        self.assertEqual("drift", payload["source_claude_parity"]["status"])
        self.assertIn("SKILL.md", payload["source_bundle_parity"]["content_differences"])
        self.assertTrue(any(item["code"] == "SOURCE_BUNDLE_DRIFT" for item in payload["findings"]))
        self.assertTrue(any(item["code"] == "SOURCE_CLAUDE_DRIFT" for item in payload["findings"]))

    def test_sync_guard_reports_missing_installed_cache(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            codex_home = Path(tmp) / "codex"
            repo.mkdir()
            write_sync_guard_repo(repo, codex_home, include_cache=False)
            run_git(repo, "init")
            commit_all(repo, "initial package")

            payload = spec_runtime.sync_guard(repo, codex_home, commit_count=1)

        self.assertEqual("missing", payload["bundle_cache_parity"]["status"])
        self.assertEqual(0, payload["bundle_cache_parity"]["candidate_count"])
        self.assertTrue(any(item["code"] == "BUNDLE_CACHE_DRIFT" for item in payload["findings"]))

    def test_sync_guard_reports_skill_commit_without_sync_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            codex_home = Path(tmp) / "codex"
            repo.mkdir()
            write_sync_guard_repo(repo, codex_home)
            run_git(repo, "init")
            commit_all(repo, "initial package")
            (repo / "skills/spec-lifecycle-manager/SKILL.md").write_text("name: changed\n", encoding="utf-8")
            commit_all(repo, "change source skill only")

            payload = spec_runtime.sync_guard(repo, codex_home, commit_count=1)

        self.assertEqual("missing_evidence", payload["commit_evidence"]["status"])
        self.assertEqual(1, payload["commit_evidence"]["source_skill_commit_count"])
        self.assertFalse(payload["commit_evidence"]["commits"][0]["touched_sync_evidence"])

    def test_resolve_spec_reference_classifies_active_archived_missing_and_ambiguous(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_complete_spec(repo)
            nested = repo / "docs/platform/specs/001-current"
            shutil.copytree(repo / "docs/specs/001-current", nested)
            history = repo / "docs/history"
            history.mkdir(parents=True)
            (history / "spec-closure-log.md").write_text("# Spec Closure Log\n", encoding="utf-8")
            (history / "spec-archive-index.md").write_text(
                "\n".join(
                    [
                        "# Spec Archive Index",
                        "",
                        "## Entries",
                        "",
                        "| Spec ID | Title | Package path | Status | Final spec commit | Cleanup commit | Closure action | Durable destinations | Verification |",
                        "|---------|-------|--------------|--------|-------------------|----------------|----------------|----------------------|--------------|",
                        "| 002-closed | Closed | `docs/specs/002-closed/` | removed | abc1234 | def5678 | removed-after-index | `docs/reference/current.md` | `docs/history/spec-closure-log.md` |",
                    ]
                ),
                encoding="utf-8",
            )

            active = spec_runtime.resolve_spec_reference(repo, "docs/specs/001-current")
            ambiguous = spec_runtime.resolve_spec_reference(repo, "001-current")
            archived = spec_runtime.resolve_spec_reference(repo, "002")
            missing = spec_runtime.resolve_spec_reference(repo, "999-missing")

        self.assertEqual("active", active["status"])
        self.assertEqual("001-current", active["spec_id"])
        self.assertEqual("ambiguous", ambiguous["status"])
        self.assertEqual(2, len(ambiguous["matches"]))
        self.assertEqual("archived", archived["status"])
        self.assertEqual("002-closed", archived["archive_matches"][0]["spec_id"])
        self.assertEqual("missing", missing["status"])
        self.assertIn("active_candidates", missing)

    def test_mcp_audit_summarizes_session_errors_and_mentions(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            sessions = Path(tmp) / "sessions/2026/06/11"
            repo.mkdir()
            sessions.mkdir(parents=True)
            (sessions / "rollout.jsonl").write_text(
                "\n".join(
                    [
                        json.dumps({"payload": {"role": "user", "content": "spec-lifecycle-manager.review_packet({})"}}),
                        json.dumps({"payload": {"role": "assistant", "content": "Unknown review packet type: implementation-readiness"}}),
                        json.dumps({"payload": {"role": "assistant", "content": "read specs://active"}}),
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            payload = spec_runtime.mcp_audit(repo, sessions.parent.parent.parent)

        self.assertEqual("ok", payload["status"])
        self.assertEqual(1, payload["matched_files"])
        self.assertEqual(1, payload["error_counts"]["unknown_review_packet_type"])
        self.assertGreaterEqual(payload["mention_counts"]["tool_call"], 1)
        self.assertGreaterEqual(payload["mention_counts"]["resource"], 1)

    def test_scan_discovers_current_and_old_format_specs(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_archived_old_format_spec(repo)
            payload = spec_runtime.scan_specs(repo)

        specs = {item["spec_id"]: item for item in payload["specs"]}
        archived = specs["001-old-format"]

        self.assertEqual("old-format", archived["format"])
        self.assertEqual("archived", archived["lifecycle"])
        self.assertEqual("archived", archived["health"]["severity"])
        self.assertTrue(archived["health"]["skipped"])
        self.assertEqual(1, payload["summary"]["archived"])

    def test_scan_can_opt_into_archived_lint_audit(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_archived_old_format_spec(repo)
            payload = spec_runtime.scan_specs(repo, include_archived_lint=True)

        specs = {item["spec_id"]: item for item in payload["specs"]}
        archived = specs["001-old-format"]

        self.assertEqual("archived", archived["lifecycle"])
        self.assertEqual("error", archived["health"]["severity"])
        self.assertFalse(archived["health"]["skipped"])
        self.assertGreater(archived["health"]["diagnostic_count"], 0)

    def test_archive_index_validates_current_index(self):
        payload = spec_runtime.archive_index(ROOT)

        self.assertEqual(0, payload["summary"]["error"])
        self.assertEqual(0, payload["summary"]["warn"])
        self.assertEqual(16, payload["summary"]["total"])
        self.assertEqual(16, payload["summary"]["removed"])
        self.assertEqual(0, payload["summary"]["retained"])
        self.assertEqual(0, payload["summary"]["superseded"])
        self.assertEqual(0, payload["summary"]["legacy_gaps"])
        expected = {
            "001-spec-lifecycle-manager-skill",
            "013-agent-backed-lifecycle-tools",
            "002-spec-lifecycle-validation",
            "003-coding-agent-operating-model",
            "004-spec-management-mcp",
            "005-spec-closure-log-management",
            "006-backlog-roadmap-templates",
            "007-spec-lifecycle-mcp-server",
            "008-agent-workbench-spec-lifecycle-install",
            "009-archived-spec-scan-hygiene",
            "010-codex-hook-dogfood",
            "011-spec-archive-index-runtime",
            "012-operating-model-governance-adoption",
            "014-plugin-comparison-improvements",
            "015-brooks-lint-findings-tracking",
            "016-commit-sync-guard",
        }
        entries = {entry["spec_id"]: entry for entry in payload["entries"]}
        self.assertEqual(expected, set(entries))
        self.assertTrue(all(entry["status"] == "removed" for entry in entries.values()))

    def test_archive_index_reports_missing_commits_and_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            history = repo / "docs/history"
            spec = repo / "docs/specs/001-example"
            durable = repo / "docs/design"
            history.mkdir(parents=True)
            spec.mkdir(parents=True)
            durable.mkdir(parents=True)
            (durable / "example.md").write_text("# Example\n", encoding="utf-8")
            (history / "spec-closure-log.md").write_text(
                "\n".join(
                    [
                        "# Spec Closure Log",
                        "",
                        "## Entries",
                        "",
                        "### 2026-06-06 - 001-example",
                        "",
                        "- **Spec:** `docs/specs/001-example/`",
                        "- **Title:** Example",
                        "- **Final spec commit:** `abc1234`",
                        "- **Closure cleanup commit:** `def5678`",
                        "- **Closure action:** retained-as-history",
                        "- **Durable docs updated:**",
                        "  - `docs/design/example.md`",
                    ]
                ),
                encoding="utf-8",
            )
            (history / "spec-archive-index.md").write_text(
                "\n".join(
                    [
                        "# Spec Archive Index",
                        "",
                        "## Entries",
                        "",
                        "| Spec ID | Title | Package path | Status | Final spec commit | Cleanup commit | Closure action | Durable destinations | Verification |",
                        "|---------|-------|--------------|--------|-------------------|----------------|----------------|----------------------|--------------|",
                        "| 001-example | Different title | `docs/specs/001-example/` | retained | pending | zzzzzzz | retained-as-history | `docs/design/missing.md` | `docs/history/spec-closure-log.md` |",
                    ]
                ),
                encoding="utf-8",
            )

            payload = spec_runtime.archive_index(repo)

        codes = {item["code"] for item in payload["diagnostics"]}
        self.assertIn("ARCHIVE_INDEX_FINAL_COMMIT_MISSING", codes)
        self.assertIn("ARCHIVE_INDEX_CLEANUP_COMMIT_INVALID", codes)
        self.assertIn("ARCHIVE_INDEX_DURABLE_DESTINATION_MISSING", codes)
        self.assertIn("ARCHIVE_INDEX_CLOSURE_LOG_DRIFT", codes)
        self.assertGreater(payload["summary"]["error"], 0)

    def test_summary_reports_tasks_and_resources(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            spec = write_complete_spec(repo, status="archived")
            payload = spec_runtime.spec_summary(spec)

        self.assertEqual("001-current", payload["spec_id"])
        self.assertEqual("archived", payload["lifecycle"])
        self.assertGreater(payload["tasks"]["total"], 0)
        self.assertEqual("current", payload["format"])
        self.assertEqual("present", payload["artifacts"]["requirements.md"])

    def test_agent_readiness_packet_returns_task_context(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = write_complete_spec(Path(tmp))
            payload = spec_runtime.agent_readiness_packet(spec, "T001")

        self.assertEqual("ready", payload["status"])
        self.assertTrue(payload["advisory"])
        self.assertEqual("T001", payload["task"]["task_id"])
        self.assertIn("Requirement 1", {item["id"] for item in payload["required_review"]["requirements"]})
        self.assertIn("docs/reference/current.md", payload["required_review"]["durable_targets"])
        self.assertEqual("mcp", payload["agent_interface"]["preferred"])
        self.assertIn("task_context", payload["agent_interface"]["mcp_tools"])
        self.assertTrue(any("traceability_lookup.py" in command for command in payload["validation_commands"]))
        self.assertEqual(payload["script_validation_commands"], payload["validation_commands"])

    def test_active_spec_preflight_selects_single_active_spec(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_complete_spec(repo)
            payload = spec_runtime.active_spec_preflight(repo, task_id="T001")

        self.assertEqual("ready", payload["status"])
        self.assertEqual(1, payload["scan_summary"]["active"])
        self.assertEqual("001-current", payload["selected_spec"]["spec_id"])
        self.assertEqual("T001", payload["agent_readiness_packet"]["task_id"])
        self.assertIsNotNone(payload["agent_readiness_packet"])
        self.assertEqual("mcp", payload["agent_interface"]["preferred"])
        self.assertIn("active_spec_preflight", payload["agent_interface"]["mcp_tools"])

    def test_no_active_spec_context_uses_durable_history(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / ".git").mkdir()
            (repo / "docs/history").mkdir(parents=True)
            (repo / "docs/backlog").mkdir(parents=True)
            (repo / "docs/roadmap").mkdir(parents=True)
            (repo / "docs/history/spec-archive-index.md").write_text(
                "\n".join(
                    [
                        "# Spec Archive Index",
                        "",
                        "## Entries",
                        "",
                        "| Spec ID | Title | Package path | Status | Final spec commit | Cleanup commit | Closure action | Durable destinations | Verification |",
                        "|---------|-------|--------------|--------|-------------------|----------------|----------------|----------------------|--------------|",
                    ]
                ),
                encoding="utf-8",
            )
            (repo / "docs/history/spec-closure-log.md").write_text("# Spec Closure Log\n", encoding="utf-8")
            (repo / "docs/backlog/README.md").write_text("# Backlog\n", encoding="utf-8")
            (repo / "docs/roadmap/README.md").write_text("# Roadmap\n", encoding="utf-8")
            payload = spec_runtime.no_active_spec_context(repo)

        self.assertEqual("no_active_spec", payload["status"])
        self.assertIn("docs/backlog/README.md", payload["durable_context"])
        self.assertIn("docs/history/spec-archive-index.md", payload["durable_context"])
        self.assertEqual("mcp", payload["agent_interface"]["preferred"])
        self.assertIn("no_active_spec_context", payload["agent_interface"]["mcp_tools"])
        self.assertTrue(any("scan" in command for command in payload["validation_commands"]))
        self.assertEqual(payload["script_validation_commands"], payload["validation_commands"])

    def test_active_spec_preflight_returns_no_active_context(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / ".git").mkdir()
            payload = spec_runtime.active_spec_preflight(repo)

        self.assertEqual("no_active_spec", payload["status"])
        self.assertIsNotNone(payload["no_active_spec_context"])
        self.assertEqual(0, payload["scan_summary"]["active"])

    def test_open_decisions_parser_ignores_table_header(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "open-decisions.md"
            path.write_text(
                "\n".join(
                    [
                        "| Decision | Status |",
                        "|----------|--------|",
                        "| D001 | accepted |",
                    ]
                ),
                encoding="utf-8",
            )

            decisions = spec_runtime.parse_open_decisions(path)

        self.assertEqual([{"id": "D001", "raw": "| D001 | accepted |"}], decisions)

    def test_cli_scan_can_opt_into_archived_lint_audit(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_archived_old_format_spec(repo)
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "scan", str(repo), "--include-archived-lint"],
                check=True,
                capture_output=True,
                text=True,
            )
        payload = json.loads(result.stdout)
        specs = {item["spec_id"]: item for item in payload["specs"]}

        self.assertEqual("error", specs["001-old-format"]["health"]["severity"])

    def test_cli_archive_index_outputs_json(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "archive-index", str(ROOT)],
            check=True,
            capture_output=True,
            text=True,
        )

        payload = json.loads(result.stdout)
        self.assertEqual(0, payload["summary"]["error"])
        self.assertIn("entries", payload)

    def test_lint_doc_reports_completed_task_without_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "tasks.md"
            path.write_text(
                "\n".join(
                    [
                        "---",
                        "title: Tasks",
                        "doc_type: spec",
                        "artifact_type: tasks",
                        "status: draft",
                        "owner: platform",
                        "last_reviewed: 2026-06-05",
                        "---",
                        "",
                        "# Tasks",
                        "",
                        "- [x] T001 Do thing.",
                        "  - Depends on: none",
                        "  - Files: `src/x`",
                        "  - Acceptance: Done.",
                        "  - Evidence: Pending.",
                    ]
                ),
                encoding="utf-8",
            )

            diagnostics = spec_runtime.lint_doc(path, "tasks")

        codes = {item["code"] for item in diagnostics}
        self.assertIn("TASK_EVIDENCE_MISSING", codes)

    def test_lint_doc_reports_explicit_waiver(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "requirements.md"
            path.write_text(
                "\n".join(
                    [
                        "---",
                        "title: Requirements",
                        "doc_type: spec",
                        "artifact_type: requirements",
                        "status: draft",
                        "owner: platform",
                        "last_reviewed: 2026-06-05",
                        "---",
                        "",
                        "# Requirements",
                        "",
                        "<!-- spec-lint-waive: REQUIREMENTS_PROPERTIES_MISSING - low-risk docs-only change -->",
                        "",
                        "## Durable Source Baseline",
                        "## Goals",
                        "## Non-Goals",
                        "## Requirements",
                        "### Requirement 1: Example",
                        "#### Acceptance Criteria",
                        "1. GIVEN context, WHEN action, THEN outcome.",
                        "## Success Criteria",
                    ]
                ),
                encoding="utf-8",
            )

            diagnostics = spec_runtime.lint_doc(path, "requirements")

        waived = [item for item in diagnostics if item["code"] == "REQUIREMENTS_PROPERTIES_MISSING"]
        self.assertTrue(waived)
        self.assertTrue(waived[0]["waived"])

    def test_lint_spec_package_returns_summary(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = write_complete_spec(Path(tmp))
            payload = spec_runtime.lint_spec_package(spec)

        self.assertIn("summary", payload)
        self.assertIsInstance(payload["diagnostics"], list)

    def test_next_task_selects_first_unblocked_task_with_context(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = write_complete_spec(Path(tmp))
            payload = spec_runtime.next_task(spec)

        self.assertIsNone(payload["selected"])
        self.assertEqual("No runnable incomplete task found.", payload["message"])

    def test_closure_check_reports_completed_spec_ready(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = write_complete_spec(Path(tmp))
            payload = spec_runtime.closure_check(spec)

        self.assertTrue(payload["ready"])
        self.assertEqual([], payload["blockers"])

    def test_cli_scan_outputs_json(self):
        completed = subprocess.run(
            [str(SCRIPT), "scan", str(ROOT)],
            check=True,
            capture_output=True,
            text=True,
        )

        payload = json.loads(completed.stdout)
        self.assertIn("specs", payload)

    def test_prompt_definitions_are_discoverable_and_valid(self):
        payload = spec_runtime.load_prompt_definitions(ROOT)

        names = {prompt["name"] for prompt in payload["prompts"]}
        self.assertTrue({"reconcile-spec", "choose-next-task", "task-context", "lint-spec"} <= names)
        self.assertEqual({"error": 0, "warn": 0, "info": 0}, payload["summary"])

    def test_hook_spec_file_changed_lints_affected_package(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_complete_spec(repo)
            payload = spec_runtime.run_hook(
                repo,
                "spec-file-changed",
                changed_files=["docs/specs/001-current/tasks.md"],
                severity_profile="advisory",
            )

        self.assertTrue(payload["advisory"])
        self.assertFalse(payload["blocked"])
        self.assertEqual({"error": 0, "warn": 0, "info": 0}, payload["summary"])
        self.assertEqual(1, len(payload["affected_specs"]))

    def test_hook_task_checkbox_changed_blocks_missing_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            spec = repo / "docs/specs/001-example"
            spec.mkdir(parents=True)
            (spec / "tasks.md").write_text(
                "\n".join(
                    [
                        "---",
                        "title: Tasks",
                        "doc_type: spec",
                        "artifact_type: tasks",
                        "status: draft",
                        "owner: platform",
                        "last_reviewed: 2026-06-05",
                        "---",
                        "",
                        "# Tasks",
                        "",
                        "- [x] T001 Do thing.",
                        "  - Depends on: none",
                        "  - Files: `src/x`",
                        "  - Acceptance: Done.",
                        "  - Evidence: Pending.",
                    ]
                ),
                encoding="utf-8",
            )

            payload = spec_runtime.run_hook(
                repo,
                "task-checkbox-changed",
                changed_files=["docs/specs/001-example/tasks.md"],
                severity_profile="blocking",
            )

        self.assertTrue(payload["blocked"])
        self.assertIn("TASK_EVIDENCE_MISSING", {item["code"] for item in payload["blocking"]})

    def test_hook_implementation_task_complete_blocks_missing_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            spec = repo / "docs/specs/001-example"
            spec.mkdir(parents=True)
            (spec / "tasks.md").write_text(
                "\n".join(
                    [
                        "---",
                        "title: Tasks",
                        "doc_type: spec",
                        "artifact_type: tasks",
                        "status: draft",
                        "owner: platform",
                        "last_reviewed: 2026-06-05",
                        "---",
                        "",
                        "# Tasks",
                        "",
                        "- [x] T001 Do thing.",
                        "  - Depends on: none",
                        "  - Files: `src/x`",
                        "  - Acceptance: Done.",
                        "  - Evidence: Pending.",
                    ]
                ),
                encoding="utf-8",
            )

            payload = spec_runtime.run_hook(
                repo,
                "implementation-task-complete",
                spec_path=spec,
                task_id="T001",
                severity_profile="blocking",
            )

        self.assertTrue(payload["blocked"])
        self.assertIn("TASK_EVIDENCE_MISSING", {item["code"] for item in payload["blocking"]})

    def test_hook_verification_updated_checks_requirement_and_task_refs(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            spec = repo / "docs/specs/001-example"
            spec.mkdir(parents=True)
            (spec / "verification.md").write_text(
                "\n".join(
                    [
                        "---",
                        "title: Verification",
                        "doc_type: spec",
                        "artifact_type: verification",
                        "status: draft",
                        "owner: platform",
                        "last_reviewed: 2026-06-05",
                        "---",
                        "",
                        "# Verification",
                        "",
                        "## Quality Gates",
                        "",
                        "## Evidence Log",
                        "",
                        "- T001 covers Requirement 1.",
                        "",
                        "## Residual Risks",
                    ]
                ),
                encoding="utf-8",
            )

            payload = spec_runtime.run_hook(
                repo,
                "verification-updated",
                spec_path=spec,
                severity_profile="blocking",
            )

        self.assertFalse(payload["blocked"])
        self.assertEqual({"error": 0, "warn": 0, "info": 0}, payload["summary"])

    def test_hook_spec_resumed_flags_old_format(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            spec = write_archived_old_format_spec(repo)
            payload = spec_runtime.run_hook(repo, "spec-resumed", spec_path=spec, severity_profile="advisory")

        self.assertFalse(payload["blocked"])
        self.assertIn("OLD_FORMAT_MIGRATION_DECISION_NEEDED", {item["code"] for item in payload["diagnostics"]})

    def test_hook_spec_close_check_blocks_incomplete_spec(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = self.write_incomplete_spec(Path(tmp))
            payload = spec_runtime.run_hook(Path(tmp), "spec-close-check", spec_path=spec, severity_profile="blocking")

        self.assertTrue(payload["blocked"])
        self.assertIn("TASK_NOT_VERIFIED", {item["code"] for item in payload["blocking"]})

    def test_reconcile_spec_reports_incomplete_work(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = self.write_incomplete_spec(Path(tmp))
            payload = spec_runtime.reconcile_spec(spec)

        self.assertIn("code incomplete", payload["summary"])

    def test_promotion_plan_returns_durable_targets(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = write_complete_spec(Path(tmp))
            payload = spec_runtime.promotion_plan(spec)

        targets = {item["target"] for item in payload["targets"]}
        self.assertIn("docs/reference/current.md", targets)

    def test_generate_review_packet_is_read_only_and_bounded(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = write_complete_spec(Path(tmp))
            payload = spec_runtime.generate_review_packet(spec, "design_requirements_trace", "cheap")

        self.assertEqual("read-only", payload["scope"])
        self.assertEqual("cheap", payload["model_class"])
        self.assertIn("expected_output_schema", payload)
        self.assertIn("requirements.md", payload["input_artifacts"])

    def test_generate_review_packet_maps_implementation_aliases(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = write_complete_spec(Path(tmp))
            implementation = spec_runtime.generate_review_packet(spec, "implementation", "coding")
            readiness = spec_runtime.generate_review_packet(spec, "implementation-readiness", "coding")

        for payload, requested in [(implementation, "implementation"), (readiness, "implementation-readiness")]:
            with self.subTest(requested=requested):
                self.assertEqual("implementation_review", payload["review_type"])
                self.assertEqual(requested, payload["requested_review_type"])
                self.assertEqual("implementation_review", payload["review_type_resolution"]["resolved"])
                self.assertIn(payload["review_type_resolution"]["source"], {"alias", "alias_normalized"})

    def test_generate_review_packet_maps_unknown_type_to_generic_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = write_complete_spec(Path(tmp))
            payload = spec_runtime.generate_review_packet(spec, "release-polish", "coding")

        self.assertEqual("generic_review", payload["review_type"])
        self.assertEqual("release-polish", payload["requested_review_type"])
        self.assertEqual("generic_fallback", payload["review_type_resolution"]["source"])
        self.assertIn("implementation", payload["review_type_resolution"]["aliases"])

    def test_validate_review_result_disposition(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "review-result.json"
            path.write_text(
                json.dumps(spec_runtime.review_result_disposition_template("design_requirements_trace")),
                encoding="utf-8",
            )

            payload = spec_runtime.validate_review_result(path)

        self.assertEqual({"error": 0, "warn": 0, "info": 0}, payload["summary"])

    def test_review_packet_schema_comes_from_schema_module(self):
        import spec_agent_schemas

        self.assertIs(spec_runtime.review_packet_output_schema, spec_agent_schemas.review_packet_output_schema)

    def test_agent_backed_tool_returns_unavailable_when_runner_disabled(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = write_complete_spec(Path(tmp))

            payload = spec_runtime.agent_backed_tool(spec, "closure_risk_review", model_class="cheap")

        self.assertTrue(payload["advisory"])
        self.assertEqual("closure_risk_review", payload["tool"])
        self.assertEqual("unavailable", payload["status"])
        self.assertEqual("disabled", payload["model_class"])
        self.assertEqual("runner_unconfigured", payload["result"]["gaps"][0]["code"])
        self.assertEqual({"error": 0, "warn": 0, "info": 1}, payload["summary"])
        self.assertIn("packet_id", payload["packet"])

    def test_cli_agent_backed_tool_outputs_unavailable_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = write_complete_spec(Path(tmp))
            completed = subprocess.run(
                [str(SCRIPT), "agent-backed-tool", str(spec), "--tool-name", "closure_risk_review", "--model-class", "cheap"],
                check=True,
                capture_output=True,
                text=True,
            )

        payload = json.loads(completed.stdout)
        self.assertEqual("unavailable", payload["status"])
        self.assertEqual("disabled", payload["model_class"])

    def test_agent_slice_start_uses_traceability(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            spec = write_complete_spec(repo)
            payload = spec_runtime.run_hook(
                repo,
                "agent-slice-start",
                spec_path=spec,
                task_id="T001",
                severity_profile="blocking",
            )

        self.assertFalse(payload["blocked"])
        self.assertEqual({"error": 0, "warn": 0, "info": 0}, payload["summary"])

    def test_agent_response_check_warns_without_changed_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            spec = write_complete_spec(repo)
            payload = spec_runtime.run_hook(
                repo,
                "agent-response-check",
                spec_path=spec,
                task_id="T001",
                severity_profile="advisory",
            )

        self.assertFalse(payload["blocked"])
        self.assertIn("AGENT_CHANGED_FILES_MISSING", {item["code"] for item in payload["diagnostics"]})

    def test_review_result_recorded_blocks_invalid_result(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "review-result.json"
            path.write_text("{}", encoding="utf-8")

            payload = spec_runtime.run_hook(
                ROOT,
                "review-result-recorded",
                result_path=path,
                severity_profile="blocking",
            )

        self.assertTrue(payload["blocked"])
        self.assertIn("REVIEW_RESULT_FIELD_MISSING", {item["code"] for item in payload["blocking"]})

    def test_cli_prompts_outputs_json(self):
        completed = subprocess.run(
            [str(SCRIPT), "prompts", str(ROOT)],
            check=True,
            capture_output=True,
            text=True,
        )

        payload = json.loads(completed.stdout)
        self.assertEqual(8, len(payload["prompts"]))

    def test_cli_spec_close_hook_exits_nonzero_when_blocking(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = self.write_incomplete_spec(Path(tmp))
            completed = subprocess.run(
                [
                    str(SCRIPT),
                    "hook",
                    "spec-close-check",
                    "--repo-root",
                    tmp,
                    "--spec-path",
                    str(spec),
                    "--severity-profile",
                    "blocking",
                ],
                capture_output=True,
                text=True,
            )

        self.assertEqual(1, completed.returncode)
        payload = json.loads(completed.stdout)
        self.assertTrue(payload["blocked"])

    def test_cli_review_packet_outputs_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = write_complete_spec(Path(tmp))
            completed = subprocess.run(
                [str(SCRIPT), "review-packet", str(spec), "--review-type", "design_requirements_trace"],
                check=True,
                capture_output=True,
                text=True,
            )

        payload = json.loads(completed.stdout)
        self.assertEqual("design_requirements_trace", payload["review_type"])

    def write_incomplete_spec(self, repo: Path) -> Path:
        spec = repo / "docs/specs/001-example"
        spec.mkdir(parents=True)
        frontmatter = [
            "---",
            "title: Example",
            "doc_type: spec",
            "status: draft",
            "owner: platform",
            "last_reviewed: 2026-06-05",
            "---",
            "",
        ]
        (spec / "requirements.md").write_text(
            "\n".join(
                frontmatter
                + [
                    "# Requirements",
                    "",
                    "## Durable Source Baseline",
                    "- No durable source exists yet.",
                    "",
                    "## Goals",
                    "## Non-Goals",
                    "## Requirements",
                    "### Requirement 1: Example",
                    "#### Acceptance Criteria",
                    "1. GIVEN context, WHEN action, THEN outcome.",
                    "## Correctness Properties",
                    "## Success Criteria",
                ]
            ),
            encoding="utf-8",
        )
        (spec / "design.md").write_text(
            "\n".join(
                frontmatter
                + [
                    "# Design",
                    "",
                    "## Overview",
                    "## High-Level Design",
                    "## Low-Level Design",
                    "## Operational Considerations",
                    "## Open Questions",
                ]
            ),
            encoding="utf-8",
        )
        (spec / "tasks.md").write_text(
            "\n".join(
                [
                    "---",
                    "title: Tasks",
                    "doc_type: spec",
                    "artifact_type: tasks",
                    "status: draft",
                    "owner: platform",
                    "last_reviewed: 2026-06-05",
                    "---",
                    "",
                    "# Tasks",
                    "",
                    "- [ ] T001 Do thing.",
                    "  - Depends on: none",
                    "  - Files: `src/x`",
                    "  - Acceptance: Done.",
                    "  - Evidence: Pending.",
                ]
            ),
            encoding="utf-8",
        )
        (spec / "verification.md").write_text(
            "\n".join(
                [
                    "---",
                    "title: Verification",
                    "doc_type: spec",
                    "artifact_type: verification",
                    "status: draft",
                    "owner: platform",
                    "last_reviewed: 2026-06-05",
                    "---",
                    "",
                    "# Verification",
                    "",
                    "## Quality Gates",
                    "## Evidence Log",
                    "- T001 covers Requirement 1.",
                    "## Residual Risks",
                ]
            ),
            encoding="utf-8",
        )
        (spec / "traceability.md").write_text(
            "\n".join(
                [
                    "---",
                    "title: Traceability",
                    "doc_type: spec",
                    "artifact_type: traceability",
                    "status: draft",
                    "owner: platform",
                    "last_reviewed: 2026-06-05",
                    "---",
                    "",
                    "# Traceability Matrix",
                    "",
                    "## Task To Context Matrix",
                    "## Requirement To Delivery Matrix",
                    "## Design To Implementation Matrix",
                    "## Open Decision Impact",
                ]
            ),
            encoding="utf-8",
        )
        return spec


if __name__ == "__main__":
    unittest.main()
