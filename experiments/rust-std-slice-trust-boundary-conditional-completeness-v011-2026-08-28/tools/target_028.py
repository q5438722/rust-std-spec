#!/usr/bin/env python3
"""Target-specific interface for input order 28, binary_search."""

from __future__ import annotations

from typing import Any

import search_family as family


CONFIG = family.TARGET_028
TARGET = CONFIG.target
INPUT_ORDER = CONFIG.input_order
ARTIFACT_ID = CONFIG.artifact_id
ACTIVE_CONTRACT_SHA256 = CONFIG.active_contract_sha256
ACTIVE_CONTRACT_TEXT = CONFIG.active_contract_text
PRIMARY = family.PRIMARY
SANITY = CONFIG.sanity_purpose
EXACT_OUTPUT = family.EXACT_OUTPUT
PURPOSES = CONFIG.purposes
ALL_AUDITED_TRUST_SITES = CONFIG.all_audited_trust_sites
EXCLUDED_RETAINED_TRUST_SITES = CONFIG.excluded_retained_trust_sites
VERUS_EXPECTED_SUMMARY = CONFIG.verus_expected_summary


def obligation_text(purpose: str) -> str:
    return family.obligation_text(CONFIG, purpose)


def obligation_metadata(purpose: str) -> dict[str, Any]:
    return family.obligation_metadata(CONFIG, purpose)


def obligation(purpose: str) -> tuple[str, dict[str, Any]]:
    return family.obligation(CONFIG, purpose)


def validate_target_obligation(text: str, metadata: dict[str, Any]) -> None:
    family.validate_target_obligation(CONFIG, text, metadata)


def fixed_model_text(purpose: str) -> str:
    return family.fixed_model_text(CONFIG, purpose)


def witness_payload() -> dict[str, Any]:
    return family.witness_payload(CONFIG)


def boundary_manifest() -> dict[str, Any]:
    return family.boundary_manifest(CONFIG)
