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
