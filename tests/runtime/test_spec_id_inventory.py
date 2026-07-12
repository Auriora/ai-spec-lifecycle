import tempfile
import unittest
from pathlib import Path
import sys
from unittest import mock
import json
import subprocess

ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = ROOT / "skills/spec-lifecycle-manager/scripts"
SCRIPT = SCRIPT_DIR / "spec_runtime.py"
sys.path.insert(0, str(SCRIPT_DIR))

from lifecycle import core


class SpecIdInventoryTests(unittest.TestCase):
    def test_empty_scope_returns_provisional_zero_without_writes(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            before = sorted(repo.rglob("*"))

            payload = core.spec_id_inventory(repo)

            self.assertEqual("000", payload["next_available_spec_number"])
            self.assertEqual([], payload["used_numbers"])
            self.assertEqual("high", payload["confidence"])
            self.assertTrue(payload["provisional"])
            self.assertEqual(before, sorted(repo.rglob("*")))

    def test_active_archive_closure_and_legacy_ranges_are_monotonic(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            specs = repo / "docs/specs"
            history = repo / "docs/history"
            (specs / "005-active").mkdir(parents=True)
            history.mkdir(parents=True)
            (history / "spec-archive-index.md").write_text(
                "# Archive\n\n## Entries\n\n"
                "| Spec ID | Status |\n|---|---|\n"
                "| 007-removed | removed |\n| 009-retained | retained |\n\n"
                "## Legacy Gaps\n\n| Range | Reason |\n|---|---|\n| 008-011 | imported history |\n",
                encoding="utf-8",
            )
            (history / "spec-closure-log.md").write_text(
                "# Closure\n\n### 2026-07-12 - 012-log-only\n",
                encoding="utf-8",
            )

            payload = core.spec_id_inventory(repo)

            self.assertEqual("013", payload["next_available_spec_number"])
            self.assertEqual(11, payload["legacy_upper_bound"])
            self.assertEqual([5, 7, 9, 12], payload["used_numbers"])
            self.assertEqual("reduced", payload["confidence"])
            self.assertEqual(
                ["active_package", "archive_index", "archive_index", "closure_log"],
                [item["source_kind"] for item in payload["evidence"]],
            )

    def test_duplicate_and_malformed_ids_are_diagnostics(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            specs = repo / "docs/specs"
            (specs / "003-one").mkdir(parents=True)
            (specs / "003-two").mkdir()
            (specs / "bad_ID").mkdir()

            payload = core.spec_id_inventory(repo)

            codes = {item["code"] for item in payload["diagnostics"]}
            self.assertEqual("004", payload["next_available_spec_number"])
            self.assertIn("SPEC_ID_PREFIX_DUPLICATE", codes)
            self.assertIn("SPEC_ID_MALFORMED", codes)
            self.assertIn("SPEC_ID_HISTORY_MISSING", codes)
            self.assertEqual("reduced", payload["confidence"])

    def test_selected_docs_root_does_not_borrow_root_history(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "docs/specs/099-root").mkdir(parents=True)
            (repo / "docs/platform/specs/004-platform").mkdir(parents=True)
            (repo / "docs/history").mkdir(parents=True)
            (repo / "docs/history/spec-closure-log.md").write_text(
                "### 2026-07-12 - 100-root-only\n", encoding="utf-8"
            )

            payload = core.spec_id_inventory(repo, "docs/platform")

            self.assertEqual("005", payload["next_available_spec_number"])
            self.assertEqual("docs/platform", payload["numbering_scope"]["docs_root"])
            self.assertEqual([], payload["numbering_scope"]["history_sources"])
            self.assertIn("SPEC_ID_HISTORY_MISSING", {item["code"] for item in payload["diagnostics"]})

    def test_docs_root_escape_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                core.spec_id_inventory(Path(tmp), "../outside")

    def test_central_history_claiming_nested_scope_is_ambiguous_not_borrowed(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "docs/platform/specs/004-platform").mkdir(parents=True)
            history = repo / "docs/history"
            history.mkdir(parents=True)
            (history / "spec-archive-index.md").write_text(
                "# Archive\n\n## Entries\n\n"
                "| Spec ID | Package path | Status |\n|---|---|---|\n"
                "| 006-old | `docs/platform/specs/006-old/` | removed |\n",
                encoding="utf-8",
            )

            payload = core.spec_id_inventory(repo, "docs/platform")

            self.assertEqual("005", payload["next_available_spec_number"])
            self.assertEqual("low", payload["confidence"])
            self.assertIn("SPEC_ID_HISTORY_AMBIGUOUS", {item["code"] for item in payload["diagnostics"]})

    def test_creation_plan_is_stable_safe_and_read_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "docs/specs/004-existing").mkdir(parents=True)
            before = sorted(path.relative_to(repo).as_posix() for path in repo.rglob("*"))

            first = core.spec_creation_plan(repo, "new-capability")
            second = core.spec_creation_plan(
                repo, "new-capability", expected_fingerprint=first["evidence_fingerprint"]
            )

            self.assertEqual("ready", first["status"])
            self.assertEqual("005-new-capability", first["proposed_spec_id"])
            self.assertEqual("docs/specs/005-new-capability", first["proposed_path"])
            self.assertTrue(first["path_within_specs_root"])
            self.assertTrue(first["provisional"])
            self.assertFalse(first["reservation"])
            self.assertTrue(second["fingerprint_valid"])
            self.assertEqual(first["evidence_fingerprint"], second["evidence_fingerprint"])
            self.assertEqual(before, sorted(path.relative_to(repo).as_posix() for path in repo.rglob("*")))

    def test_creation_plan_rejects_unsafe_slugs_without_paths(self):
        invalid = ["", "Bad", "two--parts", "-edge", "edge-", "../escape", "a/b", "naïve", "a.b", "a\nb"]
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            for slug in invalid:
                with self.subTest(slug=slug):
                    payload = core.spec_creation_plan(repo, slug)
                    self.assertEqual("invalid", payload["status"])
                    self.assertIsNone(payload["proposed_path"])
                    self.assertIsNone(payload["evidence_fingerprint"])

    def test_selected_docs_template_precedence_and_artifact_inventory(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            root_template = repo / "docs/templates/spec-package"
            selected_template = repo / "docs/platform/templates/spec-package"
            root_template.mkdir(parents=True)
            selected_template.mkdir(parents=True)
            (root_template / "requirements.md").write_text("root", encoding="utf-8")
            (selected_template / "requirements.md").write_text("selected", encoding="utf-8")
            (selected_template / "research.md").write_text("optional", encoding="utf-8")

            payload = core.spec_creation_plan(repo, "nested", "docs/platform")

            self.assertEqual("selected-docs-root", payload["template_authority"]["authority"])
            self.assertEqual("docs/platform/templates/spec-package", payload["template_authority"]["path"])
            self.assertEqual(["research.md"], payload["planned_optional_artifacts"])
            self.assertEqual(["requirements.md", "design.md", "tasks.md"], payload["planned_core_artifacts"])

    def test_changed_numbering_or_template_evidence_returns_stale_refresh(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            first = core.spec_creation_plan(repo, "fresh")
            (repo / "docs/specs/000-claimed").mkdir(parents=True)

            numbering_changed = core.spec_creation_plan(
                repo, "fresh", expected_fingerprint=first["evidence_fingerprint"]
            )
            template = repo / "docs/templates/spec-package"
            template.mkdir(parents=True)
            (template / "requirements.md").write_text("template", encoding="utf-8")
            template_changed = core.spec_creation_plan(
                repo, "fresh", expected_fingerprint=numbering_changed["evidence_fingerprint"]
            )

            self.assertEqual("stale", numbering_changed["status"])
            self.assertEqual("001-fresh", numbering_changed["proposed_spec_id"])
            self.assertFalse(numbering_changed["fingerprint_valid"])
            self.assertEqual("stale", template_changed["status"])
            self.assertEqual("selected-docs-root", template_changed["template_authority"]["authority"])

    def test_race_collision_never_claims_a_reservation(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            inventory = core.spec_id_inventory(repo)
            (repo / "docs/specs/000-race").mkdir(parents=True)
            with mock.patch.object(core, "spec_id_inventory", return_value=inventory):
                payload = core.spec_creation_plan(repo, "race")

            self.assertEqual("collision", payload["status"])
            self.assertFalse(payload["reservation"])
            self.assertIsNotNone(payload["refreshed_arguments"])
            self.assertEqual("001-race", payload["fresh_proposal"]["proposed_spec_id"])
            self.assertIn("SPEC_CREATION_PATH_COLLISION", {item["code"] for item in payload["diagnostics"]})

    def test_bootstrap_reuses_shared_allocator_for_empty_and_established_scopes(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            empty = core.bootstrap_plan(repo, create_spec=True, spec_slug="first")
            (repo / "docs/specs/004-existing").mkdir(parents=True)
            established = core.bootstrap_plan(repo, create_spec=True, spec_slug="next")

            self.assertIn("docs/specs/000-first/", {item["path"] for item in empty["writes"]})
            self.assertEqual("000", empty["spec_creation_plan"]["next_available_spec_number"])
            self.assertIn("docs/specs/005-next/", {item["path"] for item in established["writes"]})
            self.assertEqual("005", established["spec_creation_plan"]["next_available_spec_number"])

    def test_scan_adds_allocation_without_changing_inventory(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "docs/specs/002-current").mkdir(parents=True)

            payload = core.scan_specs(repo)

            self.assertEqual(["002-current"], [item["spec_id"] for item in payload["specs"]])
            self.assertEqual("003", payload["next_available_spec_number"])
            self.assertTrue(payload["spec_id_allocation"]["provisional"])
            self.assertEqual("plan_spec_creation", payload["available_next_actions"][0]["id"])

    def test_no_active_context_and_preflight_use_selected_scope_allocation(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            history = repo / "docs/platform/history"
            history.mkdir(parents=True)
            (history / "spec-archive-index.md").write_text(
                "# Archive\n\n## Entries\n\n| Spec ID | Status |\n|---|---|\n| 008-old | removed |\n",
                encoding="utf-8",
            )
            (history / "spec-closure-log.md").write_text("# Closure\n", encoding="utf-8")

            context = core.no_active_spec_context(repo, "docs/platform")
            preflight = core.active_spec_preflight(repo, docs_root="docs/platform")

            self.assertEqual("009", context["next_available_spec_number"])
            self.assertEqual("plan_spec_creation", context["available_next_actions"][0]["id"])
            self.assertEqual("009", preflight["no_active_spec_context"]["next_available_spec_number"])

    def test_unusable_allocation_does_not_advertise_creation_action(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "docs/platform/specs/004-current").mkdir(parents=True)
            central = repo / "docs/history"
            central.mkdir(parents=True)
            (central / "spec-archive-index.md").write_text(
                "# Archive\n\n## Entries\n\n| Spec ID | Package path | Status |\n|---|---|---|\n"
                "| 006-old | `docs/platform/specs/006-old/` | removed |\n",
                encoding="utf-8",
            )

            scan = core.scan_specs(repo, "docs/platform")

            self.assertEqual([], scan["available_next_actions"])
            self.assertEqual("low", scan["spec_id_allocation"]["confidence"])

    def test_cli_inventory_matches_core_and_attaches_cli_provenance(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "docs/specs/003-current").mkdir(parents=True)
            expected = core.spec_id_inventory(repo)

            completed = subprocess.run(
                [sys.executable, str(SCRIPT), "spec-id-inventory", str(repo)],
                check=True,
                capture_output=True,
                text=True,
            )

            payload = json.loads(completed.stdout)
            metadata = payload.pop("lifecycle_metadata")
            self.assertEqual(core.relativize_payload_paths(expected, repo), payload)
            self.assertEqual("cli", metadata["invocation_surface"])
            self.assertEqual("argument", metadata["root_source"])
            self.assertNotIn(str(repo), completed.stdout)

    def test_cli_creation_plan_supports_expected_fingerprint_and_invalid_slug(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            first = subprocess.run(
                [sys.executable, str(SCRIPT), "spec-creation-plan", "feature", "--repo-root", str(repo)],
                check=True,
                capture_output=True,
                text=True,
            )
            first_payload = json.loads(first.stdout)
            fingerprint = first_payload["evidence_fingerprint"]
            self.assertEqual([], sorted(repo.rglob("*")))
            (repo / "docs/specs/000-claimed").mkdir(parents=True)
            before = sorted(path.relative_to(repo).as_posix() for path in repo.rglob("*"))
            stale = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "spec-creation-plan",
                    "feature",
                    "--repo-root",
                    str(repo),
                    "--expected-fingerprint",
                    fingerprint,
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            invalid = subprocess.run(
                [sys.executable, str(SCRIPT), "spec-creation-plan", "../bad", "--repo-root", str(repo)],
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertEqual("stale", json.loads(stale.stdout)["status"])
            self.assertEqual("invalid", json.loads(invalid.stdout)["status"])
            self.assertNotIn(str(repo), stale.stdout)
            self.assertEqual(before, sorted(path.relative_to(repo).as_posix() for path in repo.rglob("*")))


if __name__ == "__main__":
    unittest.main()
