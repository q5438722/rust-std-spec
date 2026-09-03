#!/usr/bin/env python3
"""Source-backed obligations for mutable Slice split primitives."""

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
RAW_SLICE_SOURCE_PATH = "core/src/slice/raw.rs"
RAW_SLICE_SOURCE_SHA256 = (
    "0914968067f7e2bc798680c1edd72bcb032a9fd44ebb2b6fbc082a3a2b16941f"
)
INTRINSICS_SOURCE_PATH = "core/src/intrinsics/mod.rs"
INTRINSICS_SOURCE_SHA256 = (
    "6584f906e1a4c974d9493846036a6df8322e35798eb920833e90d79cd2cf69c3"
)
VOCABULARY_RANGES = ((928, 930),)
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
            name="slice_split_at_mut_unchecked",
            path=SLICE_SOURCE_PATH,
            start=2092,
            end=2112,
            file_sha256=SLICE_SOURCE_SHA256,
            filename="canonical_slice_split_at_mut_unchecked.rs",
            fragments=(
                "let len = self.len()",
                "let ptr = self.as_mut_ptr()",
                "(mid: usize = mid, len: usize = len) => mid <= len",
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
            fragments=(
                "pub const unsafe fn add(self, count: usize) -> Self",
                "unsafe { intrinsics::offset(self, count) }",
            ),
        ),
        CanonicalSource(
            name="mut_ptr_add_docs",
            path=PTR_ADD_DOCS_PATH,
            start=1,
            end=32,
            file_sha256=PTR_ADD_DOCS_SHA256,
            filename="canonical_mut_ptr_add_docs.md",
            fragments=(
                "count * size_of::<T>()",
                "the entire memory range between `self` and the result",
                "vec.as_ptr().add(vec.len())",
            ),
        ),
        CanonicalSource(
            name="slice_from_raw_parts_mut",
            path=RAW_SLICE_SOURCE_PATH,
            start=136,
            end=196,
            file_sha256=RAW_SLICE_SOURCE_SHA256,
            filename="canonical_slice_from_raw_parts_mut.rs",
            fragments=(
                "pub const unsafe fn from_raw_parts_mut",
                "contained within a single allocation",
                "non-null and aligned even for zero-length slices or slices of ZSTs",
                "&mut *ptr::slice_from_raw_parts_mut(data, len)",
            ),
        ),
        CanonicalSource(
            name="intrinsics_unchecked_sub",
            path=INTRINSICS_SOURCE_PATH,
            start=1990,
            end=1999,
            file_sha256=INTRINSICS_SOURCE_SHA256,
            filename="canonical_intrinsics_unchecked_sub.rs",
            fragments=(
                "Returns the result of an unchecked subtraction",
                "pub const unsafe fn unchecked_sub<T: Copy>(x: T, y: T) -> T",
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
class SplitTarget:
    target: str
    input_order: str
    artifact_id: str
    checked: bool
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
                    self.docs_reference,
                    *(source.reference for source in self.helper_sources),
                )
            )
        )

    @property
    def active_conjuncts(self) -> tuple[str, ...]:
        common = (
            "ActiveLeftViewConjunct",
            "ActiveRightViewConjunct",
            "ActiveSomeFinalFrameConjunct",
        )
        if self.checked:
            return (
                "ActiveSomeTagConjunct",
                "ActiveNoneTagConjunct",
                *common,
                "ActiveNoneFinalFrameConjunct",
            )
        return common


COMMON_HELPERS = (
    "slice_as_mut_ptr",
    "slice_split_at_mut_unchecked",
    "mut_ptr_add",
    "mut_ptr_add_docs",
    "slice_from_raw_parts_mut",
    "intrinsics_unchecked_sub",
)

