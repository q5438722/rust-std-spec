#!/usr/bin/env python3
"""Source-backed obligations for get_mut and the unchecked SliceIndex pair."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any

from checker_guards import GuardError, parse_smt, validate_obligation


PRIMARY = "completeness-modulo-reviewed-equivalence"
EXACT_OUTPUT = "exact-output-determinism"
PURPOSES = (PRIMARY, EXACT_OUTPUT)

SLICE_INDEX_SOURCE = "core/src/slice/index.rs"
SLICE_INDEX_SOURCE_SHA256 = (
    "16c924deb46e5e027872853736f082abae1eb45f74e55935814a20979899a935"
)
INDEX_WRAPPER_SOURCE = "core/src/index.rs"
INDEX_WRAPPER_SOURCE_SHA256 = (
    "fbe9e637cbba410ff7180b1f805f03815c31adf0d594104c846c38e738ae16cf"
)
SLICE_INDEX_VOCABULARY_RANGE = (1130, 1145)


@dataclass(frozen=True)
class IndexForm:
    tag: int
    name: str
    source_reference: str
    anchor: str
    sample: tuple[tuple[str, int | bool], ...] = ()

    @property
    def sample_values(self) -> dict[str, int | bool]:
        return dict(self.sample)


INDEX_FORMS = (
    IndexForm(
        0,
        "usize",
        "core/src/slice/index.rs:214-267",
        "unsafe impl<T> const SliceIndex<[T]> for usize",
        (("a", 1),),
    ),
    IndexForm(
        1,
        "ops_index_range",
        "core/src/slice/index.rs:285-352",
        "unsafe impl<T> const SliceIndex<[T]> for ops::IndexRange",
        (("a", 1), ("b", 3)),
    ),
    IndexForm(
        2,
        "ops_range",
        "core/src/slice/index.rs:362-453",
        "unsafe impl<T> const SliceIndex<[T]> for ops::Range<usize>",
        (("a", 1), ("b", 3)),
    ),
    IndexForm(
        3,
        "range_range",
        "core/src/slice/index.rs:463-492",
        "unsafe impl<T> const SliceIndex<[T]> for range::Range<usize>",
        (("a", 0), ("b", 2)),
    ),
    IndexForm(
        4,
        "ops_range_to",
        "core/src/slice/index.rs:502-531",
        "unsafe impl<T> const SliceIndex<[T]> for ops::RangeTo<usize>",
        (("b", 2),),
    ),
    IndexForm(
        5,
        "ops_range_from",
        "core/src/slice/index.rs:541-583",
        "unsafe impl<T> const SliceIndex<[T]> for ops::RangeFrom<usize>",
        (("a", 1),),
    ),
    IndexForm(
        6,
        "range_range_from",
        "core/src/slice/index.rs:593-621",
        "unsafe impl<T> const SliceIndex<[T]> for range::RangeFrom<usize>",
        (("a", 2),),
    ),
    IndexForm(
        7,
        "ops_range_full",
        "core/src/slice/index.rs:631-660",
        "unsafe impl<T> const SliceIndex<[T]> for ops::RangeFull",
    ),
    IndexForm(
        8,
        "ops_range_inclusive",
        "core/src/slice/index.rs:670-718",
        "unsafe impl<T> const SliceIndex<[T]> for ops::RangeInclusive<usize>",
        (("a", 2), ("b", 2), ("exhausted", True)),
    ),
    IndexForm(
        9,
        "range_range_inclusive",
        "core/src/slice/index.rs:728-757",
        "unsafe impl<T> const SliceIndex<[T]> for range::RangeInclusive<usize>",
        (("a", 0), ("b", 1)),
    ),
    IndexForm(
        10,
        "ops_range_to_inclusive",
        "core/src/slice/index.rs:767-796",
        "unsafe impl<T> const SliceIndex<[T]> for ops::RangeToInclusive<usize>",
        (("b", 1),),
    ),
    IndexForm(
        11,
        "range_range_to_inclusive",
        "core/src/slice/index.rs:806-835",
        "unsafe impl<T> const SliceIndex<[T]> for range::RangeToInclusive<usize>",
        (("b", 2),),
    ),
    IndexForm(
        12,
        "ops_bound_pair",
        "core/src/slice/index.rs:930-1075",
        "unsafe impl<T> SliceIndex<[T]> for (ops::Bound<usize>, ops::Bound<usize>)",
        (
            ("a", 1),
            ("b", 3),
            ("start_bound_kind", 1),
            ("end_bound_kind", 2),
        ),
    ),
    IndexForm(
        13,
        "clamp_usize",
        "core/src/index.rs:53-82",
        "unsafe impl<T> SliceIndex<[T]> for Clamp<usize>",
        (("a", 9),),
    ),
    IndexForm(
        14,
        "clamp_range_range",
        "core/src/index.rs:84-125",
        "unsafe impl<T> SliceIndex<[T]> for Clamp<range::Range<usize>>",
        (("a", 1), ("b", 9)),
    ),
    IndexForm(
        15,
        "clamp_ops_range",
        "core/src/index.rs:127-168",
        "unsafe impl<T> SliceIndex<[T]> for Clamp<ops::Range<usize>>",
        (("a", 0), ("b", 9)),
    ),
    IndexForm(
        16,
        "clamp_range_range_inclusive",
        "core/src/index.rs:170-211",
        "unsafe impl<T> SliceIndex<[T]> for Clamp<range::RangeInclusive<usize>>",
        (("a", 1), ("b", 9)),
    ),
    IndexForm(
        17,
        "clamp_ops_range_inclusive",
        "core/src/index.rs:213-254",
        "unsafe impl<T> SliceIndex<[T]> for Clamp<ops::RangeInclusive<usize>>",
        (("a", 0), ("b", 9)),
    ),
    IndexForm(
        18,
        "clamp_range_range_from",
        "core/src/index.rs:256-285",
        "unsafe impl<T> SliceIndex<[T]> for Clamp<range::RangeFrom<usize>>",
        (("a", 9),),
    ),
    IndexForm(
        19,
        "clamp_ops_range_from",
        "core/src/index.rs:287-316",
        "unsafe impl<T> SliceIndex<[T]> for Clamp<ops::RangeFrom<usize>>",
        (("a", 2),),
    ),
    IndexForm(
        20,
        "clamp_ops_range_to",
        "core/src/index.rs:318-347",
        "unsafe impl<T> SliceIndex<[T]> for Clamp<ops::RangeTo<usize>>",
        (("b", 9),),
    ),
    IndexForm(
        21,
        "clamp_range_range_to_inclusive",
        "core/src/index.rs:349-378",
        "unsafe impl<T> SliceIndex<[T]> for Clamp<range::RangeToInclusive<usize>>",
        (("b", 9),),
    ),
    IndexForm(
        22,
        "clamp_ops_range_to_inclusive",
        "core/src/index.rs:380-409",
        "unsafe impl<T> SliceIndex<[T]> for Clamp<ops::RangeToInclusive<usize>>",
        (("b", 1),),
    ),
    IndexForm(
        23,
        "clamp_ops_range_full",
        "core/src/index.rs:411-440",
        "unsafe impl<T> SliceIndex<[T]> for Clamp<ops::RangeFull>",
    ),
    IndexForm(
        24,
        "last",
        "core/src/index.rs:442-472",
        "unsafe impl<T> SliceIndex<[T]> for Last",
    ),
)
INDEX_FORM_BY_NAME = {form.name: form for form in INDEX_FORMS}
if len(INDEX_FORMS) != 25 or len(INDEX_FORM_BY_NAME) != 25:
    raise RuntimeError("Rust 1.96 SliceIndex coverage must contain 25 unique forms")


@dataclass(frozen=True)
class SliceIndexTarget:
    target: str
    input_order: str
    artifact_id: str
    mode: str
    active_contract_sha256: str
    active_contract_text: str
    source_start: int
    source_end: int
    docs_start: int
    docs_end: int
    generated_declaration_sha256: str
    source_item_sha256: str
    public_docs_sha256: str
    harness_sha256: str
    source_body_manifest_sha256: str
    transformation_manifest_sha256: str
    dependency_manifest_sha256: str
    trust_record_sha256: tuple[tuple[str, str], ...]
    wrapper_fragment: str
    verus_expected_summary: str

    @property
    def mutable(self) -> bool:
        return self.mode in {"checked_mut", "unchecked_mut"}

    @property
    def option_return(self) -> bool:
        return self.mode == "checked_mut"

    @property
    def exhaustive_index_coverage(self) -> bool:
        return self.mode == "unchecked_shared"

    @property
    def source_reference(self) -> str:
        return f"core/src/slice/mod.rs:{self.source_start}-{self.source_end}"

    @property
    def docs_reference(self) -> str:
        return f"core/src/slice/mod.rs:{self.docs_start}-{self.docs_end}"

    @property
    def proof_filename(self) -> str:
        return f"proofs/{self.artifact_id}.rs"

    @property
    def context_only_trust_site_ids(self) -> tuple[str, ...]:
        return tuple(
            record_id
            for record_id, _ in self.trust_record_sha256
            if record_id.endswith("D002") and self.mode == "checked_mut"
            or record_id.endswith("D001") and self.mode != "checked_mut"
        )

    @property
    def excluded_trust_site_ids(self) -> tuple[str, ...]:
        context = set(self.context_only_trust_site_ids)
        return tuple(
            record_id
            for record_id, _ in self.trust_record_sha256
            if record_id not in context
        )

    @property
    def all_trust_site_ids(self) -> tuple[str, ...]:
        return tuple(record_id for record_id, _ in self.trust_record_sha256)

    @property
    def trust_hashes(self) -> dict[str, str]:
        return dict(self.trust_record_sha256)

    @property
    def replacement_id(self) -> str:
        scope = "SEALED-25" if self.exhaustive_index_coverage else "USIZE"
        return f"SRC-{int(self.input_order):03d}-{scope}-SLICEINDEX-TRANSITIONS"

    @property
    def expected_results(self) -> dict[str, str]:
        result = "unsat" if self.exhaustive_index_coverage else "sat"
        return {PRIMARY: result, EXACT_OUTPUT: result}

    @property
    def expected_classification(self) -> dict[str, str]:
        status = (
            "conditional-complete"
            if self.exhaustive_index_coverage
            else "conditional-incomplete"
        )
        return {
            "exact_output_determinism_status": status,
            "completeness_modulo_reviewed_equivalence_status": status,
        }

    @property
    def covered_forms(self) -> tuple[IndexForm, ...]:
        return INDEX_FORMS if self.exhaustive_index_coverage else (INDEX_FORMS[0],)


TARGETS = (
    SliceIndexTarget(
        target="core::slice::get_mut",
        input_order="53",
        artifact_id="053_core_slice_get_mut",
        mode="checked_mut",
        active_contract_sha256=(
            "87a9796fc553d16e3e75cfe5ea9196e6482c5088d278a2f10112c31107e74f9c"
        ),
        active_contract_text=(
            "#[verifier::allow(undeclared_external_trait)] pub "
            "assume_specification<T, I>[ <[T]>::get_mut::<I> ]( "
            "slice: &mut [T], index: I, ) -> (ret: Option<&mut <I as "
            "core::slice::SliceIndex<[T]>>::Output>) where I: "
            "core::slice::SliceIndex<[T]> ensures ret.is_some() ==> "
            "slice_index_in_range(old(slice)@, index) && "
            "slice_index_mut_frame(old(slice)@, index, final(slice)@), "
            "ret.is_none() ==> !slice_index_in_range(old(slice)@, index) "
            "&& final(slice)@ == old(slice)@, ;"
        ),
        source_start=599,
        source_end=604,
        docs_start=579,
        docs_end=593,
        generated_declaration_sha256=(
            "41421f57df7cb4f61d6bea7c800e58841f1a9d34d82f8f774eeb43af86a969be"
        ),
        source_item_sha256=(
            "003625b19b151e26497787859485cf0ed9d8f38382d73e69831cd5de64758914"
        ),
        public_docs_sha256=(
            "07087be0a99c93f7e1ccc10d2164815561dfb76efd8e71ef2d6789a536148ada"
        ),
        harness_sha256=(
            "5e3d402338b6ddae1c5a63ca63cb2f5744117e69bc24a44cc6af3e7a6d6bbefb"
        ),
        source_body_manifest_sha256=(
            "4c12125da5516ab4a7ced015488202eb45f6462ec7000c0c7a38377d528c181c"
        ),
        transformation_manifest_sha256=(
            "a40ce01d896db83d76c9d039a1c3582b484cdbbd9fbaa410ff199e726e8139b6"
        ),
        dependency_manifest_sha256=(
            "6365e1d82f67c32639c1b2fb4e78686459dfc19295620475ff02b9d7b37a7a5a"
        ),
        trust_record_sha256=(
            (
                "TS-053-D001",
                "9f0f21e3b8942b66278c703893edba4442e4c0f5d456923ecdca706e828e58b9",
            ),
            (
                "TS-053-D002",
                "af3370cb5631d5850e4950b278c13cd65c16996c11f580df82d345ab3ae6705d",
            ),
        ),
        wrapper_fragment="index.get_mut(self)",
        verus_expected_summary="verification results:: 2 verified, 0 errors",
    ),
    SliceIndexTarget(
        target="core::slice::get_unchecked",
        input_order="54",
        artifact_id="054_core_slice_get_unchecked",
        mode="unchecked_shared",
        active_contract_sha256=(
            "71eedef5ee0aa574329fe132e65757563db0764095f5cc5dbdf2911acc0b4aad"
        ),
        active_contract_text=(
            "#[verifier::allow(undeclared_external_trait)] pub "
            "assume_specification<T, I>[ <[T]>::get_unchecked::<I> ]( "
            "slice: &[T], index: I, ) -> (ret: &<I as "
            "core::slice::SliceIndex<[T]>>::Output) where I: "
            "core::slice::SliceIndex<[T]> requires "
            "slice_index_in_range(slice@, index), ensures "
            "slice_index_result(slice@, index, ret), ;"
        ),
        source_start=639,
        source_end=647,
        docs_start=606,
        docs_end=632,
        generated_declaration_sha256=(
            "f93d72dd895691f566537c1681aca5f533f719cb2526cf6964fc666f66b2eac6"
        ),
        source_item_sha256=(
            "52a8f107029603a78f11de9d849732deb57d722ee78dbe2ce36072a67108c3d5"
        ),
        public_docs_sha256=(
            "2fd06111933a67d4ee6ec2f170b5709bf7c3d2bf289cf386bc032784b845ec8e"
        ),
        harness_sha256=(
            "65e807c56cb36fd7aebd3df7af75b29b209126c18525a168d6d95acc5d2325e3"
        ),
        source_body_manifest_sha256=(
            "7cda15479addcda2aa198f0b6ddcdc7fcefde5d2024c8deb9138be564d7730fe"
        ),
        transformation_manifest_sha256=(
            "0ca04f5dd3f017593b2f79bc7fe53ca23a57254716983b321a7179b79b6ff399"
        ),
        dependency_manifest_sha256=(
            "24484e8fa9dbb959d039fa648abc0e4c9a59cfcf66a1cc3f91de0f54d1284bbd"
        ),
        trust_record_sha256=(
            (
                "TS-054-D001",
                "89af4cc1c94dbae86f81fb0f692d0a704e48c6940162a61aaec70ea68368397e",
            ),
            (
                "TS-054-D002",
                "06f9b7fc2d0602f0c897317cc44cecc971c750f75a981a2c7eb11e4932bb9fe7",
            ),
            (
                "TS-054-E001",
                "f940155561496fc0eb1a7878109148277d542050cd90ec0ae1d8f14b8f600775",
            ),
        ),
        wrapper_fragment="&*index.get_unchecked(self)",
        verus_expected_summary="verification results:: 2 verified, 0 errors",
    ),
    SliceIndexTarget(
        target="core::slice::get_unchecked_mut",
        input_order="55",
        artifact_id="055_core_slice_get_unchecked_mut",
        mode="unchecked_mut",
        active_contract_sha256=(
            "ec6f48bf7b072e49afdad4bacb69dc2288ec2047621c339df4614e01b612903f"
        ),
        active_contract_text=(
            "#[verifier::allow(undeclared_external_trait)] pub "
            "assume_specification<T, I>[ <[T]>::get_unchecked_mut::<I> ]( "
            "slice: &mut [T], index: I, ) -> (ret: &mut <I as "
            "core::slice::SliceIndex<[T]>>::Output) where I: "
            "core::slice::SliceIndex<[T]> requires "
            "slice_index_in_range(old(slice)@, index), ensures "
            "slice_index_mut_frame(old(slice)@, index, final(slice)@), ;"
        ),
        source_start=684,
        source_end=692,
        docs_start=649,
        docs_end=677,
        generated_declaration_sha256=(
            "fb3e735024d81a34f839d7c3296ddbb6a062c9a7e64e36fa5e3298192d4e56c8"
        ),
        source_item_sha256=(
            "feb16246768c2ac347ede8b95039570e3fddfb54257e2f8abadf710ff1c139e1"
        ),
        public_docs_sha256=(
            "86e45ec7b12d9faa3a366f0b81ea89b73d99bb1c4c642f98fca6ac8c2d69269e"
        ),
        harness_sha256=(
            "13fa4051014f02a4d4379442846250e3cc16c58394c6ec95ce4639c33e17019f"
        ),
        source_body_manifest_sha256=(
            "bcfcdce3f7ed26ccfaa2fa8d56dde4f8ffe3d2b2bf1d61ec24dc73cee817bd19"
        ),
        transformation_manifest_sha256=(
            "5017364c925cdc34680fb98bc0f65f88995af6204e858bce0de8ab1f38305457"
        ),
        dependency_manifest_sha256=(
            "b371862150ea2c1ed52e05ae1bf8a8cb809d31117f709adc6fef9db10881d871"
        ),
        trust_record_sha256=(
            (
                "TS-055-D001",
                "7a0bf077a7e5264ef70c66d65254d891d94fc6de3a27d2080c8ecb0698e47e79",
            ),
            (
                "TS-055-D002",
                "33795559b1669ff3d2a2536166ce298298566f3491a1223a30df665b962f0168",
            ),
            (
                "TS-055-E001",
                "7c83ba3b895e6f34b405b9d070da976893cc3a2bc16f5fb9f85151f44503c2b0",
            ),
        ),
        wrapper_fragment="&mut *index.get_unchecked_mut(self)",
        verus_expected_summary="verification results:: 2 verified, 0 errors",
    ),
)
TARGET_KEYS = tuple((config.target, config.input_order) for config in TARGETS)
TARGET_BY_ARTIFACT = {config.artifact_id: config for config in TARGETS}


INPUT_FIELDS = (
    ("x_length", "Int"),
    ("x_value0", "Int"),
    ("x_value1", "Int"),
    ("x_value2", "Int"),
    ("x_index_tag", "Int"),
    ("x_a", "Int"),
    ("x_b", "Int"),
    ("x_exhausted", "Bool"),
    ("x_start_bound_kind", "Int"),
    ("x_end_bound_kind", "Int"),
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
    ("b_value0", "Int", "input_memory"),
    ("b_value1", "Int", "input_memory"),
    ("b_value2", "Int", "input_memory"),
    ("b_allocation", "Int", "input_memory"),
    ("b_address", "Int", "input_memory"),
    ("b_provenance", "Int", "input_provenance"),
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
COMMON_OUTPUT_FIELDS = (
    ("y_kind", "Int"),
    ("y_start", "Int"),
    ("y_length", "Int"),
    ("y_allocation", "Int"),
    ("y_address", "Int"),
    ("y_provenance", "Int"),
    ("y_parent_borrow", "Int"),
    ("y_value0", "Int"),
    ("y_value1", "Int"),
    ("y_value2", "Int"),
)
STATE_FIELDS = (
    ("s_value0", "Int"),
    ("s_value1", "Int"),
    ("s_value2", "Int"),
    ("s_length", "Int"),
    ("s_allocation", "Int"),
    ("s_address", "Int"),
    ("s_provenance", "Int"),
    ("s_root_borrow", "Int"),
    ("s_element_size", "Int"),
    ("s_element_alignment", "Int"),
    ("s_alias_readers", "Int"),
    ("s_alias_writers", "Int"),
    ("s_frame_token", "Int"),
)


def canonical_json_sha256(value: Any) -> str:
    text = json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n"
    return hashlib.sha256(text.encode()).hexdigest()


def _output_fields(config: SliceIndexTarget) -> tuple[tuple[str, str], ...]:
    prefix = (("y_present", "Bool"),) if config.option_return else ()
    return (*prefix, *COMMON_OUTPUT_FIELDS)


def _datatype(name: str, constructor: str, fields: tuple[tuple[str, str], ...]) -> str:
    body = "\n".join(f"      ({selector} {sort})" for selector, sort in fields)
    return f"""\
