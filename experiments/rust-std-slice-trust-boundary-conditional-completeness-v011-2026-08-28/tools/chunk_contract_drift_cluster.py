#!/usr/bin/env python3
"""Source-backed conditional-completeness models for five chunk-view targets."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Any

import campaign_common as common
from checker_guards import GuardError, parse_smt, validate_obligation


PRIMARY = "completeness-modulo-reviewed-equivalence"
EXACT_OUTPUT = "exact-output-determinism"
PURPOSES = (PRIMARY, EXACT_OUTPUT)

SLICE_SOURCE_PATH = "core/src/slice/mod.rs"
SLICE_SOURCE_SHA256 = (
    "58901fa6437dbd4d77c68427bbced0fc3a91a10fdb8bd2e233adf6a9ba27d2d5"
)
RAW_SOURCE_PATH = "core/src/slice/raw.rs"
RAW_SOURCE_SHA256 = (
    "0914968067f7e2bc798680c1edd72bcb032a9fd44ebb2b6fbc082a3a2b16941f"
)


@dataclass(frozen=True)
class ChunkTarget:
    target: str
    input_order: str
    artifact_id: str
    active_contract_sha256: str
    retained_contract_sha256: str
    kind: str
    mutable: bool
    source_item_span: tuple[int, int]
    docs_span: tuple[int, int]
    context_only_trust_sites: tuple[str, ...]
    admitted_trust_sites: tuple[str, ...]
    excluded_retained_trust_sites: tuple[str, ...]
    pointer_dependency: str
    lower_dependency: str | None

    @property
    def has_remainder(self) -> bool:
        return self.kind != "unchecked"

    @property
    def reverse(self) -> bool:
        return self.kind == "rchunks"

    @property
    def expected_results(self) -> dict[str, str]:
        return {
            "exact_output_determinism_status": "conditional-complete",
            "completeness_modulo_reviewed_equivalence_status": (
                "conditional-incomplete"
                if self.mutable
                else "conditional-complete"
            ),
        }

    @property
    def expected_solver_results(self) -> dict[str, str]:
        return {
            PRIMARY: "sat" if self.mutable else "unsat",
            EXACT_OUTPUT: "unsat",
        }


TARGET_014 = ChunkTarget(
    target="core::slice::as_chunks_unchecked",
    input_order="14",
    artifact_id="014_core_slice_as_chunks_unchecked",
    active_contract_sha256=(
        "a2a5116af11a32d4169f8b90ce1a319e948a4705e36b8a2c171f6a8191655b66"
    ),
    retained_contract_sha256=(
        "0d342b93267baa83df2dd43ffee6dcc76c257cf313c3f7d6a0c76f7bd309eab1"
    ),
    kind="unchecked",
    mutable=False,
    source_item_span=(1338, 1349),
    docs_span=(1295, 1332),
    context_only_trust_sites=(
        "TS-014-D001",
        "TS-014-D004",
        "TS-014-C001",
        "TS-014-C002",
        "TS-014-C003",
    ),
    admitted_trust_sites=("TS-014-D003",),
    excluded_retained_trust_sites=(
        "TS-014-D002",
        "TS-014-D005",
        "TS-014-D006",
        "TS-014-E001",
        "TS-014-E002",
    ),
    pointer_dependency="021_core_slice_as_ptr",
    lower_dependency=None,
)

TARGET_015 = ChunkTarget(
    target="core::slice::as_chunks_unchecked_mut",
    input_order="15",
    artifact_id="015_core_slice_as_chunks_unchecked_mut",
    active_contract_sha256=(
        "c7cdf29658c01698013e14c2ab14e93699f855167a15eb4e3d697742a7d40c9a"
    ),
    retained_contract_sha256=(
        "7cd825e6f6de9150b8a4e29d505fd432ddcb44e1add7c2053c43317a3dcacb0f"
    ),
    kind="unchecked",
    mutable=True,
    source_item_span=(1498, 1509),
    docs_span=(1453, 1492),
    context_only_trust_sites=(
        "TS-015-D001",
        "TS-015-D004",
        "TS-015-C001",
        "TS-015-C002",
        "TS-015-C003",
    ),
    admitted_trust_sites=("TS-015-D003",),
    excluded_retained_trust_sites=(
        "TS-015-D002",
        "TS-015-D005",
        "TS-015-D006",
        "TS-015-E001",
        "TS-015-E002",
    ),
    pointer_dependency="019_core_slice_as_mut_ptr",
    lower_dependency=None,
)

TARGET_012 = ChunkTarget(
    target="core::slice::as_chunks",
    input_order="12",
    artifact_id="012_core_slice_as_chunks",
    active_contract_sha256=(
        "9d7c778009f44f0fd043dfc0e22215c99b3c90dde9ed5434c911087402bbe05f"
    ),
    retained_contract_sha256=(
        "3b57534adcd1c2d3cf18052a45f2e11ea9dfc2889dcef6ab4586a35bc8501ef9"
    ),
    kind="chunks",
    mutable=False,
    source_item_span=(1396, 1406),
    docs_span=(1351, 1390),
    context_only_trust_sites=(
        "TS-012-D001",
        "TS-012-D004",
        "TS-012-C001",
        "TS-012-C002",
        "TS-012-C003",
    ),
    admitted_trust_sites=("TS-012-D002",),
    excluded_retained_trust_sites=(
        "TS-012-D003",
        "TS-012-E001",
        "TS-012-E002",
        "TS-012-E003",
    ),
    pointer_dependency="021_core_slice_as_ptr",
    lower_dependency=TARGET_014.artifact_id,
)

TARGET_023 = ChunkTarget(
    target="core::slice::as_rchunks",
    input_order="23",
    artifact_id="023_core_slice_as_rchunks",
    active_contract_sha256=(
        "1b3b024fdbd8f22771d68cefc3082062544ac60b7d7ac07fda1c14cab04ab3ca"
    ),
    retained_contract_sha256=(
        "e2267d28d210517821bbafb80115b79374ff4925b5096b1b27fb466f399a2cec"
    ),
    kind="rchunks",
    mutable=False,
    source_item_span=(1443, 1451),
    docs_span=(1408, 1437),
    context_only_trust_sites=("TS-023-D001", "TS-023-D004"),
    admitted_trust_sites=("TS-023-D002",),
    excluded_retained_trust_sites=("TS-023-D003", "TS-023-E001"),
    pointer_dependency="021_core_slice_as_ptr",
    lower_dependency=TARGET_014.artifact_id,
)

TARGET_024 = ChunkTarget(
    target="core::slice::as_rchunks_mut",
    input_order="24",
    artifact_id="024_core_slice_as_rchunks_mut",
    active_contract_sha256=(
        "f7f4347b6b668b99b56a86daa936797fae5b45f6ffc22dbacc872c1be89b2dde"
    ),
    retained_contract_sha256=(
        "2eb4482ca836049f0db386dc97308eeb2e7376ffde6abdd110f3691e11c6cf69"
    ),
    kind="rchunks",
    mutable=True,
    source_item_span=(1605, 1613),
    docs_span=(1564, 1599),
    context_only_trust_sites=("TS-024-D001", "TS-024-D004"),
    admitted_trust_sites=("TS-024-D002",),
    excluded_retained_trust_sites=("TS-024-D003", "TS-024-E001"),
    pointer_dependency="019_core_slice_as_mut_ptr",
    lower_dependency=TARGET_015.artifact_id,
)

ORDERED_TARGETS = (
    TARGET_014,
    TARGET_015,
    TARGET_012,
    TARGET_023,
    TARGET_024,
)
TARGET_BY_ORDER = {target.input_order: target for target in ORDERED_TARGETS}


def _datatype(
    name: str,
    constructor: str,
    fields: tuple[tuple[str, str], ...],
) -> str:
    declarations = "\n".join(
        f"      ({selector} {sort})" for selector, sort in fields
    )
    return (
        f"(declare-datatypes (({name} 0))\n"
        f"  ((({constructor}\n{declarations}))))"
    )


def _input_fields(config: ChunkTarget) -> tuple[tuple[str, str], ...]:
    fields = (
        ("x_sequence", "Int"),
        ("x_length", "Int"),
        ("x_chunk_size", "Int"),
        ("x_allocation", "Int"),
        ("x_address", "Int"),
        ("x_provenance", "Int"),
        ("x_element_size", "Int"),
        ("x_element_alignment", "Int"),
        ("x_allocation_base", "Int"),
        ("x_allocation_bytes", "Int"),
        ("x_one_allocation", "Bool"),
        ("x_initialized", "Bool"),
        ("x_isize_max", "Int"),
        ("x_address_space_limit", "Int"),
        ("x_borrow_identity", "Int"),
    )
    if config.mutable:
        fields += (
            ("x_writable", "Bool"),
            ("x_exclusive_access", "Bool"),
            ("x_frame_token", "Int"),
        )
    return fields


def _boundary_field_specs(
    config: ChunkTarget,
) -> tuple[tuple[str, str, str], ...]:
    fields = (
        ("b_input_allocation", "Int", "input_memory"),
        ("b_input_address", "Int", "input_memory"),
        ("b_input_provenance", "Int", "input_provenance"),
        ("b_element_size", "Int", "input_layout"),
        ("b_element_alignment", "Int", "input_layout"),
        ("b_allocation_base", "Int", "input_memory"),
        ("b_allocation_bytes", "Int", "input_memory"),
        ("b_one_allocation", "Bool", "input_memory"),
        ("b_initialized", "Bool", "input_initialization"),
        ("b_isize_max", "Int", "input_layout"),
        ("b_address_space_limit", "Int", "input_layout"),
        ("b_borrow_identity", "Int", "input_provenance"),
    )
    if config.mutable:
        fields += (
            ("b_writable", "Bool", "input_memory"),
            ("b_exclusive_access", "Bool", "input_provenance"),
            ("b_frame_token", "Int", "input_memory"),
        )
    return fields


def _output_fields(config: ChunkTarget) -> tuple[tuple[str, str], ...]:
    fields = (
        ("y_chunks_ref", "Reference"),
        ("y_chunks_len", "Int"),
        ("y_chunks_source", "Int"),
        ("y_chunks_start", "Int"),
        ("y_chunks_width", "Int"),
    )
    if config.has_remainder:
        fields += (
            ("y_remainder_ref", "Reference"),
            ("y_remainder_len", "Int"),
            ("y_remainder_source", "Int"),
            ("y_remainder_start", "Int"),
        )
    return fields


def _state_fields(config: ChunkTarget) -> tuple[tuple[str, str], ...]:
    fields = (
        ("s_final_sequence", "Int"),
        ("s_final_slice_len", "Int"),
        ("s_final_allocation", "Int"),
        ("s_final_address", "Int"),
        ("s_final_provenance", "Int"),
        ("s_final_borrow_identity", "Int"),
        ("s_final_one_allocation", "Bool"),
        ("s_final_initialized", "Bool"),
    )
    if config.mutable:
        fields += (
            ("s_final_writable", "Bool"),
            ("s_final_exclusive_access", "Bool"),
            ("s_final_frame_token", "Int"),
            ("s_final_chunks_len", "Int"),
            ("s_final_chunks_source", "Int"),
            ("s_final_chunks_start", "Int"),
            ("s_final_chunks_width", "Int"),
        )
        if config.has_remainder:
            fields += (
                ("s_final_remainder_len", "Int"),
                ("s_final_remainder_source", "Int"),
                ("s_final_remainder_start", "Int"),
            )
    return fields


def _observed_equalities(config: ChunkTarget) -> list[str]:
    mapping = (
        ("b_input_allocation", "x_allocation"),
        ("b_input_address", "x_address"),
        ("b_input_provenance", "x_provenance"),
        ("b_element_size", "x_element_size"),
        ("b_element_alignment", "x_element_alignment"),
        ("b_allocation_base", "x_allocation_base"),
        ("b_allocation_bytes", "x_allocation_bytes"),
        ("b_one_allocation", "x_one_allocation"),
        ("b_initialized", "x_initialized"),
        ("b_isize_max", "x_isize_max"),
        ("b_address_space_limit", "x_address_space_limit"),
        ("b_borrow_identity", "x_borrow_identity"),
    )
    if config.mutable:
        mapping += (
            ("b_writable", "x_writable"),
            ("b_exclusive_access", "x_exclusive_access"),
            ("b_frame_token", "x_frame_token"),
        )
    return [
        f"(= ({boundary} b) ({input_selector} x))"
        for boundary, input_selector in mapping
    ]


def _arithmetic_definitions(config: ChunkTarget) -> str:
    chunk_start = "(RemainderLength x)" if config.reverse else "0"
    remainder_start = "0" if config.reverse else "(ChunkSpan x)"
    return f"""\
