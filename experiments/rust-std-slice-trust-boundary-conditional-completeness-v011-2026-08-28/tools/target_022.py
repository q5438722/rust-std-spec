#!/usr/bin/env python3
"""Source-backed pointer cast/add model for input order 22, as_ptr_range."""

from __future__ import annotations

from typing import Any

from checker_guards import GuardError, parse_smt, validate_obligation


TARGET = "core::slice::as_ptr_range"
INPUT_ORDER = "22"
ARTIFACT_ID = "022_core_slice_as_ptr_range"
ACTIVE_CONTRACT_SHA256 = (
    "2bb2f31be87ccb793fb77b630b4b57ca59c5d534fd90d38b858122dee6212434"
)
ACTIVE_CONTRACT_TEXT = (
    "pub assume_specification<T>[ <[T]>::as_ptr_range ]( slice: &[T], ) -> "
    "(range: core::ops::Range<*const T>) ensures "
    "slice_ptr_range_starts_at_slice(slice@, range), ;"
)

PRIMARY = "completeness-modulo-reviewed-equivalence"
EXACT_OUTPUT = "exact-output-determinism"
PURPOSES = (PRIMARY, EXACT_OUTPUT)

CANONICAL_SLICE_CAST_REFERENCE = "core/src/slice/mod.rs:694-728"
CANONICAL_PTR_ADD_REFERENCE = "core/src/ptr/const_ptr.rs:811-864"
CANONICAL_PTR_ADD_DOCS_REFERENCE = "core/src/ptr/docs/add.md:1-32"
CANONICAL_PTR_SOURCE_SHA256 = (
    "c73503de1e8cba8cc409ccd56fba77a6ecd43ddede9591deedb061fba1491f11"
)
CANONICAL_PTR_ADD_ITEM_SHA256 = (
    "6760f0f21de6c6f2497d2097dab6f6c015c40529e2827a1ef76d0ff6304d6973"
)
CANONICAL_PTR_ADD_DOCS_SHA256 = (
    "3e51e10441c020263a930481e04896dd150ccec5f194a99a9f61b8e68fa2d40f"
)

EXCLUDED_RETAINED_TRUST_SITES = (
    "TS-022-D003",
    "TS-022-D004",
    "TS-022-E001",
)
ALL_AUDITED_TRUST_SITES = (
    "TS-022-D001",
    "TS-022-D002",
    "TS-022-D003",
    "TS-022-D004",
    "TS-022-C001",
    "TS-022-C002",
    "TS-022-C003",
    "TS-022-E001",
)

ACTIVE_CONJUNCT_SYMBOLS = (
    "ActiveSliceStartPtrConjunct",
    "ActiveSlicePtrRangeResultConjunct",
)
OUTPUT_FIELDS = (
    ("y_start_allocation", "Int"),
    ("y_start_address", "Int"),
    ("y_start_provenance", "Int"),
    ("y_end_allocation", "Int"),
    ("y_end_address", "Int"),
    ("y_end_provenance", "Int"),
)
STATE_FIELDS = (
    ("s_final_sequence", "Int"),
    ("s_final_length", "Int"),
    ("s_final_allocation", "Int"),
    ("s_final_address", "Int"),
    ("s_final_provenance", "Int"),
    ("s_final_element_size", "Int"),
    ("s_final_element_alignment", "Int"),
    ("s_final_allocation_base", "Int"),
    ("s_final_allocation_bytes", "Int"),
)
OUTPUT_SOURCE_TRANSITIONS = (
    "SliceCastAllocation",
    "SliceCastAddress",
    "SliceCastProvenance",
    "PtrAddEndAllocation",
    "PtrAddEndAddress",
    "PtrAddEndProvenance",
)
STATE_SOURCE_TRANSITIONS = (
    "FinalSequence",
    "FinalLength",
    "FinalAllocation",
    "FinalAddress",
    "FinalProvenance",
    "FinalElementSize",
    "FinalElementAlignment",
    "FinalAllocationBase",
    "FinalAllocationBytes",
)


