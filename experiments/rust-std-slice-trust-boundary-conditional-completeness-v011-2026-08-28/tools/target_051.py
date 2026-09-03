#!/usr/bin/env python3
"""Bounded active-contract model for input order 51, get_disjoint_mut."""

from __future__ import annotations

from typing import Any

from checker_guards import GuardError, parse_smt, validate_obligation


TARGET = "core::slice::get_disjoint_mut"
INPUT_ORDER = "51"
ARTIFACT_ID = "051_core_slice_get_disjoint_mut"
ACTIVE_CONTRACT_SHA256 = (
    "65402a0e5a620790d6f1413ab49efa952f05d939b14bf1066e92da32f7cd548a"
)
ACTIVE_CONTRACT_TEXT = (
    "#[verifier::allow(undeclared_external_trait)] pub "
    "assume_specification<T, I, const N: usize>[ "
    "<[T]>::get_disjoint_mut::<I, N> ]( slice: &mut [T], indices: [I; N], "
    ") -> (ret: core::result::Result< [&mut <I as "
    "core::slice::SliceIndex<[T]>>::Output; N], "
    "core::slice::GetDisjointMutError, >) where I: "
    "core::slice::GetDisjointMutIndex + core::slice::SliceIndex<[T]> "
    "ensures ret.is_ok() ==> "
    "slice_disjoint_indices_valid::<T, I, N>(old(slice)@, indices) && "
    "final(slice)@.len() == old(slice)@.len(), ret.is_err() ==> "
    "!slice_disjoint_indices_valid::<T, I, N>(old(slice)@, indices) && "
    "final(slice)@ == old(slice)@, ;"
)

PRIMARY = "completeness-modulo-reviewed-equivalence"
EXACT_OUTPUT = "exact-output-determinism"
PURPOSES = (PRIMARY, EXACT_OUTPUT)

TARGET_SOURCE_REFERENCE = "core/src/slice/mod.rs:5168-5220"
VALIDATION_LOOP_REFERENCE = "core/src/slice/mod.rs:5686-5703"
INDEX_TRAIT_REFERENCE = "core/src/slice/mod.rs:5758-5793"
BORROW_CONSTRUCTION_REFERENCE = "core/src/slice/mod.rs:5142-5166"