(define-fun ChunkCount ((x Input)) Int
  (div (x_length x) (x_chunk_size x)))
(define-fun RemainderLength ((x Input)) Int
  (mod (x_length x) (x_chunk_size x)))
(define-fun ChunkStart ((x Input)) Int
  {chunk_start})
(define-fun ChunkSpan ((x Input)) Int
  (* (ChunkCount x) (x_chunk_size x)))
(define-fun RemainderStart ((x Input)) Int
  {remainder_start})
(define-fun RemainderSpan ((x Input)) Int
  (RemainderLength x))
(define-fun SliceCastAllocation ((x Input)) Int
  (x_allocation x))
(define-fun SliceCastAddress ((x Input)) Int
  (x_address x))
(define-fun SliceCastProvenance ((x Input)) Int
  (x_provenance x))
(define-fun ArrayPointerCastAllocation ((x Input)) Int
  (SliceCastAllocation x))
(define-fun ArrayPointerCastAddress ((x Input)) Int
  (+ (SliceCastAddress x) (* (ChunkStart x) (x_element_size x))))
(define-fun ArrayPointerCastProvenance ((x Input)) Int
  (SliceCastProvenance x))
(define-fun RawChunksReference ((x Input)) Reference
  (mkReference
    (ArrayPointerCastAllocation x)
    (ArrayPointerCastAddress x)
    (ArrayPointerCastProvenance x)
    (x_borrow_identity x)
    (ChunkStart x)
    (ChunkSpan x)
    (x_chunk_size x)
    3))
(define-fun RawRemainderReference ((x Input)) Reference
  (mkReference
    (SliceCastAllocation x)
    (+ (SliceCastAddress x) (* (RemainderStart x) (x_element_size x)))
    (SliceCastProvenance x)
    (x_borrow_identity x)
    (RemainderStart x)
    (RemainderSpan x)
    1
    2))"""


def _domain_definitions(config: ChunkTarget) -> str:
    extra_requirements = []
    if config.kind == "unchecked":
        extra_requirements.append("(= (RemainderLength x) 0)")
    if config.mutable:
        extra_requirements.extend(
            ("(x_writable x)", "(x_exclusive_access x)")
        )
    extras = "".join(f"\n       {clause}" for clause in extra_requirements)
    return f"""\
(define-fun ByteSpan ((x Input)) Int
  (* (x_length x) (x_element_size x)))
(define-fun ArrayElementBytes ((x Input)) Int
  (* (x_chunk_size x) (x_element_size x)))
(define-fun InputMemoryValid ((x Input)) Bool
  (and (>= (x_length x) 0)
       (> (x_chunk_size x) 0)
       (>= (x_allocation x) 0)
       (> (x_address x) 0)
       (>= (x_provenance x) 0)
       (>= (x_element_size x) 0)
       (> (x_element_alignment x) 0)
       (= (mod (x_address x) (x_element_alignment x)) 0)
       (or (= (x_element_size x) 0)
           (and (>= (x_element_size x) (x_element_alignment x))
                (= (mod (x_element_size x) (x_element_alignment x)) 0)))
       (>= (x_allocation_base x) 0)
       (>= (x_allocation_bytes x) 0)
       (x_one_allocation x)
       (x_initialized x)
       (> (x_isize_max x) 0)
       (> (x_address_space_limit x) 0)
       (<= (ArrayElementBytes x) (x_isize_max x))
       (<= (ByteSpan x) (x_isize_max x))
       (<= (+ (x_address x) (ByteSpan x)) (x_address_space_limit x))
       (or (= (ByteSpan x) 0)
           (and (> (x_allocation x) 0)
                (> (x_provenance x) 0)
                (x_one_allocation x)
                (x_initialized x)
                (<= (+ (x_allocation_base x) (x_allocation_bytes x))
                    (x_address_space_limit x))
                (<= (x_allocation_base x) (x_address x))
                (<= (+ (x_address x) (ByteSpan x))
                    (+ (x_allocation_base x) (x_allocation_bytes x)))))
       (> (x_borrow_identity x) 0){extras}))
