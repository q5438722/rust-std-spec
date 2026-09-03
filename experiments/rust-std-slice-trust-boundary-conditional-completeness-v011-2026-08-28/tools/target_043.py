#!/usr/bin/env python3
"""Target-specific facade for core::slice::fill."""

from __future__ import annotations

from typing import Any

import clone_effect_cluster as cluster


CONFIG = cluster.TARGET_043
TARGET = CONFIG.target
INPUT_ORDER = CONFIG.input_order
ARTIFACT_ID = CONFIG.artifact_id
ACTIVE_CONTRACT_SHA256 = CONFIG.active_contract_sha256
ACTIVE_CONTRACT_TEXT = CONFIG.active_contract_text
PRIMARY = cluster.PRIMARY
EXACT_OUTPUT = cluster.EXACT_OUTPUT
PURPOSES = cluster.PURPOSES
SOURCE_CASES = cluster.SOURCE_CASES[ARTIFACT_ID]


def obligation(purpose: str) -> tuple[str, dict[str, Any]]:
    return cluster.obligation(CONFIG, purpose)


def obligation_text(purpose: str) -> str:
    return cluster.obligation_text(CONFIG, purpose)


def obligation_metadata(purpose: str) -> dict[str, Any]:
    return cluster.obligation_metadata(CONFIG, purpose)


def validate_target_obligation(text: str, metadata: dict[str, Any]) -> None:
    cluster.validate_target_obligation(CONFIG, text, metadata)


def panic_obligation_text() -> str:
    return cluster.panic_obligation_text(CONFIG)


def boundary_manifest() -> dict[str, Any]:
    return cluster.boundary_manifest(CONFIG)


def verus_text() -> str:
    return cluster.verus_text(CONFIG)
