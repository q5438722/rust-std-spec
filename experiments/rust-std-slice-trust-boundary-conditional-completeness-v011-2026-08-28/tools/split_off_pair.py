#!/usr/bin/env python3
"""Source-backed two-execution obligations for Slice split_off targets."""

from __future__ import annotations

import hashlib
import json
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
VOCABULARY_RANGES = ((879, 885),)
MAX_USIZE = 18446744073709551615
EMPTY_SEQ = "(as seq.empty (Seq Int))"

START_INCLUSIVE = 0
END = 1
END_INCLUSIVE = 2
FRONT = 0
BACK = 1


@dataclass(frozen=True)
class CanonicalSource:
    name: str
    start: int
    end: int
    filename: str
    fragments: tuple[str, ...]

    @property
    def path(self) -> str:
        return SLICE_SOURCE_PATH

    @property
    def file_sha256(self) -> str:
        return SLICE_SOURCE_SHA256

    @property
    def reference(self) -> str:
        return f"{self.path}:{self.start}-{self.end}"


CANONICAL_SOURCES = {
    source.name: source
    for source in (
        CanonicalSource(
            "split_point_of",
            80,
            99,
            "canonical_split_point_of.rs",
            (
                "(StartInclusive, i) => (Direction::Back, i)",
                "(End, i) => (Direction::Front, i)",
                "(EndInclusive, i) => (Direction::Front, i.checked_add(1)?)",
            ),
        ),
        CanonicalSource(
            "slice_as_ptr",
            720,
            728,
            "canonical_slice_as_ptr.rs",
            ("self as *const [T] as *const T",),
        ),
        CanonicalSource(
            "slice_as_mut_ptr",
            751,
            759,
            "canonical_slice_as_mut_ptr.rs",
            ("self as *mut [T] as *mut T",),
        ),
        CanonicalSource(
            "slice_split_at",
            1947,
            1957,
            "canonical_slice_split_at.rs",
            (
                "pub const fn split_at(&self, mid: usize)",
                "self.split_at_checked(mid)",
                'None => panic!("mid > len")',
            ),
        ),
        CanonicalSource(
            "slice_split_at_unchecked",
            2033,
            2054,
            "canonical_slice_split_at_unchecked.rs",
            (
                "let len = self.len()",
                "let ptr = self.as_ptr()",
                "(mid: usize = mid, len: usize = len) => mid <= len",
                "from_raw_parts(ptr, mid)",
                "from_raw_parts(ptr.add(mid), unchecked_sub(len, mid))",
            ),
        ),
        CanonicalSource(
            "slice_split_at_mut",
            1981,
            1991,
            "canonical_slice_split_at_mut.rs",
            (
                "pub const fn split_at_mut(&mut self, mid: usize)",
                "self.split_at_mut_checked(mid)",
                'None => panic!("mid > len")',
            ),
        ),
        CanonicalSource(
            "slice_split_at_mut_unchecked",
            2087,
            2112,
            "canonical_slice_split_at_mut_unchecked.rs",
            (
                "let len = self.len()",
                "let ptr = self.as_mut_ptr()",
                "(mid: usize = mid, len: usize = len) => mid <= len",
                "from_raw_parts_mut(ptr, mid)",
                "from_raw_parts_mut(ptr.add(mid), unchecked_sub(len, mid))",
            ),
        ),
    )
}


@dataclass(frozen=True)
class SourceReplacement:
    replacement_id: str
    operation: str
    symbols: tuple[str, ...]
    replaces_trust_site_ids: tuple[str, ...]


@dataclass(frozen=True)
class SplitOffTarget:
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
    context_only_trust_site_ids: tuple[str, ...]
    helper_names: tuple[str, ...]
    source_fragments: tuple[str, ...]
    source_backed_replacements: tuple[SourceReplacement, ...]

    @property
    def function_name(self) -> str:
        return self.target.rsplit("::", 1)[-1]

    @property
    def source_reference(self) -> str:
        return f"{SLICE_SOURCE_PATH}:{self.source_start}-{self.source_end}"

    @property
    def docs_reference(self) -> str:
        return f"{SLICE_SOURCE_PATH}:{self.docs_start}-{self.docs_end}"

    @property
    def all_trust_site_ids(self) -> tuple[str, ...]:
        return tuple(record_id for record_id, _ in self.trust_record_sha256)

    @property
    def trust_hashes(self) -> dict[str, str]:
        return dict(self.trust_record_sha256)

    @property
    def excluded_trust_site_ids(self) -> tuple[str, ...]:
        context = set(self.context_only_trust_site_ids)
        return tuple(
            site for site in self.all_trust_site_ids if site not in context
        )

    @property
    def helper_sources(self) -> tuple[CanonicalSource, ...]:
        return tuple(CANONICAL_SOURCES[name] for name in self.helper_names)

    @property
    def replacement_ids(self) -> tuple[str, ...]:
        return tuple(item.replacement_id for item in self.source_backed_replacements)

    @property
    def source_citations(self) -> tuple[str, ...]:
        return tuple(
            dict.fromkeys(
                (
                    self.source_reference,
                    self.docs_reference,
                    *(source.reference for source in self.helper_sources),
                )
            )
        )

    @property
    def active_conjuncts(self) -> tuple[str, ...]:
        common = (
            "ActiveNoneFrameConjunct",
            "ActiveInitialReturnPartitionConjunct",
        )
        if self.mutable:
            return (*common, "ActiveFinalReturnPartitionConjunct")
        return common