(define-fun RawChunkSliceDomainValid ((x Input)) Bool
  (and (>= (ChunkStart x) 0)
       (>= (ChunkSpan x) 0)
       (<= (+ (ChunkStart x) (ChunkSpan x)) (x_length x))
       (= (mod (ChunkSpan x) (x_chunk_size x)) 0)
       (> (ArrayPointerCastAddress x) 0)
       (= (mod (ArrayPointerCastAddress x) (x_element_alignment x)) 0)
       (<= (* (ChunkSpan x) (x_element_size x)) (x_isize_max x))
       (<= (+ (ArrayPointerCastAddress x)
              (* (ChunkSpan x) (x_element_size x)))
           (x_address_space_limit x))
       (or (= (* (ChunkSpan x) (x_element_size x)) 0)
           (and (> (ArrayPointerCastAllocation x) 0)
                (> (ArrayPointerCastProvenance x) 0)
                (x_one_allocation x)
                (x_initialized x)
                (<= (x_allocation_base x) (ArrayPointerCastAddress x))
                (<= (+ (ArrayPointerCastAddress x)
                       (* (ChunkSpan x) (x_element_size x)))
                    (+ (x_allocation_base x) (x_allocation_bytes x)))))))"""


def _source_relations(config: ChunkTarget, purpose: str) -> str:
    model_final_state = config.mutable and purpose == PRIMARY
    mutable_signature = " (s State)" if model_final_state else ""
    lower_name = (
        "LowerAsChunksUncheckedMutTransition"
        if config.mutable
        else "LowerAsChunksUncheckedTransition"
    )
    lower_final = ""
    if model_final_state:
        lower_final = """\
       (= (s_final_chunks_len s) (ChunkCount x))
       (= (s_final_chunks_source s) (s_final_sequence s))
       (= (s_final_chunks_start s) (ChunkStart x))
       (= (s_final_chunks_width s) (x_chunk_size x))
"""
    split = ""
    if config.has_remainder:
        split_name = (
            "SplitFrontRearMutProjection"
            if config.mutable
            else "SplitFrontRearProjection"
        )
        split = f"""\
(define-fun {split_name}
  ((x Input) (y Output){mutable_signature}) Bool
  (and (= (y_remainder_ref y) (RawRemainderReference x))
       (= (y_remainder_len y) (RemainderSpan x))
       (= (y_remainder_source y) (x_sequence x))
       (= (y_remainder_start y) (RemainderStart x))
       (= (+ (ChunkSpan x) (RemainderSpan x)) (x_length x))
       (<= (+ (ChunkStart x) (ChunkSpan x)) (x_length x))))
"""
    state_relation = ""
    if model_final_state:
        remainder_final = ""
        if config.has_remainder:
            remainder_final = """\
       (= (s_final_remainder_len s) (RemainderSpan x))
       (= (s_final_remainder_source s) (s_final_sequence s))
       (= (s_final_remainder_start s) (RemainderStart x))
"""
        state_relation = f"""\
(define-fun SharedStorageAliasProjection
  ((x Input) (y Output) (s State)) Bool
  (and (= (ref_allocation (y_chunks_ref y)) (x_allocation x))
       (= (ref_provenance (y_chunks_ref y)) (x_provenance x))
       (= (ref_parent_borrow (y_chunks_ref y)) (x_borrow_identity x))
       (= (s_final_allocation s) (x_allocation x))
       (= (s_final_address s) (x_address x))
       (= (s_final_provenance s) (x_provenance x))
       (= (s_final_borrow_identity s) (x_borrow_identity x))
       (= (s_final_one_allocation s) (x_one_allocation x))
       (= (s_final_initialized s) (x_initialized x))
       (= (s_final_writable s) (x_writable x))
       (= (s_final_exclusive_access s) (x_exclusive_access x))
       (= (s_final_frame_token s) (x_frame_token x))))
(define-fun MutableFinalViewProjection
  ((x Input) (y Output) (s State)) Bool
  (and (= (s_final_slice_len s) (x_length x))
       (= (s_final_chunks_len s) (ChunkCount x))
       (= (s_final_chunks_source s) (s_final_sequence s))
       (= (s_final_chunks_start s) (ChunkStart x))
       (= (s_final_chunks_width s) (x_chunk_size x))
{remainder_final.rstrip()}))
"""
    elif config.mutable:
        state_relation = """\
(define-fun SharedStorageAliasProjection
  ((x Input) (y Output)) Bool
  (and (= (ref_allocation (y_chunks_ref y)) (x_allocation x))
       (= (ref_provenance (y_chunks_ref y)) (x_provenance x))
       (= (ref_parent_borrow (y_chunks_ref y)) (x_borrow_identity x))))
"""
    elif purpose == PRIMARY:
        state_relation = """\
(define-fun ImmutableFinalStateProjection
  ((x Input) (s State)) Bool
  (and (= (s_final_sequence s) (x_sequence x))
       (= (s_final_slice_len s) (x_length x))
       (= (s_final_allocation s) (x_allocation x))
       (= (s_final_address s) (x_address x))
       (= (s_final_provenance s) (x_provenance x))
       (= (s_final_borrow_identity s) (x_borrow_identity x))
       (= (s_final_one_allocation s) (x_one_allocation x))
       (= (s_final_initialized s) (x_initialized x))))
"""
    return f"""\
(define-fun PointerCastProjection ((x Input) (y Output)) Bool
  (and (= (ref_allocation (y_chunks_ref y)) (SliceCastAllocation x))
       (= (ref_address (y_chunks_ref y)) (ArrayPointerCastAddress x))
       (= (ref_provenance (y_chunks_ref y)) (SliceCastProvenance x))))
(define-fun ArrayPointerCastProjection ((x Input) (y Output)) Bool
  (and (= (ref_allocation (y_chunks_ref y)) (ArrayPointerCastAllocation x))
       (= (ref_address (y_chunks_ref y)) (ArrayPointerCastAddress x))
       (= (ref_provenance (y_chunks_ref y)) (ArrayPointerCastProvenance x))
       (= (ref_element_width (y_chunks_ref y)) (x_chunk_size x))))
(define-fun RawSliceConstructionProjection ((x Input) (y Output)) Bool
  (and (RawChunkSliceDomainValid x)
       (= (y_chunks_ref y) (RawChunksReference x))
       (= (y_chunks_len y) (ChunkCount x))
       (= (y_chunks_source y) (x_sequence x))
       (= (y_chunks_start y) (ChunkStart x))
       (= (y_chunks_width y) (x_chunk_size x))))
(define-fun {lower_name}
  ((x Input) (y Output){mutable_signature}) Bool
  (and (PointerCastProjection x y)
       (ArrayPointerCastProjection x y)
       (RawSliceConstructionProjection x y)
       (= (y_chunks_ref y) (RawChunksReference x))
       (= (y_chunks_len y) (ChunkCount x))
       (= (y_chunks_source y) (x_sequence x))
       (= (y_chunks_start y) (ChunkStart x))
       (= (y_chunks_width y) (x_chunk_size x))
{lower_final.rstrip()}))
{split}{state_relation}"""


def _active_conjunct_symbols(config: ChunkTarget) -> tuple[str, ...]:
    if config.kind == "unchecked":
        symbols = (
            "ActiveFlattenConjunct",
            "ActiveChunksLengthConjunct",
            "ActiveInitialChunkSubrangesConjunct",
        )
    else:
        symbols = (
            "ActivePartitionConjunct",
            "ActiveChunksLengthConjunct",
            "ActiveRemainderLengthConjunct",
            "ActiveInitialChunkSubrangesConjunct",
            "ActiveInitialRemainderSubrangeConjunct",
        )
    if config.mutable:
        symbols += ("ActiveFinalChunksLengthConjunct",)
        if config.has_remainder:
            symbols += ("ActiveFinalRemainderLengthConjunct",)
        symbols += (
            "ActiveFinalFrameConjunct",
            "ActiveFinalChunkSubrangesConjunct",
        )
        if config.has_remainder:
            symbols += ("ActiveFinalRemainderSubrangeConjunct",)
    return symbols


def _active_contract_definitions(config: ChunkTarget, purpose: str) -> str:
    definitions: list[str] = []
    if config.kind == "unchecked":
        definitions.append("""\