CANONICAL_SOURCE_BINDINGS = {
    "validation_loop": {
        "path": "core/src/slice/mod.rs",
        "start": 5686,
        "end": 5703,
        "file_sha256": (
            "58901fa6437dbd4d77c68427bbced0fc3a91a10fdb8bd2e233adf6a9ba27d2d5"
        ),
        "excerpt_sha256": (
            "dfe645823002998fd85f45a791fa6deaa9180bd59d7814458417698e7b657772"
        ),
    },
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
    "index_trait_and_usize_impl": {
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
}

EXCLUDED_RETAINED_TRUST_SITES = (
    "TS-051-D002",
    "TS-051-D004",
    "TS-051-E001",
    "TS-051-E002",
)
ADMITTED_TRUST_SITES = ("TS-051-D003",)
ALL_AUDITED_TRUST_SITES = (
    "TS-051-D001",
    "TS-051-D002",
    "TS-051-D003",
    "TS-051-D004",
    "TS-051-C001",
    "TS-051-C002",
    "TS-051-C003",
    "TS-051-C004",
    "TS-051-E001",
    "TS-051-E002",
)

OUTPUT_FIELDS = (
    ("y_is_ok", "Bool"),
    ("y_error_kind", "ErrorKind"),
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
    return """\
       (= (s_length s) (PreservedSliceLength x))
       (= (s_allocation s) (PreservedSliceAllocation x))
       (= (s_address s) (PreservedSliceAddress x))
       (= (s_provenance s) (PreservedSliceProvenance x))
       (= (s_borrow s) (PreservedSliceBorrow x))
       (= (s_element_size s) (PreservedElementSize x))
       (= (s_element_alignment s) (PreservedElementAlignment x))
       (= (s_frame_token s) (PreservedFrameToken x))
       (=> (not (y_is_ok y))
           (and (= (s_value0 s) (x_value0 x))
                (= (s_value1 s) (x_value1 x))
                (= (s_value2 s) (x_value2 x))))"""


def _equivalence_body(purpose: str) -> str:
    fields = list(OUTPUT_FIELDS)
    if purpose == PRIMARY:
        fields.extend(STATE_FIELDS)
    equalities = []
    output_selectors = {selector for selector, _ in OUTPUT_FIELDS}
    for selector, _ in fields:
        left = "y1" if selector in output_selectors else "s1"
        right = "y2" if selector in output_selectors else "s2"
        equalities.append(f"(= ({selector} {left}) ({selector} {right}))")
    return "  (and " + "\n       ".join(equalities) + "))"


def _model_text(purpose: str) -> str:
    if purpose not in PURPOSES:
        raise ValueError(f"unknown target-051 obligation purpose: {purpose}")
    return f"""\
; Target: {TARGET}
; Active contract SHA-256: {ACTIVE_CONTRACT_SHA256}
; Purpose: {purpose}
; Bounded domain: N=2 usize indices over a non-ZST slice of length 3.
; Validation-loop semantics define only the Result tag. Canonical borrow
; construction is modeled but deliberately not injected into Spec_T.
(set-logic ALL)
(declare-datatypes ((ErrorKind 0))
  (((NoError) (IndexOutOfBounds) (OverlappingIndices))))
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
      (y_is_ok Bool)
      (y_error_kind ErrorKind)
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
(define-fun IndicesOverlap ((x Input)) Bool
  (= (x_index0 x) (x_index1 x)))
(define-fun ValidationLoopError ((x Input)) ErrorKind
  (ite (not (IndexInBounds x (x_index0 x)))
       IndexOutOfBounds
       (ite (not (IndexInBounds x (x_index1 x)))
            IndexOutOfBounds
            (ite (IndicesOverlap x) OverlappingIndices NoError))))
(define-fun ValidationLoopIsValid ((x Input)) Bool
  (= (ValidationLoopError x) NoError))
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
  (and
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
(define-fun InactiveBorrowFields ((y Output)) Bool
  (and (= (y_ref0_index y) (- 1))
       (= (y_ref0_allocation y) 0)
       (= (y_ref0_address y) 0)
       (= (y_ref0_provenance y) 0)
       (= (y_ref0_parent_borrow y) 0)
       (= (y_ref0_value y) 0)
       (= (y_ref1_index y) (- 1))
       (= (y_ref1_allocation y) 0)
       (= (y_ref1_address y) 0)
       (= (y_ref1_provenance y) 0)
       (= (y_ref1_parent_borrow y) 0)
       (= (y_ref1_value y) 0)))
(define-fun ResultEncodingWellFormed ((x Input) (y Output)) Bool
  (ite (y_is_ok y)
       (and (= (y_error_kind y) NoError)
            (ReturnedBorrowArrayWellFormed x y))
       (and (or (= (y_error_kind y) IndexOutOfBounds)
                (= (y_error_kind y) OverlappingIndices))
            (InactiveBorrowFields y))))
(define-fun CanonicalSlot0AfterFirstWrite ((x Input)) Int
  (x_index0 x))
(define-fun CanonicalSlot0AfterSecondWrite ((x Input)) Int
  (CanonicalSlot0AfterFirstWrite x))
(define-fun CanonicalSlot1AfterSecondWrite ((x Input)) Int
  (x_index1 x))
(define-fun CanonicalBorrowArrayConstructed
  ((x Input) (y Output)) Bool
  (and (y_is_ok y)
       (= (y_error_kind y) NoError)
       (= (y_ref0_index y) (CanonicalSlot0AfterSecondWrite x))
       (= (y_ref1_index y) (CanonicalSlot1AfterSecondWrite x))
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
(define-fun PreservedSliceAllocation ((x Input)) Int
  (x_slice_allocation x))
(define-fun PreservedSliceAddress ((x Input)) Int
  (x_slice_address x))
(define-fun PreservedSliceProvenance ((x Input)) Int
  (x_slice_provenance x))
(define-fun PreservedSliceBorrow ((x Input)) Int
  (x_slice_borrow x))
(define-fun PreservedElementSize ((x Input)) Int
  (x_element_size x))
(define-fun PreservedElementAlignment ((x Input)) Int
  (x_element_alignment x))
(define-fun PreservedFrameToken ((x Input)) Int
  (x_frame_token x))
(define-fun ActiveOkConjunct ((x Input) (y Output)) Bool
  (=> (y_is_ok y) (ValidationLoopIsValid x)))
(define-fun ActiveErrConjunct ((x Input) (y Output)) Bool
  (=> (not (y_is_ok y)) (not (ValidationLoopIsValid x))))
(define-fun Requires_T ((x Input)) Bool
  (and (= (x_length x) 3)
       (>= (x_index0 x) 0)
       (>= (x_index1 x) 0)
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
       (= (y_is_ok y) (ValidationLoopIsValid x))
       (ResultEncodingWellFormed x y)
       (ActiveOkConjunct x y)
       (ActiveErrConjunct x y)
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
        BORROW_CONSTRUCTION_REFERENCE,
        INDEX_TRAIT_REFERENCE,
    ]
    return [
        {
            "selector": selector,
            "role": role,
            "source_citations": citations,
            "trust_site_ids": list(ADMITTED_TRUST_SITES),
        }
        for selector, role in roles.items()
    ]


def obligation_metadata(purpose: str) -> dict[str, Any]:
    if purpose not in PURPOSES:
        raise ValueError(f"unknown target-051 obligation purpose: {purpose}")
    source_transitions = ["ValidationLoopIsValid"]
    if purpose == PRIMARY:
        source_transitions.extend(
            [
                "PreservedSliceLength",
                "PreservedSliceAllocation",
                "PreservedSliceAddress",
                "PreservedSliceProvenance",
                "PreservedSliceBorrow",
                "PreservedElementSize",
                "PreservedElementAlignment",
                "PreservedFrameToken",
            ]
        )
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
            "slice_length": 3,
            "element_layout": "positive-size aligned elements",
            "contract_scope": (
                "The active generated Ok/Err implications are complete for "
                "this bounded input family. Returned mutable references also "
                "satisfy Rust reference well-formedness and disjointness, but "
                "are not equated to the implementation-selected indices."
            ),
        },
        "contract_translation": {
            "ok_conjunct": (
                "Ok iff the source validation loop finds both usize indices "
                "in bounds and non-overlapping; final slice length is preserved."
            ),
            "err_conjunct": (
                "Err iff validation fails; the final slice sequence equals "
                "the input sequence. The generated contract does not constrain "
                "which GetDisjointMutError variant is returned."
            ),
            "return_type_invariant": (
                "An Ok payload contains two in-bounds, non-overlapping mutable "
                "references into the receiver allocation with matching value, "
                "address, provenance, and parent-borrow observations."
            ),
            "implementation_choice_exclusion": (
                "Canonical validation error and index-to-borrow construction "
                "are modeled for source checking and probes but are not "
                "conjoined to Spec_T beyond the Result tag and type invariants."
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
                "selected error kind",
                "returned borrow or borrow-array identity",
                "alias map",
                "resulting slice values or aggregate final state",
                "deterministic implementation choice",
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
            "validation_loop": {
                "symbols": [
                    "IndexInBounds",
                    "IndicesOverlap",
                    "ValidationLoopError",
                    "ValidationLoopIsValid",
                ],
                "replaces_trust_site_ids": ["TS-051-D002", "TS-051-E001"],
                "source_citations": [
                    VALIDATION_LOOP_REFERENCE,
                    INDEX_TRAIT_REFERENCE,
                ],
            },
            "disjoint_borrow_construction": {
                "symbols": [
                    "SliceValueAt",
                    "BorrowAddressAtIndex",
                    "BorrowWellFormed",
                    "ReturnedBorrowArrayWellFormed",
                    "CanonicalSlot0AfterFirstWrite",
                    "CanonicalSlot0AfterSecondWrite",
                    "CanonicalSlot1AfterSecondWrite",
                    "CanonicalBorrowArrayConstructed",
                ],
                "replaces_trust_site_ids": ["TS-051-D004", "TS-051-E002"],
                "source_citations": [
                    BORROW_CONSTRUCTION_REFERENCE,
                    INDEX_TRAIT_REFERENCE,
                ],
            },
        },
        "equivalence_kind": "exact",
        "equivalence_scope": (
            "Result tag, error variant, every returned-reference identity/value "
            "field, and every final-slice/frame observation"
            if purpose == PRIMARY
            else "Result tag, error variant, and every returned-reference field"
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
        raise GuardError("target-051 obligation has an unknown purpose")
    expected_text, expected_metadata = obligation(str(purpose))
    if metadata != expected_metadata:
        raise GuardError(
            "target-051 metadata differs from the reviewed active-contract model"
        )
    if parse_smt(text) != parse_smt(expected_text):
        raise GuardError(
            "target-051 SMT differs from the reviewed active-contract model"
        )


def _input_expression(index0: int, index1: int) -> str:
    values = (
        3,
        10,
        20,
        30,
        index0,
        index1,
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


def _error_output(kind: str) -> str:
    inactive = (-1, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0)
    return (
        f"(mkOutput false {kind} "
        + " ".join(map(str, inactive))
        + ")"
    )


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
    return "(mkOutput true NoError " + " ".join(map(str, fields)) + ")"


def _state_expression() -> str:
    return "(mkState 3 10 20 30 41 4096 141 241 4 4 777)"


WITNESS_CASES = {
    "out_of_bounds_error_variants": {
        "indices": (0, 9),
        "output1": _error_output("IndexOutOfBounds"),
        "output2": _error_output("OverlappingIndices"),
    },
    "valid_disjoint_distinct_borrows": {
        "indices": (0, 2),
        "output1": _success_output(0, 2),
        "output2": _success_output(1, 2),
    },
}


def fixed_witness_text(name: str) -> str:
    try:
        case = WITNESS_CASES[name]
    except KeyError as exc:
        raise ValueError(f"unknown target-051 witness: {name}") from exc
    index0, index1 = case["indices"]
    return _model_text(PRIMARY) + f"""\
(assert (= x {_input_expression(index0, index1)}))
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
  (ValidationLoopError x)
  (ValidationLoopIsValid x)
  (y_is_ok y1)
  (y_error_kind y1)
  (y_ref0_index y1)
  (y_ref1_index y1)
  (y_is_ok y2)
  (y_error_kind y2)
  (y_ref0_index y2)
  (y_ref1_index y2)
  (s_value0 s1)
  (s_value0 s2)))
