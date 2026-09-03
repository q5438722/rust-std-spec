#!/usr/bin/env python3
"""Source-backed obligations for the two raw slice constructors."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any

from checker_guards import GuardError, parse_smt, validate_obligation


PRIMARY = "completeness-modulo-reviewed-equivalence"
EXACT_OUTPUT = "exact-output-determinism"
PURPOSES = (PRIMARY, EXACT_OUTPUT)

RAW_SOURCE_PATH = "core/src/slice/raw.rs"
RAW_SOURCE_SHA256 = (
    "0914968067f7e2bc798680c1edd72bcb032a9fd44ebb2b6fbc082a3a2b16941f"
)
VOCABULARY_RANGES = ((962, 1049),)
IMMUTABLE = 0
MUTABLE = 1
VERUS_EXPECTED_SUMMARY = "verification results:: 2 verified, 0 errors"


@dataclass(frozen=True)
class RawSliceTarget:
    target: str
    input_order: str
    artifact_id: str
    mutable: bool
    active_contract_sha256: str
    active_contract_text: str
    source_start: int
    source_end: int
    docs_start: int
    docs_end: int
    source_item_sha256: str
    generated_declaration_sha256: str
    harness_sha256: str
    source_body_manifest_sha256: str
    transformation_manifest_sha256: str
    dependency_manifest_sha256: str
    trust_record_sha256: tuple[tuple[str, str], ...]
    source_fragments: tuple[str, ...]
    docs_fragments: tuple[str, ...]

    @property
    def function_name(self) -> str:
        return self.target.rsplit("::", 1)[-1]

    @property
    def source_reference(self) -> str:
        return f"{RAW_SOURCE_PATH}:{self.source_start}-{self.source_end}"

    @property
    def docs_reference(self) -> str:
        return f"{RAW_SOURCE_PATH}:{self.docs_start}-{self.docs_end}"

    @property
    def context_only_trust_site_ids(self) -> tuple[str, ...]:
        return (f"TS-{int(self.input_order):03d}-D001",)

    @property
    def excluded_trust_site_ids(self) -> tuple[str, ...]:
        prefix = f"TS-{int(self.input_order):03d}"
        return (f"{prefix}-D002", f"{prefix}-E001")

    @property
    def all_trust_site_ids(self) -> tuple[str, ...]:
        return tuple(record_id for record_id, _ in self.trust_record_sha256)

    @property
    def trust_hashes(self) -> dict[str, str]:
        return dict(self.trust_record_sha256)

    @property
    def mutability_value(self) -> int:
        return MUTABLE if self.mutable else IMMUTABLE

    @property
    def replacement_id(self) -> str:
        return (
            f"SRC-{int(self.input_order):03d}-UB-CHECK-RAW-FAT-POINTER-DEREF"
        )

    @property
    def expected_results(self) -> dict[str, str]:
        return {
            EXACT_OUTPUT: "unsat",
            PRIMARY: "sat" if self.mutable else "unsat",
        }

    @property
    def expected_classification(self) -> dict[str, str]:
        return {
            "exact_output_determinism_status": "conditional-complete",
            "completeness_modulo_reviewed_equivalence_status": (
                "conditional-incomplete"
                if self.mutable
                else "conditional-complete"
            ),
        }


TARGETS = (
    RawSliceTarget(
        target="core::slice::from_raw_parts",
        input_order="48",
        artifact_id="048_core_slice_from_raw_parts",
        mutable=False,
        active_contract_sha256=(
            "73ec9d9cba07629dcf152cde202578a52cea87134075f0568244d747a3183769"
        ),
        active_contract_text=(
            "pub assume_specification<'a, T>[ core::slice::from_raw_parts::<T> ]"
            "( data: *const T, len: usize, ) -> (ret: &'a [T]) requires "
            "slice_raw_domain_valid_for( slice_raw_domain(data, len, "
            "SliceRawMutability::Immutable), len, "
            "SliceRawMutability::Immutable, ), ensures "
            "slice_from_raw_parts_result(data, len, ret), ;"
        ),
        source_start=124,
        source_end=141,
        docs_start=6,
        docs_end=117,
        source_item_sha256=(
            "9544e272f2c1f29c72893c67e1739041f27647e99198cc311eac1870c87bcfcb"
        ),
        generated_declaration_sha256=(
            "c877f2a2138011203d32801ec4320330f06603fa3b8f4fbadd771e43fd3bf01c"
        ),
        harness_sha256=(
            "3e42cd5003d6c86d4e2f7e9dea23d37b29ffa42e49c787d1495f4bac800ac700"
        ),
        source_body_manifest_sha256=(
            "ec2cc1721a5d7d6a985b766985ffc0b3b55331c5cb2e0801d1e835b9d610837f"
        ),
        transformation_manifest_sha256=(
            "4aee810639b57a53adcc891a46b6b2852b5d96a72709046f02744b9ae9ef32f1"
        ),
        dependency_manifest_sha256=(
            "19bcd652a05891d7606586e8613a56a68067696ce7788709a57d577b4297fb59"
        ),
        trust_record_sha256=(
            (
                "TS-048-D001",
                "8024399bf2002ec725027540003b730af28db2df8d84d097754768b09c3a9836",
            ),
            (
                "TS-048-D002",
                "6a6d15ce0e8f6c03dcb738f76cfbf1659de77b9a61c1ab33e2ddd6f805e96feb",
            ),
            (
                "TS-048-E001",
                "4870ef7b4e4d4711fcad4aa753aee1e2d4e5b54efb249fa6c9c4b432bde1a0b7",
            ),
        ),
        source_fragments=(
            "ub_checks::maybe_is_aligned_and_not_null(data, align, false)",
            "ub_checks::is_valid_allocation_size(size, len)",
            "&*ptr::slice_from_raw_parts(data, len)",
        ),
        docs_fragments=(
            "contained within a single allocation",
            "non-null and aligned even for zero-length slices or slices of ZSTs",
            "properly initialized values of type `T`",
            "must not be mutated for the duration of lifetime `'a`",
            "must not \"wrap around\" the address space",
        ),
    ),
    RawSliceTarget(
        target="core::slice::from_raw_parts_mut",
        input_order="49",
        artifact_id="049_core_slice_from_raw_parts_mut",
        mutable=True,
        active_contract_sha256=(
            "47e90942a15f2cdb0e6584968eedeeb627353ed37da324f1af080c3917f0dc40"
        ),
        active_contract_text=(
            "pub assume_specification<'a, T>[ "
            "core::slice::from_raw_parts_mut::<T> ]( data: *mut T, len: usize, "
            ") -> (ret: &'a mut [T]) requires slice_raw_domain_valid_for( "
            "slice_raw_mut_domain(data, len, SliceRawMutability::Mutable), "
            "len, SliceRawMutability::Mutable, ), ensures "
            "slice_from_raw_parts_mut_result(data, len, ret), ;"
        ),
        source_start=179,
        source_end=196,
        docs_start=143,
        docs_end=172,
        source_item_sha256=(
            "b19fba4b6bde2fc2195bda8acded38ced9f42f1eb67c475260a1e84a9c667093"
        ),
        generated_declaration_sha256=(
            "6a2fc24c253598070947e45b742e09f6ec9a34ea60b671e7aca644845c5a1649"
        ),
        harness_sha256=(
            "27d7b7060a7a6dc7d3d118ad5300bedfc3d6470c115baaaaf0e93101e424598d"
        ),
        source_body_manifest_sha256=(
            "c23b86d5b695c810bedc22e3932aa566e9c9a58e519ec8b48a8d5e8632ae72ed"
        ),
        transformation_manifest_sha256=(
            "b2f34c32a9bb19ce5293c77529fdcd9fd8dd55b066b244fdca11fb2f28b37fb7"
        ),
        dependency_manifest_sha256=(
            "431c74ca8527b5dd68ec1c7daa2987e359b25f7872c148ac114526724fb19764"
        ),
        trust_record_sha256=(
            (
                "TS-049-D001",
                "0e51dcf3bf9800324ae1222ed5f5445509c64f9d1fcad637d749af83c625a6e5",
            ),
            (
                "TS-049-D002",
                "0090ca0f517dccfbe747e1aa60c76a0ab9e98cd7872e7f6d83798af7cb251e0a",
            ),
            (
                "TS-049-E001",
                "e3b674983021a05cd2357dffeab541012f9beab4bcca97073a0b1f7b8ce7ac77",
            ),
        ),
        source_fragments=(
            "ub_checks::maybe_is_aligned_and_not_null(data, align, false)",
            "ub_checks::is_valid_allocation_size(size, len)",
            "&mut *ptr::slice_from_raw_parts_mut(data, len)",
        ),
        docs_fragments=(
            "contained within a single allocation",
            "non-null and aligned even for zero-length slices or slices of ZSTs",
            "properly initialized values of type `T`",
            "Both read and write accesses are forbidden",
            "must not \"wrap around\" the address space",
        ),
    ),
)

TARGET_BY_ARTIFACT = {config.artifact_id: config for config in TARGETS}
TARGET_KEYS = tuple((config.target, config.input_order) for config in TARGETS)

INPUT_FIELDS = (
    ("x_length", "Int"),
    ("x_allocation", "Int"),
    ("x_address", "Int"),
    ("x_provenance", "Int"),
    ("x_root_borrow", "Int"),
    ("x_single_allocation", "Bool"),
    ("x_allocation_base", "Int"),
    ("x_allocation_bytes", "Int"),
    ("x_element_size", "Int"),
    ("x_element_alignment", "Int"),
    ("x_usize_max", "Int"),
    ("x_isize_max", "Int"),
    ("x_address_space_limit", "Int"),
    ("x_alias_readers", "Int"),
    ("x_alias_writers", "Int"),
    ("x_frame_token", "Int"),
)

BOUNDARY_FIELDS = (
    ("b_memory", "(Array Int MemoryCell)", "input_memory"),
    ("b_initialized", "(Array Int Bool)", "input_initialization"),
    ("b_input_allocation", "Int", "input_memory"),
    ("b_input_address", "Int", "input_memory"),
    ("b_input_provenance", "Int", "input_provenance"),
    ("b_root_borrow", "Int", "input_provenance"),
    ("b_single_allocation", "Bool", "input_memory"),
    ("b_allocation_base", "Int", "input_memory"),
    ("b_allocation_bytes", "Int", "input_memory"),
    ("b_element_size", "Int", "input_layout"),
    ("b_element_alignment", "Int", "input_layout"),
    ("b_usize_max", "Int", "input_layout"),
    ("b_isize_max", "Int", "input_layout"),
    ("b_address_space_limit", "Int", "input_layout"),
    ("b_alias_readers", "Int", "input_provenance"),
    ("b_alias_writers", "Int", "input_provenance"),
    ("b_frame_token", "Int", "input_memory"),
)

OUTPUT_FIELDS = (
    ("y_return_memory", "(Seq Int)"),
    ("y_return_length", "Int"),
    ("y_return_allocation", "Int"),
    ("y_return_address", "Int"),
    ("y_return_provenance", "Int"),
    ("y_return_borrow", "Int"),
    ("y_return_mutability", "Int"),
)

STATE_FIELDS = (
    ("s_final_memory", "(Seq Int)"),
    ("s_final_length", "Int"),
    ("s_final_allocation", "Int"),
    ("s_final_address", "Int"),
    ("s_final_provenance", "Int"),
    ("s_final_borrow", "Int"),
    ("s_final_mutability", "Int"),
    ("s_final_alias_readers", "Int"),
    ("s_final_alias_writers", "Int"),
    ("s_final_frame_token", "Int"),
)

NEGATIVE_PROBES = (
    "null_empty",
    "null_nonempty_zst",
    "misaligned_empty",
    "misaligned_nonempty_zst",
    "nonzero_without_allocation",
    "nonzero_without_provenance",
    "multi_allocation_span",
    "span_past_allocation",
    "uninitialized_element",
    "alias_violation",
    "isize_overflow",
    "address_wrap",
    "usize_overflow",
    "wrong_return_memory",
    "wrong_first_addressed_element",
    "wrong_interior_addressed_element",
    "nonempty_starts_at_one_past",
    "zst_nonzero_stride",
    "empty_one_past_dereference",
    "wrong_return_length",
    "wrong_return_allocation",
    "wrong_return_address",
    "wrong_return_provenance",
    "wrong_return_borrow",
    "wrong_return_mutability",
    "state_frame_semantics",
    "boundary_mismatch",
)


def canonical_json_sha256(record: dict[str, str]) -> str:
    payload = json.dumps(
        record, sort_keys=True, separators=(",", ":")
    ).encode()
    return hashlib.sha256(payload).hexdigest()


def _normalized(text: str) -> str:
    return " ".join(text.split())


def validate_source_anchors(
    config: RawSliceTarget,
    source_item: str,
    public_docs: str,
    vocabulary: str,
) -> None:
    normalized_source = _normalized(source_item)
    normalized_docs = _normalized(public_docs)
    for fragment in config.source_fragments:
        if _normalized(fragment) not in normalized_source:
            raise GuardError(
                f"{config.target}: canonical source fragment is absent: {fragment}"
            )
    for fragment in config.docs_fragments:
        if _normalized(fragment) not in normalized_docs:
            raise GuardError(
                f"{config.target}: public safety fragment is absent: {fragment}"
            )
    vocabulary_fragments = (
        "pub ghost enum SliceRawMutability",
        "pub ghost struct SliceRawDomain",
        "pub open spec fn slice_raw_domain_valid",
        "pub open spec fn slice_raw_domain_valid_for",
        (
            "pub open spec fn slice_from_raw_parts_mut_result"
            if config.mutable
            else "pub open spec fn slice_from_raw_parts_result"
        ),
    )
    for fragment in vocabulary_fragments:
        if fragment not in vocabulary:
            raise GuardError(
                f"{config.target}: raw-domain vocabulary is incomplete: {fragment}"
            )
    prohibited = (
        "external_body",
        "assume_specification",
        "TargetDefinition_T",
        "Equivalent_T",
    )
    if any(token in source_item for token in prohibited):
        raise GuardError(f"{config.target}: canonical source is synthetic")
    active_function = (
        "slice_from_raw_parts_mut_result"
        if config.mutable
        else "slice_from_raw_parts_result"
    )
    if active_function not in _normalized(vocabulary):
        raise GuardError(f"{config.target}: active result predicate is absent")


def _record_fields(fields: tuple[tuple[str, str], ...]) -> str:
    return "\n".join(f"      ({name} {sort})" for name, sort in fields)


def _datatype(
    name: str,
    constructor: str,
    fields: tuple[tuple[str, str], ...],
) -> str:
    return (
        f"(declare-datatypes (({name} 0))\n"
        f"  ((({constructor}\n{_record_fields(fields)}))))"
    )


def _state_declaration(purpose: str) -> str:
    if purpose == EXACT_OUTPUT:
        return "(declare-datatypes ((State 0)) (((mkState))))"
    return _datatype("State", "mkState", STATE_FIELDS)


def _boundary_equalities() -> str:
    mapping = (
        ("b_input_allocation", "x_allocation"),
        ("b_input_address", "x_address"),
        ("b_input_provenance", "x_provenance"),
        ("b_root_borrow", "x_root_borrow"),
        ("b_single_allocation", "x_single_allocation"),
        ("b_allocation_base", "x_allocation_base"),
        ("b_allocation_bytes", "x_allocation_bytes"),
        ("b_element_size", "x_element_size"),
        ("b_element_alignment", "x_element_alignment"),
        ("b_usize_max", "x_usize_max"),
        ("b_isize_max", "x_isize_max"),
        ("b_address_space_limit", "x_address_space_limit"),
        ("b_alias_readers", "x_alias_readers"),
        ("b_alias_writers", "x_alias_writers"),
        ("b_frame_token", "x_frame_token"),
    )
    return "\n       ".join(
        f"(= ({boundary} b) ({input_field} x))"
        for boundary, input_field in mapping
    )


def _raw_domain(config: RawSliceTarget) -> str:
    alias = (
        "(and (= (x_alias_readers x) 0)\n"
        "            (= (x_alias_writers x) 0))"
        if config.mutable
        else "(and (>= (x_alias_readers x) 0)\n"
        "            (= (x_alias_writers x) 0))"
    )
    return f"""\
  (and (>= (x_length x) 0)
       (<= (x_length x) (x_usize_max x))
       (> (x_address x) 0)
       (> (x_root_borrow x) 0)
       (x_single_allocation x)
       (>= (x_allocation x) 0)
       (>= (x_provenance x) 0)
       (>= (x_allocation_base x) 0)
       (>= (x_allocation_bytes x) 0)
       (>= (x_element_size x) 0)
       (> (x_element_alignment x) 0)
       (> (x_usize_max x) 0)
       (> (x_isize_max x) 0)
       (> (x_address_space_limit x) 0)
       (= (mod (x_address x) (x_element_alignment x)) 0)
       (or (= (x_element_size x) 0)
           (and (>= (x_element_size x) (x_element_alignment x))
                (= (mod (x_element_size x)
                        (x_element_alignment x)) 0)))
       (<= (ByteCount x) (x_isize_max x))
       (<= (EndAddress x) (x_address_space_limit x))
       (or
         (and (= (ByteCount x) 0)
              (or
                (and (= (x_allocation x) 0)
                     (= (x_provenance x) 0))
                (and (> (x_allocation x) 0)
                     (> (x_provenance x) 0)
                     (<= (x_allocation_base x) (x_address x))
                     (<= (x_address x) (AllocationEnd x))
                     (<= (AllocationEnd x)
                         (x_address_space_limit x)))))
         (and (> (ByteCount x) 0)
              (> (x_allocation x) 0)
              (> (x_provenance x) 0)
              (<= (x_allocation_base x) (x_address x))
              (<= (EndAddress x) (AllocationEnd x))
              (<= (AllocationEnd x) (x_address_space_limit x))))
       {alias}
       (> (x_frame_token x) 0))"""


def _state_transition(config: RawSliceTarget) -> tuple[str, str]:
    name = (
        "MutableExclusiveIdentityFrame"
        if config.mutable
        else "ImmutableNoMutationFrame"
    )
    clauses = []
    if not config.mutable:
        clauses.append(
            "(= (s_final_memory s) (FiniteReturnedView x b 0))"
        )
    clauses.extend(
        (
            "(= (seq.len (s_final_memory s)) (x_length x))",
            "(= (s_final_length s) (x_length x))",
            "(= (s_final_allocation s) (x_allocation x))",
            "(= (s_final_address s) (x_address x))",
            "(= (s_final_provenance s) (x_provenance x))",
            "(= (s_final_borrow s) (x_root_borrow x))",
            f"(= (s_final_mutability s) {config.mutability_value})",
            "(= (s_final_alias_readers s) (x_alias_readers x))",
            "(= (s_final_alias_writers s) (x_alias_writers x))",
            "(= (s_final_frame_token s) (x_frame_token x))",
        )
    )
    body = "\n       ".join(clauses)
    return name, (
        f"(define-fun {name} ((x Input) (b Boundary) (s State)) Bool\n"
        f"  (and {body}))"
    )


def _source_transition_names(
    config: RawSliceTarget, purpose: str
) -> list[str]:
    names = ["RawFatPointerConstruction", "ReferenceDereferenceTransition"]
    if purpose == PRIMARY:
        names.append(_state_transition(config)[0])
    return names


def _source_definitions(config: RawSliceTarget, purpose: str) -> str:
    definitions = f"""\