def _state_declaration(purpose: str) -> str:
    if purpose == EXACT_OUTPUT:
        return "(declare-datatypes ((State 0)) (((mkState))))"
    return """\
(declare-datatypes ((State 0))
  (((mkState
      (s_final_sequence Int)
      (s_final_length Int)
      (s_final_allocation Int)
      (s_final_address Int)
      (s_final_provenance Int)
      (s_final_element_size Int)
      (s_final_element_alignment Int)
      (s_final_allocation_base Int)
      (s_final_allocation_bytes Int)))))"""


def _final_state_arguments(purpose: str) -> str:
    if purpose == EXACT_OUTPUT:
        return "       (FinalStateExists x)"
    return """\
       (= (s_final_sequence s) (FinalSequence x))
       (= (s_final_length s) (FinalLength x))
       (= (s_final_allocation s) (FinalAllocation x))
       (= (s_final_address s) (FinalAddress x))
       (= (s_final_provenance s) (FinalProvenance x))
       (= (s_final_element_size s) (FinalElementSize x))
       (= (s_final_element_alignment s) (FinalElementAlignment x))
       (= (s_final_allocation_base s) (FinalAllocationBase x))
       (= (s_final_allocation_bytes s) (FinalAllocationBytes x))"""


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
        raise ValueError(f"unknown target-022 obligation purpose: {purpose}")
    return f"""\
; Target: {TARGET}
; Active contract SHA-256: {ACTIVE_CONTRACT_SHA256}
; Purpose: {purpose}
; The boundary contains only pre-existing input memory/provenance/layout facts.
(set-logic ALL)
(declare-datatypes ((Input 0))
  (((mkInput
      (x_sequence Int)
      (x_length Int)
      (x_allocation Int)
      (x_address Int)
      (x_provenance Int)
      (x_element_size Int)
      (x_element_alignment Int)
      (x_allocation_base Int)
      (x_allocation_bytes Int)
      (x_isize_max Int)
      (x_address_space_limit Int)))))
(declare-datatypes ((Boundary 0))
  (((mkBoundary
      (b_input_allocation Int)
      (b_input_address Int)
      (b_input_provenance Int)
      (b_element_size Int)
      (b_element_alignment Int)
      (b_allocation_base Int)
      (b_allocation_bytes Int)
      (b_isize_max Int)
      (b_address_space_limit Int)))))
(declare-datatypes ((Output 0))
  (((mkOutput
      (y_start_allocation Int)
      (y_start_address Int)
      (y_start_provenance Int)
      (y_end_allocation Int)
      (y_end_address Int)
      (y_end_provenance Int)))))
{_state_declaration(purpose)}
(declare-const x Input)
(declare-const b Boundary)
(declare-const y1 Output)
(declare-const s1 State)
(declare-const y2 Output)
(declare-const s2 State)
(define-fun InputMemoryLayoutObserved ((x Input) (b Boundary)) Bool
  (and (= (b_input_allocation b) (x_allocation x))
       (= (b_input_address b) (x_address x))
       (= (b_input_provenance b) (x_provenance x))
       (= (b_element_size b) (x_element_size x))
       (= (b_element_alignment b) (x_element_alignment x))
       (= (b_allocation_base b) (x_allocation_base x))
       (= (b_allocation_bytes b) (x_allocation_bytes x))
       (= (b_isize_max b) (x_isize_max x))
       (= (b_address_space_limit b) (x_address_space_limit x))))
(define-fun SliceCastAllocation ((x Input)) Int
  (x_allocation x))
(define-fun SliceCastAddress ((x Input)) Int
  (x_address x))
(define-fun SliceCastProvenance ((x Input)) Int
  (x_provenance x))
(define-fun PtrAddEndAllocation ((x Input)) Int
  (SliceCastAllocation x))
(define-fun PtrAddEndAddress ((x Input)) Int
  (+ (SliceCastAddress x) (* (x_length x) (x_element_size x))))
(define-fun PtrAddEndProvenance ((x Input)) Int
  (SliceCastProvenance x))
(define-fun FinalSequence ((x Input)) Int
  (x_sequence x))
(define-fun FinalLength ((x Input)) Int
  (x_length x))
(define-fun FinalAllocation ((x Input)) Int
  (x_allocation x))
(define-fun FinalAddress ((x Input)) Int
  (x_address x))
(define-fun FinalProvenance ((x Input)) Int
  (x_provenance x))
(define-fun FinalElementSize ((x Input)) Int
  (x_element_size x))
(define-fun FinalElementAlignment ((x Input)) Int
  (x_element_alignment x))
(define-fun FinalAllocationBase ((x Input)) Int
  (x_allocation_base x))
(define-fun FinalAllocationBytes ((x Input)) Int
  (x_allocation_bytes x))
(define-fun FinalStateExists ((x Input)) Bool
  (exists
    ((final_sequence Int)
     (final_length Int)
     (final_allocation Int)
     (final_address Int)
     (final_provenance Int)
     (final_element_size Int)
     (final_element_alignment Int)
     (final_allocation_base Int)
     (final_allocation_bytes Int))
    (and (= final_sequence (FinalSequence x))
         (= final_length (FinalLength x))
         (= final_allocation (FinalAllocation x))
         (= final_address (FinalAddress x))
         (= final_provenance (FinalProvenance x))
         (= final_element_size (FinalElementSize x))
         (= final_element_alignment (FinalElementAlignment x))
         (= final_allocation_base (FinalAllocationBase x))
         (= final_allocation_bytes (FinalAllocationBytes x)))))
(define-fun ActiveSliceStartPtrConjunct ((x Input) (y Output)) Bool
  (and (= (y_start_allocation y) (SliceCastAllocation x))
       (= (y_start_address y) (SliceCastAddress x))
       (= (y_start_provenance y) (SliceCastProvenance x))))
(define-fun ActiveSlicePtrRangeResultConjunct
  ((x Input) (y Output)) Bool
  (and (= (y_end_allocation y) (PtrAddEndAllocation x))
       (= (y_end_address y) (PtrAddEndAddress x))
       (= (y_end_provenance y) (PtrAddEndProvenance x))
       (= (- (y_end_address y) (y_start_address y))
          (* (x_length x) (x_element_size x)))
       (= (y_end_allocation y) (y_start_allocation y))
       (= (y_end_provenance y) (y_start_provenance y))
       (<= (* (x_length x) (x_element_size x)) (x_isize_max x))
       (<= (+ (y_start_address y)
              (* (x_length x) (x_element_size x)))
           (x_address_space_limit x))
       (or (= (* (x_length x) (x_element_size x)) 0)
           (<= (+ (y_start_address y)
                  (* (x_length x) (x_element_size x)))
               (+ (x_allocation_base x) (x_allocation_bytes x))))))
(define-fun Requires_T ((x Input)) Bool
  (and (>= (x_length x) 0)
       (>= (x_allocation x) 0)
       (> (x_address x) 0)
       (>= (x_provenance x) 0)
       (>= (x_element_size x) 0)
       (> (x_element_alignment x) 0)
       (>= (x_allocation_base x) 0)
       (>= (x_allocation_bytes x) 0)
       (> (x_isize_max x) 0)
       (> (x_address_space_limit x) 0)
       (= (mod (x_address x) (x_element_alignment x)) 0)
       (or (= (x_element_size x) 0)
           (and (>= (x_element_size x) (x_element_alignment x))
                (= (mod (x_element_size x)
                        (x_element_alignment x))
                   0)))
       (<= (* (x_length x) (x_element_size x)) (x_isize_max x))
       (<= (+ (x_address x)
              (* (x_length x) (x_element_size x)))
           (x_address_space_limit x))
       (or (= (* (x_length x) (x_element_size x)) 0)
           (and (> (x_allocation x) 0)
                (> (x_provenance x) 0)
                (<= (+ (x_allocation_base x) (x_allocation_bytes x))
                    (x_address_space_limit x))
                (<= (x_allocation_base x) (x_address x))
                (<= (+ (x_address x)
                       (* (x_length x) (x_element_size x)))
                    (+ (x_allocation_base x)
                       (x_allocation_bytes x)))))))
(define-fun Boundary_T ((x Input) (b Boundary)) Bool
  (and (>= (b_input_allocation b) 0)
       (> (b_input_address b) 0)
       (>= (b_input_provenance b) 0)
       (>= (b_element_size b) 0)
       (> (b_element_alignment b) 0)
       (>= (b_allocation_base b) 0)
       (>= (b_allocation_bytes b) 0)
       (> (b_isize_max b) 0)
       (> (b_address_space_limit b) 0)
       (or (= (* (x_length x) (x_element_size x)) 0)
           (and (> (b_input_allocation b) 0)
                (> (b_input_provenance b) 0)))
       (InputMemoryLayoutObserved x b)))
(define-fun TargetDefinition_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and (InputMemoryLayoutObserved x b)
       (= (y_start_allocation y) (SliceCastAllocation x))
       (= (y_start_address y) (SliceCastAddress x))
       (= (y_start_provenance y) (SliceCastProvenance x))
       (= (y_end_allocation y) (PtrAddEndAllocation x))
       (= (y_end_address y) (PtrAddEndAddress x))
       (= (y_end_provenance y) (PtrAddEndProvenance x))
{_final_state_arguments(purpose)}
       (ActiveSliceStartPtrConjunct x y)
       (ActiveSlicePtrRangeResultConjunct x y)))
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
        ("b_input_allocation", "input_memory"),
        ("b_input_address", "input_memory"),
        ("b_input_provenance", "input_provenance"),
        ("b_element_size", "input_layout"),
        ("b_element_alignment", "input_layout"),
        ("b_allocation_base", "input_memory"),
        ("b_allocation_bytes", "input_memory"),
        ("b_isize_max", "input_layout"),
        ("b_address_space_limit", "input_layout"),
    )
    return [
        {
            "selector": selector,
            "role": role,
            "source_citations": [
                CANONICAL_SLICE_CAST_REFERENCE,
                CANONICAL_PTR_ADD_REFERENCE,
                CANONICAL_PTR_ADD_DOCS_REFERENCE,
            ],
            "trust_site_ids": ["TS-022-D002"],
        }
        for selector, role in fields
    ]


def obligation_metadata(purpose: str) -> dict[str, Any]:
    if purpose not in PURPOSES:
        raise ValueError(f"unknown target-022 obligation purpose: {purpose}")
    return {
        "schema_version": 2,
        "target": TARGET,
        "input_order": INPUT_ORDER,
        "obligation_purpose": purpose,
        "active_contract_sha256": ACTIVE_CONTRACT_SHA256,
        "active_contract_text": ACTIVE_CONTRACT_TEXT,
        "domain": {
            "slice": "arbitrary nonnegative length and unchanged sequence identity",
            "pointer": (
                "non-null aligned start address; allocation/provenance may be "
                "absent exactly when len * element_size is zero"
            ),
            "layout": (
                "arbitrary positive alignment and nonnegative element size, "
                "including zero-sized types"
            ),
            "safety": (
                "mathematical byte offset fits isize and does not exceed the "
                "address-space limit; a nonzero offset additionally requires "
                "allocation provenance and an in-allocation range through the "
                "permitted one-past endpoint"
            ),
        },
        "contract_translation": {
            "active_conjuncts": list(ACTIVE_CONJUNCT_SYMBOLS),
            "slice_start_ptr": (
                "interpreted by the canonical &[T] -> *const [T] -> *const T "
                "cast, retaining input allocation, address, and provenance"
            ),
            "slice_ptr_range_result": (
                "interpreted by ptr::add with end address start + len * "
                "size_of::<T>(), retained allocation/provenance, mathematical "
                "no-wrap and isize-fit, plus in-allocation one-past semantics "
                "only for a nonzero byte offset"
            ),
        },
        "boundary_scope": {
            "shared_observations": [
                "input allocation identity and bounds",
                "input start address and provenance",
                "element size and alignment",
                "isize and address-space limits",
            ],
            "excluded_observations": [
                "returned start endpoint",
                "returned end endpoint",
                "returned pointer range",
                "target truth value",
                "answer-equivalent encoding",
                "aggregate final state",
                "selected or complete execution trace",
            ],
            "admitted_trust_site_ids": ["TS-022-D002"],
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
            "slice_to_thin_pointer_cast": {
                "symbols": list(OUTPUT_SOURCE_TRANSITIONS[:3]),
                "trust_site_ids": ["TS-022-D002"],
                "source_citations": [CANONICAL_SLICE_CAST_REFERENCE],
            },
            "pointer_add": {
                "symbols": list(OUTPUT_SOURCE_TRANSITIONS[3:]),
                "replaces_trust_site_ids": ["TS-022-D004", "TS-022-E001"],
                "source_citations": [
                    CANONICAL_PTR_ADD_REFERENCE,
                    CANONICAL_PTR_ADD_DOCS_REFERENCE,
                ],
            },
            "unchanged_final_state": {
                "symbols": list(STATE_SOURCE_TRANSITIONS),
                "source_citations": ["core/src/slice/mod.rs:761-814"],
            },
        },
        "equivalence_kind": "exact",
        "equivalence_scope": (
            "both pointer endpoints and every modeled final-state observation"
            if purpose == PRIMARY
            else "both pointer endpoints"
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
        raise GuardError("target-022 obligation has an unknown purpose")
    expected_text, expected_metadata = obligation(str(purpose))
    if metadata != expected_metadata:
        raise GuardError(
            "target-022 metadata differs from the reviewed pointer translation"
        )
    if parse_smt(text) != parse_smt(expected_text):
        raise GuardError(
            "target-022 SMT differs from the reviewed cast/add translation"
        )


PROBE_CASES: dict[str, dict[str, int]] = {
    "empty_non_zst": {
        "sequence": 101,
        "length": 0,
        "allocation": 11,
        "address": 1024,
        "provenance": 31,
        "element_size": 4,
        "element_alignment": 4,
        "allocation_base": 1024,
        "allocation_bytes": 16,
        "isize_max": 2_147_483_647,
        "address_space_limit": 4_294_967_295,
        "expected_end": 1024,
    },
    "nonempty_non_zst": {
        "sequence": 102,
        "length": 3,
        "allocation": 12,
        "address": 2052,
        "provenance": 32,
        "element_size": 4,
        "element_alignment": 4,
        "allocation_base": 2048,
        "allocation_bytes": 32,
        "isize_max": 2_147_483_647,
        "address_space_limit": 4_294_967_295,
        "expected_end": 2064,
    },
    "nonempty_zst": {
        "sequence": 103,
        "length": 5,
        "allocation": 13,
        "address": 4096,
        "provenance": 33,
        "element_size": 0,
        "element_alignment": 1,
        "allocation_base": 4096,
        "allocation_bytes": 0,
        "isize_max": 2_147_483_647,
        "address_space_limit": 4_294_967_295,
        "expected_end": 4096,
    },
    "dangling_empty_non_zst": {
        "sequence": 104,
        "length": 0,
        "allocation": 0,
        "address": 4,
        "provenance": 0,
        "element_size": 4,
        "element_alignment": 4,
        "allocation_base": 0,
        "allocation_bytes": 0,
        "isize_max": 2_147_483_647,
        "address_space_limit": 4_294_967_295,
        "expected_end": 4,
    },
    "dangling_nonempty_zst": {
        "sequence": 105,
        "length": 5,
        "allocation": 0,
        "address": 8,
        "provenance": 0,
        "element_size": 0,
        "element_alignment": 8,
        "allocation_base": 0,
        "allocation_bytes": 0,
        "isize_max": 2_147_483_647,
        "address_space_limit": 4_294_967_295,
        "expected_end": 8,
    },
    "invalid_null_empty_non_zst": {
        "sequence": 106,
        "length": 0,
        "allocation": 0,
        "address": 0,
        "provenance": 0,
        "element_size": 4,
        "element_alignment": 4,
        "allocation_base": 0,
        "allocation_bytes": 0,
        "isize_max": 2_147_483_647,
        "address_space_limit": 4_294_967_295,
        "expected_end": 0,
    },
    "invalid_no_allocation_nonempty_non_zst": {
        "sequence": 107,
        "length": 2,
        "allocation": 0,
        "address": 8192,
        "provenance": 34,
        "element_size": 4,
        "element_alignment": 4,
        "allocation_base": 8192,
        "allocation_bytes": 16,
        "isize_max": 2_147_483_647,
        "address_space_limit": 4_294_967_295,
        "expected_end": 8200,
    },
    "invalid_no_provenance_nonempty_non_zst": {
        "sequence": 108,
        "length": 2,
        "allocation": 14,
        "address": 12288,
        "provenance": 0,
        "element_size": 4,
        "element_alignment": 4,
        "allocation_base": 12288,
        "allocation_bytes": 16,
        "isize_max": 2_147_483_647,
        "address_space_limit": 4_294_967_295,
        "expected_end": 12296,
    },
}

PROBE_EXPECTED_RESULTS = {
    name: (
        "unsat"
        if name.startswith("invalid_")
        else "sat"
    )
    for name in PROBE_CASES
}


def probe_text(name: str) -> str:
    try:
        case = PROBE_CASES[name]
    except KeyError as exc:
        raise ValueError(f"unknown target-022 probe: {name}") from exc
    input_values = (
        case["sequence"],
        case["length"],
        case["allocation"],
        case["address"],
        case["provenance"],
        case["element_size"],
        case["element_alignment"],
        case["allocation_base"],
        case["allocation_bytes"],
        case["isize_max"],
        case["address_space_limit"],
    )
    boundary_values = input_values[2:]
    return _model_text(PRIMARY) + f"""\
