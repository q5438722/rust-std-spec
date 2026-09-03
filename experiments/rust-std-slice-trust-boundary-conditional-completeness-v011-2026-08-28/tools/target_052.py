#!/usr/bin/env python3
"""Bounded active-contract model for input order 52, get_disjoint_unchecked_mut."""

from __future__ import annotations

from typing import Any

from checker_guards import GuardError, parse_smt, validate_obligation


TARGET = "core::slice::get_disjoint_unchecked_mut"
INPUT_ORDER = "52"
ARTIFACT_ID = "052_core_slice_get_disjoint_unchecked_mut"
ACTIVE_CONTRACT_SHA256 = (
    "98e2ff139533e1b36cd1ecef3a408b5045f5780bf76ff9a04f2b8f34879e368b"
)
ACTIVE_CONTRACT_TEXT = (
    "#[verifier::allow(undeclared_external_trait)] pub "
    "assume_specification<T, I, const N: usize>[ "
    "<[T]>::get_disjoint_unchecked_mut::<I, N> ]( slice: &mut [T], "
    "indices: [I; N], ) -> (ret: [&mut <I as "
    "core::slice::SliceIndex<[T]>>::Output; N]) where I: "
    "core::slice::GetDisjointMutIndex + core::slice::SliceIndex<[T]> "
    "requires slice_disjoint_indices_valid::<T, I, N>(old(slice)@, indices), "
    "ensures final(slice)@.len() == old(slice)@.len(), ;"
)

PRIMARY = "completeness-modulo-reviewed-equivalence"
EXACT_OUTPUT = "exact-output-determinism"
PURPOSES = (PRIMARY, EXACT_OUTPUT)

TARGET_SOURCE_REFERENCE = "core/src/slice/mod.rs:5142-5166"
PUBLIC_DOCS_REFERENCE = "core/src/slice/mod.rs:5093-5138"
INDEX_VALIDITY_REFERENCE = "core/src/slice/mod.rs:5758-5793"
USIZE_CLONE_REFERENCE = "core/src/clone.rs:607-632"
SLICE_INDEX_REFERENCE = "core/src/slice/index.rs:214-267"

CANONICAL_SOURCE_BINDINGS = {
    "unchecked_borrow_construction": {
        "path": "core/src/slice/mod.rs",
        "start": 5142,
        "end": 5166,
        "file_sha256": (
            "58901fa6437dbd4d77c68427bbced0fc3a91a10fdb8bd2e233adf6a9ba27d2d5"
        ),
        "excerpt_sha256": (
            "fadb1cf499d963bdf8603a8901d68a9dc03c5ce7ebf3f084ce0fe58348b65be2"
        ),
    },
    "get_disjoint_usize_validity": {
        "path": "core/src/slice/mod.rs",
        "start": 5758,
        "end": 5793,
        "file_sha256": (
            "58901fa6437dbd4d77c68427bbced0fc3a91a10fdb8bd2e233adf6a9ba27d2d5"
        ),
        "excerpt_sha256": (
            "8f1edfdb357227abb20b8ca0e1a8c69250a435d4831af352593a612cbba70216"
        ),
    },
    "usize_clone": {
        "path": "core/src/clone.rs",
        "start": 607,
        "end": 632,
        "file_sha256": (
            "6bfe77fc369801a72c08598ad4cda4be5ee0fc24d521dd910dfe42bd0aae97b8"
        ),
        "excerpt_sha256": (
            "9c5b51081a58474f4682b86c9febb31bb9ae39cc9b4ca82b3d30ddbc4e6f1f73"
        ),
    },
    "usize_slice_index": {
        "path": "core/src/slice/index.rs",
        "start": 214,
        "end": 267,
        "file_sha256": (
            "16c924deb46e5e027872853736f082abae1eb45f74e55935814a20979899a935"
        ),
        "excerpt_sha256": (
            "2bbf18e695d8d18513b68ee646877dce703c00eab4c9e5f6b111fb1f976726e5"
        ),
    },
}

EXCLUDED_RETAINED_TRUST_SITES = ("TS-052-D004", "TS-052-E001")
ADMITTED_TRUST_SITES = ("TS-052-D002", "TS-052-D003")
ALL_AUDITED_TRUST_SITES = (
    "TS-052-D001",
    "TS-052-D002",
    "TS-052-D003",
    "TS-052-D004",
    "TS-052-E001",
)