TARGETS = (
    SplitOffTarget(
        target="core::slice::split_off",
        input_order="99",
        artifact_id="099_core_slice_split_off",
        mutable=False,
        active_contract_sha256=(
            "980c0fc48d42c16666be982fb8949777aea4c339d73a52ba80f62fded2ae7085"
        ),
        active_contract_text=(
            "pub assume_specification<'a, T, R: core::ops::OneSidedRange<usize>>"
            "[ <[T]>::split_off::<R> ]( slice_ref: &mut &'a [T], range: R, ) "
            "-> (ret: Option<&'a [T]>) ensures ret.is_none() ==> "
            "(*final(slice_ref))@ == (*old(slice_ref))@, ret.is_some() ==> "
            "slice_split_off_partition::<T>( (*old(slice_ref))@, "
            "(*final(slice_ref))@, ret.unwrap()@, ), ;"
        ),
        source_start=4906,
        source_end=4925,
        docs_start=4861,
        docs_end=4902,
        source_item_sha256=(
            "fb19cd4b355c594bef6afbe10c0e9b9fc58e5aca2904b0b2038c4bf72df4768a"
        ),
        generated_declaration_sha256=(
            "1da2b681288110d4feed06d70d3cb9083c757b1601f526158e1bfcb52c847167"
        ),
        harness_sha256=(
            "d8a5f9a6474961b9f59339ca207d11a7f2eab997e73ebf60c5add4e62d83b59c"
        ),
        source_body_manifest_sha256=(
            "418eb8bf8eda909c1d41102acde92f49a7c9c63be803154bb64b028f5106bc3e"
        ),
        transformation_manifest_sha256=(
            "f18016d21450901b13f3289003d1cd708316fb7abfb6db39d92e669bfa7fbafe"
        ),
        dependency_manifest_sha256=(
            "546a89b7305989b545499403bad79954a37803ce773307bf8cea7c2601d7e5fe"
        ),
        trust_record_sha256=(
            (
                "TS-099-D001",
                "930b0787546f76f7cf96cafec7c1db449f74bd4fdab6238d2d66b718f6f80ffc",
            ),
            (
                "TS-099-D002",
                "b7791ff838cf4b4ff7f30c719a871725fc8bd7b8bdc80c0ecb38739e1bec6705",
            ),
            (
                "TS-099-D003",
                "0e69f6c879dfc996be1d33ad119b3b36d043398c80fa362349d3a61ec43a0220",
            ),
            (
                "TS-099-C001",
                "e03839d092822cbf022b54ada9ce1e6298ac58e89b8a4ec2121dc7363aeed479",
            ),
        ),
        context_only_trust_site_ids=("TS-099-D003", "TS-099-C001"),
        helper_names=(
            "split_point_of",
            "slice_as_ptr",
            "slice_split_at",
            "slice_split_at_unchecked",
        ),
        source_fragments=(
            "let (direction, split_index) = split_point_of(range)?",
            "if split_index > self.len()",
            "let (front, back) = self.split_at(split_index)",
            "Direction::Front",
            "*self = back",
            "Some(front)",
            "Direction::Back",
            "*self = front",
            "Some(back)",
        ),
        source_backed_replacements=(
            SourceReplacement(
                "SRC-099-SPLIT-POINT",
                (
                    "StartInclusive-to-Back, End-to-Front, and EndInclusive "
                    "checked-add split-point transition"
                ),
                ("SplitPointTransition",),
                ("TS-099-D001",),
            ),
            SourceReplacement(
                "SRC-099-IMMUTABLE-SPLIT",
                (
                    "bounds rejection, exact front/back regions, directional "
                    "receiver reassignment, returned shared-reference identity, "
                    "and unchanged ordered frame"
                ),
                (
                    "BoundsTransition",
                    "SplitRegionsTransition",
                    "DirectionalReturnTransition",
                    "BorrowCompositionTransition",
                    "FinalFrameTransition",
                ),
                ("TS-099-D002",),
            ),
        ),
    ),
    SplitOffTarget(
        target="core::slice::split_off_mut",
        input_order="104",
        artifact_id="104_core_slice_split_off_mut",
        mutable=True,
        active_contract_sha256=(
            "74829510395c909f4449ed0dd06a0ac44332151e2a9d1feba392c5728e616e99"
        ),
        active_contract_text=(
            "pub assume_specification<'a, T, R: core::ops::OneSidedRange<usize>>"
            "[ <[T]>::split_off_mut::<R> ]( slice_ref: &mut &'a mut [T], "
            "range: R, ) -> (ret: Option<&'a mut [T]>) ensures ret.is_none() "
            "==> (*final(slice_ref))@ == (*old(slice_ref))@, ret.is_some() "
            "==> slice_split_off_partition::<T>( (*old(slice_ref))@, "
            "(*final(slice_ref))@, ret.unwrap()@, ), ret.is_some() ==> "
            "slice_split_off_partition::<T>( (*old(slice_ref))@, "
            "(*final(slice_ref))@, final(ret.unwrap())@, ), ;"
        ),
        source_start=4972,
        source_end=4991,
        docs_start=4927,
        docs_end=4968,
        source_item_sha256=(
            "e1678d19e42198d5c9fc2b61a072aa4dbc114905a60b0f55a3b44bfe37429d46"
        ),
        generated_declaration_sha256=(
            "1e2f6a1761d197ceb678cc9b694124b1ffeda4bbb3649bd48a298c5e6224b1e6"
        ),
        harness_sha256=(
            "870bb881b247e42e6e40071061eaeac4a94b5cf7408ba7229c54126ef87a27b0"
        ),
        source_body_manifest_sha256=(
            "1cddd1d3aa5758b53efd1b3b7933c07fec2276bd22c01180b7838101456226c8"
        ),
        transformation_manifest_sha256=(
            "a954a8bd48a0455bcaa5ef9e0cc2cfa0384ff804144b273f6742c2a7fc41601c"
        ),
        dependency_manifest_sha256=(
            "323bc29843b2a8e6e205da191f1fed7906e825483705c7fc72ab71136265cfd9"
        ),
        trust_record_sha256=(
            (
                "TS-104-D001",
                "53cc836482cf83df14927982617b67226786dc2c9fe71c46369e42261857022b",
            ),
            (
                "TS-104-D002",
                "b1ae308d33a641e3fe4f52be58f6335097b108a98562e7c9177aba6cf7af15ae",
            ),
            (
                "TS-104-D003",
                "a259d3e8c5bd001da86454ef6af8e71124e5ecd6da5ff68bb0b2ecd104833e5c",
            ),
            (
                "TS-104-D004",
                "2160e7fbea5f1212a24001d30e14fdfafd9b71bcfd2755fdc0cd441ab6873875",
            ),
            (
                "TS-104-C001",
                "a876c9dd63d417b8a0a3c054517c1d186ebeb4cfac69a1e9caf5ca6fec1d8ac7",
            ),
        ),
        context_only_trust_site_ids=("TS-104-C001",),
        helper_names=(
            "split_point_of",
            "slice_as_mut_ptr",
            "slice_split_at_mut",
            "slice_split_at_mut_unchecked",
        ),
        source_fragments=(
            "let (direction, split_index) = split_point_of(range)?",
            "if split_index > self.len()",
            "mem::take(self).split_at_mut(split_index)",
            "Direction::Front",
            "*self = back",
            "Some(front)",
            "Direction::Back",
            "*self = front",
            "Some(back)",
        ),
        source_backed_replacements=(
            SourceReplacement(
                "SRC-104-SPLIT-POINT",
                (
                    "StartInclusive-to-Back, End-to-Front, and EndInclusive "
                    "checked-add split-point transition"
                ),
                ("SplitPointTransition",),
                ("TS-104-D001",),
            ),
            SourceReplacement(
                "SRC-104-MEM-TAKE",
                (
                    "mem::take ownership transfer to the local split receiver "
                    "with an empty temporary receiver"
                ),
                ("MemTakeTransition",),
                ("TS-104-D002",),
            ),
            SourceReplacement(
                "SRC-104-MUTABLE-SPLIT",
                (
                    "bounds rejection, exact mutable front/back regions, "
                    "disjoint derived borrows, directional reassignment, and "
                    "ordered frame composition"
                ),
                (
                    "BoundsTransition",
                    "SplitRegionsTransition",
                    "DirectionalReturnTransition",
                    "BorrowCompositionTransition",
                    "FinalFrameTransition",
                ),
                ("TS-104-D003",),
            ),
            SourceReplacement(
                "SRC-104-ACTIVE-CONTRACT",
                (
                    "literal active initial-return and final-return partition "
                    "conjuncts; the retained corrected-contract substitution is "
                    "not used"
                ),
                (
                    "FinalFrameTransition",
                ),
                ("TS-104-D004",),
            ),
        ),
    ),
)
TARGET_BY_ARTIFACT = {config.artifact_id: config for config in TARGETS}
TARGET_KEYS = tuple((config.target, config.input_order) for config in TARGETS)


@dataclass(frozen=True)
class SourceCase:
    length: int
    range_kind: int
    range_index: int
    element_size: int = 8
    element_alignment: int = 8


SOURCE_CASES = {
    "empty_start_zero": SourceCase(0, START_INCLUSIVE, 0),
    "empty_end_zero": SourceCase(0, END, 0),
    "start_zero": SourceCase(3, START_INCLUSIVE, 0),
    "start_interior": SourceCase(5, START_INCLUSIVE, 2),
    "start_len": SourceCase(3, START_INCLUSIVE, 3),
    "start_out_of_bounds": SourceCase(3, START_INCLUSIVE, 4),
    "end_zero": SourceCase(3, END, 0),
    "end_interior": SourceCase(5, END, 2),
    "end_len": SourceCase(3, END, 3),
    "end_out_of_bounds": SourceCase(3, END, 4),
    "end_inclusive_interior": SourceCase(5, END_INCLUSIVE, 2),
    "end_inclusive_len": SourceCase(3, END_INCLUSIVE, 3),
    "end_inclusive_usize_max": SourceCase(3, END_INCLUSIVE, MAX_USIZE),
    "zst_start_interior": SourceCase(5, START_INCLUSIVE, 2, 0, 8),
}

