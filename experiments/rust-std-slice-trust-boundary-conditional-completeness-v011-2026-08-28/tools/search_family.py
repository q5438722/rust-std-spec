#!/usr/bin/env python3
"""Bounded source-backed models for the Slice search-wrapper family."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from checker_guards import GuardError, parse_smt, validate_obligation


PRIMARY = "completeness-modulo-reviewed-equivalence"
EXACT_OUTPUT = "exact-output-determinism"

SLICE_SOURCE_PATH = "core/src/slice/mod.rs"
SLICE_SOURCE_SHA256 = (
    "58901fa6437dbd4d77c68427bbced0fc3a91a10fdb8bd2e233adf6a9ba27d2d5"
)
LOWER_SOURCE_START = 2970
LOWER_SOURCE_END = 3022
LOWER_SOURCE_SHA256 = (
    "8a7ce9ee452f424a23a87b3d92b45c675e3d2b4a27c219bfe45f14f1832a42b3"
)
LOWER_ARTIFACT_ID = "029_core_slice_binary_search_by"
LOWER_TARGET = "core::slice::binary_search_by"
LOWER_ACTIVE_CONTRACT_SHA256 = (
    "bbea7d2146da8d9116c68e9603460103ed4f7322c785180266a17b23b06c0f6b"
)
POSITIVE_EQUIVALENCE_WITNESS = (
    "evidence/equivalence/binary_search_duplicate.positive.smt2"
)
NEGATIVE_EQUIVALENCE_WITNESS = (
    "evidence/equivalence/binary_search_duplicate.negative.smt2"
)


@dataclass(frozen=True)
class SearchTarget:
    target: str
    input_order: str
    artifact_id: str
    kind: str
    active_contract_sha256: str
    active_contract_text: str
    sanity_purpose: str
    source_reference: str
    docs_reference: str
    source_item_filename: str
    source_docs_filename: str
    all_audited_trust_sites: tuple[str, ...]
    excluded_retained_trust_sites: tuple[str, ...]
    context_only_trust_sites: tuple[str, ...]
    admitted_boundary_trust_sites: tuple[str, ...]
    replacement_id: str
    replacement_operation: str
    replacement_symbol: str
    replacement_citations: tuple[str, ...]
    classification_basis: str
    verus_expected_summary: str = "verification results:: 3 verified, 0 errors"

    @property
    def purposes(self) -> tuple[str, str, str]:
        return (PRIMARY, self.sanity_purpose, EXACT_OUTPUT)

    @property
    def weak_equivalence(self) -> bool:
        return self.kind in {"ord", "key"}

    @property
    def label(self) -> str:
        return f"target-{int(self.input_order):03d}"


TARGET_028 = SearchTarget(
    target="core::slice::binary_search",
    input_order="28",
    artifact_id="028_core_slice_binary_search",
    kind="ord",
    active_contract_sha256=(
        "27d8e9d741e10e00091ad567844c0aca7d8bd48425cd705dfcf7173e0c973975"
    ),
    active_contract_text=(
        "pub assume_specification<T: core::cmp::Ord>[ <[T]>::binary_search ]"
        "(slice: &[T], x: &T) -> (result: core::result::Result<usize, usize>) "
        "ensures slice_binary_search_result(slice@, *x, result);"
    ),
    sanity_purpose="ordered-domain-sanity",
    source_reference="core/src/slice/mod.rs:2919-2924",
    docs_reference="core/src/slice/mod.rs:2849-2917",
    source_item_filename="binary_search_item.rs",
    source_docs_filename="binary_search_docs.md",
    all_audited_trust_sites=(
        "TS-028-D001",
        "TS-028-D002",
        "TS-028-D003",
        "TS-028-D004",
        "TS-028-E001",
        "TS-028-E002",
        "TS-028-E003",
    ),
    excluded_retained_trust_sites=(
        "TS-028-D002",
        "TS-028-D003",
        "TS-028-D004",
        "TS-028-E001",
        "TS-028-E003",
    ),
    context_only_trust_sites=("TS-028-D001",),
    admitted_boundary_trust_sites=("TS-028-E002",),
    replacement_id="SRC-028-ORD-BINARY-SEARCH-WRAPPER",
    replacement_operation=(
        "binary_search_by(|p| p.cmp(x)) with transparent Ord comparison "
        "adaptation and the reviewed lower search relation"
    ),
    replacement_symbol="SourceBackedBinarySearchWrapper",
    replacement_citations=(
        "core/src/slice/mod.rs:2919-2924",
        "core/src/slice/mod.rs:2970-3022",
    ),
    classification_basis=(
        "The unconstrained active contract admits fixed-boundary Ok(0) and "
        "Err(0) results for one descending input, while the ordered-domain "
        "theorem is UNSAT modulo matching-index equivalence. Equal duplicates "
        "admit distinct Ok indices, so exact output remains incomplete."
    ),
)

TARGET_030 = SearchTarget(
    target="core::slice::binary_search_by_key",
    input_order="30",
    artifact_id="030_core_slice_binary_search_by_key",
    kind="key",
    active_contract_sha256=(
        "613ffeb61ff37d877cf411db0ed8f76bcb2a93646330438d2a55cfb46e1a5ce5"
    ),
    active_contract_text=(
        "pub assume_specification<'a, T, B: core::cmp::Ord, F: "
        "core::ops::FnMut(&'a T) -> B>[ <[T]>::binary_search_by_key::<B, F> ]"
        "(slice: &'a [T], key: &B, f: F) -> "
        "(result: core::result::Result<usize, usize>) ensures "
        "slice_binary_search_by_key_result::<F, T, B>(slice@, *key, f, result);"
    ),
    sanity_purpose="ordered-domain-sanity",
    source_reference="core/src/slice/mod.rs:3071-3077",
    docs_reference="core/src/slice/mod.rs:3024-3063",
    source_item_filename="binary_search_by_key_item.rs",
    source_docs_filename="binary_search_by_key_docs.md",
    all_audited_trust_sites=(
        "TS-030-D001",
        "TS-030-D002",
        "TS-030-D003",
        "TS-030-D004",
        "TS-030-D005",
        "TS-030-D006",
        "TS-030-E001",
        "TS-030-E002",
    ),
    excluded_retained_trust_sites=(
        "TS-030-D005",
        "TS-030-D006",
        "TS-030-E001",
        "TS-030-E002",
    ),
    context_only_trust_sites=("TS-030-D001",),
    admitted_boundary_trust_sites=(
        "TS-030-D002",
        "TS-030-D003",
        "TS-030-D004",
    ),
    replacement_id="SRC-030-KEY-BINARY-SEARCH-WRAPPER",
    replacement_operation=(
        "binary_search_by(|k| f(k).cmp(key)) with explicit key extraction, "
        "Ord comparison, callback state, and reviewed lower search relation"
    ),
    replacement_symbol="SourceBackedBinarySearchByKeyWrapper",
    replacement_citations=(
        "core/src/slice/mod.rs:3071-3077",
        "core/src/slice/mod.rs:2970-3022",
    ),
    classification_basis=(
        "The unconstrained active contract admits fixed-boundary Ok(0) and "
        "Err(0) results for descending extracted keys, while the ordered-key "
        "theorem is UNSAT modulo matching-index equivalence. Duplicate keys "
        "admit distinct Ok indices, so exact output remains incomplete."
    ),
)

TARGET_065 = SearchTarget(
    target="core::slice::partition_point",
    input_order="65",
    artifact_id="065_core_slice_partition_point",
    kind="partition",
    active_contract_sha256=(
        "f28650f03f1c7e571f308b88c4dea8453057ce7b4b33946af0745ae5517fd695"
    ),
    active_contract_text=(
        "pub assume_specification<T, P: core::ops::FnMut(&T) -> bool>"
        "[ <[T]>::partition_point::<P> ](slice: &[T], pred: P) -> "
        "(index: usize) ensures slice_partition_point_result(slice@, pred, index);"
    ),
    sanity_purpose="partitioned-domain-sanity",
    source_reference="core/src/slice/mod.rs:4854-4859",
    docs_reference="core/src/slice/mod.rs:4803-4851",
    source_item_filename="partition_point_item.rs",
    source_docs_filename="partition_point_docs.md",
    all_audited_trust_sites=(
        "TS-065-D001",
        "TS-065-D002",
        "TS-065-D003",
        "TS-065-C001",
        "TS-065-E001",
    ),
    excluded_retained_trust_sites=("TS-065-D002", "TS-065-E001"),
    context_only_trust_sites=("TS-065-D001", "TS-065-C001"),
    admitted_boundary_trust_sites=("TS-065-D003",),
    replacement_id="SRC-065-PARTITION-POINT-WRAPPER",
    replacement_operation=(
        "binary_search_by predicate-to-Ordering adapter followed by "
        "Result::unwrap_or_else identity mapping"
    ),
    replacement_symbol="SourceBackedPartitionPointWrapper",
    replacement_citations=(
        "core/src/slice/mod.rs:4854-4859",
        "core/src/slice/mod.rs:2970-3022",
    ),
    classification_basis=(
        "The non-partitioned [false, true] profile admits distinct indices "
        "under one fixed boundary, so both exact-output and full exact-state "
        "theorems are SAT. The partitioned-domain theorem is UNSAT."
    ),
)


def _common_prefix(config: SearchTarget) -> str:
    input_fields = {
        "ord": """\
      (x_length Int)
      (x_element0 Int)
      (x_element1 Int)
      (x_search_value Int)
      (x_callback_initial_state Int)""",
        "key": """\
      (x_length Int)
      (x_element0 Int)
      (x_element1 Int)
      (x_search_key Key)
      (x_callback_initial_state Int)""",
        "partition": """\
      (x_length Int)
      (x_element0 Int)
      (x_element1 Int)
      (x_callback_initial_state Int)""",
    }[config.kind]
    boundary_fields = {
        "ord": """\
      (b_read0 Int)
      (b_read1 Int)
      (b_cmp0 Ordering)
      (b_cmp1 Ordering)
      (b_state_delta0 Delta)
      (b_state_delta1 Delta)""",
        "key": """\
      (b_read0 Int)
      (b_read1 Int)
      (b_key0 Key)
      (b_key1 Key)
      (b_cmp0 Ordering)
      (b_cmp1 Ordering)
      (b_state_delta0 Delta)
      (b_state_delta1 Delta)""",
        "partition": """\
      (b_read0 Int)
      (b_read1 Int)
      (b_pred0 Bool)
      (b_pred1 Bool)
      (b_state_delta0 Delta)
      (b_state_delta1 Delta)""",
    }[config.kind]
    output_fields = (
        "(y_index Int)"
        if config.kind == "partition"
        else "(y_is_ok Bool) (y_index Int)"
    )
    key_datatype = (
        "(declare-datatypes ((Key 0)) (((KLow) (KMid) (KHigh))))\n"
        if config.kind == "key"
        else ""
    )
    return f"""\
