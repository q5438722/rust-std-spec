#!/usr/bin/env python3
"""Source-backed conditional-completeness model for assume_init_drop."""

from __future__ import annotations

from typing import Any

from checker_guards import GuardError, parse_smt, validate_obligation


TARGET = "core::slice::assume_init_drop"
INPUT_ORDER = "25"
ARTIFACT_ID = "025_core_slice_assume_init_drop"
ACTIVE_CONTRACT_SHA256 = (
    "ec9d059a1f66ae03009745a3d37edfc5306f2c23387856ea9aa3f52cfff09efe"
)
ACTIVE_CONTRACT_TEXT = (
    "pub assume_specification<T>[ <[core::mem::MaybeUninit<T>]>::"
    "assume_init_drop ]( slice: &mut [core::mem::MaybeUninit<T>], ) "
    "requires maybe_uninit_all_initialized(maybe_uninit_seq_relation("
    "old(slice)@)), ensures maybe_uninit_relation_well_formed( "
    "maybe_uninit_seq_relation(old(slice)@), old(slice)@.len() as int, ), "
    "maybe_uninit_relation_well_formed( maybe_uninit_seq_relation("
    "final(slice)@), final(slice)@.len() as int, ), final(slice)@.len() "
    "== old(slice)@.len(), maybe_uninit_drop_all( "
    "maybe_uninit_seq_relation(old(slice)@), maybe_uninit_seq_relation("
    "final(slice)@), ), ;"
)

PRIMARY = "completeness-modulo-reviewed-equivalence"
EXACT_OUTPUT = "exact-output-determinism"
PURPOSES = (PRIMARY, EXACT_OUTPUT)

TARGET_SOURCE_REFERENCE = "core/src/mem/maybe_uninit.rs:1467-1496"
DROP_IN_PLACE_REFERENCE = "core/src/ptr/mod.rs:716-819"
REPLACEMENT_ID = "RB-025-RAW-SLICE-DROP-GLUE-DESTRUCT-STEPS"
ADMITTED_TRUST_SITES = ("TS-025-D003",)
EXCLUDED_RETAINED_TRUST_SITES = ("TS-025-D002", "TS-025-E001")
CONTEXT_ONLY_TRUST_SITES = ("TS-025-D001",)
ALL_AUDITED_TRUST_SITES = (
    "TS-025-D001",
    "TS-025-D002",
    "TS-025-D003",
    "TS-025-E001",
)

ACTIVE_CONJUNCT_SYMBOLS = (
    "ActiveInitialAllInitializedConjunct",
    "ActiveInitialRelationWellFormedConjunct",
    "ActiveFinalRelationWellFormedConjunct",
    "ActiveFinalSliceLengthConjunct",
    "ActiveDropAllConjunct",
)

OUTPUT_FIELDS = (("y_return_unit", "Bool"),)
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
    ("s_destruct_state", "Int"),
    ("s_element_size", "Int"),
    ("s_element_alignment", "Int"),
    ("s_isize_max", "Int"),
    ("s_address_space_limit", "Int"),
    ("s_frame_token", "Int"),
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
        return "       (DropFinalContract x b)"
    return """\
       (= (s_slice_length s) (x_slice_length x))
       (= (s_relation_initialized_length s) (x_slice_length x))
       (= (s_relation_values_length s) (x_slice_length x))
       (= (s_storage s) (DropFinalStorage x b))
       (= (s_destination_allocation s) (RawSliceAllocation x))
       (= (s_destination_address s) (RawSliceAddress x))
       (= (s_destination_provenance s) (RawSliceProvenance x))
       (= (s_destination_borrow s) (RawSliceBorrow x))
       (= (s_destination_allocation_base s)
          (x_destination_allocation_base x))
       (= (s_destination_allocation_bytes s)
          (x_destination_allocation_bytes x))
       (= (s_destruct_state s) (DropFinalDestructState x b))
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
       (ActiveDropAllConjunct
         x
         (s_slice_length s)
         (s_relation_initialized_length s)
         (s_relation_values_length s)
         (s_storage s))"""


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


def _source_transitions(purpose: str) -> tuple[str, ...]:
    if purpose == EXACT_OUTPUT:
        return ("DropUnitReturn",)
    return ("DropUnitReturn", "DropFinalStorage", "DropFinalDestructState")


