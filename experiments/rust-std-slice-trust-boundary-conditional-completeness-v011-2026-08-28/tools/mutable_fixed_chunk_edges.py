#!/usr/bin/env python3
"""Source-backed obligations for mutable fixed-size Slice edge operations."""

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
RAW_SLICE_SOURCE_PATH = "core/src/slice/raw.rs"
RAW_SLICE_SOURCE_SHA256 = (
    "0914968067f7e2bc798680c1edd72bcb032a9fd44ebb2b6fbc082a3a2b16941f"
)
VOCABULARY_RANGES = ((916, 938),)
EMPTY_SEQ = "(as seq.empty (Seq Int))"


@dataclass(frozen=True)
class CanonicalSource:
    name: str
    path: str
    start: int
    end: int
    file_sha256: str
    filename: str
    fragments: tuple[str, ...]

    @property
    def reference(self) -> str:
        return f"{self.path}:{self.start}-{self.end}"


CANONICAL_SOURCES = {
    source.name: source
    for source in (
        CanonicalSource(
            name="slice_as_mut_ptr",
            path=SLICE_SOURCE_PATH,
            start=757,
            end=759,
            file_sha256=SLICE_SOURCE_SHA256,
            filename="canonical_slice_as_mut_ptr.rs",
            fragments=("self as *mut [T] as *mut T",),
        ),
        CanonicalSource(
            name="slice_split_at_mut",
            path=SLICE_SOURCE_PATH,
            start=1986,
            end=1991,
            file_sha256=SLICE_SOURCE_SHA256,
            filename="canonical_slice_split_at_mut.rs",
            fragments=(
                "match self.split_at_mut_checked(mid)",
                "Some(pair) => pair",
                'None => panic!("mid > len")',
            ),
        ),
        CanonicalSource(
            name="slice_split_at_mut_unchecked",
            path=SLICE_SOURCE_PATH,
            start=2092,
            end=2112,
            file_sha256=SLICE_SOURCE_SHA256,
            filename="canonical_slice_split_at_mut_unchecked.rs",
            fragments=(
                "let ptr = self.as_mut_ptr()",
                "mid <= len",
                "from_raw_parts_mut(ptr, mid)",
                "from_raw_parts_mut(ptr.add(mid), unchecked_sub(len, mid))",
            ),
        ),
        CanonicalSource(
            name="slice_split_at_mut_checked",
            path=SLICE_SOURCE_PATH,
            start=2192,
            end=2200,
            file_sha256=SLICE_SOURCE_SHA256,
            filename="canonical_slice_split_at_mut_checked.rs",
            fragments=(
                "if mid <= self.len()",
                "Some(unsafe { self.split_at_mut_unchecked(mid) })",
                "None",
            ),
        ),
        CanonicalSource(
            name="mut_ptr_add",
            path=MUT_PTR_SOURCE_PATH,
            start=909,
            end=962,
            file_sha256=MUT_PTR_SOURCE_SHA256,
            filename="canonical_mut_ptr_add.rs",
            fragments=("pub const unsafe fn add(self, count: usize) -> Self",),
        ),
        CanonicalSource(
            name="mut_ptr_cast_array",
            path=MUT_PTR_SOURCE_PATH,
            start=1999,
            end=2001,
            file_sha256=MUT_PTR_SOURCE_SHA256,
            filename="canonical_mut_ptr_cast_array.rs",
            fragments=(
                "pub const fn cast_array<const N: usize>(self) -> *mut [T; N]",
                "self.cast()",
            ),
        ),
        CanonicalSource(
            name="slice_from_raw_parts_mut",
            path=RAW_SLICE_SOURCE_PATH,
            start=179,
            end=196,
            file_sha256=RAW_SLICE_SOURCE_SHA256,
            filename="canonical_slice_from_raw_parts_mut.rs",
            fragments=(
                "pub const unsafe fn from_raw_parts_mut",
                "maybe_is_aligned_and_not_null",
                "&mut *ptr::slice_from_raw_parts_mut(data, len)",
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
class FixedChunkTarget:
    target: str
    input_order: str
    artifact_id: str
    kind: str
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
    all_trust_site_ids: tuple[str, ...]
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
    def excluded_trust_site_ids(self) -> tuple[str, ...]:
        context = set(self.context_only_trust_site_ids)
        return tuple(site for site in self.all_trust_site_ids if site not in context)

    @property
    def replacement_ids(self) -> tuple[str, ...]:
        return tuple(item.replacement_id for item in self.source_backed_replacements)

    @property
    def helper_sources(self) -> tuple[CanonicalSource, ...]:
        return tuple(CANONICAL_SOURCES[name] for name in self.helper_names)

    @property
    def source_citations(self) -> tuple[str, ...]:
        return tuple(
            dict.fromkeys(
                (
                    self.source_reference,
                    *(source.reference for source in self.helper_sources),
                )
            )
        )

    @property
    def array_is_prefix(self) -> bool:
        return self.kind == "split_first"

    @property
    def returns_other(self) -> bool:
        return self.kind != "last"

    @property
    def tuple_array_position(self) -> int:
        if self.kind == "last":
            return 0
        return 1 if self.kind == "split_first" else 2

    @property
    def active_conjuncts(self) -> tuple[str, ...]:
        common = (
            "ActiveSomeTagConjunct",
            "ActiveNoneTagConjunct",
            "ActiveArrayViewConjunct",
            "ActiveArrayLengthConjunct",
            "ActiveTupleOrientationConjunct",
            "ActiveSomeFinalFrameConjunct",
            "ActiveNoneFinalFrameConjunct",
            "ActiveRangeDisjointConjunct",
        )
        if self.returns_other:
            return common + ("ActiveOtherViewConjunct",)
        return common


COMMON_HELPERS = (
    "slice_as_mut_ptr",
    "slice_split_at_mut_unchecked",
    "slice_split_at_mut_checked",
    "mut_ptr_add",
    "mut_ptr_cast_array",
    "slice_from_raw_parts_mut",
)
LAST_CONTEXT = (
    "TS-062-D001",
    "TS-062-C001",
    "TS-062-C002",
    "TS-062-C003",
)
SPLIT_LAST_CONTEXT = (
    "TS-096-D001",
    "TS-096-C001",
    "TS-096-C002",
    "TS-096-C003",
)


TARGETS = (
    FixedChunkTarget(
        target="core::slice::last_chunk_mut",
        input_order="62",
        artifact_id="062_core_slice_last_chunk_mut",
        kind="last",
        active_contract_sha256=(
            "32a4497f959b05a42448f7ea2a070f4e3635c1b46d5c08628772d7601f9f9e57"
        ),
        active_contract_text=(
            "pub assume_specification<T, const N: usize>[ <[T]>::"
            "last_chunk_mut::<N> ]( slice: &mut [T], ) -> (ret: "
            "Option<&mut [T; N]>) ensures (N as int) <= old(slice)@.len() "
            "==> ret.is_some() && array_mut_ref_view(ret.unwrap()) == "
            "slice_fixed_suffix::<T, N>(old(slice)@) && final(slice)@ == "
            "old(slice)@.subrange(0, (old(slice)@.len() - N) as int) + "
            "array_value_view(*final(ret.unwrap())), (N as int) > "
            "old(slice)@.len() ==> ret.is_none() && final(slice)@ == "
            "old(slice)@, ;"
        ),
        source_start=539,
        source_end=548,
        docs_start=519,
        docs_end=535,
        source_item_sha256=(
            "cc48aeefd7888744bec1500626ba5bc1a4dc8e47df42e3d7e458d293f366ebd4"
        ),
        generated_declaration_sha256=(
            "315b1f1958cc910948a0e8821f6577ffa2348baef4301ff595797b14b1012238"
        ),
        harness_sha256=(
            "655375293532cd49660ea4330d29f016f144e7d661df6d548080753cdb1a700b"
        ),
        source_body_manifest_sha256=(
            "7f0adc8a3070044bb4fcf556adb06a53715d7179b1dbaf4a7a2a568e00e6d54d"
        ),
        transformation_manifest_sha256=(
            "28fc4bf7c140e6053fd1bd17e2efd2f3f2d6215077b41295ee6e917d0d597ccc"
        ),
        dependency_manifest_sha256=(
            "87dd95df9a4d15aeec04f4ade3c12bf1470a8023d3d39899067392430e155c5f"
        ),
        all_trust_site_ids=(
            "TS-062-D001",
            "TS-062-D002",
            "TS-062-D003",
            "TS-062-C001",
            "TS-062-C002",
            "TS-062-C003",
            "TS-062-E001",
        ),
        context_only_trust_site_ids=LAST_CONTEXT,
        helper_names=("slice_split_at_mut", *COMMON_HELPERS),
        source_fragments=(
            "let Some(index) = self.len().checked_sub(N) else { return None }",
            "let (_, last) = self.split_at_mut(index)",
            "Some(unsafe { &mut *(last.as_mut_ptr().cast_array()) })",
        ),
        source_backed_replacements=(
            SourceReplacement(
                replacement_id="SRC-062-CANONICAL-CHECKED-SPLIT",
                operation="checked_sub followed by canonical mutable raw-parts split",
                symbols=(
                    "BranchTransition",
                    "CheckedArithmeticTransition",
                    "RawPartsSplitTransition",
                    "UniqueBorrowTransition",
                ),
                replaces_trust_site_ids=("TS-062-D002",),
            ),
            SourceReplacement(
                replacement_id="SRC-062-CANONICAL-MUT-PTR-ARRAY-REF",
                operation="canonical as_mut_ptr, cast_array, and mutable dereference",
                symbols=(
                    "AsMutPtrTransition",
                    "CastArrayTransition",
                    "ArrayDereferenceTransition",
                    "TupleOrientationTransition",
                ),
                replaces_trust_site_ids=("TS-062-D003", "TS-062-E001"),
            ),
        ),
    ),
    FixedChunkTarget(
        target="core::slice::split_first_chunk_mut",
        input_order="90",
        artifact_id="090_core_slice_split_first_chunk_mut",
        kind="split_first",
        active_contract_sha256=(
            "eb599a67a0f7b786e404c9b3f97181b56e9b01bb82f3cc21822b93d2d46ab950"
        ),
        active_contract_text=(
            "pub assume_specification<T, const N: usize>[ <[T]>::"
            "split_first_chunk_mut::<N> ]( slice: &mut [T], ) -> (ret: "
            "Option<(&mut [T; N], &mut [T])>) ensures (N as int) <= "
            "old(slice)@.len() ==> ret.is_some() && "
            "array_mut_ref_view(ret.unwrap().0) == "
            "slice_fixed_prefix::<T, N>(old(slice)@) && ret.unwrap().1@ == "
            "old(slice)@.subrange(N as int, old(slice)@.len() as int) && "
            "final(slice)@ == array_value_view(*final(ret.unwrap().0)) + "
            "final(ret.unwrap().1)@, (N as int) > old(slice)@.len() ==> "
            "ret.is_none() && final(slice)@ == old(slice)@, ;"
        ),
        source_start=417,
        source_end=426,
        docs_start=395,
        docs_end=413,
        source_item_sha256=(
            "3be6504bdddb52013d9143e4e18804170bf42fae8db6e9404c432e967877e3ab"
        ),
        generated_declaration_sha256=(
            "fb22a7216f5fd30ce74eddca47abaebebb49efcac3d424779c467e8fa20dce7c"
        ),
        harness_sha256=(
            "a0267dfc672df4c2020cee1b3c35f05582001aec76b9f8c505978675c951909b"
        ),
        source_body_manifest_sha256=(
            "ceab6de1198b85daa4672b2257b163a76db13dbfd54025355cc25de1d084daa5"
        ),
        transformation_manifest_sha256=(
            "66831ecb168cd8dee0dc961f947f10a1db8493fc027bbde4ce52b607cfbd1b49"
        ),
        dependency_manifest_sha256=(
            "06520373dbb6363b1fc487af7343d80a796b78ecfaa301a43c916eabc577ff86"
        ),
        all_trust_site_ids=(
            "TS-090-D001",
            "TS-090-D002",
            "TS-090-D003",
            "TS-090-D004",
            "TS-090-E001",
            "TS-090-E002",
            "TS-090-E003",
            "TS-090-E004",
        ),
        context_only_trust_site_ids=("TS-090-D001",),
        helper_names=COMMON_HELPERS,
        source_fragments=(
            "let Some((first, tail)) = self.split_at_mut_checked(N) else",
            "Some((unsafe { &mut *(first.as_mut_ptr().cast_array()) }, tail))",
        ),
        source_backed_replacements=(
            SourceReplacement(
                replacement_id="SRC-090-CANONICAL-CHECKED-RAW-PARTS-SPLIT",
                operation="canonical checked split and mutable raw-parts partition",
                symbols=(
                    "BranchTransition",
                    "CheckedArithmeticTransition",
                    "RawPartsSplitTransition",
                    "UniqueBorrowTransition",
                ),
                replaces_trust_site_ids=(
                    "TS-090-D002",
                    "TS-090-E001",
                    "TS-090-E002",
                ),
            ),
            SourceReplacement(
                replacement_id="SRC-090-CANONICAL-MUT-PTR-ARRAY-REF",
                operation="canonical as_mut_ptr, cast_array, and mutable dereference",
                symbols=(
                    "AsMutPtrTransition",
                    "CastArrayTransition",
                    "ArrayDereferenceTransition",
                    "TupleOrientationTransition",
                ),
                replaces_trust_site_ids=(
                    "TS-090-D003",
                    "TS-090-D004",
                    "TS-090-E003",
                    "TS-090-E004",
                ),
            ),
        ),
    ),
    FixedChunkTarget(
        target="core::slice::split_last_chunk_mut",
        input_order="96",
        artifact_id="096_core_slice_split_last_chunk_mut",
        kind="split_last",
        active_contract_sha256=(
            "0c9131cd588a99217fc333ad32e54ac62deaf95cfc245fffb3523ba683296ce5"
        ),
        active_contract_text=(
            "pub assume_specification<T, const N: usize>[ <[T]>::"
            "split_last_chunk_mut::<N> ]( slice: &mut [T], ) -> (ret: "
            "Option<(&mut [T], &mut [T; N])>) ensures (N as int) <= "
            "old(slice)@.len() ==> ret.is_some() && ret.unwrap().0@ == "
            "old(slice)@.subrange(0, (old(slice)@.len() - N) as int) && "
            "array_mut_ref_view(ret.unwrap().1) == "
            "slice_fixed_suffix::<T, N>(old(slice)@) && final(slice)@ == "
            "final(ret.unwrap().0)@ + "
            "array_value_view(*final(ret.unwrap().1)), (N as int) > "
            "old(slice)@.len() ==> ret.is_none() && final(slice)@ == "
            "old(slice)@, ;"
        ),
        source_start=478,
        source_end=488,
        docs_start=456,
        docs_end=474,
        source_item_sha256=(
            "9b9156326fe8307c826a2e1599a682000caa3c60a78b9953c9e7b929dab147bd"
        ),
        generated_declaration_sha256=(
            "d63caa69d351c6a7bff2838ed5ad5c46d92a824f7b10f25e3256c42a0a2e20cb"
        ),
        harness_sha256=(
            "3eb054811b2d82a7c308e6481991aadae8da301428a41172695d920f67cec3e6"
        ),
        source_body_manifest_sha256=(
            "fd8b292a813c372fe17b72297b902cdc46a5ebeb8a2678a6ce7b9eb4da99de6f"
        ),
        transformation_manifest_sha256=(
            "5d61dd381ace9a6a9d455181303f673b0980d2b36ccaf55e7808930d5fa906d0"
        ),
        dependency_manifest_sha256=(
            "82f51875c2e94cf5f0cb1d5ccad20875b4fdfba658f625f4b899e0053145750a"
        ),
        all_trust_site_ids=(
            "TS-096-D001",
            "TS-096-D002",
            "TS-096-D003",
            "TS-096-C001",
            "TS-096-C002",
            "TS-096-C003",
            "TS-096-E001",
        ),
        context_only_trust_site_ids=SPLIT_LAST_CONTEXT,
        helper_names=("slice_split_at_mut", *COMMON_HELPERS),
        source_fragments=(
            "let Some(index) = self.len().checked_sub(N) else { return None }",
            "let (init, last) = self.split_at_mut(index)",
            "Some((init, unsafe { &mut *(last.as_mut_ptr().cast_array()) }))",
        ),
        source_backed_replacements=(
            SourceReplacement(
                replacement_id="SRC-096-CANONICAL-CHECKED-SPLIT",
                operation="checked_sub followed by canonical mutable raw-parts split",
                symbols=(
                    "BranchTransition",
                    "CheckedArithmeticTransition",
                    "RawPartsSplitTransition",
                    "UniqueBorrowTransition",
                ),
                replaces_trust_site_ids=("TS-096-D002",),
            ),
            SourceReplacement(
                replacement_id="SRC-096-CANONICAL-MUT-PTR-ARRAY-REF",
                operation="canonical as_mut_ptr, cast_array, and mutable dereference",
                symbols=(
                    "AsMutPtrTransition",
                    "CastArrayTransition",
                    "ArrayDereferenceTransition",
                    "TupleOrientationTransition",
                ),
                replaces_trust_site_ids=("TS-096-D003", "TS-096-E001"),
            ),
        ),
    ),
)
TARGET_BY_ARTIFACT = {config.artifact_id: config for config in TARGETS}
TARGET_KEYS = tuple((config.target, config.input_order) for config in TARGETS)


@dataclass(frozen=True)
class SourceCase:
    length: int
    n: int
    element_size: int


SOURCE_CASES = {
    "empty_n0": SourceCase(0, 0, 8),
    "empty_n_positive": SourceCase(0, 1, 8),
    "nonempty_n0": SourceCase(3, 0, 8),
    "n_greater_than_length": SourceCase(3, 4, 8),
    "n_equal_length": SourceCase(3, 3, 8),
    "strict_interior": SourceCase(5, 2, 8),
    "zst_equal_addresses": SourceCase(5, 2, 0),
}
NEGATIVE_PROBES = (
    "wrong_branching",
    "wrong_checked_arithmetic",
    "swapped_ranges",
    "swapped_tuple_order",
    "unchecked_array_length",
    "synthetic_null_provenance",
    "allocation_loss",
    "borrow_loss",
    "address_based_zst_disjointness",
    "missing_final_frame_composition",
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
    ("x_n", "Int"),
)
BOUNDARY_FIELDS = (
    ("b_input_address", "Int"),
    ("b_input_allocation", "Int"),
    ("b_input_provenance", "Int"),
    ("b_parent_borrow", "Int"),
    ("b_element_size", "Int"),
)
OUTPUT_FIELDS = (
    ("y_is_some", "Bool"),
    ("y_split_index", "Int"),
    ("y_tuple_array_position", "Int"),
    ("y_array_values", "(Seq Int)"),
    ("y_array_start", "Int"),
    ("y_array_length", "Int"),
    ("y_array_address", "Int"),
    ("y_array_allocation", "Int"),
    ("y_array_provenance", "Int"),
    ("y_array_parent_borrow", "Int"),
    ("y_array_element_size", "Int"),
    ("y_array_projection", "Int"),
    ("y_array_unique", "Bool"),
    ("y_other_values", "(Seq Int)"),
    ("y_other_start", "Int"),
    ("y_other_length", "Int"),
    ("y_other_address", "Int"),
    ("y_other_allocation", "Int"),
    ("y_other_provenance", "Int"),
    ("y_other_parent_borrow", "Int"),
    ("y_other_element_size", "Int"),
    ("y_other_projection", "Int"),
    ("y_other_unique", "Bool"),
)
STATE_FIELDS = (
    ("s_backing_values", "(Seq Int)"),
    ("s_backing_start", "Int"),
    ("s_backing_length", "Int"),
    ("s_backing_address", "Int"),
    ("s_backing_allocation", "Int"),
    ("s_backing_provenance", "Int"),
    ("s_backing_parent_borrow", "Int"),
    ("s_backing_element_size", "Int"),
    ("s_prefix_values", "(Seq Int)"),
    ("s_prefix_start", "Int"),
    ("s_prefix_length", "Int"),
    ("s_prefix_address", "Int"),
    ("s_prefix_allocation", "Int"),
    ("s_prefix_provenance", "Int"),
    ("s_prefix_parent_borrow", "Int"),
    ("s_prefix_element_size", "Int"),
    ("s_suffix_values", "(Seq Int)"),
    ("s_suffix_start", "Int"),
    ("s_suffix_length", "Int"),
    ("s_suffix_address", "Int"),
    ("s_suffix_allocation", "Int"),
    ("s_suffix_provenance", "Int"),
    ("s_suffix_parent_borrow", "Int"),
    ("s_suffix_element_size", "Int"),
    ("s_composed_final", "(Seq Int)"),
    ("s_unique_partition", "Bool"),
    ("s_elements_unchanged", "Bool"),
)
SOURCE_TRANSITIONS = (
    "BranchTransition",
    "CheckedArithmeticTransition",
    "RawPartsSplitTransition",
    "AsMutPtrTransition",
    "CastArrayTransition",
    "ArrayDereferenceTransition",
    "TupleOrientationTransition",
    "UniqueBorrowTransition",
    "FinalFrameTransition",
)
OUTPUT_SOURCE_TRANSITIONS = (
    "BranchTransition",
    "CheckedArithmeticTransition",
    "RawPartsOutputTransition",
    "AsMutPtrTransition",
    "CastArrayTransition",
    "ArrayDereferenceTransition",
    "TupleOrientationTransition",
    "UniqueBorrowOutputTransition",
)


def _normalized(text: str) -> str:
    return " ".join(text.split())


def validate_source_anchors(
    config: FixedChunkTarget,
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
    required_vocabulary = (
        "pub open spec fn array_mut_ref_view",
        "pub open spec fn array_value_view",
        (
            "pub open spec fn slice_fixed_prefix"
            if config.array_is_prefix
            else "pub open spec fn slice_fixed_suffix"
        ),
    )
    normalized_vocabulary = _normalized(vocabulary)
    for fragment in required_vocabulary:
        if _normalized(fragment) not in normalized_vocabulary:
            raise GuardError(
                f"{config.target}: shared vocabulary fragment changed: {fragment}"
            )
    if set(helpers) != set(config.helper_names):
        raise GuardError(f"{config.target}: canonical helper set changed")
    for helper in config.helper_sources:
        normalized_helper = _normalized(helpers[helper.name])
        for fragment in helper.fragments:
            if _normalized(fragment) not in normalized_helper:
                raise GuardError(
                    f"{config.target}: {helper.name} fragment changed: {fragment}"
                )
    prohibited = (
        "slice_start_mut_ptr",
        "Provenance::null()",
        "null_mut::<T>().with_addr",
    )
    combined = " ".join(_normalized(text) for text in helpers.values())
    if any(token in combined for token in prohibited):
        raise GuardError(
            f"{config.target}: synthetic pointer helper entered canonical sources"
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


def _success() -> str:
    return "(<= (x_n x) (x_length x))"


def _split_index(config: FixedChunkTarget) -> str:
    if config.kind == "split_first":
        return "(x_n x)"
    return "(- (x_length x) (x_n x))"


def _array_offset(config: FixedChunkTarget) -> str:
    return "0" if config.array_is_prefix else _split_index(config)


def _other_offset(config: FixedChunkTarget) -> str:
    return "(x_n x)" if config.kind == "split_first" else "0"


def _other_length(config: FixedChunkTarget) -> str:
    if config.kind == "split_first":
        return "(- (x_length x) (x_n x))"
    if config.kind == "split_last":
        return _split_index(config)
    return "0"


def _region_values(offset: str, length: str) -> str:
    return f"(seq.extract (x_source x) {offset} {length})"


def _region_address(offset: str) -> str:
    return f"(+ (x_address x) (* {offset} (x_element_size x)))"


def _input_boundary_observed() -> str:
    return """\
(define-fun InputBoundaryObserved ((x Input) (b Boundary)) Bool
  (and (= (b_input_address b) (x_address x))
       (= (b_input_allocation b) (x_allocation x))
       (= (b_input_provenance b) (x_provenance x))
       (= (b_parent_borrow b) (x_parent_borrow x))
       (= (b_element_size b) (x_element_size x))))"""


def _branch_transition() -> str:
    return f"""\
(define-fun BranchTransition ((x Input) (y Output)) Bool
  (= (y_is_some y) {_success()}))"""


def _checked_arithmetic_transition(config: FixedChunkTarget) -> str:
    return f"""\
(define-fun CheckedArithmeticTransition ((x Input) (y Output)) Bool
  (= (y_split_index y)
     (ite {_success()} {_split_index(config)} (- 1))))"""


def _raw_parts_split_transition(config: FixedChunkTarget) -> str:
    split = _split_index(config)
    prefix_values = _region_values("0", split)
    suffix_values = _region_values(split, f"(- (x_length x) {split})")
    if config.returns_other:
        other_offset = _other_offset(config)
        other_length = _other_length(config)
        other = f"""\
       (= (y_other_values y) {_region_values(other_offset, other_length)})
       (= (y_other_start y) (+ (x_start x) {other_offset}))
       (= (y_other_length y) {other_length})
       (= (y_other_address y) {_region_address(other_offset)})
       (= (y_other_allocation y) (x_allocation x))
       (= (y_other_provenance y) (x_provenance x))
       (= (y_other_parent_borrow y) (x_parent_borrow x))
       (= (y_other_element_size y) (x_element_size x))
       (= (y_other_projection y) 2)"""
    else:
        other = f"""\
       (= (y_other_values y) {EMPTY_SEQ})
       (= (y_other_start y) 0)
       (= (y_other_length y) 0)
       (= (y_other_address y) 0)
       (= (y_other_allocation y) 0)
       (= (y_other_provenance y) 0)
       (= (y_other_parent_borrow y) 0)
       (= (y_other_element_size y) 0)
       (= (y_other_projection y) 0)"""
    success = f"""\
       {other}
       (= (s_prefix_values s) {prefix_values})
       (= (s_prefix_start s) (x_start x))
       (= (s_prefix_length s) {split})
       (= (s_prefix_address s) (x_address x))
       (= (s_prefix_allocation s) (x_allocation x))
       (= (s_prefix_provenance s) (x_provenance x))
       (= (s_prefix_parent_borrow s) (x_parent_borrow x))
       (= (s_prefix_element_size s) (x_element_size x))
       (= (s_suffix_values s) {suffix_values})
       (= (s_suffix_start s) (+ (x_start x) {split}))
       (= (s_suffix_length s) (- (x_length x) {split}))
       (= (s_suffix_address s) {_region_address(split)})
       (= (s_suffix_allocation s) (x_allocation x))
       (= (s_suffix_provenance s) (x_provenance x))
       (= (s_suffix_parent_borrow s) (x_parent_borrow x))
       (= (s_suffix_element_size s) (x_element_size x))"""
    inactive = f"""\
       (= (y_other_values y) {EMPTY_SEQ})
       (= (y_other_start y) 0)
       (= (y_other_length y) 0)
       (= (y_other_address y) 0)
       (= (y_other_allocation y) 0)
       (= (y_other_provenance y) 0)
       (= (y_other_parent_borrow y) 0)
       (= (y_other_element_size y) 0)
       (= (y_other_projection y) 0)
       (= (s_prefix_values s) {EMPTY_SEQ})
       (= (s_prefix_start s) 0)
       (= (s_prefix_length s) 0)
       (= (s_prefix_address s) 0)
       (= (s_prefix_allocation s) 0)
       (= (s_prefix_provenance s) 0)
       (= (s_prefix_parent_borrow s) 0)
       (= (s_prefix_element_size s) 0)
       (= (s_suffix_values s) {EMPTY_SEQ})
       (= (s_suffix_start s) 0)
       (= (s_suffix_length s) 0)
       (= (s_suffix_address s) 0)
       (= (s_suffix_allocation s) 0)
       (= (s_suffix_provenance s) 0)
       (= (s_suffix_parent_borrow s) 0)
       (= (s_suffix_element_size s) 0)"""
    return f"""\
(define-fun RawPartsSplitTransition
  ((x Input) (y Output) (s State)) Bool
  (ite {_success()}
       (and {success})
       (and {inactive})))"""


def _raw_parts_output_transition(config: FixedChunkTarget) -> str:
    if config.returns_other:
        offset = _other_offset(config)
        length = _other_length(config)
        success = f"""\
       (= (y_other_values y) {_region_values(offset, length)})
       (= (y_other_start y) (+ (x_start x) {offset}))
       (= (y_other_length y) {length})
       (= (y_other_address y) {_region_address(offset)})
       (= (y_other_allocation y) (x_allocation x))
       (= (y_other_provenance y) (x_provenance x))
       (= (y_other_parent_borrow y) (x_parent_borrow x))
       (= (y_other_element_size y) (x_element_size x))
       (= (y_other_projection y) 2)"""
    else:
        success = f"""\
       (= (y_other_values y) {EMPTY_SEQ})
       (= (y_other_start y) 0)
       (= (y_other_length y) 0)
       (= (y_other_address y) 0)
       (= (y_other_allocation y) 0)
       (= (y_other_provenance y) 0)
       (= (y_other_parent_borrow y) 0)
       (= (y_other_element_size y) 0)
       (= (y_other_projection y) 0)"""
    inactive = f"""\
       (= (y_other_values y) {EMPTY_SEQ})
       (= (y_other_start y) 0)
       (= (y_other_length y) 0)
       (= (y_other_address y) 0)
       (= (y_other_allocation y) 0)
       (= (y_other_provenance y) 0)
       (= (y_other_parent_borrow y) 0)
       (= (y_other_element_size y) 0)
       (= (y_other_projection y) 0)"""
    return f"""\
(define-fun RawPartsOutputTransition ((x Input) (y Output)) Bool
  (ite {_success()}
       (and {success})
       (and {inactive})))"""


def _as_mut_ptr_transition(config: FixedChunkTarget) -> str:
    offset = _array_offset(config)
    return f"""\
(define-fun AsMutPtrTransition ((x Input) (y Output)) Bool
  (ite {_success()}
       (and (= (y_array_address y) {_region_address(offset)})
            (= (y_array_allocation y) (x_allocation x))
            (= (y_array_provenance y) (x_provenance x)))
       (and (= (y_array_address y) 0)
            (= (y_array_allocation y) 0)
            (= (y_array_provenance y) 0))))"""


def _cast_array_transition() -> str:
    return f"""\
(define-fun CastArrayTransition ((x Input) (y Output)) Bool
  (ite {_success()}
       (and (= (y_array_length y) (x_n x))
            (= (y_array_projection y) 1))
       (and (= (y_array_length y) 0)
            (= (y_array_projection y) 0))))"""


def _array_dereference_transition(config: FixedChunkTarget) -> str:
    offset = _array_offset(config)
    return f"""\
(define-fun ArrayDereferenceTransition ((x Input) (y Output)) Bool
  (ite {_success()}
       (and (= (y_array_values y) {_region_values(offset, "(x_n x)")})
            (= (y_array_start y) (+ (x_start x) {offset}))
            (= (y_array_parent_borrow y) (x_parent_borrow x))
            (= (y_array_element_size y) (x_element_size x)))
       (and (= (y_array_values y) {EMPTY_SEQ})
            (= (y_array_start y) 0)
            (= (y_array_parent_borrow y) 0)
            (= (y_array_element_size y) 0))))"""


def _tuple_orientation_transition(config: FixedChunkTarget) -> str:
    return f"""\
(define-fun TupleOrientationTransition ((x Input) (y Output)) Bool
  (= (y_tuple_array_position y)
     (ite {_success()} {config.tuple_array_position} (- 1))))"""


def _unique_borrow_transition(config: FixedChunkTarget) -> str:
    other_unique = "true" if config.returns_other else "false"
    return f"""\
(define-fun UniqueBorrowTransition
  ((x Input) (y Output) (s State)) Bool
  (ite {_success()}
       (and (= (y_array_unique y) true)
            (= (y_other_unique y) {other_unique})
            (= (s_unique_partition s)
               (or (= (s_prefix_length s) 0)
                   (= (s_suffix_length s) 0)
                   (<= (+ (s_prefix_start s) (s_prefix_length s))
                       (s_suffix_start s)))))
       (and (= (y_array_unique y) false)
            (= (y_other_unique y) false)
            (= (s_unique_partition s) true))))"""


def _unique_borrow_output_transition(config: FixedChunkTarget) -> str:
    other_unique = "true" if config.returns_other else "false"
    return f"""\
(define-fun UniqueBorrowOutputTransition ((x Input) (y Output)) Bool
  (ite {_success()}
       (and (= (y_array_unique y) true)
            (= (y_other_unique y) {other_unique}))
       (and (= (y_array_unique y) false)
            (= (y_other_unique y) false))))"""


def _final_frame_transition() -> str:
    return """\
(define-fun FinalFrameTransition ((x Input) (y Output) (s State)) Bool
  (and (= (s_backing_values s) (x_source x))
       (= (s_backing_start s) (x_start x))
       (= (s_backing_length s) (x_length x))
       (= (s_backing_address s) (x_address x))
       (= (s_backing_allocation s) (x_allocation x))
       (= (s_backing_provenance s) (x_provenance x))
       (= (s_backing_parent_borrow s) (x_parent_borrow x))
       (= (s_backing_element_size s) (x_element_size x))
       (= (s_composed_final s) (x_source x))
       (= (s_elements_unchanged s) true)))"""


def _active_contract_definitions(config: FixedChunkTarget) -> str:
    array_offset = _array_offset(config)
    array_values = _region_values(array_offset, "(x_n x)")
    if config.kind == "last":
        composition = (
            f"(seq.++ {_region_values('0', _split_index(config))} "
            "(y_array_values y))"
        )
    elif config.kind == "split_first":
        composition = "(seq.++ (y_array_values y) (y_other_values y))"
    else:
        composition = "(seq.++ (y_other_values y) (y_array_values y))"
    definitions = f"""\
(define-fun ActiveSomeTagConjunct ((x Input) (y Output)) Bool
  (=> {_success()} (y_is_some y)))
(define-fun ActiveNoneTagConjunct ((x Input) (y Output)) Bool
  (=> (> (x_n x) (x_length x)) (not (y_is_some y))))
(define-fun ActiveArrayViewConjunct ((x Input) (y Output)) Bool
  (=> {_success()} (= (y_array_values y) {array_values})))
(define-fun ActiveArrayLengthConjunct ((x Input) (y Output)) Bool
  (=> {_success()} (= (y_array_length y) (x_n x))))
(define-fun ActiveTupleOrientationConjunct ((x Input) (y Output)) Bool
  (=> {_success()}
      (= (y_tuple_array_position y) {config.tuple_array_position})))
(define-fun ActiveSomeFinalFrameConjunct
  ((x Input) (y Output) (s State)) Bool
  (=> {_success()}
      (and (= (s_composed_final s) {composition})
           (= (s_backing_values s) (s_composed_final s)))))
(define-fun ActiveNoneFinalFrameConjunct
  ((x Input) (s State)) Bool
  (=> (> (x_n x) (x_length x))
      (and (= (s_backing_values s) (x_source x))
           (= (s_composed_final s) (x_source x)))))
(define-fun ActiveRangeDisjointConjunct ((x Input) (s State)) Bool
  (=> {_success()}
      (or (= (s_prefix_length s) 0)
          (= (s_suffix_length s) 0)
          (<= (+ (s_prefix_start s) (s_prefix_length s))
              (s_suffix_start s)))))"""
    if config.returns_other:
        other_values = _region_values(
            _other_offset(config), _other_length(config)
        )
        definitions += f"""\

(define-fun ActiveOtherViewConjunct ((x Input) (y Output)) Bool
  (=> {_success()} (= (y_other_values y) {other_values})))"""
    return definitions


def _target_source_transition(config: FixedChunkTarget) -> str:
    calls = (
        "(InputBoundaryObserved x b)",
        "(BranchTransition x y)",
        "(CheckedArithmeticTransition x y)",
        "(RawPartsSplitTransition x y s)",
        "(AsMutPtrTransition x y)",
        "(CastArrayTransition x y)",
        "(ArrayDereferenceTransition x y)",
        "(TupleOrientationTransition x y)",
        "(UniqueBorrowTransition x y s)",
        "(FinalFrameTransition x y s)",
    )
    return """\
(define-fun TargetSourceTransition
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and %s))""" % "\n       ".join(calls)


def _requires() -> str:
    return """\
(define-fun Requires_T ((x Input)) Bool
  (and (= (x_length x) (seq.len (x_source x)))
       (>= (x_length x) 0)
       (>= (x_start x) 0)
       (> (x_address x) 0)
       (>= (x_allocation x) 0)
       (>= (x_provenance x) 0)
       (> (x_parent_borrow x) 0)
       (>= (x_element_size x) 0)
       (>= (x_n x) 0)
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
       (or (= (* (x_length x) (x_element_size x)) 0)
           (and (> (b_input_allocation b) 0)
                (> (b_input_provenance b) 0)))
       (InputBoundaryObserved x b)))"""


def _target_definition(config: FixedChunkTarget, purpose: str) -> str:
    direct_calls = [
        "(InputBoundaryObserved x b)",
        "(BranchTransition x y)",
        "(CheckedArithmeticTransition x y)",
        (
            "(RawPartsOutputTransition x y)"
            if purpose == EXACT_OUTPUT
            else "(RawPartsSplitTransition x y s)"
        ),
        "(AsMutPtrTransition x y)",
        "(CastArrayTransition x y)",
        "(ArrayDereferenceTransition x y)",
        "(TupleOrientationTransition x y)",
        (
            "(UniqueBorrowOutputTransition x y)"
            if purpose == EXACT_OUTPUT
            else "(UniqueBorrowTransition x y s)"
        ),
    ]
    state = "s" if purpose == PRIMARY else "f"
    active_calls = [
        f"({name} x y {state})"
        if name in {
            "ActiveSomeFinalFrameConjunct",
        }
        else f"({name} x {state})"
        if name in {
            "ActiveNoneFinalFrameConjunct",
            "ActiveRangeDisjointConjunct",
        }
        else f"({name} x y)"
        for name in config.active_conjuncts
    ]
    state_calls = [f"(FinalFrameTransition x y {state})", *active_calls]
    if purpose == EXACT_OUTPUT:
        state_calls = [
            "(RawPartsSplitTransition x y f)",
            "(UniqueBorrowTransition x y f)",
            *state_calls,
        ]
    if purpose == EXACT_OUTPUT:
        body = (
            "\n       ".join(direct_calls)
            + "\n       (exists ((f FrameState))\n"
            + "         (and "
            + "\n              ".join(state_calls)
            + "))"
        )
    else:
        body = "\n       ".join(direct_calls + state_calls)
    return """\
(define-fun TargetDefinition_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and %s))""" % body


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
    config: FixedChunkTarget,
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
            _branch_transition(),
            _checked_arithmetic_transition(config),
            _frame_adapt(_raw_parts_split_transition(config), purpose),
            *(
                (_raw_parts_output_transition(config),)
                if purpose == EXACT_OUTPUT
                else ()
            ),
            _as_mut_ptr_transition(config),
            _cast_array_transition(),
            _array_dereference_transition(config),
            _tuple_orientation_transition(config),
            _frame_adapt(_unique_borrow_transition(config), purpose),
            *(
                (_unique_borrow_output_transition(config),)
                if purpose == EXACT_OUTPUT
                else ()
            ),
            _frame_adapt(_final_frame_transition(), purpose),
            _frame_adapt(_active_contract_definitions(config), purpose),
        )
    )
    return f"""\
; Target: {config.target}
; Active contract SHA-256: {config.active_contract_sha256}
; Purpose: {purpose}
; N is shared input. The boundary contains only the initial slice address,
; allocation, provenance, unique parent borrow, and element layout.
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


def obligation_text(config: FixedChunkTarget, purpose: str) -> str:
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
    config: FixedChunkTarget,
    purpose: str = PRIMARY,
) -> list[dict[str, Any]]:
    substitutions = (
        {
            "RawPartsSplitTransition": "RawPartsOutputTransition",
            "UniqueBorrowTransition": "UniqueBorrowOutputTransition",
        }
        if purpose == EXACT_OUTPUT
        else {}
    )
    return [
        {
            "replacement_id": replacement.replacement_id,
            "operation": replacement.operation,
            "symbols": [
                substitutions.get(symbol, symbol)
                for symbol in replacement.symbols
            ],
            "source_citations": list(config.source_citations),
            "replaces_trust_site_ids": list(
                replacement.replaces_trust_site_ids
            ),
        }
        for replacement in config.source_backed_replacements
    ]


def _boundary_metadata(config: FixedChunkTarget) -> list[dict[str, Any]]:
    roles = {
        "b_input_address": "input_memory",
        "b_input_allocation": "input_provenance",
        "b_input_provenance": "input_provenance",
        "b_parent_borrow": "input_provenance",
        "b_element_size": "input_layout",
    }
    return [
        {
            "selector": selector,
            "role": roles[selector],
            "meaning": {
                "b_input_address": "initial non-null slice data address",
                "b_input_allocation": "initial allocation identity",
                "b_input_provenance": "initial pointer provenance",
                "b_parent_borrow": "initial unique parent-borrow identity",
                "b_element_size": "element size, including zero",
            }[selector],
            "source_citations": list(config.source_citations),
            "trust_site_ids": [],
            "source_backed_replacement_ids": list(config.replacement_ids),
        }
        for selector, _ in BOUNDARY_FIELDS
    ]


def obligation_metadata(
    config: FixedChunkTarget,
    purpose: str,
) -> dict[str, Any]:
    if purpose not in PURPOSES:
        raise ValueError(f"{config.target}: unknown purpose {purpose}")
    source_transitions = list(
        OUTPUT_SOURCE_TRANSITIONS
        if purpose == EXACT_OUTPUT
        else SOURCE_TRANSITIONS
    )
    return {
        "schema_version": 3,
        "target": config.target,
        "input_order": config.input_order,
        "obligation_purpose": purpose,
        "active_contract_sha256": config.active_contract_sha256,
        "active_contract_text": config.active_contract_text,
        "model_status": "source-backed-complete",
        "domain": {
            "slice_length": "arbitrary nonnegative integer",
            "array_length_n": "arbitrary nonnegative integer in shared input x",
            "element_size": (
                "arbitrary nonnegative integer; empty and nonempty ZST slices "
                "are included"
            ),
            "source_model_complete": True,
        },
        "active_contract_conjuncts": list(config.active_conjuncts),
        "contract_translation": {
            "branch": "Some exactly when N <= len; otherwise None",
            "checked_index": (
                "N through split_at_mut_checked"
                if config.kind == "split_first"
                else "checked subtraction len - N"
            ),
            "array_region": (
                "fixed prefix [0,N)"
                if config.array_is_prefix
                else "fixed suffix [len-N,len)"
            ),
            "tuple_orientation": config.tuple_array_position,
            "immediate_final_frame": (
                "prefix and suffix preserve their initial values and compose "
                "to the parent slice"
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
                "N, which belongs to shared input x",
                "branch result and checked subtraction or split index",
                "prefix, suffix, array, and tuple orientation",
                "returned references and unique derived borrows",
                "output and aggregate final state",
                "answer-equivalent encoding and execution trace",
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
        "source_transition_definitions": source_transitions,
        "source_transition_bindings": {
            "public_target": {
                "operation": config.target,
                "source_citations": [config.source_reference],
            },
            "checked_branch_and_index": {
                "symbols": [
                    "BranchTransition",
                    "CheckedArithmeticTransition",
                ],
                "source_citations": [config.source_reference],
            },
            "canonical_raw_parts_split": {
                "symbols": [
                    (
                        "RawPartsOutputTransition"
                        if purpose == EXACT_OUTPUT
                        else "RawPartsSplitTransition"
                    ),
                    (
                        "UniqueBorrowOutputTransition"
                        if purpose == EXACT_OUTPUT
                        else "UniqueBorrowTransition"
                    ),
                ],
                "source_citations": [
                    source.reference
                    for source in config.helper_sources
                    if "split_at_mut" in source.name
                    or source.name
                    in {"mut_ptr_add", "slice_from_raw_parts_mut"}
                ],
            },
            "canonical_array_reference_chain": {
                "symbols": [
                    "AsMutPtrTransition",
                    "CastArrayTransition",
                    "ArrayDereferenceTransition",
                    "TupleOrientationTransition",
                ],
                "source_citations": [
                    config.source_reference,
                    *(
                        source.reference
                        for source in config.helper_sources
                        if source.name
                        in {"slice_as_mut_ptr", "mut_ptr_cast_array"}
                    ),
                ],
            },
            "immediate_final_frame": {
                "symbols": ["FinalFrameTransition"],
                "source_citations": [config.source_reference],
            },
        },
        "equivalence_kind": "exact",
        "equivalence_scope": (
            "every principal return/reference identity and every immediate "
            "final-state observation"
            if purpose == PRIMARY
            else "every principal return/reference identity"
        ),
        "principal_observations": _principal_observations(purpose),
        "expected_solver_result": "unsat",
    }


def obligation(
    config: FixedChunkTarget,
    purpose: str,
) -> tuple[str, dict[str, Any]]:
    return obligation_text(config, purpose), obligation_metadata(config, purpose)


def validate_target_obligation(
    config: FixedChunkTarget,
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
            f"{config.target}: metadata differs from reviewed fixed-chunk model"
        )
    if parse_smt(text) != parse_smt(expected_text):
        raise GuardError(
            f"{config.target}: SMT differs from reviewed fixed-chunk model"
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
        "(assert (= (x_address x) 1000))",
        "(assert (= (x_allocation x) 11))",
        "(assert (= (x_provenance x) 13))",
        "(assert (= (x_parent_borrow x) 17))",
        f"(assert (= (x_element_size x) {case.element_size}))",
        f"(assert (= (x_n x) {case.n}))",
    ]


def _model_query() -> str:
    terms = [
        "(x_length x)",
        "(x_n x)",
        "(x_element_size x)",
        *(f"({selector} y1)" for selector, _ in OUTPUT_FIELDS),
        *(f"({selector} s1)" for selector, _ in STATE_FIELDS),
    ]
    return "(get-value (\n  %s))" % "\n  ".join(terms)


def source_instance_text(
    config: FixedChunkTarget,
    case: SourceCase,
    *,
    extra_assertions: tuple[str, ...] = (),
) -> str:
    if case.length < 0 or case.n < 0 or case.element_size < 0:
        raise ValueError("fixed-chunk source cases require nonnegative inputs")
    assertions = [
        *_fixed_input_assertions(case),
        "(assert (Requires_T x))",
        "(assert (Boundary_T x b))",
        "(assert (Spec_T x b y1 s1))",
    ]
    if case == SOURCE_CASES["zst_equal_addresses"]:
        assertions.append(
            "(assert (= (s_prefix_address s1) (s_suffix_address s1)))"
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


def negative_probe_text(config: FixedChunkTarget, name: str) -> str:
    if name not in NEGATIVE_PROBES:
        raise ValueError(f"unknown fixed-chunk negative probe: {name}")
    case = (
        SOURCE_CASES["zst_equal_addresses"]
        if name == "address_based_zst_disjointness"
        else SOURCE_CASES["strict_interior"]
    )
    expected_index = _split_index(config)
    expected_array_start = f"(+ (x_start x) {_array_offset(config)})"
    contradictions = {
        "wrong_branching": (
            "(not (= (y_is_some y1) (<= (x_n x) (x_length x))))"
        ),
        "wrong_checked_arithmetic": (
            f"(not (= (y_split_index y1) {expected_index}))"
        ),
        "swapped_ranges": (
            f"(not (= (y_array_start y1) {expected_array_start}))"
        ),
        "swapped_tuple_order": (
            f"(not (= (y_tuple_array_position y1) "
            f"{config.tuple_array_position}))"
        ),
        "unchecked_array_length": (
            "(not (= (y_array_length y1) (x_n x)))"
        ),
        "synthetic_null_provenance": (
            "(= (y_array_provenance y1) 0)"
        ),
        "allocation_loss": (
            "(not (= (y_array_allocation y1) (x_allocation x)))"
        ),
        "borrow_loss": (
            "(not (= (y_array_parent_borrow y1) (x_parent_borrow x)))"
        ),
        "address_based_zst_disjointness": (
            "(distinct (s_prefix_address s1) (s_suffix_address s1))"
        ),
        "missing_final_frame_composition": (
            "(not (= (s_composed_final s1) (x_source x)))"
        ),
    }
    return (
        _model_text(config, PRIMARY, include_theorem=False)
        + "\n"
        + "\n".join(
            (
                *_fixed_input_assertions(case),
                "(assert (Requires_T x))",
                "(assert (Boundary_T x b))",
                "(assert (Spec_T x b y1 s1))",
                f"(assert {contradictions[name]})",
            )
        )
        + "\n(check-sat)\n"
    )


def boundary_manifest(config: FixedChunkTarget) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "target": config.target,
        "input_order": config.input_order,
        "boundary_narrower_than_target": True,
        "proof_boundary_assumption": (
            "The same initial non-null slice address, allocation, provenance, "
            "unique parent-borrow identity, and element size are observed in "
            "both executions. N is shared input x, not a boundary observation."
        ),
        "shared_boundary_observations": _boundary_metadata(config),
        "canonical_source_transition": {
            "branch": "N <= len",
            "checked_index": (
                "N"
                if config.kind == "split_first"
                else "len - N after checked_sub"
            ),
            "split": "[0,index) and [index,len)",
            "array_region": (
                "prefix"
                if config.array_is_prefix
                else "suffix"
            ),
            "tuple_array_position": config.tuple_array_position,
            "pointer_chain": (
                "canonical slice as_mut_ptr -> raw-parts split -> "
                "cast_array -> mutable dereference"
            ),
            "reference_identity": (
                "address, allocation, provenance, parent borrow, element "
                "range, layout, and projection"
            ),
            "zst_disjointness": (
                "range-based; nonempty disjoint regions may have equal addresses"
            ),
            "immediate_final_frame": "unchanged prefix + unchanged suffix",
        },
        "source_backed_replacements": _source_backed_replacements(config),
        "context_only_trust_site_ids": list(
            config.context_only_trust_site_ids
        ),
        "excluded_retained_trust_site_ids": list(
            config.excluded_trust_site_ids
        ),
        "all_audited_trust_site_ids": list(config.all_trust_site_ids),
        "excluded_from_boundary": [
            "N",
            "branch result, subtraction, and split index",
            "prefix/suffix ranges and tuple orientation",
            "array view and returned reference identities",
            "derived borrows and immediate final state",
            "answers, answer encodings, and traces",
        ],
    }


def verus_text(config: FixedChunkTarget) -> str:
    function = config.function_name
    array_prefix = "true" if config.array_is_prefix else "false"
    returns_other = "true" if config.returns_other else "false"
    split_expression = (
        "input.n as int"
        if config.kind == "split_first"
        else "input.slice.source.len() as int - input.n as int"
    )
    other_expression = (
        "suffix"
        if config.kind == "split_first"
        else "prefix"
        if config.kind == "split_last"
        else "empty_region()"
    )
    array_expression = "prefix" if config.array_is_prefix else "suffix"
    tuple_position = config.tuple_array_position
    composition = (
        "state.prefix.values + output.array.values"
        if config.kind == "last"
        else "output.array.values + output.other.values"
        if config.kind == "split_first"
        else "output.other.values + output.array.values"
    )
    return f"""\
#![allow(dead_code, unused_imports, unused_variables)]
// Source-backed mutable fixed-chunk model for {config.target}.

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
    pub projection: int,
    pub unique: bool,
}}

pub ghost struct RawPointerIdentity {{
    pub address: int,
    pub allocation: int,
    pub provenance: int,
    pub parent_borrow: int,
    pub element_size: nat,
}}

pub ghost struct ArrayPointerIdentity {{
    pub raw: RawPointerIdentity,
    pub length: nat,
}}

pub ghost struct Input {{
    pub slice: SliceIdentity,
    pub n: nat,
}}

pub ghost struct Boundary {{
    pub input_address: int,
    pub input_allocation: int,
    pub input_provenance: int,
    pub parent_borrow: int,
    pub element_size: nat,
}}

pub ghost struct Output {{
    pub is_some: bool,
    pub split_index: int,
    pub tuple_array_position: int,
    pub array: RegionIdentity,
    pub other: RegionIdentity,
}}

pub ghost struct FinalState {{
    pub backing: SliceIdentity,
    pub prefix: RegionIdentity,
    pub suffix: RegionIdentity,
    pub composed_final: Seq<int>,
    pub unique_partition: bool,
    pub elements_unchanged: bool,
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
        projection: 0,
        unique: false,
    }}
}}