"""


PROBE_CASES = {
    "validation_loop_out_of_bounds": {
        "kind": "source_validation",
        "expected": "sat",
    },
    "validation_loop_overlap": {
        "kind": "source_validation",
        "expected": "sat",
    },
    "canonical_disjoint_construction": {
        "kind": "source_construction",
        "expected": "sat",
    },
    "invalid_success_out_of_bounds_reference": {
        "kind": "invalid_success_reference",
        "expected": "unsat",
    },
    "invalid_success_overlapping_references": {
        "kind": "overlapping_success_references",
        "expected": "unsat",
    },
    "invalid_prior_result_mutation": {
        "kind": "prior_result_mutation",
        "expected": "unsat",
    },
}
PROBE_EXPECTED_RESULTS = {
    name: str(case["expected"]) for name, case in PROBE_CASES.items()
}


def probe_text(name: str) -> str:
    if name not in PROBE_CASES:
        raise ValueError(f"unknown target-051 probe: {name}")
    if name == "validation_loop_out_of_bounds":
        assertions = [
            f"(= x {_input_expression(0, 9)})",
            f"(= b {_boundary_expression()})",
            "(Requires_T x)",
            "(Boundary_T x b)",
            "(= (ValidationLoopError x) IndexOutOfBounds)",
            "(not (ValidationLoopIsValid x))",
        ]
    elif name == "validation_loop_overlap":
        assertions = [
            f"(= x {_input_expression(1, 1)})",
            f"(= b {_boundary_expression()})",
            "(Requires_T x)",
            "(Boundary_T x b)",
            "(= (ValidationLoopError x) OverlappingIndices)",
            "(not (ValidationLoopIsValid x))",
        ]
    elif name == "canonical_disjoint_construction":
        assertions = [
            f"(= x {_input_expression(0, 2)})",
            f"(= b {_boundary_expression()})",
            f"(= y1 {_success_output(0, 2)})",
            "(Requires_T x)",
            "(Boundary_T x b)",
            "(ValidationLoopIsValid x)",
            "(CanonicalBorrowArrayConstructed x y1)",
        ]
    elif name == "invalid_success_out_of_bounds_reference":
        bad = (
            "(mkOutput true NoError "
            "3 41 4108 141 241 0 "
            "2 41 4104 141 241 30)"
        )
        assertions = [
            f"(= x {_input_expression(0, 2)})",
            f"(= b {_boundary_expression()})",
            f"(= y1 {bad})",
            f"(= s1 {_state_expression()})",
            "(Requires_T x)",
            "(Boundary_T x b)",
            "(Spec_T x b y1 s1)",
        ]
    elif name == "invalid_success_overlapping_references":
        assertions = [
            f"(= x {_input_expression(0, 2)})",
            f"(= b {_boundary_expression()})",
            f"(= y1 {_success_output(0, 0)})",
            f"(= s1 {_state_expression()})",
            "(Requires_T x)",
            "(Boundary_T x b)",
            "(Spec_T x b y1 s1)",
        ]
    else:
        assertions = [
            f"(= x {_input_expression(0, 2)})",
            f"(= b {_boundary_expression()})",
            "(Requires_T x)",
            "(Boundary_T x b)",
            "(ValidationLoopIsValid x)",
            "(not (= (CanonicalSlot0AfterSecondWrite x) (x_index0 x)))",
        ]
    body = "\n       ".join(assertions)
    return _model_text(PRIMARY) + f"""\