TARGETS = (
    SplitTarget(
        target="core::slice::split_at_mut_checked",
        input_order="85",
        artifact_id="085_core_slice_split_at_mut_checked",
        checked=True,
        active_contract_sha256=(
            "f545d70fd2f00566e6847d457980a532ef48cdc82fe2e12eba1be9ccff4aebd6"
        ),
        active_contract_text=(
            "pub assume_specification<T>[ <[T]>::split_at_mut_checked ]( "
            "slice: &mut [T], mid: usize, ) -> (ret: Option<(&mut [T], "
            "&mut [T])>) ensures mid <= old(slice)@.len() ==> ret.is_some() "
            "&& ret.unwrap().0@ == old(slice)@.subrange(0, mid as int) && "
            "ret.unwrap().1@ == old(slice)@.subrange(mid as int, "
            "old(slice)@.len() as int) && final(slice)@ == "
            "final(ret.unwrap().0)@ + final(ret.unwrap().1)@, mid > "
            "old(slice)@.len() ==> ret.is_none() && final(slice)@ == "
            "old(slice)@, ;"
        ),
        source_start=2192,
        source_end=2200,
        docs_start=2163,
        docs_end=2187,
        source_item_sha256=(
            "abfee0fdb5817382bcc578ea7e47395312bd55464b5fb9a4ba5cd32cfd090110"
        ),
        generated_declaration_sha256=(
            "ef29bc68515c03a970938f2f5f9e631c232708308fb8d551a1d067cb01bc71f2"
        ),
        harness_sha256=(
            "f82578ac2d75f55792ca09fd9ebe7152f262b60dc710a993f83e871d6a66a715"
        ),
        source_body_manifest_sha256=(
            "49e56dbec2ab3894358eafb3e215d1ea771c54b05f3d6963e057d8a49caee92c"
        ),
        transformation_manifest_sha256=(
            "d2d07fcd3363b26e80fa0cd69c31e45cc6d6503cdd880bb68bf285d8a4559cae"
        ),
        dependency_manifest_sha256=(
            "3daf32faa469f29f283f3a0072705d47f4f193a44085fe418acf3db1bed6530e"
        ),
        all_trust_site_ids=(
            "TS-085-D001",
            "TS-085-D002",
            "TS-085-D003",
            "TS-085-C001",
            "TS-085-C002",
            "TS-085-C003",
            "TS-085-E001",
            "TS-085-E002",
        ),
        context_only_trust_site_ids=(
            "TS-085-D001",
            "TS-085-C001",
            "TS-085-C002",
            "TS-085-C003",
        ),
        helper_names=("slice_split_at_mut_checked", *COMMON_HELPERS),
        source_fragments=(
            "if mid <= self.len()",
            "Some(unsafe { self.split_at_mut_unchecked(mid) })",
            "None",
        ),
        source_backed_replacements=(
            SourceReplacement(
                replacement_id="SRC-085-CHECKED-BRANCH",
                operation="canonical checked mid <= len branch and None frame",
                symbols=("CheckedBranchTransition",),
                replaces_trust_site_ids=("TS-085-D003",),
            ),
            SourceReplacement(
                replacement_id="SRC-085-CANONICAL-MUT-SPLIT",
                operation=(
                    "canonical unchecked domain, mutable pointer cast, pointer "
                    "addition, unchecked subtraction, raw-slice construction, "
                    "derived borrows, and ordered final frame"
                ),
                symbols=(
                    "UncheckedDomainTransition",
                    "AsMutPtrCastTransition",
                    "PointerAddTransition",
                    "UncheckedSubTransition",
                    "RawSliceRegionsTransition",
                    "StructuralReferenceIdentityTransition",
                    "UniqueDerivedBorrowTransition",
                    "FinalFrameTransition",
                ),
                replaces_trust_site_ids=(
                    "TS-085-D002",
                    "TS-085-E001",
                    "TS-085-E002",
                ),
            ),
        ),
    ),
    SplitTarget(
        target="core::slice::split_at_mut_unchecked",
        input_order="86",
        artifact_id="086_core_slice_split_at_mut_unchecked",
        checked=False,
        active_contract_sha256=(
            "dfe96dd890e058e02f390e85bdfce250a48823c9e43c15ad599961b2f28f2da9"
        ),
        active_contract_text=(
            "pub assume_specification<T>[ <[T]>::split_at_mut_unchecked ]( "
            "slice: &mut [T], mid: usize, ) -> (ret: (&mut [T], &mut [T])) "
            "requires split_point_in_range(old(slice)@, mid), ensures ret.0@ "
            "== old(slice)@.subrange(0, mid as int), ret.1@ == "
            "old(slice)@.subrange(mid as int, old(slice)@.len() as int), "
            "final(slice)@ == final(ret.0)@ + final(ret.1)@, ;"
        ),
        source_start=2092,
        source_end=2112,
        docs_start=2056,
        docs_end=2086,
        source_item_sha256=(
            "64e5aaab27b44c5104ff431b7f8c1be361ea556baa432a36e7386e76089a4531"
        ),
        generated_declaration_sha256=(
            "7e81e93580f62d1271f7f0c4fae137ad32ed91574532c6591624ba8a99d748fa"
        ),
        harness_sha256=(
            "65fae584953a02ffa863313e147e3cb520b3b64f298f792d5b347742180d0832"
        ),
        source_body_manifest_sha256=(
            "3b588eddba50ac7d193ba2b7e06f597a37069d924aa222ad570aadccba28d5c9"
        ),
        transformation_manifest_sha256=(
            "e1b73deef875ca75055cf165ba3fea602c820ee110b5cd2772ca3847d12eae48"
        ),
        dependency_manifest_sha256=(
            "641355e7fb8a18d13b1c0a88f8ea5cd07813a78630cafd42db4fb706f4b77394"
        ),
        all_trust_site_ids=(
            "TS-086-D001",
            "TS-086-D002",
            "TS-086-D003",
            "TS-086-D004",
            "TS-086-D005",
            "TS-086-C001",
            "TS-086-C002",
            "TS-086-C003",
            "TS-086-E001",
            "TS-086-E002",
        ),
        context_only_trust_site_ids=(
            "TS-086-D001",
            "TS-086-C001",
            "TS-086-C002",
            "TS-086-C003",
        ),
        helper_names=COMMON_HELPERS,
        source_fragments=(
            "let len = self.len()",
            "let ptr = self.as_mut_ptr()",
            "(mid: usize = mid, len: usize = len) => mid <= len",
            "from_raw_parts_mut(ptr, mid)",
            "from_raw_parts_mut(ptr.add(mid), unchecked_sub(len, mid))",
        ),
        source_backed_replacements=(
            SourceReplacement(
                replacement_id="SRC-086-AS-MUT-PTR-CAST",
                operation="canonical slice-to-thin mutable pointer cast",
                symbols=("AsMutPtrCastTransition",),
                replaces_trust_site_ids=("TS-086-D002",),
            ),
            SourceReplacement(
                replacement_id="SRC-086-UNSAFE-DOMAIN",
                operation="source unsafe precondition mid <= len",
                symbols=("UncheckedDomainTransition",),
                replaces_trust_site_ids=("TS-086-D003",),
            ),
            SourceReplacement(
                replacement_id="SRC-086-UNCHECKED-SUB",
                operation="source unchecked subtraction len - mid under mid <= len",
                symbols=("UncheckedSubTransition",),
                replaces_trust_site_ids=("TS-086-D004",),
            ),
            SourceReplacement(
                replacement_id="SRC-086-RAW-PARTS-AND-FRAME",
                operation=(
                    "canonical pointer addition, two raw-slice regions, "
                    "structural references, unique borrows, and ordered frame"
                ),
                symbols=(
                    "CheckedBranchTransition",
                    "PointerAddTransition",
                    "RawSliceRegionsTransition",
                    "StructuralReferenceIdentityTransition",
                    "UniqueDerivedBorrowTransition",
                    "FinalFrameTransition",
                ),
                replaces_trust_site_ids=(
                    "TS-086-D005",
                    "TS-086-E001",
                    "TS-086-E002",
                ),
            ),
        ),
    ),
)
TARGET_BY_ARTIFACT = {config.artifact_id: config for config in TARGETS}
TARGET_KEYS = tuple((config.target, config.input_order) for config in TARGETS)


@dataclass(frozen=True)
class SourceCase:
    length: int
    mid: int
    element_size: int
    element_alignment: int