(declare-datatypes (({name} 0))
  ((({constructor}
{body}))))"""


def _state_declaration(purpose: str) -> str:
    if purpose == EXACT_OUTPUT:
        return "(declare-datatypes ((State 0)) (((mkState))))"
    return _datatype("State", "mkState", STATE_FIELDS)


def _minimum(left: str, right: str) -> str:
    return f"(ite (<= {left} {right}) {left} {right})"


def _bound_start() -> str:
    return (
        "(ite (= (x_start_bound_kind x) 0) 0 "
        "(ite (= (x_start_bound_kind x) 1) (x_a x) (+ (x_a x) 1)))"
    )


def _bound_end() -> str:
    return (
        "(ite (= (x_end_bound_kind x) 0) (x_length x) "
        "(ite (= (x_end_bound_kind x) 1) (+ (x_b x) 1) (x_b x)))"
    )


def _form_semantics(form: IndexForm) -> tuple[bool, str, str, str]:
    a = "(x_a x)"
    b = "(x_b x)"
    length = "(x_length x)"
    last = "(- (x_length x) 1)"
    min_a_len = _minimum(a, length)
    min_b_len = _minimum(b, length)
    min_a_last = _minimum(a, last)
    min_b_last = _minimum(b, last)
    name = form.name
    if name == "usize":
        return True, a, f"(+ {a} 1)", f"(< {a} {length})"
    if name == "ops_index_range":
        return False, a, b, f"(and (<= {a} {b}) (<= {b} {length}))"
    if name in {"ops_range", "range_range"}:
        return False, a, b, f"(and (<= {a} {b}) (<= {b} {length}))"
    if name == "ops_range_to":
        return False, "0", b, f"(<= {b} {length})"
    if name in {"ops_range_from", "range_range_from"}:
        return False, a, length, f"(<= {a} {length})"
    if name == "ops_range_full":
        return False, "0", length, "true"
    if name == "ops_range_inclusive":
        start = f"(ite (x_exhausted x) (+ {b} 1) {a})"
        end = f"(+ {b} 1)"
        guard = (
            f"(and (< {b} {length}) "
            f"(or (x_exhausted x) (<= {a} {b})))"
        )
        return False, start, end, guard
    if name == "range_range_inclusive":
        return (
            False,
            a,
            f"(+ {b} 1)",
            f"(and (<= {a} {b}) (< {b} {length}))",
        )
    if name in {"ops_range_to_inclusive", "range_range_to_inclusive"}:
        return False, "0", f"(+ {b} 1)", f"(< {b} {length})"
    if name == "ops_bound_pair":
        start = _bound_start()
        end = _bound_end()
        guard = (
            "(and (<= 0 (x_start_bound_kind x)) "
            "(<= (x_start_bound_kind x) 2) "
            "(<= 0 (x_end_bound_kind x)) "
            "(<= (x_end_bound_kind x) 2) "
            "(=> (= (x_start_bound_kind x) 2) (< (x_a x) (x_usize_max x))) "
            "(=> (= (x_end_bound_kind x) 1) (< (x_b x) (x_usize_max x))) "
            f"(<= {start} {end}) (<= {end} {length}))"
        )
        return False, start, end, guard
    if name == "clamp_usize":
        start = min_a_last
        return True, start, f"(+ {start} 1)", f"(> {length} 0)"
    if name in {"clamp_range_range", "clamp_ops_range"}:
        return (
            False,
            min_a_len,
            min_b_len,
            f"(<= {min_a_len} {min_b_len})",
        )
    if name in {
        "clamp_range_range_inclusive",
        "clamp_ops_range_inclusive",
    }:
        return (
            False,
            min_a_last,
            f"(+ {min_b_last} 1)",
            f"(and (> {length} 0) (<= {min_a_last} {min_b_last}))",
        )
    if name in {"clamp_range_range_from", "clamp_ops_range_from"}:
        return False, min_a_len, length, "true"
    if name == "clamp_ops_range_to":
        return False, "0", min_b_len, "true"
    if name in {
        "clamp_range_range_to_inclusive",
        "clamp_ops_range_to_inclusive",
    }:
        return (
            False,
            "0",
            f"(+ {min_b_last} 1)",
            f"(> {length} 0)",
        )
    if name == "clamp_ops_range_full":
        return False, "0", length, "true"
    if name == "last":
        return True, last, length, f"(> {length} 0)"
    raise ValueError(f"unmodeled SliceIndex form: {name}")


def _tag_ite(values: list[str], default: str) -> str:
    result = default
    for form, value in reversed(list(zip(INDEX_FORMS, values))):
        result = f"(ite (= (x_index_tag x) {form.tag}) {value} {result})"
    return result


def _normalization_definitions() -> str:
    elements: list[str] = []
    starts: list[str] = []
    ends: list[str] = []
    guards: list[str] = []
    for form in INDEX_FORMS:
        element, start, end, guard = _form_semantics(form)
        elements.append("true" if element else "false")
        starts.append(start)
        ends.append(end)
        guards.append(guard)
    return f"""\
