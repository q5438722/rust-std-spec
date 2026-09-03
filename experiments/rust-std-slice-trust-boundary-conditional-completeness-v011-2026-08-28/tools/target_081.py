#!/usr/bin/env python3
"""Bounded active-contract model for input order 81, sort_unstable_by."""

from __future__ import annotations

from typing import Any

from checker_guards import GuardError, parse_smt, validate_obligation


TARGET = "core::slice::sort_unstable_by"
INPUT_ORDER = "81"
ARTIFACT_ID = "081_core_slice_sort_unstable_by"
ACTIVE_CONTRACT_SHA256 = (
    "420e250d3b0ae471b64eb3d6474588eaec8acfc7644b5c1dd4420e4c1b2c0597"
)
ACTIVE_CONTRACT_TEXT = (
    "pub assume_specification<T, F: core::ops::FnMut(&T, &T) -> "
    "core::cmp::Ordering>[ <[T]>::sort_unstable_by::<F> ]( slice: &mut [T], "
    "compare: F, ) ensures slice_permutation(old(slice)@, final(slice)@), "
    "slice_sorted_by_cmp(final(slice)@, comparator_observation(compare, "
    "old(slice)@)), ;"
)

PRIMARY = "completeness-modulo-reviewed-equivalence"
TOTAL_ORDER_SANITY = "total-order-sanity"
EXACT_FINAL_SLICE = "exact-final-slice-determinism"
PURPOSES = (PRIMARY, TOTAL_ORDER_SANITY, EXACT_FINAL_SLICE)

SOURCE_CITATIONS = [
    "core/src/slice/mod.rs:3140-3185",
    "core/src/slice/mod.rs:3188-3193",
    "core/src/slice/sort/unstable/mod.rs:22-58",
    "core/src/slice/sort/shared/smallsort.rs:540-604",
]
POSITIVE_EQUIVALENCE_WITNESS = (
    "evidence/equivalence/unstable_sort_equal_keys.positive.smt2"
)
NEGATIVE_EQUIVALENCE_WITNESS = (
    "evidence/equivalence/unstable_sort_equal_keys.negative.smt2"
)
EXCLUDED_RETAINED_TRUST_SITES = (
    "TS-081-D002",
    "TS-081-D003",
    "TS-081-E001",
)
ALL_AUDITED_TRUST_SITES = (
    "TS-081-D001",
    "TS-081-D002",
    "TS-081-D003",
    "TS-081-D004",
    "TS-081-C001",
    "TS-081-E001",
)
COMPARATOR_FIELDS = tuple(
    f"b_cmp{left}{right}" for left in range(3) for right in range(3)
)
OUTPUT_FIELDS = (("y_return_unit", "Bool"),)
STATE_FIELDS = (
    ("s_final0", "Int"),
    ("s_final1", "Int"),
    ("s_final2", "Int"),
    ("s_callback_state", "Int"),
)
ACTIVE_CONJUNCT_SYMBOLS = (
    "GeneratedPermutation",
    "GeneratedComparatorSortedness",
)


def _boundary_declaration() -> str:
    fields = [
        "(b_id0 Int)",
        "(b_id1 Int)",
        "(b_id2 Int)",
        *(f"({selector} Ordering)" for selector in COMPARATOR_FIELDS),
        "(b_callback_state_delta Int)",
    ]
    return "\n      ".join(fields)


def _ordering_validity() -> str:
    return "\n       ".join(
        f"(OrderingObservation ({selector} b))"
        for selector in COMPARATOR_FIELDS
    )


def _observed_ordering_body() -> str:
    rows = []
    for left in range(3):
        row = (
            f"(ite (= right (b_id0 b)) (b_cmp{left}0 b)\n"
            f"             (ite (= right (b_id1 b)) (b_cmp{left}1 b) "
            f"(b_cmp{left}2 b)))"
        )
        rows.append(row)
    return (
        f"(ite (= left (b_id0 b)) {rows[0]}\n"
        f"       (ite (= left (b_id1 b)) {rows[1]} {rows[2]}))"
    )


