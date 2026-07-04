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
                "Return requirement, design, verification, durable target links, and CP-001 coverage.",
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
                "## Correctness Property Mapping",
                "",
                "| Property | Design | Covered by tasks | Verification |",
                "|----------|--------|------------------|--------------|",
                "| CP-001 | `design.md#task-context` | T001 | `verification.md#quality-gates` |",
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


def write_evidence_quality_spec(repo: Path) -> Path:
    spec = repo / "docs/specs/020-evidence-quality"
    spec.mkdir(parents=True)
    frontmatter = "\n".join(
        [
            "---",
            "title: Evidence Quality",
            "doc_type: spec",
            "artifact_type: {artifact}",
            "status: draft",
            "owner: platform",
            "last_reviewed: 2026-06-13",
            "---",
            "",
        ]
    )
    (spec / "tasks.md").write_text(
        frontmatter.format(artifact="tasks")
        + "\n".join(
            [
                "# Tasks",
                "",
                "- [x] T001 Concrete evidence.",
                "  - Files: `skills/spec-lifecycle-manager/scripts/spec_runtime.py`",
                "  - Acceptance: Done.",
                "  - Evidence: `python3 -m unittest tests/runtime/test_spec_runtime.py` passed 7 tests.",
                "- [x] T002 Vague evidence.",
                "  - Files: `skills/spec-lifecycle-manager/scripts/spec_runtime.py`",
                "  - Acceptance: Done.",
                "  - Evidence: Done.",
                "- [x] T003 Missing evidence.",
                "  - Files: `skills/spec-lifecycle-manager/scripts/spec_runtime.py`",
                "  - Acceptance: Done.",
                "  - Evidence: Pending.",
                "- [x] T004 Waived evidence.",
                "  - Files: `skills/spec-lifecycle-manager/scripts/spec_runtime.py`",
                "  - Acceptance: Done.",
                "  - Evidence: Waived by maintainer; accepted risk for manual-only review.",
                "- [x] T005 Deferred evidence.",
                "  - Files: `skills/spec-lifecycle-manager/scripts/spec_runtime.py`",
                "  - Acceptance: Done.",
                "  - Evidence: Deferred to follow-up backlog item BL-123.",
                "- [x] T006 Docs-only not applicable evidence.",
                "  - Files: `docs/reference/spec-lifecycle-runtime.md`",
                "  - Acceptance: Done.",
                "  - Evidence: Documentation-only change; no automated validation applies.",
                "- [x] T007 Unsupported not applicable evidence.",
                "  - Files: `skills/spec-lifecycle-manager/scripts/spec_runtime.py`",
                "  - Acceptance: Done.",
                "  - Evidence: Not applicable.",
                "- [x] T008 Not-run evidence.",
                "  - Files: `skills/spec-lifecycle-manager/scripts/spec_runtime.py`",
                "  - Acceptance: Done.",
                "  - Evidence: Not run; local interpreter unavailable.",
                "",
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
                "## Evidence Log",
                "",
                "| Date | Check | Result | Notes |",
                "|------|-------|--------|-------|",
                "| 2026-06-13 | Runtime tests | pass | `python3 -m unittest` passed 7 tests |",
                "- Pending.",
                "",
                "## Residual Risks",
                "",
                "None.",
            ]
        ),
        encoding="utf-8",
    )
    return spec


def write_closure_risk_ready_spec(repo: Path) -> Path:
    spec = write_complete_spec(repo)
    tasks = spec / "tasks.md"
    tasks.write_text(
        tasks.read_text(encoding="utf-8").replace("Evidence: Done.", "Evidence: `python3 -m unittest` passed 1 test."),
        encoding="utf-8",
    )
    verification = spec / "verification.md"
    verification.write_text(
        verification.read_text(encoding="utf-8")
        .replace("| 2026-06-06 | Fixture check | pass | T001 Requirement 1 |", "| 2026-06-06 | Fixture check | pass | `python3 -m unittest` passed 1 test. |")
        .replace("None.", "No residual risk accepted after `python3 -m unittest` passed 1 test."),
        encoding="utf-8",
    )
    write_archive_recovery_entry(repo, spec)
    return spec


def write_archive_recovery_entry(repo: Path, spec: Path) -> None:
    history = repo / "docs/history"
    history.mkdir(parents=True, exist_ok=True)
    (history / "spec-closure-log.md").write_text(
        "\n".join(
            [
                "# Spec Closure Log",
                "",
                "## Entries",
                "",
                "### 2026-06-13 - 001-current",
                "",
                "- **Spec:** `docs/specs/001-current/`",
                "- **Title:** Current format",
                "- **Final spec commit:** `abc1234`",
                "- **Closure cleanup commit:** `def5678`",
                "- **Closure action:** retained-as-history",
                "- **Durable docs updated:**",
                "  - `docs/reference/current.md`",
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
                f"| 001-current | Current format | `{spec.relative_to(repo).as_posix()}/` | retained | abc1234 | def5678 | retained-as-history | `docs/reference/current.md` | `docs/history/spec-closure-log.md` |",
            ]
        ),
        encoding="utf-8",
    )