; Target: {config.target}
; Active contract SHA-256: {config.active_contract_sha256}
; Purpose is supplied below. Bounded domain: exactly two elements.
(set-logic ALL)
(declare-datatypes ((Ordering 0)) (((Less) (Equal) (Greater))))
(declare-datatypes ((Delta 0)) (((DNeg) (DZero) (DPos))))
{key_datatype}(declare-datatypes ((Input 0))
  (((mkInput
{input_fields}))))
(declare-datatypes ((Boundary 0))
  (((mkBoundary
{boundary_fields}))))
(declare-datatypes ((Output 0))
  (((mkOutput {output_fields}))))
(declare-datatypes ((State 0))
  (((mkState (s_callback_state Int)))))
(declare-const x Input)
(declare-const b Boundary)
(declare-const y1 Output)
(declare-const s1 State)
(declare-const y2 Output)
(declare-const s2 State)
(define-fun OrderingRank ((ordering Ordering)) Int
  (ite (= ordering Less) (- 1) (ite (= ordering Equal) 0 1)))
(define-fun OrderingObservation ((ordering Ordering)) Bool
  (or (= ordering Less) (= ordering Equal) (= ordering Greater)))
(define-fun DeltaValue ((delta Delta)) Int
  (ite (= delta DNeg) (- 1) (ite (= delta DZero) 0 1)))