(define-fun ByteCount ((x Input)) Int
  (* (x_length x) (x_element_size x)))
(define-fun EndAddress ((x Input)) Int
  (+ (x_address x) (ByteCount x)))
(define-fun AllocationEnd ((x Input)) Int
  (+ (x_allocation_base x) (x_allocation_bytes x)))
(define-fun ReturnedIndex ((x Input) (i Int)) Bool
  (and (<= 0 i) (< i (x_length x))))
(define-fun ElementAddress ((x Input) (i Int)) Int
  (ite (= (x_element_size x) 0)
       (x_address x)
       (+ (x_address x) (* i (x_element_size x)))))
(define-fun-rec AddressedRangeInitializedFrom
  ((x Input) (b Boundary) (i Int)) Bool
  (ite (>= i (x_length x))
       true
       (and ((_ is InitializedCell)
              (select (b_memory b) (ElementAddress x i)))
            (select (b_initialized b) (ElementAddress x i))
            (AddressedRangeInitializedFrom x b (+ i 1)))))
(define-fun AddressedRangeInitialized ((x Input) (b Boundary)) Bool
  (AddressedRangeInitializedFrom x b 0))
(define-fun-rec FiniteReturnedView
  ((x Input) (b Boundary) (i Int)) (Seq Int)
  (ite (>= i (x_length x))
       (as seq.empty (Seq Int))
       (seq.++ (seq.unit
                 (cell_value
                   (select (b_memory b) (ElementAddress x i))))
               (FiniteReturnedView x b (+ i 1)))))