OUTPUT_FIELDS = (
    ("y_array_length", "Int"),
    ("y_ref0_index", "Int"),
    ("y_ref0_allocation", "Int"),
    ("y_ref0_address", "Int"),
    ("y_ref0_provenance", "Int"),
    ("y_ref0_parent_borrow", "Int"),
    ("y_ref0_value", "Int"),
    ("y_ref1_index", "Int"),
    ("y_ref1_allocation", "Int"),
    ("y_ref1_address", "Int"),
    ("y_ref1_provenance", "Int"),
    ("y_ref1_parent_borrow", "Int"),
    ("y_ref1_value", "Int"),
)
STATE_FIELDS = (
    ("s_length", "Int"),
    ("s_value0", "Int"),
    ("s_value1", "Int"),
    ("s_value2", "Int"),
    ("s_allocation", "Int"),
    ("s_address", "Int"),
    ("s_provenance", "Int"),
    ("s_borrow", "Int"),
    ("s_element_size", "Int"),
    ("s_element_alignment", "Int"),
    ("s_frame_token", "Int"),
)


def _state_declaration(purpose: str) -> str:
    if purpose == EXACT_OUTPUT:
        return "(declare-datatypes ((State 0)) (((mkState))))"
    fields = "\n".join(
        f"      ({selector} {sort})" for selector, sort in STATE_FIELDS
    )
    return f"""\
(declare-datatypes ((State 0))
  (((mkState
{fields}))))"""


def _state_constraints(purpose: str) -> str:
    if purpose == EXACT_OUTPUT:
        return ""
    return "       (= (s_length s) (PreservedSliceLength x))"


def _equivalence_body(purpose: str) -> str:
    fields = list(OUTPUT_FIELDS)
    if purpose == PRIMARY:
        fields.extend(STATE_FIELDS)
    output_selectors = {selector for selector, _ in OUTPUT_FIELDS}
    equalities = [
        f"(= ({selector} {'y1' if selector in output_selectors else 's1'}) "
        f"({selector} {'y2' if selector in output_selectors else 's2'}))"
        for selector, _ in fields
    ]
    return "  (and " + "\n       ".join(equalities) + "))"