(define-fun DeltaObservation ((delta Delta)) Bool
  (or (= delta DNeg) (= delta DZero) (= delta DPos)))
(define-fun LengthTwo ((x Input)) Bool
  (= (x_length x) 2))
(define-fun ElementReadsMatch ((x Input) (b Boundary)) Bool
  (and (= (b_read0 b) (x_element0 x))
       (= (b_read1 b) (x_element1 x))))
(define-fun CallbackStateAfterTwo ((x Input) (b Boundary)) Int
  (+ (x_callback_initial_state x)
     (DeltaValue (b_state_delta0 b))
     (DeltaValue (b_state_delta1 b))))
"""


def _search_equivalence(exact: bool) -> str:
    if exact:
        return """\
  (and (= (y_is_ok y1) (y_is_ok y2))
       (= (y_index y1) (y_index y2))
       (= (s_callback_state s1) (s_callback_state s2))))"""
    return """\
  (and (= (s_callback_state s1) (s_callback_state s2))
       (= (y_is_ok y1) (y_is_ok y2))
       (ite (y_is_ok y1)
            (and (EqualAt x b (y_index y1))
                 (EqualAt x b (y_index y2)))
            (= (y_index y1) (y_index y2)))))"""


def _ord_model(config: SearchTarget, purpose: str) -> str:
    boundary_extra = ""
    if purpose == config.sanity_purpose:
        boundary_extra = "\n       (SliceSortedByOrd x b)"
    elif purpose == EXACT_OUTPUT:
        boundary_extra = (
            "\n       (= (b_cmp0 b) Equal)"
            "\n       (= (b_cmp1 b) Equal)"
        )
    return _common_prefix(config) + f"""\
; Purpose: {purpose}
(define-fun CompareInt ((left Int) (right Int)) Ordering
  (ite (< left right) Less (ite (= left right) Equal Greater)))
(define-fun OrdComparisonAdapter ((x Input) (b Boundary)) Bool
  (and (= (b_cmp0 b) (CompareInt (b_read0 b) (x_search_value x)))
       (= (b_cmp1 b) (CompareInt (b_read1 b) (x_search_value x)))))
(define-fun SliceSortedByOrd ((x Input) (b Boundary)) Bool
  (<= (b_read0 b) (b_read1 b)))
(define-fun ComparatorProfileOrdered ((b Boundary)) Bool
  (<= (OrderingRank (b_cmp0 b)) (OrderingRank (b_cmp1 b))))
(define-fun OutputInBounds ((x Input) (y Output)) Bool
  (and (>= (y_index y) 0)
       (ite (y_is_ok y)
            (< (y_index y) (x_length x))
            (<= (y_index y) (x_length x)))))
(define-fun EqualAt ((x Input) (b Boundary) (index Int)) Bool
  (and (>= index 0)
       (< index (x_length x))
       (= (ite (= index 0) (b_cmp0 b) (b_cmp1 b)) Equal)))
(define-fun InsertionPoint ((x Input) (b Boundary) (index Int)) Bool
  (and (>= index 0)
       (<= index (x_length x))
       (=> (> index 0) (= (b_cmp0 b) Less))
       (=> (> index 1) (= (b_cmp1 b) Less))
       (=> (<= index 0) (= (b_cmp0 b) Greater))
       (=> (<= index 1) (= (b_cmp1 b) Greater))))
(define-fun GeneratedBinarySearchResult
  ((x Input) (b Boundary) (y Output)) Bool
  (and (OutputInBounds x y)
       (=>
         (SliceSortedByOrd x b)
         (ite (y_is_ok y)
              (EqualAt x b (y_index y))
              (InsertionPoint x b (y_index y))))))
(define-fun ReviewedBinarySearchByLowerResult
  ((x Input) (b Boundary) (y Output)) Bool
  (and (OutputInBounds x y)
       (=>
         (ComparatorProfileOrdered b)
         (ite (y_is_ok y)
              (EqualAt x b (y_index y))
              (InsertionPoint x b (y_index y))))))
(define-fun SourceBackedBinarySearchWrapper
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and (ElementReadsMatch x b)
       (OrdComparisonAdapter x b)
       (GeneratedBinarySearchResult x b y)
       (ReviewedBinarySearchByLowerResult x b y)
       (= (s_callback_state s) (CallbackStateAfterTwo x b))))
(define-fun Requires_T ((x Input)) Bool
  (LengthTwo x))
