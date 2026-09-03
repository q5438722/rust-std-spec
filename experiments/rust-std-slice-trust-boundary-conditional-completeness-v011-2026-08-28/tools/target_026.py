#!/usr/bin/env python3
"""Source-backed conditional-completeness model for assume_init_mut."""

from __future__ import annotations

from typing import Any

from checker_guards import GuardError, parse_smt, validate_obligation


TARGET = "core::slice::assume_init_mut"
INPUT_ORDER = "26"
ARTIFACT_ID = "026_core_slice_assume_init_mut"
ACTIVE_CONTRACT_SHA256 = (
    "8d0e90b87ee12383ef38b353ff71f43a4136f565d0ae0f63651ee295c06f649a"
)
ACTIVE_CONTRACT_TEXT = (
    "pub assume_specification<T>[ <[core::mem::MaybeUninit<T>]>::"
    "assume_init_mut ]( slice: &mut [core::mem::MaybeUninit<T>], ) -> "
    "(ret: &mut [T]) requires maybe_uninit_all_initialized("
    "maybe_uninit_seq_relation(old(slice)@)), ensures "
    "maybe_uninit_relation_well_formed( maybe_uninit_seq_relation("
    "old(slice)@), old(slice)@.len() as int, ), "
    "maybe_uninit_relation_well_formed( maybe_uninit_seq_relation("
    "final(slice)@), final(slice)@.len() as int, ), final(slice)@.len() "
    "== old(slice)@.len(), ret@ == maybe_uninit_seq_relation("
    "old(slice)@).values, ret@.len() == old(slice)@.len(), "
    "final(ret)@.len() == final(slice)@.len(), "
    "maybe_uninit_all_initialized(maybe_uninit_seq_relation("
    "final(slice)@)), maybe_uninit_seq_relation(final(slice)@).values "
    "== final(ret)@, ;"
)

PRIMARY = "completeness-modulo-reviewed-equivalence"
EXACT_OUTPUT = "exact-output-determinism"
PURPOSES = (PRIMARY, EXACT_OUTPUT)

TARGET_SOURCE_REFERENCE = "core/src/mem/maybe_uninit.rs:1516-1531"
LAYOUT_REFERENCE = "core/src/mem/maybe_uninit.rs:1512-1531"
REPLACEMENT_ID = "RB-026-LAYOUT-PRESERVING-MUTABLE-SLICE-CAST"
EXCLUDED_RETAINED_TRUST_SITES = ("TS-026-D002", "TS-026-E001")
CONTEXT_ONLY_TRUST_SITES = ("TS-026-D001",)
ALL_AUDITED_TRUST_SITES = (
    "TS-026-D001",
    "TS-026-D002",
    "TS-026-E001",
)

ACTIVE_CONJUNCT_SYMBOLS = (
    "ActiveInitialAllInitializedConjunct",
    "ActiveInitialRelationWellFormedConjunct",
    "ActiveFinalRelationWellFormedConjunct",
    "ActiveFinalSliceLengthConjunct",
    "ActiveReturnValuesConjunct",
    "ActiveReturnLengthConjunct",
    "ActiveFinalReturnLengthConjunct",
    "ActiveFinalAllInitializedConjunct",
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
    ("s_slice_length", "Int"),
    ("s_relation_initialized_length", "Int"),
    ("s_relation_values_length", "Int"),
    ("s_storage", "Array Int Cell"),
    ("s_destination_allocation", "Int"),
    ("s_destination_address", "Int"),
    ("s_destination_provenance", "Int"),
    ("s_destination_borrow", "Int"),
    ("s_destination_allocation_base", "Int"),
    ("s_destination_allocation_bytes", "Int"),
    ("s_return_allocation", "Int"),
    ("s_return_address", "Int"),
    ("s_return_provenance", "Int"),
    ("s_return_borrow", "Int"),
    ("s_return_length", "Int"),
    ("s_return_values", "Array Int Int"),
    ("s_element_size", "Int"),
    ("s_element_alignment", "Int"),
    ("s_isize_max", "Int"),
    ("s_address_space_limit", "Int"),
    ("s_frame_token", "Int"),
)