(assert
  (and (= x (mkInput {" ".join(map(str, input_values))}))
       (= b (mkBoundary {" ".join(map(str, boundary_values))}))
       (Requires_T x)
       (Boundary_T x b)
       (Spec_T x b y1 s1)
       (= (y_start_allocation y1) {case["allocation"]})
       (= (y_start_address y1) {case["address"]})
       (= (y_start_provenance y1) {case["provenance"]})
       (= (y_end_allocation y1) {case["allocation"]})
       (= (y_end_address y1) {case["expected_end"]})
       (= (y_end_provenance y1) {case["provenance"]})))
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
                    "b_input_allocation",
                    "b_allocation_base",
                    "b_allocation_bytes",
                ],
                "kind": "pre-existing input allocation identity and bounds",
                "trust_site_ids": ["TS-022-D002"],
            },
            {
                "fields": ["b_input_address", "b_input_provenance"],
                "kind": "pre-existing slice data-pointer address and provenance",
                "trust_site_ids": ["TS-022-D002"],
            },
            {
                "fields": [
                    "b_element_size",
                    "b_element_alignment",
                    "b_isize_max",
                    "b_address_space_limit",
                ],
                "kind": "pre-existing pointee and target-platform layout",
                "trust_site_ids": ["TS-022-D002"],
            },
        ],
        "deterministic_source_transitions": [
            {
                "operation": "self as *const [T] as *const T",
                "semantics": (
                    "retains the input slice allocation, data address, and "
                    "provenance in the thin start pointer"
                ),
                "source_citations": [CANONICAL_SLICE_CAST_REFERENCE],
            },
            {
                "operation": "start.add(self.len())",
                "semantics": (
                    "adds len * size_of::<T>() on mathematical integers, "
                    "retains allocation/provenance, always permits a zero-byte "
                    "addition, and otherwise requires allocation provenance and "
                    "an in-allocation one-past endpoint without address wrapping"
                ),
                "source_citations": [
                    CANONICAL_PTR_ADD_REFERENCE,
                    CANONICAL_PTR_ADD_DOCS_REFERENCE,
                ],
            },
        ],
        "excluded_retained_sites": [
            {
                "trust_site_id": "TS-022-D003",
                "reason": (
                    "The retained model synthesizes a null-provenance pointer "
                    "whose address is the slice length; the replacement uses "
                    "the canonical slice cast from concrete input memory."
                ),
            },
            {
                "trust_site_id": "TS-022-D004",
                "reason": (
                    "The retained dependency supplies the complete range-result "
                    "predicate; explicit ptr::add semantics replace it."
                ),
            },
            {
                "trust_site_id": "TS-022-E001",
                "reason": (
                    "The external body ensures an answer-equivalent endpoint "
                    "relation and is not used by either replacement proof."
                ),
            },
        ],
        "context_only_trust_sites": [
            "TS-022-D001",
            "TS-022-C001",
            "TS-022-C002",
            "TS-022-C003",
        ],
        "admitted_boundary_trust_site_ids": ["TS-022-D002"],
        "all_audited_trust_site_ids": list(ALL_AUDITED_TRUST_SITES),
        "excluded_from_boundary": [
            "returned start endpoint",
            "returned end endpoint",
            "returned range",
            "target truth value",
            "answer-equivalent encodings",
            "aggregate final state",
            "selected or complete execution traces",
        ],
    }