(define-fun RawDomainValid ((x Input)) Bool
{_raw_domain(config)})
(define-fun UbCheckTransition ((x Input) (b Boundary)) Bool
  (and (RawDomainValid x)
       (AddressedRangeInitialized x b)
       (> (x_address x) 0)
       (= (mod (x_address x) (x_element_alignment x)) 0)
       (<= (ByteCount x) (x_isize_max x))
       (<= (EndAddress x) (x_address_space_limit x))))
(define-fun RawFatPointerConstruction
  ((x Input) (y Output)) Bool
  (and (= (y_return_length y) (x_length x))
       (= (y_return_allocation y) (x_allocation x))
       (= (y_return_address y) (x_address x))
       (= (y_return_provenance y) (x_provenance x))
       (= (y_return_mutability y) {config.mutability_value})))
(define-fun ReferenceDereferenceTransition
  ((x Input) (b Boundary) (y Output)) Bool
  (and (= (y_return_memory y) (FiniteReturnedView x b 0))
       (= (y_return_borrow y) (x_root_borrow x))))
(define-fun ActiveRawDomainConjunct ((x Input) (b Boundary)) Bool
  (and (RawDomainValid x)
       (AddressedRangeInitialized x b)))
(define-fun ActiveReturnLengthConjunct
  ((x Input) (y Output)) Bool
  (= (y_return_length y) (x_length x)))
