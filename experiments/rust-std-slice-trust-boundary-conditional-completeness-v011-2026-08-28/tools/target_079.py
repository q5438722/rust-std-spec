#!/usr/bin/env python3
"""Target 079 key-callback selection configuration."""

from __future__ import annotations

from typing import Any

import selection_callback_targets as shared


TARGET = "core::slice::select_nth_unstable_by_key"
INPUT_ORDER = "79"
ARTIFACT_ID = "079_core_slice_select_nth_unstable_by_key"
ACTIVE_CONTRACT_SHA256 = (
    "9366859a88badc5f8d8cdfb15fbc544ef81edb756429e14a887b1ce6c73e3e95"
)
ACTIVE_CONTRACT_TEXT = (
    "pub assume_specification<T, K: core::cmp::Ord, F: "
    "core::ops::FnMut(&T) -> K>[ "
    "<[T]>::select_nth_unstable_by_key::<K, F> ]( slice: &mut [T], "
    "index: usize, f: F, ) -> (ret: (&mut [T], &mut T, &mut [T])) "
    "requires index < old(slice)@.len(), ensures final(slice)@ == "
    "final(ret.0)@ + seq![*final(ret.1)] + final(ret.2)@, "
    "final(ret.0)@.len() == index, *final(ret.1) == "
    "final(slice)@[index as int], final(ret.2)@.len() == "
    "old(slice)@.len() - (index as int) - 1, "
    "slice_permutation(old(slice)@, final(slice)@), "
    "slice_select_partition_key::<F, T, K>(final(ret.0)@, "
    "*final(ret.1), final(ret.2)@, f), ;"
)
ADMITTED_TRUST_SITES = ("TS-079-D004",)
EXCLUDED_RETAINED_TRUST_SITES = (
    "TS-079-D002",
    "TS-079-D003",
    "TS-079-E001",
)
CONTEXT_ONLY_TRUST_SITES = ("TS-079-D001", "TS-079-C001")
ALL_AUDITED_TRUST_SITES = (
    "TS-079-D001",
    "TS-079-D002",
    "TS-079-D003",
    "TS-079-D004",
    "TS-079-C001",
    "TS-079-E001",
)
CONFIG = shared.TargetConfig(
    target=TARGET,
    input_order=INPUT_ORDER,
    artifact_id=ARTIFACT_ID,
    active_contract_sha256=ACTIVE_CONTRACT_SHA256,
    active_contract_text=ACTIVE_CONTRACT_TEXT,
    mode="key",
    target_source="core/src/slice/mod.rs:3648-3658",
    public_docs="core/src/slice/mod.rs:3592-3645",
    selection_source="core/src/slice/sort/select.rs:17-307",
    partition_source="core/src/slice/sort/unstable/quicksort.rs:93-137",
    small_sort_source=(
        "core/src/slice/sort/shared/smallsort.rs:295-309,542-607"
    ),
    vocabulary_source="specs/slice_shared_vocabulary.rs:316-379,590-610,778-788",
    admitted_trust_site="TS-079-D004",
    excluded_trust_sites=EXCLUDED_RETAINED_TRUST_SITES,
    context_only_trust_sites=CONTEXT_ONLY_TRUST_SITES,
    all_trust_sites=ALL_AUDITED_TRUST_SITES,
    replacement_id="RB-079-BOUNDED-KEY-ORD-SMALLSORT",
    proof_filename="proofs/079_core_slice_select_nth_unstable_by_key.rs",
    verus_expected_summary="verification results:: 5 verified, 0 errors",
)

PRIMARY = shared.PRIMARY
EXACT = shared.EXACT
PURPOSES = shared.PURPOSES
SOURCE_TRANSITIONS = shared.SOURCE_TRANSITIONS
ACTIVE_CONJUNCTS = shared.ACTIVE_CONJUNCTS


def obligation_text(purpose: str) -> str:
    return shared.obligation_text(CONFIG, purpose)


def obligation_metadata(purpose: str) -> dict[str, Any]:
    return shared.obligation_metadata(CONFIG, purpose)


def obligation(purpose: str) -> tuple[str, dict[str, Any]]:
    return shared.obligation(CONFIG, purpose)


def validate_target_obligation(
    text: str, metadata: dict[str, Any]
) -> None:
    shared.validate_target_obligation(CONFIG, text, metadata)


def boundary_manifest() -> dict[str, Any]:
    return shared.boundary_manifest(CONFIG)


def missing_source_phases() -> tuple[str, ...]:
    return shared.missing_source_phases(CONFIG)


def nonvacuity_text() -> str:
    return shared.nonvacuity_text(CONFIG)


def mixed_source_execution_text() -> str:
    return shared.mixed_source_execution_text(CONFIG)


def length_four_wrong_schedule_text() -> str:
    return shared.length_four_wrong_schedule_text(CONFIG)


def length_four_source_execution_text() -> str:
    return shared.length_four_source_execution_text(CONFIG)


def small_sort_regression_text(case: str) -> str:
    return shared.small_sort_regression_text(CONFIG, case)


def panic_after_shift_text(*, restored: bool) -> str:
    return shared.panic_after_shift_text(CONFIG, restored=restored)


def panic_probe_kinds() -> tuple[str, ...]:
    return shared.panic_probe_kinds(CONFIG)


def panic_probe_text(kind: str) -> str:
    return shared.panic_probe_text(CONFIG, kind)


def witness_payload() -> dict[str, Any]:
    return shared.witness_payload(CONFIG)
