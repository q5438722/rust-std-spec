#!/usr/bin/env python3
"""Per-slot source model for input order 120, write_copy_of_slice."""

from __future__ import annotations

from typing import Any

from checker_guards import GuardError, parse_smt, validate_obligation


TARGET = "core::slice::write_copy_of_slice"
INPUT_ORDER = "120"
ARTIFACT_ID = "120_core_slice_write_copy_of_slice"
ACTIVE_CONTRACT_SHA256 = (
    "09f266d66c804f7e0f5f296f4050ba156240da188db824b5f5f6efc0a0145e69"
)
ACTIVE_CONTRACT_TEXT = (
    "pub assume_specification<'a, 'b, T: core::marker::Copy>[ "
    "<[core::mem::MaybeUninit<T>]>::write_copy_of_slice ]( slice: &'a mut "
    "[core::mem::MaybeUninit<T>], src: &'b [T], ) -> (ret: &'a mut [T]) "
    "requires old(slice)@.len() == src@.len(), ensures ret@ == src@, "
    "ret@.len() == src@.len(), final(slice)@.len() == old(slice)@.len(), "
    "maybe_uninit_relation_well_formed( maybe_uninit_seq_relation(old(slice)@), "
    "old(slice)@.len() as int, ), maybe_uninit_relation_well_formed( "
    "maybe_uninit_seq_relation(final(slice)@), final(slice)@.len() as int, ), "
    "maybe_uninit_written_from( maybe_uninit_seq_relation(old(slice)@), "
    "maybe_uninit_seq_relation(final(slice)@), src@, ), "
    "maybe_uninit_all_initialized(maybe_uninit_seq_relation(final(slice)@)), "
    "final(ret)@.len() == src@.len(), "
    "maybe_uninit_seq_relation(final(slice)@).values == final(ret)@, ;"
)

PRIMARY = "completeness-modulo-reviewed-equivalence"
EXACT_OUTPUT = "exact-output-determinism"
PURPOSES = (PRIMARY, EXACT_OUTPUT)

TARGET_SOURCE_REFERENCE = "core/src/mem/maybe_uninit.rs:1120-1173"
TRANSMUTE_REFERENCE = "core/src/intrinsics/mod.rs:790-841"
COPY_FROM_SLICE_REFERENCE = "core/src/slice/mod.rs:5548-5586"
COPY_NONOVERLAPPING_REFERENCE = "core/src/ptr/mod.rs:440-546"
ASSUME_INIT_MUT_REFERENCE = "core/src/mem/maybe_uninit.rs:1512-1531"

CANONICAL_SOURCE_BINDINGS = {
    "copy_from_slice": {
        "path": "core/src/slice/mod.rs",
        "start": 5548,
        "end": 5586,
        "file_sha256": (
            "58901fa6437dbd4d77c68427bbced0fc3a91a10fdb8bd2e233adf6a9ba27d2d5"
        ),
        "excerpt_sha256": (
            "5b21f0f22a40660651ad146097432b6029f1565937b2a257ef879c44e29300e0"
        ),
    },
    "copy_nonoverlapping": {
        "path": "core/src/ptr/mod.rs",
        "start": 440,
        "end": 546,
        "file_sha256": (
            "1fd4ecb1650cfc995f29a172ad3f72ffa378702ea55493eabf6a80355b38035e"
        ),
        "excerpt_sha256": (
            "1040f9d57326a1712dc3264227e4c180fcb7359751db22c094dbe5ff3ce20842"
        ),
    },
    "transmute": {
        "path": "core/src/intrinsics/mod.rs",
        "start": 790,
        "end": 841,
        "file_sha256": (
            "6584f906e1a4c974d9493846036a6df8322e35798eb920833e90d79cd2cf69c3"
        ),
        "excerpt_sha256": (
            "ad537b6cf085c494780e7a481bbc553e1fae7fc5e13ed28cd7d31cb36b313dd7"
        ),
    },
    "assume_init_mut": {
        "path": "core/src/mem/maybe_uninit.rs",
        "start": 1512,
        "end": 1531,
        "file_sha256": (
            "cd1152779de3a6bc96b29997e8a95d3beb9ff1018f99223b429ed0df66baa8ef"
        ),
        "excerpt_sha256": (
            "e276199bdbc2730255ce8baaf5e4bf20cde269cc2f42c72cdcee7b92e045d023"
        ),
    },
}

EXCLUDED_RETAINED_TRUST_SITES = ("TS-120-D004", "TS-120-E005")
ADMITTED_TRUST_SITES = (
    "TS-120-D002",
    "TS-120-D003",
    "TS-120-D005",
    "TS-120-E001",
    "TS-120-E002",
    "TS-120-E003",
    "TS-120-E004",
    "TS-120-E006",
)
ALL_AUDITED_TRUST_SITES = (
    "TS-120-D001",
    "TS-120-D002",
    "TS-120-D003",
    "TS-120-D004",
    "TS-120-D005",
    "TS-120-C001",
    "TS-120-E001",
    "TS-120-E002",
    "TS-120-E003",
    "TS-120-E004",
    "TS-120-E005",
    "TS-120-E006",
)

ACTIVE_CONJUNCT_SYMBOLS = (
    "ActiveReturnEqualsSourceConjunct",
    "ActiveReturnLengthConjunct",
    "ActiveFinalDestinationLengthConjunct",
    "ActiveInitialRelationWellFormedConjunct",
    "ActiveFinalRelationWellFormedConjunct",
    "ActiveWrittenFromConjunct",
    "ActiveAllInitializedConjunct",
    "ActiveFinalReturnLengthConjunct",
    "ActiveFinalStorageEqualsReturnConjunct",
)

