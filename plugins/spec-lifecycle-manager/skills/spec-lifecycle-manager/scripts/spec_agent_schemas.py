"""Schema helpers for spec lifecycle agent-backed tools."""

from __future__ import annotations

from typing import Any


def detail_selector_schema() -> dict[str, Any]:
    """Input fragment for the v1 compact/full/section detail contract."""

    return {
        "type": "object",
        "properties": {
            "detail": {
                "type": "string",
                "enum": ["compact", "full", "section"],
                "default": "compact",
            },
            "section": {"type": "string", "minLength": 1},
        },
        "allOf": [
            {
                "if": {
                    "required": ["detail"],
                    "properties": {"detail": {"const": "section"}},
                },
                "then": {"required": ["section"]},
                "else": {"not": {"required": ["section"]}},
            }
        ],
        "additionalProperties": False,
    }


def evidence_fingerprint_schema() -> dict[str, Any]:
    """Fingerprint produced from canonical, decision-relevant evidence."""

    return {"type": "string", "pattern": "^sha256:[0-9a-f]{64}$"}


def expansion_follow_up_schema() -> dict[str, Any]:
    """Deterministic same-tool follow-up call for omitted current detail."""

    return {
        "type": "object",
        "required": ["tool", "arguments"],
        "properties": {
            "tool": {"type": "string", "minLength": 1},
            "arguments": {"type": "object"},
        },
        "additionalProperties": False,
    }


def compact_limit_state_schema() -> dict[str, Any]:
    """Explicit truncation and size-target state for a compact result."""

    def counter(limit: int) -> dict[str, Any]:
        return {
            "type": "object",
            "required": ["returned", "total", "limit", "truncated"],
            "properties": {
                "returned": {"type": "integer", "minimum": 0, "maximum": limit},
                "total": {"type": "integer", "minimum": 0},
                "limit": {"type": "integer", "const": limit},
                "truncated": {"type": "boolean"},
            },
            "additionalProperties": False,
        }

    return {
        "type": "object",
        "required": ["findings", "next_actions", "payload_target_bytes", "limit_exceeded"],
        "properties": {
            "findings": counter(20),
            "next_actions": counter(10),
            "payload_target_bytes": {"type": "integer", "const": 32768},
            "limit_exceeded": {"type": "boolean"},
        },
        "additionalProperties": False,
    }


def lifecycle_metadata_schema() -> dict[str, Any]:
    """Reusable v1 provenance schema for additive adapter metadata."""

    return {
        "type": "object",
        "required": [
            "schema_version",
            "package_version",
            "build_identity",
            "invocation_surface",
            "composition_sources",
            "repo_root",
            "repo_identity",
            "root_source",
            "fallback_reason",
        ],
        "properties": {
            "schema_version": {"type": "string", "const": "1"},
            "package_version": {"type": "string"},
            "build_identity": {"type": "string"},
            "invocation_surface": {
                "type": "string",
                "enum": ["mcp", "cli", "hook", "prompt", "unknown"],
            },
            "composition_sources": {
                "type": "array",
                "maxItems": 20,
                "items": {"type": "string"},
            },
            "repo_root": {"type": "string", "const": "."},
            "repo_identity": {
                "type": "string",
                "pattern": "^(unknown|sha256:[0-9a-f]{64})$",
            },
            "root_source": {
                "type": "string",
                "enum": ["argument", "environment", "cwd", "unknown"],
            },
            "fallback_reason": {
                "type": "string",
                "enum": [
                    "ci",
                    "package_validation",
                    "hook_execution",
                    "mcp_debugging",
                    "mcp_unavailable",
                    "explicit_recovery",
                    "other",
                    "none",
                ],
            },
        },
        "additionalProperties": False,
    }


def compact_aggregate_envelope_schema() -> dict[str, Any]:
    """Reusable output schema for new aggregate tools in compact mode."""

    return {
        "type": "object",
        "required": [
            "detail",
            "schema_version",
            "decision",
            "findings",
            "next_actions",
            "limits",
            "evidence_fingerprint",
            "expansion",
            "lifecycle_metadata",
        ],
        "properties": {
            "detail": {"type": "string", "const": "compact"},
            "schema_version": {"type": "string", "const": "1"},
            "decision": {"type": "object"},
            "findings": {
                "type": "array",
                "maxItems": 20,
                "items": {"type": "object"},
            },
            "next_actions": {
                "type": "array",
                "maxItems": 10,
                "items": {"type": "object"},
            },
            "limits": compact_limit_state_schema(),
            "evidence_fingerprint": evidence_fingerprint_schema(),
            "expansion": expansion_follow_up_schema(),
            "lifecycle_metadata": lifecycle_metadata_schema(),
        },
        "additionalProperties": False,
    }