def _model_text(purpose: str) -> str:
    if purpose not in PURPOSES:
        raise ValueError(f"unknown target-052 obligation purpose: {purpose}")
    return f"""\
; Target: {TARGET}
; Active contract SHA-256: {ACTIVE_CONTRACT_SHA256}
; Purpose: {purpose}
; Bounded domain: N=2 usize indices [0, 2] over a non-ZST slice of length 3.
; The canonical source construction is modeled for audits and probes but is
; deliberately not injected into the generated contract relation.
(set-logic ALL)
(declare-datatypes ((Input 0))
  (((mkInput
      (x_length Int)
      (x_value0 Int)
      (x_value1 Int)
      (x_value2 Int)
      (x_index0 Int)
      (x_index1 Int)
      (x_slice_allocation Int)
      (x_slice_address Int)
      (x_slice_provenance Int)
      (x_slice_borrow Int)
      (x_element_size Int)
      (x_element_alignment Int)
      (x_allocation_base Int)
      (x_allocation_bytes Int)
      (x_isize_max Int)
      (x_address_space_limit Int)
      (x_frame_token Int)))))
(declare-datatypes ((Boundary 0))
  (((mkBoundary
      (b_length Int)
      (b_value0 Int)
      (b_value1 Int)
      (b_value2 Int)
      (b_slice_allocation Int)
      (b_slice_address Int)
      (b_slice_provenance Int)
      (b_slice_borrow Int)
      (b_element_size Int)
      (b_element_alignment Int)
      (b_allocation_base Int)
      (b_allocation_bytes Int)
      (b_isize_max Int)
      (b_address_space_limit Int)
      (b_frame_token Int)))))
(declare-datatypes ((Output 0))
  (((mkOutput
      (y_array_length Int)
      (y_ref0_index Int)
      (y_ref0_allocation Int)
      (y_ref0_address Int)
      (y_ref0_provenance Int)
      (y_ref0_parent_borrow Int)
      (y_ref0_value Int)
      (y_ref1_index Int)
      (y_ref1_allocation Int)
      (y_ref1_address Int)
      (y_ref1_provenance Int)
      (y_ref1_parent_borrow Int)
      (y_ref1_value Int)))))
{_state_declaration(purpose)}
(declare-const x Input)
(declare-const b Boundary)
(declare-const y1 Output)
(declare-const s1 State)
(declare-const y2 Output)
(declare-const s2 State)
(define-fun SliceByteLength ((x Input)) Int
  (* (x_length x) (x_element_size x)))
(define-fun IndexInBounds ((x Input) (index Int)) Bool
  (and (>= index 0) (< index (x_length x))))
(define-fun IndicesValid ((x Input)) Bool
  (and (IndexInBounds x (x_index0 x))
       (IndexInBounds x (x_index1 x))
       (not (= (x_index0 x) (x_index1 x)))))
(define-fun SliceValueAt ((x Input) (index Int)) Int
  (ite (= index 0)
       (x_value0 x)
       (ite (= index 1) (x_value1 x) (x_value2 x))))
(define-fun BorrowAddressAtIndex ((x Input) (index Int)) Int
  (+ (x_slice_address x) (* index (x_element_size x))))
(define-fun BorrowWellFormed
  ((x Input)
   (index Int)
   (allocation Int)
   (address Int)
   (provenance Int)
   (parent_borrow Int)
   (value Int)) Bool
  (and (IndexInBounds x index)
       (= allocation (x_slice_allocation x))
       (= address (BorrowAddressAtIndex x index))
       (= provenance (x_slice_provenance x))
       (= parent_borrow (x_slice_borrow x))
       (= value (SliceValueAt x index))))
(define-fun ReturnedBorrowArrayWellFormed
  ((x Input) (y Output)) Bool
  (and (= (y_array_length y) 2)
    (BorrowWellFormed
      x
      (y_ref0_index y)
      (y_ref0_allocation y)
      (y_ref0_address y)
      (y_ref0_provenance y)
      (y_ref0_parent_borrow y)
      (y_ref0_value y))
    (BorrowWellFormed
      x
      (y_ref1_index y)
      (y_ref1_allocation y)
      (y_ref1_address y)
      (y_ref1_provenance y)
      (y_ref1_parent_borrow y)
      (y_ref1_value y))
    (not (= (y_ref0_index y) (y_ref1_index y)))))
(define-fun ClonedIndex0 ((x Input)) Int
  (x_index0 x))
(define-fun ClonedIndex1 ((x Input)) Int
  (x_index1 x))
(define-fun GetUncheckedMutResolvedIndex ((x Input) (index Int)) Int
  index)
(define-fun Slot0InitializedAfterFirstWrite ((x Input)) Bool
  (IndexInBounds x (ClonedIndex0 x)))
(define-fun Slot1InitializedAfterFirstWrite ((x Input)) Bool
  false)
(define-fun Slot0IndexAfterFirstWrite ((x Input)) Int
  (GetUncheckedMutResolvedIndex x (ClonedIndex0 x)))
(define-fun Slot0InitializedAfterSecondWrite ((x Input)) Bool
  (Slot0InitializedAfterFirstWrite x))
(define-fun Slot1InitializedAfterSecondWrite ((x Input)) Bool
  (IndexInBounds x (ClonedIndex1 x)))
(define-fun Slot0IndexAfterSecondWrite ((x Input)) Int
  (Slot0IndexAfterFirstWrite x))
(define-fun Slot1IndexAfterSecondWrite ((x Input)) Int
  (GetUncheckedMutResolvedIndex x (ClonedIndex1 x)))
(define-fun AllSlotsInitializedAfterSecondWrite ((x Input)) Bool
  (and (Slot0InitializedAfterSecondWrite x)
       (Slot1InitializedAfterSecondWrite x)))
(define-fun AssumeInitPermittedAfterFirstWrite ((x Input)) Bool
  (and (Slot0InitializedAfterFirstWrite x)
       (Slot1InitializedAfterFirstWrite x)))
(define-fun AssumeInitPermittedAfterSecondWrite ((x Input)) Bool
  (AllSlotsInitializedAfterSecondWrite x))
(define-fun CanonicalBorrowArrayConstructed
  ((x Input) (y Output)) Bool
  (and (AssumeInitPermittedAfterSecondWrite x)
       (= (y_ref0_index y) (Slot0IndexAfterSecondWrite x))
       (= (y_ref1_index y) (Slot1IndexAfterSecondWrite x))
       (ReturnedBorrowArrayWellFormed x y)))
(define-fun InitialSliceObserved ((x Input) (b Boundary)) Bool
  (and (= (b_length b) (x_length x))
       (= (b_value0 b) (x_value0 x))
       (= (b_value1 b) (x_value1 x))
       (= (b_value2 b) (x_value2 x))
       (= (b_slice_allocation b) (x_slice_allocation x))
       (= (b_slice_address b) (x_slice_address x))
       (= (b_slice_provenance b) (x_slice_provenance x))
       (= (b_slice_borrow b) (x_slice_borrow x))
       (= (b_element_size b) (x_element_size x))
       (= (b_element_alignment b) (x_element_alignment x))
       (= (b_allocation_base b) (x_allocation_base x))
       (= (b_allocation_bytes b) (x_allocation_bytes x))
       (= (b_isize_max b) (x_isize_max x))
       (= (b_address_space_limit b) (x_address_space_limit x))
       (= (b_frame_token b) (x_frame_token x))))
(define-fun PreservedSliceLength ((x Input)) Int
  (x_length x))
(define-fun ReturnedArrayLength ((x Input)) Int
  2)
(define-fun Requires_T ((x Input)) Bool
  (and (= (x_length x) 3)
       (= (x_index0 x) 0)
       (= (x_index1 x) 2)
       (IndicesValid x)
       (> (x_slice_allocation x) 0)
       (> (x_slice_address x) 0)
       (> (x_slice_provenance x) 0)
       (> (x_slice_borrow x) 0)
       (> (x_element_size x) 0)
       (> (x_element_alignment x) 0)
       (= (mod (x_slice_address x) (x_element_alignment x)) 0)
       (= (mod (x_element_size x) (x_element_alignment x)) 0)
       (>= (x_allocation_base x) 0)
       (> (x_allocation_bytes x) 0)
       (<= (x_allocation_base x) (x_slice_address x))
       (<= (+ (x_slice_address x) (SliceByteLength x))
           (+ (x_allocation_base x) (x_allocation_bytes x)))
       (<= (SliceByteLength x) (x_isize_max x))
       (<= (+ (x_slice_address x) (SliceByteLength x))
           (x_address_space_limit x))))
(define-fun Boundary_T ((x Input) (b Boundary)) Bool
  (and (> (b_length b) 0)
       (> (b_slice_allocation b) 0)
       (> (b_slice_address b) 0)
       (> (b_slice_provenance b) 0)
       (> (b_slice_borrow b) 0)
       (> (b_element_size b) 0)
       (> (b_element_alignment b) 0)
       (> (b_allocation_bytes b) 0)
       (> (b_isize_max b) 0)
       (> (b_address_space_limit b) 0)
       (InitialSliceObserved x b)))
(define-fun TargetDefinition_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and (InitialSliceObserved x b)
       (= (y_array_length y) (ReturnedArrayLength x))
       (ReturnedBorrowArrayWellFormed x y)
{_state_constraints(purpose)}))
(define-fun Spec_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (TargetDefinition_T x b y s))
(define-fun Equivalent_T
  ((x Input) (b Boundary)
   (y1 Output) (s1 State) (y2 Output) (s2 State)) Bool
{_equivalence_body(purpose)}
"""