OUTPUT_FIELDS = (
    ("y_return_allocation", "Int"),
    ("y_return_address", "Int"),
    ("y_return_provenance", "Int"),
    ("y_return_borrow", "Int"),
    ("y_return_length", "Int"),
    ("y_return_values", "Array Int Int"),
)

STATE_FIELDS = (
    ("s_destination_length", "Int"),
    ("s_destination_storage", "Array Int Cell"),
    ("s_destination_allocation", "Int"),
    ("s_destination_address", "Int"),
    ("s_destination_provenance", "Int"),
    ("s_destination_borrow", "Int"),
    ("s_destination_allocation_base", "Int"),
    ("s_destination_allocation_bytes", "Int"),
    ("s_source_length", "Int"),
    ("s_source_values", "Array Int Int"),
    ("s_source_allocation", "Int"),
    ("s_source_address", "Int"),
    ("s_source_provenance", "Int"),
    ("s_source_allocation_base", "Int"),
    ("s_source_allocation_bytes", "Int"),
    ("s_return_length", "Int"),
    ("s_return_values", "Array Int Int"),
    ("s_return_allocation", "Int"),
    ("s_return_address", "Int"),
    ("s_return_provenance", "Int"),
    ("s_return_borrow", "Int"),
    ("s_element_size", "Int"),
    ("s_element_alignment", "Int"),
    ("s_isize_max", "Int"),
    ("s_address_space_limit", "Int"),
    ("s_frame_token", "Int"),
)

OUTPUT_SOURCE_TRANSITIONS = (
    "AssumeInitReturnAllocation",
    "AssumeInitReturnAddress",
    "AssumeInitReturnProvenance",
    "AssumeInitReturnBorrow",
    "AssumeInitReturnLength",
    "AssumeInitReturnValues",
)

STATE_SOURCE_TRANSITIONS = (
    "FinalDestinationLength",
    "FinalDestinationStorage",
    "FinalDestinationAllocation",
    "FinalDestinationAddress",
    "FinalDestinationProvenance",
    "FinalDestinationBorrow",
    "FinalDestinationAllocationBase",
    "FinalDestinationAllocationBytes",
    "PreservedSourceLength",
    "PreservedSourceValues",
    "PreservedSourceAllocation",
    "PreservedSourceAddress",
    "PreservedSourceProvenance",
    "PreservedSourceAllocationBase",
    "PreservedSourceAllocationBytes",
    "FinalReturnLength",
    "FinalReturnValues",
    "FinalReturnAllocation",
    "FinalReturnAddress",
    "FinalReturnProvenance",
    "FinalReturnBorrow",
    "PreservedElementSize",
    "PreservedElementAlignment",
    "PreservedIsizeMax",
    "PreservedAddressSpaceLimit",
    "PreservedFrameToken",
)


def _state_declaration(purpose: str) -> str:
    if purpose == EXACT_OUTPUT:
        return "(declare-datatypes ((State 0)) (((mkState))))"
    fields = "\n".join(
        f"      ({selector} ({sort}))"
        if sort.startswith("Array ")
        else f"      ({selector} {sort})"
        for selector, sort in STATE_FIELDS
    )
    return (
        "(declare-datatypes ((State 0))\n"
        "  (((mkState\n"
        f"{fields}))))"
    )


def _state_equalities(purpose: str) -> str:
    if purpose == EXACT_OUTPUT:
        return "       (DeterministicFinalContract x y)"
    equalities = [
        f"       (= ({selector} s) ({transition} x))"
        for (selector, _), transition in zip(
            STATE_FIELDS, STATE_SOURCE_TRANSITIONS, strict=True
        )
    ]
    return "\n".join(equalities)


def _equivalence_body(purpose: str) -> str:
    equalities = [
        f"(= ({selector} y1) ({selector} y2))"
        for selector, _ in OUTPUT_FIELDS
    ]
    if purpose == PRIMARY:
        equalities.extend(
            f"(= ({selector} s1) ({selector} s2))"
            for selector, _ in STATE_FIELDS
        )
    return "  (and " + "\n       ".join(equalities) + "))"