(define-fun SealedIndexKindCovered ((x Input)) Bool
  (and (<= 0 (x_index_tag x)) (< (x_index_tag x) {len(INDEX_FORMS)})))
(define-fun IsElementIndex ((x Input)) Bool
  {_tag_ite(elements, "false")})
(define-fun NormalizedStart ((x Input)) Int
  {_tag_ite(starts, "0")})
(define-fun NormalizedEnd ((x Input)) Int
  {_tag_ite(ends, "0")})
(define-fun IndexFormDomain ((x Input)) Bool
  {_tag_ite(guards, "false")})
(define-fun SliceIndexInRange ((x Input)) Bool
  (and (SealedIndexKindCovered x)
       (IndexFormDomain x)
       (<= 0 (NormalizedStart x))
       (<= (NormalizedStart x) (NormalizedEnd x))
       (<= (NormalizedEnd x) (x_length x))))
(define-fun NormalizedLength ((x Input)) Int
  (- (NormalizedEnd x) (NormalizedStart x)))"""


def _boundary_equalities() -> str:
    pairs = (
        ("b_value0", "x_value0"),
        ("b_value1", "x_value1"),
        ("b_value2", "x_value2"),
        ("b_allocation", "x_allocation"),
        ("b_address", "x_address"),
        ("b_provenance", "x_provenance"),
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
    return "\n       ".join(f"(= ({left} b) ({right} x))" for left, right in pairs)


def _output_constraints(config: SliceIndexTarget, canonical: bool) -> str:
    if canonical:
        start = "(NormalizedStart x)"
        length = "(NormalizedLength x)"
        kind = "(ite (IsElementIndex x) 0 1)"
    else:
        start = "(y_start y)"
        length = "1"
        kind = "0"
    present = (
        "       (= (y_present y) true)\n" if config.option_return else ""
    )
    return f"""\
{present}       (= (y_kind y) {kind})
       (= (y_start y) {start})
       (= (y_length y) {length})
       (= (y_allocation y) (x_allocation x))
       (= (y_address y)
          (ReturnAddress x {start}))
       (= (y_provenance y) (x_provenance x))
       (= (y_parent_borrow y) (x_root_borrow x))
       (= (y_value0 y)
          (ite (> {length} 0)
               (SliceValueAt x {start})
               0))
       (= (y_value1 y)
          (ite (> {length} 1)
               (SliceValueAt x (+ {start} 1))
               0))
       (= (y_value2 y)
          (ite (> {length} 2)
               (SliceValueAt x (+ {start} 2))
               0))"""


def _output_transition_name(config: SliceIndexTarget) -> str:
    if config.mode == "checked_mut":
        return "CheckedGetMutResultTransition"
    if config.mode == "unchecked_shared":
        return "SliceIndexResultTransition"
    return "UncheckedMutReferenceTransition"


def _frame_transition_name(config: SliceIndexTarget) -> str:
    return (
        "SliceIndexMutableFrameTransition"
        if config.mutable
        else "ImmutableReferenceFrameTransition"
    )


def _source_transition_names(
    config: SliceIndexTarget, purpose: str
) -> tuple[str, ...]:
    names = [_output_transition_name(config)]
    if purpose == PRIMARY:
        names.append(_frame_transition_name(config))
    return tuple(names)


def _state_constraints(config: SliceIndexTarget) -> str:
    identity = """\
       (= (s_length s) (x_length x))
       (= (s_allocation s) (x_allocation x))
       (= (s_address s) (x_address x))
       (= (s_provenance s) (x_provenance x))
       (= (s_root_borrow s) (x_root_borrow x))
       (= (s_element_size s) (x_element_size x))
       (= (s_element_alignment s) (x_element_alignment x))
       (= (s_alias_readers s) (x_alias_readers x))
       (= (s_alias_writers s) (x_alias_writers x))
       (= (s_frame_token s) (x_frame_token x))"""
    values: list[str] = []
    for index in range(3):
        if config.mutable:
            condition = (
                f"(not (and (< {index} (x_length x)) "
                f"(<= (NormalizedStart x) {index}) "
                f"(< {index} (NormalizedEnd x))))"
            )
            values.append(
                f"(=> {condition} (= (s_value{index} s) (x_value{index} x)))"
            )
        else:
            values.append(f"(= (s_value{index} s) (x_value{index} x))")
    return identity + "\n       " + "\n       ".join(values)


def _source_definitions(config: SliceIndexTarget, purpose: str) -> str:
    canonical_output = _output_constraints(config, canonical=True)
    active_output = _output_constraints(
        config, canonical=config.exhaustive_index_coverage
    )
    if not config.exhaustive_index_coverage:
        active_output = (
            "       (= (x_index_tag x) 0)\n"
            "       (<= 0 (y_start y))\n"
            "       (< (y_start y) (x_length x))\n"
            + active_output
        )
    output_name = _output_transition_name(config)
    result = f"""\