(assert
  (and {body}))
(check-sat)
"""


def witness_payload() -> dict[str, Any]:
    shared_input = {
        "length": 3,
        "values": [10, 20, 30],
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
        if key != "values"
    }
    boundary["values"] = list(shared_input["values"])
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
        "out_of_bounds_error_variants": {
            "input": {**shared_input, "indices": [0, 9]},
            "boundary": boundary,
            "execution1": {
                "result": {"tag": "Err", "error": "IndexOutOfBounds"},
                "final_state": unchanged_state,
            },
            "execution2": {
                "result": {"tag": "Err", "error": "OverlappingIndices"},
                "final_state": unchanged_state,
            },
            "expected": {
                "shared_boundary": True,
                "validation_error": "IndexOutOfBounds",
                "execution1_satisfies_contract": True,
                "execution2_satisfies_contract": True,
                "exact_output_equal": False,
                "exact_final_state_equal": True,
                "exact_equivalent": False,
            },
        },
        "valid_disjoint_distinct_borrows": {
            "input": {**shared_input, "indices": [0, 2]},
            "boundary": boundary,
            "execution1": {
                "result": {
                    "tag": "Ok",
                    "borrows": [
                        {
                            "index": 0,
                            "allocation": 41,
                            "address": 4096,
                            "provenance": 141,
                            "parent_borrow": 241,
                            "value": 10,
                        },
                        {
                            "index": 2,
                            "allocation": 41,
                            "address": 4104,
                            "provenance": 141,
                            "parent_borrow": 241,
                            "value": 30,
                        },
                    ],
                },
                "final_state": unchanged_state,
            },
            "execution2": {
                "result": {
                    "tag": "Ok",
                    "borrows": [
                        {
                            "index": 1,
                            "allocation": 41,
                            "address": 4100,
                            "provenance": 141,
                            "parent_borrow": 241,
                            "value": 20,
                        },
                        {
                            "index": 2,
                            "allocation": 41,
                            "address": 4104,
                            "provenance": 141,
                            "parent_borrow": 241,
                            "value": 30,
                        },
                    ],
                },
                "final_state": unchanged_state,
            },
            "expected": {
                "shared_boundary": True,
                "validation_error": "NoError",
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
        "bounded_domain": "N=2 usize indices, length-3 non-ZST slice",
        "boundary_narrower_than_target": True,
        "shared_boundary_observations": [
            {
                "fields": ["b_length", "b_value0", "b_value1", "b_value2"],
                "kind": "initial receiver slice values",
                "trust_site_ids": list(ADMITTED_TRUST_SITES),
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
                "trust_site_ids": list(ADMITTED_TRUST_SITES),
            },
            {
                "fields": [
                    "b_element_size",
                    "b_element_alignment",
                    "b_isize_max",
                    "b_address_space_limit",
                ],
                "kind": "element layout and target-platform pointer limits",
                "trust_site_ids": list(ADMITTED_TRUST_SITES),
            },
            {
                "fields": ["b_frame_token"],
                "kind": "pre-existing memory outside the receiver",
                "trust_site_ids": list(ADMITTED_TRUST_SITES),
            },
        ],
        "forbidden_boundary_observations": [
            "validity bit",
            "opaque validity relation",
            "error kind",
            "returned borrow",
            "alias map",
            "resulting state",
            "answer-equivalent encoding",
            "deterministic implementation choice",
            "full execution trace",
        ],
        "deterministic_source_semantics": [
            {
                "operation": "get_disjoint_check_valid",
                "semantics": (
                    "Checks index 0 in bounds, then index 1 in bounds, then "
                    "index 1 against index 0 for overlap; the first failed "
                    "check selects the implementation error variant."
                ),
                "source_citations": [
                    VALIDATION_LOOP_REFERENCE,
                    INDEX_TRAIT_REFERENCE,
                ],
                "replaces_trust_site_ids": ["TS-051-D002", "TS-051-E001"],
            },
            {
                "operation": "get_disjoint_unchecked_mut borrow-array loop",
                "semantics": (
                    "Each loop iteration clones its input index, derives the "
                    "receiver element address/provenance/value, writes exactly "
                    "that mutable reference to its MaybeUninit slot, preserves "
                    "prior slots, and assumes initialization only after both writes."
                ),
                "source_citations": [
                    BORROW_CONSTRUCTION_REFERENCE,
                    INDEX_TRAIT_REFERENCE,
                ],
                "replaces_trust_site_ids": ["TS-051-D004", "TS-051-E002"],
            },
        ],
        "spec_relation_policy": (
            "Spec_T is the active generated contract relation. It fixes the "
            "Ok/Err tag through source-backed validity and enforces Rust "
            "reference type invariants, but does not inject the implementation's "
            "error variant or exact index-to-borrow selection."
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
