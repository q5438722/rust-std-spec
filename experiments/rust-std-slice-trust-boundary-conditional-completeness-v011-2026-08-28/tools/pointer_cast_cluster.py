#!/usr/bin/env python3
"""Source-backed models for the slice pointer-cast target cluster."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from checker_guards import GuardError, parse_smt, validate_obligation


PRIMARY = "completeness-modulo-reviewed-equivalence"
EXACT_OUTPUT = "exact-output-determinism"
PURPOSES = (PRIMARY, EXACT_OUTPUT)

SLICE_SOURCE_PATH = "core/src/slice/mod.rs"
SLICE_SOURCE_SHA256 = (
    "58901fa6437dbd4d77c68427bbced0fc3a91a10fdb8bd2e233adf6a9ba27d2d5"
)
MUT_PTR_SOURCE_PATH = "core/src/ptr/mut_ptr.rs"
MUT_PTR_SOURCE_SHA256 = (
    "f6da79cac4ff864801bb186481a19393e6e4cb66636327295b40550769af4fa8"
)
PTR_ADD_DOCS_PATH = "core/src/ptr/docs/add.md"
PTR_ADD_DOCS_SHA256 = (
    "3e51e10441c020263a930481e04896dd150ccec5f194a99a9f61b8e68fa2d40f"
)


@dataclass(frozen=True)
class CanonicalSource:
    name: str
    path: str
    start: int
    end: int
    file_sha256: str
    excerpt_sha256: str
    filename: str

    @property
    def reference(self) -> str:
        return f"{self.path}:{self.start}-{self.end}"


@dataclass(frozen=True)
class SourceBackedReplacement:
    replacement_id: str
    operation: str
    symbols: tuple[str, ...]
    source_citations: tuple[str, ...]
    replaces_trust_site_ids: tuple[str, ...]


@dataclass(frozen=True)
class PointerTarget:
    target: str
    input_order: str
    artifact_id: str
    active_contract_sha256: str
    active_contract_text: str
    mutable: bool
    range_output: bool
    source_item_filename: str
    source_docs_filename: str
    target_source_reference: str
    all_audited_trust_sites: tuple[str, ...]
    excluded_retained_trust_sites: tuple[str, ...]
    context_only_trust_sites: tuple[str, ...]
    admitted_boundary_trust_sites: tuple[str, ...]
    boundary_backing_trust_sites: tuple[str, ...]
    boundary_backing_source_replacement_ids: tuple[str, ...]
    canonical_sources: tuple[CanonicalSource, ...]
    source_backed_replacements: tuple[SourceBackedReplacement, ...] = ()
    source_dependency: tuple[str, str, str] | None = None

    @property
    def label(self) -> str:
        return f"target-{int(self.input_order):03d}"


CAST_MUT = CanonicalSource(
    name="slice_to_mut_pointer_cast",
    path=SLICE_SOURCE_PATH,
    start=757,
    end=759,
    file_sha256=SLICE_SOURCE_SHA256,
    excerpt_sha256=(
        "99e25e7a86cc5c6b6b7557a4e100daf10a6be356072e931c8a093b6c6198dd9c"
    ),
    filename="canonical_slice_to_mut_pointer_cast.rs",
)
CAST_CONST = CanonicalSource(
    name="slice_to_const_pointer_cast",
    path=SLICE_SOURCE_PATH,
    start=726,
    end=728,
    file_sha256=SLICE_SOURCE_SHA256,
    excerpt_sha256=(
        "df0d49a1417773cb8932d48e9e7bb06a553039beaca7f20000b9fc6319236c1d"
    ),
    filename="canonical_slice_to_const_pointer_cast.rs",
)
MUT_PTR_ADD = CanonicalSource(
    name="mutable_pointer_add",
    path=MUT_PTR_SOURCE_PATH,
    start=909,
    end=962,
    file_sha256=MUT_PTR_SOURCE_SHA256,
    excerpt_sha256=(
        "6e8ec9ed6efba1532abb29e497b6e352f2876d67fab63e9cd056d517f387ebf5"
    ),
    filename="canonical_mut_ptr_add.rs",
)
PTR_ADD_SAFETY = CanonicalSource(
    name="pointer_add_safety",
    path=PTR_ADD_DOCS_PATH,
    start=1,
    end=32,
    file_sha256=PTR_ADD_DOCS_SHA256,
    excerpt_sha256=PTR_ADD_DOCS_SHA256,
    filename="canonical_ptr_add_safety.md",
)

TARGET_019 = PointerTarget(
    target="core::slice::as_mut_ptr",
    input_order="19",
    artifact_id="019_core_slice_as_mut_ptr",
    active_contract_sha256=(
        "840c4efc8976016ca0b1c8728d1cabb13529c6e83939e8ca3cbc31232ba6a14a"
    ),
    active_contract_text=(
        "pub assume_specification<T>[ <[T]>::as_mut_ptr ]( slice: &mut [T], ) "
        "-> (ptr: *mut T) ensures slice_start_mut_ptr(old(slice)@, ptr), "
        "final(slice)@ == old(slice)@, ;"
    ),
    mutable=True,
    range_output=False,
    source_item_filename="slice_as_mut_ptr_item.rs",
    source_docs_filename="slice_as_mut_ptr_docs.md",
    target_source_reference="core/src/slice/mod.rs:730-759",
    all_audited_trust_sites=("TS-019-D001", "TS-019-D002"),
    excluded_retained_trust_sites=("TS-019-D001",),
    context_only_trust_sites=("TS-019-D002",),
    admitted_boundary_trust_sites=(),
    boundary_backing_trust_sites=(),
    boundary_backing_source_replacement_ids=(
        "SRC-019-CANONICAL-SLICE-TO-MUT-PTR",
    ),
    canonical_sources=(CAST_MUT,),
    source_backed_replacements=(
        SourceBackedReplacement(
            replacement_id="SRC-019-CANONICAL-SLICE-TO-MUT-PTR",
            operation="self as *mut [T] as *mut T",
            symbols=(
                "SliceCastAllocation",
                "SliceCastAddress",
                "SliceCastProvenance",
            ),
            source_citations=(
                CAST_MUT.reference,
                "core/src/slice/mod.rs:730-759",
            ),
            replaces_trust_site_ids=("TS-019-D001",),
        ),
    ),
)

TARGET_021 = PointerTarget(
    target="core::slice::as_ptr",
    input_order="21",
    artifact_id="021_core_slice_as_ptr",
    active_contract_sha256=(
        "52c2a91bc8c7e49cd77d4429bb2b2a6e50a788211f2abca511f4df650f1a5edc"
    ),
    active_contract_text=(
        "pub assume_specification<T>[ <[T]>::as_ptr ]( slice: &[T], ) -> "
        "(ptr: *const T) ensures slice_start_ptr(slice@, ptr), ;"
    ),
    mutable=False,
    range_output=False,
    source_item_filename="slice_as_ptr_item.rs",
    source_docs_filename="slice_as_ptr_docs.md",
    target_source_reference="core/src/slice/mod.rs:694-728",
    all_audited_trust_sites=("TS-021-D001", "TS-021-D002"),
    excluded_retained_trust_sites=("TS-021-D001",),
    context_only_trust_sites=("TS-021-D002",),
    admitted_boundary_trust_sites=(),
    boundary_backing_trust_sites=(),
    boundary_backing_source_replacement_ids=(
        "SRC-021-CANONICAL-SLICE-TO-CONST-PTR",
    ),
    canonical_sources=(CAST_CONST,),
    source_backed_replacements=(
        SourceBackedReplacement(
            replacement_id="SRC-021-CANONICAL-SLICE-TO-CONST-PTR",
            operation="self as *const [T] as *const T",
            symbols=(
                "SliceCastAllocation",
                "SliceCastAddress",
                "SliceCastProvenance",
            ),
            source_citations=(
                CAST_CONST.reference,
                "core/src/slice/mod.rs:694-728",
            ),
            replaces_trust_site_ids=("TS-021-D001",),
        ),
    ),
)

TARGET_020 = PointerTarget(
    target="core::slice::as_mut_ptr_range",
    input_order="20",
    artifact_id="020_core_slice_as_mut_ptr_range",
    active_contract_sha256=(
        "0d55922a668ea2e52e07ca14a1146f6ff2d0c9a9d68d9369ff4171f9a6d574c1"
    ),
    active_contract_text=(
        "pub assume_specification<T>[ <[T]>::as_mut_ptr_range ]( "
        "slice: &mut [T], ) -> (range: core::ops::Range<*mut T>) ensures "
        "slice_mut_ptr_range_starts_at_slice(old(slice)@, range), "
        "final(slice)@ == old(slice)@, ;"
    ),
    mutable=True,
    range_output=True,
    source_item_filename="slice_as_mut_ptr_range_item.rs",
    source_docs_filename="slice_as_mut_ptr_range_docs.md",
    target_source_reference="core/src/slice/mod.rs:816-841",
    all_audited_trust_sites=(
        "TS-020-D001",
        "TS-020-D002",
        "TS-020-D003",
        "TS-020-D004",
        "TS-020-C001",
        "TS-020-C002",
        "TS-020-C003",
        "TS-020-E001",
    ),
    excluded_retained_trust_sites=(
        "TS-020-D003",
        "TS-020-D004",
        "TS-020-E001",
    ),
    context_only_trust_sites=(
        "TS-020-D001",
        "TS-020-C001",
        "TS-020-C002",
        "TS-020-C003",
    ),
    admitted_boundary_trust_sites=("TS-020-D002",),
    boundary_backing_trust_sites=("TS-020-D002",),
    boundary_backing_source_replacement_ids=(),
    canonical_sources=(CAST_MUT, MUT_PTR_ADD, PTR_ADD_SAFETY),
    source_backed_replacements=(
        SourceBackedReplacement(
            replacement_id="SRC-020-CANONICAL-SLICE-TO-MUT-PTR",
            operation="self as *mut [T] as *mut T",
            symbols=(
                "SliceCastAllocation",
                "SliceCastAddress",
                "SliceCastProvenance",
            ),
            source_citations=(
                CAST_MUT.reference,
                "core/src/slice/mod.rs:816-841",
            ),
            replaces_trust_site_ids=("TS-020-D003",),
        ),
        SourceBackedReplacement(
            replacement_id="SRC-020-CANONICAL-MUT-PTR-ADD",
            operation="start.add(self.len())",
            symbols=(
                "PtrAddEndAllocation",
                "PtrAddEndAddress",
                "PtrAddEndProvenance",
            ),
            source_citations=(
                MUT_PTR_ADD.reference,
                PTR_ADD_SAFETY.reference,
            ),
            replaces_trust_site_ids=("TS-020-D004", "TS-020-E001"),
        ),
    ),
    source_dependency=(
        "TS-020-D002",
        TARGET_019.target,
        TARGET_019.artifact_id,
    ),
)


def _input_fields(config: PointerTarget) -> tuple[tuple[str, str], ...]:
    fields = (
        ("x_sequence", "Int"),
        ("x_length", "Int"),
        ("x_allocation", "Int"),
        ("x_address", "Int"),
        ("x_provenance", "Int"),
        ("x_element_size", "Int"),
        ("x_element_alignment", "Int"),
        ("x_allocation_base", "Int"),
        ("x_allocation_bytes", "Int"),
        ("x_isize_max", "Int"),
        ("x_address_space_limit", "Int"),
    )
    if config.mutable:
        fields += (
            ("x_mutable_identity", "Int"),
            ("x_frame_token", "Int"),
        )
    return fields


def _boundary_field_specs(
    config: PointerTarget,
) -> tuple[tuple[str, str, str], ...]:
    fields = (
        ("b_input_allocation", "Int", "input_memory"),
        ("b_input_address", "Int", "input_memory"),
        ("b_input_provenance", "Int", "input_provenance"),
        ("b_element_size", "Int", "input_layout"),
        ("b_element_alignment", "Int", "input_layout"),
        ("b_allocation_base", "Int", "input_memory"),
        ("b_allocation_bytes", "Int", "input_memory"),
        ("b_isize_max", "Int", "input_layout"),
        ("b_address_space_limit", "Int", "input_layout"),
    )
    if config.mutable:
        fields += (
            ("b_mutable_identity", "Int", "input_provenance"),
            ("b_frame_token", "Int", "input_memory"),
        )
    return fields


def _output_fields(config: PointerTarget) -> tuple[tuple[str, str], ...]:
    fields = (
        ("y_start_allocation", "Int"),
        ("y_start_address", "Int"),
        ("y_start_provenance", "Int"),
    )
    if config.range_output:
        fields += (
            ("y_end_allocation", "Int"),
            ("y_end_address", "Int"),
            ("y_end_provenance", "Int"),
        )
    return fields


def _state_fields(config: PointerTarget) -> tuple[tuple[str, str], ...]:
    fields = (
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
    if config.mutable:
        fields += (
            ("s_final_mutable_identity", "Int"),
            ("s_final_frame_token", "Int"),
        )
    return fields


def _datatype(name: str, constructor: str, fields: tuple[tuple[str, str], ...]) -> str:
    declarations = "\n".join(
        f"      ({selector} {sort})" for selector, sort in fields
    )
    return (
        f"(declare-datatypes (({name} 0))\n"
        f"  ((({constructor}\n{declarations}))))"
    )


def _state_source_transitions(
    config: PointerTarget,
) -> tuple[tuple[str, str, str], ...]:
    fields = (
        ("s_final_sequence", "FinalSequence", "x_sequence"),
        ("s_final_length", "FinalLength", "x_length"),
        ("s_final_allocation", "FinalAllocation", "x_allocation"),
        ("s_final_address", "FinalAddress", "x_address"),
        ("s_final_provenance", "FinalProvenance", "x_provenance"),
        ("s_final_element_size", "FinalElementSize", "x_element_size"),
        (
            "s_final_element_alignment",
            "FinalElementAlignment",
            "x_element_alignment",
        ),
        ("s_final_allocation_base", "FinalAllocationBase", "x_allocation_base"),
        ("s_final_allocation_bytes", "FinalAllocationBytes", "x_allocation_bytes"),
    )
    if config.mutable:
        fields += (
            (
                "s_final_mutable_identity",
                "FinalMutableIdentity",
                "x_mutable_identity",
            ),
            ("s_final_frame_token", "FinalFrameToken", "x_frame_token"),
        )
    return fields


def _state_declaration(config: PointerTarget, purpose: str) -> str:
    if purpose == EXACT_OUTPUT:
        return "(declare-datatypes ((State 0)) (((mkState))))"
    return _datatype("State", "mkState", _state_fields(config))


def _observed_equalities(config: PointerTarget) -> list[str]:
    mapping = (
        ("b_input_allocation", "x_allocation"),
        ("b_input_address", "x_address"),
        ("b_input_provenance", "x_provenance"),
        ("b_element_size", "x_element_size"),
        ("b_element_alignment", "x_element_alignment"),
        ("b_allocation_base", "x_allocation_base"),
        ("b_allocation_bytes", "x_allocation_bytes"),
        ("b_isize_max", "x_isize_max"),
        ("b_address_space_limit", "x_address_space_limit"),
    )
    if config.mutable:
        mapping += (
            ("b_mutable_identity", "x_mutable_identity"),
            ("b_frame_token", "x_frame_token"),
        )
    return [f"(= ({boundary} b) ({input_field} x))" for boundary, input_field in mapping]


def _source_definitions(config: PointerTarget) -> str:
    definitions = [
        "(define-fun SliceCastAllocation ((x Input)) Int\n  (x_allocation x))",
        "(define-fun SliceCastAddress ((x Input)) Int\n  (x_address x))",
        "(define-fun SliceCastProvenance ((x Input)) Int\n  (x_provenance x))",
    ]
    if config.range_output:
        definitions.extend(
            (
                "(define-fun PtrAddEndAllocation ((x Input)) Int\n"
                "  (SliceCastAllocation x))",
                "(define-fun PtrAddEndAddress ((x Input)) Int\n"
                "  (+ (SliceCastAddress x) (* (x_length x) (x_element_size x))))",
                "(define-fun PtrAddEndProvenance ((x Input)) Int\n"
                "  (SliceCastProvenance x))",
            )
        )
    definitions.extend(
        f"(define-fun {transition} ((x Input)) Int\n  ({input_field} x))"
        for _, transition, input_field in _state_source_transitions(config)
    )
    return "\n".join(definitions)


def _final_state_exists(config: PointerTarget) -> str:
    bindings = [
        (selector.removeprefix("s_"), transition)
        for selector, transition, _ in _state_source_transitions(config)
    ]
    declarations = "\n".join(f"     ({name} Int)" for name, _ in bindings)
    equalities = "\n         ".join(
        f"(= {name} ({transition} x))" for name, transition in bindings
    )
    return (
        "(define-fun FinalStateExists ((x Input)) Bool\n"
        "  (exists\n"
        f"    ({declarations})\n"
        f"    (and {equalities})))"
    )


def _active_contract_definitions(config: PointerTarget) -> str:
    start_name = (
        "ActiveSliceStartMutPtrConjunct"
        if config.mutable
        else "ActiveSliceStartPtrConjunct"
    )
    start = (
        f"(define-fun {start_name} ((x Input) (y Output)) Bool\n"
        "  (and (= (y_start_allocation y) (SliceCastAllocation x))\n"
        "       (= (y_start_address y) (SliceCastAddress x))\n"
        "       (= (y_start_provenance y) (SliceCastProvenance x))))"
    )
    if not config.range_output:
        return start
    result = """\
