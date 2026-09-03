#!/usr/bin/env python3
"""Target-specific interface for input order 19, as_mut_ptr."""

from __future__ import annotations

from typing import Any

import pointer_cast_cluster as cluster


CONFIG = cluster.TARGET_019
TARGET = CONFIG.target
INPUT_ORDER = CONFIG.input_order
ARTIFACT_ID = CONFIG.artifact_id
ACTIVE_CONTRACT_SHA256 = CONFIG.active_contract_sha256
ACTIVE_CONTRACT_TEXT = CONFIG.active_contract_text
PRIMARY = cluster.PRIMARY
EXACT_OUTPUT = cluster.EXACT_OUTPUT
PURPOSES = cluster.PURPOSES
ALL_AUDITED_TRUST_SITES = CONFIG.all_audited_trust_sites
EXCLUDED_RETAINED_TRUST_SITES = CONFIG.excluded_retained_trust_sites
CANONICAL_SOURCE_BINDINGS = CONFIG.canonical_sources
PROBE_CASES = cluster.probe_cases(CONFIG)
PROBE_EXPECTED_RESULTS = {
    name: case["expected_solver_result"] for name, case in PROBE_CASES.items()
}


def obligation_text(purpose: str) -> str:
    return cluster.obligation_text(CONFIG, purpose)


def obligation_metadata(purpose: str) -> dict[str, Any]:
    return cluster.obligation_metadata(CONFIG, purpose)


def obligation(purpose: str) -> tuple[str, dict[str, Any]]:
    return cluster.obligation(CONFIG, purpose)


def validate_target_obligation(text: str, metadata: dict[str, Any]) -> None:
    cluster.validate_target_obligation(CONFIG, text, metadata)


def probe_text(name: str) -> str:
    return cluster.probe_text(CONFIG, name)


def boundary_manifest() -> dict[str, Any]:
    return cluster.boundary_manifest(CONFIG)