def _transitivity_clauses() -> str:
    identities = [f"(b_id{index} b)" for index in range(3)]
    clauses = [
        "(ComparatorLeqTransitive\n"
        f"         (ObservedOrdering b {left} {middle})\n"
        f"         (ObservedOrdering b {middle} {right})\n"
        f"         (ObservedOrdering b {left} {right}))"
        for left in identities
        for middle in identities
        for right in identities
    ]
    return "\n       ".join(clauses)


def _boundary_body(purpose: str) -> str:
    total_order = (
        "\n       (TotalOrderProfile x b)"
        if purpose == TOTAL_ORDER_SANITY
        else ""
    )
    return f"""\
  (and (BoundaryIdsMatch x b)
       {_ordering_validity()}
       (= (b_callback_state_delta b) 0){total_order}))"""


def _equivalence_body(purpose: str) -> str:
    if purpose == EXACT_FINAL_SLICE:
        return """\
  (and (= (y_return_unit y1) (y_return_unit y2))
       (= (s_final0 s1) (s_final0 s2))
       (= (s_final1 s1) (s_final1 s2))
       (= (s_final2 s1) (s_final2 s2))
       (= (s_callback_state s1) (s_callback_state s2))))"""
    return """\
  (and (= (y_return_unit y1) (y_return_unit y2))
       (= (s_callback_state s1) (s_callback_state s2))
       (SameElementMultiset s1 s2)
       (ComparatorEquivalent b (s_final0 s1) (s_final0 s2))
       (ComparatorEquivalent b (s_final1 s1) (s_final1 s2))
       (ComparatorEquivalent b (s_final2 s1) (s_final2 s2))))"""