NEGATIVE_PROBES = (
    "direction_reversal",
    "wrapping_end_inclusive_add",
    "altered_bounds_comparison",
    "off_by_one_split",
    "swapped_directional_branches",
    "mutated_none_frame",
    "lost_reference_identity",
    "lost_borrow_disjointness",
    "reversed_ordered_frame",
    "final_return_drift",
)

INPUT_FIELDS = (
    ("x_source", "(Seq Int)"),
    ("x_start", "Int"),
    ("x_length", "Int"),
    ("x_address", "Int"),
    ("x_allocation", "Int"),
    ("x_provenance", "Int"),
    ("x_parent_borrow", "Int"),
    ("x_element_size", "Int"),
    ("x_element_alignment", "Int"),
    ("x_range_kind", "Int"),
    ("x_range_index", "Int"),
)
BOUNDARY_FIELDS = (
    ("b_input_address", "Int"),
    ("b_input_allocation", "Int"),
    ("b_input_provenance", "Int"),
    ("b_parent_borrow", "Int"),
    ("b_element_size", "Int"),
    ("b_element_alignment", "Int"),
)
REGION_FIELDS = (
    ("values", "(Seq Int)"),
    ("start", "Int"),
    ("length", "Int"),
    ("address", "Int"),
    ("allocation", "Int"),
    ("provenance", "Int"),
    ("parent_borrow", "Int"),
    ("element_size", "Int"),
    ("element_alignment", "Int"),
    ("projection", "Int"),
    ("unique", "Bool"),
)
OUTPUT_FIELDS = (
    ("y_is_some", "Bool"),
    *((f"y_return_{name}", sort) for name, sort in REGION_FIELDS),
)
STATE_FIELDS = (
    ("s_helper_has_split", "Bool"),
    ("s_direction", "Int"),
    ("s_split_index", "Int"),
    ("s_bounds_ok", "Bool"),
    ("s_take_performed", "Bool"),
    ("s_receiver_empty_after_take", "Bool"),
    *((f"s_taken_{name}", sort) for name, sort in REGION_FIELDS),
    *((f"s_front_{name}", sort) for name, sort in REGION_FIELDS),
    *((f"s_back_{name}", sort) for name, sort in REGION_FIELDS),
    *((f"s_receiver_{name}", sort) for name, sort in REGION_FIELDS),
    *((f"s_return_final_{name}", sort) for name, sort in REGION_FIELDS),
    ("s_borrows_disjoint", "Bool"),
    ("s_receiver_reassigned", "Bool"),
    ("s_initial_partition", "Bool"),
    ("s_final_partition", "Bool"),
    ("s_ordered_final", "(Seq Int)"),
    ("s_values_unchanged", "Bool"),
)
SOURCE_TRANSITIONS = (
    "SplitPointTransition",
    "BoundsTransition",
    "MemTakeTransition",
    "SplitRegionsTransition",
    "DirectionalReturnTransition",
    "BorrowCompositionTransition",
    "FinalFrameTransition",
)
OUTPUT_SOURCE_TRANSITIONS = ("SourceOutputTransition",)


def canonical_json_sha256(record: dict[str, str]) -> str:
    data = json.dumps(
        record, sort_keys=True, separators=(",", ":")
    ).encode()
    return hashlib.sha256(data).hexdigest()


def _normalized(text: str) -> str:
    return " ".join(text.split())


def validate_source_anchors(
    config: SplitOffTarget,
    source_item: str,
    vocabulary: str,
    helpers: dict[str, str],
) -> None:
    normalized_source = _normalized(source_item)
    for fragment in config.source_fragments:
        if _normalized(fragment) not in normalized_source:
            raise GuardError(
                f"{config.target}: canonical target fragment changed: {fragment}"
            )
    normalized_vocabulary = _normalized(vocabulary)
    for fragment in (
        "pub open spec fn slice_split_off_partition",
        "removed + remaining == source || remaining + removed == source",
    ):
        if _normalized(fragment) not in normalized_vocabulary:
            raise GuardError(f"{config.target}: split vocabulary changed")
    if set(helpers) != set(config.helper_names):
        raise GuardError(f"{config.target}: canonical helper set changed")
    for helper in config.helper_sources:
        normalized_helper = _normalized(helpers[helper.name])
        for fragment in helper.fragments:
            if _normalized(fragment) not in normalized_helper:
                raise GuardError(
                    f"{config.target}: {helper.name} changed: {fragment}"
                )
    prohibited = (
        "slice_split_off_partition::<T>(",
        "assume_specification",
        "external_body",
    )
    combined = " ".join(_normalized(text) for text in helpers.values())
    if any(token in combined for token in prohibited):
        raise GuardError(
            f"{config.target}: answer-bearing helper entered canonical sources"
        )


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


def _state_declarations(purpose: str) -> str:
    if purpose == EXACT_OUTPUT:
        return (
            "(declare-datatypes ((State 0)) (((mkState))))\n"
            + _datatype("FrameState", "mkFrameState", STATE_FIELDS)
        )
    return _datatype("State", "mkState", STATE_FIELDS)


def _frame_adapt(text: str, purpose: str) -> str:
    if purpose == PRIMARY:
        return text
    return text.replace("(s State)", "(f FrameState)").replace(" s)", " f)")


def _default(sort: str) -> str:
    if sort == "(Seq Int)":
        return EMPTY_SEQ
    if sort == "Bool":
        return "false"
    return "0"


def _region_assignments(
    prefix: str,
    values: dict[str, str],
    *,
    variable: str,
) -> str:
    return "\n       ".join(
        f"(= ({prefix}_{name} {variable}) {values[name]})"
        for name, _ in REGION_FIELDS
    )


def _empty_region(prefix: str, *, variable: str) -> str:
    return "\n       ".join(
        f"(= ({prefix}_{name} {variable}) {_default(sort)})"
        for name, sort in REGION_FIELDS
    )


def _copy_region(
    destination: str,
    source: str,
    *,
    destination_variable: str,
    source_variable: str,
) -> str:
    return "\n       ".join(
        f"(= ({destination}_{name} {destination_variable}) "
        f"({source}_{name} {source_variable}))"
        for name, _ in REGION_FIELDS
    )


def _input_region_values(config: SplitOffTarget) -> dict[str, str]:
    return {
        "values": "(x_source x)",
        "start": "(x_start x)",
        "length": "(x_length x)",
        "address": "(x_address x)",
        "allocation": "(x_allocation x)",
        "provenance": "(x_provenance x)",
        "parent_borrow": "(x_parent_borrow x)",
        "element_size": "(x_element_size x)",
        "element_alignment": "(x_element_alignment x)",
        "projection": "0",
        "unique": "true" if config.mutable else "false",
    }