class SpecRuntimeTests(unittest.TestCase):
    def test_closure_risk_review_reports_low_risk_for_ready_spec(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = write_closure_risk_ready_spec(Path(tmp))

            payload = spec_runtime.closure_risk_review(spec)

        self.assertEqual("low", payload["risk_level"])
        self.assertEqual([], payload["findings"])
        self.assertEqual([], payload["blind_spots"])
        self.assertTrue(payload["advisory"])
        self.assertFalse(payload["mutates_files"])
        self.assertTrue(payload["signals"]["closure_check"]["ready"])
        self.assertEqual(1, payload["signals"]["promotion_plan"]["target_count"])

    def test_closure_risk_review_reports_missing_promotion_and_weak_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            spec = write_closure_risk_ready_spec(repo)
            (spec / "requirements.md").write_text(
                (spec / "requirements.md")
                .read_text(encoding="utf-8")
                .replace("- `docs/reference/current.md`", ""),
                encoding="utf-8",
            )
            (spec / "traceability.md").unlink()
            (spec / "tasks.md").write_text(
                (spec / "tasks.md")
                .read_text(encoding="utf-8")
                .replace("Evidence: `python3 -m unittest` passed 1 test.", "Evidence: Done."),
                encoding="utf-8",
            )

            payload = spec_runtime.closure_risk_review(spec)

        classifications = {item["classification"] for item in payload["findings"]}
        self.assertEqual("high", payload["risk_level"])
        self.assertIn("missing_durable_promotion", classifications)
        self.assertIn("weak_or_missing_evidence", classifications)
        self.assertIn("closure_blocker", classifications)
        self.assertEqual(1, payload["signals"]["promotion_plan"]["missing_target_count"])

    def test_closure_risk_review_reports_active_doc_risk(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            spec = write_closure_risk_ready_spec(repo)
            (repo / "docs/reference/search-result.md").write_text(
                "# Search Result\n\nThis obsolete active documentation remains current guidance for 001-current.\n",
                encoding="utf-8",
            )

            payload = spec_runtime.closure_risk_review(spec)

        stale = [item for item in payload["findings"] if item["classification"] == "stale_active_documentation"]
        self.assertEqual("high", payload["risk_level"])
        self.assertEqual(1, len(stale))
        self.assertEqual("high", stale[0]["severity"])
        self.assertIn("consumer_risk", stale[0])
        self.assertEqual(1, payload["signals"]["active_documentation"]["stale_candidate_count"])

    def test_closure_risk_review_reports_archive_recovery_signal(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            spec = write_closure_risk_ready_spec(repo)
            write_archive_recovery_entry(repo, spec)

            payload = spec_runtime.closure_risk_review(spec)

        recovery = payload["signals"]["historical_recoverability"]
        self.assertEqual("indexed", recovery["recoverability"])
        self.assertEqual(1, len(recovery["matching_entries"]))
        self.assertEqual("001-current", recovery["matching_entries"][0]["spec_id"])

    def test_evidence_quality_check_classifies_task_and_verification_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = write_evidence_quality_spec(Path(tmp))

            payload = spec_runtime.evidence_quality_check(spec)

        records = {item["id"]: item for item in payload["records"]}
        self.assertEqual("concrete", records["T001"]["classification"])
        self.assertEqual("vague", records["T002"]["classification"])
        self.assertEqual("missing", records["T003"]["classification"])
        self.assertEqual("waived", records["T004"]["classification"])
        self.assertEqual("deferred", records["T005"]["classification"])
        self.assertEqual("not_applicable", records["T006"]["classification"])
        self.assertEqual("weak", records["T007"]["classification"])
        self.assertEqual("not_run", records["T008"]["classification"])
        self.assertEqual("concrete", records["verification:17"]["classification"])
        self.assertEqual("missing", records["verification:18"]["classification"])
        self.assertTrue(payload["advisory"])
        self.assertFalse(payload["mutates_files"])
        self.assertEqual(2, payload["summary"]["by_classification"]["concrete"])
        self.assertEqual(2, payload["summary"]["error"])
        self.assertTrue(any(item["code"] == "EVIDENCE_MISSING" for item in payload["diagnostics"]))
        self.assertTrue(any(item["code"] == "EVIDENCE_NOT_RUN" for item in payload["diagnostics"]))

    def test_evidence_quality_cli_outputs_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = write_evidence_quality_spec(Path(tmp))

            completed = subprocess.run(
                [sys.executable, str(SCRIPT), "evidence-quality", str(spec)],
                check=False,
                capture_output=True,
                text=True,
            )

        payload = json.loads(completed.stdout)
        self.assertEqual(1, completed.returncode)
        self.assertEqual("findings", payload["status"])
        self.assertIn("by_classification", payload["summary"])

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
                        json.dumps({"payload": {"role": "user", "content": "I think these specs are missing verification and traceability."}}),
                        json.dumps({"payload": {"role": "assistant", "content": "The spec is incomplete and the agent was confused about the skill tools."}}),
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            payload = spec_runtime.mcp_audit(repo, sessions.parent.parent.parent)
            detailed = spec_runtime.mcp_audit(repo, sessions.parent.parent.parent, include_sessions=True)

        self.assertEqual("ok", payload["status"])
        self.assertEqual(1, payload["matched_files"])
        self.assertEqual(1, payload["error_counts"]["unknown_review_packet_type"])
        self.assertGreaterEqual(payload["mention_counts"]["tool_call"], 1)
        self.assertGreaterEqual(payload["mention_counts"]["resource"], 1)
        self.assertGreaterEqual(payload["interaction_counts"]["spec_missing_artifacts"], 1)
        self.assertGreaterEqual(payload["interaction_counts"]["spec_incomplete_or_stale"], 1)
        self.assertGreaterEqual(payload["interaction_counts"]["skill_interaction_confusion"], 1)
        self.assertEqual(1, payload["interaction_role_counts"]["spec_missing_artifacts"]["user"])
        self.assertIn("examples", payload)
        self.assertIn("interactions", payload["examples"])
        self.assertNotIn("sessions", payload)
        self.assertEqual(0, payload["summary"]["error"])
        self.assertIn("sessions", detailed)
        self.assertGreaterEqual(detailed["sessions"][0]["interaction_count"], 3)

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

    def test_lifecycle_guide_reports_blank_repo_bootstrap_preview(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / ".git").mkdir()
            payload = spec_runtime.lifecycle_guide(repo)

        self.assertEqual("blank", payload["repo_classification"])
        self.assertEqual("preview", payload["bootstrap"]["mode"])
        self.assertEqual("blank", payload["bootstrap"]["repo_classification"])
        self.assertTrue(any(item["path"] == "docs/README.md" for item in payload["bootstrap"]["writes"]))
        self.assertTrue(any(item["name"] == "project_summary" for item in payload["bootstrap"]["required_user_values"]))
        self.assertTrue(any(item["action"] == "review_bootstrap_plan" for item in payload["next_actions"]))
        self.assertIn("lifecycle_guide", payload["tooling"]["mcp_tools"])

    def test_lifecycle_guide_reports_active_spec_readiness(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            spec = write_complete_spec(repo)
            tasks_path = spec / "tasks.md"
            tasks_path.write_text(
                tasks_path.read_text(encoding="utf-8")
                .replace("- [x] T001 Do work.", "- [ ] T001 Do work.")
                .replace("  - Evidence: Done.", "  - Evidence: Pending."),
                encoding="utf-8",
            )
            payload = spec_runtime.lifecycle_guide(repo)

        self.assertEqual("active_specs", payload["repo_classification"])
        self.assertEqual("not_applicable", payload["bootstrap"]["mode"])
        self.assertEqual(1, len(payload["spec_readiness"]))
        self.assertEqual("001-current", payload["spec_readiness"][0]["spec_id"])
        self.assertEqual("implement", payload["spec_readiness"][0]["stage"])
        self.assertEqual("T001", payload["spec_readiness"][0]["next_task"]["task_id"])

    def test_stage_readiness_reports_ready_coverage(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            spec = write_complete_spec(repo)
            tasks_path = spec / "tasks.md"
            tasks_path.write_text(
                tasks_path.read_text(encoding="utf-8")
                .replace("- [x] T001 Do work.", "- [ ] T001 Do work.")
                .replace("  - Evidence: Done.", "  - Evidence: Pending."),
                encoding="utf-8",
            )
            payload = spec_runtime.stage_readiness(spec)

        self.assertEqual("implement", payload["stage"])
        self.assertTrue(payload["ready_for_agent"])
        self.assertTrue(payload["ready_to_implement"])
        self.assertEqual(0, payload["summary"]["blocking_gap_count"])
        self.assertEqual(0, payload["summary"]["property_gap_count"])
        self.assertEqual(0, payload["summary"]["acceptance_gap_count"])
        self.assertEqual("CP-001", payload["coverage"]["properties"][0]["id"])
        self.assertTrue(payload["coverage"]["properties"][0]["design_mapped"])

    def test_stage_readiness_reports_property_and_acceptance_gaps(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            spec = write_complete_spec(repo)
            tasks_path = spec / "tasks.md"
            tasks_path.write_text(
                tasks_path.read_text(encoding="utf-8")
                .replace("- [x] T001 Do work.", "- [ ] T001 Do work.")
                .replace("  - Evidence: Done.", "  - Evidence: Pending."),
                encoding="utf-8",
            )
            design_path = spec / "design.md"
            design_path.write_text(design_path.read_text(encoding="utf-8").replace(" and CP-001 coverage", ""), encoding="utf-8")
            traceability_path = spec / "traceability.md"
            traceability_path.write_text(
                traceability_path.read_text(encoding="utf-8")
                .replace("| T001 | Requirement 1 | AC1 |", "| T001 | Requirement 1 | none |")
                .replace("| Requirement 1 | AC1 |", "| Requirement 1 | none |")
                .replace("| CP-001 | `design.md#task-context` | T001 | `verification.md#quality-gates` |", "| CP-001 | none | none | none |"),
                encoding="utf-8",
            )
            payload = spec_runtime.stage_readiness(spec)

        gap_codes = {gap["code"] for gap in payload["blocking_gaps"]}
        self.assertFalse(payload["ready_to_implement"])
        self.assertIn("PROPERTY_DESIGN_MAPPING_MISSING", gap_codes)
        self.assertIn("PROPERTY_TASK_MAPPING_MISSING", gap_codes)
        self.assertIn("PROPERTY_VERIFICATION_MAPPING_MISSING", gap_codes)
        self.assertEqual(3, payload["summary"]["property_gap_count"])
        self.assertEqual(1, payload["summary"]["acceptance_gap_count"])
        self.assertEqual("requirement_covered_acceptance_unspecified", payload["coverage"]["acceptance_criteria"][0]["status"])

    def test_stage_readiness_reports_downstream_review_needs(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            spec = write_complete_spec(repo)
            tasks_path = spec / "tasks.md"
            tasks_path.write_text(
                tasks_path.read_text(encoding="utf-8")
                .replace("- [x] T001 Do work.", "- [ ] T001 Do work.")
                .replace("  - Evidence: Done.", "  - Evidence: Pending."),
                encoding="utf-8",
            )
            older = 1_700_000_000
            newer = older + 100
            for name in ["design.md", "tasks.md", "traceability.md", "verification.md"]:
                os.utime(spec / name, (older, older))
            os.utime(spec / "requirements.md", (newer, newer))
            payload = spec_runtime.stage_readiness(spec)

        self.assertFalse(payload["ready_to_implement"])
        self.assertEqual(4, payload["summary"]["downstream_review_need_count"])
        self.assertEqual({"requirements.md"}, {item["source"] for item in payload["downstream_review_needs"]})

    def test_bootstrap_plan_is_preview_only_for_near_blank_repo(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / ".git").mkdir()
            (repo / "README.md").write_text("# Example\n", encoding="utf-8")
            payload = spec_runtime.bootstrap_plan(
                repo,
                project_summary="Example project.",
                create_spec=True,
                spec_slug="first-feature",
            )

        self.assertEqual("preview", payload["mode"])
        self.assertEqual("near_blank", payload["repo_classification"])
        self.assertFalse((repo / "docs").exists())
        write_paths = {item["path"] for item in payload["writes"]}
        self.assertIn("docs/README.md", write_paths)
        self.assertIn("docs/reference/project-summary.md", write_paths)
        self.assertIn("docs/specs/000-first-feature/", write_paths)
        self.assertFalse(payload["required_user_values"])
        self.assertTrue(all(item["preview_only"] for item in payload["writes"]))

    def test_durable_templates_do_not_override_spec_package_fallback(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "docs/templates").mkdir(parents=True)
            (repo / "docs/templates/README.md").write_text("# Durable templates\n", encoding="utf-8")

            authority = spec_runtime.template_authority(repo)

        self.assertEqual("skill-fallback", authority["authority"])
        self.assertEqual(str(repo / "docs/templates"), authority["durable_templates_path"])
        self.assertTrue(authority["path"].endswith(os.path.join("references", "spec-package")))

    def test_repository_spec_package_templates_override_fallback(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "docs/templates/spec-package").mkdir(parents=True)
            (repo / "docs/templates/spec-package/tasks.md").write_text("# Tasks\n", encoding="utf-8")

            authority = spec_runtime.template_authority(repo)

        self.assertEqual("repository-spec-package", authority["authority"])
        self.assertEqual(str(repo / "docs/templates/spec-package"), authority["path"])

    def test_archive_index_validates_current_index(self):
        payload = spec_runtime.archive_index(ROOT)

        self.assertEqual(0, payload["summary"]["error"])
        self.assertEqual(0, payload["summary"]["warn"])
        self.assertEqual(27, payload["summary"]["total"])
        self.assertEqual(27, payload["summary"]["removed"])
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
            "017-npm-distribution-packaging",
            "018-mcp-ergonomics-observability",
            "019-validation-plan-builder",
            "020-evidence-quality-check",
            "021-closure-risk-review",
            "025-dev-cli-workflow-tools",
            "024-staged-developer-onboarding",
            "027-spec-local-canonical-context",
            "023-task-state-management-tools",
            "023-hierarchical-spec-authoring-hooks",
            "028-cross-platform-packaging",
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

    def test_validation_plan_classifies_runtime_change_and_task_contract(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            spec = write_complete_spec(repo)
            tasks_path = spec / "tasks.md"
            tasks_path.write_text(
                tasks_path.read_text(encoding="utf-8")
                .replace("- [x] T001 Do work.", "- [ ] T001 Do work.")
                .replace("  - Evidence: Done.", "  - Evidence: Pending."),
                encoding="utf-8",
            )

            payload = spec_runtime.validation_plan(
                repo,
                ["skills/spec-lifecycle-manager/scripts/spec_runtime.py"],
                spec,
                "T001",
            )

        checks = {item["id"]: item for item in payload["checks"]}
        self.assertIn("runtime", payload["file_classification"]["active_groups"])
        self.assertTrue(checks["unit-tests"]["required"])
        self.assertEqual("planned", checks["unit-tests"]["validation_state"])
        self.assertEqual("planned", payload["validation_contract"]["status"])
        self.assertFalse(payload["validation_contract"]["executed_evidence"])
        self.assertTrue(
            any(item["check_id"] == "unit-tests" for item in payload["validation_contract"]["automated_proof"])
        )

    def test_validation_plan_marks_unit_tests_not_applicable_for_docs_only_change(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_complete_spec(repo)
            payload = spec_runtime.validation_plan(repo, ["docs/reference/current.md"])

        checks = {item["id"]: item for item in payload["checks"]}
        self.assertTrue(payload["file_classification"]["docs_only"])
        self.assertFalse(checks["unit-tests"]["required"])
        self.assertEqual("not_applicable", checks["unit-tests"]["applicability"])
        self.assertEqual("not_applicable", checks["unit-tests"]["validation_state"])
        self.assertTrue(checks["scan"]["required"])
        self.assertTrue(checks["git-diff-check"]["required"])

    def test_validation_plan_classifies_spec_history_and_prompt_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_complete_spec(repo)
            payload = spec_runtime.validation_plan(
                repo,
                [
                    "docs/specs/001-current/tasks.md",
                    "docs/history/spec-archive-index.md",
                    "skills/spec-lifecycle-manager/prompts/task-context.json",
                ],
            )

        groups = payload["file_classification"]["active_groups"]
        checks = {item["id"]: item for item in payload["checks"]}
        self.assertIn("spec_package", groups)
        self.assertIn("history", groups)
        self.assertIn("prompts", groups)
        self.assertTrue(payload["file_classification"]["docs_only"])
        self.assertTrue(checks["archive-index"]["required"])
        self.assertTrue(checks["prompts"]["required"])
        self.assertEqual("not_applicable", checks["unit-tests"]["applicability"])

    def test_validation_plan_returns_baseline_without_changed_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_complete_spec(repo)
            payload = spec_runtime.validation_plan(repo)

        checks = {item["id"]: item for item in payload["checks"]}
        self.assertFalse(payload["file_classification"]["has_changes"])
        self.assertTrue(checks["scan"]["required"])
        self.assertEqual("recommended", checks["unit-tests"]["applicability"])
        self.assertEqual("recommended", checks["prompts"]["applicability"])

    def test_validation_plan_includes_package_and_sync_checks_for_package_change(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_sync_guard_repo(repo, Path(tmp) / "codex-home")
            payload = spec_runtime.validation_plan(repo, ["plugins/spec-lifecycle-manager/.codex-plugin/plugin.json"])

        checks = {item["id"]: item for item in payload["checks"]}
        self.assertIn("plugin_bundle", payload["file_classification"]["active_groups"])
        self.assertTrue(checks["package-contract"]["required"])
        self.assertTrue(checks["sync-guard"]["required"])
        self.assertTrue(checks["npm-pack-dry-run"]["required"])
        self.assertEqual("planned", checks["sync-guard"]["validation_state"])

    def test_validation_plan_reports_not_run_when_package_dry_run_input_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "plugins/spec-lifecycle-manager").mkdir(parents=True)
            payload = spec_runtime.validation_plan(repo, ["plugins/spec-lifecycle-manager/.codex-plugin/plugin.json"])

        checks = {item["id"]: item for item in payload["checks"]}
        self.assertEqual("not_run", checks["sync-guard"]["applicability"])
        self.assertEqual("blocked", checks["sync-guard"]["validation_state"])
        self.assertIn("blocker", checks["sync-guard"])
        self.assertEqual("not_run", checks["npm-pack-dry-run"]["applicability"])
        self.assertIn("package.json is missing", checks["npm-pack-dry-run"]["blocker"])

    def test_validation_plan_reports_contract_gaps_for_missing_task_context(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            spec = write_complete_spec(repo)
            tasks_path = spec / "tasks.md"
            tasks_path.write_text(
                tasks_path.read_text(encoding="utf-8").replace("  - Acceptance: Done.\n", ""),
                encoding="utf-8",
            )
            payload = spec_runtime.validation_plan(repo, ["docs/reference/current.md"], spec, "T001")

        fields = {item["field"] for item in payload["validation_contract"]["gaps"]}
        self.assertIn("false_positive_risk", fields)
        self.assertIn("false_negative_risk", fields)

    def test_validation_plan_reports_traceability_gap_for_missing_task(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            spec = write_complete_spec(repo)
            payload = spec_runtime.validation_plan(repo, ["docs/reference/current.md"], spec, "T999")

        gaps = payload["task_context"]["gaps"]
        self.assertTrue(any(item["code"] == "TASK_NOT_FOUND" for item in gaps))
        self.assertIsNone(payload["validation_contract"])

    def test_validation_plan_preserves_executed_evidence_from_task(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            spec = write_complete_spec(repo)
            payload = spec_runtime.validation_plan(repo, ["docs/reference/current.md"], spec, "T001")

        contract = payload["validation_contract"]
        self.assertEqual("executed", contract["status"])
        self.assertEqual(["Done."], contract["executed_evidence"])

    def test_cli_validation_plan_outputs_json(self):
        completed = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "validation-plan",
                str(ROOT),
                "--changed-files",
                "docs/reference/spec-lifecycle-runtime.md",
            ],
            check=True,
            capture_output=True,
            text=True,
        )

        payload = json.loads(completed.stdout)
        self.assertIn("checks", payload)
        self.assertIn("docs", payload["file_classification"]["active_groups"])

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

    def test_lint_spec_package_warns_for_missing_canonical_context_when_risk_declared(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = write_complete_spec(Path(tmp))
            requirements = spec / "requirements.md"
            requirements.write_text(
                requirements.read_text(encoding="utf-8")
                + "\n\n## Stale Doc Risk\n\nLegacy docs may be non-canonical background sources.\n",
                encoding="utf-8",
            )

            payload = spec_runtime.lint_spec_package(spec)

        diagnostics = payload["diagnostics"]
        self.assertIn("CANONICAL_CONTEXT_MISSING", {item["code"] for item in diagnostics})
        diagnostic = next(item for item in diagnostics if item["code"] == "CANONICAL_CONTEXT_MISSING")
        self.assertEqual("warn", diagnostic["severity"])
        self.assertTrue(diagnostic["import_plan"])

    def test_stage_readiness_returns_canonical_context_import_plan_for_stale_doc_risk(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = write_complete_spec(Path(tmp))
            requirements = spec / "requirements.md"
            requirements.write_text(
                requirements.read_text(encoding="utf-8")
                + "\n\n## Stale Doc Risk\n\nLegacy docs may be non-canonical background sources.\n",
                encoding="utf-8",
            )

            payload = spec_runtime.stage_readiness(spec)

        canonical_gap = next(
            item
            for item in payload["context_budget"]["gaps"]
            if item["code"] == "CANONICAL_CONTEXT_MISSING"
        )
        self.assertEqual("warn", canonical_gap["severity"])
        self.assertIn("stale-doc-risk", canonical_gap["signals"])
        self.assertTrue(canonical_gap["import_plan"])
        self.assertEqual("canonical-context.md", canonical_gap["import_plan"][0]["target_spec_path"])
        self.assertEqual("docs/reference/current.md", canonical_gap["import_plan"][0]["source_path"])

    def test_lint_spec_package_accepts_canonical_context_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = write_complete_spec(Path(tmp))
            (spec / "canonical-context.md").write_text(
                "\n".join(
                    [
                        "---",
                        "title: Canonical Context",
                        "doc_type: spec",
                        "artifact_type: canonical-context",
                        "status: draft",
                        "owner: platform",
                        "last_reviewed: 2026-07-02",
                        "---",
                        "",
                        "# Canonical Context",
                        "",
                        "## Purpose",
                        "Use an imported source.",
                        "",
                        "## Authority Hierarchy",
                        "AGENTS.md and governance remain authoritative.",
                        "",
                        "## Always-Canonical External Sources",
                        "| Source | Authority reason | Handling |",
                        "|--------|------------------|----------|",
                        "| `AGENTS.md` | repo instructions | read first |",
                        "",
                        "## Spec-Canonical Working Sources",
                        "| Source | Role | Scope | Notes |",
                        "|--------|------|-------|-------|",
                        "| `requirements.md` | intent | this spec | none |",
                        "",
                        "## Imported Sources",
                        "| Spec path | Source path | Source revision or date | Status | Canonical scope | Promotion target |",
                        "|-----------|-------------|-------------------------|--------|-----------------|------------------|",
                        "| `canonical-context.md` | `docs/reference/current.md` | 2026-07-02 | adapted | current behavior | `docs/reference/current.md` |",
                        "",
                        "## Non-Canonical Background Sources",
                        "| Source | Reason non-canonical | Handling |",
                        "|--------|----------------------|----------|",
                        "| `docs/reference/old.md` | stale | background only |",
                        "",
                        "## Promotion Map",
                        "| Spec-local content | Durable destination or route | Required before closure |",
                        "|--------------------|------------------------------|-------------------------|",
                        "| imported current behavior | `docs/reference/current.md` | yes |",
                    ]
                ),
                encoding="utf-8",
            )

            payload = spec_runtime.lint_spec_package(spec)
            promotion = spec_runtime.promotion_plan(spec)
            closure = spec_runtime.closure_check(spec)

        self.assertNotIn("CANONICAL_CONTEXT_MISSING", {item["code"] for item in payload["diagnostics"]})
        self.assertIn("docs/reference/current.md", {item["target"] for item in promotion["targets"]})
        self.assertTrue(closure["ready"])

    def test_closure_check_blocks_unresolved_required_canonical_promotion(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = write_complete_spec(Path(tmp))
            (spec / "canonical-context.md").write_text(
                "\n".join(
                    [
                        "---",
                        "title: Canonical Context",
                        "doc_type: spec",
                        "artifact_type: canonical-context",
                        "status: draft",
                        "owner: platform",
                        "last_reviewed: 2026-07-02",
                        "---",
                        "",
                        "# Canonical Context",
                        "",
                        "## Purpose",
                        "Use an imported source.",
                        "",
                        "## Authority Hierarchy",
                        "AGENTS.md and governance remain authoritative.",
                        "",
                        "## Always-Canonical External Sources",
                        "| Source | Authority reason | Handling |",
                        "|--------|------------------|----------|",
                        "| `AGENTS.md` | repo instructions | read first |",
                        "",
                        "## Spec-Canonical Working Sources",
                        "| Source | Role | Scope | Notes |",
                        "|--------|------|-------|-------|",
                        "| `requirements.md` | intent | this spec | none |",
                        "",
                        "## Imported Sources",
                        "| Spec path | Source path | Source revision or date | Status | Canonical scope | Promotion target |",
                        "|-----------|-------------|-------------------------|--------|-----------------|------------------|",
                        "| `canonical-context.md` | `docs/reference/current.md` | 2026-07-02 | adapted | current behavior | TBD |",
                        "",
                        "## Non-Canonical Background Sources",
                        "| Source | Reason non-canonical | Handling |",
                        "|--------|----------------------|----------|",
                        "| none | none | none |",
                        "",
                        "## Promotion Map",
                        "| Spec-local content | Durable destination or route | Required before closure |",
                        "|--------------------|------------------------------|-------------------------|",
                        "| imported current behavior | TBD | yes |",
                    ]
                ),
                encoding="utf-8",
            )

            lint_payload = spec_runtime.lint_spec_package(spec)
            closure = spec_runtime.closure_check(spec)

        self.assertIn(
            "CANONICAL_CONTEXT_IMPORTED_SOURCE_METADATA_MISSING",
            {item["code"] for item in lint_payload["diagnostics"]},
        )
        self.assertFalse(closure["ready"])
        self.assertIn("CANONICAL_CONTEXT_PROMOTION_UNRESOLVED", {item["code"] for item in closure["blockers"]})

    def test_next_task_selects_first_unblocked_task_with_context(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = write_complete_spec(Path(tmp))
            payload = spec_runtime.next_task(spec)

        self.assertIsNone(payload["selected"])
        self.assertEqual("No runnable incomplete task found.", payload["message"])

    def test_parse_tasks_reports_extended_task_status_markers(self):
        text = "\n".join(
            [
                "# Tasks",
                "",
                "- [ ] T001 Pending.",
                "- [~] T002 In progress.",
                "- [/] T003 Partial.",
                "- [>] T004 Follow-up.",
                "- [-] T005 No-op.",
                "- [?] T006 Review.",
                "- [!] T007 Attention.",
                "- [Y] T008 Legacy partial.",
                "- [*] T009 Legacy hold.",
                "- [e] T010 Legacy error.",
                "- [x] T011 Complete.",
            ]
        )

        tasks = spec_runtime.parse_tasks_from_text(text)
        statuses = {task.task_id: task.status for task in tasks}
        legacy_markers = {task.task_id: task.legacy_marker for task in tasks if task.legacy_marker}
        counts = spec_runtime.task_status_counts(tasks)

        self.assertEqual(
            {
                "T001": "pending",
                "T002": "in_progress",
                "T003": "partial",
                "T004": "follow_up",
                "T005": "no_op",
                "T006": "review_needed",
                "T007": "attention",
                "T008": "partial",
                "T009": "attention",
                "T010": "attention",
                "T011": "complete",
            },
            statuses,
        )
        self.assertEqual(1, counts["pending"])
        self.assertEqual(1, counts["in_progress"])
        self.assertEqual(2, counts["partial"])
        self.assertEqual(1, counts["follow_up"])
        self.assertEqual(1, counts["no_op"])
        self.assertEqual(1, counts["review_needed"])
        self.assertEqual(3, counts["attention"])
        self.assertEqual(1, counts["complete"])
        self.assertEqual({"T008": "partial", "T009": "on_hold", "T010": "error"}, legacy_markers)
        self.assertTrue(next(task for task in tasks if task.task_id == "T011").complete)
        self.assertFalse(next(task for task in tasks if task.task_id == "T003").complete)

    def test_parse_tasks_reports_metadata_and_subtask_relationships(self):
        text = "\n".join(
            [
                "# Tasks",
                "",
                "- [~] T001 Parent task.",
                "  - Status: Waiting for fixture coverage.",
                "  - Evidence mode: implementation",
                "  - Follow-up: Route downstream docs.",
                "  - Destination: `docs/backlog/README.md`",
                "  - Decision owner: platform",
                "  - Upstream specs: `docs/specs/020-evidence-quality-check`, T002",
                "  - Downstream specs: `docs/specs/024-staged-developer-onboarding`",
                "  - Evidence: Parser payload updated.",
                "  - [ ] T001.1 Child task.",
                "    - Evidence: Pending.",
            ]
        )

        tasks = spec_runtime.parse_tasks_from_text(text)
        parent = tasks[0]
        child = tasks[1]
        payload = spec_runtime.task_payload(parent)

        self.assertEqual(["T001.1"], parent.children)
        self.assertEqual("T001", child.parent_id)
        self.assertEqual("Waiting for fixture coverage.", payload["status_note"])
        self.assertEqual("implementation", payload["evidence_mode"])
        self.assertEqual("Route downstream docs.", payload["follow_up"])
        self.assertEqual("docs/backlog/README.md", payload["destination"])
        self.assertEqual("platform", payload["decision_owner"])
        self.assertEqual(["docs/specs/020-evidence-quality-check"], payload["upstream_specs"])
        self.assertEqual(["docs/specs/024-staged-developer-onboarding"], payload["downstream_specs"])

    def test_next_task_skips_non_runnable_states_but_selects_partial(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = write_complete_spec(Path(tmp))
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
                        "- [>] T001 Waiting on owner.",
                        "  - Depends on: none",
                        "  - Files: `docs/reference/current.md`",
                        "  - Acceptance: Done.",
                        "  - Evidence: Status: routed - owner decision needed.",
                        "",
                        "- [!] T002 Failed migration.",
                        "  - Depends on: none",
                        "  - Files: `docs/reference/current.md`",
                        "  - Acceptance: Done.",
                        "  - Evidence: Status: attention - missing credential.",
                        "",
                        "- [/] T003 Finish remaining docs.",
                        "  - Depends on: none",
                        "  - Files: `docs/reference/current.md`",
                        "  - Acceptance: Done.",
                        "  - Evidence: Partial local docs update complete.",
                    ]
                ),
                encoding="utf-8",
            )

            payload = spec_runtime.next_task(spec)

        self.assertEqual("T003", payload["selected"]["task_id"])
        self.assertEqual("partial", payload["selected"]["status"])
        blocked = {item["task_id"]: item["blockers"][0]["reason"] for item in payload["blocked"]}
        self.assertEqual("task status is follow_up", blocked["T001"])
        self.assertEqual("task status is attention", blocked["T002"])

    def test_task_list_groups_tasks_and_reports_dependency_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = write_complete_spec(Path(tmp))
            (spec / "tasks.md").write_text(
                "\n".join(
                    [
                        "# Tasks",
                        "",
                        "## Phase 1: Runtime",
                        "",
                        "- [x] T001 Build parser.",
                        "  - Evidence: Parser tests passed.",
                        "",
                        "- [ ] T002 Add grouped task listing and detail helpers.",
                        "  - Depends on: T001",
                        "  - Files: `skills/spec-lifecycle-manager/scripts/spec_runtime.py`, `tests/runtime/test_spec_runtime.py`, `docs/reference/spec-lifecycle-runtime.md`",
                        "  - Acceptance: Helpers return grouped tasks and dependency state.",
                        "  - Evidence: Pending.",
                        "  - [ ] T002.1 Add list helper.",
                        "    - Evidence: Pending.",
                    ]
                ),
                encoding="utf-8",
            )

            payload = spec_runtime.task_list(spec)

        self.assertEqual(3, payload["summary"]["total"])
        self.assertEqual("Phase 1: Runtime", payload["phases"][0]["name"])
        tasks = {task["task_id"]: task for task in payload["phases"][0]["tasks"]}
        self.assertTrue(tasks["T002"]["dependency_state"]["ready"])
        self.assertEqual(["T002.1"], tasks["T002"]["children"])
        self.assertEqual("pending", tasks["T002"]["evidence_summary"]["state"])
        self.assertTrue(tasks["T002"]["broad_task_warnings"])
        self.assertEqual("broad_task", payload["findings"][0]["classification"])

    def test_task_details_returns_traceability_parent_and_children(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = write_complete_spec(Path(tmp))
            (spec / "tasks.md").write_text(
                "\n".join(
                    [
                        "# Tasks",
                        "",
                        "- [x] T001 Parent.",
                        "  - Depends on: none",
                        "  - Files: `docs/reference/current.md`",
                        "  - Acceptance: Done.",
                        "  - Evidence: Done.",
                        "  - [ ] T001.1 Child.",
                        "    - Evidence: Pending.",
                    ]
                ),
                encoding="utf-8",
            )

            payload = spec_runtime.task_details(spec, "T001")

        self.assertEqual("ready", payload["status"])
        self.assertEqual("T001", payload["task"]["task_id"])
        self.assertEqual(["T001.1"], payload["task"]["children"])
        self.assertEqual("T001.1", payload["children"][0]["task_id"])
        self.assertEqual("Requirement 1", payload["traceability_context"]["traceability_row"]["Requirements"])
        self.assertTrue(payload["dependency_state"]["ready"])

    def test_task_state_audit_reports_core_findings(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            spec = write_complete_spec(repo)
            (spec / "tasks.md").write_text(
                "\n".join(
                    [
                        "# Tasks",
                        "",
                        "- [x] T001 Complete with pending evidence.",
                        "  - Evidence: Pending.",
                        "  - [ ] T001.1 Incomplete child.",
                        "    - Evidence: Pending.",
                        "",
                        "- [ ] T002 Pending with work.",
                        "  - Evidence: Runtime helper implemented.",
                        "",
                        "- [>] T003 Routed without destination.",
                        "  - Evidence: Follow-up remains.",
                        "",
                        "- [~] T004 In progress pending.",
                        "  - Evidence: Pending.",
                    ]
                ),
                encoding="utf-8",
            )

            payload = spec_runtime.task_state_audit(spec)

        classes = {item["classification"] for item in payload["findings"]}
        self.assertIn("contradictory_completion_evidence", classes)
        self.assertIn("complete_parent_with_incomplete_children", classes)
        self.assertIn("candidate_complete", classes)
        self.assertIn("metadata_missing", classes)
        self.assertIn("non_pending_marker_with_pending_evidence", classes)

    def test_task_state_audit_reports_cross_spec_dependency_untrusted(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_complete_spec(repo)
            upstream = repo / "docs/specs/002-upstream"
            upstream.mkdir(parents=True)
            (upstream / "tasks.md").write_text("# Tasks\n\n- [ ] T001 Unfinished.\n  - Evidence: Pending.\n", encoding="utf-8")
            spec = repo / "docs/specs/001-current"
            (spec / "tasks.md").write_text(
                "# Tasks\n\n- [ ] T001 Depends upstream.\n  - Upstream specs: `docs/specs/002-upstream`\n  - Evidence: Pending.\n",
                encoding="utf-8",
            )

            payload = spec_runtime.task_state_audit(spec)

        classes = {item["classification"] for item in payload["findings"]}
        self.assertIn("cross_spec_dependency_untrusted", classes)

    def test_set_task_state_defaults_to_dry_run_and_requires_write_intent(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = write_complete_spec(Path(tmp))
            before = (spec / "tasks.md").read_text(encoding="utf-8")

            preview = spec_runtime.set_task_state(spec, "T001", "complete", "Unit tests passed.")
            rejected = spec_runtime.set_task_state(spec, "T001", "complete", "Unit tests passed.", dry_run=False)
            after = (spec / "tasks.md").read_text(encoding="utf-8")

        self.assertEqual("preview", preview["status"])
        self.assertEqual("rejected", rejected["status"])
        self.assertEqual(before, after)
        self.assertIn("TASK_STATE_WRITE_INTENT_MISSING", {item["code"] for item in rejected["validation"]["findings"]})

    def test_set_task_state_writes_only_selected_block(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = write_complete_spec(Path(tmp))
            (spec / "tasks.md").write_text(
                "# Tasks\n\n- [ ] T001 First.\n  - Evidence: Pending.\n\n- [ ] T002 Second.\n  - Evidence: Pending.\n",
                encoding="utf-8",
            )

            payload = spec_runtime.set_task_state(
                spec,
                "T001",
                "follow_up",
                "Routed to backlog.",
                destination="docs/backlog/README.md",
                dry_run=False,
                write_intent=True,
                evidence_mode="routing",
            )
            text = (spec / "tasks.md").read_text(encoding="utf-8")

        self.assertEqual("updated", payload["status"])
        self.assertIn("- [>] T001 First.", text)
        self.assertIn("- Evidence: Routed to backlog.", text)
        self.assertIn("- Destination: docs/backlog/README.md", text)
        self.assertIn("- [ ] T002 Second.", text)

    def test_set_task_state_replaces_multiline_field_value(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = write_complete_spec(Path(tmp))
            (spec / "tasks.md").write_text(
                "# Tasks\n\n- [ ] T001 Multiline evidence.\n  - Evidence: Old evidence.\n    stale continuation\n  - Acceptance: Done when tests pass.\n",
                encoding="utf-8",
            )

            payload = spec_runtime.set_task_state(
                spec,
                "T001",
                "complete",
                "Unit tests passed.",
                dry_run=False,
                write_intent=True,
            )
            text = (spec / "tasks.md").read_text(encoding="utf-8")

        self.assertEqual("updated", payload["status"])
        self.assertIn("- Evidence: Unit tests passed.", text)
        self.assertNotIn("stale continuation", text)
        self.assertIn("- Acceptance: Done when tests pass.", text)

    def test_set_task_state_rejects_unsafe_completion(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = write_complete_spec(Path(tmp))

            payload = spec_runtime.set_task_state(spec, "T001", "complete", "Pending follow-up review.")

        self.assertEqual("rejected", payload["status"])
        self.assertIn("TASK_STATE_UNSAFE_COMPLETION_EVIDENCE", {item["code"] for item in payload["validation"]["findings"]})

    def test_set_task_state_rejects_contract_only_completion_without_acceptance(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = write_complete_spec(Path(tmp))

            payload = spec_runtime.set_task_state(spec, "T001", "complete", "Contract drafted.", evidence_mode="contract")

        self.assertEqual("rejected", payload["status"])
        self.assertIn("TASK_STATE_EVIDENCE_MODE_NOT_COMPLETABLE", {item["code"] for item in payload["validation"]["findings"]})

    def test_set_task_state_rejects_out_of_bound_and_archived_specs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            outside = root / "notes"
            outside.mkdir()
            (outside / "tasks.md").write_text("# Tasks\n\n- [ ] T001 Outside.\n  - Evidence: Pending.\n", encoding="utf-8")
            archived = write_complete_spec(root, status="archived")

            outside_payload = spec_runtime.set_task_state(outside, "T001", "complete", "Done.")
            archived_payload = spec_runtime.set_task_state(archived, "T001", "complete", "Done.")

        self.assertIn("TASK_STATE_TARGET_INVALID", {item["code"] for item in outside_payload["validation"]["findings"]})
        self.assertIn("TASK_STATE_ARCHIVED_SPEC", {item["code"] for item in archived_payload["validation"]["findings"]})

    def test_closure_check_reports_completed_spec_ready(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = write_complete_spec(Path(tmp))
            payload = spec_runtime.closure_check(spec)

        self.assertTrue(payload["ready"])
        self.assertEqual([], payload["blockers"])

    def test_cli_scan_outputs_json(self):
        completed = subprocess.run(
            [sys.executable, str(SCRIPT),"scan", str(ROOT)],
            check=True,
            capture_output=True,
            text=True,
        )

        payload = json.loads(completed.stdout)
        self.assertIn("specs", payload)

    def test_cli_lifecycle_guide_and_bootstrap_plan_output_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / ".git").mkdir()
            spec = write_complete_spec(repo)
            guide = subprocess.run(
                [sys.executable, str(SCRIPT),"lifecycle-guide", str(repo)],
                check=True,
                capture_output=True,
                text=True,
            )
            bootstrap = subprocess.run(
                [sys.executable, str(SCRIPT),"bootstrap-plan", str(repo), "--project-summary", "Example."],
                check=True,
                capture_output=True,
                text=True,
            )
            stage = subprocess.run(
                [sys.executable, str(SCRIPT),"stage-readiness", str(spec)],
                check=True,
                capture_output=True,
                text=True,
            )

        guide_payload = json.loads(guide.stdout)
        bootstrap_payload = json.loads(bootstrap.stdout)
        stage_payload = json.loads(stage.stdout)
        self.assertEqual("active_specs", guide_payload["repo_classification"])
        self.assertEqual("preview", bootstrap_payload["mode"])
        self.assertEqual("001-current", stage_payload["spec_id"])

    def test_prompt_definitions_are_discoverable_and_valid(self):
        payload = spec_runtime.load_prompt_definitions(ROOT)

        names = {prompt["name"] for prompt in payload["prompts"]}
        self.assertTrue({"reconcile-spec", "choose-next-task", "task-context", "lint-spec", "developer-start"} <= names)
        self.assertEqual({"error": 0, "warn": 0, "info": 0}, payload["summary"])

    def test_spec_authoring_context_recommends_next_artifact(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / ".git").mkdir()
            spec = repo / "docs/specs/001-new"
            spec.mkdir(parents=True)
            (spec / "requirements.md").write_text("# Requirements\n", encoding="utf-8")

            payload = spec_runtime.spec_authoring_context(
                repo,
                ["docs/specs/001-new/requirements.md"],
                "spec-file-changed",
            )

        context = payload["contexts"][0]
        self.assertEqual("initial_authoring", context["mode"])
        self.assertEqual(["requirements.md"], context["changed_artifacts"])
        self.assertEqual("design.md", context["next_authoring_step"]["artifact"])
        self.assertEqual([], context["downstream_review"])

    def test_spec_authoring_context_reports_downstream_review_for_revision(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_complete_spec(repo)

            payload = spec_runtime.spec_authoring_context(
                repo,
                ["docs/specs/001-current/requirements.md"],
                "spec-file-changed",
            )

        context = payload["contexts"][0]
        downstream = {item["artifact"]: item["reason"] for item in context["downstream_review"]}
        downstream_paths = {item["artifact"]: item["path"] for item in context["downstream_review"]}
        self.assertEqual("revision", context["mode"])
        self.assertEqual("docs/specs/001-current", context["spec_path"])
        self.assertIsNone(context["next_authoring_step"])
        self.assertEqual("review_existing_downstream", downstream["design.md"])
        self.assertEqual("review_existing_downstream", downstream["tasks.md"])
        self.assertEqual("docs/specs/001-current/tasks.md", downstream_paths["tasks.md"])
        self.assertNotIn(str(repo), json.dumps(payload))

    def test_spec_authoring_context_reports_missing_prerequisite(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / ".git").mkdir()
            spec = repo / "docs/specs/001-new"
            spec.mkdir(parents=True)
            (spec / "design.md").write_text("# Design\n", encoding="utf-8")

            payload = spec_runtime.spec_authoring_context(
                repo,
                ["docs/specs/001-new/design.md"],
                "spec-file-changed",
            )

        context = payload["contexts"][0]
        missing = {(item["artifact"], item["for_artifact"]) for item in context["missing_prerequisites"]}
        missing_paths = {item["artifact"]: item["path"] for item in context["missing_prerequisites"]}
        codes = {item["code"] for item in payload["diagnostics"]}
        self.assertEqual("initial_authoring", context["mode"])
        self.assertIn(("requirements.md", "design.md"), missing)
        self.assertEqual("docs/specs/001-new/requirements.md", missing_paths["requirements.md"])
        self.assertIn("SPEC_AUTHORING_PREREQUISITE_MISSING", codes)
        self.assertNotIn(str(repo), json.dumps(payload))

    def test_hook_spec_file_changed_reports_authoring_context_for_affected_package(self):
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
        self.assertEqual({"error": 0, "warn": 0, "info": 1}, payload["summary"])
        self.assertEqual(1, len(payload["affected_specs"]))
        self.assertEqual(["docs/specs/001-current"], payload["affected_specs"])
        self.assertEqual("task_update", payload["authoring_context"]["contexts"][0]["mode"])
        self.assertNotIn(str(repo), json.dumps(payload))

    def test_hook_normalizes_absolute_changed_files_to_repo_relative_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            spec = write_complete_spec(repo)
            payload = spec_runtime.run_hook(
                repo,
                "spec-file-changed",
                changed_files=[str(spec / "requirements.md")],
                severity_profile="advisory",
            )

        self.assertEqual(["docs/specs/001-current/requirements.md"], payload["changed_files"])
        self.assertEqual(["docs/specs/001-current"], payload["affected_specs"])
        self.assertNotIn(str(repo), json.dumps(payload))

    def test_hook_spec_file_changed_uses_authoring_context_without_package_lint_flood(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / ".git").mkdir()
            spec = repo / "docs/specs/001-new"
            spec.mkdir(parents=True)
            (spec / "requirements.md").write_text("# Requirements\n", encoding="utf-8")
            (spec / "design.md").write_text("# Design\n", encoding="utf-8")

            payload = spec_runtime.run_hook(
                repo,
                "spec-file-changed",
                changed_files=["docs/specs/001-new/design.md"],
                severity_profile="advisory",
            )

        context = payload["authoring_context"]["contexts"][0]
        codes = {item["code"] for item in payload["diagnostics"]}
        self.assertEqual("initial_authoring", context["mode"])
        self.assertEqual("tasks.md", context["next_authoring_step"]["artifact"])
        self.assertNotIn("CORE_ARTIFACT_MISSING", codes)
        self.assertNotIn("TASKS_MISSING", codes)

    def test_hook_spec_file_changed_reports_revision_downstream_context(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_complete_spec(repo)

            payload = spec_runtime.run_hook(
                repo,
                "spec-file-changed",
                changed_files=["docs/specs/001-current/design.md"],
                severity_profile="advisory",
            )

        context = payload["authoring_context"]["contexts"][0]
        downstream = {item["artifact"] for item in context["downstream_review"]}
        self.assertEqual("revision", context["mode"])
        self.assertIsNone(context["next_authoring_step"])
        self.assertIn("tasks.md", downstream)
        self.assertIn("SPEC_AUTHORING_DOWNSTREAM_REVIEW", {item["code"] for item in payload["diagnostics"]})

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
        self.assertIn("TASK_AUDIT_CONTRADICTORY_COMPLETION_EVIDENCE", {item["code"] for item in payload["diagnostics"]})

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

    def test_agent_slice_start_reports_existing_in_progress_task(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            spec = write_complete_spec(repo)
            (spec / "tasks.md").write_text(
                "# Tasks\n\n- [~] T001 Existing.\n  - Evidence: Work started.\n\n- [ ] T002 New.\n  - Evidence: Pending.\n",
                encoding="utf-8",
            )

            payload = spec_runtime.run_hook(
                repo,
                "agent-slice-start",
                spec_path=spec,
                task_id="T002",
                severity_profile="advisory",
            )

        self.assertIn("TASK_IN_PROGRESS_EXISTS", {item["code"] for item in payload["diagnostics"]})

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
                [sys.executable, str(SCRIPT),"agent-backed-tool", str(spec), "--tool-name", "closure_risk_review", "--model-class", "cheap"],
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
            [sys.executable, str(SCRIPT),"prompts", str(ROOT)],
            check=True,
            capture_output=True,
            text=True,
        )

        payload = json.loads(completed.stdout)
        self.assertEqual(9, len(payload["prompts"]))

    def test_cli_spec_close_hook_exits_nonzero_when_blocking(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = self.write_incomplete_spec(Path(tmp))
            completed = subprocess.run(
                [
                    sys.executable,
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
                [sys.executable, str(SCRIPT),"review-packet", str(spec), "--review-type", "design_requirements_trace"],
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