def obligation_text(purpose: str) -> str:
    return _model_text(purpose) + """\
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


def _principal_observations(purpose: str) -> list[dict[str, str]]:
    observations = [
        {
            "selector": selector,
            "left": "output1",
            "right": "output2",
            "sort": sort,
        }
        for selector, sort in OUTPUT_FIELDS
    ]
    if purpose == PRIMARY:
        observations.extend(
            {
                "selector": selector,
                "left": "state1",
                "right": "state2",
                "sort": sort,
            }
            for selector, sort in STATE_FIELDS
        )
    return observations


def _boundary_fields() -> list[dict[str, Any]]:
    roles = {
        "b_length": "input_memory",
        "b_value0": "input_memory",
        "b_value1": "input_memory",
        "b_value2": "input_memory",
        "b_slice_allocation": "input_memory",
        "b_slice_address": "input_memory",
        "b_slice_provenance": "input_provenance",
        "b_slice_borrow": "input_provenance",
        "b_element_size": "input_layout",
        "b_element_alignment": "input_layout",
        "b_allocation_base": "input_memory",
        "b_allocation_bytes": "input_memory",
        "b_isize_max": "input_layout",
        "b_address_space_limit": "input_layout",
        "b_frame_token": "input_memory",
    }
    citations = [
        TARGET_SOURCE_REFERENCE,
        INDEX_VALIDITY_REFERENCE,
        SLICE_INDEX_REFERENCE,
    ]
    return [
        {
            "selector": selector,
            "role": role,
            "source_citations": citations,
            "trust_site_ids": ["TS-052-D002"],
        }
        for selector, role in roles.items()
    ]


def obligation_metadata(purpose: str) -> dict[str, Any]:
    if purpose not in PURPOSES:
        raise ValueError(f"unknown target-052 obligation purpose: {purpose}")
    source_transitions = ["ReturnedArrayLength"]
    if purpose == PRIMARY:
        source_transitions.append("PreservedSliceLength")
    return {
        "schema_version": 2,
        "target": TARGET,
        "input_order": INPUT_ORDER,
        "obligation_purpose": purpose,
        "active_contract_sha256": ACTIVE_CONTRACT_SHA256,
        "active_contract_text": ACTIVE_CONTRACT_TEXT,
        "bounded_domain": {
            "index_type": "usize",
            "index_count": 2,
            "indices": [0, 2],
            "slice_length": 3,
            "element_layout": "positive-size aligned elements",
            "contract_scope": (
                "The generated unsafe precondition and final-length postcondition "
                "are complete for this bounded input. Returned mutable references "
                "also satisfy Rust reference well-formedness and disjointness, "
                "but are not equated to the source-selected indices."
            ),
        },
        "contract_translation": {
            "requires": (
                "Both cloned usize indices are in bounds for the length-three "
                "slice and are distinct, expanding slice_disjoint_indices_valid."
            ),
            "ensures": "The final slice length equals the initial slice length.",
            "return_type_invariant": (
                "The two returned mutable references are valid, non-overlapping "
                "borrows into the receiver allocation with matching value, "
                "address, provenance, and parent-borrow observations."
            ),
            "implementation_choice_exclusion": (
                "The source-selected [index0, index1] borrow array and complete "
                "final state are modeled for probes but are not conjoined to Spec_T."
            ),
        },
        "boundary_scope": {
            "shared_observations": [
                "initial slice length and element values",
                "initial allocation, address, provenance, and mutable-borrow identity",
                "element layout and target-platform pointer limits",
                "pre-existing outside-memory frame token",
            ],
            "excluded_observations": [
                "validity bit or opaque validity relation",
                "returned borrow or borrow-array identity",
                "MaybeUninit slot contents or initialization result",
                "alias map",
                "resulting slice values or aggregate final state",
                "canonical answer or deterministic implementation choice",
                "selected or complete execution trace",
            ],
            "admitted_trust_site_ids": list(ADMITTED_TRUST_SITES),
            "excluded_retained_trust_site_ids": list(
                EXCLUDED_RETAINED_TRUST_SITES
            ),
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
        "boundary_fields": _boundary_fields(),
        "declared_functions": [],
        "source_transition_definitions": source_transitions,
        "source_transition_bindings": {
            "usize_clone": {
                "symbols": ["ClonedIndex0", "ClonedIndex1"],
                "source_citations": [USIZE_CLONE_REFERENCE],
            },
            "usize_get_unchecked_mut": {
                "symbols": [
                    "IndexInBounds",
                    "GetUncheckedMutResolvedIndex",
                    "BorrowAddressAtIndex",
                    "BorrowWellFormed",
                    "ReturnedBorrowArrayWellFormed",
                ],
                "source_citations": [
                    TARGET_SOURCE_REFERENCE,
                    SLICE_INDEX_REFERENCE,
                ],
            },
            "maybeuninit_two_slot_loop": {
                "symbols": [
                    "Slot0InitializedAfterFirstWrite",
                    "Slot1InitializedAfterFirstWrite",
                    "Slot0IndexAfterFirstWrite",
                    "Slot0InitializedAfterSecondWrite",
                    "Slot1InitializedAfterSecondWrite",
                    "Slot0IndexAfterSecondWrite",
                    "Slot1IndexAfterSecondWrite",
                    "AllSlotsInitializedAfterSecondWrite",
                    "AssumeInitPermittedAfterFirstWrite",
                    "AssumeInitPermittedAfterSecondWrite",
                    "CanonicalBorrowArrayConstructed",
                ],
                "replaces_trust_site_ids": ["TS-052-D004", "TS-052-E001"],
                "source_citations": [
                    TARGET_SOURCE_REFERENCE,
                    USIZE_CLONE_REFERENCE,
                    SLICE_INDEX_REFERENCE,
                ],
            },
        },
        "equivalence_kind": "exact",
        "equivalence_scope": (
            "Every returned-reference identity/value field and every modeled "
            "final-slice/frame observation"
            if purpose == PRIMARY
            else "Every returned-reference identity/value field"
        ),
        "principal_observations": _principal_observations(purpose),
        "expected_solver_result": "sat",
    }


def obligation(purpose: str) -> tuple[str, dict[str, Any]]:
    return obligation_text(purpose), obligation_metadata(purpose)


def validate_target_obligation(text: str, metadata: dict[str, Any]) -> None:
    validate_obligation(text, metadata)
    purpose = metadata.get("obligation_purpose")
    if purpose not in PURPOSES:
        raise GuardError("target-052 obligation has an unknown purpose")
    expected_text, expected_metadata = obligation(str(purpose))
    if metadata != expected_metadata:
        raise GuardError(
            "target-052 metadata differs from the reviewed active-contract model"
        )
    if parse_smt(text) != parse_smt(expected_text):
        raise GuardError(
            "target-052 SMT differs from the reviewed active-contract model"
        )


def _input_expression() -> str:
    values = (
        3,
        10,
        20,
        30,
        0,
        2,
        41,
        4096,
        141,
        241,
        4,
        4,
        4096,
        256,
        2_147_483_647,
        4_294_967_295,
        777,
    )
    return "(mkInput " + " ".join(map(str, values)) + ")"


def _boundary_expression() -> str:
    values = (
        3,
        10,
        20,
        30,
        41,
        4096,
        141,
        241,
        4,
        4,
        4096,
        256,
        2_147_483_647,
        4_294_967_295,
        777,
    )
    return "(mkBoundary " + " ".join(map(str, values)) + ")"


def _success_output(ref0: int, ref1: int) -> str:
    values = {0: 10, 1: 20, 2: 30}

    def borrow(index: int) -> tuple[int, ...]:
        return (
            index,
            41,
            4096 + index * 4,
            141,
            241,
            values[index],
        )

    fields = (*borrow(ref0), *borrow(ref1))
    return "(mkOutput 2 " + " ".join(map(str, fields)) + ")"


def _state_expression() -> str:
    return "(mkState 3 10 20 30 41 4096 141 241 4 4 777)"


WITNESS_CASES = {
    "valid_disjoint_distinct_borrows": {
        "output1": _success_output(0, 2),
        "output2": _success_output(1, 2),
    },
}


def fixed_witness_text(name: str) -> str:
    try:
        case = WITNESS_CASES[name]
    except KeyError as exc:
        raise ValueError(f"unknown target-052 witness: {name}") from exc
    return _model_text(PRIMARY) + f"""\