(define-fun ActiveSliceStartPointerConjunct
  ((x Input) (y Output)) Bool
  (and (= (y_return_allocation y) (x_allocation x))
       (= (y_return_address y) (x_address x))
       (= (y_return_provenance y) (x_provenance x))
       (= (y_return_borrow y) (x_root_borrow x))
       (= (y_return_mutability y) {config.mutability_value})))"""
    if purpose == PRIMARY:
        definitions += "\n" + _state_transition(config)[1]
    return definitions


def _target_body(config: RawSliceTarget, purpose: str) -> str:
    clauses = [
        "(InitialBoundaryObserved x b)",
        "(UbCheckTransition x b)",
        "(RawFatPointerConstruction x y)",
        "(ReferenceDereferenceTransition x b y)",
        "(ActiveRawDomainConjunct x b)",
        "(ActiveReturnLengthConjunct x y)",
        "(ActiveSliceStartPointerConjunct x y)",
    ]
    if purpose == PRIMARY:
        clauses.append(f"({_state_transition(config)[0]} x b s)")
    return "  (and " + "\n       ".join(clauses) + "))"


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


def model_text(config: RawSliceTarget, purpose: str) -> str:
    if purpose not in PURPOSES:
        raise ValueError(f"{config.target}: unknown obligation purpose {purpose}")
    boundary_fields = tuple(
        (selector, sort) for selector, sort, _ in BOUNDARY_FIELDS
    )
    return f"""\
; Target: {config.target}
; Active contract SHA-256: {config.active_contract_sha256}
; Purpose: {purpose}
; Boundary_T contains only genuine initial memory, allocation/provenance,
; initialization, alias permission, layout/platform, root-borrow, and frame data.
(set-logic ALL)
(declare-datatypes ((MemoryCell 0))
  (((UninitializedCell)
    (InitializedCell (cell_value Int)))))
{_datatype("Input", "mkInput", INPUT_FIELDS)}
{_datatype("Boundary", "mkBoundary", boundary_fields)}
{_datatype("Output", "mkOutput", OUTPUT_FIELDS)}
{_state_declaration(purpose)}
(declare-const x Input)
(declare-const b Boundary)
(declare-const y1 Output)
(declare-const s1 State)
(declare-const y2 Output)
(declare-const s2 State)
(define-fun InitialBoundaryObserved ((x Input) (b Boundary)) Bool
  (and {_boundary_equalities()}))
{_source_definitions(config, purpose)}
(define-fun Requires_T ((x Input)) Bool
  (RawDomainValid x))
(define-fun Boundary_T ((x Input) (b Boundary)) Bool
  (and (InitialBoundaryObserved x b)
       (AddressedRangeInitialized x b)
       (> (b_input_address b) 0)
       (> (b_root_borrow b) 0)
       (b_single_allocation b)
       (> (b_element_alignment b) 0)
       (> (b_usize_max b) 0)
       (> (b_isize_max b) 0)
       (> (b_address_space_limit b) 0)
       (> (b_frame_token b) 0)))