(define-fun SliceValueAt ((x Input) (index Int)) Int
  (ite (= index 0)
       (x_value0 x)
       (ite (= index 1) (x_value1 x) (x_value2 x))))
(define-fun ReturnAddress ((x Input) (start Int)) Int
  (+ (x_address x)
     (ite (= (x_element_size x) 0)
          0
          (* start (x_element_size x)))))
(define-fun CanonicalSliceIndexResult
  ((x Input) (b Boundary) (y Output)) Bool
  (and (SliceIndexInRange x)
{canonical_output}))
(define-fun {output_name}
  ((x Input) (b Boundary) (y Output)) Bool
  (and (SliceIndexInRange x)
{active_output}))
"""
    if purpose == PRIMARY:
        result += f"""\
(define-fun {_frame_transition_name(config)}
  ((x Input) (b Boundary) (s State)) Bool
  (and
{_state_constraints(config)}))
"""
    return result


def _requires_body(config: SliceIndexTarget) -> str:
    coverage = (
        "(SealedIndexKindCovered x)"
        if config.exhaustive_index_coverage
        else "(= (x_index_tag x) 0)"
    )
    alias = (
        "(and (= (x_alias_readers x) 0) (= (x_alias_writers x) 0))"
        if config.mutable
        else "(and (>= (x_alias_readers x) 0) (= (x_alias_writers x) 0))"
    )
    return f"""\
  (and (<= 0 (x_length x))
       (<= (x_length x) 3)
       {coverage}
       (<= 0 (x_a x))
       (<= (x_a x) (x_usize_max x))
       (<= 0 (x_b x))
       (<= (x_b x) (x_usize_max x))
       (SliceIndexInRange x)
       (> (x_allocation x) 0)
       (> (x_address x) 0)
       (> (x_provenance x) 0)
       (> (x_root_borrow x) 0)
       (x_single_allocation x)
       (<= 0 (x_allocation_base x))
       (<= 0 (x_allocation_bytes x))
       (<= 0 (x_element_size x))
       (> (x_element_alignment x) 0)
       (> (x_usize_max x) 0)
       (> (x_isize_max x) 0)
       (> (x_address_space_limit x) 0)
       (= (mod (x_address x) (x_element_alignment x)) 0)
       (or (= (x_element_size x) 0)
           (and (>= (x_element_size x) (x_element_alignment x))
                (= (mod (x_element_size x) (x_element_alignment x)) 0)))
       (<= (x_allocation_base x) (x_address x))
       (<= (+ (x_address x)
              (* (x_length x) (x_element_size x)))
           (+ (x_allocation_base x) (x_allocation_bytes x)))
       (<= (* (x_length x) (x_element_size x)) (x_isize_max x))
       (<= (+ (x_address x)
              (* (x_length x) (x_element_size x)))
           (x_address_space_limit x))
       {alias}
       (> (x_frame_token x) 0))"""


def _boundary_body() -> str:
    return f"""\
  (and (> (b_allocation b) 0)
       (> (b_address b) 0)
       (> (b_provenance b) 0)
       (> (b_root_borrow b) 0)
       (b_single_allocation b)
       (<= 0 (b_allocation_bytes b))
       (<= 0 (b_element_size b))
       (> (b_element_alignment b) 0)
       (> (b_usize_max b) 0)
       (> (b_isize_max b) 0)
       (> (b_address_space_limit b) 0)
       (> (b_frame_token b) 0)
       (InitialSliceObserved x b))"""


def _equivalence_body(
    config: SliceIndexTarget, purpose: str
) -> str:
    selectors = [selector for selector, _ in _output_fields(config)]
    equalities = [
        f"(= ({selector} y1) ({selector} y2))" for selector in selectors
    ]
    if purpose == PRIMARY:
        equalities.extend(
            f"(= ({selector} s1) ({selector} s2))"
            for selector, _ in STATE_FIELDS
        )
    return "  (and " + "\n       ".join(equalities) + "))"


def model_text(config: SliceIndexTarget, purpose: str) -> str:
    if purpose not in PURPOSES:
        raise ValueError(f"{config.target}: unknown obligation purpose {purpose}")
    input_decl = _datatype("Input", "mkInput", INPUT_FIELDS)
    boundary_decl = _datatype(
        "Boundary",
        "mkBoundary",
        tuple((selector, sort) for selector, sort, _ in BOUNDARY_FIELDS),
    )
    output_decl = _datatype("Output", "mkOutput", _output_fields(config))
    frame_call = (
        f"\n       ({_frame_transition_name(config)} x b s)"
        if purpose == PRIMARY
        else ""
    )
    return f"""\