(define-fun Boundary_T ((x Input) (b Boundary)) Bool
  (and (ElementReadsMatch x b)
       (OrderingObservation (b_cmp0 b))
       (OrderingObservation (b_cmp1 b))
       (DeltaObservation (b_state_delta0 b))
       (DeltaObservation (b_state_delta1 b)){boundary_extra}))
(define-fun TargetDefinition_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (SourceBackedBinarySearchWrapper x b y s))
(define-fun Spec_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (TargetDefinition_T x b y s))
(define-fun Equivalent_T
  ((x Input) (b Boundary)
   (y1 Output) (s1 State) (y2 Output) (s2 State)) Bool
{_search_equivalence(purpose == EXACT_OUTPUT)}
"""


def _key_model(config: SearchTarget, purpose: str) -> str:
    boundary_extra = ""
    if purpose == config.sanity_purpose:
        boundary_extra = "\n       (ExtractedKeysOrdered b)"
    elif purpose == EXACT_OUTPUT:
        boundary_extra = (
            "\n       (= (b_cmp0 b) Equal)"
            "\n       (= (b_cmp1 b) Equal)"
        )
    return _common_prefix(config) + f"""\
; Purpose: {purpose}
(define-fun KeyRank ((key Key)) Int
  (ite (= key KLow) (- 1) (ite (= key KMid) 0 1)))
(define-fun KeyObservation ((key Key)) Bool
  (or (= key KLow) (= key KMid) (= key KHigh)))
(define-fun CompareKey ((left Key) (right Key)) Ordering
  (ite (< (KeyRank left) (KeyRank right))
       Less
       (ite (= left right) Equal Greater)))
(define-fun KeyExtractionAdapter ((b Boundary)) Bool
  (and (KeyObservation (b_key0 b))
       (KeyObservation (b_key1 b))))
(define-fun OrdComparisonAdapter ((x Input) (b Boundary)) Bool
  (and (= (b_cmp0 b) (CompareKey (b_key0 b) (x_search_key x)))
       (= (b_cmp1 b) (CompareKey (b_key1 b) (x_search_key x)))))
(define-fun ExtractedKeysOrdered ((b Boundary)) Bool
  (<= (KeyRank (b_key0 b)) (KeyRank (b_key1 b))))
(define-fun ComparatorProfileOrdered ((b Boundary)) Bool
  (<= (OrderingRank (b_cmp0 b)) (OrderingRank (b_cmp1 b))))
(define-fun OutputInBounds ((x Input) (y Output)) Bool
  (and (>= (y_index y) 0)
       (ite (y_is_ok y)
            (< (y_index y) (x_length x))
            (<= (y_index y) (x_length x)))))
(define-fun EqualAt ((x Input) (b Boundary) (index Int)) Bool
  (and (>= index 0)
       (< index (x_length x))
       (= (ite (= index 0) (b_cmp0 b) (b_cmp1 b)) Equal)))
(define-fun InsertionPoint ((x Input) (b Boundary) (index Int)) Bool
  (and (>= index 0)
       (<= index (x_length x))
       (=> (> index 0) (= (b_cmp0 b) Less))
       (=> (> index 1) (= (b_cmp1 b) Less))
       (=> (<= index 0) (= (b_cmp0 b) Greater))
       (=> (<= index 1) (= (b_cmp1 b) Greater))))
(define-fun GeneratedBinarySearchByKeyResult
  ((x Input) (b Boundary) (y Output)) Bool
  (and (OutputInBounds x y)
       (=>
         (ExtractedKeysOrdered b)
         (ite (y_is_ok y)
              (EqualAt x b (y_index y))
              (InsertionPoint x b (y_index y))))))
(define-fun ReviewedBinarySearchByLowerResult
  ((x Input) (b Boundary) (y Output)) Bool
  (and (OutputInBounds x y)
       (=>
         (ComparatorProfileOrdered b)
         (ite (y_is_ok y)
              (EqualAt x b (y_index y))
              (InsertionPoint x b (y_index y))))))
(define-fun SourceBackedBinarySearchByKeyWrapper
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and (ElementReadsMatch x b)
       (KeyExtractionAdapter b)
       (OrdComparisonAdapter x b)
       (GeneratedBinarySearchByKeyResult x b y)
       (ReviewedBinarySearchByLowerResult x b y)
       (= (s_callback_state s) (CallbackStateAfterTwo x b))))
(define-fun Requires_T ((x Input)) Bool
  (LengthTwo x))
(define-fun Boundary_T ((x Input) (b Boundary)) Bool
  (and (ElementReadsMatch x b)
       (KeyExtractionAdapter b)
       (OrderingObservation (b_cmp0 b))
       (OrderingObservation (b_cmp1 b))
       (DeltaObservation (b_state_delta0 b))
       (DeltaObservation (b_state_delta1 b)){boundary_extra}))