def _split_region_values(
    config: SplitOffTarget,
    side: str,
) -> dict[str, str]:
    if side == "front":
        offset = "0"
        length = "(s_split_index s)"
        projection = "1"
    else:
        offset = "(s_split_index s)"
        length = "(- (x_length x) (s_split_index s))"
        projection = "2"
    source = "(s_taken_values s)" if config.mutable else "(x_source x)"
    return {
        "values": f"(seq.extract {source} {offset} {length})",
        "start": f"(+ (x_start x) {offset})",
        "length": length,
        "address": (
            f"(+ (x_address x) (* {offset} (x_element_size x)))"
        ),
        "allocation": "(x_allocation x)",
        "provenance": "(x_provenance x)",
        "parent_borrow": "(x_parent_borrow x)",
        "element_size": "(x_element_size x)",
        "element_alignment": "(x_element_alignment x)",
        "projection": projection,
        "unique": "true" if config.mutable else "false",
    }


def _source_output_region_values(config: SplitOffTarget) -> dict[str, str]:
    helper_has_split = (
        f"(not (and (= (x_range_kind x) {END_INCLUSIVE}) "
        f"(= (x_range_index x) {MAX_USIZE})))"
    )
    split_index = (
        f"(ite (= (x_range_kind x) {END_INCLUSIVE}) "
        "(+ (x_range_index x) 1) (x_range_index x))"
    )
    success = f"(and {helper_has_split} (<= {split_index} (x_length x)))"
    front = f"(= (x_range_kind x) {START_INCLUSIVE})"
    offset = f"(ite {front} {split_index} 0)"
    length = (
        f"(ite {front} (- (x_length x) {split_index}) {split_index})"
    )
    return {
        "values": f"(seq.extract (x_source x) {offset} {length})",
        "start": f"(+ (x_start x) {offset})",
        "length": length,
        "address": (
            f"(+ (x_address x) (* {offset} (x_element_size x)))"
        ),
        "allocation": "(x_allocation x)",
        "provenance": "(x_provenance x)",
        "parent_borrow": "(x_parent_borrow x)",
        "element_size": "(x_element_size x)",
        "element_alignment": "(x_element_alignment x)",
        "projection": f"(ite {front} 2 1)",
        "unique": "true" if config.mutable else "false",
        "_success": success,
    }


def _input_boundary_observed() -> str:
    return """\
(define-fun InputBoundaryObserved ((x Input) (b Boundary)) Bool
  (and (= (b_input_address b) (x_address x))
       (= (b_input_allocation b) (x_allocation x))
       (= (b_input_provenance b) (x_provenance x))
       (= (b_parent_borrow b) (x_parent_borrow x))
       (= (b_element_size b) (x_element_size x))
       (= (b_element_alignment b) (x_element_alignment x))))"""


def _partition_definition() -> str:
    return """\
(define-fun SliceSplitOffPartition
  ((source (Seq Int)) (remaining (Seq Int)) (removed (Seq Int))) Bool
  (or (= (seq.++ removed remaining) source)
      (= (seq.++ remaining removed) source)))"""


def _source_output_transition(config: SplitOffTarget) -> str:
    values = _source_output_region_values(config)
    success = values.pop("_success")
    return f"""\
(define-fun SourceOutputTransition ((x Input) (y Output)) Bool
  (and (= (y_is_some y) {success})
       (ite (y_is_some y)
            (and {_region_assignments("y_return", values, variable="y")})
            (and {_empty_region("y_return", variable="y")}))))"""


def _split_point_transition() -> str:
    return f"""\
(define-fun SplitPointTransition ((x Input) (y Output) (s State)) Bool
  (and
    (= (s_helper_has_split s)
       (not (and (= (x_range_kind x) {END_INCLUSIVE})
                 (= (x_range_index x) {MAX_USIZE}))))
    (= (s_direction s)
       (ite (s_helper_has_split s)
            (ite (= (x_range_kind x) {START_INCLUSIVE}) {BACK} {FRONT})
            (- 1)))
    (= (s_split_index s)
       (ite (s_helper_has_split s)
            (ite (= (x_range_kind x) {END_INCLUSIVE})
                 (+ (x_range_index x) 1)
                 (x_range_index x))
            (- 1)))))"""


def _bounds_transition() -> str:
    return """\
(define-fun BoundsTransition ((x Input) (y Output) (s State)) Bool
  (and
    (= (s_bounds_ok s)
       (and (s_helper_has_split s)
            (<= (s_split_index s) (x_length x))))
    (= (y_is_some y) (s_bounds_ok s))))"""


def _mem_take_transition(config: SplitOffTarget) -> str:
    if config.mutable:
        return f"""\
(define-fun MemTakeTransition ((x Input) (y Output) (s State)) Bool
  (ite (y_is_some y)
       (and (= (s_take_performed s) true)
            (= (s_receiver_empty_after_take s) true)
            {_region_assignments("s_taken", _input_region_values(config), variable="s")})
       (and (= (s_take_performed s) false)
            (= (s_receiver_empty_after_take s) false)
            {_empty_region("s_taken", variable="s")})))"""
    return f"""\
(define-fun MemTakeTransition ((x Input) (y Output) (s State)) Bool
  (and (= (s_take_performed s) false)
       (= (s_receiver_empty_after_take s) false)
       {_empty_region("s_taken", variable="s")}))"""


def _split_regions_transition(config: SplitOffTarget) -> str:
    return f"""\
(define-fun SplitRegionsTransition ((x Input) (y Output) (s State)) Bool
  (ite (y_is_some y)
       (and {_region_assignments("s_front", _split_region_values(config, "front"), variable="s")}
            {_region_assignments("s_back", _split_region_values(config, "back"), variable="s")})
       (and {_empty_region("s_front", variable="s")}
            {_empty_region("s_back", variable="s")})))"""


def _directional_return_transition(config: SplitOffTarget) -> str:
    receiver_unique = "true" if config.mutable else "false"
    input_receiver = _input_region_values(config)
    return f"""\
(define-fun DirectionalReturnTransition
  ((x Input) (y Output) (s State)) Bool
  (ite (y_is_some y)
       (ite (= (s_direction s) {FRONT})
            (and {_copy_region("y_return", "s_front", destination_variable="y", source_variable="s")}
                 {_copy_region("s_receiver", "s_back", destination_variable="s", source_variable="s")})
            (and {_copy_region("y_return", "s_back", destination_variable="y", source_variable="s")}
                 {_copy_region("s_receiver", "s_front", destination_variable="s", source_variable="s")}))
       (and {_empty_region("y_return", variable="y")}
            {_region_assignments("s_receiver", input_receiver, variable="s")}
            (= (s_receiver_unique s) {receiver_unique}))))"""


def _borrow_composition_transition(config: SplitOffTarget) -> str:
    unique = "true" if config.mutable else "false"
    return f"""\
(define-fun BorrowCompositionTransition
  ((x Input) (y Output) (s State)) Bool
  (and
    (= (s_borrows_disjoint s)
       (ite (y_is_some y)
            (<= (+ (s_front_start s) (s_front_length s))
                (s_back_start s))
            true))
    (=> (y_is_some y)
        (and (= (s_front_unique s) {unique})
             (= (s_back_unique s) {unique})
             (= (y_return_unique y) {unique})
             (= (s_receiver_unique s) {unique})
             (= (s_front_parent_borrow s) (x_parent_borrow x))
             (= (s_back_parent_borrow s) (x_parent_borrow x))
             (= (y_return_parent_borrow y) (x_parent_borrow x))
             (= (s_receiver_parent_borrow s) (x_parent_borrow x))))))"""