pub open spec fn make_region(
    slice: SliceIdentity,
    offset: int,
    length: int,
    projection: int,
) -> RegionIdentity {{
    RegionIdentity {{
        values: slice.source.subrange(offset, offset + length),
        start: slice.start + offset,
        length,
        address: slice.address + offset * slice.element_size as int,
        allocation: slice.allocation,
        provenance: slice.provenance,
        parent_borrow: slice.parent_borrow,
        element_size: slice.element_size,
        projection,
        unique: true,
    }}
}}

pub open spec fn branch_succeeds(input: Input) -> bool {{
    input.n <= input.slice.source.len()
}}

pub open spec fn checked_sub_or_split_index(input: Input) -> int {{
    if branch_succeeds(input) {{
        {split_expression}
    }} else {{
        -1
    }}
}}

pub open spec fn raw_parts_split(
    input: Input,
) -> (RegionIdentity, RegionIdentity) {{
    let split = checked_sub_or_split_index(input);
    (
        make_region(input.slice, 0, split, 2),
        make_region(
            input.slice,
            split,
            input.slice.source.len() as int - split,
            2,
        ),
    )
}}

pub open spec fn as_mut_ptr_transition(
    region: RegionIdentity,
) -> RawPointerIdentity {{
    RawPointerIdentity {{
        address: region.address,
        allocation: region.allocation,
        provenance: region.provenance,
        parent_borrow: region.parent_borrow,
        element_size: region.element_size,
    }}
}}