def _model_text(purpose: str) -> str:
    if purpose not in PURPOSES:
        raise ValueError(f"unknown target-120 obligation purpose: {purpose}")
    output_equalities = "\n".join(
        f"       (= ({selector} y) ({transition} x))"
        for (selector, _), transition in zip(
            OUTPUT_FIELDS, OUTPUT_SOURCE_TRANSITIONS, strict=True
        )
    )
    return f"""\
; Target: {TARGET}
; Active contract SHA-256: {ACTIVE_CONTRACT_SHA256}
; Purpose: {purpose}
; Initial MaybeUninit values are observed only at initialized slots.
; Final storage is derived slot-by-slot by the canonical raw-copy transition.
(set-logic ALL)
(declare-datatypes ((Cell 0))
  (((Uninitialized)
    (Initialized (initialized_value Int)))))
(declare-datatypes ((Input 0))
  (((mkInput
      (x_destination_length Int)
      (x_source_length Int)
      (x_destination_storage (Array Int Cell))
      (x_source_values (Array Int Int))
      (x_destination_allocation Int)
      (x_destination_address Int)
      (x_destination_provenance Int)
      (x_destination_borrow Int)
      (x_destination_allocation_base Int)
      (x_destination_allocation_bytes Int)
      (x_source_allocation Int)
      (x_source_address Int)
      (x_source_provenance Int)
      (x_source_allocation_base Int)
      (x_source_allocation_bytes Int)
      (x_element_size Int)
      (x_element_alignment Int)
      (x_isize_max Int)
      (x_address_space_limit Int)
      (x_frame_token Int)))))
(declare-datatypes ((Boundary 0))
  (((mkBoundary
      (b_destination_length Int)
      (b_source_length Int)
      (b_destination_storage (Array Int Cell))
      (b_source_values (Array Int Int))
      (b_destination_allocation Int)
      (b_destination_address Int)
      (b_destination_provenance Int)
      (b_destination_borrow Int)
      (b_destination_allocation_base Int)
      (b_destination_allocation_bytes Int)
      (b_source_allocation Int)
      (b_source_address Int)
      (b_source_provenance Int)
      (b_source_allocation_base Int)
      (b_source_allocation_bytes Int)
      (b_element_size Int)
      (b_element_alignment Int)
      (b_isize_max Int)
      (b_address_space_limit Int)
      (b_frame_token Int)))))
(declare-datatypes ((Output 0))
  (((mkOutput
      (y_return_allocation Int)
      (y_return_address Int)
      (y_return_provenance Int)
      (y_return_borrow Int)
      (y_return_length Int)
      (y_return_values (Array Int Int))))))
{_state_declaration(purpose)}
(declare-const x Input)
(declare-const b Boundary)
(declare-const y1 Output)
(declare-const s1 State)
(declare-const y2 Output)
(declare-const s2 State)
(define-fun CopyByteCount ((x Input)) Int
  (* (x_destination_length x) (x_element_size x)))
(define-fun CanonicalSourceValues ((x Input)) (Array Int Int)
  (x_source_values x))
(define-fun SameLayoutTransmuteValues ((x Input)) (Array Int Int)
  (CanonicalSourceValues x))
(define-fun InitialStorageObserved ((x Input) (b Boundary)) Bool
  (and (= (b_destination_length b) (x_destination_length x))
       (= (b_source_length b) (x_source_length x))
       (= (b_destination_allocation b) (x_destination_allocation x))
       (= (b_destination_address b) (x_destination_address x))
       (= (b_destination_provenance b) (x_destination_provenance x))
       (= (b_destination_borrow b) (x_destination_borrow x))
       (= (b_destination_allocation_base b)
          (x_destination_allocation_base x))
       (= (b_destination_allocation_bytes b)
          (x_destination_allocation_bytes x))
       (= (b_source_allocation b) (x_source_allocation x))
       (= (b_source_address b) (x_source_address x))
       (= (b_source_provenance b) (x_source_provenance x))
       (= (b_source_allocation_base b) (x_source_allocation_base x))
       (= (b_source_allocation_bytes b) (x_source_allocation_bytes x))
       (= (b_element_size b) (x_element_size x))
       (= (b_element_alignment b) (x_element_alignment x))
       (= (b_isize_max b) (x_isize_max x))
       (= (b_address_space_limit b) (x_address_space_limit x))
       (= (b_frame_token b) (x_frame_token x))
       (= (b_destination_storage b)
          (x_destination_storage x))
       (= (b_source_values b) (CanonicalSourceValues x))))
(define-fun FinalDestinationStorage ((x Input)) (Array Int Cell)
  ((_ map Initialized) (SameLayoutTransmuteValues x)))
(define-fun FinalDestinationLength ((x Input)) Int
  (x_destination_length x))
(define-fun FinalDestinationAllocation ((x Input)) Int
  (x_destination_allocation x))
(define-fun FinalDestinationAddress ((x Input)) Int
  (x_destination_address x))
(define-fun FinalDestinationProvenance ((x Input)) Int
  (x_destination_provenance x))
(define-fun FinalDestinationBorrow ((x Input)) Int
  (x_destination_borrow x))
(define-fun FinalDestinationAllocationBase ((x Input)) Int
  (x_destination_allocation_base x))
(define-fun FinalDestinationAllocationBytes ((x Input)) Int
  (x_destination_allocation_bytes x))
(define-fun AssumeInitReturnAllocation ((x Input)) Int
  (FinalDestinationAllocation x))
(define-fun AssumeInitReturnAddress ((x Input)) Int
  (FinalDestinationAddress x))
(define-fun AssumeInitReturnProvenance ((x Input)) Int
  (FinalDestinationProvenance x))
(define-fun AssumeInitReturnBorrow ((x Input)) Int
  (FinalDestinationBorrow x))
(define-fun AssumeInitReturnLength ((x Input)) Int
  (FinalDestinationLength x))
(define-fun AssumeInitReturnValues ((x Input)) (Array Int Int)
  (SameLayoutTransmuteValues x))
(define-fun PreservedSourceLength ((x Input)) Int
  (x_source_length x))
(define-fun PreservedSourceValues ((x Input)) (Array Int Int)
  (CanonicalSourceValues x))
(define-fun PreservedSourceAllocation ((x Input)) Int
  (x_source_allocation x))
(define-fun PreservedSourceAddress ((x Input)) Int
  (x_source_address x))
(define-fun PreservedSourceProvenance ((x Input)) Int
  (x_source_provenance x))
(define-fun PreservedSourceAllocationBase ((x Input)) Int
  (x_source_allocation_base x))
(define-fun PreservedSourceAllocationBytes ((x Input)) Int
  (x_source_allocation_bytes x))
(define-fun FinalReturnLength ((x Input)) Int
  (AssumeInitReturnLength x))
(define-fun FinalReturnValues ((x Input)) (Array Int Int)
  (AssumeInitReturnValues x))
(define-fun FinalReturnAllocation ((x Input)) Int
  (AssumeInitReturnAllocation x))
(define-fun FinalReturnAddress ((x Input)) Int
  (AssumeInitReturnAddress x))
(define-fun FinalReturnProvenance ((x Input)) Int
  (AssumeInitReturnProvenance x))
(define-fun FinalReturnBorrow ((x Input)) Int
  (AssumeInitReturnBorrow x))
(define-fun PreservedElementSize ((x Input)) Int
  (x_element_size x))
(define-fun PreservedElementAlignment ((x Input)) Int
  (x_element_alignment x))
(define-fun PreservedIsizeMax ((x Input)) Int
  (x_isize_max x))
(define-fun PreservedAddressSpaceLimit ((x Input)) Int
  (x_address_space_limit x))
(define-fun PreservedFrameToken ((x Input)) Int
  (x_frame_token x))
(define-fun ActiveReturnEqualsSourceConjunct
  ((x Input) (y Output)) Bool
  (= (y_return_values y) (CanonicalSourceValues x)))
(define-fun ActiveReturnLengthConjunct ((x Input) (y Output)) Bool
  (= (y_return_length y) (x_source_length x)))
(define-fun ActiveFinalDestinationLengthConjunct
  ((x Input) (final_length Int)) Bool
  (= final_length (x_destination_length x)))
(define-fun ActiveInitialRelationWellFormedConjunct ((x Input)) Bool
  (and (>= (x_destination_length x) 0)
       (= (x_destination_length x) (x_source_length x))))
(define-fun ActiveFinalRelationWellFormedConjunct
  ((x Input) (final_length Int)) Bool
  (and (>= final_length 0)
       (= final_length (x_source_length x))))
(define-fun ActiveWrittenFromConjunct
  ((x Input)
   (final_length Int)
   (final_storage (Array Int Cell))) Bool
  (and (= final_length (x_source_length x))
       (= final_storage
          ((_ map Initialized) (CanonicalSourceValues x)))))
(define-fun ActiveAllInitializedConjunct
  ((x Input)
   (final_length Int)
   (final_storage (Array Int Cell))) Bool
  (= final_storage
     ((_ map Initialized) (CanonicalSourceValues x))))
(define-fun ActiveFinalReturnLengthConjunct
  ((x Input) (final_return_length Int)) Bool
  (= final_return_length (x_source_length x)))
(define-fun ActiveFinalStorageEqualsReturnConjunct
  ((final_storage (Array Int Cell))
   (final_return_values (Array Int Int))) Bool
  (= final_storage ((_ map Initialized) final_return_values)))
(define-fun DeterministicFinalContract ((x Input) (y Output)) Bool
  (and
    (ActiveFinalDestinationLengthConjunct
      x (FinalDestinationLength x))
    (ActiveInitialRelationWellFormedConjunct x)
    (ActiveFinalRelationWellFormedConjunct
      x (FinalDestinationLength x))
    (ActiveWrittenFromConjunct
      x
      (FinalDestinationLength x)
      (FinalDestinationStorage x))
    (ActiveAllInitializedConjunct
      x
      (FinalDestinationLength x)
      (FinalDestinationStorage x))
    (ActiveFinalReturnLengthConjunct x (FinalReturnLength x))
    (ActiveFinalStorageEqualsReturnConjunct
      (FinalDestinationStorage x)
      (FinalReturnValues x))
    (= (y_return_values y) (FinalReturnValues x))))
(define-fun Requires_T ((x Input)) Bool
  (and (>= (x_destination_length x) 0)
       (= (x_destination_length x) (x_source_length x))
       (> (x_destination_address x) 0)
       (> (x_source_address x) 0)
       (> (x_destination_borrow x) 0)
       (>= (x_destination_allocation x) 0)
       (>= (x_destination_provenance x) 0)
       (>= (x_destination_allocation_base x) 0)
       (>= (x_destination_allocation_bytes x) 0)
       (>= (x_source_allocation x) 0)
       (>= (x_source_provenance x) 0)
       (>= (x_source_allocation_base x) 0)
       (>= (x_source_allocation_bytes x) 0)
       (>= (x_element_size x) 0)
       (> (x_element_alignment x) 0)
       (> (x_isize_max x) 0)
       (> (x_address_space_limit x) 0)
       (= (mod (x_destination_address x) (x_element_alignment x)) 0)
       (= (mod (x_source_address x) (x_element_alignment x)) 0)
       (or (= (x_element_size x) 0)
           (and (>= (x_element_size x) (x_element_alignment x))
                (= (mod (x_element_size x) (x_element_alignment x)) 0)))
       (<= (CopyByteCount x) (x_isize_max x))
       (<= (+ (x_destination_address x) (CopyByteCount x))
           (x_address_space_limit x))
       (<= (+ (x_source_address x) (CopyByteCount x))
           (x_address_space_limit x))
       (or (= (CopyByteCount x) 0)
           (and (> (x_destination_allocation x) 0)
                (> (x_destination_provenance x) 0)
                (> (x_source_allocation x) 0)
                (> (x_source_provenance x) 0)
                (<= (x_destination_allocation_base x)
                    (x_destination_address x))
                (<= (+ (x_destination_address x) (CopyByteCount x))
                    (+ (x_destination_allocation_base x)
                       (x_destination_allocation_bytes x)))
                (<= (x_source_allocation_base x) (x_source_address x))
                (<= (+ (x_source_address x) (CopyByteCount x))
                    (+ (x_source_allocation_base x)
                       (x_source_allocation_bytes x)))
                (or (not (= (x_destination_allocation x)
                            (x_source_allocation x)))
                    (<= (+ (x_destination_address x) (CopyByteCount x))
                        (x_source_address x))
                    (<= (+ (x_source_address x) (CopyByteCount x))
                        (x_destination_address x)))))
       (ActiveInitialRelationWellFormedConjunct x)))
(define-fun Boundary_T ((x Input) (b Boundary)) Bool
  (and (>= (b_destination_length b) 0)
       (>= (b_source_length b) 0)
       (> (b_destination_address b) 0)
       (> (b_source_address b) 0)
       (> (b_destination_borrow b) 0)
       (> (b_element_alignment b) 0)
       (> (b_isize_max b) 0)
       (> (b_address_space_limit b) 0)
       (InitialStorageObserved x b)))
(define-fun TargetDefinition_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and (InitialStorageObserved x b)
{output_equalities}
{_state_equalities(purpose)}
       (ActiveReturnEqualsSourceConjunct x y)
       (ActiveReturnLengthConjunct x y)
       (DeterministicFinalContract x y)))
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
    fields = (
        ("b_destination_length", "input_memory", ("TS-120-D003",)),
        ("b_source_length", "input_memory", ("TS-120-D002", "TS-120-D003")),
        (
            "b_destination_storage",
            "input_initialization",
            ("TS-120-E003", "TS-120-E004"),
        ),
        ("b_source_values", "input_memory", ("TS-120-D002", "TS-120-E001")),
        (
            "b_destination_allocation",
            "input_memory",
            ("TS-120-E003", "TS-120-E004"),
        ),
        (
            "b_destination_address",
            "input_memory",
            ("TS-120-E003", "TS-120-E004"),
        ),
        (
            "b_destination_provenance",
            "input_provenance",
            ("TS-120-E003", "TS-120-E004"),
        ),
        ("b_destination_borrow", "input_provenance", ("TS-120-E003", "TS-120-E006")),
        (
            "b_destination_allocation_base",
            "input_memory",
            ("TS-120-E003", "TS-120-E004"),
        ),
        (
            "b_destination_allocation_bytes",
            "input_memory",
            ("TS-120-E003", "TS-120-E004"),
        ),
        ("b_source_allocation", "input_memory", ("TS-120-E002", "TS-120-E004")),
        ("b_source_address", "input_memory", ("TS-120-E002", "TS-120-E004")),
        (
            "b_source_provenance",
            "input_provenance",
            ("TS-120-E002", "TS-120-E004"),
        ),
        (
            "b_source_allocation_base",
            "input_memory",
            ("TS-120-E002", "TS-120-E004"),
        ),
        (
            "b_source_allocation_bytes",
            "input_memory",
            ("TS-120-E002", "TS-120-E004"),
        ),
        ("b_element_size", "input_layout", ("TS-120-D002", "TS-120-E004")),
        ("b_element_alignment", "input_layout", ("TS-120-D002", "TS-120-E004")),
        ("b_isize_max", "input_layout", ("TS-120-E004",)),
        ("b_address_space_limit", "input_layout", ("TS-120-E004",)),
        ("b_frame_token", "input_memory", ("TS-120-E004",)),
    )
    citations = [
        TARGET_SOURCE_REFERENCE,
        TRANSMUTE_REFERENCE,
        COPY_FROM_SLICE_REFERENCE,
        COPY_NONOVERLAPPING_REFERENCE,
        ASSUME_INIT_MUT_REFERENCE,
    ]
    return [
        {
            "selector": selector,
            "role": role,
            "source_citations": citations,
            "trust_site_ids": list(trust_sites),
        }
        for selector, role, trust_sites in fields
    ]


def obligation_metadata(purpose: str) -> dict[str, Any]:
    if purpose not in PURPOSES:
        raise ValueError(f"unknown target-120 obligation purpose: {purpose}")
    return {
        "schema_version": 2,
        "target": TARGET,
        "input_order": INPUT_ORDER,
        "obligation_purpose": purpose,
        "active_contract_sha256": ACTIVE_CONTRACT_SHA256,
        "active_contract_text": ACTIVE_CONTRACT_TEXT,
        "domain": {
            "length": (
                "arbitrary equal nonnegative destination and source lengths, "
                "including zero"
            ),
            "initialization": (
                    "arbitrary destination cell array whose Uninitialized variant "
                    "contains no value and whose Initialized variant contains one value"
            ),
            "values": "arbitrary initialized source and destination values",
            "memory": (
                "non-null aligned source/destination pointers; nonzero byte "
                "copies require valid allocation/provenance and disjoint ranges"
            ),
            "layout": (
                "arbitrary nonnegative element size and positive alignment, "
                "including zero-sized types, with isize-fit and no-wrap"
            ),
        },
        "contract_translation": {
            "active_conjuncts": list(ACTIVE_CONJUNCT_SYMBOLS),
            "source_flow": [
                "same-layout &[T] to &[MaybeUninit<T>] transmute",
                "equal-length copy_from_slice branch",
                "slice pointer exposure and copy_nonoverlapping",
                "per-slot initialization and value copy",
                "initialized-storage assume_init_mut cast",
            ],
            "copy_semantics": (
                "array-map of the Initialized constructor gives the per-slot "
                "rule destination[i] = Initialized(source[i]); the transition "
                "never projects a value from an Uninitialized destination cell"
            ),
            "final_state_projection": (
                "explicit theorem state"
                if purpose == PRIMARY
                else "source-derived final contract retained while comparing output"
            ),
        },
        "boundary_scope": {
            "shared_observations": [
                "initial source length, values, allocation, address, and provenance",
                "initial destination length and Uninitialized-or-Initialized(value) cells",
                "initial destination allocation, address, provenance, and mutable-borrow identity",
                "element layout and target-platform pointer limits",
                "pre-existing memory frame token",
            ],
            "excluded_observations": [
                "resulting destination initialization mask or values",
                "returned reference identity or values",
                "aggregate final storage",
                "answer-equivalent storage-effect relation",
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
        "source_transition_definitions": list(
            OUTPUT_SOURCE_TRANSITIONS
            + (() if purpose == EXACT_OUTPUT else STATE_SOURCE_TRANSITIONS)
        ),
        "source_transition_bindings": {
            "same_layout_transmute": {
                "symbols": [
                    "SameLayoutTransmuteValues",
                    "CanonicalSourceValues",
                ],
                "trust_site_ids": ["TS-120-D002", "TS-120-E001"],
                "source_citations": [
                    TARGET_SOURCE_REFERENCE,
                    TRANSMUTE_REFERENCE,
                ],
            },
            "copy_from_slice_equal_length_flow": {
                "symbols": ["CopyByteCount"],
                "trust_site_ids": ["TS-120-D003"],
                "source_citations": [
                    TARGET_SOURCE_REFERENCE,
                    COPY_FROM_SLICE_REFERENCE,
                ],
            },
            "copy_nonoverlapping_per_slot": {
                "symbols": [
                    "FinalDestinationStorage",
                ],
                "trust_site_ids": [
                    "TS-120-E002",
                    "TS-120-E003",
                    "TS-120-E004",
                ],
                "replaces_trust_site_ids": [
                    "TS-120-D004",
                    "TS-120-E005",
                ],
                "source_citations": [
                    COPY_FROM_SLICE_REFERENCE,
                    COPY_NONOVERLAPPING_REFERENCE,
                ],
            },
            "assume_init_mut": {
                "symbols": list(OUTPUT_SOURCE_TRANSITIONS)
                + [
                    "FinalReturnLength",
                    "FinalReturnValues",
                    "FinalReturnAllocation",
                    "FinalReturnAddress",
                    "FinalReturnProvenance",
                    "FinalReturnBorrow",
                ],
                "trust_site_ids": ["TS-120-D005", "TS-120-E006"],
                "source_citations": [
                    TARGET_SOURCE_REFERENCE,
                    ASSUME_INIT_MUT_REFERENCE,
                ],
            },
            "preserved_source_and_frame": {
                "symbols": [
                    symbol
                    for symbol in STATE_SOURCE_TRANSITIONS
                    if symbol.startswith("Preserved")
                ],
                "source_citations": [
                    TARGET_SOURCE_REFERENCE,
                    COPY_NONOVERLAPPING_REFERENCE,
                ],
            },
        },
        "equivalence_kind": "exact",
        "equivalence_scope": (
            "returned reference identity and values plus every destination, "
            "source, layout, return-view, and frame observation"
            if purpose == PRIMARY
            else "returned reference identity, length, and values"
        ),
        "principal_observations": _principal_observations(purpose),
        "expected_solver_result": "unsat",
    }


def obligation(purpose: str) -> tuple[str, dict[str, Any]]:
    return obligation_text(purpose), obligation_metadata(purpose)


def validate_target_obligation(text: str, metadata: dict[str, Any]) -> None:
    validate_obligation(text, metadata)
    purpose = metadata.get("obligation_purpose")
    if purpose not in PURPOSES:
        raise GuardError("target-120 obligation has an unknown purpose")
    expected_text, expected_metadata = obligation(str(purpose))
    if metadata != expected_metadata:
        raise GuardError(
            "target-120 metadata differs from the reviewed per-slot translation"
        )
    if parse_smt(text) != parse_smt(expected_text):
        raise GuardError(
            "target-120 SMT differs from the reviewed per-slot translation"
        )


def _array_expr(
    sort: str,
    default: int | bool,
    updates: dict[int, int | bool],
) -> str:
    if isinstance(default, bool):
        default_text = "true" if default else "false"
    else:
        default_text = str(default)
    expression = f"((as const (Array Int {sort})) {default_text})"
    for index, value in sorted(updates.items()):
        value_text = (
            ("true" if value else "false")
            if isinstance(value, bool)
            else str(value)
        )
        expression = f"(store {expression} {index} {value_text})"
    return expression


def _cell_array_expr(
    initialized: dict[int, bool],
    values: dict[int, int],
) -> str:
    expression = "((as const (Array Int Cell)) Uninitialized)"
    for index in sorted(key for key, value in initialized.items() if value):
        expression = (
            f"(store {expression} {index} "
            f"(Initialized {values[index]}))"
        )
    return expression


def _base_case(
    *,
    destination_length: int,
    source_length: int | None = None,
    source_values: dict[int, int] | None = None,
    initialized_indices: tuple[int, ...] = (),
    destination_values: dict[int, int] | None = None,
) -> dict[str, Any]:
    return {
        "destination_length": destination_length,
        "source_length": (
            destination_length if source_length is None else source_length
        ),
        "source_values": source_values or {},
        "destination_initialized": {
            index: True for index in initialized_indices
        },
        "destination_values": destination_values or {},
        "destination_allocation": 41,
        "destination_address": 4096,
        "destination_provenance": 141,
        "destination_borrow": 241,
        "destination_allocation_base": 4096,
        "destination_allocation_bytes": 256,
        "source_allocation": 42,
        "source_address": 8192,
        "source_provenance": 142,
        "source_allocation_base": 8192,
        "source_allocation_bytes": 256,
        "element_size": 4,
        "element_alignment": 4,
        "isize_max": 2_147_483_647,
        "address_space_limit": 4_294_967_295,
        "frame_token": 777,
    }


PROBE_CASES: dict[str, dict[str, Any]] = {
    "valid_empty": {
        **_base_case(destination_length=0),
        "kind": "valid",
        "expected": "sat",
    },
    "valid_wholly_uninitialized": {
        **_base_case(
            destination_length=3,
            source_values={0: 11, 1: 22, 2: 33},
            destination_values={0: 901, 1: 902, 2: 903},
        ),
        "kind": "valid",
        "expected": "sat",
    },
    "valid_mixed_initialization": {
        **_base_case(
            destination_length=4,
            source_values={0: 14, 1: 28, 2: 42, 3: 56},
            initialized_indices=(0, 2),
            destination_values={0: 91, 1: 999, 2: 93, 3: 998},
        ),
        "kind": "valid",
        "expected": "sat",
    },
    "valid_fully_initialized": {
        **_base_case(
            destination_length=2,
            source_values={0: 7, 1: 8},
            initialized_indices=(0, 1),
            destination_values={0: 70, 1: 80},
        ),
        "kind": "valid",
        "expected": "sat",
    },
    "invalid_unequal_lengths": {
        **_base_case(
            destination_length=3,
            source_length=2,
            source_values={0: 1, 1: 2},
        ),
        "kind": "unequal_lengths",
        "expected": "unsat",
    },
    "invalid_partial_copy": {
        **_base_case(
            destination_length=3,
            source_values={0: 3, 1: 6, 2: 9},
        ),
        "kind": "wrong_destination_value",
        "index": 2,
        "wrong_value": 0,
        "expected": "unsat",
    },
    "invalid_no_op_copy": {
        **_base_case(
            destination_length=2,
            source_values={0: 31, 1: 37},
            initialized_indices=(0, 1),
            destination_values={0: 101, 1: 103},
        ),
        "kind": "no_op_copy",
        "expected": "unsat",
    },
    "invalid_omitted_initialization": {
        **_base_case(
            destination_length=2,
            source_values={0: 5, 1: 10},
        ),
        "kind": "uninitialized_final_slot",
        "index": 1,
        "expected": "unsat",
    },
    "invalid_wrong_return_identity": {
        **_base_case(
            destination_length=1,
            source_values={0: 12},
        ),
        "kind": "wrong_return_identity",
        "expected": "unsat",
    },
    "invalid_wrong_destination_identity": {
        **_base_case(
            destination_length=1,
            source_values={0: 13},
        ),
        "kind": "wrong_destination_identity",
        "expected": "unsat",
    },
    "invalid_changed_source": {
        **_base_case(
            destination_length=2,
            source_values={0: 17, 1: 19},
        ),
        "kind": "changed_source",
        "index": 1,
        "wrong_value": 20,
        "expected": "unsat",
    },
    "invalid_changed_frame": {
        **_base_case(
            destination_length=1,
            source_values={0: 23},
        ),
        "kind": "changed_frame",
        "expected": "unsat",
    },
}

PROBE_EXPECTED_RESULTS = {
    name: str(case["expected"]) for name, case in PROBE_CASES.items()
}


def _input_expression(case: dict[str, Any]) -> str:
    destination_storage = _cell_array_expr(
        case["destination_initialized"],
        case["destination_values"],
    )
    source_values = _array_expr("Int", 0, case["source_values"])
    values = (
        case["destination_length"],
        case["source_length"],
        destination_storage,
        source_values,
        case["destination_allocation"],
        case["destination_address"],
        case["destination_provenance"],
        case["destination_borrow"],
        case["destination_allocation_base"],
        case["destination_allocation_bytes"],
        case["source_allocation"],
        case["source_address"],
        case["source_provenance"],
        case["source_allocation_base"],
        case["source_allocation_bytes"],
        case["element_size"],
        case["element_alignment"],
        case["isize_max"],
        case["address_space_limit"],
        case["frame_token"],
    )
    return "(mkInput " + " ".join(map(str, values)) + ")"


def _boundary_expression(case: dict[str, Any]) -> str:
    destination_storage = _cell_array_expr(
        case["destination_initialized"],
        case["destination_values"],
    )
    source_values = _array_expr("Int", 0, case["source_values"])
    values = (
        case["destination_length"],
        case["source_length"],
        destination_storage,
        source_values,
        case["destination_allocation"],
        case["destination_address"],
        case["destination_provenance"],
        case["destination_borrow"],
        case["destination_allocation_base"],
        case["destination_allocation_bytes"],
        case["source_allocation"],
        case["source_address"],
        case["source_provenance"],
        case["source_allocation_base"],
        case["source_allocation_bytes"],
        case["element_size"],
        case["element_alignment"],
        case["isize_max"],
        case["address_space_limit"],
        case["frame_token"],
    )
    return "(mkBoundary " + " ".join(map(str, values)) + ")"


def probe_text(name: str) -> str:
    try:
        case = PROBE_CASES[name]
    except KeyError as exc:
        raise ValueError(f"unknown target-120 probe: {name}") from exc
    assertions = [
        f"(= x {_input_expression(case)})",
        f"(= b {_boundary_expression(case)})",
        "(Requires_T x)",
        "(Boundary_T x b)",
        "(Spec_T x b y1 s1)",
    ]
    kind = case["kind"]
    if kind == "valid":
        assertions.extend(
            [
                (
                    "(= (y_return_allocation y1) "
                    f"{case['destination_allocation']})"
                ),
                f"(= (y_return_address y1) {case['destination_address']})",
                (
                    "(= (y_return_provenance y1) "
                    f"{case['destination_provenance']})"
                ),
                f"(= (y_return_borrow y1) {case['destination_borrow']})",
                f"(= (y_return_length y1) {case['source_length']})",
                f"(= (s_frame_token s1) {case['frame_token']})",
            ]
        )
        for index, value in sorted(case["source_values"].items()):
            assertions.extend(
                [
                    (
                        f"(= (select (s_destination_storage s1) {index}) "
                        f"(Initialized {value}))"
                    ),
                    f"(= (select (y_return_values y1) {index}) {value})",
                    f"(= (select (s_source_values s1) {index}) {value})",
                ]
            )
    elif kind == "wrong_destination_value":
        assertions.append(
            "(= (select (s_destination_storage s1) "
            f"{case['index']}) (Initialized {case['wrong_value']}))"
        )
    elif kind == "no_op_copy":
        assertions.append(
            "(= (s_destination_storage s1) (x_destination_storage x))"
        )
    elif kind == "uninitialized_final_slot":
        assertions.append(
            f"(= (select (s_destination_storage s1) {case['index']}) "
            "Uninitialized)"
        )
    elif kind == "wrong_return_identity":
        assertions.append(
            f"(= (y_return_allocation y1) {case['source_allocation']})"
        )
    elif kind == "wrong_destination_identity":
        assertions.append(
            "(= (s_destination_allocation s1) "
            f"{case['source_allocation']})"
        )
    elif kind == "changed_source":
        assertions.append(
            "(= (select (s_source_values s1) "
            f"{case['index']}) {case['wrong_value']})"
        )
    elif kind == "changed_frame":
        assertions.append(
            f"(= (s_frame_token s1) {case['frame_token'] + 1})"
        )
    elif kind != "unequal_lengths":
        raise ValueError(f"unknown target-120 probe kind: {kind}")
    body = "\n       ".join(assertions)
    return _model_text(PRIMARY) + f"""\