(define-fun TargetDefinition_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (SourceBackedBinarySearchByKeyWrapper x b y s))
(define-fun Spec_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (TargetDefinition_T x b y s))
(define-fun Equivalent_T
  ((x Input) (b Boundary)
   (y1 Output) (s1 State) (y2 Output) (s2 State)) Bool
{_search_equivalence(purpose == EXACT_OUTPUT)}
"""


def _partition_model(config: SearchTarget, purpose: str) -> str:
    boundary_extra = (
        "\n       (PredicateProfilePartitioned b)"
        if purpose == config.sanity_purpose
        else ""
    )
    return _common_prefix(config) + f"""\
; Purpose: {purpose}
(define-fun PredicateObservation ((value Bool)) Bool
  (or value (not value)))
(define-fun PredicateToOrdering ((value Bool)) Ordering
  (ite value Less Greater))
(define-fun PredicateProfilePartitioned ((b Boundary)) Bool
  (=> (b_pred1 b) (b_pred0 b)))
(define-fun ComparatorProfileOrdered ((b Boundary)) Bool
  (<= (OrderingRank (PredicateToOrdering (b_pred0 b)))
      (OrderingRank (PredicateToOrdering (b_pred1 b)))))
(define-fun IndexInBounds ((x Input) (index Int)) Bool
  (and (>= index 0) (<= index (x_length x))))
(define-fun PartitionPointAt ((x Input) (b Boundary) (index Int)) Bool
  (and (IndexInBounds x index)
       (=> (> index 0) (b_pred0 b))
       (=> (> index 1) (b_pred1 b))
       (=> (<= index 0) (not (b_pred0 b)))
       (=> (<= index 1) (not (b_pred1 b)))))
(define-fun GeneratedPartitionPointResult
  ((x Input) (b Boundary) (y Output)) Bool
  (and (IndexInBounds x (y_index y))
       (=> (PredicateProfilePartitioned b)
           (PartitionPointAt x b (y_index y)))))
(define-fun LowerEqualAt ((x Input) (b Boundary) (index Int)) Bool
  (and (>= index 0)
       (< index (x_length x))
       (= (ite (= index 0)
               (PredicateToOrdering (b_pred0 b))
               (PredicateToOrdering (b_pred1 b)))
          Equal)))
(define-fun LowerInsertionPoint ((x Input) (b Boundary) (index Int)) Bool
  (and (IndexInBounds x index)
       (=> (> index 0) (= (PredicateToOrdering (b_pred0 b)) Less))
       (=> (> index 1) (= (PredicateToOrdering (b_pred1 b)) Less))
       (=> (<= index 0) (= (PredicateToOrdering (b_pred0 b)) Greater))
       (=> (<= index 1) (= (PredicateToOrdering (b_pred1 b)) Greater))))
(define-fun ReviewedBinarySearchByLowerResult
  ((x Input) (b Boundary) (is_ok Bool) (index Int)) Bool
  (and (>= index 0)
       (ite is_ok (< index (x_length x)) (<= index (x_length x)))
       (=>
         (ComparatorProfileOrdered b)
         (ite is_ok
              (LowerEqualAt x b index)
              (LowerInsertionPoint x b index)))))
(define-fun UnwrapOrElseIdentity
  ((is_ok Bool) (index Int) (y Output)) Bool
  (= (y_index y) index))
(define-fun SourceBackedPartitionPointWrapper
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and (ElementReadsMatch x b)
       (GeneratedPartitionPointResult x b y)
       (or
         (and (ReviewedBinarySearchByLowerResult x b true (y_index y))
              (UnwrapOrElseIdentity true (y_index y) y))
         (and (ReviewedBinarySearchByLowerResult x b false (y_index y))
              (UnwrapOrElseIdentity false (y_index y) y)))
       (= (s_callback_state s) (CallbackStateAfterTwo x b))))
(define-fun Requires_T ((x Input)) Bool
  (LengthTwo x))
(define-fun Boundary_T ((x Input) (b Boundary)) Bool
  (and (ElementReadsMatch x b)
       (PredicateObservation (b_pred0 b))
       (PredicateObservation (b_pred1 b))
       (DeltaObservation (b_state_delta0 b))
       (DeltaObservation (b_state_delta1 b)){boundary_extra}))
(define-fun TargetDefinition_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (SourceBackedPartitionPointWrapper x b y s))
(define-fun Spec_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (TargetDefinition_T x b y s))
(define-fun Equivalent_T
  ((x Input) (b Boundary)
   (y1 Output) (s1 State) (y2 Output) (s2 State)) Bool
  (and (= (y_index y1) (y_index y2))
       (= (s_callback_state s1) (s_callback_state s2))))
