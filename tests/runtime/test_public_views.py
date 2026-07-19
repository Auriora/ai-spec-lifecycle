import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = ROOT / "skills/spec-lifecycle-manager/scripts"
FIXTURE = ROOT / "tests/fixtures/public-cli-contract.json"
sys.path.insert(0, str(SCRIPT_DIR))

from lifecycle import core
from lifecycle import public_views


def tree_fingerprint(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode())
        digest.update(path.read_bytes())
    return digest.hexdigest()


def task(task_id: str, marker: str, status: str, *, parent_id=None) -> dict:
    return {
        "task_id": task_id,
        "title": f"Summary for {task_id}",
        "marker": marker,
        "status": status,
        "depends_on": [],
        "parent_id": parent_id,
    }


class PublicContractTests(unittest.TestCase):
    def test_contract_fixture_freezes_public_identity_and_envelope(self):
        contract = json.loads(FIXTURE.read_text(encoding="utf-8"))
        self.assertEqual("slm", contract["public_executable"])
        self.assertEqual(["slm"], contract["package_bins"])
        self.assertEqual(list(public_views.PUBLIC_COMMANDS), contract["commands"])
        self.assertEqual(list(public_views.QUERY_COMMANDS), contract["query_commands"])
        self.assertEqual(list(public_views.ENVELOPE_FIELDS), contract["json_envelope_fields"])
        self.assertEqual(set(core.TASK_STATE_MARKERS), set(contract["task_states"]))
        self.assertEqual(public_views.OPEN_TASK_STATES, frozenset(contract["open_task_states"]))

    def test_command_view_has_stable_repo_relative_envelope(self):
        with tempfile.TemporaryDirectory() as temp:
            view = public_views.command_view("specs", Path(temp), [{"spec_id": "001-a"}], {"total": 1})
        self.assertEqual(list(public_views.ENVELOPE_FIELDS), list(view))
        self.assertEqual("1", view["schema_version"])
        self.assertEqual(".", view["repo_root"])


class TaskViewTests(unittest.TestCase):
    def setUp(self):
        self.repo = Path("/repo")
        self.spec = self.repo / "docs/specs/001-example"
        self.tasks = [
            task("T001", " ", "pending"),
            task("T002", "x", "complete"),
            task("T003", "~", "in_progress"),
            task("T004", "/", "partial"),
            task("T005", ">", "follow_up"),
            task("T006", "-", "no_op"),
            task("T007", "?", "review_needed"),
            task("T008", "!", "attention", parent_id="T007"),
        ]
        self.task_payload = {
            "summary": {"total": len(self.tasks)},
            "phases": [{"name": "Phase 1", "tasks": self.tasks}],
        }
        self.tables = {
            "Task To Context Matrix": [
                {"Task ID": item["task_id"], "Requirements": f"Requirement {index + 1}"}
                for index, item in enumerate(self.tasks)
            ]
        }

    def build(self, filters=None):
        with (
            mock.patch.object(public_views.core, "task_list", return_value=self.task_payload),
            mock.patch.object(public_views.traceability, "load_spec", return_value=({}, [], self.tables)),
        ):
            return public_views.build_tasks_view(self.repo, self.spec, filters=filters)

    def test_marker_states_are_projected_without_reinterpretation(self):
        view = self.build()
        self.assertEqual(
            [(item["marker"], item["status"]) for item in self.tasks],
            [(item["marker"], item["state"]) for item in view["records"]],
        )
        self.assertEqual(["Requirement 1"], view["records"][0]["requirements"])
        self.assertTrue(view["records"][-1]["is_subtask"])

    def test_compatible_filters_form_a_deduplicated_union(self):
        filters = public_views.TaskFilters(complete=True, pending=True, open=True, states=("complete", "attention"))
        records = self.build(filters)["records"]
        self.assertEqual(
            ["T001", "T002", "T003", "T004", "T007", "T008"],
            [item["task_id"] for item in records],
        )

    def test_pending_means_literal_pending_and_open_excludes_terminal_outcomes(self):
        self.assertEqual(["T001"], [item["task_id"] for item in self.build(public_views.TaskFilters(pending=True))["records"]])
        self.assertEqual(
            ["T001", "T003", "T004", "T007", "T008"],
            [item["task_id"] for item in self.build(public_views.TaskFilters(open=True))["records"]],
        )

    def test_next_is_exclusive_and_matches_shared_next_task(self):
        with self.assertRaisesRegex(public_views.PublicViewError, "exclusive"):
            self.build(public_views.TaskFilters(next_only=True, pending=True))
        with (
            mock.patch.object(public_views.core, "task_list", return_value=self.task_payload),
            mock.patch.object(public_views.core, "next_task", return_value={"selected": self.tasks[2]}),
            mock.patch.object(public_views.traceability, "load_spec", return_value=({}, [], self.tables)),
        ):
            view = public_views.build_tasks_view(self.repo, self.spec, filters=public_views.TaskFilters(next_only=True))
        self.assertEqual(["T003"], [item["task_id"] for item in view["records"]])

    def test_unknown_state_is_a_usage_error(self):
        with self.assertRaisesRegex(public_views.PublicViewError, "Unknown task state"):
            self.build(public_views.TaskFilters(states=("finished",)))