def _active_contract_definitions(config: SplitOffTarget) -> str:
    common = """\
(define-fun ActiveNoneFrameConjunct
  ((x Input) (y Output) (s State)) Bool
  (=> (not (y_is_some y))
      (= (s_receiver_values s) (x_source x))))
(define-fun ActiveInitialReturnPartitionConjunct
  ((x Input) (y Output) (s State)) Bool
  (=> (y_is_some y)
      (SliceSplitOffPartition
        (x_source x) (s_receiver_values s) (y_return_values y))))"""
    if not config.mutable:
        return common
    return common + """\

(define-fun ActiveFinalReturnPartitionConjunct
  ((x Input) (y Output) (s State)) Bool
  (=> (y_is_some y)
      (SliceSplitOffPartition
        (x_source x)
        (s_receiver_values s)
        (s_return_final_values s))))"""


def _final_frame_transition() -> str:
    return f"""\
(define-fun FinalFrameTransition ((x Input) (y Output) (s State)) Bool
  (and
    {_copy_region("s_return_final", "y_return", destination_variable="s", source_variable="y")}
    (= (s_receiver_reassigned s) (y_is_some y))
    (= (s_initial_partition s)
       (ite (y_is_some y)
            (SliceSplitOffPartition
              (x_source x)
              (s_receiver_values s)
              (y_return_values y))
            (= (s_receiver_values s) (x_source x))))
    (= (s_final_partition s)
       (ite (y_is_some y)
            (SliceSplitOffPartition
              (x_source x)
              (s_receiver_values s)
              (s_return_final_values s))
            (= (s_receiver_values s) (x_source x))))
    (= (s_initial_partition s) true)
    (= (s_final_partition s) true)
    (= (s_ordered_final s)
       (ite (y_is_some y)
            (seq.++ (s_front_values s) (s_back_values s))
            (x_source x)))
    (= (s_ordered_final s) (x_source x))
    (= (s_values_unchanged s) true)))"""


def _requires() -> str:
    return f"""\
(define-fun Requires_T ((x Input)) Bool
  (and (= (x_length x) (seq.len (x_source x)))
       (>= (x_length x) 0)
       (<= (x_length x) {MAX_USIZE})
       (>= (x_start x) 0)
       (> (x_address x) 0)
       (>= (x_allocation x) 0)
       (>= (x_provenance x) 0)
       (> (x_parent_borrow x) 0)
       (>= (x_element_size x) 0)
       (> (x_element_alignment x) 0)
       (= (mod (x_address x) (x_element_alignment x)) 0)
       (= (mod (x_element_size x) (x_element_alignment x)) 0)
       (>= (x_range_kind x) {START_INCLUSIVE})
       (<= (x_range_kind x) {END_INCLUSIVE})
       (>= (x_range_index x) 0)
       (<= (x_range_index x) {MAX_USIZE})
       (<= (* (x_length x) (x_element_size x)) 9223372036854775807)
       (or (= (* (x_length x) (x_element_size x)) 0)
           (and (> (x_allocation x) 0)
                (> (x_provenance x) 0)))))"""


def _boundary() -> str:
    return """\
(define-fun Boundary_T ((x Input) (b Boundary)) Bool
  (and (> (b_input_address b) 0)
       (>= (b_input_allocation b) 0)
       (>= (b_input_provenance b) 0)
       (> (b_parent_borrow b) 0)
       (>= (b_element_size b) 0)
       (> (b_element_alignment b) 0)
       (or (= (* (x_length x) (x_element_size x)) 0)
           (and (> (b_input_allocation b) 0)
                (> (b_input_provenance b) 0)))
       (InputBoundaryObserved x b)))"""


def _target_definition(config: SplitOffTarget, purpose: str) -> str:
    frame = "s" if purpose == PRIMARY else "f"
    calls = (
        "(InputBoundaryObserved x b)",
        f"(SplitPointTransition x y {frame})",
        f"(BoundsTransition x y {frame})",
        f"(MemTakeTransition x y {frame})",
        f"(SplitRegionsTransition x y {frame})",
        f"(DirectionalReturnTransition x y {frame})",
        f"(BorrowCompositionTransition x y {frame})",
        f"(FinalFrameTransition x y {frame})",
        *(
            f"({name} x y {frame})"
            for name in config.active_conjuncts
        ),
    )
    if purpose == EXACT_OUTPUT:
        return """\
(define-fun TargetDefinition_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and (InputBoundaryObserved x b)
       (SourceOutputTransition x y)
       (exists ((f FrameState))
         (and %s))))""" % "\n              ".join(calls[1:])
    return """\
(define-fun TargetDefinition_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and %s))""" % "\n       ".join(calls)


def _equivalence(purpose: str) -> str:
    equalities = [
        f"(= ({selector} y1) ({selector} y2))"
        for selector, _ in OUTPUT_FIELDS
    ]
    if purpose == PRIMARY:
        equalities.extend(
            f"(= ({selector} s1) ({selector} s2))"
            for selector, _ in STATE_FIELDS
        )
    return """\
(define-fun Equivalent_T
  ((x Input) (b Boundary)
   (y1 Output) (s1 State) (y2 Output) (s2 State)) Bool
  (and %s))""" % "\n       ".join(equalities)


def _model_text(
    config: SplitOffTarget,
    purpose: str,
    *,
    include_theorem: bool,
) -> str:
    if purpose not in PURPOSES:
        raise ValueError(f"{config.target}: unknown purpose {purpose}")
    theorem = ""
    if include_theorem:
        theorem = """\
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
    transitions = "\n".join(
        (
            _input_boundary_observed(),
            _partition_definition(),
            _source_output_transition(config),
            _frame_adapt(_split_point_transition(), purpose),
            _frame_adapt(_bounds_transition(), purpose),
            _frame_adapt(_mem_take_transition(config), purpose),
            _frame_adapt(_split_regions_transition(config), purpose),
            _frame_adapt(_directional_return_transition(config), purpose),
            _frame_adapt(_borrow_composition_transition(config), purpose),
            _frame_adapt(_final_frame_transition(), purpose),
            _frame_adapt(_active_contract_definitions(config), purpose),
        )
    )
    return f"""\
