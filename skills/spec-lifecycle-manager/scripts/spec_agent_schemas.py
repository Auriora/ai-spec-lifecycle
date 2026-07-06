"""Schema helpers for spec lifecycle agent-backed tools."""

from __future__ import annotations

from typing import Any


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
        "required": ["status", "server", "client", "dynamic_tools", "available_next_actions"],
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