(define-fun ActiveFlattenConjunct ((x Input) (y Output)) Bool
  (and (= (y_chunks_source y) (x_sequence x))
       (= (y_chunks_start y) 0)
       (= (y_chunks_width y) (x_chunk_size x))
       (= (* (y_chunks_len y) (x_chunk_size x)) (x_length x))))""")
    else:
        definitions.append("""\
(define-fun ActivePartitionConjunct ((x Input) (y Output)) Bool
  (and (>= (y_remainder_len y) 0)
       (< (y_remainder_len y) (x_chunk_size x))
       (= (x_length x)
          (+ (* (y_chunks_len y) (x_chunk_size x))
             (y_remainder_len y)))
       (= (y_chunks_source y) (x_sequence x))
       (= (y_remainder_source y) (x_sequence x))))""")
    definitions.append("""\
(define-fun ActiveChunksLengthConjunct ((x Input) (y Output)) Bool
  (= (y_chunks_len y) (div (x_length x) (x_chunk_size x))))""")
    if config.has_remainder:
        definitions.append("""\
(define-fun ActiveRemainderLengthConjunct ((x Input) (y Output)) Bool
  (= (y_remainder_len y) (mod (x_length x) (x_chunk_size x))))""")
    definitions.append("""\
(define-fun ActiveInitialChunkSubrangesConjunct
  ((x Input) (y Output)) Bool
  (and (= (y_chunks_source y) (x_sequence x))
       (= (y_chunks_start y) (ChunkStart x))
       (= (y_chunks_width y) (x_chunk_size x))))""")
    if config.has_remainder:
        definitions.append("""\
(define-fun ActiveInitialRemainderSubrangeConjunct
  ((x Input) (y Output)) Bool
  (and (= (y_remainder_source y) (x_sequence x))
       (= (y_remainder_start y) (RemainderStart x))))""")
    if config.mutable and purpose == PRIMARY:
        definitions.append("""\
(define-fun ActiveFinalChunksLengthConjunct
  ((y Output) (s State)) Bool
  (= (s_final_chunks_len s) (y_chunks_len y)))""")
        if config.has_remainder:
            definitions.append("""\
(define-fun ActiveFinalRemainderLengthConjunct
  ((y Output) (s State)) Bool
  (= (s_final_remainder_len s) (y_remainder_len y)))""")
        frame = """\