class SpecSelectionTests(unittest.TestCase):
    def test_shared_resolution_accepts_numeric_prefix_and_slug(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            spec = root / "docs/specs/039-slm-public-cli"
            spec.mkdir(parents=True)
            (spec / "requirements.md").write_text(
                "---\nstatus: draft\n---\n# Requirements\n",
                encoding="utf-8",
            )
            numeric = core.resolve_spec_reference(root, "039")
            slug = core.resolve_spec_reference(root, "slm-public-cli")
        self.assertEqual("active", numeric["status"])
        self.assertEqual("039-slm-public-cli", numeric["spec_id"])
        self.assertEqual("active", slug["status"])

    def test_exactly_one_active_spec_is_selected(self):
        scan = {"specs": [{"spec_id": "001-one", "path": "/repo/docs/specs/001-one", "lifecycle": "active"}]}
        with mock.patch.object(public_views.core, "scan_specs", return_value=scan):
            selected = public_views.select_active_spec(Path("/repo"))
        self.assertEqual(Path("/repo/docs/specs/001-one"), selected)

    def test_multiple_active_specs_are_reported_without_guessing(self):
        scan = {
            "specs": [
                {"spec_id": "002-two", "path": "/repo/docs/specs/002-two", "lifecycle": "active"},
                {"spec_id": "001-one", "path": "/repo/docs/specs/001-one", "lifecycle": "active"},
            ]
        }
        with mock.patch.object(public_views.core, "scan_specs", return_value=scan):
            with self.assertRaises(public_views.PublicViewError) as caught:
                public_views.select_active_spec(Path("/repo"))
        self.assertEqual("spec_ambiguous", caught.exception.code)
        self.assertEqual(["001-one", "002-two"], caught.exception.candidates)

    def test_explicit_historic_reference_is_distinguished(self):
        with mock.patch.object(
            public_views.core,
            "resolve_spec_reference",
            return_value={"status": "archived", "archive_matches": [{"spec_id": "001-old"}]},
        ):
            with self.assertRaises(public_views.PublicViewError) as caught:
                public_views.select_active_spec(Path("/repo"), "001")
        self.assertEqual("spec_historic", caught.exception.code)


class RequirementViewTests(unittest.TestCase):
    def write_spec(self, root: Path) -> Path:
        spec = root / "docs/specs/001-example"
        spec.mkdir(parents=True)
        (spec / "requirements.md").write_text(
            """# Requirements

### Requirement 1: Required behavior

**Priority:** must-have

#### Acceptance Criteria

1. It works.

### Requirement 2: Compatibility behavior

**Priority:** should

#### Acceptance Criteria

1. It is compatible.

### Requirement 3: Unprioritized behavior

#### Acceptance Criteria

1. It is visible.
""",
            encoding="utf-8",
        )
        (spec / "traceability.md").write_text(
            """# Traceability Matrix

## Requirement To Delivery Matrix

| Requirement | Tasks |
|-------------|-------|
| Requirement 1 | T001-T003 |
| Requirement 2 | T003 |
| Requirement 3 | none |
""",
            encoding="utf-8",
        )
        (spec / "tasks.md").write_text(
            "# Tasks\n\n- [ ] T001 One.\n- [ ] T002 Two.\n- [ ] T003 Three.\n",
            encoding="utf-8",
        )
        return spec

    def test_priorities_linked_tasks_and_parser_diagnostics_are_preserved(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            spec = self.write_spec(root)
            before = tree_fingerprint(root)
            view = public_views.build_requirements_view(root, spec)
            after = tree_fingerprint(root)
        self.assertEqual(["must-have", "unspecified", "unspecified"], [item["priority"] for item in view["records"]])
        self.assertEqual(["T001", "T002", "T003"], view["records"][0]["tasks"])
        self.assertEqual("Required behavior", view["records"][0]["title"])
        self.assertEqual("REQUIREMENT_PRIORITY_SHORTHAND", view["records"][1]["diagnostics"][0]["code"])
        self.assertEqual(before, after)

    def test_priority_and_missing_priority_filters_are_exclusive(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            spec = self.write_spec(root)
            filtered = public_views.build_requirements_view(
                root, spec, filters=public_views.RequirementFilters(priorities=("must-have",))
            )
            missing = public_views.build_requirements_view(
                root, spec, filters=public_views.RequirementFilters(missing_priority=True)
            )
            with self.assertRaisesRegex(public_views.PublicViewError, "exclusive"):
                public_views.build_requirements_view(
                    root,
                    spec,
                    filters=public_views.RequirementFilters(priorities=("must-have",), missing_priority=True),
                )
        self.assertEqual(["Requirement 1"], [item["requirement_id"] for item in filtered["records"]])
        self.assertEqual(["Requirement 2", "Requirement 3"], [item["requirement_id"] for item in missing["records"]])


class HistoryAndSpecsViewTests(unittest.TestCase):
    def test_specs_view_returns_a_successful_empty_result(self):
        with mock.patch.object(public_views.core, "scan_specs", return_value={"specs": []}):
            view = public_views.build_specs_view(Path("/repo"))
        self.assertEqual([], view["records"])
        self.assertEqual({"total": 0, "active": 0, "historic": 0, "empty": True}, view["summary"])

    def test_history_uses_durable_order_filters_union_and_limit(self):
        payload = {
            "entries": [
                {"spec_id": "001-a", "title": "A", "status": "retained", "closure_action": "archive", "package_path": "docs/specs/001-a", "final_spec_commit": "a", "cleanup_commit": "b"},
                {"spec_id": "002-b", "title": "B", "status": "removed", "closure_action": "remove", "package_path": "docs/specs/002-b", "final_spec_commit": "c", "cleanup_commit": "d"},
                {"spec_id": "003-c", "title": "C", "status": "superseded", "closure_action": "archive", "package_path": "docs/specs/003-c", "final_spec_commit": "e", "cleanup_commit": "f"},
            ],
            "diagnostics": [],
        }
        filters = public_views.HistoryFilters(archived=True, removed=True, limit=2)
        with mock.patch.object(public_views.core, "archive_index", return_value=payload):
            view = public_views.build_history_view(Path("/repo"), filters=filters)
        self.assertEqual(["001-a", "002-b"], [item["spec_id"] for item in view["records"]])
        self.assertEqual(["archived", "removed"], [item["disposition"] for item in view["records"]])

    def test_malformed_history_fails_closed_with_shared_diagnostics(self):
        payload = {"entries": [], "diagnostics": [{"severity": "error", "code": "ARCHIVE_BAD", "message": "bad row"}]}
        with mock.patch.object(public_views.core, "archive_index", return_value=payload):
            with self.assertRaises(public_views.PublicViewError) as caught:
                public_views.build_history_view(Path("/repo"))
        self.assertEqual("history_invalid", caught.exception.code)
        self.assertEqual("ARCHIVE_BAD", caught.exception.diagnostics[0]["code"])

    def test_specs_view_keeps_state_dimensions_separate_and_paths_relative(self):
        scan = {
            "specs": [
                {
                    "spec_id": "001-one",
                    "path": "/repo/docs/specs/001-one",
                    "status": "draft",
                    "lifecycle": "active",
                    "health": {"severity": "warn"},
                }
            ]
        }
        with (
            mock.patch.object(public_views.core, "scan_specs", return_value=scan),
            mock.patch.object(
                public_views.core,
                "parse_tasks",
                return_value=[SimpleNamespace(complete=True), SimpleNamespace(complete=False), SimpleNamespace(complete=False)],
            ),
            mock.patch.object(public_views.core, "next_task", return_value={"selected": {"task_id": "T002"}}),
            mock.patch.object(public_views.core, "spec_summary") as repeated_lint,
        ):
            view = public_views.build_specs_view(Path("/repo"))
        repeated_lint.assert_not_called()
        self.assertEqual(
            {
                "spec_id": "001-one",
                "path": "docs/specs/001-one",
                "status": "draft",
                "lifecycle": "active",
                "disposition": None,
                "health": "warn",
                "tasks_total": 3,
                "tasks_complete": 1,
                "next_task": "T002",
            },
            view["records"][0],
        )


if __name__ == "__main__":
    unittest.main()