def stale_expansion_response_schema() -> dict[str, Any]:
    """Response returned when requested evidence no longer matches the repo."""

    return {
        "type": "object",
        "required": [
            "status",
            "schema_version",
            "requested_fingerprint",
            "current_evidence_fingerprint",
            "expansion",
            "lifecycle_metadata",
        ],
        "properties": {
            "status": {"type": "string", "const": "stale"},
            "schema_version": {"type": "string", "const": "1"},
            "requested_fingerprint": evidence_fingerprint_schema(),
            "current_evidence_fingerprint": evidence_fingerprint_schema(),
            "expansion": expansion_follow_up_schema(),
            "lifecycle_metadata": lifecycle_metadata_schema(),
        },
        "additionalProperties": False,
    }


def phase_gate_check_output_schema() -> dict[str, Any]:
    """Closed output union for the phase-gate aggregate and stale expansion."""

    base_properties = {
        "schema_version": {"type": "string", "const": "1"},
        "decision": {"type": "object"},
        "evidence_fingerprint": evidence_fingerprint_schema(),
        "lifecycle_metadata": lifecycle_metadata_schema(),
    }
    compact = compact_aggregate_envelope_schema()
    full = {
        "type": "object",
        "required": [
            "detail", "schema_version", "decision", "evidence_fingerprint",
            "findings", "next_actions", "context", "lifecycle_metadata",
        ],
        "properties": {
            **base_properties,
            "detail": {"type": "string", "const": "full"},
            "findings": {"type": "array", "maxItems": 200, "items": {"type": "object"}},
            "next_actions": {"type": "array", "maxItems": 100, "items": {"type": "object"}},
            "context": {"type": "object"},
        },
        "additionalProperties": False,
    }
    section = {
        "type": "object",
        "required": [
            "detail", "schema_version", "decision", "evidence_fingerprint",
            "section", "content", "lifecycle_metadata",
        ],
        "properties": {
            **base_properties,
            "detail": {"type": "string", "const": "section"},
            "section": {
                "type": "string",
                "enum": ["source_signals", "coverage", "validation", "promotion", "closure"],
            },
            "content": {"type": "object"},
        },
        "additionalProperties": False,
    }
    return {"oneOf": [compact, full, section, stale_expansion_response_schema()]}


def spec_id_inventory_output_schema() -> dict[str, Any]:
    properties = {
        "schema_version": {"type": "string", "const": "1"},
        "numbering_scope": {"type": "object"},
        "used_numbers": {"type": "array", "items": {"type": "integer", "minimum": 0}},
        "highest_used_number": {"type": ["integer", "null"], "minimum": 0},
        "next_available_spec_number": {"type": "string", "pattern": "^[0-9]{3,}$"},
        "provisional": {"type": "boolean", "const": True},
        "confidence": {"type": "string", "enum": ["high", "reduced", "low"]},
        "legacy_upper_bound": {"type": ["integer", "null"], "minimum": 0},
        "evidence": {"type": "array", "items": {"type": "object"}},
        "diagnostics": {"type": "array", "items": {"type": "object"}},
        "summary": {"type": "object"},
        "lifecycle_metadata": lifecycle_metadata_schema(),
    }
    return {
        "type": "object",
        "required": list(properties),
        "properties": properties,
        "additionalProperties": False,
    }


def spec_creation_plan_output_schema() -> dict[str, Any]:
    base = {
        "schema_version": {"type": "string", "const": "1"},
        "decision": {"type": "object"},
        "evidence_fingerprint": evidence_fingerprint_schema(),
        "lifecycle_metadata": lifecycle_metadata_schema(),
    }
    full = {
        "type": "object",
        "required": ["detail", *base, "plan"],
        "properties": {**base, "detail": {"type": "string", "const": "full"}, "plan": {"type": "object"}},
        "additionalProperties": False,
    }
    section = {
        "type": "object",
        "required": ["detail", *base, "section", "content"],
        "properties": {
            **base,
            "detail": {"type": "string", "const": "section"},
            "section": {"type": "string", "enum": ["numbering", "template", "validation"]},
            "content": {"type": "object"},
        },
        "additionalProperties": False,
    }
    return {"oneOf": [compact_aggregate_envelope_schema(), full, section, stale_expansion_response_schema()]}