COMMON_SOURCE_CASES = {
    "empty_mid0": SourceCase(0, 0, 8, 8),
    "nonempty_mid0": SourceCase(3, 0, 8, 8),
    "mid_equal_len": SourceCase(3, 3, 8, 8),
    "strict_interior": SourceCase(5, 2, 8, 8),
    "zst_equal_addresses": SourceCase(5, 2, 0, 8),
}
CHECKED_ONLY_SOURCE_CASES = {
    "checked_mid_greater_than_len": SourceCase(3, 4, 8, 8),
}
NEGATIVE_PROBES = (
    "wrong_branching",
    "off_by_one_split",
    "off_by_one_subtraction",
    "swapped_regions",
    "pointer_address_loss",
    "allocation_loss",
    "provenance_loss",
    "borrow_loss",
    "address_based_zst_disjointness",
    "missing_final_frame",
    "reversed_final_frame",
)
INVALID_UNCHECKED_PROBE = "invalid_unchecked_domain"


def source_cases(config: SplitTarget) -> dict[str, SourceCase]:
    cases = dict(COMMON_SOURCE_CASES)
    if config.checked:
        cases.update(CHECKED_ONLY_SOURCE_CASES)
    return cases


def negative_probe_names(config: SplitTarget) -> tuple[str, ...]:
    if config.checked:
        return NEGATIVE_PROBES
    return (*NEGATIVE_PROBES, INVALID_UNCHECKED_PROBE)


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
    ("x_mid", "Int"),
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
    ("y_has_pair", "Bool"),
    ("y_split_index", "Int"),
    *((f"y_left_{name}", sort) for name, sort in REGION_FIELDS),
    *((f"y_right_{name}", sort) for name, sort in REGION_FIELDS),
)
POINTER_STATE_FIELDS = (
    ("s_base_address", "Int"),
    ("s_base_allocation", "Int"),
    ("s_base_provenance", "Int"),
    ("s_base_parent_borrow", "Int"),
    ("s_base_element_size", "Int"),
    ("s_base_element_alignment", "Int"),
    ("s_mid_address", "Int"),
    ("s_mid_allocation", "Int"),
    ("s_mid_provenance", "Int"),
    ("s_mid_parent_borrow", "Int"),
    ("s_mid_element_size", "Int"),
    ("s_mid_element_alignment", "Int"),
    ("s_tail_length", "Int"),
)
BACKING_STATE_FIELDS = (
    ("s_backing_values", "(Seq Int)"),
    ("s_backing_start", "Int"),
    ("s_backing_length", "Int"),
    ("s_backing_address", "Int"),
    ("s_backing_allocation", "Int"),
    ("s_backing_provenance", "Int"),
    ("s_backing_parent_borrow", "Int"),
    ("s_backing_element_size", "Int"),
    ("s_backing_element_alignment", "Int"),
)
STATE_FIELDS = (
    *POINTER_STATE_FIELDS,
    *BACKING_STATE_FIELDS,
    *((f"s_left_{name}", sort) for name, sort in REGION_FIELDS),
    *((f"s_right_{name}", sort) for name, sort in REGION_FIELDS),
    ("s_composed_final", "(Seq Int)"),
    ("s_unique_partition", "Bool"),
    ("s_elements_unchanged", "Bool"),
)
SOURCE_TRANSITIONS = (
    "CheckedBranchTransition",
    "UncheckedDomainTransition",
    "AsMutPtrCastTransition",
    "PointerAddTransition",
    "UncheckedSubTransition",
    "RawSliceRegionsTransition",
    "StructuralReferenceIdentityTransition",
    "UniqueDerivedBorrowTransition",
    "FinalFrameTransition",
)
OUTPUT_SOURCE_TRANSITIONS = (
    "CheckedBranchTransition",
    "UncheckedDomainTransition",
    "AsMutPtrCastOutputTransition",
    "PointerAddOutputTransition",
    "UncheckedSubOutputTransition",
    "RawSliceRegionsOutputTransition",
    "StructuralReferenceIdentityOutputTransition",
    "UniqueDerivedBorrowOutputTransition",
)


def _normalized(text: str) -> str:
    return " ".join(text.split())


def validate_source_anchors(
    config: SplitTarget,
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
    if _normalized(
        "pub open spec fn split_point_in_range"
    ) not in _normalized(vocabulary):
        raise GuardError(f"{config.target}: split-domain vocabulary changed")
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


def _success(config: SplitTarget) -> str:
    return "(<= (x_mid x) (x_length x))" if config.checked else "true"


def _region_value(offset: str, length: str) -> str:
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
       (= (b_element_size b) (x_element_size x))
       (= (b_element_alignment b) (x_element_alignment x))))"""


def _checked_branch_transition(config: SplitTarget) -> str:
    return f"""\
(define-fun CheckedBranchTransition ((x Input) (y Output)) Bool
  (= (y_has_pair y) {_success(config)}))"""


def _unchecked_domain_transition() -> str:
    return """\
(define-fun UncheckedDomainTransition ((x Input) (y Output)) Bool
  (=> (y_has_pair y) (<= (x_mid x) (x_length x))))"""


def _zero_pointer(prefix: str) -> str:
    return "\n       ".join(
        f"(= ({prefix}_{name} s) 0)"
        for name in (
            "address",
            "allocation",
            "provenance",
            "parent_borrow",
            "element_size",
            "element_alignment",
        )
    )


def _as_mut_ptr_cast_transition() -> str:
    return f"""\
(define-fun AsMutPtrCastTransition
  ((x Input) (y Output) (s State)) Bool
  (ite (y_has_pair y)
       (and (= (s_base_address s) (x_address x))
            (= (s_base_allocation s) (x_allocation x))
            (= (s_base_provenance s) (x_provenance x))
            (= (s_base_parent_borrow s) (x_parent_borrow x))
            (= (s_base_element_size s) (x_element_size x))
            (= (s_base_element_alignment s) (x_element_alignment x)))
       (and {_zero_pointer("s_base")})))"""


def _as_mut_ptr_cast_output_transition() -> str:
    return """\
(define-fun AsMutPtrCastOutputTransition ((x Input) (y Output)) Bool
  (ite (y_has_pair y)
       (and (= (y_left_address y) (x_address x))
            (= (y_left_allocation y) (x_allocation x))
            (= (y_left_provenance y) (x_provenance x)))
       (and (= (y_left_address y) 0)
            (= (y_left_allocation y) 0)
            (= (y_left_provenance y) 0))))"""


def _pointer_add_transition() -> str:
    return f"""\