(define-fun ActiveSliceMutPtrRangeResultConjunct
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
               (+ (x_allocation_base x) (x_allocation_bytes x))))))"""
    return start + "\n" + result


def _requires_body(config: PointerTarget) -> str:
    clauses = [
        "(>= (x_length x) 0)",
        "(>= (x_allocation x) 0)",
        "(> (x_address x) 0)",
        "(>= (x_provenance x) 0)",
        "(>= (x_element_size x) 0)",
        "(> (x_element_alignment x) 0)",
        "(>= (x_allocation_base x) 0)",
        "(>= (x_allocation_bytes x) 0)",
        "(> (x_isize_max x) 0)",
        "(> (x_address_space_limit x) 0)",
        "(= (mod (x_address x) (x_element_alignment x)) 0)",
        "(or (= (x_element_size x) 0)\n"
        "           (and (>= (x_element_size x) (x_element_alignment x))\n"
        "                (= (mod (x_element_size x) (x_element_alignment x)) 0)))",
        "(<= (* (x_length x) (x_element_size x)) (x_isize_max x))",
        "(<= (+ (x_address x) (* (x_length x) (x_element_size x)))\n"
        "           (x_address_space_limit x))",
        "(or (= (* (x_length x) (x_element_size x)) 0)\n"
        "           (and (> (x_allocation x) 0)\n"
        "                (> (x_provenance x) 0)\n"
        "                (<= (+ (x_allocation_base x) (x_allocation_bytes x))\n"
        "                    (x_address_space_limit x))\n"
        "                (<= (x_allocation_base x) (x_address x))\n"
        "                (<= (+ (x_address x)\n"
        "                       (* (x_length x) (x_element_size x)))\n"
        "                    (+ (x_allocation_base x) (x_allocation_bytes x)))))",
    ]
    if config.mutable:
        clauses.append("(> (x_mutable_identity x) 0)")
    return "  (and " + "\n       ".join(clauses) + "))"


def _boundary_body(config: PointerTarget) -> str:
    clauses = [
        "(>= (b_input_allocation b) 0)",
        "(> (b_input_address b) 0)",
        "(>= (b_input_provenance b) 0)",
        "(>= (b_element_size b) 0)",
        "(> (b_element_alignment b) 0)",
        "(>= (b_allocation_base b) 0)",
        "(>= (b_allocation_bytes b) 0)",
        "(> (b_isize_max b) 0)",
        "(> (b_address_space_limit b) 0)",
        "(or (= (* (x_length x) (x_element_size x)) 0)\n"
        "           (and (> (b_input_allocation b) 0)\n"
        "                (> (b_input_provenance b) 0)))",
    ]
    if config.mutable:
        clauses.append("(> (b_mutable_identity b) 0)")
    clauses.append("(InputMemoryLayoutObserved x b)")
    return "  (and " + "\n       ".join(clauses) + "))"


def _target_body(config: PointerTarget, purpose: str) -> str:
    clauses = [
        "(InputMemoryLayoutObserved x b)",
        "(= (y_start_allocation y) (SliceCastAllocation x))",
        "(= (y_start_address y) (SliceCastAddress x))",
        "(= (y_start_provenance y) (SliceCastProvenance x))",
    ]
    if config.range_output:
        clauses.extend(
            (
                "(= (y_end_allocation y) (PtrAddEndAllocation x))",
                "(= (y_end_address y) (PtrAddEndAddress x))",
                "(= (y_end_provenance y) (PtrAddEndProvenance x))",
            )
        )
    if purpose == EXACT_OUTPUT:
        clauses.append("(FinalStateExists x)")
    else:
        clauses.extend(
            f"(= ({selector} s) ({transition} x))"
            for selector, transition, _ in _state_source_transitions(config)
        )
    start_name = (
        "ActiveSliceStartMutPtrConjunct"
        if config.mutable
        else "ActiveSliceStartPtrConjunct"
    )
    clauses.append(f"({start_name} x y)")
    if config.range_output:
        clauses.append("(ActiveSliceMutPtrRangeResultConjunct x y)")
    return "  (and " + "\n       ".join(clauses) + "))"


def _equivalence_body(config: PointerTarget, purpose: str) -> str:
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


def model_text(config: PointerTarget, purpose: str) -> str:
    if purpose not in PURPOSES:
        raise ValueError(f"{config.label}: unknown obligation purpose {purpose}")
    observed = "\n       ".join(_observed_equalities(config))
    return f"""\