def obligation_text(purpose: str) -> str:
    if purpose not in PURPOSES:
        raise ValueError(f"unknown target-081 obligation purpose: {purpose}")
    return f"""\
; Target: {TARGET}
; Active contract SHA-256: {ACTIVE_CONTRACT_SHA256}
; Purpose: {purpose}
; Bounded domain: three distinct input identities and no total-order precondition,
; except in the separately reported total-order sanity obligation.
(set-logic ALL)
(declare-datatypes ((Ordering 0)) (((Less) (Equal) (Greater))))
(declare-datatypes ((Input 0))
  (((mkInput
      (x_id0 Int)
      (x_id1 Int)
      (x_id2 Int)
      (x_callback_initial_state Int)))))
(declare-datatypes ((Boundary 0))
  (((mkBoundary
      {_boundary_declaration()}))))
(declare-datatypes ((Output 0))
  (((mkOutput (y_return_unit Bool)))))
(declare-datatypes ((State 0))
  (((mkState
      (s_final0 Int)
      (s_final1 Int)
      (s_final2 Int)
      (s_callback_state Int)))))
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
(define-fun ComparatorLeqResult ((ordering Ordering)) Bool
  (<= (OrderingRank ordering) 0))
(define-fun ComparatorLeqTransitive
  ((left_middle Ordering) (middle_right Ordering) (left_right Ordering)) Bool
  (=> (and (ComparatorLeqResult left_middle)
           (ComparatorLeqResult middle_right))
      (ComparatorLeqResult left_right)))
(define-fun OrderingDual ((left Ordering) (right Ordering)) Bool
  (or (and (= left Less) (= right Greater))
      (and (= left Equal) (= right Equal))
      (and (= left Greater) (= right Less))))
(define-fun DistinctInput ((x Input)) Bool
  (and (distinct (x_id0 x) (x_id1 x) (x_id2 x))))
(define-fun BoundaryIdsMatch ((x Input) (b Boundary)) Bool
  (and (= (b_id0 b) (x_id0 x))
       (= (b_id1 b) (x_id1 x))
       (= (b_id2 b) (x_id2 x))))
(define-fun ObservedOrdering
  ((b Boundary) (left Int) (right Int)) Ordering
  {_observed_ordering_body()})
(define-fun ComparatorLeq
  ((b Boundary) (left Int) (right Int)) Bool
  (ComparatorLeqResult (ObservedOrdering b left right)))
(define-fun ComparatorEquivalent
  ((b Boundary) (left Int) (right Int)) Bool
  (and (= (ObservedOrdering b left right) Equal)
       (= (ObservedOrdering b right left) Equal)))
(define-fun InputMultiplicity ((x Input) (identity Int)) Int
  (+ (ite (= (x_id0 x) identity) 1 0)
     (ite (= (x_id1 x) identity) 1 0)
     (ite (= (x_id2 x) identity) 1 0)))
(define-fun FinalMultiplicity ((s State) (identity Int)) Int
  (+ (ite (= (s_final0 s) identity) 1 0)
     (ite (= (s_final1 s) identity) 1 0)
     (ite (= (s_final2 s) identity) 1 0)))
(define-fun GeneratedPermutation ((x Input) (s State)) Bool
  (and
    (= (InputMultiplicity x (x_id0 x))
       (FinalMultiplicity s (x_id0 x)))
    (= (InputMultiplicity x (x_id1 x))
       (FinalMultiplicity s (x_id1 x)))
    (= (InputMultiplicity x (x_id2 x))
       (FinalMultiplicity s (x_id2 x)))
    (= (InputMultiplicity x (s_final0 s))
       (FinalMultiplicity s (s_final0 s)))
    (= (InputMultiplicity x (s_final1 s))
       (FinalMultiplicity s (s_final1 s)))
    (= (InputMultiplicity x (s_final2 s))
       (FinalMultiplicity s (s_final2 s)))))
(define-fun GeneratedComparatorSortedness
  ((x Input) (b Boundary) (s State)) Bool
  (and
    (BoundaryIdsMatch x b)
    (ComparatorLeq b (s_final0 s) (s_final0 s))
    (ComparatorLeq b (s_final0 s) (s_final1 s))
    (ComparatorLeq b (s_final0 s) (s_final2 s))
    (ComparatorLeq b (s_final1 s) (s_final1 s))
    (ComparatorLeq b (s_final1 s) (s_final2 s))
    (ComparatorLeq b (s_final2 s) (s_final2 s))))
(define-fun SameElementMultiset ((left State) (right State)) Bool
  (and
    (= (FinalMultiplicity left (s_final0 left))
       (FinalMultiplicity right (s_final0 left)))
    (= (FinalMultiplicity left (s_final1 left))
       (FinalMultiplicity right (s_final1 left)))
    (= (FinalMultiplicity left (s_final2 left))
       (FinalMultiplicity right (s_final2 left)))
    (= (FinalMultiplicity left (s_final0 right))
       (FinalMultiplicity right (s_final0 right)))
    (= (FinalMultiplicity left (s_final1 right))
       (FinalMultiplicity right (s_final1 right)))
    (= (FinalMultiplicity left (s_final2 right))
       (FinalMultiplicity right (s_final2 right)))))
(define-fun TotalOrderProfile ((x Input) (b Boundary)) Bool
  (and
    (BoundaryIdsMatch x b)
    (= (ObservedOrdering b (b_id0 b) (b_id0 b)) Equal)
    (= (ObservedOrdering b (b_id1 b) (b_id1 b)) Equal)
    (= (ObservedOrdering b (b_id2 b) (b_id2 b)) Equal)
    (OrderingDual
      (ObservedOrdering b (b_id0 b) (b_id1 b))
      (ObservedOrdering b (b_id1 b) (b_id0 b)))
    (OrderingDual
      (ObservedOrdering b (b_id0 b) (b_id2 b))
      (ObservedOrdering b (b_id2 b) (b_id0 b)))
    (OrderingDual
      (ObservedOrdering b (b_id1 b) (b_id2 b))
      (ObservedOrdering b (b_id2 b) (b_id1 b)))
    {_transitivity_clauses()}))
(define-fun CallbackStateAfterSort ((x Input) (b Boundary)) Int
  (+ (x_callback_initial_state x) (b_callback_state_delta b)))
(define-fun UnitReturnAfterSort ((x Input)) Bool
  (= (x_id0 x) (x_id0 x)))
(define-fun Requires_T ((x Input)) Bool
  (DistinctInput x))
(define-fun Boundary_T ((x Input) (b Boundary)) Bool
{_boundary_body(purpose)}
(define-fun TargetDefinition_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and (GeneratedPermutation x s)
       (GeneratedComparatorSortedness x b s)
       (= (y_return_unit y) (UnitReturnAfterSort x))
       (= (s_callback_state s) (CallbackStateAfterSort x b))))
(define-fun Spec_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (TargetDefinition_T x b y s))
(define-fun Equivalent_T
  ((x Input) (b Boundary)
   (y1 Output) (s1 State) (y2 Output) (s2 State)) Bool
{_equivalence_body(purpose)}
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


def _boundary_fields() -> list[dict[str, Any]]:
    fields = [
        {
            "selector": f"b_id{index}",
            "role": "input_memory",
            "source_citations": [
                "core/src/slice/mod.rs:3188-3193",
                "core/src/slice/sort/unstable/mod.rs:22-58",
            ],
            "trust_site_ids": ["TS-081-D004"],
        }
        for index in range(3)
    ]
    fields.extend(
        {
            "selector": selector,
            "role": "callback_result",
            "source_citations": ["core/src/slice/mod.rs:3188-3193"],
            "trust_site_ids": ["TS-081-D004"],
        }
        for selector in COMPARATOR_FIELDS
    )
    fields.append(
        {
            "selector": "b_callback_state_delta",
            "role": "callback_state_transition",
            "source_citations": ["core/src/slice/mod.rs:3188-3193"],
            "trust_site_ids": ["TS-081-D004"],
        }
    )
    return fields


def obligation_metadata(purpose: str) -> dict[str, Any]:
    if purpose not in PURPOSES:
        raise ValueError(f"unknown target-081 obligation purpose: {purpose}")
    metadata: dict[str, Any] = {
        "schema_version": 2,
        "target": TARGET,
        "input_order": INPUT_ORDER,
        "obligation_purpose": purpose,
        "active_contract_sha256": ACTIVE_CONTRACT_SHA256,
        "active_contract_text": ACTIVE_CONTRACT_TEXT,
        "bounded_domain": {
            "length": 3,
            "distinct_element_identities": True,
            "requires_adds_total_order": purpose == TOTAL_ORDER_SANITY,
            "callback_transition_profile": "state-preserving",
            "contract_translation": [
                "exact element multiplicity for every identity in either sequence",
                "all six i <= j comparator-sortedness observations",
            ],
        },
        "boundary_scope": {
            "shared_observations": [
                "three input element identities",
                "the finite 3-by-3 comparator result table",
                "one state-preserving callback transition delta",
            ],
            "excluded_observations": [
                "final sequence",
                "final permutation",
                "selected ordering",
                "aggregate final state",
                "answer-equivalent encoding",
                "pivot or swap decisions",
                "complete comparator-call trace",
                "complete target execution trace",
            ],
            "admitted_trust_site_ids": ["TS-081-D004"],
            "excluded_retained_trust_site_ids": list(
                EXCLUDED_RETAINED_TRUST_SITES
            ),
        },
        "active_contract_conjuncts": list(ACTIVE_CONJUNCT_SYMBOLS),
        "target_definition": "TargetDefinition_T",
        "theorem_variables": {
            "input": "x",
            "boundary": "b",
            "output1": "y1",
            "state1": "s1",
            "output2": "y2",
            "state2": "s2",
        },
        "boundary_fields": _boundary_fields(),
        "declared_functions": [],
        "source_transition_definitions": [
            "CallbackStateAfterSort",
            "UnitReturnAfterSort",
        ],
        "equivalence_kind": (
            "exact"
            if purpose == EXACT_FINAL_SLICE
            else "equal-key-reordering-equivalence"
        ),
        "principal_observations": [
            {
                "selector": selector,
                "left": "output1",
                "right": "output2",
                "sort": sort,
            }
            for selector, sort in OUTPUT_FIELDS
        ]
        + [
            {
                "selector": selector,
                "left": "state1",
                "right": "state2",
                "sort": sort,
            }
            for selector, sort in STATE_FIELDS
        ],
        "expected_solver_result": (
            "unsat" if purpose == TOTAL_ORDER_SANITY else "sat"
        ),
    }
    if purpose != EXACT_FINAL_SLICE:
        metadata["weak_equivalence_review"] = {
            "source_citations": SOURCE_CITATIONS,
            "positive_witness": POSITIVE_EQUIVALENCE_WITNESS,
            "negative_witness": NEGATIVE_EQUIVALENCE_WITNESS,
            "policy": (
                "Unit return and callback state remain exact. Final sequences "
                "must preserve exact identity multiplicities over both outputs "
                "and may differ position-wise only where the shared comparator "
                "reports Equal in both directions."
            ),
        }
    return metadata


def obligation(purpose: str) -> tuple[str, dict[str, Any]]:
    return obligation_text(purpose), obligation_metadata(purpose)


def validate_target_obligation(text: str, metadata: dict[str, Any]) -> None:
    validate_obligation(text, metadata)
    purpose = metadata.get("obligation_purpose")
    if purpose not in PURPOSES:
        raise GuardError("target-081 obligation has an unknown purpose")
    expected_text, expected_metadata = obligation(str(purpose))
    if metadata != expected_metadata:
        raise GuardError(
            "target-081 metadata differs from the reviewed bounded translation"
        )
    if parse_smt(text) != parse_smt(expected_text):
        raise GuardError(
            "target-081 SMT differs from the reviewed active-contract translation"
        )


def boundary_manifest() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "target": TARGET,
        "input_order": INPUT_ORDER,
        "active_contract_sha256": ACTIVE_CONTRACT_SHA256,
        "bounded_domain": "three distinct input identities",
        "boundary_narrower_than_target": True,
        "shared_boundary_observations": [
            {
                "fields": ["b_id0", "b_id1", "b_id2"],
                "kind": "input element identities",
                "trust_site_ids": ["TS-081-D004"],
            },
            {
                "fields": list(COMPARATOR_FIELDS),
                "kind": "finite extensional comparator results",
                "trust_site_ids": ["TS-081-D004"],
            },
            {
                "fields": ["b_callback_state_delta"],
                "kind": "state-preserving callback transition",
                "trust_site_ids": ["TS-081-D004"],
            },
        ],
        "excluded_retained_sites": [
            {
                "trust_site_id": "TS-081-D002",
                "reason": (
                    "The closure-lowering support is linked to the complete "
                    "private-sort postcondition and is not used by this model."
                ),
            },
            {
                "trust_site_id": "TS-081-D003",
                "reason": (
                    "The retained private-sort boundary supplies permutation "
                    "and sortedness, so it is excluded rather than relabeled."
                ),
            },
            {
                "trust_site_id": "TS-081-E001",
                "reason": (
                    "The external-body sort helper is an opaque whole algorithm "
                    "with the complete target postcondition."
                ),
            },
        ],
        "context_only_sites": ["TS-081-D001", "TS-081-C001"],
        "all_audited_trust_site_ids": list(ALL_AUDITED_TRUST_SITES),
        "excluded_observations": [
            "returned unit value",
            "final sequence or permutation",
            "selected ordering",
            "aggregate final state",
            "answer encoding",
            "pivot/swap choices",
            "comparison-call sequence",
            "complete execution trace",
        ],
        "assumption": (
            "Both executions share exactly the same three input identities, "
            "finite comparator table, and callback state-transition delta. "
            "The active permutation and comparator-sortedness conjuncts derive "
            "the admissible final sequences; no final ordering is placed in b."
        ),
        "scope_limitation": (
            "This is a length-three witness/sanity model of active-contract "
            "completeness, not a replacement proof of the private ipnsort "
            "implementation for arbitrary lengths."
        ),
    }


def witness_payload() -> dict[str, Any]:
    exact_table = [
        ["Equal", "Equal", "Less"],
        ["Equal", "Equal", "Less"],
        ["Greater", "Greater", "Equal"],
    ]
    non_total_table = [
        ["Equal", "Less", "Less"],
        ["Less", "Equal", "Less"],
        ["Greater", "Greater", "Equal"],
    ]
    common_input = {
        "identities": [10, 11, 20],
        "callback_initial_state": 7,
    }
    return {
        "schema_version": 1,
        "target": TARGET,
        "input_order": INPUT_ORDER,
        "active_contract_sha256": ACTIVE_CONTRACT_SHA256,
        "exact_final_slice_counterexample": {
            "input": common_input,
            "boundary": {
                "input_identities": [10, 11, 20],
                "comparator_results": exact_table,
                "callback_state_delta": 0,
            },
            "execution1": {
                "return_unit": True,
                "final_slice": [10, 11, 20],
                "callback_final_state": 7,
            },
            "execution2": {
                "return_unit": True,
                "final_slice": [11, 10, 20],
                "callback_final_state": 7,
            },
            "expected": {
                "boundary_is_total_order": True,
                "execution1_satisfies_active_contract": True,
                "execution2_satisfies_active_contract": True,
                "execution1_preserves_exact_multiplicities": True,
                "execution2_preserves_exact_multiplicities": True,
                "callback_final_state_equal": True,
                "reviewed_equal_key_equivalent": True,
                "exact_final_slice_equal": False,
            },
        },
        "general_non_total_counterexample": {
            "input": common_input,
            "boundary": {
                "input_identities": [10, 11, 20],
                "comparator_results": non_total_table,
                "callback_state_delta": 0,
            },
            "execution1": {
                "return_unit": True,
                "final_slice": [10, 11, 20],
                "callback_final_state": 7,
            },
            "execution2": {
                "return_unit": True,
                "final_slice": [11, 10, 20],
                "callback_final_state": 7,
            },
            "expected": {
                "boundary_is_total_order": False,
                "execution1_satisfies_active_contract": True,
                "execution2_satisfies_active_contract": True,
                "execution1_preserves_exact_multiplicities": True,
                "execution2_preserves_exact_multiplicities": True,
                "callback_final_state_equal": True,
                "reviewed_equal_key_equivalent": False,
                "exact_final_slice_equal": False,
            },
        },
    }


def _boundary_constructor(purpose: str) -> str:
    if purpose == PRIMARY:
        orderings = (
            "Equal Less Less "
            "Less Equal Less "
            "Greater Greater Equal"
        )
    elif purpose == EXACT_FINAL_SLICE:
        orderings = (
            "Equal Equal Less "
            "Equal Equal Less "
            "Greater Greater Equal"
        )
    else:
        raise ValueError("fixed models exist only for SAT obligations")
    return f"(mkBoundary 10 11 20 {orderings} 0)"


def fixed_model_text(purpose: str) -> str:
    if purpose not in {PRIMARY, EXACT_FINAL_SLICE}:
        raise ValueError("fixed models exist only for SAT obligations")
    text = obligation_text(purpose)
    terminal = "(check-sat)\n"
    if not text.endswith(terminal):
        raise ValueError("target obligation lacks the expected terminal check-sat")
    return (
        text[: -len(terminal)]
        + f"""\
(assert (= x (mkInput 10 11 20 7)))
(assert (= b {_boundary_constructor(purpose)}))
(assert (= y1 (mkOutput true)))
(assert (= s1 (mkState 10 11 20 7)))
(assert (= y2 (mkOutput true)))
(assert (= s2 (mkState 11 10 20 7)))
(check-sat)
(get-value (
  (s_final0 s1)
  (s_final1 s1)
  (s_final2 s1)
  (s_callback_state s1)
  (s_final0 s2)
  (s_final1 s2)
  (s_final2 s2)
  (s_callback_state s2)
  (TotalOrderProfile x b)
  (SameElementMultiset s1 s2)
  (Equivalent_T x b y1 s1 y2 s2)))
"""
    )