(define-fun PointerAddTransition ((x Input) (y Output) (s State)) Bool
  (ite (y_has_pair y)
       (and (= (s_mid_address s)
               (+ (s_base_address s) (* (x_mid x) (s_base_element_size s))))
            (= (s_mid_allocation s) (s_base_allocation s))
            (= (s_mid_provenance s) (s_base_provenance s))
            (= (s_mid_parent_borrow s) (s_base_parent_borrow s))
            (= (s_mid_element_size s) (s_base_element_size s))
            (= (s_mid_element_alignment s) (s_base_element_alignment s)))
       (and {_zero_pointer("s_mid")})))"""


def _pointer_add_output_transition() -> str:
    return """\
(define-fun PointerAddOutputTransition ((x Input) (y Output)) Bool
  (ite (y_has_pair y)
       (and (= (y_right_address y)
               (+ (x_address x) (* (x_mid x) (x_element_size x))))
            (= (y_right_allocation y) (x_allocation x))
            (= (y_right_provenance y) (x_provenance x)))
       (and (= (y_right_address y) 0)
            (= (y_right_allocation y) 0)
            (= (y_right_provenance y) 0))))"""


def _unchecked_sub_transition() -> str:
    return """\
(define-fun UncheckedSubTransition ((x Input) (y Output) (s State)) Bool
  (= (s_tail_length s)
     (ite (y_has_pair y) (- (x_length x) (x_mid x)) (- 1))))"""


def _unchecked_sub_output_transition() -> str:
    return """\
(define-fun UncheckedSubOutputTransition ((x Input) (y Output)) Bool
  (= (y_right_length y)
     (ite (y_has_pair y) (- (x_length x) (x_mid x)) 0)))"""


def _state_region_assignments(side: str, offset: str, length: str) -> str:
    values = {
        "values": _region_value(offset, length),
        "start": f"(+ (x_start x) {offset})",
        "length": length,
        "address": _region_address(offset),
        "allocation": "(x_allocation x)",
        "provenance": "(x_provenance x)",
        "parent_borrow": "(x_parent_borrow x)",
        "element_size": "(x_element_size x)",
        "element_alignment": "(x_element_alignment x)",
        "projection": "1" if side == "left" else "2",
        "unique": "true",
    }
    return "\n       ".join(
        f"(= (s_{side}_{name} s) {values[name]})" for name, _ in REGION_FIELDS
    )


def _zero_state_region(side: str) -> str:
    return "\n       ".join(
        f"(= (s_{side}_{name} s) "
        f"{EMPTY_SEQ if sort == '(Seq Int)' else 'false' if sort == 'Bool' else '0'})"
        for name, sort in REGION_FIELDS
    )


def _raw_slice_regions_transition() -> str:
    return f"""\
(define-fun RawSliceRegionsTransition
  ((x Input) (y Output) (s State)) Bool
  (ite (y_has_pair y)
       (and {_state_region_assignments("left", "0", "(x_mid x)")}
            {_state_region_assignments("right", "(x_mid x)", "(s_tail_length s)")})
       (and {_zero_state_region("left")}
            {_zero_state_region("right")})))"""


def _raw_slice_regions_output_transition() -> str:
    return f"""\
(define-fun RawSliceRegionsOutputTransition ((x Input) (y Output)) Bool
  (ite (y_has_pair y)
       (and (= (y_left_values y)
               {_region_value("0", "(x_mid x)")})
            (= (y_left_start y) (x_start x))
            (= (y_left_length y) (x_mid x))
            (= (y_right_values y)
               {_region_value("(x_mid x)", "(- (x_length x) (x_mid x))")})
            (= (y_right_start y) (+ (x_start x) (x_mid x))))
       (and (= (y_left_values y) {EMPTY_SEQ})
            (= (y_left_start y) 0)
            (= (y_left_length y) 0)
            (= (y_right_values y) {EMPTY_SEQ})
            (= (y_right_start y) 0))))"""


def _output_region_from_state(side: str) -> str:
    return "\n       ".join(
        f"(= (y_{side}_{name} y) (s_{side}_{name} s))"
        for name, _ in REGION_FIELDS
    )


def _zero_output_region(side: str) -> str:
    return "\n       ".join(
        f"(= (y_{side}_{name} y) "
        f"{EMPTY_SEQ if sort == '(Seq Int)' else 'false' if sort == 'Bool' else '0'})"
        for name, sort in REGION_FIELDS
    )


def _structural_reference_identity_transition() -> str:
    return f"""\
(define-fun StructuralReferenceIdentityTransition
  ((x Input) (y Output) (s State)) Bool
  (ite (y_has_pair y)
       (and (= (y_split_index y) (x_mid x))
            {_output_region_from_state("left")}
            {_output_region_from_state("right")})
       (and (= (y_split_index y) (- 1))
            {_zero_output_region("left")}
            {_zero_output_region("right")})))"""


def _structural_reference_identity_output_transition() -> str:
    return """\
(define-fun StructuralReferenceIdentityOutputTransition
  ((x Input) (y Output)) Bool
  (ite (y_has_pair y)
       (and (= (y_split_index y) (x_mid x))
            (= (y_left_parent_borrow y) (x_parent_borrow x))
            (= (y_left_element_size y) (x_element_size x))
            (= (y_left_element_alignment y) (x_element_alignment x))
            (= (y_left_projection y) 1)
            (= (y_right_parent_borrow y) (x_parent_borrow x))
            (= (y_right_element_size y) (x_element_size x))
            (= (y_right_element_alignment y) (x_element_alignment x))
            (= (y_right_projection y) 2))
       (and (= (y_split_index y) (- 1))
            (= (y_left_parent_borrow y) 0)
            (= (y_left_element_size y) 0)
            (= (y_left_element_alignment y) 0)
            (= (y_left_projection y) 0)
            (= (y_right_parent_borrow y) 0)
            (= (y_right_element_size y) 0)
            (= (y_right_element_alignment y) 0)
            (= (y_right_projection y) 0))))"""


def _unique_derived_borrow_transition() -> str:
    return """\
(define-fun UniqueDerivedBorrowTransition
  ((x Input) (y Output) (s State)) Bool
  (ite (y_has_pair y)
       (and (= (y_left_unique y) true)
            (= (y_right_unique y) true)
            (= (s_left_unique s) true)
            (= (s_right_unique s) true)
            (= (s_unique_partition s)
               (or (= (s_left_length s) 0)
                   (= (s_right_length s) 0)
                   (<= (+ (s_left_start s) (s_left_length s))
                       (s_right_start s)))))
       (and (= (y_left_unique y) false)
            (= (y_right_unique y) false)
            (= (s_left_unique s) false)
            (= (s_right_unique s) false)
            (= (s_unique_partition s) true))))"""


def _unique_derived_borrow_output_transition() -> str:
    return """\