"""


def model_text(config: SearchTarget, purpose: str) -> str:
    if purpose not in config.purposes:
        raise ValueError(f"{config.label}: unknown obligation purpose {purpose}")
    if config.kind == "ord":
        return _ord_model(config, purpose)
    if config.kind == "key":
        return _key_model(config, purpose)
    if config.kind == "partition":
        return _partition_model(config, purpose)
    raise ValueError(f"{config.label}: unknown model kind {config.kind}")


def obligation_text(config: SearchTarget, purpose: str) -> str:
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


def _field(
    selector: str,
    role: str,
    citations: list[str],
    trust_sites: list[str],
) -> dict[str, Any]:
    return {
        "selector": selector,
        "role": role,
        "source_citations": citations,
        "trust_site_ids": trust_sites,
        "source_backed_replacement_ids": [],
    }


def _boundary_fields(config: SearchTarget) -> list[dict[str, Any]]:
    lower = "core/src/slice/mod.rs:2970-3022"
    target = config.source_reference
    if config.kind == "ord":
        trust = ["TS-028-E002"]
        return [
            _field("b_read0", "callback_argument", [target, lower], trust),
            _field("b_read1", "callback_argument", [target, lower], trust),
            _field("b_cmp0", "callback_result", [target], trust),
            _field("b_cmp1", "callback_result", [target], trust),
            _field(
                "b_state_delta0",
                "callback_state_transition",
                [target],
                trust,
            ),
            _field(
                "b_state_delta1",
                "callback_state_transition",
                [target],
                trust,
            ),
        ]
    if config.kind == "key":
        return [
            _field(
                "b_read0",
                "callback_argument",
                [target, lower],
                ["TS-030-D002"],
            ),
            _field(
                "b_read1",
                "callback_argument",
                [target, lower],
                ["TS-030-D002"],
            ),
            _field(
                "b_key0",
                "callback_result",
                [target],
                ["TS-030-D003"],
            ),
            _field(
                "b_key1",
                "callback_result",
                [target],
                ["TS-030-D003"],
            ),
            _field(
                "b_cmp0",
                "callback_result",
                [target],
                ["TS-030-D004"],
            ),
            _field(
                "b_cmp1",
                "callback_result",
                [target],
                ["TS-030-D004"],
            ),
            _field(
                "b_state_delta0",
                "callback_state_transition",
                [target],
                ["TS-030-D003"],
            ),
            _field(
                "b_state_delta1",
                "callback_state_transition",
                [target],
                ["TS-030-D003"],
            ),
        ]
    return [
        _field(
            "b_read0",
            "callback_argument",
            [target, lower],
            ["TS-065-D003"],
        ),
        _field(
            "b_read1",
            "callback_argument",
            [target, lower],
            ["TS-065-D003"],
        ),
        _field(
            "b_pred0",
            "callback_result",
            [target],
            ["TS-065-D003"],
        ),
        _field(
            "b_pred1",
            "callback_result",
            [target],
            ["TS-065-D003"],
        ),
        _field(
            "b_state_delta0",
            "callback_state_transition",
            [target],
            ["TS-065-D003"],
        ),
        _field(
            "b_state_delta1",
            "callback_state_transition",
            [target],
            ["TS-065-D003"],
        ),
    ]


def _shared_observations(config: SearchTarget) -> list[str]:
    if config.kind == "ord":
        return [
            "source element reads passed to Ord::cmp",
            "per-element Ord comparison outcomes against the search value",
            "per-call comparison state-transition deltas",
        ]
    if config.kind == "key":
        return [
            "source elements passed to the key callback",
            "per-element extracted key values",
            "per-key Ord comparison outcomes against the search key",
            "per-call key-callback state-transition deltas",
        ]
    return [
        "source elements passed to the predicate callback",
        "per-element predicate outcomes",
        "per-call predicate state-transition deltas",
    ]


def _replacement(config: SearchTarget) -> dict[str, Any]:
    return {
        "replacement_id": config.replacement_id,
        "operation": config.replacement_operation,
        "symbols": [config.replacement_symbol],
        "source_citations": list(config.replacement_citations),
        "replaces_trust_site_ids": list(
            config.excluded_retained_trust_sites
        ),
    }


def obligation_metadata(
    config: SearchTarget, purpose: str
) -> dict[str, Any]:
    if purpose not in config.purposes:
        raise ValueError(f"{config.label}: unknown obligation purpose {purpose}")
    principal = (
        [
            {
                "selector": "y_index",
                "left": "output1",
                "right": "output2",
                "sort": "Int",
            }
        ]
        if config.kind == "partition"
        else [
            {
                "selector": "y_is_ok",
                "left": "output1",
                "right": "output2",
                "sort": "Bool",
            },
            {
                "selector": "y_index",
                "left": "output1",
                "right": "output2",
                "sort": "Int",
            },
        ]
    )
    principal.append(
        {
            "selector": "s_callback_state",
            "left": "state1",
            "right": "state2",
            "sort": "Int",
        }
    )
    metadata: dict[str, Any] = {
        "schema_version": 3,
        "target": config.target,
        "input_order": config.input_order,
        "obligation_purpose": purpose,
        "active_contract_sha256": config.active_contract_sha256,
        "active_contract_text": config.active_contract_text,
        "bounded_domain": {
            "length": 2,
            "requires_adds_sortedness_or_partitioning": False,
            "boundary_profile": (
                "ordered"
                if purpose == config.sanity_purpose and config.kind != "partition"
                else "partitioned"
                if purpose == config.sanity_purpose
                else "duplicate-match"
                if purpose == EXACT_OUTPUT and config.weak_equivalence
                else "all comparator or predicate profiles"
            ),
            "callback_transition_profile": (
                "two source observations with independently fixed deltas"
            ),
        },
        "contract_translation": {
            "generated_relation": (
                "unconditional result/index bounds plus the generated "
                "ordered-or-partitioned implication"
            ),
            "lower_transition": (
                "the accepted binary_search_by relation over the wrapper's "
                "derived comparator observations"
            ),
            "wrapper": config.replacement_operation,
        },
        "boundary_scope": {
            "shared_observations": _shared_observations(config),
            "excluded_observations": [
                "selected index",
                "returned Result",
                "aggregate callback final state",
                "answer-equivalent encoding",
                "selected or complete execution trace",
            ],
            "admitted_trust_site_ids": list(
                config.admitted_boundary_trust_sites
            ),
            "excluded_retained_trust_site_ids": list(
                config.excluded_retained_trust_sites
            ),
            "context_only_trust_site_ids": list(
                config.context_only_trust_sites
            ),
            "all_audited_trust_site_ids": list(
                config.all_audited_trust_sites
            ),
            "source_backed_replacement_ids": [],
            "narrower_than_target": True,
        },
        "target_definition": "TargetDefinition_T",
        "theorem_variables": {
            "input": "x",
            "boundary": "b",
            "output1": "y1",
            "state1": "s1",
            "output2": "y2",
            "state2": "s2",
        },
        "boundary_fields": _boundary_fields(config),
        "source_backed_replacements": [_replacement(config)],
        "declared_functions": [],
        "source_transition_definitions": [config.replacement_symbol],
        "source_transition_bindings": {
            "wrapper": {
                "symbols": [config.replacement_symbol],
                "source_citations": list(config.replacement_citations),
                "replaces_trust_site_ids": list(
                    config.excluded_retained_trust_sites
                ),
                "accepted_lower_dependency": {
                    "target": LOWER_TARGET,
                    "artifact_id": LOWER_ARTIFACT_ID,
                    "active_contract_sha256": LOWER_ACTIVE_CONTRACT_SHA256,
                    "mode": (
                        "reviewed relational transition; no lower Result or "
                        "selected index enters Boundary_T"
                    ),
                },
            }
        },
        "equivalence_kind": (
            "exact"
            if config.kind == "partition" or purpose == EXACT_OUTPUT
            else "matching-index-equivalence"
        ),
        "principal_observations": principal,
        "expected_solver_result": (
            "unsat" if purpose == config.sanity_purpose else "sat"
        ),
    }
    if config.weak_equivalence and purpose != EXACT_OUTPUT:
        metadata["weak_equivalence_review"] = {
            "source_citations": [
                config.docs_reference,
                "core/src/slice/mod.rs:2849-2967",
            ],
            "positive_witness": POSITIVE_EQUIVALENCE_WITNESS,
            "negative_witness": NEGATIVE_EQUIVALENCE_WITNESS,
            "policy": (
                "Result tags and callback final state are exact. Err indices "
                "are exact. Distinct Ok indices are equivalent only when both "
                "identify matching elements under the shared observations."
            ),
        }
    return metadata


def obligation(
    config: SearchTarget, purpose: str
) -> tuple[str, dict[str, Any]]:
    return obligation_text(config, purpose), obligation_metadata(config, purpose)


def validate_target_obligation(
    config: SearchTarget, text: str, metadata: dict[str, Any]
) -> None:
    validate_obligation(text, metadata)
    purpose = metadata.get("obligation_purpose")
    if purpose not in config.purposes:
        raise GuardError(f"{config.label}: obligation has an unknown purpose")
    expected_text, expected_metadata = obligation(config, str(purpose))
    if metadata != expected_metadata:
        raise GuardError(
            f"{config.label}: metadata differs from the reviewed source translation"
        )
    if parse_smt(text) != parse_smt(expected_text):
        raise GuardError(
            f"{config.label}: SMT differs from the reviewed source translation"
        )


def boundary_manifest(config: SearchTarget) -> dict[str, Any]:
    return {
        "schema_version": 2,
        "target": config.target,
        "input_order": config.input_order,
        "model_boundary_admissibility": "admissible",
        "model_boundary_narrower_than_target": True,
        "retained_boundary_admissibility": "inadmissible",
        "shared_boundary_observations": _shared_observations(config),
        "excluded_observations": [
            "selected index",
            "returned Result",
            "aggregate callback final state",
            "answer-equivalent encoding",
            "selected or complete execution trace",
        ],
        "admitted_boundary_trust_site_ids": list(
            config.admitted_boundary_trust_sites
        ),
        "context_only_trust_site_ids": list(
            config.context_only_trust_sites
        ),
        "excluded_retained_sites": [
            {
                "trust_site_id": trust_site,
                "disposition": "replaced-not-relabeled",
                "replacement_id": config.replacement_id,
            }
            for trust_site in config.excluded_retained_trust_sites
        ],
        "source_backed_replacements": [_replacement(config)],
        "accepted_lower_dependency": {
            "target": LOWER_TARGET,
            "artifact_id": LOWER_ARTIFACT_ID,
            "active_contract_sha256": LOWER_ACTIVE_CONTRACT_SHA256,
            "admission": (
                "defined relational transition only; no selected index or "
                "returned Result is a boundary observation"
            ),
        },
    }


def witness_payload(config: SearchTarget) -> dict[str, Any]:
    common = {
        "schema_version": 1,
        "target": config.target,
        "input_order": config.input_order,
        "active_contract_sha256": config.active_contract_sha256,
    }
    if config.kind == "ord":
        common.update(
            {
                "general_counterexample": {
                    "input": {
                        "length": 2,
                        "elements": [20, 10],
                        "search_value": 15,
                        "callback_initial_state": 7,
                    },
                    "boundary": {
                        "element_reads": [20, 10],
                        "comparator_results": ["Greater", "Less"],
                        "callback_state_deltas": [0, 0],
                    },
                    "execution1": {
                        "result": {"tag": "Ok", "index": 0},
                        "callback_final_state": 7,
                    },
                    "execution2": {
                        "result": {"tag": "Err", "index": 0},
                        "callback_final_state": 7,
                    },
                    "expected": {
                        "domain_profile": "unordered",
                        "execution1_satisfies_contract": True,
                        "execution2_satisfies_contract": True,
                        "reviewed_equivalent": False,
                    },
                },
                "exact_output_counterexample": {
                    "input": {
                        "length": 2,
                        "elements": [10, 10],
                        "search_value": 10,
                        "callback_initial_state": 7,
                    },
                    "boundary": {
                        "element_reads": [10, 10],
                        "comparator_results": ["Equal", "Equal"],
                        "callback_state_deltas": [0, 0],
                    },
                    "execution1": {
                        "result": {"tag": "Ok", "index": 0},
                        "callback_final_state": 7,
                    },
                    "execution2": {
                        "result": {"tag": "Ok", "index": 1},
                        "callback_final_state": 7,
                    },
                    "expected": {
                        "domain_profile": "ordered",
                        "execution1_satisfies_contract": True,
                        "execution2_satisfies_contract": True,
                        "matching_index_equivalent": True,
                        "exactly_equal": False,
                    },
                },
            }
        )
    elif config.kind == "key":
        common.update(
            {
                "general_counterexample": {
                    "input": {
                        "length": 2,
                        "elements": [100, 200],
                        "search_key": "KMid",
                        "callback_initial_state": 7,
                    },
                    "boundary": {
                        "element_reads": [100, 200],
                        "extracted_keys": ["KHigh", "KLow"],
                        "comparator_results": ["Greater", "Less"],
                        "callback_state_deltas": [0, 0],
                    },
                    "execution1": {
                        "result": {"tag": "Ok", "index": 0},
                        "callback_final_state": 7,
                    },
                    "execution2": {
                        "result": {"tag": "Err", "index": 0},
                        "callback_final_state": 7,
                    },
                    "expected": {
                        "domain_profile": "unordered",
                        "execution1_satisfies_contract": True,
                        "execution2_satisfies_contract": True,
                        "reviewed_equivalent": False,
                    },
                },
                "exact_output_counterexample": {
                    "input": {
                        "length": 2,
                        "elements": [100, 200],
                        "search_key": "KMid",
                        "callback_initial_state": 7,
                    },
                    "boundary": {
                        "element_reads": [100, 200],
                        "extracted_keys": ["KMid", "KMid"],
                        "comparator_results": ["Equal", "Equal"],
                        "callback_state_deltas": [0, 0],
                    },
                    "execution1": {
                        "result": {"tag": "Ok", "index": 0},
                        "callback_final_state": 7,
                    },
                    "execution2": {
                        "result": {"tag": "Ok", "index": 1},
                        "callback_final_state": 7,
                    },
                    "expected": {
                        "domain_profile": "ordered",
                        "execution1_satisfies_contract": True,
                        "execution2_satisfies_contract": True,
                        "matching_index_equivalent": True,
                        "exactly_equal": False,
                    },
                },
            }
        )
    else:
        common.update(
            {
                "general_counterexample": {
                    "input": {
                        "length": 2,
                        "elements": [100, 200],
                        "callback_initial_state": 7,
                    },
                    "boundary": {
                        "element_reads": [100, 200],
                        "predicate_results": [False, True],
                        "callback_state_deltas": [0, 0],
                    },
                    "execution1": {
                        "index": 0,
                        "callback_final_state": 7,
                    },
                    "execution2": {
                        "index": 1,
                        "callback_final_state": 7,
                    },
                    "expected": {
                        "domain_profile": "non-partitioned",
                        "execution1_satisfies_contract": True,
                        "execution2_satisfies_contract": True,
                        "exactly_equal": False,
                    },
                },
                "exact_output_counterexample": {
                    "input": {
                        "length": 2,
                        "elements": [100, 200],
                        "callback_initial_state": 7,
                    },
                    "boundary": {
                        "element_reads": [100, 200],
                        "predicate_results": [False, True],
                        "callback_state_deltas": [0, 0],
                    },
                    "execution1": {
                        "index": 0,
                        "callback_final_state": 7,
                    },
                    "execution2": {
                        "index": 2,
                        "callback_final_state": 7,
                    },
                    "expected": {
                        "domain_profile": "non-partitioned",
                        "execution1_satisfies_contract": True,
                        "execution2_satisfies_contract": True,
                        "exactly_equal": False,
                    },
                },
            }
        )
    return common


def _fixed_values(config: SearchTarget, purpose: str) -> tuple[str, str, str, str]:
    if purpose not in {PRIMARY, EXACT_OUTPUT}:
        raise ValueError("fixed models exist only for SAT obligations")
    if config.kind == "ord":
        if purpose == PRIMARY:
            return (
                "(mkInput 2 20 10 15 7)",
                "(mkBoundary 20 10 Greater Less DZero DZero)",
                "(mkOutput true 0)",
                "(mkOutput false 0)",
            )
        return (
            "(mkInput 2 10 10 10 7)",
            "(mkBoundary 10 10 Equal Equal DZero DZero)",
            "(mkOutput true 0)",
            "(mkOutput true 1)",
        )
    if config.kind == "key":
        if purpose == PRIMARY:
            return (
                "(mkInput 2 100 200 KMid 7)",
                "(mkBoundary 100 200 KHigh KLow Greater Less DZero DZero)",
                "(mkOutput true 0)",
                "(mkOutput false 0)",
            )
        return (
            "(mkInput 2 100 200 KMid 7)",
            "(mkBoundary 100 200 KMid KMid Equal Equal DZero DZero)",
            "(mkOutput true 0)",
            "(mkOutput true 1)",
        )
    if purpose == PRIMARY:
        return (
            "(mkInput 2 100 200 7)",
            "(mkBoundary 100 200 false true DZero DZero)",
            "(mkOutput 0)",
            "(mkOutput 1)",
        )
    return (
        "(mkInput 2 100 200 7)",
        "(mkBoundary 100 200 false true DZero DZero)",
        "(mkOutput 0)",
        "(mkOutput 2)",
    )


def fixed_model_text(config: SearchTarget, purpose: str) -> str:
    text = obligation_text(config, purpose)
    terminal = "(check-sat)\n"
    if not text.endswith(terminal):
        raise ValueError("target obligation lacks the expected terminal check-sat")
    input_value, boundary, output1, output2 = _fixed_values(config, purpose)
    value_terms = (
        """\
  (y_is_ok y1)
  (y_index y1)
  (y_is_ok y2)
  (y_index y2)"""
        if config.kind != "partition"
        else """\
  (y_index y1)
  (y_index y2)"""
    )
    return (
        text[: -len(terminal)]
        + f"""\
(assert (= x {input_value}))
(assert (= b {boundary}))
(assert (= y1 {output1}))
(assert (= s1 (mkState 7)))
(assert (= y2 {output2}))
(assert (= s2 (mkState 7)))
(check-sat)
(get-value (
  (x_length x)
{value_terms}
  (s_callback_state s1)
  (s_callback_state s2)))
"""
    )