def review_packet_output_schema() -> dict[str, Any]:
    return {
        "review_type": "string",
        "summary": "string",
        "findings": [
            {
                "severity": "error|warn|info",
                "artifact": "string",
                "reference": "string",
                "finding": "string",
                "recommendation": "string",
            }
        ],
        "confidence": "low|medium|high",
        "blind_spots": ["string"],
    }


def review_result_disposition_template(review_type: str) -> dict[str, Any]:
    return {
        "review_type": review_type,
        "summary": "",
        "findings": [],
        "confidence": "medium",
        "blind_spots": [],
        "disposition": {
            "accepted": [],
            "rejected": [],
            "deferred": [],
            "human_decision_required": [],
        },
    }


def agent_unavailable_result_schema() -> dict[str, Any]:
    return {
        "tool": "string",
        "advisory": "boolean",
        "status": "unavailable",
        "model_class": "disabled",
        "packet": {
            "packet_id": "string",
            "inputs": ["string"],
            "limits": {
                "writes_files": False,
                "runner": "disabled",
            },
        },
        "result": {
            "observed_facts": ["string"],
            "inferences": ["string"],
            "recommendations": ["string"],
            "gaps": [
                {
                    "code": "string",
                    "message": "string",
                }
            ],
            "confidence": "low|medium|high",
        },
        "diagnostics": [
            {
                "severity": "info|warn|error",
                "code": "string",
                "message": "string",
            }
        ],
        "summary": {
            "error": "integer",
            "warn": "integer",
            "info": "integer",
        },
    }


def lifecycle_capabilities_output_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "required": ["status", "server", "client", "dynamic_tools", "available_next_actions", "validation_or_recovery", "lifecycle_metadata"],
        "properties": {
            "status": {"type": "string"},
            "server": {
                "type": "object",
                "required": ["name", "version", "protocol_version", "capabilities"],
                "properties": {
                    "name": {"type": "string"},
                    "version": {"type": "string"},
                    "protocol_version": {"type": "string"},
                    "capabilities": {"type": "object"},
                },
            },
            "client": {"type": "object"},
            "dynamic_tools": {
                "type": "object",
                "required": ["server_support", "client_refresh_observed", "decision"],
                "properties": {
                    "server_support": {"type": "boolean"},
                    "client_refresh_observed": {"type": "string"},
                    "decision": {"type": "string"},
                },
            },
            "available_next_actions": {"type": "array", "items": {"type": "object"}},
            "validation_or_recovery": {
                "type": "object",
                "required": ["fallback_reason", "commands"],
                "properties": {
                    "fallback_reason": {"type": "string", "const": "mcp_unavailable"},
                    "commands": {"type": "array", "items": {"type": "object"}},
                },
                "additionalProperties": False,
            },
            "lifecycle_metadata": lifecycle_metadata_schema(),
        },
    }


def script_migration_inventory_output_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "required": ["status", "repo_root", "scripts", "migrated_scripts", "retained_scripts", "closure_blockers"],
        "properties": {
            "status": {"type": "string"},
            "repo_root": {"type": "string"},
            "scripts": {"type": "array", "items": {"type": "object"}},
            "migrated_scripts": {"type": "array", "items": {"type": "object"}},
            "retained_scripts": {"type": "array", "items": {"type": "object"}},
            "closure_blockers": {"type": "array", "items": {"type": "object"}},
        },
    }


def traceability_lookup_output_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "required": ["lookup", "traceability_row", "gaps"],
        "properties": {
            "lookup": {"type": "object"},
            "traceability_row": {"type": "object"},
            "requirements": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "title": {"type": "string"},
                        "priority": {
                            "anyOf": [
                                {"type": "string", "enum": ["must-have", "should-have", "could-have"]},
                                {"type": "null"},
                            ]
                        },
                        "acceptance_criteria": {"type": "array", "items": {"type": "object"}},
                    },
                },
            },
            "design_sections": {"type": "array", "items": {"type": "string"}},
            "durable_targets": {"type": "array", "items": {"type": "string"}},
            "gaps": {"type": "array", "items": {"type": "object"}},
        },
    }