(define-fun UniqueDerivedBorrowOutputTransition
  ((x Input) (y Output)) Bool
  (ite (y_has_pair y)
       (and (= (y_left_unique y) true)
            (= (y_right_unique y) true))
       (and (= (y_left_unique y) false)
            (= (y_right_unique y) false))))"""


def _backing_assignments() -> str:
    values = {
        "values": "(x_source x)",
        "start": "(x_start x)",
        "length": "(x_length x)",
        "address": "(x_address x)",
        "allocation": "(x_allocation x)",
        "provenance": "(x_provenance x)",
        "parent_borrow": "(x_parent_borrow x)",
        "element_size": "(x_element_size x)",
        "element_alignment": "(x_element_alignment x)",
    }
    return "\n       ".join(
        f"(= (s_backing_{name} s) {value})" for name, value in values.items()
    )


def _final_frame_transition() -> str:
    return f"""\
(define-fun FinalFrameTransition
  ((x Input) (y Output) (s State)) Bool
  (and {_backing_assignments()}
       (= (s_composed_final s)
          (ite (y_has_pair y)
               (seq.++ (s_left_values s) (s_right_values s))
               (x_source x)))
       (= (s_composed_final s) (x_source x))
       (= (s_elements_unchanged s) true)))"""


def _active_contract_definitions(config: SplitTarget) -> str:
    common = """\
(define-fun ActiveLeftViewConjunct ((x Input) (y Output)) Bool
  (=> (y_has_pair y)
      (= (y_left_values y)
         (seq.extract (x_source x) 0 (x_mid x)))))
(define-fun ActiveRightViewConjunct ((x Input) (y Output)) Bool
  (=> (y_has_pair y)
      (= (y_right_values y)
         (seq.extract (x_source x) (x_mid x)
                      (- (x_length x) (x_mid x))))))
(define-fun ActiveSomeFinalFrameConjunct
  ((x Input) (y Output) (s State)) Bool
  (=> (y_has_pair y)
      (and (= (s_composed_final s)
              (seq.++ (y_left_values y) (y_right_values y)))
           (= (s_backing_values s) (s_composed_final s)))))"""
    if not config.checked:
        return common
    return f"""\
(define-fun ActiveSomeTagConjunct ((x Input) (y Output)) Bool
  (=> (<= (x_mid x) (x_length x)) (y_has_pair y)))
(define-fun ActiveNoneTagConjunct ((x Input) (y Output)) Bool
  (=> (> (x_mid x) (x_length x)) (not (y_has_pair y))))
{common}
(define-fun ActiveNoneFinalFrameConjunct
  ((x Input) (y Output) (s State)) Bool
  (=> (not (y_has_pair y))
      (and (= (s_backing_values s) (x_source x))
           (= (s_composed_final s) (x_source x)))))"""


def _requires(config: SplitTarget) -> str:
    unchecked = (
        "\n       (<= (x_mid x) (x_length x))" if not config.checked else ""
    )
    return f"""\
(define-fun Requires_T ((x Input)) Bool
  (and (= (x_length x) (seq.len (x_source x)))
       (>= (x_length x) 0)
       (>= (x_start x) 0)
       (> (x_address x) 0)
       (>= (x_allocation x) 0)
       (>= (x_provenance x) 0)
       (> (x_parent_borrow x) 0)
       (>= (x_element_size x) 0)
       (> (x_element_alignment x) 0)
       (= (mod (x_address x) (x_element_alignment x)) 0)
       (= (mod (x_element_size x) (x_element_alignment x)) 0)
       (>= (x_mid x) 0)
       (<= (* (x_length x) (x_element_size x)) 9223372036854775807)
       (or (= (* (x_length x) (x_element_size x)) 0)
           (and (> (x_allocation x) 0)
                (> (x_provenance x) 0))){unchecked}))"""


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


def _target_definition(config: SplitTarget, purpose: str) -> str:
    direct_calls: tuple[str, ...] = (
        "(InputBoundaryObserved x b)",
        "(CheckedBranchTransition x y)",
        "(UncheckedDomainTransition x y)",
    )
    if purpose == EXACT_OUTPUT:
        direct_calls = (
            *direct_calls,
            "(AsMutPtrCastOutputTransition x y)",
            "(PointerAddOutputTransition x y)",
            "(UncheckedSubOutputTransition x y)",
            "(RawSliceRegionsOutputTransition x y)",
            "(StructuralReferenceIdentityOutputTransition x y)",
            "(UniqueDerivedBorrowOutputTransition x y)",
        )
    frame = "s" if purpose == PRIMARY else "f"
    state_calls = (
        f"(AsMutPtrCastTransition x y {frame})",
        f"(PointerAddTransition x y {frame})",
        f"(UncheckedSubTransition x y {frame})",
        f"(RawSliceRegionsTransition x y {frame})",
        f"(StructuralReferenceIdentityTransition x y {frame})",
        f"(UniqueDerivedBorrowTransition x y {frame})",
        f"(FinalFrameTransition x y {frame})",
    )
    active_calls = tuple(
        f"({name} x y {frame})"
        if name in {
            "ActiveSomeFinalFrameConjunct",
            "ActiveNoneFinalFrameConjunct",
        }
        else f"({name} x y)"
        for name in config.active_conjuncts
    )
    body = "\n       ".join((*direct_calls, *state_calls, *active_calls))
    if purpose == EXACT_OUTPUT:
        body = (
            "\n       ".join(direct_calls)
            + "\n       (exists ((f FrameState))\n"
            + "         (and "
            + "\n              ".join((*state_calls, *active_calls))
            + "))"
        )
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
    config: SplitTarget,
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
            _checked_branch_transition(config),
            _unchecked_domain_transition(),
            _frame_adapt(_as_mut_ptr_cast_transition(), purpose),
            *(
                (_as_mut_ptr_cast_output_transition(),)
                if purpose == EXACT_OUTPUT
                else ()
            ),
            _frame_adapt(_pointer_add_transition(), purpose),
            *(
                (_pointer_add_output_transition(),)
                if purpose == EXACT_OUTPUT
                else ()
            ),
            _frame_adapt(_unchecked_sub_transition(), purpose),
            *(
                (_unchecked_sub_output_transition(),)
                if purpose == EXACT_OUTPUT
                else ()
            ),
            _frame_adapt(_raw_slice_regions_transition(), purpose),
            *(
                (_raw_slice_regions_output_transition(),)
                if purpose == EXACT_OUTPUT
                else ()
            ),
            _frame_adapt(
                _structural_reference_identity_transition(), purpose
            ),
            *(
                (_structural_reference_identity_output_transition(),)
                if purpose == EXACT_OUTPUT
                else ()
            ),
            _frame_adapt(_unique_derived_borrow_transition(), purpose),
            *(
                (_unique_derived_borrow_output_transition(),)
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
; mid is shared input. Boundary contains only initial address, allocation,
; provenance, unique parent borrow, and element size/alignment observations.
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
{_requires(config)}
{_boundary()}
{_target_definition(config, purpose)}
(define-fun Spec_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (TargetDefinition_T x b y s))
{_equivalence(purpose)}
{theorem}"""


