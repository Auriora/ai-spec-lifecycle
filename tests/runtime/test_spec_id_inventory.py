import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = ROOT / "skills/spec-lifecycle-manager/scripts"
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


if __name__ == "__main__":
    unittest.main()