pub open spec fn cast_array_transition(
    raw: RawPointerIdentity,
    n: nat,
) -> ArrayPointerIdentity {{
    ArrayPointerIdentity {{ raw, length: n }}
}}

pub open spec fn dereference_array_transition(
    region: RegionIdentity,
    ptr: ArrayPointerIdentity,
) -> RegionIdentity {{
    RegionIdentity {{
        values: region.values,
        start: region.start,
        length: ptr.length as int,
        address: ptr.raw.address,
        allocation: ptr.raw.allocation,
        provenance: ptr.raw.provenance,
        parent_borrow: ptr.raw.parent_borrow,
        element_size: ptr.raw.element_size,
        projection: 1,
        unique: true,
    }}
}}

pub open spec fn source_output(input: Input) -> Output {{
    if branch_succeeds(input) {{
        let pair = raw_parts_split(input);
        let prefix = pair.0;
        let suffix = pair.1;
        let array_region = if {array_prefix} {{ prefix }} else {{ suffix }};
        let raw = as_mut_ptr_transition(array_region);
        let array_ptr = cast_array_transition(raw, input.n);
        let array = dereference_array_transition(array_region, array_ptr);
        Output {{
            is_some: true,
            split_index: checked_sub_or_split_index(input),
            tuple_array_position: {tuple_position},
            array,
            other: {other_expression},
        }}
    }} else {{
        Output {{
            is_some: false,
            split_index: -1,
            tuple_array_position: -1,
            array: empty_region(),
            other: empty_region(),
        }}
    }}
}}