def obligation_text(config: SplitTarget, purpose: str) -> str:
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
    config: SplitTarget,
    purpose: str,
) -> list[dict[str, Any]]:
    output_substitutions = {
        "AsMutPtrCastTransition": "AsMutPtrCastOutputTransition",
        "PointerAddTransition": "PointerAddOutputTransition",
        "UncheckedSubTransition": "UncheckedSubOutputTransition",
        "RawSliceRegionsTransition": "RawSliceRegionsOutputTransition",
        "StructuralReferenceIdentityTransition": (
            "StructuralReferenceIdentityOutputTransition"
        ),
        "UniqueDerivedBorrowTransition": "UniqueDerivedBorrowOutputTransition",
    }
    substitutions = output_substitutions if purpose == EXACT_OUTPUT else {}
    return [
        {
            "replacement_id": replacement.replacement_id,
            "operation": replacement.operation,
            "symbols": [
                substitutions.get(symbol, symbol)
                for symbol in replacement.symbols
                if purpose == PRIMARY or symbol != "FinalFrameTransition"
            ],
            "source_citations": list(config.source_citations),
            "replaces_trust_site_ids": list(
                replacement.replaces_trust_site_ids
            ),
        }
        for replacement in config.source_backed_replacements
    ]


def _boundary_metadata(config: SplitTarget) -> list[dict[str, Any]]:
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
        "b_parent_borrow": "initial unique parent-borrow identity",
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
    config: SplitTarget,
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
            "slice_length": "arbitrary nonnegative integer",
            "mid": (
                "arbitrary nonnegative shared input"
                if config.checked
                else "arbitrary nonnegative shared input constrained by mid <= len"
            ),
            "element_layout": (
                "arbitrary nonnegative size and positive alignment; empty and "
                "nonempty ZST slices are included"
            ),
            "source_model_complete": True,
        },
        "active_contract_conjuncts": list(config.active_conjuncts),
        "contract_translation": {
            "branch": (
                "Some exactly when mid <= len; otherwise None"
                if config.checked
                else "pair returned under required mid <= len domain"
            ),
            "left_region": "[0,mid)",
            "right_region": "[mid,len)",
            "tail_length": "len - mid through unchecked_sub under mid <= len",
            "immediate_final_frame": (
                "left then right, preserving the parent slice and initial values"
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
                "mid, which belongs to shared input x",
                "checked branch and unchecked domain decision",
                "pointer-add result and unchecked subtraction",
                "left/right ranges and structural reference identities",
                "unique derived borrows",
                "principal output and immediate final state",
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
            "checked_branch_and_unsafe_domain": {
                "symbols": [
                    "CheckedBranchTransition",
                    "UncheckedDomainTransition",
                ],
                "source_citations": [
                    source.reference
                    for source in config.helper_sources
                    if "split_at_mut" in source.name
                ],
            },
            "canonical_pointer_chain": {
                "symbols": [
                    (
                        "AsMutPtrCastOutputTransition"
                        if purpose == EXACT_OUTPUT
                        else "AsMutPtrCastTransition"
                    ),
                    (
                        "PointerAddOutputTransition"
                        if purpose == EXACT_OUTPUT
                        else "PointerAddTransition"
                    ),
                ],
                "source_citations": [
                    source.reference
                    for source in config.helper_sources
                    if source.name
                    in {
                        "slice_as_mut_ptr",
                        "mut_ptr_add",
                        "mut_ptr_add_docs",
                    }
                ],
            },
            "canonical_subtraction_and_raw_slices": {
                "symbols": [
                    (
                        "UncheckedSubOutputTransition"
                        if purpose == EXACT_OUTPUT
                        else "UncheckedSubTransition"
                    ),
                    (
                        "RawSliceRegionsOutputTransition"
                        if purpose == EXACT_OUTPUT
                        else "RawSliceRegionsTransition"
                    ),
                ],
                "source_citations": [
                    source.reference
                    for source in config.helper_sources
                    if source.name
                    in {
                        "intrinsics_unchecked_sub",
                        "slice_from_raw_parts_mut",
                    }
                ],
            },
            "structural_borrows_and_frame": {
                "symbols": [
                    (
                        "StructuralReferenceIdentityOutputTransition"
                        if purpose == EXACT_OUTPUT
                        else "StructuralReferenceIdentityTransition"
                    ),
                    (
                        "UniqueDerivedBorrowOutputTransition"
                        if purpose == EXACT_OUTPUT
                        else "UniqueDerivedBorrowTransition"
                    ),
                    *(
                        []
                        if purpose == EXACT_OUTPUT
                        else ["FinalFrameTransition"]
                    ),
                ],
                "source_citations": list(config.source_citations),
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
    config: SplitTarget,
    purpose: str,
) -> tuple[str, dict[str, Any]]:
    return obligation_text(config, purpose), obligation_metadata(config, purpose)


def validate_target_obligation(
    config: SplitTarget,
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
            f"{config.target}: metadata differs from reviewed split model"
        )
    if parse_smt(text) != parse_smt(expected_text):
        raise GuardError(f"{config.target}: SMT differs from reviewed split model")


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
        f"(assert (= (x_mid x) {case.mid}))",
    ]


def _model_query() -> str:
    selectors = (
        "y_has_pair",
        "y_split_index",
        "y_left_start",
        "y_left_length",
        "y_left_address",
        "y_left_allocation",
        "y_left_provenance",
        "y_left_parent_borrow",
        "y_left_projection",
        "y_left_unique",
        "y_right_start",
        "y_right_length",
        "y_right_address",
        "y_right_allocation",
        "y_right_provenance",
        "y_right_parent_borrow",
        "y_right_projection",
        "y_right_unique",
    )
    state_selectors = (
        "s_base_address",
        "s_mid_address",
        "s_tail_length",
        "s_composed_final",
        "s_unique_partition",
        "s_elements_unchanged",
    )
    terms = [
        "(x_length x)",
        "(x_mid x)",
        "(x_element_size x)",
        *(f"({selector} y1)" for selector in selectors),
        *(f"({selector} s1)" for selector in state_selectors),
    ]
    return "(get-value (\n  %s))" % "\n  ".join(terms)


def source_instance_text(
    config: SplitTarget,
    case: SourceCase,
    *,
    extra_assertions: tuple[str, ...] = (),
) -> str:
    if (
        case.length < 0
        or case.mid < 0
        or case.element_size < 0
        or case.element_alignment <= 0
    ):
        raise ValueError("split source cases require a valid nonnegative layout")
    if not config.checked and case.mid > case.length:
        raise ValueError("unchecked split source case violates mid <= len")
    assertions = [
        *_fixed_input_assertions(case),
        "(assert (Requires_T x))",
        "(assert (Boundary_T x b))",
        "(assert (Spec_T x b y1 s1))",
    ]
    if case == COMMON_SOURCE_CASES["zst_equal_addresses"]:
        assertions.append(
            "(assert (= (y_left_address y1) (y_right_address y1)))"
        )
    if case == COMMON_SOURCE_CASES["mid_equal_len"]:
        assertions.extend(
            (
                "(assert (= (s_mid_address s1)"
                " (+ (x_address x) (* (x_length x) (x_element_size x)))))",
                "(assert (= (y_right_length y1) 0))",
            )
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


def negative_probe_text(config: SplitTarget, name: str) -> str:
    if name not in negative_probe_names(config):
        raise ValueError(f"unknown split negative probe: {name}")
    if name == INVALID_UNCHECKED_PROBE:
        case = CHECKED_ONLY_SOURCE_CASES["checked_mid_greater_than_len"]
        return (
            _model_text(config, PRIMARY, include_theorem=False)
            + "\n"
            + "\n".join(
                (
                    *_fixed_input_assertions(case),
                    "(assert (Requires_T x))",
                )
            )
            + "\n(check-sat)\n"
        )
    case = (
        COMMON_SOURCE_CASES["zst_equal_addresses"]
        if name == "address_based_zst_disjointness"
        else COMMON_SOURCE_CASES["strict_interior"]
    )
    contradictions = {
        "wrong_branching": "(not (y_has_pair y1))",
        "off_by_one_split": (
            "(not (= (y_split_index y1) (x_mid x)))"
        ),
        "off_by_one_subtraction": (
            "(not (= (s_tail_length s1) (- (x_length x) (x_mid x))))"
        ),
        "swapped_regions": (
            "(= (y_left_start y1) (+ (x_start x) (x_mid x)))"
        ),
        "pointer_address_loss": (
            "(not (= (s_mid_address s1)"
            " (+ (x_address x) (* (x_mid x) (x_element_size x)))))"
        ),
        "allocation_loss": (
            "(not (= (y_right_allocation y1) (x_allocation x)))"
        ),
        "provenance_loss": (
            "(not (= (y_right_provenance y1) (x_provenance x)))"
        ),
        "borrow_loss": (
            "(not (= (y_right_parent_borrow y1) (x_parent_borrow x)))"
        ),
        "address_based_zst_disjointness": (
            "(distinct (y_left_address y1) (y_right_address y1))"
        ),
        "missing_final_frame": (
            "(not (= (s_composed_final s1) (x_source x)))"
        ),
        "reversed_final_frame": (
            "(= (s_composed_final s1)"
            " (seq.++ (y_right_values y1) (y_left_values y1)))"
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


def boundary_manifest(config: SplitTarget) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "target": config.target,
        "input_order": config.input_order,
        "boundary_narrower_than_target": True,
        "proof_boundary_assumption": (
            "Both executions observe the same initial non-null slice address, "
            "allocation, strict provenance, unique parent-borrow identity, "
            "element size, and element alignment. mid is shared input x."
        ),
        "shared_boundary_observations": _boundary_metadata(config),
        "canonical_source_transition": {
            "checked_branch": (
                "mid <= len selects Some; mid > len selects None"
                if config.checked
                else "not applicable; unsafe precondition requires mid <= len"
            ),
            "unchecked_domain": "mid <= len",
            "as_mut_ptr": (
                "slice-to-thin mutable cast preserves address, allocation, "
                "provenance, borrow, and layout"
            ),
            "pointer_add": (
                "base + mid * element_size, preserving allocation/provenance; "
                "one-past-end is admitted"
            ),
            "unchecked_sub": "len - mid under mid <= len",
            "raw_regions": "[0,mid) then [mid,len)",
            "reference_identity": (
                "values, logical range, address, allocation, provenance, "
                "parent borrow, layout, projection, and uniqueness"
            ),
            "zst_disjointness": (
                "range-based; nonempty disjoint regions may have equal addresses"
            ),
            "immediate_final_frame": "unchanged left followed by unchanged right",
        },
        "source_backed_replacements": _source_backed_replacements(
            config, PRIMARY
        ),
        "context_only_trust_site_ids": list(
            config.context_only_trust_site_ids
        ),
        "excluded_retained_trust_site_ids": list(
            config.excluded_trust_site_ids
        ),
        "all_audited_trust_site_ids": list(config.all_trust_site_ids),
        "excluded_from_boundary": [
            "mid",
            "branch and unchecked-domain result",
            "pointer-add result and tail subtraction",
            "left/right regions and structural reference identities",
            "unique derived borrows and immediate final frame",
            "answers, answer encodings, and traces",
        ],
    }


def verus_text(config: SplitTarget) -> str:
    function = config.function_name
    branch = (
        "input.mid <= input.slice.source.len()"
        if config.checked
        else "true"
    )
    valid_domain = (
        "true"
        if config.checked
        else "input.mid <= input.slice.source.len()"
    )
    active_contract = (
        """\
    if branch_succeeds(input) {
        output.has_pair
            && output.left.values
                == input.slice.source.subrange(0, input.mid as int)
            && output.right.values
                == input.slice.source.subrange(
                    input.mid as int,
                    input.slice.source.len() as int,
                )
            && state.backing.source
                == output.left.values + output.right.values
            && state.composed_final == state.backing.source
    } else {
        !output.has_pair
            && state.backing.source == input.slice.source
            && state.composed_final == input.slice.source
    }"""
        if config.checked
        else """\
    output.left.values
            == input.slice.source.subrange(0, input.mid as int)
        && output.right.values
            == input.slice.source.subrange(
                input.mid as int,
                input.slice.source.len() as int,
            )
        && state.backing.source
            == output.left.values + output.right.values
        && state.composed_final == state.backing.source"""
    )
    return f"""\
#![allow(dead_code, unused_imports, unused_variables)]
// Source-backed mutable split model for {config.target}.

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

pub ghost struct PointerIdentity {{
    pub address: int,
    pub allocation: int,
    pub provenance: int,
    pub parent_borrow: int,
    pub element_size: nat,
    pub element_alignment: nat,
}}

pub ghost struct Input {{
    pub slice: SliceIdentity,
    pub mid: nat,
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
    pub has_pair: bool,
    pub split_index: int,
    pub left: RegionIdentity,
    pub right: RegionIdentity,
}}

pub ghost struct FinalState {{
    pub base_ptr: PointerIdentity,
    pub mid_ptr: PointerIdentity,
    pub tail_length: int,
    pub backing: SliceIdentity,
    pub left: RegionIdentity,
    pub right: RegionIdentity,
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
        element_alignment: 1,
        projection: 0,
        unique: false,
    }}
}}

pub open spec fn empty_pointer() -> PointerIdentity {{
    PointerIdentity {{
        address: 0,
        allocation: 0,
        provenance: 0,
        parent_borrow: 0,
        element_size: 0,
        element_alignment: 1,
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
        element_alignment: slice.element_alignment,
        projection,
        unique: true,
    }}
}}

pub open spec fn valid_input(input: Input) -> bool {{
    {valid_domain}
}}

pub open spec fn branch_succeeds(input: Input) -> bool {{
    {branch}
}}

pub open spec fn as_mut_ptr_cast_transition(
    slice: SliceIdentity,
) -> PointerIdentity {{
    PointerIdentity {{
        address: slice.address,
        allocation: slice.allocation,
        provenance: slice.provenance,
        parent_borrow: slice.parent_borrow,
        element_size: slice.element_size,
        element_alignment: slice.element_alignment,
    }}
}}

pub open spec fn pointer_add_transition(
    ptr: PointerIdentity,
    count: nat,
) -> PointerIdentity {{
    PointerIdentity {{
        address: ptr.address + count as int * ptr.element_size as int,
        allocation: ptr.allocation,
        provenance: ptr.provenance,
        parent_borrow: ptr.parent_borrow,
        element_size: ptr.element_size,
        element_alignment: ptr.element_alignment,
    }}
}}

pub open spec fn unchecked_sub_transition(input: Input) -> int
    recommends input.mid <= input.slice.source.len()
{{
    input.slice.source.len() as int - input.mid as int
}}

pub open spec fn raw_slice_regions(
    input: Input,
) -> (RegionIdentity, RegionIdentity)
    recommends input.mid <= input.slice.source.len()
{{
    (
        make_region(input.slice, 0, input.mid as int, 1),
        make_region(
            input.slice,
            input.mid as int,
            unchecked_sub_transition(input),
            2,
        ),
    )
}}

pub open spec fn source_output(input: Input) -> Output {{
    if branch_succeeds(input) {{
        let regions = raw_slice_regions(input);
        Output {{
            has_pair: true,
            split_index: input.mid as int,
            left: regions.0,
            right: regions.1,
        }}
    }} else {{
        Output {{
            has_pair: false,
            split_index: -1,
            left: empty_region(),
            right: empty_region(),
        }}
    }}
}}

pub open spec fn source_state(input: Input) -> FinalState {{
    if branch_succeeds(input) {{
        let base_ptr = as_mut_ptr_cast_transition(input.slice);
        let mid_ptr = pointer_add_transition(base_ptr, input.mid);
        let regions = raw_slice_regions(input);
        FinalState {{
            base_ptr,
            mid_ptr,
            tail_length: unchecked_sub_transition(input),
            backing: input.slice,
            left: regions.0,
            right: regions.1,
            composed_final: regions.0.values + regions.1.values,
            unique_partition: true,
            elements_unchanged: true,
        }}
    }} else {{
        FinalState {{
            base_ptr: empty_pointer(),
            mid_ptr: empty_pointer(),
            tail_length: -1,
            backing: input.slice,
            left: empty_region(),
            right: empty_region(),
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
        && boundary.element_alignment == input.slice.element_alignment
}}

pub open spec fn active_contract(
    input: Input,
    output: Output,
    state: FinalState,
) -> bool {{
{active_contract}
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
        && left.element_alignment == right.element_alignment
        && left.projection == right.projection
        && left.unique == right.unique
}}

pub open spec fn same_pointer(
    left: PointerIdentity,
    right: PointerIdentity,
) -> bool {{
    left.address == right.address
        && left.allocation == right.allocation
        && left.provenance == right.provenance
        && left.parent_borrow == right.parent_borrow
        && left.element_size == right.element_size
        && left.element_alignment == right.element_alignment
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
        && left.element_alignment == right.element_alignment
}}

pub open spec fn same_output(left: Output, right: Output) -> bool {{
    left.has_pair == right.has_pair
        && left.split_index == right.split_index
        && same_region(left.left, right.left)
        && same_region(left.right, right.right)
}}

pub open spec fn same_state(
    left: FinalState,
    right: FinalState,
) -> bool {{
    same_pointer(left.base_ptr, right.base_ptr)
        && same_pointer(left.mid_ptr, right.mid_ptr)
        && left.tail_length == right.tail_length
        && same_slice(left.backing, right.backing)
        && same_region(left.left, right.left)
        && same_region(left.right, right.right)
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
    reveal(same_pointer);
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
