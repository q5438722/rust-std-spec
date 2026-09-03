#!/usr/bin/env python3
"""Target-specific entry point for core::slice::sort_unstable_by_key."""

from __future__ import annotations

from typing import Any

import unstable_sort_companions as shared


TARGET = "core::slice::sort_unstable_by_key"
INPUT_ORDER = "82"
ARTIFACT_ID = "082_core_slice_sort_unstable_by_key"
ACTIVE_CONTRACT_SHA256 = (
    "019252db65344fd8830ffbbd90d127355a93541c6fbfab3fde3e6b3abe16e8ae"
)
ACTIVE_CONTRACT_TEXT = (
    "pub assume_specification<T, K: core::cmp::Ord, F: "
    "core::ops::FnMut(&T) -> K>[ <[T]>::sort_unstable_by_key::<K, F> ]( "
    "slice: &mut [T], f: F, ) ensures slice_permutation(old(slice)@, "
    "final(slice)@), slice_sorted_by_key::<F, T, K>(final(slice)@, f), ;"
)
EXCLUDED_RETAINED_TRUST_SITES = (
    "TS-082-D002",
    "TS-082-D003",
    "TS-082-E001",
)
ALL_AUDITED_TRUST_SITES = (
    "TS-082-D001",
    "TS-082-D002",
    "TS-082-D003",
    "TS-082-D004",
    "TS-082-C001",
    "TS-082-E001",
)
CONFIG = shared.TargetConfig(
    target=TARGET,
    input_order=INPUT_ORDER,
    artifact_id=ARTIFACT_ID,
    active_contract_sha256=ACTIVE_CONTRACT_SHA256,
    active_contract_text=ACTIVE_CONTRACT_TEXT,
    mode="key",
    target_source_citation="core/src/slice/mod.rs:3240-3246",
    public_docs_citation="core/src/slice/mod.rs:3195-3237",
    admitted_trust_site_id="TS-082-D004",
    excluded_retained_trust_site_ids=EXCLUDED_RETAINED_TRUST_SITES,
    all_audited_trust_site_ids=ALL_AUDITED_TRUST_SITES,
    proof_filename="proofs/082_core_slice_sort_unstable_by_key.rs",
    verus_expected_summary="verification results:: 3 verified, 0 errors",
)
PRIMARY = shared.PRIMARY
BOUNDED_SANITY = shared.BOUNDED_SANITY
EXACT_FINAL_SLICE = shared.EXACT_FINAL_SLICE
PURPOSES = shared.PURPOSES


def obligation_text(purpose: str) -> str:
    return shared.obligation_text(CONFIG, purpose)


def obligation_metadata(purpose: str) -> dict[str, Any]:
    return shared.obligation_metadata(CONFIG, purpose)


def obligation(purpose: str) -> tuple[str, dict[str, Any]]:
    return shared.obligation(CONFIG, purpose)


def validate_target_obligation(text: str, metadata: dict[str, Any]) -> None:
    shared.validate_target_obligation(CONFIG, text, metadata)


def fixed_exact_model_text() -> str:
    return shared.fixed_exact_model_text(CONFIG)


def equivalence_probe_text(*, positive: bool) -> str:
    return shared.equivalence_probe_text(CONFIG, positive=positive)


def boundary_manifest() -> dict[str, Any]:
    return shared.boundary_manifest(CONFIG)


def witness_payload() -> dict[str, Any]:
    return shared.witness_payload(CONFIG)