(assert (= x {_input_expression()}))
(assert (= b {_boundary_expression()}))
(assert (= y1 {case["output1"]}))
(assert (= s1 {_state_expression()}))
(assert (= y2 {case["output2"]}))
(assert (= s2 {_state_expression()}))
(assert (Requires_T x))
(assert (Boundary_T x b))
(assert (Spec_T x b y1 s1))
(assert (Spec_T x b y2 s2))
(assert (not (Equivalent_T x b y1 s1 y2 s2)))
(check-sat)
(get-value (
  (IndicesValid x)
  (ClonedIndex0 x)
  (ClonedIndex1 x)
  (Slot0InitializedAfterFirstWrite x)
  (Slot1InitializedAfterFirstWrite x)
  (Slot0InitializedAfterSecondWrite x)
  (Slot1InitializedAfterSecondWrite x)
  (AssumeInitPermittedAfterFirstWrite x)
  (AssumeInitPermittedAfterSecondWrite x)
  (y_ref0_index y1)
  (y_ref1_index y1)
  (y_ref0_index y2)
  (y_ref1_index y2)
  (s_value0 s1)
  (s_value0 s2)))
"""


PROBE_CASES = {
    "usize_clone_identity": {
        "kind": "source_clone",
        "expected": "sat",
    },
    "get_unchecked_mut_resolution": {
        "kind": "source_index_resolution",
        "expected": "sat",
    },
    "complete_initialization_then_assume_init": {
        "kind": "source_maybeuninit",
        "expected": "sat",
    },
    "invalid_success_out_of_bounds_reference": {
        "kind": "invalid_return_reference",
        "expected": "unsat",
    },
    "invalid_success_overlapping_references": {
        "kind": "overlapping_return_references",
        "expected": "unsat",
    },
    "invalid_prior_slot_mutation": {
        "kind": "prior_slot_mutation",
        "expected": "unsat",
    },
    "invalid_partial_initialization": {
        "kind": "partial_initialization",
        "expected": "unsat",
    },
    "invalid_premature_assume_init": {
        "kind": "premature_assume_init",
        "expected": "unsat",
    },
}
PROBE_EXPECTED_RESULTS = {
    name: str(case["expected"]) for name, case in PROBE_CASES.items()
}


def probe_text(name: str) -> str:
    if name not in PROBE_CASES:
        raise ValueError(f"unknown target-052 probe: {name}")
    common_assertions = [
        f"(= x {_input_expression()})",
        f"(= b {_boundary_expression()})",
        "(Requires_T x)",
        "(Boundary_T x b)",
    ]
    if name == "usize_clone_identity":
        assertions = common_assertions + [
            "(= (ClonedIndex0 x) 0)",
            "(= (ClonedIndex1 x) 2)",
        ]
    elif name == "get_unchecked_mut_resolution":
        assertions = common_assertions + [
            f"(= y1 {_success_output(0, 2)})",
            "(CanonicalBorrowArrayConstructed x y1)",
            "(= (Slot0IndexAfterSecondWrite x) 0)",
            "(= (Slot1IndexAfterSecondWrite x) 2)",
        ]
    elif name == "complete_initialization_then_assume_init":
        assertions = common_assertions + [
            "(Slot0InitializedAfterFirstWrite x)",
            "(not (Slot1InitializedAfterFirstWrite x))",
            "(Slot0InitializedAfterSecondWrite x)",
            "(Slot1InitializedAfterSecondWrite x)",
            "(AllSlotsInitializedAfterSecondWrite x)",
            "(AssumeInitPermittedAfterSecondWrite x)",
        ]
    elif name == "invalid_success_out_of_bounds_reference":
        bad = (
            "(mkOutput 2 "
            "3 41 4108 141 241 0 "
            "2 41 4104 141 241 30)"
        )
        assertions = common_assertions + [
            f"(= y1 {bad})",
            f"(= s1 {_state_expression()})",
            "(Spec_T x b y1 s1)",
        ]
    elif name == "invalid_success_overlapping_references":
        assertions = common_assertions + [
            f"(= y1 {_success_output(2, 2)})",
            f"(= s1 {_state_expression()})",
            "(Spec_T x b y1 s1)",
        ]
    elif name == "invalid_prior_slot_mutation":
        assertions = common_assertions + [
            "(not (= (Slot0IndexAfterSecondWrite x) "
            "(Slot0IndexAfterFirstWrite x)))",
        ]
    elif name == "invalid_partial_initialization":
        assertions = common_assertions + [
            "(not (AllSlotsInitializedAfterSecondWrite x))",
        ]
    else:
        assertions = common_assertions + [
            "(AssumeInitPermittedAfterFirstWrite x)",
        ]
    body = "\n       ".join(assertions)
    return _model_text(PRIMARY) + f"""\