; Target: {config.target}
; Active contract SHA-256: {config.active_contract_sha256}
; Purpose: {purpose}
; Range kind/index are shared input. Boundary contains only initial
; address, allocation, provenance, parent borrow, and layout observations.
(set-logic ALL)
{_datatype("Input", "mkInput", INPUT_FIELDS)}
{_datatype("Boundary", "mkBoundary", BOUNDARY_FIELDS)}
{_datatype("Output", "mkOutput", OUTPUT_FIELDS)}
{_state_declarations(purpose)}
(declare-const x Input)
(declare-const b Boundary)
(declare-const y1 Output)
(declare-const s1 State)
(declare-const y2 Output)
(declare-const s2 State)
{transitions}
{_requires()}
{_boundary()}
{_target_definition(config, purpose)}
(define-fun Spec_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (TargetDefinition_T x b y s))
{_equivalence(purpose)}
{theorem}"""


def obligation_text(config: SplitOffTarget, purpose: str) -> str:
    return _model_text(config, purpose, include_theorem=True)


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


def _source_backed_replacements(
    config: SplitOffTarget,
    purpose: str,
) -> list[dict[str, Any]]:
    return [
        {
            "replacement_id": replacement.replacement_id,
            "operation": replacement.operation,
            "symbols": (
                ["SourceOutputTransition"]
                if purpose == EXACT_OUTPUT
                else list(replacement.symbols)
            ),
            "source_citations": list(config.source_citations),
            "replaces_trust_site_ids": list(
                replacement.replaces_trust_site_ids
            ),
        }
        for replacement in config.source_backed_replacements
    ]


def _boundary_metadata(config: SplitOffTarget) -> list[dict[str, Any]]:
    roles = {
        "b_input_address": "input_memory",
        "b_input_allocation": "input_provenance",
        "b_input_provenance": "input_provenance",
        "b_parent_borrow": "input_provenance",
        "b_element_size": "input_layout",
        "b_element_alignment": "input_layout",
    }
    meanings = {
        "b_input_address": "initial non-null slice data address",
        "b_input_allocation": "initial allocation identity",
        "b_input_provenance": "initial strict-provenance identity",
        "b_parent_borrow": "initial parent-borrow identity",
        "b_element_size": "element size, including zero",
        "b_element_alignment": "positive element alignment",
    }
    return [
        {
            "selector": selector,
            "role": roles[selector],
            "meaning": meanings[selector],
            "source_citations": list(config.source_citations),
            "trust_site_ids": [],
            "source_backed_replacement_ids": list(config.replacement_ids),
        }
        for selector, _ in BOUNDARY_FIELDS
    ]


def obligation_metadata(
    config: SplitOffTarget,
    purpose: str,
) -> dict[str, Any]:
    if purpose not in PURPOSES:
        raise ValueError(f"{config.target}: unknown purpose {purpose}")
    return {
        "schema_version": 3,
        "target": config.target,
        "input_order": config.input_order,
        "obligation_purpose": purpose,
        "active_contract_sha256": config.active_contract_sha256,
        "active_contract_text": config.active_contract_text,
        "model_status": "source-backed-complete",
        "domain": {
            "slice_length": "arbitrary usize-sized nonnegative integer",
            "range_kind": (
                "StartInclusive, End, or EndInclusive in shared input x"
            ),
            "range_index": "arbitrary usize value in shared input x",
            "element_layout": (
                "arbitrary nonnegative size and positive alignment; empty and "
                "nonempty ZST slices are included"
            ),
            "source_model_complete": True,
        },
        "active_contract_conjuncts": list(config.active_conjuncts),
        "contract_translation": {
            "none_frame": "None leaves the receiver sequence unchanged",
            "initial_return_partition": (
                "Some requires the active prefix/suffix partition using the "
                "initial returned-reference view"
            ),
            "final_return_partition": (
                "Some additionally requires the active prefix/suffix partition "
                "using final(ret.unwrap())"
                if config.mutable
                else "not present in the immutable active contract"
            ),
            "active_contract_substitution": (
                "prohibited; the retained corrected mutable harness is bound "
                "as evidence but its deleted final-return clause is not used"
                if config.mutable
                else "none"
            ),
        },
        "boundary_scope": {
            "shared_observations": [
                selector for selector, _ in BOUNDARY_FIELDS
            ],
            "admitted_trust_site_ids": [],
            "excluded_retained_trust_site_ids": list(
                config.excluded_trust_site_ids
            ),
            "context_only_trust_site_ids": list(
                config.context_only_trust_site_ids
            ),
            "all_audited_trust_site_ids": list(config.all_trust_site_ids),
            "source_backed_replacement_ids": list(config.replacement_ids),
            "excluded_observations": [
                "range kind and index, which belong to shared input x",
                "direction, split index, checked-add result, and bounds decision",
                "front/back, returned, remaining, or final returned regions",
                "derived borrows, output, final state, answer encoding, and trace",
            ],
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
        "boundary_fields": _boundary_metadata(config),
        "source_backed_replacements": _source_backed_replacements(
            config, purpose
        ),
        "unresolved_source_model_trust_site_ids": [],
        "declared_functions": [],
        "source_transition_definitions": list(
            OUTPUT_SOURCE_TRANSITIONS
            if purpose == EXACT_OUTPUT
            else SOURCE_TRANSITIONS
        ),
        "source_transition_bindings": {
            "public_target": {
                "operation": config.target,
                "source_citations": [config.source_reference],
            },
            "range_helper": {
                "symbols": [
                    "SourceOutputTransition"
                    if purpose == EXACT_OUTPUT
                    else "SplitPointTransition"
                ],
                "source_citations": [
                    CANONICAL_SOURCES["split_point_of"].reference
                ],
            },
            "bounds_and_directional_partition": {
                "symbols": (
                    ["SourceOutputTransition"]
                    if purpose == EXACT_OUTPUT
                    else [
                        "BoundsTransition",
                        "SplitRegionsTransition",
                        "DirectionalReturnTransition",
                    ]
                ),
                "source_citations": list(config.source_citations),
            },
            "ownership_borrows_and_frame": {
                "symbols": (
                    ["SourceOutputTransition"]
                    if purpose == EXACT_OUTPUT
                    else [
                        "MemTakeTransition",
                        "BorrowCompositionTransition",
                        "FinalFrameTransition",
                    ]
                ),
                "source_citations": list(config.source_citations),
            },
        },
        "equivalence_kind": "exact",
        "equivalence_scope": (
            "every principal return/reference identity and every final-state "
            "and source-transition observation"
            if purpose == PRIMARY
            else "every principal return/reference identity"
        ),
        "principal_observations": _principal_observations(purpose),
        "expected_solver_result": "unsat",
    }


def obligation(
    config: SplitOffTarget,
    purpose: str,
) -> tuple[str, dict[str, Any]]:
    return obligation_text(config, purpose), obligation_metadata(config, purpose)


def validate_target_obligation(
    config: SplitOffTarget,
    text: str,
    metadata: dict[str, Any],
) -> None:
    validate_obligation(text, metadata)
    purpose = metadata.get("obligation_purpose")
    if purpose not in PURPOSES:
        raise GuardError(f"{config.target}: unknown obligation purpose")
    expected_text, expected_metadata = obligation(config, str(purpose))
    if metadata != expected_metadata:
        raise GuardError(
            f"{config.target}: metadata differs from reviewed split-off model"
        )
    if parse_smt(text) != parse_smt(expected_text):
        raise GuardError(
            f"{config.target}: SMT differs from reviewed split-off model"
        )


def _sequence_term(length: int) -> str:
    if length == 0:
        return EMPTY_SEQ
    terms = [f"(seq.unit {10 + index})" for index in range(length)]
    while len(terms) > 1:
        terms = [f"(seq.++ {terms[0]} {terms[1]})", *terms[2:]]
    return terms[0]


def _fixed_input_assertions(case: SourceCase) -> list[str]:
    return [
        f"(assert (= (x_source x) {_sequence_term(case.length)}))",
        "(assert (= (x_start x) 7))",
        f"(assert (= (x_length x) {case.length}))",
        "(assert (= (x_address x) 1024))",
        "(assert (= (x_allocation x) 11))",
        "(assert (= (x_provenance x) 13))",
        "(assert (= (x_parent_borrow x) 17))",
        f"(assert (= (x_element_size x) {case.element_size}))",
        f"(assert (= (x_element_alignment x) {case.element_alignment}))",
        f"(assert (= (x_range_kind x) {case.range_kind}))",
        f"(assert (= (x_range_index x) {case.range_index}))",
    ]


def _model_query() -> str:
    selectors = (
        "(x_range_kind x)",
        "(x_range_index x)",
        "(y_is_some y1)",
        "(y_return_start y1)",
        "(y_return_length y1)",
        "(y_return_address y1)",
        "(y_return_allocation y1)",
        "(y_return_provenance y1)",
        "(y_return_parent_borrow y1)",
        "(y_return_projection y1)",
        "(y_return_unique y1)",
        "(s_helper_has_split s1)",
        "(s_direction s1)",
        "(s_split_index s1)",
        "(s_bounds_ok s1)",
        "(s_take_performed s1)",
        "(s_receiver_start s1)",
        "(s_receiver_length s1)",
        "(s_receiver_address s1)",
        "(s_return_final_length s1)",
        "(s_borrows_disjoint s1)",
        "(s_initial_partition s1)",
        "(s_final_partition s1)",
    )
    return "(get-value (\n  %s))" % "\n  ".join(selectors)


def source_instance_text(
    config: SplitOffTarget,
    case: SourceCase,
    *,
    extra_assertions: tuple[str, ...] = (),
) -> str:
    if (
        case.length < 0
        or case.range_kind not in (START_INCLUSIVE, END, END_INCLUSIVE)
        or not 0 <= case.range_index <= MAX_USIZE
        or case.element_size < 0
        or case.element_alignment <= 0
    ):
        raise ValueError("split-off source case has invalid input")
    assertions = [
        *_fixed_input_assertions(case),
        "(assert (Requires_T x))",
        "(assert (Boundary_T x b))",
        "(assert (Spec_T x b y1 s1))",
    ]
    if case == SOURCE_CASES["zst_start_interior"]:
        assertions.append(
            "(assert (= (y_return_address y1) (s_receiver_address s1)))"
        )
    if case in (
        SOURCE_CASES["start_len"],
        SOURCE_CASES["end_len"],
    ):
        assertions.append(
            "(assert (= (s_back_address s1)"
            " (+ (x_address x) (* (x_length x) (x_element_size x)))))"
        )
    assertions.extend(f"(assert {item})" for item in extra_assertions)
    return (
        _model_text(config, PRIMARY, include_theorem=False)
        + "\n"
        + "\n".join(assertions)
        + "\n(check-sat)\n"
        + _model_query()
        + "\n"
    )


def negative_probe_text(
    config: SplitOffTarget,
    name: str,
) -> str:
    if name not in NEGATIVE_PROBES:
        raise ValueError(f"unknown split-off negative probe: {name}")
    cases = {
        "direction_reversal": SOURCE_CASES["start_interior"],
        "wrapping_end_inclusive_add": SOURCE_CASES[
            "end_inclusive_usize_max"
        ],
        "altered_bounds_comparison": SOURCE_CASES["end_len"],
        "off_by_one_split": SOURCE_CASES["end_interior"],
        "swapped_directional_branches": SOURCE_CASES["start_interior"],
        "mutated_none_frame": SOURCE_CASES["start_out_of_bounds"],
        "lost_reference_identity": SOURCE_CASES["end_interior"],
        "lost_borrow_disjointness": SOURCE_CASES["start_interior"],
        "reversed_ordered_frame": SOURCE_CASES["start_interior"],
        "final_return_drift": SOURCE_CASES["end_interior"],
    }
    contradictions = {
        "direction_reversal": f"(not (= (s_direction s1) {BACK}))",
        "wrapping_end_inclusive_add": "(s_helper_has_split s1)",
        "altered_bounds_comparison": "(not (y_is_some y1))",
        "off_by_one_split": (
            "(not (= (s_split_index s1) (x_range_index x)))"
        ),
        "swapped_directional_branches": (
            "(= (y_return_values y1) (s_front_values s1))"
        ),
        "mutated_none_frame": (
            "(not (= (s_receiver_values s1) (x_source x)))"
        ),
        "lost_reference_identity": (
            "(not (= (y_return_allocation y1) (x_allocation x)))"
        ),
        "lost_borrow_disjointness": "(not (s_borrows_disjoint s1))",
        "reversed_ordered_frame": (
            "(= (s_ordered_final s1)"
            " (seq.++ (s_back_values s1) (s_front_values s1)))"
        ),
        "final_return_drift": (
            "(not (= (s_return_final_values s1) (y_return_values y1)))"
        ),
    }
    return (
        _model_text(config, PRIMARY, include_theorem=False)
        + "\n"
        + "\n".join(
            (
                *_fixed_input_assertions(cases[name]),
                "(assert (Requires_T x))",
                "(assert (Boundary_T x b))",
                "(assert (Spec_T x b y1 s1))",
                f"(assert {contradictions[name]})",
            )
        )
        + "\n(check-sat)\n"
    )


def boundary_manifest(config: SplitOffTarget) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "target": config.target,
        "input_order": config.input_order,
        "boundary_narrower_than_target": True,
        "proof_boundary_assumption": (
            "Both executions observe the same initial non-null slice address, "
            "allocation, strict provenance, parent-borrow identity, element "
            "size, and element alignment. Range kind and index are shared x."
        ),
        "shared_boundary_observations": _boundary_metadata(config),
        "canonical_source_transition": {
            "split_point": (
                "StartInclusive -> Back/index; End -> Front/index; "
                "EndInclusive -> Front/checked_add(index, 1), overflow -> None"
            ),
            "bounds": "split_index > len -> None with unchanged receiver",
            "regions": "front [0, split_index), back [split_index, len)",
            "directional_result": (
                "Front returns front and retains back; Back returns back and "
                "retains front"
            ),
            "ownership_transfer": (
                "successful mutable path takes the receiver into a local "
                "owner, temporarily leaves an empty receiver, then reassigns "
                "one disjoint split borrow"
                if config.mutable
                else "not applicable to immutable receiver"
            ),
            "reference_identity": (
                "logical range, address, allocation, provenance, parent "
                "borrow, layout, side projection, and mutability uniqueness"
            ),
            "zst_and_one_past": (
                "logical range identity remains distinct when ZST addresses "
                "are equal; a split at len retains the one-past address"
            ),
            "final_frame": (
                "front then back reconstructs the source; returned final view "
                "equals its initial view because the target performs no "
                "element write"
            ),
        },
        "source_backed_replacements": _source_backed_replacements(
            config, PRIMARY
        ),
        "context_only_trust_site_ids": list(config.context_only_trust_site_ids),
        "excluded_retained_trust_site_ids": list(
            config.excluded_trust_site_ids
        ),
        "all_audited_trust_site_ids": list(config.all_trust_site_ids),
        "active_contract_substitution_prohibited": (
            config.mutable
            and "TS-104-D004" in config.excluded_trust_site_ids
        ),
        "excluded_from_boundary": [
            "range kind and index (shared input x)",
            "direction and split index",
            "checked-add overflow and bounds decisions",
            "returned, remaining, front, back, or final-return regions",
            "derived borrows, output, final state, answer encoding, and trace",
        ],
    }


def _verus_active_contract(config: SplitOffTarget) -> str:
    final_clause = (
        "\n            && split_partition(\n"
        "                input.slice.source,\n"
        "                state.receiver.values,\n"
        "                state.returned_final.values,\n"
        "            )"
        if config.mutable
        else ""
    )
    return f"""\
    if output.is_some {{
        split_partition(
            input.slice.source,
            state.receiver.values,
            output.returned.values,
        ){final_clause}
    }} else {{
        state.receiver.values == input.slice.source
    }}"""


def verus_text(config: SplitOffTarget) -> str:
    function = config.function_name
    mutable = "true" if config.mutable else "false"
    return f"""\