def _model_text(purpose: str) -> str:
    if purpose not in PURPOSES:
        raise ValueError(f"unknown target-025 obligation purpose: {purpose}")
    return f"""\
; Target: {TARGET}
; Active contract SHA-256: {ACTIVE_CONTRACT_SHA256}
; Purpose: {purpose}
; The source nonempty branch casts the same raw slice, invokes slice drop glue,
; and applies one Destruct transition per element in increasing slice order.
(set-logic ALL)
(declare-datatypes ((Cell 0))
  (((Uninitialized)
    (Initialized (initialized_value Int)))))
(declare-datatypes ((CallbackOutcome 0)) (((Completed) (Panicked))))
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
      (x_frame_token Int)
      (x_destruct_initial_state Int)))))
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
      (b_frame_token Int)
      (b_destruct_initial_state Int)
      (b_destruct_state_before (Array Int Int))
      (b_destruct_state_after (Array Int Int))
      (b_destruct_outcome (Array Int CallbackOutcome))))))
(declare-datatypes ((Output 0))
  (((mkOutput (y_return_unit Bool)))))
{_state_declaration(purpose)}
(declare-const x Input)
(declare-const b Boundary)
(declare-const y1 Output)
(declare-const s1 State)
(declare-const y2 Output)
(declare-const s2 State)
(define-fun ByteCount ((x Input)) Int
  (* (x_slice_length x) (x_element_size x)))
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
       (= (b_frame_token b) (x_frame_token x))
       (= (b_destruct_initial_state b) (x_destruct_initial_state x))))
(define-fun ValidDropMemory ((x Input)) Bool
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
(define-fun DropIndexAtStep ((x Input) (step Int)) Int step)
(define-fun DropOperationCount ((x Input)) Int (x_slice_length x))
(define-fun DropFinalStorage
  ((x Input) (b Boundary)) (Array Int Cell)
  ((as const (Array Int Cell)) Uninitialized))
(define-fun DropStorageAfterStep
  ((storage (Array Int Cell)) (index Int)) (Array Int Cell)
  (store storage index Uninitialized))
(define-fun-rec DropStorageAfterSteps
  ((x Input) (count Int)) (Array Int Cell)
  (ite (<= count 0)
       (x_storage x)
       (let ((step (- count 1)))
         (DropStorageAfterStep
           (DropStorageAfterSteps x step)
           (DropIndexAtStep x step)))))
(define-fun-rec DestructCompletedThrough
  ((x Input) (b Boundary) (count Int)) Bool
  (ite (<= count 0)
       true
       (let ((step (- count 1)))
         (let ((index (DropIndexAtStep x step)))
           (and
             (DestructCompletedThrough x b step)
             (= index step)
             (= (select (b_destruct_outcome b) index) Completed)
             (= (select (b_destruct_state_before b) index)
                (ite (= step 0)
                     (x_destruct_initial_state x)
                     (select
                       (b_destruct_state_after b)
                       (DropIndexAtStep x (- step 1)))))
             (= (select (DropFinalStorage x b) index)
                (select
                  (DropStorageAfterSteps x count)
                  index)))))))
(define-fun RawSliceAllocation ((x Input)) Int
  (x_destination_allocation x))
(define-fun RawSliceAddress ((x Input)) Int
  (x_destination_address x))
(define-fun RawSliceProvenance ((x Input)) Int
  (x_destination_provenance x))
(define-fun RawSliceBorrow ((x Input)) Int
  (x_destination_borrow x))
(define-fun DropUnitReturn ((x Input)) Bool
  (>= (x_slice_length x) 0))
(define-fun DropFinalDestructState ((x Input) (b Boundary)) Int
  (ite (= (DropOperationCount x) 0)
       (x_destruct_initial_state x)
       (select
         (b_destruct_state_after b)
         (DropIndexAtStep x (- (DropOperationCount x) 1)))))
(define-fun DropSourceExecution_T ((x Input) (b Boundary)) Bool
  (and (= (DropOperationCount x) (x_slice_length x))
       (DestructCompletedThrough x b (DropOperationCount x))))
(define-fun ActiveInitialAllInitializedConjunct ((x Input)) Bool
  (= (x_storage x) ((_ map Initialized) (x_values x))))
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
(define-fun ActiveDropAllConjunct
  ((x Input)
   (final_length Int)
   (final_initialized_length Int)
   (final_values_length Int)
   (final_storage (Array Int Cell))) Bool
  (and (ActiveInitialRelationWellFormedConjunct x)
       (ActiveFinalRelationWellFormedConjunct
         final_length final_initialized_length final_values_length)
       (ActiveInitialAllInitializedConjunct x)
       (= final_storage ((as const (Array Int Cell)) Uninitialized))))
(define-fun DropFinalContract ((x Input) (b Boundary)) Bool
  (and (DropSourceExecution_T x b)
       (ActiveInitialRelationWellFormedConjunct x)
       (ActiveFinalRelationWellFormedConjunct
         (x_slice_length x) (x_slice_length x) (x_slice_length x))
       (ActiveFinalSliceLengthConjunct x (x_slice_length x))
       (ActiveDropAllConjunct
         x
         (x_slice_length x)
         (x_slice_length x)
         (x_slice_length x)
         (DropFinalStorage x b))))
(define-fun Requires_T ((x Input)) Bool
  (and (ActiveInitialRelationWellFormedConjunct x)
       (ActiveInitialAllInitializedConjunct x)
       (ValidDropMemory x)))
(define-fun Boundary_T ((x Input) (b Boundary)) Bool
  (and (BoundaryInputsObserved x b)
       (>= (b_slice_length b) 0)
       (> (b_destination_address b) 0)
       (> (b_destination_borrow b) 0)
       (> (b_element_alignment b) 0)
       (> (b_isize_max b) 0)
       (> (b_address_space_limit b) 0)
       (DestructCompletedThrough x b (DropOperationCount x))))
(define-fun TargetDefinition_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and (BoundaryInputsObserved x b)
       (DropSourceExecution_T x b)
       (= (y_return_unit y) (DropUnitReturn x))
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
        "b_destruct_initial_state": "callback_argument",
        "b_destruct_state_before": "callback_state_transition",
        "b_destruct_state_after": "callback_state_transition",
        "b_destruct_outcome": "callback_panic",
    }
    result: list[dict[str, Any]] = []
    for selector, role in roles.items():
        trust_sites = ["TS-025-D003"] if selector == "b_slice_length" else []
        result.append(
            {
                "selector": selector,
                "role": role,
                "source_citations": [
                    TARGET_SOURCE_REFERENCE,
                    DROP_IN_PLACE_REFERENCE,
                ],
                "trust_site_ids": trust_sites,
                "source_backed_replacement_ids": [REPLACEMENT_ID],
            }
        )
    return result


def obligation_metadata(purpose: str) -> dict[str, Any]:
    if purpose not in PURPOSES:
        raise ValueError(f"unknown target-025 obligation purpose: {purpose}")
    source_transitions = _source_transitions(purpose)
    return {
        "schema_version": 3,
        "target": TARGET,
        "input_order": INPUT_ORDER,
        "obligation_purpose": purpose,
        "active_contract_sha256": ACTIVE_CONTRACT_SHA256,
        "active_contract_text": ACTIVE_CONTRACT_TEXT,
        "domain": {
            "length": "arbitrary nonnegative slice length, including empty",
            "initialization": "every in-range logical slot is initialized",
            "memory": (
                "nonnull aligned mutable slice with valid provenance for every "
                "nonzero byte range; dangling empty and ZST slices remain valid"
            ),
            "destruct": (
                "one nonpanicking Destruct observation per element, keyed by "
                "source index and chained in increasing slice order"
            ),
        },
        "contract_translation": {
            "active_conjuncts": list(ACTIVE_CONJUNCT_SYMBOLS),
            "source_flow": [
                "empty check",
                "same-allocation raw [MaybeUninit<T>] to [T] slice cast",
                "compiler drop glue for the nonempty raw slice",
                "one ordered Destruct transition per element",
                "each dropped logical slot becomes Uninitialized",
            ],
            "final_state_projection": (
                "explicit exact theorem state"
                if purpose == PRIMARY
                else "source-derived final contract retained while comparing unit return"
            ),
        },
        "boundary_scope": {
            "shared_observations": [
                "initial initialized storage and relation lengths",
                "initial allocation, address, provenance, and mutable-borrow identity",
                "element layout and platform pointer limits",
                "per-element Destruct outcomes and state transitions",
                "pre-existing frame and initial Destruct state",
            ],
            "excluded_observations": [
                "resulting storage",
                "aggregate final Destruct state",
                "drop order or count",
                "answer encoding",
                "complete target execution trace",
            ],
            "admitted_trust_site_ids": list(ADMITTED_TRUST_SITES),
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
                "symbols": list(source_transitions),
                "source_citations": [
                    TARGET_SOURCE_REFERENCE,
                    DROP_IN_PLACE_REFERENCE,
                ],
                "semantics": (
                    "derive the raw slice identity, source-ordered drop count, "
                    "per-element Destruct composition, and Uninitialized final slots"
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
        "source_transition_definitions": list(source_transitions),
        "source_transition_bindings": {
            "nonempty_branch": {
                "symbols": [
                    "DropOperationCount",
                    "DropIndexAtStep",
                    "DropSourceExecution_T",
                ],
                "trust_site_ids": ["TS-025-D003"],
                "source_citations": [TARGET_SOURCE_REFERENCE],
            },
            "raw_slice_cast": {
                "symbols": [
                    "RawSliceAllocation",
                    "RawSliceAddress",
                    "RawSliceProvenance",
                    "RawSliceBorrow",
                ],
                "replacement_id": REPLACEMENT_ID,
                "source_citations": [
                    TARGET_SOURCE_REFERENCE,
                    DROP_IN_PLACE_REFERENCE,
                ],
            },
            "drop_glue_and_destruct": {
                "symbols": [
                    "DestructCompletedThrough",
                    "DropStorageAfterStep",
                    "DropStorageAfterSteps",
                    "DropFinalStorage",
                    "DropFinalDestructState",
                ],
                "replacement_id": REPLACEMENT_ID,
                "source_citations": [
                    TARGET_SOURCE_REFERENCE,
                    DROP_IN_PLACE_REFERENCE,
                ],
            },
        },
        "equivalence_kind": "exact",
        "equivalence_scope": (
            "unit return plus exact storage, pointer, Destruct state, layout, and frame"
            if purpose == PRIMARY
            else "unit return"
        ),
        "principal_observations": _principal_observations(purpose),
    }


def obligation(purpose: str) -> tuple[str, dict[str, Any]]:
    return obligation_text(purpose), obligation_metadata(purpose)


def validate_target_obligation(text: str, metadata: dict[str, Any]) -> None:
    validate_obligation(text, metadata)
    purpose = metadata.get("obligation_purpose")
    if purpose not in PURPOSES:
        raise GuardError("target-025 obligation has an unknown purpose")
    expected_text, expected_metadata = obligation(str(purpose))
    if metadata != expected_metadata:
        raise GuardError(
            "target-025 metadata differs from the reviewed drop translation"
        )
    if parse_smt(text) != parse_smt(expected_text):
        raise GuardError(
            "target-025 SMT differs from the reviewed drop translation"
        )


def _cell_array(values: dict[int, int]) -> str:
    expression = "((as const (Array Int Cell)) (Initialized 0))"
    for index, value in sorted(values.items()):
        expression = (
            f"(store {expression} {index} (Initialized {value}))"
        )
    return expression


def _int_array(values: dict[int, int], default: int = 0) -> str:
    expression = f"((as const (Array Int Int)) {default})"
    for index, value in sorted(values.items()):
        expression = f"(store {expression} {index} {value})"
    return expression


def _outcome_array(completed: tuple[int, ...]) -> str:
    expression = "((as const (Array Int CallbackOutcome)) Panicked)"
    for index in completed:
        expression = f"(store {expression} {index} Completed)"
    return expression


def _case(
    *,
    length: int = 2,
    initialized: dict[int, int] | None = None,
    uninitialized_index: int | None = None,
) -> dict[str, Any]:
    values = (
        {0: 10, 1: 20} if initialized is None and length == 2
        else (initialized or {})
    )
    before = {index: 100 + index for index in range(length)}
    after = {index: 101 + index for index in range(length)}
    return {
        "length": length,
        "relation_initialized_length": length,
        "relation_values_length": length,
        "values": values,
        "uninitialized_index": uninitialized_index,
        "allocation": 51,
        "address": 4096,
        "provenance": 151,
        "borrow": 251,
        "allocation_base": 4096,
        "allocation_bytes": 64,
        "element_size": 4,
        "element_alignment": 4,
        "isize_max": 2_147_483_647,
        "address_space_limit": 4_294_967_295,
        "frame_token": 888,
        "destruct_initial_state": 100,
        "destruct_before": before,
        "destruct_after": after,
        "completed": tuple(range(length)),
    }


PROBE_CASES: dict[str, dict[str, Any]] = {
    "valid_empty": {
        **_case(length=0),
        "kind": "valid",
        "expected": "sat",
    },
    "valid_nonempty": {
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
    "invalid_initialization_mask": {
        **_case(uninitialized_index=1),
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
    "invalid_no_op_drop": {
        **_case(),
        "kind": "no_op_drop",
        "expected": "unsat",
    },
    "invalid_partial_drop": {
        **_case(),
        "kind": "partial_drop",
        "expected": "unsat",
    },
    "invalid_duplicate_drop": {
        **_case(),
        "kind": "duplicate_drop",
        "expected": "unsat",
    },
    "invalid_out_of_order_drop": {
        **_case(),
        "kind": "out_of_order_drop",
        "expected": "unsat",
    },
    "invalid_drop_count": {
        **_case(),
        "kind": "drop_count",
        "expected": "unsat",
    },
    "invalid_callback_order": {
        **_case(),
        "destruct_before": {0: 100, 1: 999},
        "kind": "invalid_domain",
        "expected": "unsat",
    },
    "invalid_callback_state": {
        **_case(),
        "kind": "callback_state",
        "expected": "unsat",
    },
    "invalid_pointer_identity": {
        **_case(),
        "kind": "pointer_identity",
        "expected": "unsat",
    },
    "invalid_frame_token_mutation": {
        **_case(),
        "kind": "frame_token",
        "expected": "unsat",
    },
}

PROBE_EXPECTED_RESULTS = {
    name: str(case["expected"]) for name, case in PROBE_CASES.items()
}


def _storage_expression(case: dict[str, Any]) -> str:
    expression = _cell_array(case["values"])
    index = case["uninitialized_index"]
    if index is not None:
        expression = f"(store {expression} {index} Uninitialized)"
    return expression


def _input_expression(case: dict[str, Any]) -> str:
    values = (
        case["length"],
        case["relation_initialized_length"],
        case["relation_values_length"],
        _storage_expression(case),
        _int_array(case["values"]),
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
        case["destruct_initial_state"],
    )
    return "(mkInput " + " ".join(map(str, values)) + ")"


def _boundary_expression(case: dict[str, Any]) -> str:
    values = (
        case["length"],
        case["relation_initialized_length"],
        case["relation_values_length"],
        _storage_expression(case),
        _int_array(case["values"]),
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
        case["destruct_initial_state"],
        _int_array(case["destruct_before"]),
        _int_array(case["destruct_after"]),
        _outcome_array(case["completed"]),
    )
    return "(mkBoundary " + " ".join(map(str, values)) + ")"


def _model_with_source_mutation(kind: str) -> str:
    text = _model_text(PRIMARY)
    mutations = {
        "duplicate_drop": (
            "(define-fun DropIndexAtStep ((x Input) (step Int)) Int step)",
            "(define-fun DropIndexAtStep ((x Input) (step Int)) Int\n"
            "  (ite (= step 1) 0 step))",
        ),
        "out_of_order_drop": (
            "(define-fun DropIndexAtStep ((x Input) (step Int)) Int step)",
            "(define-fun DropIndexAtStep ((x Input) (step Int)) Int\n"
            "  (- (x_slice_length x) step 1))",
        ),
        "drop_count": (
            "(define-fun DropOperationCount ((x Input)) Int "
            "(x_slice_length x))",
            "(define-fun DropOperationCount ((x Input)) Int\n"
            "  (- (x_slice_length x) 1))",
        ),
    }
    try:
        old, new = mutations[kind]
    except KeyError as exc:
        raise ValueError(f"unknown target-025 source mutation: {kind}") from exc
    if text.count(old) != 1:
        raise RuntimeError(f"target-025 mutation anchor changed: {kind}")
    return text.replace(old, new, 1)


def probe_text(name: str) -> str:
    try:
        case = PROBE_CASES[name]
    except KeyError as exc:
        raise ValueError(f"unknown target-025 probe: {name}") from exc
    kind = case["kind"]
    model = (
        _model_with_source_mutation(kind)
        if kind in {"duplicate_drop", "out_of_order_drop", "drop_count"}
        else _model_text(PRIMARY)
    )
    assertions = [
        f"(= x {_input_expression(case)})",
        f"(= b {_boundary_expression(case)})",
        "(Requires_T x)",
        "(Boundary_T x b)",
        "(Spec_T x b y1 s1)",
    ]
    if kind == "valid":
        assertions.extend(
            [
                "(= (y_return_unit y1) true)",
                f"(= (s_slice_length s1) {case['length']})",
                (
                    "(= (s_storage s1) "
                    "((as const (Array Int Cell)) Uninitialized))"
                ),
            ]
        )
    elif kind == "no_op_drop":
        assertions.append("(= (s_storage s1) (x_storage x))")
    elif kind == "partial_drop":
        assertions.append(
            "(= (select (s_storage s1) 1) (Initialized 20))"
        )
    elif kind in {"duplicate_drop", "out_of_order_drop", "drop_count"}:
        pass
    elif kind == "callback_state":
        assertions.append(
            f"(= (s_destruct_state s1) {case['destruct_after'][1] + 1})"
        )
    elif kind == "pointer_identity":
        assertions.append(
            f"(= (s_destination_address s1) {case['address'] + 4})"
        )
    elif kind == "frame_token":
        assertions.append(
            f"(= (s_frame_token s1) {case['frame_token'] + 1})"
        )
    elif kind != "invalid_domain":
        raise ValueError(f"unknown target-025 probe kind: {kind}")
    body = "\n       ".join(assertions)
    return model + f"""\
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
                    "b_slice_length",
                    "b_relation_initialized_length",
                    "b_relation_values_length",
                    "b_storage",
                    "b_values",
                ],
                "kind": "initial fully initialized MaybeUninit storage only",
                "trust_site_ids": ["TS-025-D003"],
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
                    "b_element_size",
                    "b_element_alignment",
                    "b_isize_max",
                    "b_address_space_limit",
                    "b_frame_token",
                ],
                "kind": "initial memory, provenance, layout, borrow, and frame",
                "source_backed_replacement_ids": [REPLACEMENT_ID],
            },
            {
                "fields": [
                    "b_destruct_initial_state",
                    "b_destruct_state_before",
                    "b_destruct_state_after",
                    "b_destruct_outcome",
                ],
                "kind": (
                    "individual Destruct outcomes and state transitions keyed "
                    "by element index; source derives order, count, and final state"
                ),
                "source_backed_replacement_ids": [REPLACEMENT_ID],
            },
        ],
        "source_backed_replacements": obligation_metadata(PRIMARY)[
            "source_backed_replacements"
        ],
        "admitted_retained_trust_site_ids": list(ADMITTED_TRUST_SITES),
        "excluded_retained_trust_site_ids": list(
            EXCLUDED_RETAINED_TRUST_SITES
        ),
        "context_only_trust_site_ids": list(CONTEXT_ONLY_TRUST_SITES),
        "all_audited_trust_site_ids": list(ALL_AUDITED_TRUST_SITES),
        "excluded_from_boundary": [
            "resulting storage",
            "aggregate final Destruct state",
            "drop order or drop count",
            "answer encoding",
            "selected or complete target execution trace",
        ],
        "boundary_statement": (
            "The boundary fixes initial storage/layout/identity and each lower "
            "Destruct observation. The source nonempty branch, raw slice cast, "
            "drop glue, increasing element order, exact call count, final "
            "Uninitialized slots, and final callback state are all derived."
        ),
    }