(define-fun ActiveFinalFrameConjunct
  ((x Input) (s State)) Bool
  (and (= (s_final_slice_len s) (x_length x))
       (= (s_final_chunks_source s) (s_final_sequence s))
       (= (s_final_chunks_start s) (ChunkStart x))
       (= (s_final_chunks_width s) (x_chunk_size x))
       (= (* (s_final_chunks_len s) (x_chunk_size x)) (ChunkSpan x))"""
        if config.has_remainder:
            frame += """
       (= (s_final_remainder_source s) (s_final_sequence s))
       (= (s_final_remainder_start s) (RemainderStart x))
       (= (s_final_slice_len s)
          (+ (* (s_final_chunks_len s) (x_chunk_size x))
             (s_final_remainder_len s)))"""
        else:
            frame += """
       (= (s_final_slice_len s)
          (* (s_final_chunks_len s) (x_chunk_size x)))"""
        frame += "))"
        definitions.append(frame)
        definitions.append("""\
(define-fun ActiveFinalChunkSubrangesConjunct
  ((x Input) (s State)) Bool
  (and (= (s_final_chunks_source s) (s_final_sequence s))
       (= (s_final_chunks_start s) (ChunkStart x))
       (= (s_final_chunks_width s) (x_chunk_size x))))""")
        if config.has_remainder:
            definitions.append("""\
(define-fun ActiveFinalRemainderSubrangeConjunct
  ((x Input) (s State)) Bool
  (and (= (s_final_remainder_source s) (s_final_sequence s))
       (= (s_final_remainder_start s) (RemainderStart x))))""")
    elif config.mutable:
        definitions.extend(
            (
                """\
(define-fun ActiveFinalChunksLengthConjunct
  ((y Output) (final_chunks_len Int)) Bool
  (= final_chunks_len (y_chunks_len y)))""",
                """\
(define-fun ActiveFinalFrameConjunct
  ((x Input)
   (final_sequence Int)
   (final_slice_len Int)
   (final_chunks_len Int)
   (final_chunks_source Int)
   (final_chunks_start Int)
   (final_chunks_width Int)
   (final_remainder_len Int)
   (final_remainder_source Int)
   (final_remainder_start Int)) Bool
  (and (= final_slice_len (x_length x))
       (= final_chunks_source final_sequence)
       (= final_chunks_start (ChunkStart x))
       (= final_chunks_width (x_chunk_size x))
       (= (* final_chunks_len (x_chunk_size x)) (ChunkSpan x))
       (= final_remainder_len (RemainderSpan x))
       (= final_remainder_source final_sequence)
       (= final_remainder_start (RemainderStart x))
       (= final_slice_len
          (+ (* final_chunks_len (x_chunk_size x))
             final_remainder_len))))""",
                """\
(define-fun ActiveFinalChunkSubrangesConjunct
  ((x Input)
   (final_sequence Int)
   (final_chunks_source Int)
   (final_chunks_start Int)
   (final_chunks_width Int)) Bool
  (and (= final_chunks_source final_sequence)
       (= final_chunks_start (ChunkStart x))
       (= final_chunks_width (x_chunk_size x))))""",
                """\
(define-fun ActiveFinalRemainderLengthConjunct
  ((y Output) (final_remainder_len Int)) Bool
  """
                + (
                    "(= final_remainder_len (y_remainder_len y)))"
                    if config.has_remainder
                    else "(= final_remainder_len 0))"
                ),
                """\
(define-fun ActiveFinalRemainderSubrangeConjunct
  ((x Input)
   (final_sequence Int)
   (final_remainder_source Int)
   (final_remainder_start Int)) Bool
  (and (= final_remainder_source final_sequence)
       (= final_remainder_start (RemainderStart x))))""",
                """\
(define-fun FinalContractExists ((x Input) (y Output)) Bool
  (exists
    ((final_sequence Int)
     (final_slice_len Int)
     (final_chunks_len Int)
     (final_chunks_source Int)
     (final_chunks_start Int)
     (final_chunks_width Int)
     (final_remainder_len Int)
     (final_remainder_source Int)
     (final_remainder_start Int))
    (and
      (ActiveFinalChunksLengthConjunct y final_chunks_len)
      """
                + (
                    "(ActiveFinalRemainderLengthConjunct y final_remainder_len)"
                    if config.has_remainder
                    else "(= final_remainder_len 0)"
                )
                + """
      (ActiveFinalFrameConjunct
        x final_sequence final_slice_len final_chunks_len
        final_chunks_source final_chunks_start final_chunks_width
        final_remainder_len final_remainder_source final_remainder_start)
      (ActiveFinalChunkSubrangesConjunct
        x final_sequence final_chunks_source final_chunks_start
        final_chunks_width)
      """
                + (
                    "(ActiveFinalRemainderSubrangeConjunct "
                    "x final_sequence final_remainder_source "
                    "final_remainder_start)"
                    if config.has_remainder
                    else "(= final_remainder_start (RemainderStart x))"
                )
                + ")))",
            )
        )
    return "\n".join(definitions)


def _source_transition_definitions(
    config: ChunkTarget,
    purpose: str,
) -> tuple[str, ...]:
    if config.kind == "unchecked":
        transitions = (
            "PointerCastProjection",
            "ArrayPointerCastProjection",
            "RawSliceConstructionProjection",
            (
                "LowerAsChunksUncheckedMutTransition"
                if config.mutable
                else "LowerAsChunksUncheckedTransition"
            ),
        )
    else:
        transitions = (
            (
                "SplitFrontRearMutProjection"
                if config.mutable
                else "SplitFrontRearProjection"
            ),
            (
                "LowerAsChunksUncheckedMutTransition"
                if config.mutable
                else "LowerAsChunksUncheckedTransition"
            ),
        )
    if config.mutable:
        transitions += ("SharedStorageAliasProjection",)
        if purpose == PRIMARY:
            transitions += ("MutableFinalViewProjection",)
    elif purpose == PRIMARY:
        transitions += ("ImmutableFinalStateProjection",)
    return transitions


def _target_body(config: ChunkTarget, purpose: str) -> str:
    calls: list[str] = ["(InputMemoryLayoutObserved x b)"]
    lower = (
        "LowerAsChunksUncheckedMutTransition"
        if config.mutable
        else "LowerAsChunksUncheckedTransition"
    )
    state_argument = " s" if config.mutable and purpose == PRIMARY else ""
    if config.kind == "unchecked":
        calls.extend(
            (
                "(PointerCastProjection x y)",
                "(ArrayPointerCastProjection x y)",
                "(RawSliceConstructionProjection x y)",
                f"({lower} x y{state_argument})",
            )
        )
    else:
        split = (
            "SplitFrontRearMutProjection"
            if config.mutable
            else "SplitFrontRearProjection"
        )
        calls.extend((f"({split} x y{state_argument})", f"({lower} x y{state_argument})"))
    if config.mutable and purpose == PRIMARY:
        calls.extend(
            (
                "(SharedStorageAliasProjection x y s)",
                "(MutableFinalViewProjection x y s)",
            )
        )
    elif config.mutable:
        calls.append("(SharedStorageAliasProjection x y)")
    elif purpose == PRIMARY:
        calls.append("(ImmutableFinalStateProjection x s)")
    for symbol in _active_conjunct_symbols(config):
        if purpose == EXACT_OUTPUT and symbol.startswith("ActiveFinal"):
            continue
        arguments = "x y"
        if symbol.startswith("ActiveFinal"):
            arguments = "y s" if "Length" in symbol else "x s"
        calls.append(f"({symbol} {arguments})")
    if config.mutable and purpose == EXACT_OUTPUT:
        calls.append("(FinalContractExists x y)")
    return "  (and " + "\n       ".join(calls) + "))"


def _equivalence_body(config: ChunkTarget, purpose: str) -> str:
    equalities = [
        f"(= ({selector} y1) ({selector} y2))"
        for selector, _ in _output_fields(config)
    ]
    if purpose == PRIMARY:
        equalities.extend(
            f"(= ({selector} s1) ({selector} s2))"
            for selector, _ in _state_fields(config)
        )
    return "  (and " + "\n       ".join(equalities) + "))"


def model_text(config: ChunkTarget, purpose: str) -> str:
    if purpose not in PURPOSES:
        raise ValueError(f"{config.artifact_id}: unknown obligation purpose {purpose}")
    observed = "\n       ".join(_observed_equalities(config))
    mutable_requirement = (
        "\n       (> (x_frame_token x) 0)" if config.mutable else ""
    )
    state_declaration = (
        "(declare-datatypes ((State 0)) (((mkState))))"
        if purpose == EXACT_OUTPUT
        else _datatype("State", "mkState", _state_fields(config))
    )
    return f"""\
; Target: {config.target}
; Active contract SHA-256: {config.active_contract_sha256}
; Retained contract SHA-256 (rejected): {config.retained_contract_sha256}
; Purpose: {purpose}
; Values are represented by canonical source/range descriptors.
(set-logic ALL)
{_datatype("Input", "mkInput", _input_fields(config))}
{_datatype("Boundary", "mkBoundary", tuple((name, sort) for name, sort, _ in _boundary_field_specs(config)))}
(declare-datatypes ((Reference 0))
  (((mkReference
      (ref_allocation Int)
      (ref_address Int)
      (ref_provenance Int)
      (ref_parent_borrow Int)
      (ref_start Int)
      (ref_span Int)
      (ref_element_width Int)
      (ref_projection_kind Int)))))
{_datatype("Output", "mkOutput", _output_fields(config))}
{state_declaration}
(declare-const x Input)
(declare-const b Boundary)
(declare-const y1 Output)
(declare-const s1 State)
(declare-const y2 Output)
(declare-const s2 State)
(define-fun InputMemoryLayoutObserved ((x Input) (b Boundary)) Bool
  (and {observed}))
{_arithmetic_definitions(config)}
{_domain_definitions(config)}
{_source_relations(config, purpose)}
{_active_contract_definitions(config, purpose)}
(define-fun Requires_T ((x Input)) Bool
  (and (InputMemoryValid x){mutable_requirement}))
(define-fun Boundary_T ((x Input) (b Boundary)) Bool
  (and (InputMemoryLayoutObserved x b)
       (>= (b_input_allocation b) 0)
       (> (b_input_address b) 0)
       (>= (b_input_provenance b) 0)
       (> (b_element_alignment b) 0)
       (> (b_borrow_identity b) 0)))
(define-fun TargetDefinition_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
{_target_body(config, purpose)}
(define-fun Spec_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (TargetDefinition_T x b y s))
(define-fun Equivalent_T
  ((x Input) (b Boundary)
   (y1 Output) (s1 State) (y2 Output) (s2 State)) Bool
{_equivalence_body(config, purpose)}
"""


def obligation_text(config: ChunkTarget, purpose: str) -> str:
    return model_text(config, purpose) + """\
(assert
  (not
    (=>
      (and (Requires_T x)
           (Boundary_T x b)
           (Spec_T x b y1 s1)
           (Spec_T x b y2 s2))
      (Equivalent_T x b y1 s1 y2 s2))))
(check-sat)
"""


@lru_cache(maxsize=None)
def authority_row(input_order: str) -> dict[str, str]:
    config = TARGET_BY_ORDER[input_order]
    matches = [
        row
        for row in common.read_csv(
            common.OUT / "crosswalk/target_to_proof_boundary.csv"
        )
        if row["target"] == config.target and row["input_order"] == input_order
    ]
    if len(matches) != 1:
        raise ValueError(f"{config.artifact_id}: missing or duplicate authority row")
    row = matches[0]
    if (
        row["active_contract_sha256"] != config.active_contract_sha256
        or common.sha256_text(row["active_contract_text"])
        != config.active_contract_sha256
        or row["retained_contract_sha256"] != config.retained_contract_sha256
        or common.sha256_text(row["retained_contract_text"])
        != config.retained_contract_sha256
        or row["active_contract_text"] == row["retained_contract_text"]
        or row["contract_drift"] != "yes"
        or row["equivalence_kind"] != "exact-principal-return-and-final-state"
    ):
        raise ValueError(f"{config.artifact_id}: active/retained authority changed")
    return row


def _replacement_records(
    config: ChunkTarget,
    purpose: str = PRIMARY,
) -> list[dict[str, Any]]:
    prefix = f"SRC-{config.input_order}"
    site = f"TS-{int(config.input_order):03d}"
    if config.kind == "unchecked":
        pointer_site = (
            "core/src/slice/mod.rs:757-759"
            if config.mutable
            else "core/src/slice/mod.rs:726-728"
        )
        raw_site = (
            "core/src/slice/raw.rs:143-196"
            if config.mutable
            else "core/src/slice/raw.rs:80-141"
        )
        records = [
            {
                "replacement_id": f"{prefix}-REVIEWED-SLICE-POINTER-CAST",
                "operation": (
                    "compose target 019 as_mut_ptr cast semantics"
                    if config.mutable
                    else "compose target 021 as_ptr cast semantics"
                ),
                "symbols": ["PointerCastProjection"],
                "source_citations": [pointer_site, config.pointer_dependency],
                "replaces_trust_site_ids": [
                    f"{site}-D002",
                ],
            },
            {
                "replacement_id": f"{prefix}-ARRAY-POINTER-CAST",
                "operation": (
                    "cast the source thin pointer to an N-element array pointer "
                    "without changing address, allocation, or provenance"
                ),
                "symbols": ["ArrayPointerCastProjection"],
                "source_citations": [
                    f"{SLICE_SOURCE_PATH}:{config.source_item_span[0]}-{config.source_item_span[1]}"
                ],
                "replaces_trust_site_ids": [
                    f"{site}-D005",
                    f"{site}-E001",
                ],
            },
            {
                "replacement_id": f"{prefix}-RAW-SLICE-CONSTRUCTION",
                "operation": (
                    "construct the array slice from a non-null aligned pointer "
                    "inside one initialized allocation with isize-fit/no-wrap "
                    "geometry"
                ),
                "symbols": [
                    "RawSliceConstructionProjection",
                    (
                        "SharedStorageAliasProjection"
                        if config.mutable
                        else (
                            "LowerAsChunksUncheckedTransition"
                        )
                    ),
                ],
                "source_citations": [raw_site],
                "replaces_trust_site_ids": [
                    f"{site}-D006",
                    f"{site}-E002",
                ],
            },
        ]
        if config.mutable:
            records[-1]["symbols"].append(
                "LowerAsChunksUncheckedMutTransition"
            )
            if purpose == PRIMARY:
                records[-1]["symbols"].append("MutableFinalViewProjection")
        return records

    split_ids = (
        [
            f"{site}-E001",
            f"{site}-E002",
        ]
        if config.kind == "chunks"
        else []
    )
    lower_ids = [f"{site}-D003"]
    if config.kind == "chunks":
        lower_ids.append(f"{site}-E003")
    else:
        lower_ids.append(f"{site}-E001")
    records = [
        {
            "replacement_id": f"{prefix}-FRONT-REAR-SPLIT",
            "operation": (
                "derive exact front and rear subranges at the source split index"
            ),
            "symbols": [
                (
                    "SplitFrontRearMutProjection"
                    if config.mutable
                    else "SplitFrontRearProjection"
                )
            ],
            "source_citations": [
                (
                    "core/src/slice/mod.rs:1961-1991"
                    if config.mutable
                    else (
                        "core/src/slice/mod.rs:1993-2054"
                        if config.kind == "chunks"
                        else "core/src/slice/mod.rs:1912-1959"
                    )
                )
            ],
            "replaces_trust_site_ids": split_ids,
        },
        {
            "replacement_id": f"{prefix}-LOWER-{config.lower_dependency}",
            "operation": (
                "compose the checked lower array-chunk transition without "
                "placing its returned view in Boundary_T"
            ),
            "symbols": [
                (
                    "LowerAsChunksUncheckedMutTransition"
                    if config.mutable
                    else "LowerAsChunksUncheckedTransition"
                )
            ],
            "source_citations": [
                config.lower_dependency or "",
                (
                    "core/src/slice/mod.rs:1498-1509"
                    if config.mutable
                    else "core/src/slice/mod.rs:1338-1349"
                ),
            ],
            "replaces_trust_site_ids": lower_ids,
        },
    ]
    if not split_ids:
        records[0]["replaces_trust_site_ids"] = [
            f"{site}-D002"
        ]
        admitted = set(config.admitted_trust_sites)
        if f"{site}-D002" in admitted:
            records.pop(0)
    return records


def _boundary_backing(
    config: ChunkTarget,
    purpose: str = PRIMARY,
) -> tuple[list[str], list[str]]:
    replacements = _replacement_records(config, purpose)
    if config.kind == "unchecked":
        return (
            [
                replacements[0]["replacement_id"],
                replacements[2]["replacement_id"],
            ],
            list(config.admitted_trust_sites),
        )
    return ([], list(config.admitted_trust_sites))


def _boundary_fields(
    config: ChunkTarget,
    purpose: str = PRIMARY,
) -> list[dict[str, Any]]:
    replacement_ids, trust_ids = _boundary_backing(config, purpose)
    pointer_citation = (
        "core/src/slice/mod.rs:757-759"
        if config.mutable
        else "core/src/slice/mod.rs:726-728"
    )
    raw_citation = (
        "core/src/slice/raw.rs:143-196"
        if config.mutable
        else "core/src/slice/raw.rs:80-141"
    )
    fields = []
    for selector, _, role in _boundary_field_specs(config):
        pointer_field = selector in {
            "b_input_allocation",
            "b_input_address",
            "b_input_provenance",
        }
        citations = (
            [pointer_citation, config.pointer_dependency]
            if pointer_field
            else [raw_citation]
        )
        if config.kind != "unchecked":
            citations.append(
                f"{SLICE_SOURCE_PATH}:{config.source_item_span[0]}-{config.source_item_span[1]}"
            )
        field_replacements = []
        if replacement_ids:
            field_replacements = [
                replacement_ids[0] if pointer_field else replacement_ids[-1]
            ]
        fields.append(
            {
                "selector": selector,
                "role": role,
                "source_citations": citations,
                "trust_site_ids": trust_ids,
                "source_backed_replacement_ids": field_replacements,
            }
        )
    return fields


def _principal_observations(
    config: ChunkTarget,
    purpose: str,
) -> list[dict[str, str]]:
    result = [
        {
            "selector": selector,
            "left": "output1",
            "right": "output2",
            "sort": sort,
        }
        for selector, sort in _output_fields(config)
    ]
    if purpose == PRIMARY:
        result.extend(
            {
                "selector": selector,
                "left": "state1",
                "right": "state2",
                "sort": sort,
            }
            for selector, sort in _state_fields(config)
        )
    return result


def obligation_metadata(config: ChunkTarget, purpose: str) -> dict[str, Any]:
    row = authority_row(config.input_order)
    all_sites = row["all_trust_site_ids"].split(";")
    replacements = _replacement_records(config, purpose)
    replacement_ids, _ = _boundary_backing(config, purpose)
    return {
        "schema_version": 3,
        "target": config.target,
        "input_order": config.input_order,
        "obligation_purpose": purpose,
        "active_contract_sha256": config.active_contract_sha256,
        "active_contract_text": row["active_contract_text"],
        "rejected_retained_contract_sha256": config.retained_contract_sha256,
        "rejected_retained_contract_text": row["retained_contract_text"],
        "domain": {
            "length": "arbitrary nonnegative mathematical integer",
            "chunk_size": "arbitrary positive mathematical integer",
            "memory": (
                "non-null aligned pointer, valid type layout, isize-fit and "
                "no-wrap byte span, one allocation for every nonempty byte span"
            ),
            "empty_and_zst": (
                "aligned non-null dangling pointers are permitted when the byte "
                "span is zero"
            ),
        },
        "contract_translation": {
            "active_conjuncts": list(_active_conjunct_symbols(config)),
            "source_flow": (
                [
                    "assert N != 0 and exact divisibility",
                    f"compose {config.pointer_dependency}",
                    "cast the thin element pointer to an array pointer",
                    (
                        "construct a mutable raw array slice and preserve "
                        "shared-storage/final-view projections"
                        if config.mutable
                        else "construct an immutable raw array slice"
                    ),
                ]
                if config.kind == "unchecked"
                else [
                    "assert N != 0",
                    "compute quotient, remainder, and exact split index",
                    "derive front and rear source ranges",
                    f"compose {config.lower_dependency}",
                    (
                        "project mutable aliasing and final views"
                        if config.mutable
                        else "preserve the immutable receiver"
                    ),
                ]
            ),
            "front_rear_policy": (
                "front chunks, rear remainder"
                if config.kind == "chunks"
                else (
                    "front remainder, rear chunks"
                    if config.kind == "rchunks"
                    else "entire slice is the chunk range"
                )
            ),
        },
        "boundary_scope": {
            "admitted_trust_site_ids": list(config.admitted_trust_sites),
            "excluded_retained_trust_site_ids": list(
                config.excluded_retained_trust_sites
            ),
            "context_only_trust_site_ids": list(config.context_only_trust_sites),
            "all_audited_trust_site_ids": all_sites,
            "source_backed_replacement_ids": replacement_ids,
            "shared_observations": [
                selector for selector, _, _ in _boundary_field_specs(config)
            ],
            "excluded_observations": [
                "returned references and ranges",
                "chunk or remainder values",
                "final storage or final view",
                "answer encodings",
                "partial or complete execution traces",
            ],
            "narrower_than_target": True,
        },
        "boundary_fields": _boundary_fields(config, purpose),
        "source_backed_replacements": replacements,
        "declared_functions": [],
        "source_transition_definitions": list(
            _source_transition_definitions(config, purpose)
        ),
        "target_definition": "TargetDefinition_T",
        "theorem_variables": {
            "input": "x",
            "boundary": "b",
            "output1": "y1",
            "state1": "s1",
            "output2": "y2",
            "state2": "s2",
        },
        "equivalence_kind": "exact",
        "equivalence_scope": (
            "principal return and every modeled final-state observation"
            if purpose == PRIMARY
            else "principal return only; final contract remains in each Spec_T"
        ),
        "principal_observations": _principal_observations(config, purpose),
        "expected_solver_result": config.expected_solver_results[purpose],
    }


def obligation(
    config: ChunkTarget,
    purpose: str,
) -> tuple[str, dict[str, Any]]:
    return obligation_text(config, purpose), obligation_metadata(config, purpose)


def validate_target_obligation(
    config: ChunkTarget,
    text: str,
    metadata: dict[str, Any],
) -> None:
    validate_obligation(text, metadata)
    purpose = metadata.get("obligation_purpose")
    if purpose not in PURPOSES:
        raise GuardError(f"{config.artifact_id}: unknown obligation purpose")
    expected_text, expected_metadata = obligation(config, str(purpose))
    if metadata != expected_metadata:
        raise GuardError(
            f"{config.artifact_id}: metadata differs from reviewed translation"
        )
    if parse_smt(text) != parse_smt(expected_text):
        raise GuardError(
            f"{config.artifact_id}: SMT differs from reviewed translation"
        )


def boundary_manifest(config: ChunkTarget) -> dict[str, Any]:
    row = authority_row(config.input_order)
    return {
        "schema_version": 1,
        "target": config.target,
        "input_order": config.input_order,
        "active_contract_sha256": config.active_contract_sha256,
        "rejected_retained_contract_sha256": config.retained_contract_sha256,
        "boundary_narrower_than_target": True,
        "shared_boundary_observations": _boundary_fields(config),
        "source_backed_replacements": _replacement_records(config),
        "source_transition_definitions": list(
            _source_transition_definitions(config, PRIMARY)
        ),
        "all_audited_trust_site_ids": row["all_trust_site_ids"].split(";"),
        "admitted_retained_trust_site_ids": list(config.admitted_trust_sites),
        "excluded_retained_trust_site_ids": list(
            config.excluded_retained_trust_sites
        ),
        "context_only_trust_site_ids": list(config.context_only_trust_sites),
        "lower_dependency": config.lower_dependency,
        "pointer_dependency": config.pointer_dependency,
        "excluded_from_boundary": [
            "returned references",
            "front or rear ranges",
            "chunk and remainder values",
            "final storage",
            "final views",
            "answer encodings",
            "execution traces",
        ],
    }


def _base_values(
    config: ChunkTarget,
    *,
    length: int | None = None,
    element_size: int = 4,
    address: int = 1024,
    provenance: int = 7,
    allocation: int = 5,
    alignment: int = 4,
    isize_max: int = 1_000_000,
) -> dict[str, int]:
    if length is None:
        length = 4 if config.kind == "unchecked" else 5
    values = {
        "sequence": 101,
        "length": length,
        "chunk_size": 2,
        "allocation": allocation,
        "address": address,
        "provenance": provenance,
        "element_size": element_size,
        "element_alignment": alignment,
        "allocation_base": 1024,
        "allocation_bytes": 256,
        "one_allocation": True,
        "initialized": True,
        "isize_max": isize_max,
        "address_space_limit": 1_000_000,
        "borrow_identity": 11,
        "writable": True,
        "exclusive_access": True,
        "frame_token": 13,
    }
    return values


def _input_term(config: ChunkTarget, values: dict[str, int]) -> str:
    order = [selector.removeprefix("x_") for selector, _ in _input_fields(config)]
    return "(mkInput " + " ".join(_smt_value(values[name]) for name in order) + ")"


def _boundary_term(config: ChunkTarget, values: dict[str, int]) -> str:
    order = [
        selector.removeprefix("b_").removeprefix("input_")
        for selector, _, _ in _boundary_field_specs(config)
    ]
    aliases = {
        "element_size": "element_size",
        "element_alignment": "element_alignment",
        "allocation_base": "allocation_base",
        "allocation_bytes": "allocation_bytes",
        "isize_max": "isize_max",
        "address_space_limit": "address_space_limit",
        "borrow_identity": "borrow_identity",
        "frame_token": "frame_token",
    }
    return "(mkBoundary " + " ".join(
        _smt_value(values[aliases.get(name, name)]) for name in order
    ) + ")"


def _smt_value(value: int | bool) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def _geometry(config: ChunkTarget, values: dict[str, int]) -> dict[str, int]:
    length = values["length"]
    n = values["chunk_size"]
    chunks = length // n
    remainder = length % n
    chunk_start = remainder if config.reverse else 0
    chunk_span = chunks * n
    remainder_start = 0 if config.reverse else chunk_span
    return {
        "chunks_len": chunks,
        "remainder_len": remainder,
        "chunk_start": chunk_start,
        "chunk_span": chunk_span,
        "remainder_start": remainder_start,
    }


def _reference_term(
    values: dict[str, int],
    *,
    start: int,
    span: int,
    width: int,
    kind: int,
) -> str:
    address = values["address"] + start * values["element_size"]
    return (
        "(mkReference "
        f"{values['allocation']} {address} {values['provenance']} "
        f"{values['borrow_identity']} {start} {span} {width} {kind})"
    )


def _output_term(config: ChunkTarget, values: dict[str, int]) -> str:
    geometry = _geometry(config, values)
    terms = [
        _reference_term(
            values,
            start=geometry["chunk_start"],
            span=geometry["chunk_span"],
            width=values["chunk_size"],
            kind=3,
        ),
        str(geometry["chunks_len"]),
        str(values["sequence"]),
        str(geometry["chunk_start"]),
        str(values["chunk_size"]),
    ]
    if config.has_remainder:
        terms.extend(
            (
                _reference_term(
                    values,
                    start=geometry["remainder_start"],
                    span=geometry["remainder_len"],
                    width=1,
                    kind=2,
                ),
                str(geometry["remainder_len"]),
                str(values["sequence"]),
                str(geometry["remainder_start"]),
            )
        )
    return "(mkOutput " + " ".join(terms) + ")"


def _state_term(
    config: ChunkTarget,
    values: dict[str, int],
    *,
    final_sequence: int | None = None,
) -> str:
    geometry = _geometry(config, values)
    sequence = values["sequence"] if final_sequence is None else final_sequence
    terms = [
        str(sequence),
        str(values["length"]),
        str(values["allocation"]),
        str(values["address"]),
        str(values["provenance"]),
        str(values["borrow_identity"]),
        _smt_value(values["one_allocation"]),
        _smt_value(values["initialized"]),
    ]
    if config.mutable:
        terms.extend(
            (
                _smt_value(values["writable"]),
                _smt_value(values["exclusive_access"]),
                str(values["frame_token"]),
                str(geometry["chunks_len"]),
                str(sequence),
                str(geometry["chunk_start"]),
                str(values["chunk_size"]),
            )
        )
        if config.has_remainder:
            terms.extend(
                (
                    str(geometry["remainder_len"]),
                    str(sequence),
                    str(geometry["remainder_start"]),
                )
            )
    return "(mkState " + " ".join(terms) + ")"


def probe_cases(config: ChunkTarget) -> dict[str, dict[str, Any]]:
    valid = _base_values(config)
    empty = _base_values(
        config,
        length=0,
        allocation=0,
        provenance=0,
    )
    zst = _base_values(
        config,
        length=4 if config.kind == "unchecked" else 5,
        element_size=0,
        allocation=0,
        provenance=0,
        alignment=8,
    )
    zero = dict(valid, chunk_size=0)
    indivisible = dict(valid, length=3)
    null = dict(valid, address=0)
    misaligned = dict(valid, address=1026)
    overflow = dict(valid, element_size=8, isize_max=16)
    uninitialized = dict(valid, initialized=False)
    multi_allocation = dict(valid, one_allocation=False)
    cases: dict[str, dict[str, Any]] = {
        "valid_nonempty": {"kind": "valid", "values": valid, "expected": "sat"},
        "valid_empty": {"kind": "valid", "values": empty, "expected": "sat"},
        "valid_zst": {"kind": "valid", "values": zst, "expected": "sat"},
        "invalid_n_zero": {"kind": "invalid-domain", "values": zero, "expected": "unsat"},
        "invalid_null_pointer": {
            "kind": "invalid-domain",
            "values": null,
            "expected": "unsat",
        },
        "invalid_misaligned_pointer": {
            "kind": "invalid-domain",
            "values": misaligned,
            "expected": "unsat",
        },
        "invalid_isize_overflow": {
            "kind": "invalid-domain",
            "values": overflow,
            "expected": "unsat",
        },
        "invalid_uninitialized_storage": {
            "kind": "invalid-domain",
            "values": uninitialized,
            "expected": "unsat",
        },
        "invalid_multiple_allocation_span": {
            "kind": "invalid-domain",
            "values": multi_allocation,
            "expected": "unsat",
        },
        "changed_output_provenance": {
            "kind": "invalid-transition",
            "values": valid,
            "expected": "unsat",
        },
        "invalid_lower_divisibility": {
            "kind": "invalid-transition",
            "values": indivisible if config.kind == "unchecked" else valid,
            "expected": "unsat",
        },
    }
    if config.has_remainder:
        cases["swapped_front_rear"] = {
            "kind": "invalid-transition",
            "values": valid,
            "expected": "unsat",
        }
    if config.mutable:
        cases["invalid_nonwritable_storage"] = {
            "kind": "invalid-domain",
            "values": dict(valid, writable=False),
            "expected": "unsat",
        }
        cases["invalid_alias_exclusivity"] = {
            "kind": "invalid-domain",
            "values": dict(valid, exclusive_access=False),
            "expected": "unsat",
        }
    return cases


def probe_text(config: ChunkTarget, name: str) -> str:
    case = probe_cases(config)[name]
    values = case["values"]
    lines = [
        model_text(config, PRIMARY),
        f"(assert (= x {_input_term(config, values)}))",
    ]
    if case["kind"] == "valid":
        lines.extend(
            (
                f"(assert (= b {_boundary_term(config, values)}))",
                "(assert (Requires_T x))",
                "(assert (Boundary_T x b))",
                "(assert (TargetDefinition_T x b y1 s1))",
            )
        )
    elif name == "changed_output_provenance":
        lines.extend(
            (
                f"(assert (= b {_boundary_term(config, values)}))",
                "(assert (Requires_T x))",
                "(assert (Boundary_T x b))",
                "(assert (TargetDefinition_T x b y1 s1))",
                "(assert (distinct (ref_provenance (y_chunks_ref y1)) "
                "(x_provenance x)))",
            )
        )
    elif name == "invalid_lower_divisibility" and config.kind != "unchecked":
        lines.extend(
            (
                f"(assert (= b {_boundary_term(config, values)}))",
                "(assert (Requires_T x))",
                "(assert (Boundary_T x b))",
                "(assert (TargetDefinition_T x b y1 s1))",
                "(assert (distinct (mod (ChunkSpan x) (x_chunk_size x)) 0))",
            )
        )
    elif name == "swapped_front_rear":
        lines.extend(
            (
                f"(assert (= b {_boundary_term(config, values)}))",
                "(assert (Requires_T x))",
                "(assert (Boundary_T x b))",
                "(assert (TargetDefinition_T x b y1 s1))",
                "(assert (= (y_chunks_start y1) (RemainderStart x)))",
                "(assert (= (y_remainder_start y1) (ChunkStart x)))",
            )
        )
    else:
        lines.append("(assert (Requires_T x))")
    lines.extend(
        (
            "(check-sat)",
            "(get-value ((x_length x) (x_chunk_size x) (x_address x) "
            "(x_provenance x) (x_element_size x)))"
            if case["expected"] == "sat"
            else "",
        )
    )
    return "\n".join(line for line in lines if line) + "\n"


def witness_payload(config: ChunkTarget) -> dict[str, Any]:
    if not config.mutable:
        raise ValueError("immutable chunk targets do not require SAT witnesses")
    values = [10, 20, 30, 40] if config.kind == "unchecked" else [10, 20, 30, 40, 50]
    n = 2
    chunks_count = len(values) // n
    remainder_count = len(values) % n
    chunk_start = remainder_count if config.reverse else 0
    chunk_values = values[chunk_start:]
    output = {
        "chunks_reference": {
            "allocation": 5,
            "address": 1024 + chunk_start * 4,
            "provenance": 7,
            "parent_borrow": 11,
            "start": chunk_start,
            "span": chunks_count * n,
            "element_width": n,
            "projection_kind": "array-chunks",
        },
        "chunks": [
            chunk_values[index : index + n]
            for index in range(0, len(chunk_values), n)
        ],
    }
    if config.has_remainder:
        remainder_start = 0 if config.reverse else chunks_count * n
        output["remainder_reference"] = {
            "allocation": 5,
            "address": 1024 + remainder_start * 4,
            "provenance": 7,
            "parent_borrow": 11,
            "start": remainder_start,
            "span": remainder_count,
            "element_width": 1,
            "projection_kind": "slice-remainder",
        }
        output["remainder"] = (
            values[:remainder_count]
            if config.reverse
            else values[chunks_count * n :]
        )

    def final(values_after: list[int]) -> dict[str, Any]:
        chunk_values_after = values_after[chunk_start:]
        result: dict[str, Any] = {
            "slice": values_after,
            "chunks": [
                chunk_values_after[index : index + n]
                for index in range(0, len(chunk_values_after), n)
            ],
        }
        if config.has_remainder:
            result["remainder"] = (
                values_after[:remainder_count]
                if config.reverse
                else values_after[chunks_count * n :]
            )
        return result

    first = list(range(1, len(values) + 1))
    second = list(range(11, 11 + len(values)))
    return {
        "schema_version": 1,
        "target": config.target,
        "input_order": config.input_order,
        "active_contract_sha256": config.active_contract_sha256,
        "input": {
            "slice": values,
            "chunk_size": n,
            "allocation": 5,
            "address": 1024,
            "provenance": 7,
            "element_size": 4,
            "element_alignment": 4,
            "allocation_base": 1024,
            "allocation_bytes": 256,
            "one_allocation": True,
            "initialized": True,
            "isize_max": 1_000_000,
            "address_space_limit": 1_000_000,
            "borrow_identity": 11,
            "writable": True,
            "exclusive_access": True,
            "frame_token": 13,
        },
        "boundary": {
            "input_allocation": 5,
            "input_address": 1024,
            "input_provenance": 7,
            "element_size": 4,
            "element_alignment": 4,
            "allocation_base": 1024,
            "allocation_bytes": 256,
            "one_allocation": True,
            "initialized": True,
            "isize_max": 1_000_000,
            "address_space_limit": 1_000_000,
            "borrow_identity": 11,
            "writable": True,
            "exclusive_access": True,
            "frame_token": 13,
        },
        "execution1": {"output": output, "final": final(first)},
        "execution2": {"output": output, "final": final(second)},
        "expected": {
            "same_input": True,
            "same_boundary": True,
            "execution1_satisfies_all_active_conjuncts": True,
            "execution2_satisfies_all_active_conjuncts": True,
            "exact_output_equal": True,
            "exact_final_state_equal": False,
            "full_exact_equivalent": False,
        },
    }


def fixed_model_text(config: ChunkTarget) -> str:
    if not config.mutable:
        raise ValueError("immutable chunk targets have no SAT classification")
    values = _base_values(config)
    return model_text(config, PRIMARY) + f"""\
(assert (= x {_input_term(config, values)}))
(assert (= b {_boundary_term(config, values)}))
(assert (= y1 {_output_term(config, values)}))
(assert (= y2 {_output_term(config, values)}))
(assert (= s1 {_state_term(config, values, final_sequence=201)}))
(assert (= s2 {_state_term(config, values, final_sequence=202)}))
(assert (Requires_T x))
(assert (Boundary_T x b))
(assert (Spec_T x b y1 s1))
(assert (Spec_T x b y2 s2))
(assert (not (Equivalent_T x b y1 s1 y2 s2)))
(check-sat)
(get-value (
  (y_chunks_ref y1)
  (y_chunks_ref y2)
  (s_final_sequence s1)
  (s_final_sequence s2)
  (Equivalent_T x b y1 s1 y2 s2)))
"""