(define-fun TargetDefinition_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
{_target_body(config, purpose)}
(define-fun Spec_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (TargetDefinition_T x b y s))
(define-fun Equivalent_T
  ((x Input) (b Boundary)
   (y1 Output) (s1 State) (y2 Output) (s2 State)) Bool
{_equivalence_body(purpose)}
"""


def obligation_text(config: RawSliceTarget, purpose: str) -> str:
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


def _principal_observations(purpose: str) -> list[dict[str, str]]:
    observations = [
        {
            "selector": selector,
            "left": "output1",
            "right": "output2",
            "sort": sort.strip("()"),
        }
        for selector, sort in OUTPUT_FIELDS
    ]
    if purpose == PRIMARY:
        observations.extend(
            {
                "selector": selector,
                "left": "state1",
                "right": "state2",
                "sort": sort.strip("()"),
            }
            for selector, sort in STATE_FIELDS
        )
    return observations


def _source_replacements(
    config: RawSliceTarget, purpose: str
) -> list[dict[str, Any]]:
    return [
        {
            "replacement_id": config.replacement_id,
            "operation": (
                "source UB precondition; ptr::slice_from_raw_parts_mut; "
                "&mut pointwise address-indexed raw-slice dereference"
                if config.mutable
                else (
                    "source UB precondition; ptr::slice_from_raw_parts; "
                    "& pointwise address-indexed raw-slice dereference"
                )
            ),
            "symbols": _source_transition_names(config, purpose),
            "source_citations": [
                config.source_reference,
                config.docs_reference,
            ],
            "replaces_trust_site_ids": list(config.excluded_trust_site_ids),
        }
    ]


def _boundary_metadata(
    config: RawSliceTarget, purpose: str
) -> list[dict[str, Any]]:
    return [
        {
            "selector": selector,
            "role": role,
            "source_citations": [
                config.source_reference,
                config.docs_reference,
            ],
            "trust_site_ids": [],
            "source_backed_replacement_ids": [config.replacement_id],
        }
        for selector, _, role in BOUNDARY_FIELDS
    ]


def obligation_metadata(
    config: RawSliceTarget, purpose: str
) -> dict[str, Any]:
    if purpose not in PURPOSES:
        raise ValueError(f"{config.target}: unknown obligation purpose {purpose}")
    mutable_state = (
        "The returned unique reference may mutate its in-range memory during "
        "the borrow lifetime. The safety docs forbid competing accesses but "
        "permit accesses derived from that return, while the active contract "
        "fixes only its initial view and states no final returned-memory "
        "clause. Final in-range memory is therefore a legitimate unconstrained "
        "State field."
        if config.mutable
        else (
            "The shared-reference safety domain prohibits mutation for the "
            "borrow lifetime, so the source transition preserves input memory."
        )
    )
    return {
        "schema_version": 3,
        "target": config.target,
        "input_order": config.input_order,
        "obligation_purpose": purpose,
        "active_contract_sha256": config.active_contract_sha256,
        "active_contract_text": config.active_contract_text,
        "domain": {
            "length": (
                "arbitrary usize length, including allocated or dangling empty "
                "slices and nonempty zero-sized slices"
            ),
            "memory": (
                "boundary storage is indexed by concrete addresses; every "
                "logical element address is initialized, and every nonzero-byte "
                "span has one allocation and provenance and permits only its "
                "one-past endpoint"
            ),
            "layout": (
                "nonnull aligned pointer even for empty/ZST inputs; byte-count "
                "multiplication fits isize and endpoint arithmetic does not wrap"
            ),
            "aliasing": (
                "exclusive root borrow with no competing readers or writers"
                if config.mutable
                else (
                    "shared root borrow permits readers but prohibits mutation "
                    "for the lifetime"
                )
            ),
            "mutable_final_state": mutable_state,
        },
        "contract_translation": {
            "active_conjuncts": [
                "ActiveRawDomainConjunct",
                "ActiveReturnLengthConjunct",
                "ActiveSliceStartPointerConjunct",
            ],
            "source_flow": [
                "evaluate nonnull/alignment and allocation-size UB checks",
                "construct a raw fat pointer from data and len",
                (
                    "derive each finite returned-view element from boundary "
                    "memory at data + index * element size, using data itself "
                    "for ZST elements and no memory cell for an empty view"
                ),
                (
                    "preserve immutable memory and frame"
                    if not config.mutable
                    else (
                        "preserve unique reference identity and outside frame "
                        "without inventing a final-memory clause"
                    )
                ),
            ],
        },
        "boundary_scope": {
            "shared_observations": [
                "initial address-indexed memory and initialization",
                "initial allocation bounds, provenance, and one-allocation fact",
                "root borrow and alias permissions",
                "element layout and platform limits",
                "pre-existing frame token",
            ],
            "excluded_observations": [
                "returned reference or sequence",
                "final storage",
                "target truth or answer encoding",
                "raw fat-pointer result",
                "selected or complete execution trace",
            ],
            "admitted_trust_site_ids": [],
            "excluded_retained_trust_site_ids": list(
                config.excluded_trust_site_ids
            ),
            "context_only_trust_site_ids": list(
                config.context_only_trust_site_ids
            ),
            "all_audited_trust_site_ids": list(config.all_trust_site_ids),
            "source_backed_replacement_ids": [config.replacement_id],
            "narrower_than_target": True,
        },
        "source_backed_replacements": _source_replacements(config, purpose),
        "target_definition": "TargetDefinition_T",
        "theorem_variables": {
            "input": "x",
            "boundary": "b",
            "output1": "y1",
            "state1": "s1",
            "output2": "y2",
            "state2": "s2",
        },
        "boundary_fields": _boundary_metadata(config, purpose),
        "declared_functions": [],
        "source_transition_definitions": _source_transition_names(
            config, purpose
        ),
        "source_transition_bindings": {
            "ub_check": {
                "symbol": "UbCheckTransition",
                "source_citations": [
                    config.source_reference,
                    config.docs_reference,
                ],
            },
            "raw_fat_pointer_construction": {
                "symbol": "RawFatPointerConstruction",
                "source_citations": [config.source_reference],
            },
            "reference_dereference": {
                "symbol": "ReferenceDereferenceTransition",
                "source_citations": [
                    config.source_reference,
                    config.docs_reference,
                ],
            },
            "state_frame": {
                "symbol": (
                    _state_transition(config)[0]
                    if purpose == PRIMARY
                    else "not projected"
                ),
                "source_citations": [
                    config.source_reference,
                    config.docs_reference,
                ],
            },
        },
        "equivalence_kind": "exact",
        "equivalence_scope": (
            "every return/reference field and every modeled state field"
            if purpose == PRIMARY
            else "every initial return/reference field"
        ),
        "principal_observations": _principal_observations(purpose),
        "expected_solver_result": config.expected_results[purpose],
    }


def obligation(
    config: RawSliceTarget, purpose: str
) -> tuple[str, dict[str, Any]]:
    return obligation_text(config, purpose), obligation_metadata(config, purpose)


def validate_target_obligation(
    config: RawSliceTarget,
    text: str,
    metadata: dict[str, Any],
) -> None:
    validate_obligation(text, metadata)
    purpose = metadata.get("obligation_purpose")
    if purpose not in PURPOSES:
        raise GuardError(f"{config.target}: unknown raw-slice purpose")
    expected_text, expected_metadata = obligation(config, str(purpose))
    if metadata != expected_metadata:
        raise GuardError(
            f"{config.target}: metadata differs from the reviewed source model"
        )
    if parse_smt(text) != parse_smt(expected_text):
        raise GuardError(
            f"{config.target}: SMT differs from the reviewed source model"
        )


def _memory_array(values: dict[int, int]) -> str:
    expression = (
        "((as const (Array Int MemoryCell)) UninitializedCell)"
    )
    for address, value in sorted(values.items()):
        expression = (
            f"(store {expression} {address} (InitializedCell {value}))"
        )
    return expression


def _int_sequence(values: tuple[int, ...]) -> str:
    expression = "(as seq.empty (Seq Int))"
    for value in values:
        expression = f"(seq.++ {expression} (seq.unit {value}))"
    return expression


def _element_address(case: dict[str, Any], index: int) -> int:
    if case["element_size"] == 0:
        return int(case["address"])
    return int(case["address"]) + index * int(case["element_size"])


def _view_values(case: dict[str, Any]) -> tuple[int, ...]:
    return tuple(
        int(case["memory"][_element_address(case, index)])
        for index in range(max(int(case["length"]), 0))
    )


def _initialized_array(case: dict[str, Any]) -> str:
    expression = "((as const (Array Int Bool)) false)"
    missing = set(case["initialized_missing"])
    for index in range(max(int(case["length"]), 0)):
        if index not in missing:
            address = _element_address(case, index)
            expression = f"(store {expression} {address} true)"
    return expression


def base_case(config: RawSliceTarget) -> dict[str, Any]:
    return {
        "memory": {4096: 10, 4100: 20, 4104: 30},
        "initialized_missing": (),
        "length": 3,
        "allocation": 41,
        "address": 4096,
        "provenance": 141,
        "root_borrow": 241,
        "single_allocation": True,
        "allocation_base": 4096,
        "allocation_bytes": 64,
        "element_size": 4,
        "element_alignment": 4,
        "usize_max": 4_294_967_295,
        "isize_max": 2_147_483_647,
        "address_space_limit": 4_294_967_295,
        "alias_readers": 0 if config.mutable else 2,
        "alias_writers": 0,
        "frame_token": 777,
    }


def source_cases(config: RawSliceTarget) -> dict[str, dict[str, Any]]:
    base = base_case(config)
    return {
        "allocated_nonempty": dict(base),
        "allocated_empty": {
            **base,
            "memory": {},
            "length": 0,
        },
        "dangling_empty": {
            **base,
            "memory": {},
            "length": 0,
            "allocation": 0,
            "address": 8,
            "provenance": 0,
            "allocation_base": 0,
            "allocation_bytes": 0,
            "element_alignment": 4,
        },
        "allocated_nonempty_zst": {
            **base,
            "memory": {4096: 7},
            "length": 4,
            "element_size": 0,
            "element_alignment": 8,
        },
        "dangling_nonempty_zst": {
            **base,
            "memory": {8: 7},
            "length": 4,
            "allocation": 0,
            "address": 8,
            "provenance": 0,
            "allocation_base": 0,
            "allocation_bytes": 0,
            "element_size": 0,
            "element_alignment": 8,
        },
        "permitted_one_past_endpoint": {
            **base,
            "length": 4,
            "memory": {4096: 1, 4100: 2, 4104: 3, 4108: 4},
            "allocation_bytes": 16,
        },
        "allocated_empty_at_one_past": {
            **base,
            "memory": {4160: 999},
            "length": 0,
            "address": 4160,
        },
    }


def negative_probe_case(
    config: RawSliceTarget, name: str
) -> tuple[dict[str, Any], str]:
    if name not in NEGATIVE_PROBES:
        raise ValueError(f"{config.target}: unknown negative probe {name}")
    case = base_case(config)
    kind = "invalid-domain"
    if name == "null_empty":
        case.update(memory={}, length=0, address=0)
    elif name == "null_nonempty_zst":
        case.update(element_size=0, address=0)
    elif name == "misaligned_empty":
        case.update(memory={}, length=0, address=4098)
    elif name == "misaligned_nonempty_zst":
        case.update(element_size=0, element_alignment=8, address=4098)
    elif name == "nonzero_without_allocation":
        case["allocation"] = 0
    elif name == "nonzero_without_provenance":
        case["provenance"] = 0
    elif name == "multi_allocation_span":
        case["single_allocation"] = False
    elif name == "span_past_allocation":
        case["allocation_bytes"] = 8
    elif name == "uninitialized_element":
        case["initialized_missing"] = (1,)
    elif name == "alias_violation":
        if config.mutable:
            case["alias_readers"] = 1
        else:
            case["alias_writers"] = 1
    elif name == "isize_overflow":
        case["isize_max"] = 8
    elif name == "address_wrap":
        case.update(
            address=4_294_967_292,
            allocation_base=4_294_967_280,
            allocation_bytes=32,
        )
    elif name == "usize_overflow":
        case["usize_max"] = 2
    elif name == "nonempty_starts_at_one_past":
        case.update(
            memory={4160: 10},
            length=1,
            address=4160,
        )
    elif name == "zst_nonzero_stride":
        case.update(
            memory={4096: 7, 4097: 99},
            element_size=0,
            element_alignment=4,
        )
        kind = name
    elif name == "empty_one_past_dereference":
        case.update(
            memory={4160: 999},
            length=0,
            address=4160,
        )
        kind = name
    elif name.startswith("wrong_return_"):
        kind = name
    elif name in {
        "wrong_first_addressed_element",
        "wrong_interior_addressed_element",
    }:
        kind = name
    elif name == "state_frame_semantics":
        kind = name
    elif name == "boundary_mismatch":
        kind = name
    return case, kind


def _input_expression(case: dict[str, Any]) -> str:
    values = (
        case["length"],
        case["allocation"],
        case["address"],
        case["provenance"],
        case["root_borrow"],
        str(bool(case["single_allocation"])).lower(),
        case["allocation_base"],
        case["allocation_bytes"],
        case["element_size"],
        case["element_alignment"],
        case["usize_max"],
        case["isize_max"],
        case["address_space_limit"],
        case["alias_readers"],
        case["alias_writers"],
        case["frame_token"],
    )
    return "(mkInput " + " ".join(map(str, values)) + ")"


def _boundary_expression(
    case: dict[str, Any], *, mismatch: bool = False
) -> str:
    values = (
        _memory_array(case["memory"]),
        _initialized_array(case),
        case["allocation"],
        case["address"] + (8 if mismatch else 0),
        case["provenance"],
        case["root_borrow"],
        str(bool(case["single_allocation"])).lower(),
        case["allocation_base"],
        case["allocation_bytes"],
        case["element_size"],
        case["element_alignment"],
        case["usize_max"],
        case["isize_max"],
        case["address_space_limit"],
        case["alias_readers"],
        case["alias_writers"],
        case["frame_token"],
    )
    return "(mkBoundary " + " ".join(map(str, values)) + ")"


def _model_query() -> str:
    fields = [f"({selector} y1)" for selector, _ in OUTPUT_FIELDS]
    fields.extend(f"({selector} s1)" for selector, _ in STATE_FIELDS)
    return "(get-value (" + " ".join(fields) + "))\n"


def source_instance_text(
    config: RawSliceTarget, name: str
) -> str:
    try:
        case = source_cases(config)[name]
    except KeyError as exc:
        raise ValueError(f"{config.target}: unknown source case {name}") from exc
    return model_text(config, PRIMARY) + f"""\
(assert (= x {_input_expression(case)}))
(assert (= b {_boundary_expression(case)}))
(assert (Requires_T x))
(assert (Boundary_T x b))
(assert (Spec_T x b y1 s1))
(check-sat)
{_model_query()}"""


def _negative_mutation(
    config: RawSliceTarget,
    name: str,
    case: dict[str, Any],
) -> list[str]:
    if name == "state_frame_semantics":
        if config.mutable:
            return ["(= (s_final_alias_writers s1) 1)"]
        changed = list(_view_values(case))
        changed[0] = 999
        return [
            f"(= (s_final_memory s1) {_int_sequence(tuple(changed))})"
        ]
    mutations = {
        "wrong_return_memory": (
            f"(= (y_return_memory y1) {_int_sequence((999,))})"
        ),
        "wrong_first_addressed_element": (
            "(not (= (seq.nth (y_return_memory y1) 0) "
            "(cell_value (select (b_memory b) 4096))))"
        ),
        "wrong_interior_addressed_element": (
            "(exists ((i Int)) "
            "(and (ReturnedIndex x i) "
            "(not (= (seq.nth (y_return_memory y1) i) "
            "(cell_value (select (b_memory b) "
            "(+ (x_address x) (* i (x_element_size x)))))))))"
        ),
        "zst_nonzero_stride": (
            "(= (seq.nth (y_return_memory y1) 1) "
            "(cell_value "
            "(select (b_memory b) (+ (x_address x) 1))))"
        ),
        "empty_one_past_dereference": (
            "(not (= (y_return_memory y1) "
            "(as seq.empty (Seq Int))))"
        ),
        "wrong_return_length": (
            f"(= (y_return_length y1) {case['length'] + 1})"
        ),
        "wrong_return_allocation": (
            f"(= (y_return_allocation y1) {case['allocation'] + 1})"
        ),
        "wrong_return_address": (
            f"(= (y_return_address y1) {case['address'] + 8})"
        ),
        "wrong_return_provenance": (
            f"(= (y_return_provenance y1) {case['provenance'] + 1})"
        ),
        "wrong_return_borrow": (
            f"(= (y_return_borrow y1) {case['root_borrow'] + 1})"
        ),
        "wrong_return_mutability": (
            f"(= (y_return_mutability y1) {1 - config.mutability_value})"
        ),
    }
    return [mutations[name]] if name in mutations else []


def negative_probe_text(config: RawSliceTarget, name: str) -> str:
    case, kind = negative_probe_case(config, name)
    assertions = [
        f"(= x {_input_expression(case)})",
        (
            f"(= b {_boundary_expression(case, mismatch=name == 'boundary_mismatch')})"
        ),
        "(Requires_T x)",
        "(Boundary_T x b)",
    ]
    if kind != "invalid-domain" and name != "boundary_mismatch":
        assertions.append("(Spec_T x b y1 s1)")
        assertions.extend(_negative_mutation(config, name, case))
    body = "\n       ".join(assertions)
    return model_text(config, PRIMARY) + f"""\
(assert
  (and {body}))
(check-sat)
"""


def witness_payload(config: RawSliceTarget) -> dict[str, Any]:
    if not config.mutable:
        raise ValueError("only the mutable raw constructor has a witness")
    return {
        "schema_version": 1,
        "target": config.target,
        "input_order": config.input_order,
        "active_contract_sha256": config.active_contract_sha256,
        "shared_input": {
            "length": 3,
            "allocation": 41,
            "address": 4096,
            "provenance": 141,
            "root_borrow": 241,
            "element_size": 4,
            "element_alignment": 4,
        },
        "shared_boundary": {
            "kind": (
                "address-indexed memory/initialization plus "
                "allocation/provenance/borrow/layout"
            ),
            "memory": {"4096": 10, "4100": 20, "4104": 30},
            "same_for_both_executions": True,
        },
        "execution1": {
            "initial_return_memory": [10, 20, 30],
            "final_memory": [101, 202, 303],
        },
        "execution2": {
            "initial_return_memory": [10, 20, 30],
            "final_memory": [404, 505, 606],
        },
        "active_conjuncts": {
            "raw_domain_valid_for": True,
            "return_length": 3,
            "slice_start_mut_ptr": "same data/provenance/borrow and initial memory",
            "final_memory_clause": "absent from active contract",
        },
        "expected": {
            "both_executions_satisfy_every_active_conjunct": True,
            "exact_output_equal": True,
            "full_state_equal": False,
            "full_exact_equivalent": False,
        },
    }


def fixed_witness_text(config: RawSliceTarget) -> str:
    if not config.mutable:
        raise ValueError("only the mutable raw constructor has a witness")
    case = base_case(config)
    first = _int_sequence((101, 202, 303))
    second = _int_sequence((404, 505, 606))
    return model_text(config, PRIMARY) + f"""\
(assert (= x {_input_expression(case)}))
(assert (= b {_boundary_expression(case)}))
(assert (Requires_T x))
(assert (Boundary_T x b))
(assert (Spec_T x b y1 s1))
(assert (Spec_T x b y2 s2))
(assert (= (s_final_memory s1) {first}))
(assert (= (s_final_memory s2) {second}))
(assert (not (Equivalent_T x b y1 s1 y2 s2)))
(check-sat)
(get-value (
  (y_return_memory y1)
  (y_return_memory y2)
  (s_final_memory s1)
  (s_final_memory s2)
  (Equivalent_T x b y1 s1 y2 s2)))
"""


def boundary_manifest(config: RawSliceTarget) -> dict[str, Any]:
    return {
        "schema_version": 2,
        "target": config.target,
        "input_order": config.input_order,
        "active_contract_sha256": config.active_contract_sha256,
        "boundary_narrower_than_target": True,
        "proof_boundary_assumption": (
            "Both executions share x and observe one identical Boundary_T "
            "containing only address-indexed initial memory and initialization, "
            "allocation/provenance, alias permissions, layout/platform limits, "
            "root borrow, and frame data. Input x contains no logical result "
            "array."
        ),
        "shared_boundary_observations": [
            {
                "fields": [
                    "b_memory",
                    "b_initialized",
                ],
                "kind": "genuine initial address-indexed memory",
            },
            {
                "fields": [
                    "b_input_allocation",
                    "b_input_address",
                    "b_input_provenance",
                    "b_single_allocation",
                    "b_allocation_base",
                    "b_allocation_bytes",
                ],
                "kind": "initial allocation and provenance",
            },
            {
                "fields": [
                    "b_root_borrow",
                    "b_alias_readers",
                    "b_alias_writers",
                    "b_frame_token",
                ],
                "kind": "initial borrow, alias permission, and root frame",
            },
            {
                "fields": [
                    "b_element_size",
                    "b_element_alignment",
                    "b_usize_max",
                    "b_isize_max",
                    "b_address_space_limit",
                ],
                "kind": "type layout and platform limits",
            },
        ],
        "deterministic_source_transitions": {
            "ub_check": (
                "nonnull/aligned pointer plus len*size isize fit, single "
                "allocation, initialized range, alias validity, and no-wrap"
            ),
            "raw_fat_pointer": (
                "construct data+length while preserving allocation/provenance"
            ),
            "reference_dereference": (
                "derive a normalized finite view pointwise from boundary memory "
                "at data + index*element-size; ZST indices reuse data and empty "
                "one-past views read no cell"
            ),
            "state": (
                "immutable memory is unchanged"
                if not config.mutable
                else (
                    "identity/exclusivity/frame are retained; final in-range "
                    "memory is not fixed because the active contract omits it"
                )
            ),
        },
        "source_backed_replacements": _source_replacements(config, PRIMARY),
        "context_only_trust_site_ids": list(
            config.context_only_trust_site_ids
        ),
        "excluded_retained_trust_site_ids": list(
            config.excluded_trust_site_ids
        ),
        "all_audited_trust_site_ids": list(config.all_trust_site_ids),
        "excluded_from_boundary": [
            "returned reference, sequence, length, or fat pointer",
            "final storage or final returned view",
            "target truth or answer encoding",
            "selected or complete execution trace",
        ],
    }


def verus_text(config: RawSliceTarget) -> str:
    mutable = "true" if config.mutable else "false"
    full_proof = (
        """
pub proof fn conditional_complete_from_raw_parts(
    input: Input,
    boundary: Boundary,
    output1: Output,
    state1: FinalState,
    output2: Output,
    state2: FinalState,
)
    requires
        target_transition(input, boundary, output1, state1),
        target_transition(input, boundary, output2, state2),
    ensures
        output1 == output2,
        state1 == state2,
{
    reveal(target_transition);
    reveal(state_frame);
}
"""
        if not config.mutable
        else """
pub proof fn mutable_distinct_final_memory_witness(
    input: Input,
    boundary: Boundary,
    first: Seq<int>,
    second: Seq<int>,
)
    requires
        valid_input(input),
        boundary_holds(input, boundary),
        first.len() == input.length,
        second.len() == input.length,
        first != second,
    ensures
        target_transition(
            input,
            boundary,
            source_output(input, boundary),
            framed_state(input, boundary, first),
        ),
        target_transition(
            input,
            boundary,
            source_output(input, boundary),
            framed_state(input, boundary, second),
        ),
        framed_state(input, boundary, first)
            != framed_state(input, boundary, second),
{
    reveal(target_transition);
    reveal(active_contract);
    reveal(state_frame);
}
"""
    )
    return f"""\
#![allow(dead_code, unused_imports, unused_variables)]
// Trusted-free source model for {config.target}.

use vstd::prelude::*;
use vstd::map::*;
use vstd::seq::*;

verus! {{

pub ghost struct Input {{
    pub length: int,
    pub allocation: int,
    pub address: int,
    pub provenance: int,
    pub root_borrow: int,
    pub single_allocation: bool,
    pub allocation_base: int,
    pub allocation_bytes: int,
    pub element_size: int,
    pub element_alignment: int,
    pub usize_max: int,
    pub isize_max: int,
    pub address_space_limit: int,
    pub alias_readers: int,
    pub alias_writers: int,
    pub frame_token: int,
}}

pub ghost struct Boundary {{
    pub memory: Map<int, int>,
    pub initialized: Map<int, bool>,
    pub allocation: int,
    pub address: int,
    pub provenance: int,
    pub root_borrow: int,
    pub single_allocation: bool,
    pub allocation_base: int,
    pub allocation_bytes: int,
    pub element_size: int,
    pub element_alignment: int,
    pub usize_max: int,
    pub isize_max: int,
    pub address_space_limit: int,
    pub alias_readers: int,
    pub alias_writers: int,
    pub frame_token: int,
}}

pub ghost struct Output {{
    pub memory: Seq<int>,
    pub length: int,
    pub allocation: int,
    pub address: int,
    pub provenance: int,
    pub borrow: int,
    pub mutable: bool,
}}

pub ghost struct FinalState {{
    pub memory: Seq<int>,
    pub length: int,
    pub allocation: int,
    pub address: int,
    pub provenance: int,
    pub borrow: int,
    pub mutable: bool,
    pub alias_readers: int,
    pub alias_writers: int,
    pub frame_token: int,
}}

pub open spec fn byte_count(input: Input) -> int {{
    input.length * input.element_size
}}

pub open spec fn endpoint(input: Input) -> int {{
    input.address + byte_count(input)
}}

pub open spec fn allocation_end(input: Input) -> int {{
    input.allocation_base + input.allocation_bytes
}}

pub open spec fn returned_index(input: Input, index: int) -> bool {{
    0 <= index < input.length
}}

pub open spec fn element_address(input: Input, index: int) -> int {{
    if input.element_size == 0 {{
        input.address
    }} else {{
        input.address + index * input.element_size
    }}
}}

pub open spec fn addressed_range_initialized(
    input: Input,
    boundary: Boundary,
) -> bool {{
    forall|i: int| #![auto] returned_index(input, i) ==> (
        boundary.memory.dom().contains(element_address(input, i))
            && boundary.initialized.dom().contains(element_address(input, i))
            && boundary.initialized[element_address(input, i)]
    )
}}

pub open spec fn returned_view(
    input: Input,
    boundary: Boundary,
) -> Seq<int> {{
    Seq::new(
        if input.length >= 0 {{ input.length as nat }} else {{ 0 }},
        |i: int| boundary.memory[element_address(input, i)],
    )
}}

pub open spec fn valid_input(input: Input) -> bool {{
    0 <= input.length <= input.usize_max
        && input.address > 0
        && input.root_borrow > 0
        && input.single_allocation
        && input.allocation >= 0
        && input.provenance >= 0
        && input.allocation_base >= 0
        && input.allocation_bytes >= 0
        && input.element_size >= 0
        && input.element_alignment > 0
        && input.usize_max > 0
        && input.isize_max > 0
        && input.address_space_limit > 0
        && input.address % input.element_alignment == 0
        && (input.element_size == 0
            || (input.element_size >= input.element_alignment
                && input.element_size % input.element_alignment == 0))
        && byte_count(input) <= input.isize_max
        && endpoint(input) <= input.address_space_limit
        && ((byte_count(input) == 0
            && ((input.allocation == 0 && input.provenance == 0)
                || (input.allocation > 0
                    && input.provenance > 0
                    && input.allocation_base <= input.address
                    && input.address <= allocation_end(input)
                    && allocation_end(input) <= input.address_space_limit)))
            || (byte_count(input) > 0
                && input.allocation > 0
                && input.provenance > 0
                && input.allocation_base <= input.address
                && endpoint(input) <= allocation_end(input)
                && allocation_end(input) <= input.address_space_limit))
        && ({mutable}
            ==> (input.alias_readers == 0 && input.alias_writers == 0))
        && (!{mutable} ==> input.alias_readers >= 0 && input.alias_writers == 0)
        && input.frame_token > 0
}}

pub open spec fn boundary_holds(input: Input, boundary: Boundary) -> bool {{
    boundary.allocation == input.allocation
        && boundary.address == input.address
        && boundary.provenance == input.provenance
        && boundary.root_borrow == input.root_borrow
        && boundary.single_allocation == input.single_allocation
        && boundary.allocation_base == input.allocation_base
        && boundary.allocation_bytes == input.allocation_bytes
        && boundary.element_size == input.element_size
        && boundary.element_alignment == input.element_alignment
        && boundary.usize_max == input.usize_max
        && boundary.isize_max == input.isize_max
        && boundary.address_space_limit == input.address_space_limit
        && boundary.alias_readers == input.alias_readers
        && boundary.alias_writers == input.alias_writers
        && boundary.frame_token == input.frame_token
        && addressed_range_initialized(input, boundary)
}}

pub open spec fn source_output(input: Input, boundary: Boundary) -> Output {{
    Output {{
        memory: returned_view(input, boundary),
        length: input.length,
        allocation: input.allocation,
        address: input.address,
        provenance: input.provenance,
        borrow: input.root_borrow,
        mutable: {mutable},
    }}
}}

pub open spec fn framed_state(
    input: Input,
    boundary: Boundary,
    final_memory: Seq<int>,
) -> FinalState {{
    FinalState {{
        memory: final_memory,
        length: input.length,
        allocation: input.allocation,
        address: input.address,
        provenance: input.provenance,
        borrow: input.root_borrow,
        mutable: {mutable},
        alias_readers: input.alias_readers,
        alias_writers: input.alias_writers,
        frame_token: input.frame_token,
    }}
}}

pub open spec fn state_frame(
    input: Input,
    boundary: Boundary,
    state: FinalState,
) -> bool {{
    state.memory.len() == input.length
        && state == framed_state(
            input,
            boundary,
            if {mutable} {{
                state.memory
            }} else {{
                returned_view(input, boundary)
            }},
        )
}}

pub open spec fn active_contract(
    input: Input,
    boundary: Boundary,
    output: Output,
) -> bool {{
    valid_input(input)
        && output.length == input.length
        && output.memory == returned_view(input, boundary)
        && output.allocation == input.allocation
        && output.address == input.address
        && output.provenance == input.provenance
        && output.borrow == input.root_borrow
        && output.mutable == {mutable}
}}

pub open spec fn target_transition(
    input: Input,
    boundary: Boundary,
    output: Output,
    state: FinalState,
) -> bool {{
    valid_input(input)
        && boundary_holds(input, boundary)
        && output == source_output(input, boundary)
        && state_frame(input, boundary, state)
        && active_contract(input, boundary, output)
}}

pub proof fn conditional_complete_exact_output_{config.function_name}(
    input: Input,
    boundary: Boundary,
    output1: Output,
    state1: FinalState,
    output2: Output,
    state2: FinalState,
)
    requires
        target_transition(input, boundary, output1, state1),
        target_transition(input, boundary, output2, state2),
    ensures
        output1 == output2,
{{
    reveal(target_transition);
}}

{full_proof}
}} // verus!
"""