pub open spec fn source_state(input: Input) -> FinalState {{
    if branch_succeeds(input) {{
        let pair = raw_parts_split(input);
        FinalState {{
            backing: input.slice,
            prefix: pair.0,
            suffix: pair.1,
            composed_final: input.slice.source,
            unique_partition: true,
            elements_unchanged: true,
        }}
    }} else {{
        FinalState {{
            backing: input.slice,
            prefix: empty_region(),
            suffix: empty_region(),
            composed_final: input.slice.source,
            unique_partition: true,
            elements_unchanged: true,
        }}
    }}
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
}}

pub open spec fn active_contract(
    input: Input,
    output: Output,
    state: FinalState,
) -> bool {{
    if branch_succeeds(input) {{
        output.is_some
            && output.array.length == input.n as int
            && output.array.values
                == if {array_prefix} {{
                    input.slice.source.subrange(0, input.n as int)
                }} else {{
                    input.slice.source.subrange(
                        input.slice.source.len() as int - input.n as int,
                        input.slice.source.len() as int,
                    )
                }}
            && (!{returns_other} || output.other.unique)
            && output.tuple_array_position == {tuple_position}
            && state.backing.source == {composition}
            && state.composed_final == state.backing.source
            && state.unique_partition
    }} else {{
        !output.is_some
            && state.backing.source == input.slice.source
            && state.composed_final == input.slice.source
    }}
}}