(assert
  (and {body}))
(check-sat)
"""


def boundary_manifest() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "target": TARGET,
        "input_order": INPUT_ORDER,
        "active_contract_sha256": ACTIVE_CONTRACT_SHA256,
        "boundary_narrower_than_target": True,
        "shared_boundary_observations": [
            {
                "fields": [
                    "b_source_length",
                    "b_source_values",
                    "b_source_allocation",
                    "b_source_address",
                    "b_source_provenance",
                    "b_source_allocation_base",
                    "b_source_allocation_bytes",
                ],
                "kind": "initial initialized source slice and memory identity",
                "trust_site_ids": [
                    "TS-120-D002",
                    "TS-120-E001",
                    "TS-120-E002",
                    "TS-120-E004",
                ],
            },
            {
                "fields": [
                    "b_destination_length",
                    "b_destination_storage",
                ],
                "kind": (
                    "initial destination cells: Uninitialized carries no value; "
                    "Initialized carries exactly one old value"
                ),
                "trust_site_ids": ["TS-120-E003", "TS-120-E004"],
            },
            {
                "fields": [
                    "b_destination_allocation",
                    "b_destination_address",
                    "b_destination_provenance",
                    "b_destination_borrow",
                    "b_destination_allocation_base",
                    "b_destination_allocation_bytes",
                ],
                "kind": "initial destination memory and mutable-borrow identity",
                "trust_site_ids": [
                    "TS-120-E003",
                    "TS-120-E004",
                    "TS-120-E006",
                ],
            },
            {
                "fields": [
                    "b_element_size",
                    "b_element_alignment",
                    "b_isize_max",
                    "b_address_space_limit",
                ],
                "kind": "pointee layout and target-platform memory limits",
                "trust_site_ids": [
                    "TS-120-D002",
                    "TS-120-E004",
                ],
            },
            {
                "fields": ["b_frame_token"],
                "kind": "pre-existing memory outside source and destination",
                "trust_site_ids": ["TS-120-E004"],
            },
        ],
        "deterministic_source_transitions": [
            {
                "operation": "transmute::<&[T], &[MaybeUninit<T>]>",
                "semantics": (
                    "preserves slice length, allocation, address, provenance, "
                    "layout, and each initialized source value"
                ),
                "source_citations": [
                    TARGET_SOURCE_REFERENCE,
                    TRANSMUTE_REFERENCE,
                ],
            },
            {
                "operation": "copy_from_slice equal-length branch",
                "semantics": (
                    "admits only equal lengths and calls copy_nonoverlapping "
                    "for exactly destination.len() elements"
                ),
                "source_citations": [
                    TARGET_SOURCE_REFERENCE,
                    COPY_FROM_SLICE_REFERENCE,
                ],
            },
            {
                "operation": "copy_nonoverlapping",
                "semantics": (
                    "for every slot in [0,len), copies the transmuted source "
                    "value and initialization state to the destination; no old "
                    "destination value is read, and source and outside frame "
                    "are preserved"
                ),
                "source_citations": [
                    COPY_FROM_SLICE_REFERENCE,
                    COPY_NONOVERLAPPING_REFERENCE,
                ],
            },
            {
                "operation": "assume_init_mut",
                "semantics": (
                    "after all destination slots are initialized, returns a "
                    "mutable [T] view with the destination allocation, address, "
                    "provenance, borrow identity, length, and copied values"
                ),
                "source_citations": [
                    TARGET_SOURCE_REFERENCE,
                    ASSUME_INIT_MUT_REFERENCE,
                ],
            },
        ],
        "excluded_retained_sites": [
            {
                "trust_site_id": "TS-120-D004",
                "reason": (
                    "The mixed dependency record includes the answer-equivalent "
                    "aggregate storage-effect bridge; only its separately "
                    "audited pointer/copy primitives are retained."
                ),
            },
            {
                "trust_site_id": "TS-120-E005",
                "reason": (
                    "The external proof lemma supplies the complete copied "
                    "storage result. It is replaced, not renamed or reused, by "
                    "the explicit per-slot copy transition."
                ),
            },
        ],
        "context_only_trust_sites": ["TS-120-D001", "TS-120-C001"],
        "admitted_boundary_trust_site_ids": list(ADMITTED_TRUST_SITES),
        "all_audited_trust_site_ids": list(ALL_AUDITED_TRUST_SITES),
        "excluded_from_boundary": [
            "resulting destination storage or initialization",
            "returned reference identity or values",
            "aggregate final state",
            "answer encodings",
            "no-op, partial-copy, or selected-slot traces",
            "complete execution traces",
        ],
        "uninitialized_value_policy": (
            "An Uninitialized cell has no value field, so neither Boundary_T "
            "nor the source transition can read an uninitialized value."
        ),
    }