; Target: {config.target}
; Active contract SHA-256: {config.active_contract_sha256}
; Purpose: {purpose}
; The boundary contains only initial memory, provenance, layout, platform,
; mutable-identity, and frame observations applicable to this target.
(set-logic ALL)
{_datatype("Input", "mkInput", _input_fields(config))}
{_datatype("Boundary", "mkBoundary", tuple((name, sort) for name, sort, _ in _boundary_field_specs(config)))}
{_datatype("Output", "mkOutput", _output_fields(config))}
{_state_declaration(config, purpose)}
(declare-const x Input)
(declare-const b Boundary)
(declare-const y1 Output)
(declare-const s1 State)
(declare-const y2 Output)
(declare-const s2 State)
(define-fun InputMemoryLayoutObserved ((x Input) (b Boundary)) Bool
  (and {observed}))
{_source_definitions(config)}
{_final_state_exists(config)}
{_active_contract_definitions(config)}
(define-fun Requires_T ((x Input)) Bool
{_requires_body(config)}
(define-fun Boundary_T ((x Input) (b Boundary)) Bool
{_boundary_body(config)}
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


def obligation_text(config: PointerTarget, purpose: str) -> str:
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


def _principal_observations(
    config: PointerTarget, purpose: str
) -> list[dict[str, str]]:
    observations = [
        {
            "selector": selector,
            "left": "output1",
            "right": "output2",
            "sort": sort,
        }
        for selector, sort in _output_fields(config)
    ]
    if purpose == PRIMARY:
        observations.extend(
            {
                "selector": selector,
                "left": "state1",
                "right": "state2",
                "sort": sort,
            }
            for selector, sort in _state_fields(config)
        )
    return observations


def _boundary_fields(config: PointerTarget) -> list[dict[str, Any]]:
    citations = list(
        dict.fromkeys(
            [
                config.target_source_reference,
                *(source.reference for source in config.canonical_sources),
            ]
        )
    )
    return [
        {
            "selector": selector,
            "role": role,
            "source_citations": citations,
            "trust_site_ids": list(config.boundary_backing_trust_sites),
            "source_backed_replacement_ids": list(
                config.boundary_backing_source_replacement_ids
            ),
        }
        for selector, _, role in _boundary_field_specs(config)
    ]


def _source_backed_replacements(
    config: PointerTarget,
) -> list[dict[str, Any]]:
    return [
        {
            "replacement_id": replacement.replacement_id,
            "operation": replacement.operation,
            "symbols": list(replacement.symbols),
            "source_citations": list(replacement.source_citations),
            "replaces_trust_site_ids": list(
                replacement.replaces_trust_site_ids
            ),
        }
        for replacement in config.source_backed_replacements
    ]


def _replacement_ids_for_symbols(
    config: PointerTarget,
    symbols: list[str],
) -> list[str]:
    available = set(symbols)
    return [
        replacement.replacement_id
        for replacement in config.source_backed_replacements
        if set(replacement.symbols) <= available
    ]


def _replaced_trust_sites_for_symbols(
    config: PointerTarget,
    symbols: list[str],
) -> list[str]:
    available = set(symbols)
    return [
        trust_site_id
        for replacement in config.source_backed_replacements
        if set(replacement.symbols) <= available
        for trust_site_id in replacement.replaces_trust_site_ids
    ]


def _replacement_citations_for_symbols(
    config: PointerTarget,
    symbols: list[str],
) -> list[str]:
    available = set(symbols)
    return list(
        dict.fromkeys(
            citation
            for replacement in config.source_backed_replacements
            if set(replacement.symbols) <= available
            for citation in replacement.source_citations
        )
    )


def obligation_metadata(config: PointerTarget, purpose: str) -> dict[str, Any]:
    if purpose not in PURPOSES:
        raise ValueError(f"{config.label}: unknown obligation purpose {purpose}")
    output_transitions = [
        "SliceCastAllocation",
        "SliceCastAddress",
        "SliceCastProvenance",
    ]
    if config.range_output:
        output_transitions.extend(
            [
                "PtrAddEndAllocation",
                "PtrAddEndAddress",
                "PtrAddEndProvenance",
            ]
        )
    state_transitions = [
        transition
        for _, transition, _ in _state_source_transitions(config)
    ]
    cast_binding: dict[str, Any] = {
        "symbols": output_transitions[:3],
        "source_backed_replacement_ids": _replacement_ids_for_symbols(
            config,
            output_transitions[:3],
        ),
        "replaces_trust_site_ids": _replaced_trust_sites_for_symbols(
            config,
            output_transitions[:3],
        ),
        "source_citations": _replacement_citations_for_symbols(
            config,
            output_transitions[:3],
        ),
    }
    if config.source_dependency is not None:
        trust_site, dependency_target, artifact_id = config.source_dependency
        cast_binding["admitted_source_dependency"] = {
            "trust_site_id": trust_site,
            "target": dependency_target,
            "artifact_id": artifact_id,
            "mode": "defined source transition, not a boundary output",
        }
    bindings: dict[str, Any] = {
        "slice_to_thin_pointer_cast": cast_binding,
        "unchanged_final_state": {
            "symbols": state_transitions,
            "source_citations": [config.target_source_reference],
        },
    }
    if config.range_output:
        bindings["mutable_pointer_add"] = {
            "symbols": output_transitions[3:],
            "source_backed_replacement_ids": _replacement_ids_for_symbols(
                config,
                output_transitions[3:],
            ),
            "replaces_trust_site_ids": _replaced_trust_sites_for_symbols(
                config,
                output_transitions[3:],
            ),
            "source_citations": _replacement_citations_for_symbols(
                config,
                output_transitions[3:],
            ),
        }
    return {
        "schema_version": 3,
        "target": config.target,
        "input_order": config.input_order,
        "obligation_purpose": purpose,
        "active_contract_sha256": config.active_contract_sha256,
        "active_contract_text": config.active_contract_text,
        "domain": {
            "slice": (
                "arbitrary nonnegative length and unchanged sequence identity; "
                "mutable targets also preserve the unique borrow and frame"
            ),
            "pointer": (
                "non-null aligned data address; allocation and provenance may be "
                "absent exactly when len * element_size is zero"
            ),
            "layout": (
                "arbitrary positive alignment and nonnegative element size, "
                "including zero-sized types"
            ),
            "safety": (
                "mathematical len * size_of::<T>() fits isize and does not wrap; "
                "a nonzero byte span requires allocation provenance and remains "
                "in allocation through the permitted one-past endpoint"
            ),
        },
        "contract_translation": {
            "slice_start_pointer": (
                "the canonical slice-to-thin-pointer cast retains input "
                "allocation, address, and provenance"
            ),
            "range_result": (
                "not applicable"
                if not config.range_output
                else (
                    "mutable ptr::add computes start + len * size_of::<T>() "
                    "over mathematical integers, preserves allocation and "
                    "provenance, and enforces the documented safety domain"
                )
            ),
            "final_state": (
                "all modeled receiver observations are unchanged"
                if config.mutable
                else "all modeled immutable input observations are unchanged"
            ),
        },
        "boundary_scope": {
            "shared_observations": [
                "initial allocation identity and bounds",
                "initial data-pointer address and provenance",
                "element size and alignment",
                "isize and address-space limits",
                *(
                    ["initial mutable-borrow identity and outside-frame token"]
                    if config.mutable
                    else []
                ),
            ],
            "excluded_observations": [
                "returned pointer or pointer range",
                "returned endpoint",
                "target truth value",
                "answer-equivalent encoding",
                "aggregate final state",
                "selected or complete execution trace",
            ],
            "admitted_trust_site_ids": list(
                config.admitted_boundary_trust_sites
            ),
            "all_audited_trust_site_ids": list(
                config.all_audited_trust_sites
            ),
            "source_backed_replacement_ids": list(
                config.boundary_backing_source_replacement_ids
            ),
            "excluded_retained_trust_site_ids": list(
                config.excluded_retained_trust_sites
            ),
            "context_only_trust_site_ids": list(
                config.context_only_trust_sites
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
        "boundary_fields": _boundary_fields(config),
        "source_backed_replacements": _source_backed_replacements(config),
        "declared_functions": [],
        "source_transition_definitions": output_transitions
        + ([] if purpose == EXACT_OUTPUT else state_transitions),
        "source_transition_bindings": bindings,
        "equivalence_kind": "exact",
        "equivalence_scope": (
            "every pointer component and every modeled final-state observation"
            if purpose == PRIMARY
            else "every pointer component"
        ),
        "principal_observations": _principal_observations(config, purpose),
        "expected_solver_result": "unsat",
    }


def obligation(
    config: PointerTarget, purpose: str
) -> tuple[str, dict[str, Any]]:
    return obligation_text(config, purpose), obligation_metadata(config, purpose)


def validate_target_obligation(
    config: PointerTarget, text: str, metadata: dict[str, Any]
) -> None:
    validate_obligation(text, metadata)
    purpose = metadata.get("obligation_purpose")
    if purpose not in PURPOSES:
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


def _base_values(
    config: PointerTarget,
    *,
    sequence: int,
    length: int,
    allocation: int,
    address: int,
    provenance: int,
    element_size: int,
    element_alignment: int,
    allocation_base: int,
    allocation_bytes: int,
    isize_max: int = 2_147_483_647,
    address_space_limit: int = 4_294_967_295,
) -> dict[str, int]:
    values = {
        "sequence": sequence,
        "length": length,
        "allocation": allocation,
        "address": address,
        "provenance": provenance,
        "element_size": element_size,
        "element_alignment": element_alignment,
        "allocation_base": allocation_base,
        "allocation_bytes": allocation_bytes,
        "isize_max": isize_max,
        "address_space_limit": address_space_limit,
    }
    if config.mutable:
        values["mutable_identity"] = 71
        values["frame_token"] = 901
    return values


def probe_cases(config: PointerTarget) -> dict[str, dict[str, Any]]:
    allocated = _base_values(
        config,
        sequence=101,
        length=3,
        allocation=11,
        address=1024,
        provenance=31,
        element_size=4,
        element_alignment=4,
        allocation_base=1024,
        allocation_bytes=64,
    )
    cases: dict[str, dict[str, Any]] = {
        "allocated_nonempty_non_zst": {
            "kind": "valid-domain",
            "values": allocated,
            "expected_solver_result": "sat",
        },
        "allocated_empty_non_zst": {
            "kind": "valid-domain",
            "values": _base_values(
                config,
                sequence=102,
                length=0,
                allocation=12,
                address=2048,
                provenance=32,
                element_size=4,
                element_alignment=4,
                allocation_base=2048,
                allocation_bytes=16,
            ),
            "expected_solver_result": "sat",
        },
        "dangling_empty_non_zst": {
            "kind": "valid-domain",
            "values": _base_values(
                config,
                sequence=103,
                length=0,
                allocation=0,
                address=8,
                provenance=0,
                element_size=4,
                element_alignment=4,
                allocation_base=0,
                allocation_bytes=0,
            ),
            "expected_solver_result": "sat",
        },
        "allocated_nonempty_zst": {
            "kind": "valid-domain",
            "values": _base_values(
                config,
                sequence=104,
                length=5,
                allocation=13,
                address=4096,
                provenance=33,
                element_size=0,
                element_alignment=8,
                allocation_base=4096,
                allocation_bytes=0,
            ),
            "expected_solver_result": "sat",
        },
        "dangling_nonempty_zst": {
            "kind": "valid-domain",
            "values": _base_values(
                config,
                sequence=105,
                length=5,
                allocation=0,
                address=8,
                provenance=0,
                element_size=0,
                element_alignment=8,
                allocation_base=0,
                allocation_bytes=0,
            ),
            "expected_solver_result": "sat",
        },
        "invalid_null_pointer": {
            "kind": "invalid-input",
            "values": {**allocated, "address": 0},
            "expected_solver_result": "unsat",
        },
        "invalid_misaligned_pointer": {
            "kind": "invalid-input",
            "values": {**allocated, "address": 1026},
            "expected_solver_result": "unsat",
        },
        "invalid_address_len_null_provenance_synthesis": {
            "kind": "invalid-output-synthesis",
            "values": allocated,
            "expected_solver_result": "unsat",
        },
        "invalid_changed_output_allocation": {
            "kind": "invalid-output-allocation",
            "values": allocated,
            "expected_solver_result": "unsat",
        },
        "invalid_changed_output_provenance": {
            "kind": "invalid-output-provenance",
            "values": allocated,
            "expected_solver_result": "unsat",
        },
    }
    if config.mutable:
        cases["invalid_mutable_final_state_change"] = {
            "kind": "invalid-mutable-state",
            "values": allocated,
            "expected_solver_result": "unsat",
        }
    if config.range_output:
        cases.update(
            {
                "invalid_nonzero_offset_without_allocation": {
                    "kind": "invalid-input",
                    "values": {**allocated, "allocation": 0},
                    "expected_solver_result": "unsat",
                },
                "invalid_nonzero_offset_without_provenance": {
                    "kind": "invalid-input",
                    "values": {**allocated, "provenance": 0},
                    "expected_solver_result": "unsat",
                },
                "invalid_nonzero_offset_past_allocation": {
                    "kind": "invalid-input",
                    "values": {**allocated, "allocation_bytes": 8},
                    "expected_solver_result": "unsat",
                },
                "invalid_offset_exceeds_isize": {
                    "kind": "invalid-input",
                    "values": {**allocated, "isize_max": 8},
                    "expected_solver_result": "unsat",
                },
                "invalid_address_overflow": {
                    "kind": "invalid-input",
                    "values": {
                        **allocated,
                        "length": 2,
                        "address": 4092,
                        "allocation_base": 4080,
                        "allocation_bytes": 32,
                        "address_space_limit": 4095,
                    },
                    "expected_solver_result": "unsat",
                },
                "invalid_wrong_start_endpoint": {
                    "kind": "invalid-start-endpoint",
                    "values": allocated,
                    "expected_solver_result": "unsat",
                },
                "invalid_wrong_end_endpoint": {
                    "kind": "invalid-end-endpoint",
                    "values": allocated,
                    "expected_solver_result": "unsat",
                },
            }
        )
    return cases


def _input_value_order(config: PointerTarget) -> tuple[str, ...]:
    fields = (
        "sequence",
        "length",
        "allocation",
        "address",
        "provenance",
        "element_size",
        "element_alignment",
        "allocation_base",
        "allocation_bytes",
        "isize_max",
        "address_space_limit",
    )
    if config.mutable:
        fields += ("mutable_identity", "frame_token")
    return fields


def _boundary_value_order(config: PointerTarget) -> tuple[str, ...]:
    fields = (
        "allocation",
        "address",
        "provenance",
        "element_size",
        "element_alignment",
        "allocation_base",
        "allocation_bytes",
        "isize_max",
        "address_space_limit",
    )
    if config.mutable:
        fields += ("mutable_identity", "frame_token")
    return fields


def _expected_output_assertions(
    config: PointerTarget, values: dict[str, int]
) -> list[str]:
    assertions = [
        f"(= (y_start_allocation y1) {values['allocation']})",
        f"(= (y_start_address y1) {values['address']})",
        f"(= (y_start_provenance y1) {values['provenance']})",
    ]
    if config.range_output:
        end = values["address"] + values["length"] * values["element_size"]
        assertions.extend(
            (
                f"(= (y_end_allocation y1) {values['allocation']})",
                f"(= (y_end_address y1) {end})",
                f"(= (y_end_provenance y1) {values['provenance']})",
            )
        )
    return assertions


def _probe_mutation(
    config: PointerTarget, kind: str, values: dict[str, int]
) -> list[str]:
    if kind in {"valid-domain", "invalid-input"}:
        return []
    if kind == "invalid-output-synthesis":
        return [
            f"(= (y_start_address y1) {values['length']})",
            "(= (y_start_provenance y1) 0)",
        ]
    if kind == "invalid-output-allocation":
        return [
            f"(= (y_start_allocation y1) {values['allocation'] + 1})"
        ]
    if kind == "invalid-output-provenance":
        return [
            f"(= (y_start_provenance y1) {values['provenance'] + 1})"
        ]
    if kind == "invalid-mutable-state":
        return [
            f"(= (s_final_mutable_identity s1) {values['mutable_identity'] + 1})"
        ]
    if kind == "invalid-start-endpoint":
        return [f"(= (y_start_address y1) {values['address'] + 4})"]
    if kind == "invalid-end-endpoint":
        expected = values["address"] + values["length"] * values["element_size"]
        return [f"(= (y_end_address y1) {expected + 4})"]
    raise ValueError(f"{config.label}: unknown probe kind {kind}")


def probe_text(config: PointerTarget, name: str) -> str:
    cases = probe_cases(config)
    try:
        case = cases[name]
    except KeyError as exc:
        raise ValueError(f"{config.label}: unknown probe {name}") from exc
    values = case["values"]
    input_values = " ".join(
        str(values[field]) for field in _input_value_order(config)
    )
    boundary_values = " ".join(
        str(values[field]) for field in _boundary_value_order(config)
    )
    assertions = [
        f"(= x (mkInput {input_values}))",
        f"(= b (mkBoundary {boundary_values}))",
        "(Requires_T x)",
        "(Boundary_T x b)",
    ]
    if case["kind"] != "invalid-input":
        assertions.append("(Spec_T x b y1 s1)")
        if case["kind"] == "valid-domain":
            assertions.extend(_expected_output_assertions(config, values))
        assertions.extend(_probe_mutation(config, case["kind"], values))
    body = "\n       ".join(assertions)
    text = model_text(config, PRIMARY) + f"""\
(assert
  (and {body}))
(check-sat)
"""
    if case["expected_solver_result"] == "sat":
        observations = [
            f"({selector} y1)" for selector, _ in _output_fields(config)
        ] + [
            f"({selector} s1)" for selector, _ in _state_fields(config)
        ]
        text += "(get-value (" + " ".join(observations) + "))\n"
    return text


def boundary_manifest(config: PointerTarget) -> dict[str, Any]:
    boundary_citations = list(
        dict.fromkeys(
            [
                config.target_source_reference,
                *(source.reference for source in config.canonical_sources),
            ]
        )
    )
    observation_backing = {
        "trust_site_ids": list(config.boundary_backing_trust_sites),
        "source_backed_replacement_ids": list(
            config.boundary_backing_source_replacement_ids
        ),
    }
    observations = [
        {
            "fields": [
                "b_input_allocation",
                "b_allocation_base",
                "b_allocation_bytes",
            ],
            "kind": "pre-existing input allocation identity and bounds",
            "source_citations": boundary_citations,
            **observation_backing,
        },
        {
            "fields": ["b_input_address", "b_input_provenance"],
            "kind": "pre-existing slice data-pointer address and provenance",
            "source_citations": boundary_citations,
            **observation_backing,
        },
        {
            "fields": [
                "b_element_size",
                "b_element_alignment",
                "b_isize_max",
                "b_address_space_limit",
            ],
            "kind": "pre-existing pointee and target-platform layout",
            "source_citations": boundary_citations,
            **observation_backing,
        },
    ]
    if config.mutable:
        observations.append(
            {
                "fields": ["b_mutable_identity", "b_frame_token"],
                "kind": (
                    "pre-existing mutable-borrow identity and outside-frame "
                    "observation"
                ),
                "source_citations": boundary_citations,
                **observation_backing,
            }
        )
    transitions: list[dict[str, Any]] = [
        {
            "operation": (
                "self as *mut [T] as *mut T"
                if config.mutable
                else "self as *const [T] as *const T"
            ),
            "semantics": (
                "retains the input slice allocation, data address, and "
                "provenance in the thin pointer"
            ),
            "source_citations": _replacement_citations_for_symbols(
                config,
                [
                    "SliceCastAllocation",
                    "SliceCastAddress",
                    "SliceCastProvenance",
                ],
            ),
            "source_backed_replacement_ids": _replacement_ids_for_symbols(
                config,
                [
                    "SliceCastAllocation",
                    "SliceCastAddress",
                    "SliceCastProvenance",
                ],
            ),
        }
    ]
    if config.range_output:
        transitions.append(
            {
                "operation": "start.add(self.len())",
                "semantics": (
                    "adds len * size_of::<T>() over mathematical integers, "
                    "retains allocation/provenance, permits a zero-byte add, "
                    "and otherwise requires an in-allocation one-past endpoint "
                    "without isize or address overflow"
                ),
                "source_citations": _replacement_citations_for_symbols(
                    config,
                    [
                        "PtrAddEndAllocation",
                        "PtrAddEndAddress",
                        "PtrAddEndProvenance",
                    ],
                ),
                "source_backed_replacement_ids": _replacement_ids_for_symbols(
                    config,
                    [
                        "PtrAddEndAllocation",
                        "PtrAddEndAddress",
                        "PtrAddEndProvenance",
                    ],
                ),
            }
        )
    excluded = []
    for site in config.excluded_retained_trust_sites:
        reasons = {
            "TS-019-D001": (
                "Synthetic null-provenance/address-equals-length constructor; "
                "replaced by the canonical mutable slice cast."
            ),
            "TS-021-D001": (
                "Synthetic null-provenance/address-equals-length constructor; "
                "replaced by the canonical immutable slice cast."
            ),
            "TS-020-D003": (
                "Synthetic mutable slice pointer helper; replaced by the "
                "source-backed target-019 transition."
            ),
            "TS-020-D004": (
                "Answer-equivalent range endpoint dependency; replaced by "
                "explicit mutable ptr::add semantics."
            ),
            "TS-020-E001": (
                "External body supplies the complete endpoint relation and is "
                "not used by the replacement proof."
            ),
        }
        excluded.append({"trust_site_id": site, "reason": reasons[site]})
    dependency = None
    if config.source_dependency is not None:
        site, target, artifact_id = config.source_dependency
        dependency = {
            "trust_site_id": site,
            "target": target,
            "artifact_id": artifact_id,
            "admission": (
                "Only the independently emitted source-backed cast transition "
                "is composed; no returned pointer or target postcondition is "
                "placed in Boundary_T."
            ),
        }
    return {
        "schema_version": 2,
        "target": config.target,
        "input_order": config.input_order,
        "active_contract_sha256": config.active_contract_sha256,
        "boundary_narrower_than_target": True,
        "shared_boundary_observations": observations,
        "deterministic_source_transitions": transitions,
        "source_backed_replacements": _source_backed_replacements(config),
        "boundary_backing_source_replacement_ids": list(
            config.boundary_backing_source_replacement_ids
        ),
        "source_backed_target_dependency": dependency,
        "excluded_retained_sites": excluded,
        "context_only_trust_sites": list(config.context_only_trust_sites),
        "admitted_boundary_trust_site_ids": list(
            config.admitted_boundary_trust_sites
        ),
        "all_audited_trust_site_ids": list(
            config.all_audited_trust_sites
        ),
        "excluded_from_boundary": [
            "returned pointer",
            "returned pointer range or endpoint",
            "target truth value",
            "answer-equivalent encoding",
            "aggregate final state",
            "selected or complete execution trace",
        ],
    }