pub open spec fn target_transition(
    input: Input,
    boundary: Boundary,
    output: Output,
    state: FinalState,
) -> bool {{
    boundary_holds(input, boundary)
        && output == source_output(input)
        && state == source_state(input)
        && active_contract(input, output, state)
}}

pub open spec fn same_region(
    left: RegionIdentity,
    right: RegionIdentity,
) -> bool {{
    left.values == right.values
        && left.start == right.start
        && left.length == right.length
        && left.address == right.address
        && left.allocation == right.allocation
        && left.provenance == right.provenance
        && left.parent_borrow == right.parent_borrow
        && left.element_size == right.element_size
        && left.projection == right.projection
        && left.unique == right.unique
}}

pub open spec fn same_slice(
    left: SliceIdentity,
    right: SliceIdentity,
) -> bool {{
    left.source == right.source
        && left.start == right.start
        && left.address == right.address
        && left.allocation == right.allocation
        && left.provenance == right.provenance
        && left.parent_borrow == right.parent_borrow
        && left.element_size == right.element_size
}}

pub open spec fn same_output(left: Output, right: Output) -> bool {{
    left.is_some == right.is_some
        && left.split_index == right.split_index
        && left.tuple_array_position == right.tuple_array_position
        && same_region(left.array, right.array)
        && same_region(left.other, right.other)
}}

pub open spec fn same_state(
    left: FinalState,
    right: FinalState,
) -> bool {{
    same_slice(left.backing, right.backing)
        && same_region(left.prefix, right.prefix)
        && same_region(left.suffix, right.suffix)
        && left.composed_final == right.composed_final
        && left.unique_partition == right.unique_partition
        && left.elements_unchanged == right.elements_unchanged
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
    reveal(same_region);
    reveal(same_slice);
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
    reveal(same_region);
}}

}} // verus!
"""
