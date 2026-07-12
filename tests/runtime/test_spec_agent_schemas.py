import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = ROOT / "skills/spec-lifecycle-manager/scripts"
sys.path.insert(0, str(SCRIPT_DIR))

import spec_agent_schemas

try:
    import jsonschema
except ImportError:  # The runtime remains standard-library-only.
    jsonschema = None


def metadata() -> dict[str, object]:
    return {
        "schema_version": "1",
        "package_version": "0.3.0",
        "build_identity": "unknown",
        "invocation_surface": "mcp",
        "composition_sources": [],
        "repo_root": ".",
        "repo_identity": "unknown",
        "root_source": "argument",
        "fallback_reason": "none",
    }


def compact_fixture() -> dict[str, object]:
    return {
        "detail": "compact",
        "schema_version": "1",
        "decision": {"ready": False},
        "findings": [{"code": "BLOCKED"}],
        "next_actions": [{"action": "resolve blocker"}],
        "limits": {
            "findings": {"returned": 1, "total": 1, "limit": 20, "truncated": False},
            "next_actions": {"returned": 1, "total": 1, "limit": 10, "truncated": False},
            "payload_target_bytes": 32768,
            "limit_exceeded": False,
        },
        "evidence_fingerprint": "sha256:" + "a" * 64,
        "expansion": {
            "tool": "phase_gate_check",
            "arguments": {"detail": "full", "evidence_fingerprint": "sha256:" + "a" * 64},
        },
        "lifecycle_metadata": metadata(),
    }


@unittest.skipIf(jsonschema is None, "jsonschema is optional and not a runtime dependency")
class CompactSchemaValidationTests(unittest.TestCase):
    def assert_valid(self, instance: object, schema: dict[str, object]) -> None:
        jsonschema.Draft202012Validator.check_schema(schema)
        jsonschema.validate(instance, schema)

    def assert_invalid(self, instance: object, schema: dict[str, object]) -> None:
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(instance, schema)

    def test_detail_selector_accepts_all_modes(self):
        schema = spec_agent_schemas.detail_selector_schema()
        for fixture in (
            {},
            {"detail": "compact"},
            {"detail": "full"},
            {"detail": "section", "section": "blockers"},
        ):
            with self.subTest(fixture=fixture):
                self.assert_valid(fixture, schema)

    def test_detail_selector_rejects_invalid_or_misplaced_section(self):
        schema = spec_agent_schemas.detail_selector_schema()
        for fixture in (
            {"detail": "verbose"},
            {"detail": "section"},
            {"detail": "compact", "section": "blockers"},
            {"detail": "full", "section": "blockers"},
        ):
            with self.subTest(fixture=fixture):
                self.assert_invalid(fixture, schema)

    def test_compact_envelope_and_stale_response_are_valid(self):
        self.assert_valid(compact_fixture(), spec_agent_schemas.compact_aggregate_envelope_schema())
        stale = {
            "status": "stale",
            "schema_version": "1",
            "requested_fingerprint": "sha256:" + "a" * 64,
            "current_evidence_fingerprint": "sha256:" + "b" * 64,
            "expansion": {"tool": "phase_gate_check", "arguments": {"detail": "full"}},
            "lifecycle_metadata": metadata(),
        }
        self.assert_valid(stale, spec_agent_schemas.stale_expansion_response_schema())

    def test_compact_envelope_rejects_malformed_fingerprint_and_bounds(self):
        schema = spec_agent_schemas.compact_aggregate_envelope_schema()
        malformed = copy.deepcopy(compact_fixture())
        malformed["evidence_fingerprint"] = "sha256:ABC"
        self.assert_invalid(malformed, schema)

        too_many_findings = copy.deepcopy(compact_fixture())
        too_many_findings["findings"] = [{} for _ in range(21)]
        self.assert_invalid(too_many_findings, schema)

        too_many_actions = copy.deepcopy(compact_fixture())
        too_many_actions["next_actions"] = [{} for _ in range(11)]
        self.assert_invalid(too_many_actions, schema)

    def test_compact_envelope_rejects_invalid_metadata(self):
        fixture = copy.deepcopy(compact_fixture())
        fixture["lifecycle_metadata"]["invocation_surface"] = "internal"
        self.assert_invalid(fixture, spec_agent_schemas.compact_aggregate_envelope_schema())


class CompactSchemaStructureTests(unittest.TestCase):
    def test_fragments_publish_closed_contracts_without_mutating_metadata(self):
        metadata_schema = spec_agent_schemas.lifecycle_metadata_schema()
        envelope = spec_agent_schemas.compact_aggregate_envelope_schema()
        stale = spec_agent_schemas.stale_expansion_response_schema()

        self.assertEqual(20, envelope["properties"]["findings"]["maxItems"])
        self.assertEqual(10, envelope["properties"]["next_actions"]["maxItems"])
        self.assertEqual(
            "^sha256:[0-9a-f]{64}$",
            envelope["properties"]["evidence_fingerprint"]["pattern"],
        )
        self.assertEqual(metadata_schema, envelope["properties"]["lifecycle_metadata"])
        self.assertEqual(metadata_schema, stale["properties"]["lifecycle_metadata"])
        self.assertFalse(envelope["additionalProperties"])
        self.assertFalse(stale["additionalProperties"])


if __name__ == "__main__":
    unittest.main()