#![allow(dead_code, unused_imports, unused_variables)]
// Source-backed two-execution model for {config.target}.

use vstd::prelude::*;
use vstd::seq::*;

verus! {{

pub ghost struct SliceIdentity {{
    pub source: Seq<int>,
    pub start: int,
    pub address: int,
    pub allocation: int,
    pub provenance: int,
    pub parent_borrow: int,
    pub element_size: nat,
    pub element_alignment: nat,
}}

pub ghost struct RegionIdentity {{
    pub values: Seq<int>,
    pub start: int,
    pub length: int,
    pub address: int,
    pub allocation: int,
    pub provenance: int,
    pub parent_borrow: int,
    pub element_size: nat,
    pub element_alignment: nat,
    pub projection: int,
    pub unique: bool,
}}

pub ghost struct Input {{
    pub slice: SliceIdentity,
    pub range_kind: int,
    pub range_index: nat,
}}

pub ghost struct Boundary {{
    pub input_address: int,
    pub input_allocation: int,
    pub input_provenance: int,
    pub parent_borrow: int,
    pub element_size: nat,
    pub element_alignment: nat,
}}

pub ghost struct Output {{
    pub is_some: bool,
    pub returned: RegionIdentity,
}}

pub ghost struct FinalState {{
    pub helper_has_split: bool,
    pub direction: int,
    pub split_index: int,
    pub bounds_ok: bool,
    pub take_performed: bool,
    pub receiver_empty_after_take: bool,
    pub taken: RegionIdentity,
    pub front: RegionIdentity,
    pub back: RegionIdentity,
    pub receiver: RegionIdentity,
    pub returned_final: RegionIdentity,
    pub borrows_disjoint: bool,
    pub receiver_reassigned: bool,
    pub initial_partition: bool,
    pub final_partition: bool,
    pub ordered_final: Seq<int>,
    pub values_unchanged: bool,
}}

pub open spec fn empty_region() -> RegionIdentity {{
    RegionIdentity {{
        values: Seq::empty(),
        start: 0,
        length: 0,
        address: 0,
        allocation: 0,
        provenance: 0,
        parent_borrow: 0,
        element_size: 0,
        element_alignment: 0,
        projection: 0,
        unique: false,
    }}
}}

pub open spec fn input_region(input: Input) -> RegionIdentity {{
    RegionIdentity {{
        values: input.slice.source,
        start: input.slice.start,
        length: input.slice.source.len() as int,
        address: input.slice.address,
        allocation: input.slice.allocation,
        provenance: input.slice.provenance,
        parent_borrow: input.slice.parent_borrow,
        element_size: input.slice.element_size,
        element_alignment: input.slice.element_alignment,
        projection: 0,
        unique: {mutable},
    }}
}}

pub open spec fn make_region(
    input: Input,
    offset: int,
    length: int,
    projection: int,
) -> RegionIdentity {{
    RegionIdentity {{
        values: input.slice.source.subrange(offset, offset + length),
        start: input.slice.start + offset,
        length,
        address: input.slice.address + offset * input.slice.element_size as int,
        allocation: input.slice.allocation,
        provenance: input.slice.provenance,
        parent_borrow: input.slice.parent_borrow,
        element_size: input.slice.element_size,
        element_alignment: input.slice.element_alignment,
        projection,
        unique: {mutable},
    }}
}}

pub open spec fn helper_has_split(input: Input) -> bool {{
    !(input.range_kind == {END_INCLUSIVE}
        && input.range_index == {MAX_USIZE})
}}

pub open spec fn helper_direction(input: Input) -> int {{
    if helper_has_split(input) {{
        if input.range_kind == {START_INCLUSIVE} {{ {BACK} }} else {{ {FRONT} }}
    }} else {{
        -1
    }}
}}

pub open spec fn helper_split_index(input: Input) -> int {{
    if helper_has_split(input) {{
        if input.range_kind == {END_INCLUSIVE} {{
            input.range_index as int + 1
        }} else {{
            input.range_index as int
        }}
    }} else {{
        -1
    }}
}}

pub open spec fn branch_succeeds(input: Input) -> bool {{
    helper_has_split(input)
        && helper_split_index(input) <= input.slice.source.len() as int
}}

pub open spec fn front_region(input: Input) -> RegionIdentity
    recommends branch_succeeds(input)
{{
    make_region(input, 0, helper_split_index(input), 1)
}}

pub open spec fn back_region(input: Input) -> RegionIdentity
    recommends branch_succeeds(input)
{{
    make_region(
        input,
        helper_split_index(input),
        input.slice.source.len() as int - helper_split_index(input),
        2,
    )
}}

pub open spec fn source_output(input: Input) -> Output {{
    if branch_succeeds(input) {{
        Output {{
            is_some: true,
            returned: if helper_direction(input) == {FRONT} {{
                front_region(input)
            }} else {{
                back_region(input)
            }},
        }}
    }} else {{
        Output {{ is_some: false, returned: empty_region() }}
    }}
}}

pub open spec fn source_state(input: Input) -> FinalState {{
    if branch_succeeds(input) {{
        let front = front_region(input);
        let back = back_region(input);
        let returned = if helper_direction(input) == {FRONT} {{ front }} else {{ back }};
        let receiver = if helper_direction(input) == {FRONT} {{ back }} else {{ front }};
        FinalState {{
            helper_has_split: true,
            direction: helper_direction(input),
            split_index: helper_split_index(input),
            bounds_ok: true,
            take_performed: {mutable},
            receiver_empty_after_take: {mutable},
            taken: if {mutable} {{ input_region(input) }} else {{ empty_region() }},
            front,
            back,
            receiver,
            returned_final: returned,
            borrows_disjoint: front.start + front.length <= back.start,
            receiver_reassigned: true,
            initial_partition: split_partition(
                input.slice.source, receiver.values, returned.values,
            ),
            final_partition: split_partition(
                input.slice.source, receiver.values, returned.values,
            ),
            ordered_final: front.values + back.values,
            values_unchanged: true,
        }}
    }} else {{
        FinalState {{
            helper_has_split: helper_has_split(input),
            direction: helper_direction(input),
            split_index: helper_split_index(input),
            bounds_ok: false,
            take_performed: false,
            receiver_empty_after_take: false,
            taken: empty_region(),
            front: empty_region(),
            back: empty_region(),
            receiver: input_region(input),
            returned_final: empty_region(),
            borrows_disjoint: true,
            receiver_reassigned: false,
            initial_partition: true,
            final_partition: true,
            ordered_final: input.slice.source,
            values_unchanged: true,
        }}
    }}
}}

pub open spec fn split_partition(
    source: Seq<int>,
    remaining: Seq<int>,
    removed: Seq<int>,
) -> bool {{
    removed + remaining == source || remaining + removed == source
}}

pub open spec fn valid_input(input: Input) -> bool {{
    0 <= input.range_kind <= {END_INCLUSIVE}
        && input.range_index <= {MAX_USIZE}
        && input.slice.element_alignment > 0
}}

pub open spec fn boundary_holds(
    input: Input,
    boundary: Boundary,
) -> bool {{
    boundary.input_address == input.slice.address
        && boundary.input_allocation == input.slice.allocation
        && boundary.input_provenance == input.slice.provenance
        && boundary.parent_borrow == input.slice.parent_borrow
        && boundary.element_size == input.slice.element_size
        && boundary.element_alignment == input.slice.element_alignment
}}

pub open spec fn active_contract(
    input: Input,
    output: Output,
    state: FinalState,
) -> bool {{
{_verus_active_contract(config)}
}}

pub open spec fn target_transition(
    input: Input,
    boundary: Boundary,
    output: Output,
    state: FinalState,
) -> bool {{
    valid_input(input)
        && boundary_holds(input, boundary)
        && output == source_output(input)
        && state == source_state(input)
        && active_contract(input, output, state)
}}

pub open spec fn same_output(left: Output, right: Output) -> bool {{
    left == right
}}

pub open spec fn same_state(left: FinalState, right: FinalState) -> bool {{
    left == right
}}

pub proof fn conditional_complete_{function}(
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
        same_output(output1, output2),
        same_state(state1, state2),
{{
    reveal(target_transition);
    reveal(same_output);
    reveal(same_state);
}}

pub proof fn conditional_complete_exact_output_{function}(
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
        same_output(output1, output2),
{{
    reveal(target_transition);
    reveal(same_output);
}}

}} // verus!
"""