OUTPUT_SOURCE_TRANSITIONS = (
    "AssumeInitMutReturnAllocation",
    "AssumeInitMutReturnAddress",
    "AssumeInitMutReturnProvenance",
    "AssumeInitMutReturnBorrow",
    "AssumeInitMutReturnLength",
    "AssumeInitMutReturnValues",
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


def _state_contract(purpose: str) -> str:
    if purpose == EXACT_OUTPUT:
        return "       (FinalContractExists x y)"
    return """\
       (= (s_slice_length s) (x_slice_length x))
       (= (s_relation_initialized_length s) (x_slice_length x))
       (= (s_relation_values_length s) (x_slice_length x))
       (= (s_destination_allocation s) (x_destination_allocation x))
       (= (s_destination_address s) (x_destination_address x))
       (= (s_destination_provenance s) (x_destination_provenance x))
       (= (s_destination_borrow s) (x_destination_borrow x))
       (= (s_destination_allocation_base s)
          (x_destination_allocation_base x))
       (= (s_destination_allocation_bytes s)
          (x_destination_allocation_bytes x))
       (= (s_return_allocation s) (x_destination_allocation x))
       (= (s_return_address s) (x_destination_address x))
       (= (s_return_provenance s) (x_destination_provenance x))
       (= (s_return_borrow s) (x_destination_borrow x))
       (= (s_return_length s) (x_slice_length x))
       (= (s_element_size s) (x_element_size x))
       (= (s_element_alignment s) (x_element_alignment x))
       (= (s_isize_max s) (x_isize_max x))
       (= (s_address_space_limit s) (x_address_space_limit x))
       (= (s_frame_token s) (x_frame_token x))
       (ActiveInitialRelationWellFormedConjunct x)
       (ActiveFinalRelationWellFormedConjunct
         (s_slice_length s)
         (s_relation_initialized_length s)
         (s_relation_values_length s))
       (ActiveFinalSliceLengthConjunct x (s_slice_length s))
       (ActiveFinalReturnLengthConjunct
         (s_slice_length s) (s_return_length s))
       (ActiveFinalAllInitializedConjunct
         (s_slice_length s) (s_storage s) (s_return_values s))
       (ActiveFinalStorageEqualsReturnConjunct
         (s_slice_length s) (s_storage s) (s_return_values s))"""


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
        raise ValueError(f"unknown target-026 obligation purpose: {purpose}")
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
; The raw cast preserves layout and mutable-borrow identity. In-range final
; values remain free because the active contract exposes a returned &mut [T].
(set-logic ALL)
(declare-datatypes ((Cell 0))
  (((Uninitialized)
    (Initialized (initialized_value Int)))))
(declare-datatypes ((Input 0))
  (((mkInput
      (x_slice_length Int)
      (x_relation_initialized_length Int)
      (x_relation_values_length Int)
      (x_storage (Array Int Cell))
      (x_values (Array Int Int))
      (x_destination_allocation Int)
      (x_destination_address Int)
      (x_destination_provenance Int)
      (x_destination_borrow Int)
      (x_destination_allocation_base Int)
      (x_destination_allocation_bytes Int)
      (x_element_size Int)
      (x_element_alignment Int)
      (x_isize_max Int)
      (x_address_space_limit Int)
      (x_frame_token Int)))))
(declare-datatypes ((Boundary 0))
  (((mkBoundary
      (b_slice_length Int)
      (b_relation_initialized_length Int)
      (b_relation_values_length Int)
      (b_storage (Array Int Cell))
      (b_values (Array Int Int))
      (b_destination_allocation Int)
      (b_destination_address Int)
      (b_destination_provenance Int)
      (b_destination_borrow Int)
      (b_destination_allocation_base Int)
      (b_destination_allocation_bytes Int)
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
(define-fun ByteCount ((x Input)) Int
  (* (x_slice_length x) (x_element_size x)))
(define-fun AllInitialized
  ((storage (Array Int Cell)) (values (Array Int Int))) Bool
  (= storage ((_ map Initialized) values)))
(define-fun BoundaryInputsObserved ((x Input) (b Boundary)) Bool
  (and (= (b_slice_length b) (x_slice_length x))
       (= (b_relation_initialized_length b)
          (x_relation_initialized_length x))
       (= (b_relation_values_length b) (x_relation_values_length x))
       (= (b_storage b) (x_storage x))
       (= (b_values b) (x_values x))
       (= (b_destination_allocation b) (x_destination_allocation x))
       (= (b_destination_address b) (x_destination_address x))
       (= (b_destination_provenance b) (x_destination_provenance x))
       (= (b_destination_borrow b) (x_destination_borrow x))
       (= (b_destination_allocation_base b)
          (x_destination_allocation_base x))
       (= (b_destination_allocation_bytes b)
          (x_destination_allocation_bytes x))
       (= (b_element_size b) (x_element_size x))
       (= (b_element_alignment b) (x_element_alignment x))
       (= (b_isize_max b) (x_isize_max x))
       (= (b_address_space_limit b) (x_address_space_limit x))
       (= (b_frame_token b) (x_frame_token x))))
(define-fun ValidMutableSliceMemory ((x Input)) Bool
  (and (> (x_destination_address x) 0)
       (> (x_destination_borrow x) 0)
       (>= (x_destination_allocation x) 0)
       (>= (x_destination_provenance x) 0)
       (>= (x_destination_allocation_base x) 0)
       (>= (x_destination_allocation_bytes x) 0)
       (>= (x_element_size x) 0)
       (> (x_element_alignment x) 0)
       (> (x_isize_max x) 0)
       (> (x_address_space_limit x) 0)
       (= (mod (x_destination_address x) (x_element_alignment x)) 0)
       (or (= (x_element_size x) 0)
           (and (>= (x_element_size x) (x_element_alignment x))
                (= (mod (x_element_size x) (x_element_alignment x)) 0)))
       (<= (ByteCount x) (x_isize_max x))
       (<= (+ (x_destination_address x) (ByteCount x))
           (x_address_space_limit x))
       (or (= (ByteCount x) 0)
           (and (> (x_destination_allocation x) 0)
                (> (x_destination_provenance x) 0)
                (<= (x_destination_allocation_base x)
                    (x_destination_address x))
                (<= (+ (x_destination_address x) (ByteCount x))
                    (+ (x_destination_allocation_base x)
                       (x_destination_allocation_bytes x)))))))
(define-fun AssumeInitMutReturnAllocation ((x Input)) Int
  (x_destination_allocation x))
(define-fun AssumeInitMutReturnAddress ((x Input)) Int
  (x_destination_address x))
(define-fun AssumeInitMutReturnProvenance ((x Input)) Int
  (x_destination_provenance x))
(define-fun AssumeInitMutReturnBorrow ((x Input)) Int
  (x_destination_borrow x))
(define-fun AssumeInitMutReturnLength ((x Input)) Int
  (x_slice_length x))
(define-fun AssumeInitMutReturnValues ((x Input)) (Array Int Int)
  (x_values x))
(define-fun ActiveInitialAllInitializedConjunct ((x Input)) Bool
  (AllInitialized (x_storage x) (x_values x)))
(define-fun ActiveInitialRelationWellFormedConjunct ((x Input)) Bool
  (and (>= (x_slice_length x) 0)
       (= (x_relation_initialized_length x) (x_slice_length x))
       (= (x_relation_values_length x) (x_slice_length x))))
(define-fun ActiveFinalRelationWellFormedConjunct
  ((slice_length Int)
   (initialized_length Int)
   (values_length Int)) Bool
  (and (>= slice_length 0)
       (= initialized_length slice_length)
       (= values_length slice_length)))
(define-fun ActiveFinalSliceLengthConjunct
  ((x Input) (final_length Int)) Bool
  (= final_length (x_slice_length x)))
(define-fun ActiveReturnValuesConjunct
  ((x Input) (y Output)) Bool
  (= (y_return_values y) (x_values x)))
(define-fun ActiveReturnLengthConjunct ((x Input) (y Output)) Bool
  (= (y_return_length y) (x_slice_length x)))
(define-fun ActiveFinalReturnLengthConjunct
  ((final_slice_length Int) (final_return_length Int)) Bool
  (= final_return_length final_slice_length))
(define-fun ActiveFinalAllInitializedConjunct
  ((final_length Int)
   (final_storage (Array Int Cell))
   (final_values (Array Int Int))) Bool
  (and (>= final_length 0)
       (AllInitialized final_storage final_values)))
(define-fun ActiveFinalStorageEqualsReturnConjunct
  ((final_length Int)
   (final_storage (Array Int Cell))
   (final_return_values (Array Int Int))) Bool
  (and (>= final_length 0)
       (= final_storage ((_ map Initialized) final_return_values))))
(define-fun FinalContractExists ((x Input) (y Output)) Bool
  (exists ((final_storage (Array Int Cell))
           (final_return_values (Array Int Int)))
    (and (ActiveFinalRelationWellFormedConjunct
           (x_slice_length x) (x_slice_length x) (x_slice_length x))
         (ActiveFinalSliceLengthConjunct x (x_slice_length x))
         (ActiveFinalReturnLengthConjunct
           (x_slice_length x) (x_slice_length x))
         (ActiveFinalAllInitializedConjunct
           (x_slice_length x) final_storage final_return_values)
         (ActiveFinalStorageEqualsReturnConjunct
           (x_slice_length x) final_storage final_return_values)
         (= (y_return_length y) (x_slice_length x)))))
(define-fun Requires_T ((x Input)) Bool
  (and (ActiveInitialRelationWellFormedConjunct x)
       (ActiveInitialAllInitializedConjunct x)
       (ValidMutableSliceMemory x)))
(define-fun Boundary_T ((x Input) (b Boundary)) Bool
  (and (BoundaryInputsObserved x b)
       (>= (b_slice_length b) 0)
       (> (b_destination_address b) 0)
       (> (b_destination_borrow b) 0)
       (> (b_element_alignment b) 0)
       (> (b_isize_max b) 0)
       (> (b_address_space_limit b) 0)))
(define-fun TargetDefinition_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and (BoundaryInputsObserved x b)
{output_equalities}
       (ActiveInitialAllInitializedConjunct x)
       (ActiveReturnValuesConjunct x y)
       (ActiveReturnLengthConjunct x y)
{_state_contract(purpose)}))
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
    result = [
        {
            "selector": selector,
            "left": "output1",
            "right": "output2",
            "sort": sort,
        }
        for selector, sort in OUTPUT_FIELDS
    ]
    if purpose == PRIMARY:
        result.extend(
            {
                "selector": selector,
                "left": "state1",
                "right": "state2",
                "sort": sort,
            }
            for selector, sort in STATE_FIELDS
        )
    return result


def _boundary_fields() -> list[dict[str, Any]]:
    roles = {
        "b_slice_length": "input_initialization",
        "b_relation_initialized_length": "input_initialization",
        "b_relation_values_length": "input_initialization",
        "b_storage": "input_initialization",
        "b_values": "input_initialization",
        "b_destination_allocation": "input_memory",
        "b_destination_address": "input_memory",
        "b_destination_provenance": "input_provenance",
        "b_destination_borrow": "input_provenance",
        "b_destination_allocation_base": "input_memory",
        "b_destination_allocation_bytes": "input_memory",
        "b_element_size": "input_layout",
        "b_element_alignment": "input_layout",
        "b_isize_max": "input_layout",
        "b_address_space_limit": "input_layout",
        "b_frame_token": "input_memory",
    }
    return [
        {
            "selector": selector,
            "role": role,
            "source_citations": [TARGET_SOURCE_REFERENCE, LAYOUT_REFERENCE],
            "trust_site_ids": [],
            "source_backed_replacement_ids": [REPLACEMENT_ID],
        }
        for selector, role in roles.items()
    ]


def obligation_metadata(purpose: str) -> dict[str, Any]:
    if purpose not in PURPOSES:
        raise ValueError(f"unknown target-026 obligation purpose: {purpose}")
    return {
        "schema_version": 3,
        "target": TARGET,
        "input_order": INPUT_ORDER,
        "obligation_purpose": purpose,
        "active_contract_sha256": ACTIVE_CONTRACT_SHA256,
        "active_contract_text": ACTIVE_CONTRACT_TEXT,
        "domain": {
            "length": "arbitrary nonnegative slice length, including empty",
            "initialization": "every in-range MaybeUninit slot is initialized",
            "memory": (
                "nonnull aligned mutable slice with valid provenance for every "
                "nonzero byte range; dangling empty and ZST slices remain valid"
            ),
            "mutable_final_state": (
                "in-range final values may differ after use of the returned "
                "mutable reference; outside storage and identity are framed"
            ),
        },
        "contract_translation": {
            "active_conjuncts": list(ACTIVE_CONJUNCT_SYMBOLS),
            "source_flow": [
                "layout-preserving *mut [MaybeUninit<T>] to *mut [T] cast",
                "reborrow as the same unique mutable slice",
                "initial returned values project only initialized input slots",
                "final returned view aliases final MaybeUninit storage",
            ],
            "final_state_projection": (
                "explicit exact theorem state"
                if purpose == PRIMARY
                else "existentially retained while comparing exact return only"
            ),
        },
        "boundary_scope": {
            "shared_observations": [
                "initial initialized storage and relation lengths",
                "initial allocation, address, provenance, and mutable-borrow identity",
                "element layout and platform pointer limits",
                "pre-existing outside-frame token",
            ],
            "excluded_observations": [
                "returned reference",
                "resulting storage",
                "final returned values",
                "aggregate final state",
                "answer encoding",
                "complete execution trace",
            ],
            "admitted_trust_site_ids": [],
            "excluded_retained_trust_site_ids": list(
                EXCLUDED_RETAINED_TRUST_SITES
            ),
            "context_only_trust_site_ids": list(CONTEXT_ONLY_TRUST_SITES),
            "all_audited_trust_site_ids": list(ALL_AUDITED_TRUST_SITES),
            "source_backed_replacement_ids": [REPLACEMENT_ID],
            "narrower_than_target": True,
        },
        "source_backed_replacements": [
            {
                "replacement_id": REPLACEMENT_ID,
                "replaces_trust_site_ids": list(
                    EXCLUDED_RETAINED_TRUST_SITES
                ),
                "symbols": list(OUTPUT_SOURCE_TRANSITIONS),
                "source_citations": [
                    TARGET_SOURCE_REFERENCE,
                    LAYOUT_REFERENCE,
                ],
                "semantics": (
                    "preserve allocation, address, provenance, length, layout, "
                    "and unique borrow while projecting initialized input values"
                ),
            }
        ],
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
        "source_transition_definitions": list(OUTPUT_SOURCE_TRANSITIONS),
        "source_transition_bindings": {
            "layout_preserving_mutable_slice_cast": {
                "symbols": list(OUTPUT_SOURCE_TRANSITIONS),
                "replacement_id": REPLACEMENT_ID,
                "source_citations": [
                    TARGET_SOURCE_REFERENCE,
                    LAYOUT_REFERENCE,
                ],
            },
            "mutable_alias_final_frame": {
                "symbols": [
                    "AllInitialized",
                    "ActiveFinalStorageEqualsReturnConjunct",
                ],
                "source_citations": [TARGET_SOURCE_REFERENCE],
            },
        },
        "equivalence_kind": "exact",
        "equivalence_scope": (
            "returned reference identity and values plus every final storage, "
            "identity, layout, and frame observation"
            if purpose == PRIMARY
            else "returned reference identity, length, and initial values"
        ),
        "principal_observations": _principal_observations(purpose),
    }


def obligation(purpose: str) -> tuple[str, dict[str, Any]]:
    return obligation_text(purpose), obligation_metadata(purpose)


def validate_target_obligation(text: str, metadata: dict[str, Any]) -> None:
    validate_obligation(text, metadata)
    purpose = metadata.get("obligation_purpose")
    if purpose not in PURPOSES:
        raise GuardError("target-026 obligation has an unknown purpose")
    expected_text, expected_metadata = obligation(str(purpose))
    if metadata != expected_metadata:
        raise GuardError(
            "target-026 metadata differs from the reviewed cast translation"
        )
    if parse_smt(text) != parse_smt(expected_text):
        raise GuardError(
            "target-026 SMT differs from the reviewed cast translation"
        )


def _cell_array(
    values: dict[int, int],
    uninitialized: tuple[int, ...] = (),
) -> str:
    expression = "((as const (Array Int Cell)) (Initialized 0))"
    for index, value in sorted(values.items()):
        expression = (
            f"(store {expression} {index} (Initialized {value}))"
        )
    for index in uninitialized:
        expression = f"(store {expression} {index} Uninitialized)"
    return expression


def _int_array(values: dict[int, int]) -> str:
    expression = "((as const (Array Int Int)) 0)"
    for index, value in sorted(values.items()):
        expression = f"(store {expression} {index} {value})"
    return expression


def _case(
    *,
    length: int = 2,
    initialized: dict[int, int] | None = None,
    uninitialized: tuple[int, ...] = (),
) -> dict[str, Any]:
    return {
        "length": length,
        "relation_initialized_length": length,
        "relation_values_length": length,
        "initialized": (
            {0: 10, 1: 20} if initialized is None and length == 2
            else (initialized or {})
        ),
        "uninitialized": uninitialized,
        "allocation": 41,
        "address": 4096,
        "provenance": 141,
        "borrow": 241,
        "allocation_base": 4096,
        "allocation_bytes": 64,
        "element_size": 4,
        "element_alignment": 4,
        "isize_max": 2_147_483_647,
        "address_space_limit": 4_294_967_295,
        "frame_token": 777,
    }


PROBE_CASES: dict[str, dict[str, Any]] = {
    "valid_empty": {
        **_case(length=0),
        "kind": "valid",
        "expected": "sat",
    },
    "valid_initialized_nonempty": {
        **_case(),
        "kind": "valid",
        "expected": "sat",
    },
    "valid_zst_nonempty": {
        **_case(),
        "element_size": 0,
        "allocation": 0,
        "provenance": 0,
        "kind": "valid",
        "expected": "sat",
    },
    "valid_mutated_final_view": {
        **_case(),
        "kind": "mutated_final_view",
        "final_values": {0: 101, 1: 202},
        "expected": "sat",
    },
    "invalid_initialization_mask": {
        **_case(initialized={0: 10}, uninitialized=(1,)),
        "kind": "invalid_domain",
        "expected": "unsat",
    },
    "invalid_null_pointer": {
        **_case(),
        "address": 0,
        "kind": "invalid_domain",
        "expected": "unsat",
    },
    "invalid_missing_provenance": {
        **_case(),
        "provenance": 0,
        "kind": "invalid_domain",
        "expected": "unsat",
    },
    "invalid_misaligned_pointer": {
        **_case(),
        "address": 4098,
        "kind": "invalid_domain",
        "expected": "unsat",
    },
    "invalid_layout": {
        **_case(),
        "element_size": 6,
        "kind": "invalid_domain",
        "expected": "unsat",
    },
    "invalid_wrong_return_identity": {
        **_case(),
        "kind": "wrong_return_identity",
        "expected": "unsat",
    },
    "invalid_wrong_return_borrow": {
        **_case(),
        "kind": "wrong_return_borrow",
        "expected": "unsat",
    },
    "invalid_final_uninitialized": {
        **_case(),
        "kind": "final_uninitialized",
        "expected": "unsat",
    },
    "invalid_frame_token_mutation": {
        **_case(),
        "kind": "frame_token_mutation",
        "expected": "unsat",
    },
}

PROBE_EXPECTED_RESULTS = {
    name: str(case["expected"]) for name, case in PROBE_CASES.items()
}


def _input_expression(case: dict[str, Any]) -> str:
    values = (
        case["length"],
        case["relation_initialized_length"],
        case["relation_values_length"],
        _cell_array(case["initialized"], case["uninitialized"]),
        _int_array(case["initialized"]),
        case["allocation"],
        case["address"],
        case["provenance"],
        case["borrow"],
        case["allocation_base"],
        case["allocation_bytes"],
        case["element_size"],
        case["element_alignment"],
        case["isize_max"],
        case["address_space_limit"],
        case["frame_token"],
    )
    return "(mkInput " + " ".join(map(str, values)) + ")"


def _boundary_expression(case: dict[str, Any]) -> str:
    values = (
        case["length"],
        case["relation_initialized_length"],
        case["relation_values_length"],
        _cell_array(case["initialized"], case["uninitialized"]),
        _int_array(case["initialized"]),
        case["allocation"],
        case["address"],
        case["provenance"],
        case["borrow"],
        case["allocation_base"],
        case["allocation_bytes"],
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
        raise ValueError(f"unknown target-026 probe: {name}") from exc
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
                f"(= (y_return_allocation y1) {case['allocation']})",
                f"(= (y_return_address y1) {case['address']})",
                f"(= (y_return_provenance y1) {case['provenance']})",
                f"(= (y_return_borrow y1) {case['borrow']})",
                f"(= (y_return_length y1) {case['length']})",
            ]
        )
    elif kind == "mutated_final_view":
        final_storage = _cell_array(case["final_values"])
        assertions.extend(
            [
                f"(= (s_storage s1) {final_storage})",
                (
                    f"(= (s_return_values s1) "
                    f"{_int_array(case['final_values'])})"
                ),
            ]
        )
    elif kind == "wrong_return_identity":
        assertions.append(
            f"(= (y_return_allocation y1) {case['allocation'] + 1})"
        )
    elif kind == "wrong_return_borrow":
        assertions.append(
            f"(= (y_return_borrow y1) {case['borrow'] + 1})"
        )
    elif kind == "final_uninitialized":
        assertions.append(
            "(= (select (s_storage s1) 0) Uninitialized)"
        )
    elif kind == "frame_token_mutation":
        assertions.append(
            f"(= (s_frame_token s1) {case['frame_token'] + 1})"
        )
    elif kind != "invalid_domain":
        raise ValueError(f"unknown target-026 probe kind: {kind}")
    body = "\n       ".join(assertions)
    return _model_text(PRIMARY) + f"""\
(assert
  (and {body}))
(check-sat)
"""


def witness_payload() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "target": TARGET,
        "input_order": INPUT_ORDER,
        "active_contract_sha256": ACTIVE_CONTRACT_SHA256,
        "input": {
            "slice": [
                {"initialized": True, "value": 10},
                {"initialized": True, "value": 20},
            ],
            "allocation": 41,
            "address": 4096,
            "provenance": 141,
            "borrow": 241,
            "element_size": 4,
            "element_alignment": 4,
            "frame_token": 777,
        },
        "boundary": {
            "initial_storage": [10, 20],
            "allocation": 41,
            "address": 4096,
            "provenance": 141,
            "borrow": 241,
            "element_size": 4,
            "element_alignment": 4,
            "frame_token": 777,
        },
        "execution1": {
            "return": {
                "values": [10, 20],
                "allocation": 41,
                "address": 4096,
                "provenance": 141,
                "borrow": 241,
            },
            "final_storage": [101, 202],
            "final_return_values": [101, 202],
        },
        "execution2": {
            "return": {
                "values": [10, 20],
                "allocation": 41,
                "address": 4096,
                "provenance": 141,
                "borrow": 241,
            },
            "final_storage": [303, 404],
            "final_return_values": [303, 404],
        },
        "expected": {
            "same_valid_input": True,
            "same_boundary": True,
            "execution1_satisfies_every_active_conjunct": True,
            "execution2_satisfies_every_active_conjunct": True,
            "exact_output_equal": True,
            "exact_final_state_equal": False,
            "full_exact_equivalent": False,
        },
    }


def fixed_model_text() -> str:
    text = obligation_text(PRIMARY)
    terminal = "(check-sat)\n"
    if not text.endswith(terminal):
        raise ValueError("target-026 obligation lacks terminal check-sat")
    case = _case()
    first = {0: 101, 1: 202}
    second = {0: 303, 1: 404}
    return (
        text[: -len(terminal)]
        + f"""\
(assert (= x {_input_expression(case)}))
(assert (= b {_boundary_expression(case)}))
(assert (= (s_storage s1) {_cell_array(first)}))
(assert (= (s_return_values s1) {_int_array(first)}))
(assert (= (s_storage s2) {_cell_array(second)}))
(assert (= (s_return_values s2) {_int_array(second)}))
(check-sat)
(get-value (
  (y_return_values y1)
  (y_return_values y2)
  (s_storage s1)
  (s_storage s2)
  (Equivalent_T x b y1 s1 y2 s2)))
"""
    )


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
                    "b_slice_length",
                    "b_relation_initialized_length",
                    "b_relation_values_length",
                    "b_storage",
                    "b_values",
                ],
                "kind": "initial initialized MaybeUninit storage only",
                "source_backed_replacement_ids": [REPLACEMENT_ID],
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
                "kind": "initial memory, provenance, and unique-borrow identity",
                "source_backed_replacement_ids": [REPLACEMENT_ID],
            },
            {
                "fields": [
                    "b_element_size",
                    "b_element_alignment",
                    "b_isize_max",
                    "b_address_space_limit",
                    "b_frame_token",
                ],
                "kind": "layout, platform limits, and pre-existing frame",
                "source_backed_replacement_ids": [REPLACEMENT_ID],
            },
        ],
        "source_backed_replacements": obligation_metadata(PRIMARY)[
            "source_backed_replacements"
        ],
        "admitted_retained_trust_site_ids": [],
        "excluded_retained_trust_site_ids": list(
            EXCLUDED_RETAINED_TRUST_SITES
        ),
        "context_only_trust_site_ids": list(CONTEXT_ONLY_TRUST_SITES),
        "all_audited_trust_site_ids": list(ALL_AUDITED_TRUST_SITES),
        "excluded_from_boundary": [
            "returned mutable reference",
            "resulting storage or final returned values",
            "final state or equivalent answer encoding",
            "selected or complete execution trace",
        ],
        "boundary_statement": (
            "The boundary fixes only the initialized input representation, "
            "layout/address/provenance, mutable-borrow identity, and outside "
            "frame. The source cast derives the returned reference. The active "
            "contract itself permits distinct in-range final values through "
            "that returned mutable borrow."
        ),
    }