(assert
  (and {body}))
(check-sat)
"""


def _borrow_payload(index: int) -> dict[str, int]:
    values = [10, 20, 30]
    return {
        "index": index,
        "allocation": 41,
        "address": 4096 + index * 4,
        "provenance": 141,
        "parent_borrow": 241,
        "value": values[index],
    }


def witness_payload() -> dict[str, Any]:
    shared_input = {
        "length": 3,
        "values": [10, 20, 30],
        "indices": [0, 2],
        "allocation": 41,
        "address": 4096,
        "provenance": 141,
        "borrow": 241,
        "element_size": 4,
        "element_alignment": 4,
        "allocation_base": 4096,
        "allocation_bytes": 256,
        "isize_max": 2_147_483_647,
        "address_space_limit": 4_294_967_295,
        "frame_token": 777,
    }
    boundary = {
        key: value
        for key, value in shared_input.items()
        if key != "indices"
    }
    unchanged_state = {
        "length": 3,
        "values": [10, 20, 30],
        "allocation": 41,
        "address": 4096,
        "provenance": 141,
        "borrow": 241,
        "element_size": 4,
        "element_alignment": 4,
        "frame_token": 777,
    }
    return {
        "schema_version": 1,
        "target": TARGET,
        "input_order": INPUT_ORDER,
        "active_contract_sha256": ACTIVE_CONTRACT_SHA256,
        "valid_disjoint_distinct_borrows": {
            "input": shared_input,
            "boundary": boundary,
            "source_transition": {
                "cloned_indices": [0, 2],
                "after_first_write": {
                    "initialized": [True, False],
                    "slot0_index": 0,
                },
                "after_second_write": {
                    "initialized": [True, True],
                    "slot0_index": 0,
                    "slot1_index": 2,
                },
                "assume_init_after_first_write": False,
                "assume_init_after_second_write": True,
                "canonical_borrow_indices": [0, 2],
            },
            "execution1": {
                "result": {
                    "borrows": [_borrow_payload(0), _borrow_payload(2)],
                },
                "final_state": unchanged_state,
            },
            "execution2": {
                "result": {
                    "borrows": [_borrow_payload(1), _borrow_payload(2)],
                },
                "final_state": unchanged_state,
            },
            "expected": {
                "requires_holds": True,
                "shared_boundary": True,
                "source_transition_is_complete": True,
                "execution1_borrows_well_formed_and_disjoint": True,
                "execution2_borrows_well_formed_and_disjoint": True,
                "execution1_is_canonical_implementation_result": True,
                "execution2_is_canonical_implementation_result": False,
                "execution1_satisfies_contract": True,
                "execution2_satisfies_contract": True,
                "exact_output_equal": False,
                "exact_final_state_equal": True,
                "exact_equivalent": False,
            },
        },
    }


def boundary_manifest() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "target": TARGET,
        "input_order": INPUT_ORDER,
        "active_contract_sha256": ACTIVE_CONTRACT_SHA256,
        "bounded_domain": "N=2 usize indices [0,2], length-3 non-ZST slice",
        "boundary_narrower_than_target": True,
        "shared_boundary_observations": [
            {
                "fields": ["b_length", "b_value0", "b_value1", "b_value2"],
                "kind": "initial receiver slice values",
                "trust_site_ids": ["TS-052-D002"],
            },
            {
                "fields": [
                    "b_slice_allocation",
                    "b_slice_address",
                    "b_slice_provenance",
                    "b_slice_borrow",
                    "b_allocation_base",
                    "b_allocation_bytes",
                ],
                "kind": "initial receiver memory and mutable-borrow identity",
                "trust_site_ids": ["TS-052-D002"],
            },
            {
                "fields": [
                    "b_element_size",
                    "b_element_alignment",
                    "b_isize_max",
                    "b_address_space_limit",
                ],
                "kind": "element layout and target-platform pointer limits",
                "trust_site_ids": ["TS-052-D002"],
            },
            {
                "fields": ["b_frame_token"],
                "kind": "pre-existing memory outside the receiver",
                "trust_site_ids": ["TS-052-D002"],
            },
        ],
        "forbidden_boundary_observations": [
            "validity bit",
            "opaque validity relation",
            "returned borrow",
            "borrow-array identity",
            "MaybeUninit slot contents or initialization result",
            "alias map",
            "resulting state",
            "canonical answer",
            "answer-equivalent encoding",
            "deterministic implementation choice",
            "full execution trace",
        ],
        "deterministic_source_semantics": [
            {
                "operation": "usize Clone",
                "semantics": "Each cloned usize index equals its input value.",
                "source_citations": [USIZE_CLONE_REFERENCE],
                "retained_support_ids": ["TS-052-D003"],
            },
            {
                "operation": "SliceIndex<usize>::get_unchecked_mut",
                "semantics": (
                    "Each in-bounds cloned index resolves to the receiver element "
                    "at base_address + index * element_size with receiver "
                    "allocation, provenance, parent borrow, and value."
                ),
                "source_citations": [
                    TARGET_SOURCE_REFERENCE,
                    SLICE_INDEX_REFERENCE,
                ],
                "retained_support_ids": ["TS-052-D002"],
            },
            {
                "operation": "two-slot MaybeUninit write loop and assume_init",
                "semantics": (
                    "The first write initializes only slot 0; the second write "
                    "preserves slot 0 and initializes slot 1; assume_init is "
                    "permitted only after both slots are initialized."
                ),
                "source_citations": [TARGET_SOURCE_REFERENCE],
                "replaces_trust_site_ids": ["TS-052-D004", "TS-052-E001"],
            },
        ],
        "spec_relation_policy": (
            "Spec_T is the generated final-length contract plus Rust return-type "
            "well-formedness and disjointness. It does not inject the canonical "
            "returned references, MaybeUninit trace, or aggregate final state."
        ),
        "admitted_boundary_trust_site_ids": list(ADMITTED_TRUST_SITES),
        "excluded_retained_sites": [
            {
                "trust_site_id": identifier,
                "disposition": "excluded-answer-bearing-retained-site",
            }
            for identifier in EXCLUDED_RETAINED_TRUST_SITES
        ],
        "all_audited_trust_site_ids": list(ALL_AUDITED_TRUST_SITES),
    }