; Target: {config.target}
; Active contract SHA-256: {config.active_contract_sha256}
; Purpose: {purpose}
; No opaque SliceIndex predicate is admitted. Target 054 normalizes every
; sealed Rust 1.96 implementation; targets 053 and 055 use a concrete usize
; witness and deliberately do not add the source-selected reference to Spec_T.
(set-logic ALL)
{input_decl}
{boundary_decl}
{output_decl}
{_state_declaration(purpose)}
(declare-const x Input)
(declare-const b Boundary)
(declare-const y1 Output)
(declare-const s1 State)
(declare-const y2 Output)
(declare-const s2 State)
{_normalization_definitions()}
(define-fun InitialSliceObserved ((x Input) (b Boundary)) Bool
  (and {_boundary_equalities()}))
{_source_definitions(config, purpose)}
(define-fun Requires_T ((x Input)) Bool
{_requires_body(config)})
(define-fun Boundary_T ((x Input) (b Boundary)) Bool
{_boundary_body()})
(define-fun TargetDefinition_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and (InitialSliceObserved x b)
       ({_output_transition_name(config)} x b y){frame_call}))
(define-fun Spec_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (TargetDefinition_T x b y s))
(define-fun Equivalent_T
  ((x Input) (b Boundary)
   (y1 Output) (s1 State) (y2 Output) (s2 State)) Bool
{_equivalence_body(config, purpose)}
"""


def obligation_text(config: SliceIndexTarget, purpose: str) -> str:
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
    config: SliceIndexTarget, purpose: str
) -> list[dict[str, str]]:
    result = [
        {
            "selector": selector,
            "left": "output1",
            "right": "output2",
            "sort": sort,
        }
        for selector, sort in _output_fields(config)
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


def _source_citations(config: SliceIndexTarget) -> list[str]:
    citations = [
        config.source_reference,
        config.docs_reference,
        "specs/slice_shared_vocabulary.rs:1130-1145",
        INDEX_FORMS[0].source_reference,
    ]
    if config.exhaustive_index_coverage:
        citations.extend(
            [SLICE_INDEX_SOURCE, INDEX_WRAPPER_SOURCE]
        )
    return citations


def obligation_metadata(
    config: SliceIndexTarget, purpose: str
) -> dict[str, Any]:
    transitions = list(_source_transition_names(config, purpose))
    citations = _source_citations(config)
    coverage = [form.name for form in config.covered_forms]
    output_policy = (
        "The concrete usize result is required only to be a valid returned "
        "reference. The source-selected element is retained as a diagnostic "
        "transition and is not conjoined to Spec_T."
        if config.mutable
        else "The opaque slice_index_result predicate is faithfully expanded "
        "by the complete 25-form sealed SliceIndex normalization."
    )
    return {
        "schema_version": 3,
        "target": config.target,
        "input_order": config.input_order,
        "obligation_purpose": purpose,
        "active_contract_sha256": config.active_contract_sha256,
        "active_contract_text": config.active_contract_text,
        "target_definition": "TargetDefinition_T",
        "theorem_variables": {
            "input": "x",
            "boundary": "b",
            "output1": "y1",
            "state1": "s1",
            "output2": "y2",
            "state2": "s2",
        },
        "domain": {
            "bounded": True,
            "slice_length": "zero through three",
            "index_coverage": coverage,
            "source_model_complete": True,
            "layout": (
                "positive aligned address, nonnegative element size including "
                "ZST, one allocation, isize fit, and no address wrap"
            ),
            "mutable_aliasing": (
                "exclusive root borrow" if config.mutable else "shared readers only"
            ),
        },
        "model_status": "source-backed-complete",
        "contract_translation": {
            "opaque_vocabulary_policy": (
                "No uninterpreted SMT declaration is retained. Bounds, result, "
                "and mutable-frame predicates are expanded into readable "
                "source-backed definitions."
            ),
            "implementation_choice_exclusion": output_policy,
        },
        "boundary_scope": {
            "shared_observations": [
                "initial receiver values",
                "initial allocation, address, provenance, and root borrow identity",
                "element layout and platform pointer limits",
                "alias permissions and pre-existing outside-memory frame token",
            ],
            "excluded_observations": [
                "returned reference or option discriminant",
                "normalized or selected index result",
                "final receiver values",
                "canonical answer or target truth",
                "raw pointer result",
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
        "boundary_fields": [
            {
                "selector": selector,
                "role": role,
                "source_citations": citations,
                "trust_site_ids": [],
                "source_backed_replacement_ids": [config.replacement_id],
            }
            for selector, _, role in BOUNDARY_FIELDS
        ],
        "declared_functions": [],
        "source_transition_definitions": transitions,
        "source_backed_replacements": [
            {
                "replacement_id": config.replacement_id,
                "operation": (
                    "SliceIndex bounds decision, raw pointer address/provenance "
                    "transition, dereference/reference well-formedness, borrow "
                    "identity, and mutable or immutable frame"
                ),
                "symbols": transitions,
                "replaces_trust_site_ids": list(
                    config.excluded_trust_site_ids
                ),
                "source_citations": citations,
            }
        ],
        "unresolved_source_model_trust_site_ids": [],
        "sealed_sliceindex_coverage": [
            {
                "tag": form.tag,
                "name": form.name,
                "source_reference": form.source_reference,
            }
            for form in config.covered_forms
        ],
        "equivalence_kind": "exact",
        "equivalence_scope": (
            "every returned-reference field and every modeled final receiver/frame field"
            if purpose == PRIMARY
            else "every returned-reference field"
        ),
        "principal_observations": _principal_observations(config, purpose),
        "expected_solver_result": config.expected_results[purpose],
    }


def obligation(
    config: SliceIndexTarget, purpose: str
) -> tuple[str, dict[str, Any]]:
    return obligation_text(config, purpose), obligation_metadata(config, purpose)


def validate_target_obligation(
    config: SliceIndexTarget,
    text: str,
    metadata: dict[str, Any],
) -> None:
    validate_obligation(text, metadata)
    purpose = metadata.get("obligation_purpose")
    if purpose not in PURPOSES:
        raise GuardError(f"{config.target}: unknown obligation purpose")
    expected_text, expected_metadata = obligation(config, str(purpose))
    if metadata != expected_metadata:
        raise GuardError(f"{config.target}: obligation metadata changed")
    if parse_smt(text) != parse_smt(expected_text):
        raise GuardError(f"{config.target}: obligation SMT changed")
    if "(declare-fun" in text:
        raise GuardError(f"{config.target}: opaque SMT function is prohibited")
    target_body = text[
        text.index("(define-fun TargetDefinition_T"):
        text.index("(define-fun Spec_T")
    ]
    if config.mutable and "CanonicalSliceIndexResult" in target_body:
        raise GuardError(
            f"{config.target}: source-selected output was injected into Spec_T"
        )
    coverage = metadata.get("sealed_sliceindex_coverage")
    expected_coverage = [
        {
            "tag": form.tag,
            "name": form.name,
            "source_reference": form.source_reference,
        }
        for form in config.covered_forms
    ]
    if coverage != expected_coverage:
        raise GuardError(f"{config.target}: SliceIndex coverage changed")


def validate_source_anchors(
    config: SliceIndexTarget,
    source_item: str,
    public_docs: str,
    vocabulary: str,
    slice_index_source: str,
    index_wrapper_source: str,
) -> None:
    required = (
        config.wrapper_fragment,
        "I: [const] SliceIndex<Self>",
    )
    if any(fragment not in source_item for fragment in required):
        raise GuardError(f"{config.target}: public wrapper source changed")
    if config.mode != "checked_mut" and (
        "out-of-bounds index is *[undefined behavior]*" not in public_docs
        or "even if the resulting reference is not used" not in public_docs
    ):
        raise GuardError(f"{config.target}: public safety documentation changed")
    vocabulary_fragments = (
        "pub uninterp spec fn slice_index_in_range",
        "pub uninterp spec fn slice_index_result",
        "pub uninterp spec fn slice_index_mut_frame",
    )
    if any(fragment not in vocabulary for fragment in vocabulary_fragments):
        raise GuardError(f"{config.target}: SliceIndex vocabulary changed")
    if "pub open spec fn slice_index_" in vocabulary:
        raise GuardError(f"{config.target}: opaque vocabulary was silently defined")
    combined = slice_index_source + "\n" + index_wrapper_source
    for form in config.covered_forms:
        if form.anchor not in combined:
            raise GuardError(
                f"{config.target}: missing sealed implementation {form.name}"
            )
    if "pub const unsafe trait SliceIndex" not in slice_index_source:
        raise GuardError(f"{config.target}: SliceIndex trait declaration changed")
    if "external_body" in combined:
        raise GuardError(f"{config.target}: canonical Rust source is opaque")


def _sample_record(form: IndexForm | None = None) -> dict[str, int | bool]:
    values: dict[str, int | bool] = {
        "length": 3,
        "value0": 10,
        "value1": 20,
        "value2": 30,
        "index_tag": 0,
        "a": 0,
        "b": 2,
        "exhausted": False,
        "start_bound_kind": 1,
        "end_bound_kind": 2,
        "allocation": 41,
        "address": 4096,
        "provenance": 141,
        "root_borrow": 241,
        "single_allocation": True,
        "allocation_base": 4096,
        "allocation_bytes": 256,
        "element_size": 4,
        "element_alignment": 4,
        "usize_max": 4_294_967_295,
        "isize_max": 2_147_483_647,
        "address_space_limit": 4_294_967_295,
        "alias_readers": 0,
        "alias_writers": 0,
        "frame_token": 777,
    }
    if form is not None:
        values["index_tag"] = form.tag
        values.update(form.sample_values)
    return values


def _smt_atom(value: int | bool) -> str:
    if value is True:
        return "true"
    if value is False:
        return "false"
    return str(value)


def _input_expression(values: dict[str, int | bool]) -> str:
    ordered = [
        values[selector.removeprefix("x_")] for selector, _ in INPUT_FIELDS
    ]
    return "(mkInput " + " ".join(_smt_atom(value) for value in ordered) + ")"


def _boundary_expression(values: dict[str, int | bool]) -> str:
    ordered = [
        values[selector.removeprefix("b_")]
        for selector, _, _ in BOUNDARY_FIELDS
    ]
    return "(mkBoundary " + " ".join(_smt_atom(value) for value in ordered) + ")"


def _resolve_sample(values: dict[str, int | bool]) -> tuple[bool, int, int]:
    tag = int(values["index_tag"])
    length = int(values["length"])
    a = int(values["a"])
    b = int(values["b"])
    exhausted = bool(values["exhausted"])
    start_kind = int(values["start_bound_kind"])
    end_kind = int(values["end_bound_kind"])
    if tag == 0:
        return True, a, a + 1
    if tag in {1, 2, 3}:
        return False, a, b
    if tag == 4:
        return False, 0, b
    if tag in {5, 6}:
        return False, a, length
    if tag == 7:
        return False, 0, length
    if tag == 8:
        return False, b + 1 if exhausted else a, b + 1
    if tag == 9:
        return False, a, b + 1
    if tag in {10, 11}:
        return False, 0, b + 1
    if tag == 12:
        start = 0 if start_kind == 0 else a + (start_kind == 2)
        end = length if end_kind == 0 else b + (end_kind == 1)
        return False, int(start), int(end)
    if tag == 13:
        start = min(a, length - 1)
        return True, start, start + 1
    if tag in {14, 15}:
        return False, min(a, length), min(b, length)
    if tag in {16, 17}:
        return False, min(a, length - 1), min(b, length - 1) + 1
    if tag in {18, 19}:
        return False, min(a, length), length
    if tag == 20:
        return False, 0, min(b, length)
    if tag in {21, 22}:
        return False, 0, min(b, length - 1) + 1
    if tag == 23:
        return False, 0, length
    if tag == 24:
        return True, length - 1, length
    raise ValueError(f"unknown sample SliceIndex tag: {tag}")


def _output_expression(
    config: SliceIndexTarget,
    values: dict[str, int | bool],
    *,
    start: int,
    end: int,
    element: bool,
    address_delta: int = 0,
    provenance_delta: int = 0,
) -> str:
    sequence = [int(values[f"value{index}"]) for index in range(3)]
    returned = sequence[start:end]
    padded = [*returned, 0, 0, 0][:3]
    size = int(values["element_size"])
    address = int(values["address"]) + (0 if size == 0 else start * size)
    fields: list[int | bool] = []
    if config.option_return:
        fields.append(True)
    fields.extend(
        [
            0 if element else 1,
            start,
            end - start,
            int(values["allocation"]),
            address + address_delta,
            int(values["provenance"]) + provenance_delta,
            int(values["root_borrow"]),
            *padded,
        ]
    )
    return "(mkOutput " + " ".join(_smt_atom(value) for value in fields) + ")"


def _state_expression(values: dict[str, int | bool], final: list[int] | None = None) -> str:
    sequence = final or [int(values[f"value{index}"]) for index in range(3)]
    fields: list[int | bool] = [
        *sequence,
        int(values["length"]),
        int(values["allocation"]),
        int(values["address"]),
        int(values["provenance"]),
        int(values["root_borrow"]),
        int(values["element_size"]),
        int(values["element_alignment"]),
        int(values["alias_readers"]),
        int(values["alias_writers"]),
        int(values["frame_token"]),
    ]
    return "(mkState " + " ".join(_smt_atom(value) for value in fields) + ")"


def source_cases(config: SliceIndexTarget) -> dict[str, IndexForm]:
    return {form.name: form for form in config.covered_forms}


def source_instance_text(config: SliceIndexTarget, name: str) -> str:
    try:
        form = source_cases(config)[name]
    except KeyError as exc:
        raise ValueError(f"{config.target}: unknown source case {name}") from exc
    values = _sample_record(form)
    element, start, end = _resolve_sample(values)
    output = _output_expression(
        config, values, start=start, end=end, element=element
    )
    return model_text(config, PRIMARY) + f"""\
(assert (= x {_input_expression(values)}))
(assert (= b {_boundary_expression(values)}))
(assert (= y1 {output}))
(assert (= s1 {_state_expression(values)}))
(assert (Requires_T x))
(assert (Boundary_T x b))
(assert (CanonicalSliceIndexResult x b y1))
(assert ({_frame_transition_name(config)} x b s1))
(check-sat)
(get-value (
  (x_index_tag x)
  (NormalizedStart x)
  (NormalizedEnd x)
  (y_kind y1)
  (y_start y1)
  (y_length y1)
  (y_address y1)
  (y_provenance y1)))
"""


def witness_payload(config: SliceIndexTarget) -> dict[str, Any]:
    if not config.mutable:
        raise ValueError(f"{config.target}: no incompleteness witness is expected")
    values = _sample_record(INDEX_FORMS[0])
    values["a"] = 0
    boundary = {
        key: values[key]
        for key in (
            "value0",
            "value1",
            "value2",
            "allocation",
            "address",
            "provenance",
            "root_borrow",
            "single_allocation",
            "allocation_base",
            "allocation_bytes",
            "element_size",
            "element_alignment",
            "usize_max",
            "isize_max",
            "address_space_limit",
            "alias_readers",
            "alias_writers",
            "frame_token",
        )
    }

    def reference(index: int) -> dict[str, Any]:
        return {
            "present": True if config.option_return else None,
            "kind": "element",
            "index": index,
            "length": 1,
            "allocation": values["allocation"],
            "address": int(values["address"])
            + index * int(values["element_size"]),
            "provenance": values["provenance"],
            "parent_borrow": values["root_borrow"],
            "value": values[f"value{index}"],
        }

    state = {
        "values": [values["value0"], values["value1"], values["value2"]],
        "length": values["length"],
        "allocation": values["allocation"],
        "address": values["address"],
        "provenance": values["provenance"],
        "root_borrow": values["root_borrow"],
        "element_size": values["element_size"],
        "element_alignment": values["element_alignment"],
        "alias_readers": values["alias_readers"],
        "alias_writers": values["alias_writers"],
        "frame_token": values["frame_token"],
    }
    return {
        "schema_version": 1,
        "target": config.target,
        "input_order": config.input_order,
        "active_contract_sha256": config.active_contract_sha256,
        "case": "usize_index_zero_distinct_valid_returned_references",
        "input": {
            **values,
            "index_form": "usize",
        },
        "boundary": boundary,
        "source_result": reference(0),
        "execution1": {"result": reference(0), "final_state": state},
        "execution2": {"result": reference(1), "final_state": state},
        "expected": {
            "requires_holds": True,
            "shared_boundary": True,
            "source_result_is_execution1": True,
            "source_result_is_execution2": False,
            "execution1_reference_well_formed": True,
            "execution2_reference_well_formed": True,
            "execution1_satisfies_active_contract": True,
            "execution2_satisfies_active_contract": True,
            "exact_output_equal": False,
            "exact_final_state_equal": True,
            "full_exact_equivalent": False,
        },
    }


def fixed_witness_text(config: SliceIndexTarget) -> str:
    if not config.mutable:
        raise ValueError(f"{config.target}: no incompleteness witness is expected")
    values = _sample_record(INDEX_FORMS[0])
    values["a"] = 0
    output1 = _output_expression(
        config, values, start=0, end=1, element=True
    )
    output2 = _output_expression(
        config, values, start=1, end=2, element=True
    )
    state = _state_expression(values)
    return model_text(config, PRIMARY) + f"""\
(assert (= x {_input_expression(values)}))
(assert (= b {_boundary_expression(values)}))
(assert (= y1 {output1}))
(assert (= s1 {state}))
(assert (= y2 {output2}))
(assert (= s2 {state}))
(assert (Requires_T x))
(assert (Boundary_T x b))
(assert (Spec_T x b y1 s1))
(assert (Spec_T x b y2 s2))
(assert (CanonicalSliceIndexResult x b y1))
(assert (not (CanonicalSliceIndexResult x b y2)))
(assert (not (Equivalent_T x b y1 s1 y2 s2)))
(check-sat)
(get-value (
  (NormalizedStart x)
  (y_start y1)
  (y_start y2)
  (y_address y1)
  (y_address y2)
  (y_provenance y1)
  (y_provenance y2)
  (Equivalent_T x b y1 s1 y2 s2)))
"""


def negative_probe_names(config: SliceIndexTarget) -> tuple[str, ...]:
    common = (
        "out_of_bounds_input",
        "wrong_pointer_address",
        "wrong_provenance",
    )
    return (
        (*common, "outside_mutable_frame")
        if config.mutable
        else (*common, "wrong_normalized_reference")
    )


def negative_probe_text(config: SliceIndexTarget, name: str) -> str:
    if name not in negative_probe_names(config):
        raise ValueError(f"{config.target}: unknown negative probe {name}")
    values = _sample_record(INDEX_FORMS[0])
    values["a"] = 0
    element, start, end = _resolve_sample(values)
    state_values: list[int] | None = None
    address_delta = 0
    provenance_delta = 0
    if name == "out_of_bounds_input":
        values["a"] = values["length"]
    elif name == "wrong_pointer_address":
        address_delta = int(values["element_size"]) or 1
    elif name == "wrong_provenance":
        provenance_delta = 1
    elif name == "outside_mutable_frame":
        state_values = [10, 20, 31]
    elif name == "wrong_normalized_reference":
        start, end = 1, 2
    output = _output_expression(
        config,
        values,
        start=start,
        end=end,
        element=element,
        address_delta=address_delta,
        provenance_delta=provenance_delta,
    )
    return model_text(config, PRIMARY) + f"""\
(assert (= x {_input_expression(values)}))
(assert (= b {_boundary_expression(values)}))
(assert (= y1 {output}))
(assert (= s1 {_state_expression(values, state_values)}))
(assert (Requires_T x))
(assert (Boundary_T x b))
(assert (Spec_T x b y1 s1))
(check-sat)
"""


def boundary_manifest(config: SliceIndexTarget) -> dict[str, Any]:
    coverage = [
        {
            "tag": form.tag,
            "name": form.name,
            "source_reference": form.source_reference,
            "source_anchor": form.anchor,
        }
        for form in config.covered_forms
    ]
    return {
        "schema_version": 1,
        "target": config.target,
        "input_order": config.input_order,
        "active_contract_sha256": config.active_contract_sha256,
        "boundary_narrower_than_target": True,
        "shared_boundary_observations": [
            {
                "fields": ["b_value0", "b_value1", "b_value2"],
                "kind": "initial receiver memory",
                "source_backed_replacement_ids": [config.replacement_id],
            },
            {
                "fields": [
                    "b_allocation",
                    "b_address",
                    "b_provenance",
                    "b_root_borrow",
                    "b_single_allocation",
                    "b_allocation_base",
                    "b_allocation_bytes",
                ],
                "kind": "initial allocation, address, provenance, and borrow identity",
                "source_backed_replacement_ids": [config.replacement_id],
            },
            {
                "fields": [
                    "b_element_size",
                    "b_element_alignment",
                    "b_usize_max",
                    "b_isize_max",
                    "b_address_space_limit",
                ],
                "kind": "element layout and platform pointer limits",
                "source_backed_replacement_ids": [config.replacement_id],
            },
            {
                "fields": [
                    "b_alias_readers",
                    "b_alias_writers",
                    "b_frame_token",
                ],
                "kind": "initial alias permissions and outside-memory frame",
                "source_backed_replacement_ids": [config.replacement_id],
            },
        ],
        "forbidden_boundary_observations": [
            "returned reference",
            "option result",
            "selected or normalized index",
            "raw pointer result",
            "final receiver memory",
            "canonical answer",
            "target truth",
            "execution trace",
        ],
        "source_backed_replacement": {
            "replacement_id": config.replacement_id,
            "replaces_trust_site_ids": list(config.excluded_trust_site_ids),
            "source_citations": _source_citations(config),
            "transitions": [
                "bounds decision",
                "pointer offset and raw output pointer construction",
                "allocation/address/provenance preservation",
                "reference dereference and well-formedness",
                "root-borrow identity",
                "mutable selected-range frame or immutable no-mutation frame",
            ],
        },
        "sealed_sliceindex_coverage": coverage,
        "coverage_complete_for_claim": True,
        "spec_relation_policy": (
            "Target 054 expands slice_index_result through every sealed Rust "
            "1.96 implementation. Targets 053 and 055 expand bounds and mutable "
            "frame semantics for a concrete usize instantiation, but preserve "
            "the active contracts' omission of returned-reference identity."
        ),
        "admitted_retained_trust_site_ids": [],
        "context_only_trust_site_ids": list(
            config.context_only_trust_site_ids
        ),
        "excluded_retained_trust_site_ids": list(
            config.excluded_trust_site_ids
        ),
        "all_audited_trust_site_ids": list(config.all_trust_site_ids),
    }
