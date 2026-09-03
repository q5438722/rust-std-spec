#!/usr/bin/env python3
"""Source-backed obligations for mutable Slice view construction targets."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, replace
from typing import Any

from checker_guards import GuardError, validate_obligation


PRIMARY = "completeness-modulo-reviewed-equivalence"
EXACT_OUTPUT = "exact-output-determinism"
PURPOSES = (PRIMARY, EXACT_OUTPUT)
VERUS_EXPECTED_SUMMARY = "verification results:: 2 verified, 0 errors"

SLICE_SOURCE_PATH = "core/src/slice/mod.rs"
SLICE_SOURCE_SHA256 = (
    "58901fa6437dbd4d77c68427bbced0fc3a91a10fdb8bd2e233adf6a9ba27d2d5"
)
RAW_SLICE_SOURCE_PATH = "core/src/slice/raw.rs"
RAW_SLICE_SOURCE_SHA256 = (
    "0914968067f7e2bc798680c1edd72bcb032a9fd44ebb2b6fbc082a3a2b16941f"
)
MUT_PTR_SOURCE_PATH = "core/src/ptr/mut_ptr.rs"
MUT_PTR_SOURCE_SHA256 = (
    "f6da79cac4ff864801bb186481a19393e6e4cb66636327295b40550769af4fa8"
)
PTR_SOURCE_PATH = "core/src/ptr/mod.rs"
PTR_SOURCE_SHA256 = (
    "1fd4ecb1650cfc995f29a172ad3f72ffa378702ea55493eabf6a80355b38035e"
)
ARRAY_SOURCE_PATH = "core/src/array/mod.rs"
ARRAY_SOURCE_SHA256 = (
    "f12c8f30d5f6c57d5fb9f382eed072f0362c4b948c749e1c85b4cc23fe2bd01d"
)
ARRAY_FROM_MUT_EXCERPT_SHA256 = (
    "557605d2b9fe70d8f06e0ef29f7cd7dc71a38328bbf23ff93315c2769ede6cd7"
)
VOCABULARY_RANGES = ((913, 944),)
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
            "slice_as_mut_ptr",
            SLICE_SOURCE_PATH,
            757,
            759,
            SLICE_SOURCE_SHA256,
            "canonical_slice_as_mut_ptr.rs",
            ("self as *mut [T] as *mut T",),
        ),
        CanonicalSource(
            "mut_ptr_cast",
            MUT_PTR_SOURCE_PATH,
            27,
            33,
            MUT_PTR_SOURCE_SHA256,
            "canonical_mut_ptr_cast.rs",
            ("pub const fn cast<U>(self) -> *mut U", "self as _"),
        ),
        CanonicalSource(
            "mut_ptr_cast_array",
            MUT_PTR_SOURCE_PATH,
            1999,
            2001,
            MUT_PTR_SOURCE_SHA256,
            "canonical_mut_ptr_cast_array.rs",
            (
                "pub const fn cast_array<const N: usize>(self) -> *mut [T; N]",
                "self.cast()",
            ),
        ),
        CanonicalSource(
            "slice_from_raw_parts_mut",
            RAW_SLICE_SOURCE_PATH,
            179,
            196,
            RAW_SLICE_SOURCE_SHA256,
            "canonical_slice_from_raw_parts_mut.rs",
            (
                "pub const unsafe fn from_raw_parts_mut",
                "maybe_is_aligned_and_not_null",
                "&mut *ptr::slice_from_raw_parts_mut(data, len)",
            ),
        ),
        CanonicalSource(
            "ptr_slice_from_raw_parts_mut",
            PTR_SOURCE_PATH,
            1225,
            1227,
            PTR_SOURCE_SHA256,
            "canonical_ptr_slice_from_raw_parts_mut.rs",
            (
                "pub const fn slice_from_raw_parts_mut",
                "from_raw_parts_mut(data, len)",
            ),
        ),
        CanonicalSource(
            "array_from_mut",
            ARRAY_SOURCE_PATH,
            174,
            177,
            ARRAY_SOURCE_SHA256,
            "canonical_array_from_mut.rs",
            (
                "pub const fn from_mut<T>(s: &mut T) -> &mut [T; 1]",
                "(s as *mut T).cast::<[T; 1]>()",
            ),
        ),
    )
}


@dataclass(frozen=True)
class MutableViewTarget:
    target: str
    input_order: str
    artifact_id: str
    kind: str
    active_contract_sha256: str
    active_contract_text: str
    generated_declaration_sha256: str
    source_path: str
    source_file_sha256: str
    source_start: int
    source_end: int
    source_item_sha256: str
    docs_start: int
    docs_end: int
    public_docs_sha256: str
    harness_sha256: str
    source_body_manifest_sha256: str
    transformation_manifest_sha256: str
    dependency_manifest_sha256: str
    trust_record_sha256: tuple[tuple[str, str], ...]
    context_only_trust_site_ids: tuple[str, ...]
    excluded_trust_site_ids: tuple[str, ...]
    helper_names: tuple[str, ...]
    source_fragments: tuple[str, ...]
    docs_fragments: tuple[str, ...]
    vocabulary_fragments: tuple[str, ...]

    @property
    def function_name(self) -> str:
        return self.target.rsplit("::", 1)[-1]

    @property
    def source_reference(self) -> str:
        return f"{self.source_path}:{self.source_start}-{self.source_end}"

    @property
    def docs_reference(self) -> str:
        return f"{self.source_path}:{self.docs_start}-{self.docs_end}"

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
    def all_trust_site_ids(self) -> tuple[str, ...]:
        return tuple(record_id for record_id, _ in self.trust_record_sha256)

    @property
    def trust_hashes(self) -> dict[str, str]:
        return dict(self.trust_record_sha256)

    @property
    def admitted_trust_site_ids(self) -> tuple[str, ...]:
        context = set(self.context_only_trust_site_ids)
        excluded = set(self.excluded_trust_site_ids)
        return tuple(
            site
            for site in self.all_trust_site_ids
            if site not in context and site not in excluded
        )

    @property
    def replacement_id(self) -> str:
        return (
            f"SRC-{int(self.input_order):03d}-CANONICAL-MUTABLE-VIEW-"
            "CONSTRUCTION"
        )

    @property
    def expected_solver_results(self) -> dict[str, str]:
        return {
            EXACT_OUTPUT: "unsat",
            PRIMARY: "sat",
        }

    @property
    def expected_classification(self) -> dict[str, str]:
        return {
            "exact_output_determinism_status": "conditional-complete",
            "completeness_modulo_reviewed_equivalence_status": (
                "conditional-incomplete"
            ),
        }


TARGETS = (
    MutableViewTarget(
        target="core::slice::as_flattened_mut",
        input_order="17",
        artifact_id="017_core_slice_as_flattened_mut",
        kind="flatten",
        active_contract_sha256=(
            "a5ef69f84bb6df4db9de0ae1fa18a85f58543273066f89266651e0d57090e756"
        ),
        active_contract_text=(
            "pub assume_specification<T, const N: usize>[ <[[T; N]]>::"
            "as_flattened_mut ]( slice: &mut [[T; N]], ) -> (ret: &mut "
            "[T]) ensures ret@ == flatten_array_chunks::<T, N>(old(slice)@), "
            "flatten_array_chunks::<T, N>(final(slice)@) == final(ret)@, ;"
        ),
        generated_declaration_sha256=(
            "357c043a08d8ac465e740ff1915de3deee4fb55b147dfb1699c9bcb6c5b84735"
        ),
        source_path=SLICE_SOURCE_PATH,
        source_file_sha256=SLICE_SOURCE_SHA256,
        source_start=5487,
        source_end=5497,
        source_item_sha256=(
            "d3fdd4bf0c5162b4000f8b7d767f7802944c5834053070e69dd3469f640dc5a2"
        ),
        docs_start=5457,
        docs_end=5484,
        public_docs_sha256=(
            "7908de0c40fb04e7c35bbcf338499a2f06f08ab90a3c543c39a10a0906378e4e"
        ),
        harness_sha256=(
            "b53e7533553d3ab89c1ada866cff1967dc0abb224d6f7bd2dea143fc4a3aca00"
        ),
        source_body_manifest_sha256=(
            "5874e3c82723399608d7b37f74e38ce289de8202b1c65f156062b7175b79dc8e"
        ),
        transformation_manifest_sha256=(
            "3eb646cd2457a3cfb4955d105204f00e517811b1d4d269d86c2b5be3783d8e00"
        ),
        dependency_manifest_sha256=(
            "fb38c0fe19a752d2bdde17d4f1b95536a09b0e7fbd5ee0165f93c7afa309059e"
        ),
        trust_record_sha256=(
            ("TS-017-D001", "fd45863a9ae0a3a84798e3d76ab1b7ec9f613df229630e28a2b56b68528e653b"),
            ("TS-017-D002", "aa9c140dbad5da82d7df2ad9b4cc9ef8f1822cc9a353bc847d0f568051ba2bdc"),
            ("TS-017-D003", "1dc37227968d7ecff7d6180e00ba80e9058bedf74a23e40122f71d874e077a75"),
            ("TS-017-D004", "e760332ccc23030fe2738a11d3762e915cee7342c43d0dc5a91bc6f90903ac33"),
            ("TS-017-D005", "917979efcdc133a08ed960063b66e9b0be61abac519d17de9fbacc841782da54"),
            ("TS-017-D006", "011b5a04abac2df197ae9d40465d6e03a776b1bdae2e4b4256282fdb17d3d955"),
            ("TS-017-C001", "3f205673a68f473ecbdedb28175695bc61963ad2674ddedbc118dbd934d7a533"),
            ("TS-017-C002", "8aace6cf6293e05820206e5598acdbe034d6d26b3a78a562dbb4e765fdc9dffe"),
            ("TS-017-C003", "47a062d5379b4f14511fd0adbb09a2e3f803b7fa4b87a86dee4df0f853653af4"),
            ("TS-017-E001", "f3cce3681cd534b398ad0b5773b5143e7738704696c401e7c993b1eb0d93d1d2"),
            ("TS-017-E002", "be5b3706cfe0d4a981bb1e7b2a18abb7f100a9f331687aa490a116d5561f1c3e"),
            ("TS-017-E003", "c2854ff865ab3148524698067b27fa4056cd8effca6e5c441a3ae09d88e9052e"),
            ("TS-017-E004", "0c43c45825819a8b43a520cd5b6c3e7cd07a87ee0de0b582dde75f171d80ecc3"),
        ),
        context_only_trust_site_ids=(
            "TS-017-D001",
            "TS-017-C001",
            "TS-017-C002",
            "TS-017-C003",
        ),
        excluded_trust_site_ids=("TS-017-D006", "TS-017-E004"),
        helper_names=(
            "slice_as_mut_ptr",
            "mut_ptr_cast",
            "slice_from_raw_parts_mut",
            "ptr_slice_from_raw_parts_mut",
        ),
        source_fragments=(
            "if T::IS_ZST",
            'checked_mul(N).expect("slice len overflow")',
            "self.len().unchecked_mul(N)",
            "from_raw_parts_mut(self.as_mut_ptr().cast(), len)",
        ),
        docs_fragments=(
            "This panics if the length of the resulting slice would overflow",
            "only possible when flattening a slice of arrays of zero-sized",
        ),
        vocabulary_fragments=(
            "pub open spec fn array_value_view",
            "pub open spec fn flatten_array_chunks",
        ),
    ),
    MutableViewTarget(
        target="core::slice::as_mut_array",
        input_order="18",
        artifact_id="018_core_slice_as_mut_array",
        kind="whole_array",
        active_contract_sha256=(
            "1ac5b31b2e71effad4bc9503263318d0fe4c53b2aff998e13f2fe9faccab72c4"
        ),
        active_contract_text=(
            "pub assume_specification<T, const N: usize>[ <[T]>::"
            "as_mut_array::<N> ]( slice: &mut [T], ) -> (ret: "
            "Option<&mut [T; N]>) ensures old(slice)@.len() == N ==> "
            "ret.is_some() && array_mut_ref_view(ret.unwrap()) == "
            "old(slice)@ && final(slice)@ == "
            "array_value_view(*final(ret.unwrap())), old(slice)@.len() != "
            "N ==> ret.is_none() && final(slice)@ == old(slice)@, ;"
        ),
        generated_declaration_sha256=(
            "3038bd1a29eebe65fa0ef6ce674bd2e16531ac638a37b403c287659eb8761f20"
        ),
        source_path=SLICE_SOURCE_PATH,
        source_file_sha256=SLICE_SOURCE_SHA256,
        source_start=869,
        source_end=879,
        source_item_sha256=(
            "d2208668f0b01536cedf4b43a19beca6d879c2dca9e7fb2ba16b10a8110d0529"
        ),
        docs_start=862,
        docs_end=864,
        public_docs_sha256=(
            "97b58410072b3efa6d86d54427d5e20ea09f14c42d26dbd89f4403f4ea382221"
        ),
        harness_sha256=(
            "cfb8ce05b5087df04751b6e2e996f83e752f4b4e5c6fd40e9661c58259f3326d"
        ),
        source_body_manifest_sha256=(
            "7b1de8d9b58bfb22e299086e2b0b8bf7133eb20f29535266a5dde018d0d74155"
        ),
        transformation_manifest_sha256=(
            "c63710c5ff71970a23437a097495f4c692da2ee02f9110028bcfc7e3dc20bb50"
        ),
        dependency_manifest_sha256=(
            "5990c3796329b8b80c4f79138f3b84b55beede4dd26b29d6982856cb1b1740c1"
        ),
        trust_record_sha256=(
            ("TS-018-D001", "1f5667ea042db3d857f4cc5eaaa66f4c55afbe7009b19c5c6540976fd2d59a64"),
            ("TS-018-D002", "3a277c40b56823e999adca3704623a94576eef46869cfda88efbfbbe59d66772"),
            ("TS-018-D003", "1a0f3828035f87e94063045294e07b91c213075092fa28e540d84b7d05e2b23e"),
            ("TS-018-D004", "a7da4e6e99feb1258f8b05f95c5249910aa6ff14245202c046e9e87c01f59567"),
            ("TS-018-C001", "6c85637572ed0cb4847359d7b0efe377196b56789e3d0acd0a5d0b766a8d9ae6"),
            ("TS-018-C002", "1468e98956e1273f823d2c26b0378dc406c738e5bf067b5c9268537e9a3873ab"),
            ("TS-018-C003", "861dc58d9424e86c6dbd8d312e8da46daa73522bc2a5740a723d0c85a3b59424"),
            ("TS-018-E001", "27d01fb392b0faade04485e631279fba4cd9a10e5332ca106b302638866f738c"),
            ("TS-018-E002", "d3c2e1a1ea39b4c303d1fe629d584ce5859671472d9c51925f68c278fc025564"),
        ),
        context_only_trust_site_ids=(
            "TS-018-D001",
            "TS-018-C001",
            "TS-018-C002",
            "TS-018-C003",
        ),
        excluded_trust_site_ids=("TS-018-D004", "TS-018-E002"),
        helper_names=("slice_as_mut_ptr", "mut_ptr_cast_array"),
        source_fragments=(
            "if self.len() == N",
            "self.as_mut_ptr().cast_array()",
            "let me = unsafe { &mut *ptr }",
            "Some(me)",
            "None",
        ),
        docs_fragments=(
            "Gets a mutable reference to the slice's underlying array",
            "not exactly equal to the length of `self`",
        ),
        vocabulary_fragments=(
            "pub open spec fn array_mut_ref_view",
            "pub open spec fn array_value_view",
        ),
    ),
    MutableViewTarget(
        target="core::slice::first_chunk_mut",
        input_order="46",
        artifact_id="046_core_slice_first_chunk_mut",
        kind="prefix_array",
        active_contract_sha256=(
            "d8923bf81d0b7f8ad6deaa97aafdc3660f245da6e77099ad672c98478c31ed55"
        ),
        active_contract_text=(
            "pub assume_specification<T, const N: usize>[ <[T]>::"
            "first_chunk_mut::<N> ]( slice: &mut [T], ) -> (ret: "
            "Option<&mut [T; N]>) ensures (N as int) <= old(slice)@.len() "
            "==> ret.is_some() && array_mut_ref_view(ret.unwrap()) == "
            "slice_fixed_prefix::<T, N>(old(slice)@) && final(slice)@ == "
            "array_value_view(*final(ret.unwrap())) + "
            "old(slice)@.subrange(N as int, old(slice)@.len() as int), "
            "(N as int) > old(slice)@.len() ==> ret.is_none() && "
            "final(slice)@ == old(slice)@, ;"
        ),
        generated_declaration_sha256=(
            "80d843c11528fb69d8d4baa81da12a588f171bade1924808a8a701f40d72798b"
        ),
        source_path=SLICE_SOURCE_PATH,
        source_file_sha256=SLICE_SOURCE_SHA256,
        source_start=357,
        source_end=366,
        source_item_sha256=(
            "2170d94c79e1f26619cef13c46a6700a5a217819967b3a26a6ec3dc9fc9e703d"
        ),
        docs_start=337,
        docs_end=353,
        public_docs_sha256=(
            "7bc0017183e358cb6071dc4d56633231d9169237ae01bb65173d86f24323972f"
        ),
        harness_sha256=(
            "aeca88005b9fcb5798c1d8f3c6fb5684955bf89a0c5efdf4e512cd1b1e2854fe"
        ),
        source_body_manifest_sha256=(
            "a0c9a839fc5f47128da51c0b70953362eec87bbfbe9d5c4e81e59a1c4b31c8c2"
        ),
        transformation_manifest_sha256=(
            "879ad4a8ede98978e6ed81de613df0290cff190ccf06d2a00f6ba655b842a978"
        ),
        dependency_manifest_sha256=(
            "b13a139a2cb52a1b16ebeb495d00c1feeac01767c6ab84567f8fea406fac80d4"
        ),
        trust_record_sha256=(
            ("TS-046-D001", "b667d9df819f914dbb3e1ed5cc296b8b942f56cb1b295f09f5d8e73ca5682f65"),
            ("TS-046-D002", "07996761b0ab3c61bc2dc225e96132610b1d83ecf142c2c47164c7e274075e96"),
            ("TS-046-D003", "f0c44b02eba6b8826eba4f409d80341a0ba4255c1039a8a0791002433bf34f51"),
            ("TS-046-D004", "e8671c3140c3c764696da892bcf15d14cf644e04344bb57c4f0be2ab7413c497"),
            ("TS-046-C001", "b13054b500612e51be8a99f4dd7a0b3d316171344864d308342a8e0bede713a4"),
            ("TS-046-C002", "63280403b9f88e47df1f26aafebe41e23639c5d99a0d7bc1676557fe99b9f643"),
            ("TS-046-C003", "834005a678c43331b900825bb68da37b6270c685c1d6c7d7605907f4a6f2cd5a"),
            ("TS-046-E001", "741827c6ad1ba9e455db0bb0af2d9de81bc321c98130c31970ea73621a993f2b"),
            ("TS-046-E002", "23895cadee51c0fcf7d58879a441283fd418b526b90aea206ba0e18a80961050"),
        ),
        context_only_trust_site_ids=(
            "TS-046-D001",
            "TS-046-C001",
            "TS-046-C002",
            "TS-046-C003",
        ),
        excluded_trust_site_ids=("TS-046-D004", "TS-046-E002"),
        helper_names=("slice_as_mut_ptr", "mut_ptr_cast_array"),
        source_fragments=(
            "if self.len() < N",
            "self.as_mut_ptr().cast_array()",
            "Some(unsafe { &mut *",
        ),
        docs_fragments=(
            "Returns a mutable array reference to the first `N` items",
            "not at least `N` in length",
        ),
        vocabulary_fragments=(
            "pub open spec fn array_mut_ref_view",
            "pub open spec fn array_value_view",
            "pub open spec fn slice_fixed_prefix",
        ),
    ),
    MutableViewTarget(
        target="core::slice::from_mut",
        input_order="47",
        artifact_id="047_core_slice_from_mut",
        kind="singleton",
        active_contract_sha256=(
            "80ebb45d323e9d8d8aed367f6a62490611719746be7d20704ab6df5d59a5d4a7"
        ),
        active_contract_text=(
            "pub assume_specification<'a, T>[ core::slice::from_mut::<T> ]( "
            "value: &'a mut T, ) -> (ret: &'a mut [T]) ensures ret@ == "
            "seq![*old(value)], final(ret)@ == seq![*final(value)], ;"
        ),
        generated_declaration_sha256=(
            "1a5f2fa2211049e59be3145fd7f97398eeafda674ca6154cf5d35893f860ccbb"
        ),
        source_path=RAW_SLICE_SOURCE_PATH,
        source_file_sha256=RAW_SLICE_SOURCE_SHA256,
        source_start=211,
        source_end=213,
        source_item_sha256=(
            "9dccff9babfff3c297268487fbf17b0a6ca139a9d1de3ef5c1163f9995eb7235"
        ),
        docs_start=207,
        docs_end=207,
        public_docs_sha256=(
            "12e3b0a4f5ad91cbb4a9c19a78d62056a8ab4888df0feb61c03a87fec61d7d67"
        ),
        harness_sha256=(
            "d567e471ad0120f734126d09b1532b7ba37f1ff982ba6a65419aeae533457ddd"
        ),
        source_body_manifest_sha256=(
            "84936acd7c59966e48aab41c937343789c7492a4916c99980b3c23b005c12f7b"
        ),
        transformation_manifest_sha256=(
            "6a7c6c0ba38fa01ca6ca280f43152757633eb8de40c5be941170a6b269eb904d"
        ),
        dependency_manifest_sha256=(
            "543428ae66b72821b472a73762ce4e3733899792d482346759f7b13328e00133"
        ),
        trust_record_sha256=(
            ("TS-047-D001", "0d9e6368e797978f6161b7e1477ba70c1f819724b362b616c7bd41758655ed98"),
            ("TS-047-D002", "cbf032647319897cfbb8a91f3a9746f5ef0463c2fba9c2e1b3fbb8b262e14db3"),
            ("TS-047-E001", "1af1296855f055cf0558b00742420c08a85b54933747a00d8475d459923b1c89"),
        ),
        context_only_trust_site_ids=("TS-047-D002",),
        excluded_trust_site_ids=("TS-047-D001", "TS-047-E001"),
        helper_names=("array_from_mut",),
        source_fragments=("array::from_mut(s)",),
        docs_fragments=(
            "Converts a reference to T into a slice of length 1",
        ),
        vocabulary_fragments=(),
    ),
)

TARGET_BY_ARTIFACT = {config.artifact_id: config for config in TARGETS}
TARGET_KEYS = tuple((config.target, config.input_order) for config in TARGETS)


INPUT_FIELDS = (
    ("x_source", "(Seq Int)"),
    ("x_container_length", "Int"),
    ("x_n", "Int"),
    ("x_address", "Int"),
    ("x_allocation", "Int"),
    ("x_provenance", "Int"),
    ("x_root_borrow", "Int"),
    ("x_allocation_base", "Int"),
    ("x_allocation_bytes", "Int"),
    ("x_element_size", "Int"),
    ("x_element_alignment", "Int"),
    ("x_usize_max", "Int"),
    ("x_isize_max", "Int"),
    ("x_alias_exclusive", "Bool"),
    ("x_borrow_alive", "Bool"),
    ("x_outside_frame", "(Seq Int)"),
)
BOUNDARY_FIELDS = (
    ("b_initial_memory", "(Seq Int)", "input_memory"),
    ("b_address", "Int", "input_provenance"),
    ("b_allocation", "Int", "input_provenance"),
    ("b_provenance", "Int", "input_provenance"),
    ("b_root_borrow", "Int", "input_provenance"),
    ("b_allocation_base", "Int", "input_provenance"),
    ("b_allocation_bytes", "Int", "input_provenance"),
    ("b_element_size", "Int", "input_layout"),
    ("b_element_alignment", "Int", "input_layout"),
    ("b_usize_max", "Int", "input_layout"),
    ("b_isize_max", "Int", "input_layout"),
    ("b_alias_exclusive", "Bool", "input_provenance"),
    ("b_borrow_alive", "Bool", "input_provenance"),
    ("b_outside_frame", "(Seq Int)", "input_memory"),
)
OUTPUT_FIELDS = (
    ("y_panicked", "Bool"),
    ("y_is_some", "Bool"),
    ("y_values", "(Seq Int)"),
    ("y_start", "Int"),
    ("y_length", "Int"),
    ("y_address", "Int"),
    ("y_allocation", "Int"),
    ("y_provenance", "Int"),
    ("y_root_borrow", "Int"),
    ("y_element_size", "Int"),
    ("y_element_alignment", "Int"),
    ("y_projection", "Int"),
    ("y_unique", "Bool"),
)
STATE_FIELDS = (
    ("s_input_final", "(Seq Int)"),
    ("s_return_final", "(Seq Int)"),
    ("s_outside_final", "(Seq Int)"),
    ("s_backing_address", "Int"),
    ("s_backing_allocation", "Int"),
    ("s_backing_provenance", "Int"),
    ("s_backing_root_borrow", "Int"),
    ("s_frame_unchanged", "Bool"),
    ("s_panic_before_borrow", "Bool"),
)


def canonical_json_sha256(record: dict[str, str]) -> str:
    payload = json.dumps(
        record, sort_keys=True, separators=(",", ":")
    ).encode()
    return hashlib.sha256(payload).hexdigest()


def _normalized(text: str) -> str:
    return " ".join(text.split())


def validate_source_anchors(
    config: MutableViewTarget,
    source_item: str,
    public_docs: str,
    vocabulary: str,
    helpers: dict[str, str],
) -> None:
    source = _normalized(source_item)
    docs = _normalized(public_docs)
    for fragment in config.source_fragments:
        if _normalized(fragment) not in source:
            raise GuardError(
                f"{config.target}: canonical source fragment absent: {fragment}"
            )
    for fragment in config.docs_fragments:
        if _normalized(fragment) not in docs:
            raise GuardError(
                f"{config.target}: public docs fragment absent: {fragment}"
            )
    for fragment in config.vocabulary_fragments:
        if fragment not in vocabulary:
            raise GuardError(
                f"{config.target}: generated vocabulary fragment absent: {fragment}"
            )
    if set(helpers) != set(config.helper_names):
        raise GuardError(f"{config.target}: canonical helper set changed")
    for helper in config.helper_sources:
        normalized = _normalized(helpers[helper.name])
        for fragment in helper.fragments:
            if _normalized(fragment) not in normalized:
                raise GuardError(
                    f"{config.target}: {helper.name} fragment absent: {fragment}"
                )
    if config.kind == "singleton":
        excerpt = helpers["array_from_mut"]
        if hashlib.sha256(excerpt.encode()).hexdigest() != (
            ARRAY_FROM_MUT_EXCERPT_SHA256
        ):
            raise GuardError("core::array::from_mut excerpt hash changed")
    prohibited = (
        "TargetDefinition_T",
        "Equivalent_T",
        "assume_specification",
        "Provenance::null()",
        "null_mut::<",
    )
    if any(
        token in text
        for token in prohibited
        for text in (source_item, *helpers.values())
    ):
        raise GuardError(f"{config.target}: synthetic source helper detected")


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


def _product() -> str:
    return "(* (x_container_length x) (x_n x))"


def _panics(config: MutableViewTarget) -> str:
    if config.kind != "flatten":
        return "false"
    return (
        f"(and (= (x_element_size x) 0) "
        f"(> {_product()} (x_usize_max x)))"
    )


def _success(config: MutableViewTarget) -> str:
    if config.kind == "flatten":
        return f"(not {_panics(config)})"
    if config.kind == "whole_array":
        return "(= (x_container_length x) (x_n x))"
    if config.kind == "prefix_array":
        return "(<= (x_n x) (x_container_length x))"
    return "true"


def _result_length(config: MutableViewTarget) -> str:
    if config.kind == "flatten":
        return _product()
    if config.kind in {"whole_array", "prefix_array"}:
        return "(x_n x)"
    return "1"


def _result_values(config: MutableViewTarget) -> str:
    if config.kind == "prefix_array":
        return "(seq.extract (x_source x) 0 (x_n x))"
    return "(x_source x)"


def _reconstructed_input(
    config: MutableViewTarget,
    return_values: str,
) -> str:
    if config.kind == "prefix_array":
        return (
            f"(seq.++ {return_values} "
            "(seq.extract (x_source x) (x_n x) "
            "(- (x_container_length x) (x_n x))))"
        )
    return return_values


def _projection(config: MutableViewTarget) -> int:
    return 3 if config.kind in {"flatten", "singleton"} else 2


def _input_boundary_observed() -> str:
    equalities = (
        ("b_initial_memory", "x_source"),
        ("b_address", "x_address"),
        ("b_allocation", "x_allocation"),
        ("b_provenance", "x_provenance"),
        ("b_root_borrow", "x_root_borrow"),
        ("b_allocation_base", "x_allocation_base"),
        ("b_allocation_bytes", "x_allocation_bytes"),
        ("b_element_size", "x_element_size"),
        ("b_element_alignment", "x_element_alignment"),
        ("b_usize_max", "x_usize_max"),
        ("b_isize_max", "x_isize_max"),
        ("b_alias_exclusive", "x_alias_exclusive"),
        ("b_borrow_alive", "x_borrow_alive"),
        ("b_outside_frame", "x_outside_frame"),
    )
    clauses = "\n       ".join(
        f"(= ({boundary} b) ({input_field} x))"
        for boundary, input_field in equalities
    )
    return f"""\
(define-fun InputBoundaryObserved ((x Input) (b Boundary)) Bool
  (and {clauses}))"""


def _reference_valid() -> str:
    return """\
(define-fun ReferenceRepresentationValid ((x Input) (b Boundary)) Bool
  (let ((span (* (seq.len (x_source x)) (b_element_size b))))
    (and (> (b_address b) 0)
         (> (b_element_alignment b) 0)
         (= (mod (b_address b) (b_element_alignment b)) 0)
         (>= (b_element_size b) 0)
         (or (= (b_element_size b) 0)
             (= (mod (b_element_size b) (b_element_alignment b)) 0))
         (> (b_root_borrow b) 0)
         (b_alias_exclusive b)
         (b_borrow_alive b)
         (> (b_usize_max b) 0)
         (> (b_isize_max b) 0)
         (<= (b_isize_max b) (b_usize_max b))
         (<= (b_address b) (b_usize_max b))
         (>= (b_allocation_base b) 0)
         (>= (b_allocation_bytes b) 0)
         (<= (b_allocation_bytes b) (b_usize_max b))
         (>= span 0)
         (<= span (b_isize_max b))
         (<= (+ (b_address b) span) (b_usize_max b))
         (=> (> (b_element_size b) 0)
             (<= (seq.len (x_source x)) (b_usize_max b)))
         (or (= span 0)
             (and (> (b_allocation b) 0)
                  (> (b_provenance b) 0)
                  (<= (b_allocation_base b) (b_address b))
                  (<= (+ (b_address b) span)
                      (+ (b_allocation_base b)
                         (b_allocation_bytes b)))
                  (<= (+ (b_allocation_base b)
                         (b_allocation_bytes b))
                      (b_usize_max b)))))))"""


def _length_transition(config: MutableViewTarget) -> str:
    return f"""\
(define-fun LengthMultiplicationAndOverflowTransition
  ((x Input) (y Output)) Bool
  (and (= (y_panicked y) {_panics(config)})
       (= (y_length y)
          (ite {_success(config)} {_result_length(config)} 0))))"""


def _branch_transition(config: MutableViewTarget) -> str:
    return f"""\
(define-fun BranchSelectionTransition ((x Input) (y Output)) Bool
  (= (y_is_some y) {_success(config)}))"""


def _pointer_transition(config: MutableViewTarget) -> str:
    success = _success(config)
    return f"""\
(define-fun MutablePointerExtractionAndCastTransition
  ((x Input) (y Output)) Bool
  (ite {success}
       (and (= (y_address y) (x_address x))
            (= (y_allocation y) (x_allocation x))
            (= (y_provenance y) (x_provenance x))
            (= (y_root_borrow y) (x_root_borrow x))
            (= (y_element_size y) (x_element_size x))
            (= (y_element_alignment y) (x_element_alignment x)))
       (and (= (y_address y) 0)
            (= (y_allocation y) 0)
            (= (y_provenance y) 0)
            (= (y_root_borrow y) 0)
            (= (y_element_size y) 0)
            (= (y_element_alignment y) 0))))"""


def _reference_construction_transition(config: MutableViewTarget) -> str:
    return f"""\
(define-fun RawSliceOrArrayReferenceConstructionTransition
  ((x Input) (y Output)) Bool
  (ite {_success(config)}
       (and (= (y_values y) {_result_values(config)})
            (= (y_start y) 0)
            (= (y_length y) {_result_length(config)}))
       (and (= (y_values y) {EMPTY_SEQ})
            (= (y_start y) 0)
            (= (y_length y) 0))))"""


def _return_type_transition(config: MutableViewTarget) -> str:
    name = (
        "SingletonArrayToSliceUnsizeTransition"
        if config.kind == "singleton"
        else "MutableArrayOrSliceReturnTransition"
    )
    return f"""\
(define-fun {name} ((x Input) (y Output)) Bool
  (ite {_success(config)}
       (and (= (y_projection y) {_projection(config)})
            (= (y_unique y) true))
       (and (= (y_projection y) 0)
            (= (y_unique y) false))))"""


def _final_frame_transition(config: MutableViewTarget) -> str:
    reconstructed = _reconstructed_input(
        config,
        "(s_return_final s)",
    )
    return f"""\
(define-fun BorrowLifetimeFinalFrameTransition
  ((x Input) (y Output) (s State)) Bool
  (and (= (seq.len (s_input_final s)) (seq.len (x_source x)))
       (= (seq.len (s_return_final s)) (y_length y))
       (ite {_success(config)}
            (= (s_input_final s) {reconstructed})
            (and (= (s_input_final s) (x_source x))
                 (= (s_return_final s) {EMPTY_SEQ})))
       (= (s_outside_final s) (x_outside_frame x))
       (= (s_backing_address s) (x_address x))
       (= (s_backing_allocation s) (x_allocation x))
       (= (s_backing_provenance s) (x_provenance x))
       (= (s_backing_root_borrow s) (x_root_borrow x))
       (= (s_frame_unchanged s) true)
       (= (s_panic_before_borrow s) {_panics(config)})))"""


def _active_contract(config: MutableViewTarget, purpose: str) -> str:
    success = _success(config)
    if config.kind == "flatten":
        output = f"""\
  (and (=> (not {_panics(config)})
           (= (y_values y) (x_source x)))
       (=> {_panics(config)} (y_panicked y)))"""
        frame = (
            f"""\
       (=> (not {_panics(config)})
           (= (s_input_final s) (s_return_final s)))"""
        )
    elif config.kind == "whole_array":
        output = f"""\
  (and (=> (= (x_container_length x) (x_n x))
           (and (y_is_some y)
                (= (y_values y) (x_source x))))
       (=> (distinct (x_container_length x) (x_n x))
           (not (y_is_some y))))"""
        frame = f"""\
       (=> {success}
           (= (s_input_final s) (s_return_final s)))
       (=> (not {success})
           (= (s_input_final s) (x_source x)))"""
    elif config.kind == "prefix_array":
        output = f"""\
  (and (=> (<= (x_n x) (x_container_length x))
           (and (y_is_some y)
                (= (y_values y)
                   (seq.extract (x_source x) 0 (x_n x)))))
       (=> (> (x_n x) (x_container_length x))
           (not (y_is_some y))))"""
        frame = f"""\
       (=> {success}
           (= (s_input_final s)
              (seq.++ (s_return_final s)
                      (seq.extract
                        (x_source x)
                        (x_n x)
                        (- (x_container_length x) (x_n x))))))
       (=> (not {success})
           (= (s_input_final s) (x_source x)))"""
    else:
        output = """\
  (and (y_is_some y)
       (= (y_values y) (x_source x))
       (= (y_length y) 1))"""
        frame = """\
       (= (s_return_final s) (s_input_final s))"""
    if purpose == EXACT_OUTPUT:
        return f"""\
(define-fun ActiveGeneratedContractTransition
  ((x Input) (y Output)) Bool
{output})"""
    return f"""\
(define-fun ActiveGeneratedContractTransition
  ((x Input) (y Output) (s State)) Bool
  (and {output.strip()}
{frame}))"""


def _source_transition_names(
    config: MutableViewTarget,
    purpose: str,
) -> list[str]:
    names = [
        "LengthMultiplicationAndOverflowTransition",
        "BranchSelectionTransition",
        "MutablePointerExtractionAndCastTransition",
        "RawSliceOrArrayReferenceConstructionTransition",
        (
            "SingletonArrayToSliceUnsizeTransition"
            if config.kind == "singleton"
            else "MutableArrayOrSliceReturnTransition"
        ),
    ]
    if purpose == PRIMARY:
        names.append("BorrowLifetimeFinalFrameTransition")
    return names


def _target_definition(config: MutableViewTarget, purpose: str) -> str:
    return_type = (
        "SingletonArrayToSliceUnsizeTransition"
        if config.kind == "singleton"
        else "MutableArrayOrSliceReturnTransition"
    )
    calls = [
        "(InputBoundaryObserved x b)",
        "(ReferenceRepresentationValid x b)",
        "(LengthMultiplicationAndOverflowTransition x y)",
        "(BranchSelectionTransition x y)",
        "(MutablePointerExtractionAndCastTransition x y)",
        "(RawSliceOrArrayReferenceConstructionTransition x y)",
        f"({return_type} x y)",
        (
            "(ActiveGeneratedContractTransition x y)"
            if purpose == EXACT_OUTPUT
            else "(BorrowLifetimeFinalFrameTransition x y s)"
        ),
    ]
    if purpose == PRIMARY:
        calls.append("(ActiveGeneratedContractTransition x y s)")
    return """\
(define-fun TargetDefinition_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and %s))""" % "\n       ".join(calls)


def _requires(config: MutableViewTarget) -> str:
    if config.kind == "flatten":
        shape = f"(= (seq.len (x_source x)) {_product()})"
    else:
        shape = "(= (seq.len (x_source x)) (x_container_length x))"
    singleton = (
        "(= (x_container_length x) 1)\n"
        "       (= (x_n x) 1)"
        if config.kind == "singleton"
        else "true"
    )
    return f"""\
(define-fun Requires_T ((x Input)) Bool
  (and {shape}
       (>= (x_container_length x) 0)
       (>= (x_n x) 0)
       (>= (x_element_size x) 0)
       (> (x_element_alignment x) 0)
       (> (x_usize_max x) 0)
       (> (x_isize_max x) 0)
       (<= (x_container_length x) (x_usize_max x))
       (<= (x_n x) (x_usize_max x))
       {singleton}))"""


def _equivalence(purpose: str) -> str:
    clauses = [
        f"(= ({selector} y1) ({selector} y2))"
        for selector, _ in OUTPUT_FIELDS
    ]
    if purpose == PRIMARY:
        clauses.extend(
            f"(= ({selector} s1) ({selector} s2))"
            for selector, _ in STATE_FIELDS
        )
    return """\
(define-fun Equivalent_T
  ((x Input) (b Boundary)
   (y1 Output) (s1 State) (y2 Output) (s2 State)) Bool
  (and %s))""" % "\n       ".join(clauses)


def model_text(
    config: MutableViewTarget,
    purpose: str,
    *,
    include_theorem: bool = False,
) -> str:
    if purpose not in PURPOSES:
        raise ValueError(f"{config.target}: unknown purpose {purpose}")
    boundary_fields = tuple(
        (selector, sort) for selector, sort, _ in BOUNDARY_FIELDS
    )
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
    return f"""\
; Target: {config.target}
; Active contract SHA-256: {config.active_contract_sha256}
; Purpose: {purpose}
; Boundary_T contains only initial memory, representation, layout, platform,
; exclusive-root-borrow, and outside-frame observations.
(set-logic ALL)
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
{_input_boundary_observed()}
{_reference_valid()}
{_length_transition(config)}
{_branch_transition(config)}
{_pointer_transition(config)}
{_reference_construction_transition(config)}
{_return_type_transition(config)}
{_final_frame_transition(config) if purpose == PRIMARY else ""}
{_active_contract(config, purpose)}
{_target_definition(config, purpose)}
{_requires(config)}
(define-fun Boundary_T ((x Input) (b Boundary)) Bool
  (and (InputBoundaryObserved x b)
       (ReferenceRepresentationValid x b)))
(define-fun Spec_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (TargetDefinition_T x b y s))
{_equivalence(purpose)}
{theorem}"""


def obligation_text(config: MutableViewTarget, purpose: str) -> str:
    return model_text(config, purpose, include_theorem=True)


def _boundary_metadata(config: MutableViewTarget) -> list[dict[str, Any]]:
    return [
        {
            "selector": selector,
            "role": role,
            "source_citations": list(config.source_citations),
            "trust_site_ids": list(config.admitted_trust_site_ids),
            "source_backed_replacement_ids": [config.replacement_id],
        }
        for selector, _, role in BOUNDARY_FIELDS
    ]


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


def obligation_metadata(
    config: MutableViewTarget,
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
        "domain": {
            "source_model_complete": True,
            "active_preconditions": (
                "none beyond Rust type/reference validity; Requires_T contains "
                "only integer encoding and input-shape facts"
            ),
            "panic": (
                "as_flattened_mut panics exactly when T is zero-sized and "
                "container_length * N exceeds usize::MAX"
            ),
            "unchecked_multiplication": (
                "non-ZST multiplication is admitted only when the valid "
                "reference span proves that its product fits"
            ),
        },
        "contract_translation": {
            "active_contract_preserved": True,
            "opaque_vocabulary_declared_to_solver": False,
            "canonical_answer_conjoined_outside_active_contract": False,
            "source_flow": [
                "compute checked or valid unchecked length multiplication",
                "select the exact panic/Some/None branch",
                "extract the mutable pointer and preserve identity",
                "perform the source pointer cast",
                "construct the exact raw slice or mutable array reference",
                (
                    "unsize the singleton array reference to a mutable slice"
                    if config.kind == "singleton"
                    else "preserve the target return type projection"
                ),
                "derive the exact returned range and root-borrow identity",
                (
                    "derive the borrow-lifetime receiver/return reconstruction "
                    "with exact lengths and unchanged suffix/outside frame"
                ),
                "check every literal active generated contract clause",
            ],
        },
        "boundary_scope": {
            "shared_observations": [
                "initial memory and outside-frame memory",
                "address, allocation extent, provenance, and root borrow",
                "element layout and usize/isize platform limits",
                "initial exclusivity and root-borrow liveness",
            ],
            "excluded_observations": [
                "length product, overflow branch, or option branch",
                "returned reference, range, identity, or projection",
                "final state or outside-frame result",
                "answer encoding or complete execution trace",
            ],
            "admitted_trust_site_ids": list(
                config.admitted_trust_site_ids
            ),
            "excluded_retained_trust_site_ids": list(
                config.excluded_trust_site_ids
            ),
            "context_only_trust_site_ids": list(
                config.context_only_trust_site_ids
            ),
            "all_audited_trust_site_ids": list(
                config.all_trust_site_ids
            ),
            "source_backed_replacement_ids": [config.replacement_id],
            "narrower_than_target": True,
        },
        "source_backed_replacements": [
            {
                "replacement_id": config.replacement_id,
                "operation": (
                    "canonical Rust 1.96 length/overflow, mutable-pointer "
                    "cast, raw-slice or array-reference construction, exact "
                    "range/root-borrow, singleton unsizing where applicable, "
                    "and relational borrow-lifetime frame transitions"
                ),
                "symbols": _source_transition_names(config, purpose),
                "source_citations": list(config.source_citations),
                "replaces_trust_site_ids": list(
                    config.excluded_trust_site_ids
                ),
            }
        ],
        "unresolved_source_model_trust_site_ids": [],
        "model_status": "complete",
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
        "declared_functions": [],
        "source_transition_definitions": _source_transition_names(
            config, purpose
        ),
        "source_semantics": [
            "LengthMultiplicationAndOverflowTransition",
            "BranchSelectionTransition",
            "MutablePointerExtractionAndCastTransition",
            "RawSliceOrArrayReferenceConstructionTransition",
            (
                "SingletonArrayToSliceUnsizeTransition"
                if config.kind == "singleton"
                else "MutableArrayOrSliceReturnTransition"
            ),
            *(
                ["BorrowLifetimeFinalFrameTransition"]
                if purpose == PRIMARY
                else []
            ),
            "ActiveGeneratedContractTransition",
        ],
        "principal_observations": _principal_observations(purpose),
        "equivalence_kind": "exact",
        "equivalence_review": {
            "principal_return": (
                "exact panic/option tag, values, range, address, allocation, "
                "provenance, root-borrow, layout, projection, and uniqueness"
            ),
            "final_state": (
                "not projected by exact-output obligation"
                if purpose == EXACT_OUTPUT
                else (
                    "exact receiver, returned-view, outside-memory, backing "
                    "identity, provenance, and frame equality"
                )
            ),
            "weakened_observations": [],
        },
    }


def obligation(
    config: MutableViewTarget,
    purpose: str,
) -> tuple[str, dict[str, Any]]:
    return obligation_text(config, purpose), obligation_metadata(config, purpose)


def validate_target_obligation(
    config: MutableViewTarget,
    text: str,
    metadata: dict[str, Any],
) -> None:
    purpose = metadata.get("obligation_purpose")
    if purpose not in PURPOSES:
        raise GuardError(f"{config.target}: invalid obligation purpose")
    if text != obligation_text(config, purpose):
        raise GuardError(f"{config.target}: reviewed SMT text changed")
    if metadata != obligation_metadata(config, purpose):
        raise GuardError(f"{config.target}: reviewed metadata changed")
    prohibited = (
        "(declare-fun",
        "b_output",
        "b_result",
        "b_return",
        "b_final",
        "b_trace",
        "b_product",
        "b_branch",
    )
    if any(token in text for token in prohibited):
        raise GuardError(f"{config.target}: answer-bearing or opaque model")
    required = (
        "LengthMultiplicationAndOverflowTransition",
        "BranchSelectionTransition",
        "MutablePointerExtractionAndCastTransition",
        "RawSliceOrArrayReferenceConstructionTransition",
        "ActiveGeneratedContractTransition",
        "TargetDefinition_T",
    )
    if any(token not in text for token in required):
        raise GuardError(f"{config.target}: source transition is incomplete")
    if config.kind == "singleton" and (
        "SingletonArrayToSliceUnsizeTransition" not in text
    ):
        raise GuardError(f"{config.target}: singleton unsizing is absent")
    if (
        purpose == PRIMARY
        and "BorrowLifetimeFinalFrameTransition" not in text
    ):
        raise GuardError(f"{config.target}: final frame is absent")
    if "ImmediateFinalFrameTransition" in text:
        raise GuardError(f"{config.target}: strengthened immediate frame remains")
    validate_obligation(text, metadata)


@dataclass(frozen=True)
class SourceCase:
    values: tuple[int, ...]
    container_length: int
    n: int
    address: int = 64
    allocation: int = 7
    provenance: int = 11
    root_borrow: int = 17
    allocation_base: int = 32
    allocation_bytes: int = 160
    element_size: int = 4
    element_alignment: int = 4
    usize_max: int = 255
    isize_max: int = 127
    alias_exclusive: bool = True
    borrow_alive: bool = True
    outside_frame: tuple[int, ...] = (90, 91)


def _values(length: int) -> tuple[int, ...]:
    return tuple(range(10, 10 + length))


def _zst(case: SourceCase, *, usize_max: int | None = None) -> SourceCase:
    return replace(
        case,
        address=8,
        allocation=0,
        provenance=0,
        allocation_base=0,
        allocation_bytes=0,
        element_size=0,
        element_alignment=8,
        usize_max=case.usize_max if usize_max is None else usize_max,
        isize_max=min(
            case.isize_max,
            case.usize_max if usize_max is None else usize_max,
        ),
    )


def source_cases(config: MutableViewTarget) -> dict[str, SourceCase]:
    if config.kind == "flatten":
        return {
            "empty_n0": SourceCase((), 0, 0),
            "empty_n_positive": SourceCase((), 0, 3),
            "nonempty_n0": SourceCase((), 3, 0),
            "nonzst_valid_unchecked_mul": SourceCase(_values(6), 3, 2),
            "zst_valid_checked_mul": _zst(
                SourceCase(_values(12), 3, 4)
            ),
            "zst_checked_mul_overflow": _zst(
                SourceCase(_values(16), 8, 2),
                usize_max=15,
            ),
        }
    if config.kind == "whole_array":
        return {
            "empty_n0": SourceCase((), 0, 0),
            "empty_n_positive": SourceCase((), 0, 1),
            "nonempty_n0": SourceCase(_values(3), 3, 0),
            "n_less_than_length": SourceCase(_values(3), 3, 2),
            "n_equal_length": SourceCase(_values(3), 3, 3),
            "n_greater_than_length": SourceCase(_values(3), 3, 4),
            "zst_n_equal_length": _zst(
                SourceCase(_values(3), 3, 3)
            ),
        }
    if config.kind == "prefix_array":
        return {
            "empty_n0": SourceCase((), 0, 0),
            "empty_n_positive": SourceCase((), 0, 1),
            "nonempty_n0": SourceCase(_values(3), 3, 0),
            "n_less_than_length": SourceCase(_values(3), 3, 2),
            "n_equal_length": SourceCase(_values(3), 3, 3),
            "n_greater_than_length": SourceCase(_values(3), 3, 4),
            "zst_n_less_than_length": _zst(
                SourceCase(_values(3), 3, 2)
            ),
        }
    return {
        "singleton_nonzst": SourceCase((10,), 1, 1),
        "singleton_zst": _zst(SourceCase((10,), 1, 1)),
    }


def evaluate_source(
    config: MutableViewTarget,
    case: SourceCase,
) -> dict[str, Any]:
    product = case.container_length * case.n
    panicked = (
        config.kind == "flatten"
        and case.element_size == 0
        and product > case.usize_max
    )
    if panicked:
        return {
            "kind": "panic",
            "length": 0,
            "values": (),
            "projection": 0,
        }
    if config.kind == "whole_array":
        success = case.container_length == case.n
    elif config.kind == "prefix_array":
        success = case.n <= case.container_length
    else:
        success = True
    if not success:
        return {
            "kind": "none",
            "length": 0,
            "values": (),
            "projection": 0,
        }
    length = (
        product
        if config.kind == "flatten"
        else case.n
        if config.kind in {"whole_array", "prefix_array"}
        else 1
    )
    values = (
        case.values[: case.n]
        if config.kind == "prefix_array"
        else case.values
    )
    return {
        "kind": "some",
        "length": length,
        "values": values,
        "projection": _projection(config),
    }


def _seq(values: tuple[int, ...]) -> str:
    if not values:
        return EMPTY_SEQ
    terms = [f"(seq.unit {value})" for value in values]
    while len(terms) > 1:
        terms = [f"(seq.++ {terms[0]} {terms[1]})", *terms[2:]]
    return terms[0]


def _bool(value: bool) -> str:
    return str(value).lower()


def _input_expression(case: SourceCase) -> str:
    values: tuple[Any, ...] = (
        _seq(case.values),
        case.container_length,
        case.n,
        case.address,
        case.allocation,
        case.provenance,
        case.root_borrow,
        case.allocation_base,
        case.allocation_bytes,
        case.element_size,
        case.element_alignment,
        case.usize_max,
        case.isize_max,
        _bool(case.alias_exclusive),
        _bool(case.borrow_alive),
        _seq(case.outside_frame),
    )
    return "(mkInput " + " ".join(map(str, values)) + ")"


def _boundary_expression(
    case: SourceCase,
    *,
    memory_mismatch: bool = False,
) -> str:
    initial = (
        case.values + (999,)
        if memory_mismatch
        else case.values
    )
    values: tuple[Any, ...] = (
        _seq(initial),
        case.address,
        case.allocation,
        case.provenance,
        case.root_borrow,
        case.allocation_base,
        case.allocation_bytes,
        case.element_size,
        case.element_alignment,
        case.usize_max,
        case.isize_max,
        _bool(case.alias_exclusive),
        _bool(case.borrow_alive),
        _seq(case.outside_frame),
    )
    return "(mkBoundary " + " ".join(map(str, values)) + ")"


def _model_query(purpose: str) -> str:
    terms = [
        *(f"({selector} y1)" for selector, _ in OUTPUT_FIELDS),
        *(
            (f"({selector} s1)" for selector, _ in STATE_FIELDS)
            if purpose == PRIMARY
            else ()
        ),
    ]
    return "(get-value (\n  %s))" % "\n  ".join(terms)


def source_instance_text(
    config: MutableViewTarget,
    name: str,
) -> str:
    try:
        case = source_cases(config)[name]
    except KeyError as exc:
        raise ValueError(f"{config.target}: unknown source case {name}") from exc
    expected = evaluate_source(config, case)
    expected_kind = expected["kind"]
    expected_panicked = expected_kind == "panic"
    expected_some = expected_kind == "some"
    assertions = [
        f"(assert (= x {_input_expression(case)}))",
        f"(assert (= b {_boundary_expression(case)}))",
        "(assert (Requires_T x))",
        "(assert (Boundary_T x b))",
        "(assert (Spec_T x b y1 s1))",
        f"(assert (= (y_panicked y1) {_bool(expected_panicked)}))",
        f"(assert (= (y_is_some y1) {_bool(expected_some)}))",
        f"(assert (= (y_values y1) {_seq(expected['values'])}))",
        f"(assert (= (y_length y1) {expected['length']}))",
        f"(assert (= (y_projection y1) {expected['projection']}))",
    ]
    return (
        model_text(config, PRIMARY)
        + "\n"
        + "\n".join(assertions)
        + "\n(check-sat)\n"
        + _model_query(PRIMARY)
        + "\n"
    )


WITNESS_CASES = {
    "flatten": "nonzst_valid_unchecked_mul",
    "whole_array": "n_equal_length",
    "prefix_array": "n_less_than_length",
    "singleton": "singleton_nonzst",
}


def full_state_witness_case(
    config: MutableViewTarget,
) -> tuple[str, SourceCase]:
    name = WITNESS_CASES[config.kind]
    return name, source_cases(config)[name]


def _changed_first(values: tuple[int, ...]) -> tuple[int, ...]:
    if not values:
        raise ValueError("full-state witness requires a nonempty return")
    return (99, *values[1:])


def _witness_input_final(
    config: MutableViewTarget,
    case: SourceCase,
    return_final: tuple[int, ...],
) -> tuple[int, ...]:
    if config.kind == "prefix_array":
        return return_final + case.values[case.n :]
    return return_final


def witness_payload(config: MutableViewTarget) -> dict[str, Any]:
    case_name, case = full_state_witness_case(config)
    initial_return = tuple(evaluate_source(config, case)["values"])
    changed_return = _changed_first(initial_return)
    initial_input = _witness_input_final(config, case, initial_return)
    changed_input = _witness_input_final(config, case, changed_return)
    return {
        "schema_version": 1,
        "target": config.target,
        "input_order": config.input_order,
        "active_contract_sha256": config.active_contract_sha256,
        "source_case": case_name,
        "shared_input": {
            field: list(value) if isinstance(value, tuple) else value
            for field, value in vars(case).items()
        },
        "shared_boundary": {
            "initial_memory": list(case.values),
            "outside_frame": list(case.outside_frame),
            "address": case.address,
            "allocation": case.allocation,
            "provenance": case.provenance,
            "root_borrow": case.root_borrow,
            "same_for_both_executions": True,
        },
        "execution1": {
            "initial_output_values": list(initial_return),
            "return_final": list(initial_return),
            "input_final": list(initial_input),
        },
        "execution2": {
            "initial_output_values": list(initial_return),
            "return_final": list(changed_return),
            "input_final": list(changed_input),
        },
        "enforced_frame": {
            "return_final_length": len(initial_return),
            "receiver_return_reconstruction": (
                "returned prefix plus unchanged old suffix"
                if config.kind == "prefix_array"
                else "receiver final equals returned final"
            ),
            "backing_identity": (
                "same address/allocation/provenance/root borrow"
            ),
            "outside_frame_unchanged": True,
        },
        "expected": {
            "both_executions_satisfy_every_active_conjunct": True,
            "exact_output_equal": True,
            "full_state_equal": False,
            "full_exact_equivalent": False,
        },
    }


def fixed_full_state_witness_text(config: MutableViewTarget) -> str:
    _, case = full_state_witness_case(config)
    initial_return = tuple(evaluate_source(config, case)["values"])
    changed_return = _changed_first(initial_return)
    initial_input = _witness_input_final(config, case, initial_return)
    changed_input = _witness_input_final(config, case, changed_return)
    return model_text(config, PRIMARY) + f"""\
(assert (= x {_input_expression(case)}))
(assert (= b {_boundary_expression(case)}))
(assert (Requires_T x))
(assert (Boundary_T x b))
(assert (Spec_T x b y1 s1))
(assert (Spec_T x b y2 s2))
(assert (= (s_return_final s1) {_seq(initial_return)}))
(assert (= (s_return_final s2) {_seq(changed_return)}))
(assert (= (s_input_final s1) {_seq(initial_input)}))
(assert (= (s_input_final s2) {_seq(changed_input)}))
(assert (not (Equivalent_T x b y1 s1 y2 s2)))
(check-sat)
(get-value (
  (y_values y1)
  (y_values y2)
  (y_length y1)
  (y_address y1)
  (y_allocation y1)
  (y_provenance y1)
  (y_root_borrow y1)
  (s_return_final s1)
  (s_return_final s2)
  (s_input_final s1)
  (s_input_final s2)
  (s_outside_final s1)
  (s_outside_final s2)
  (s_backing_address s1)
  (s_backing_allocation s1)
  (s_backing_provenance s1)
  (s_backing_root_borrow s1)
  (Equivalent_T x b y1 s1 y2 s2)))
"""


INVALID_PROBES = (
    "invalid_null",
    "invalid_misaligned",
    "invalid_allocation",
    "invalid_provenance",
    "invalid_alias_permission",
    "invalid_root_borrow",
    "invalid_allocation_range",
    "invalid_platform_limit",
    "boundary_memory_mismatch",
)
COMMON_SEMANTIC_PROBES = (
    "wrong_branch",
    "wrong_range",
    "wrong_address",
    "wrong_allocation_identity",
    "wrong_provenance",
    "wrong_borrow_identity",
    "wrong_return_values",
    "wrong_final_frame",
    "wrong_outside_frame",
    "answer_laundered_length",
)


def negative_probe_names(
    config: MutableViewTarget,
) -> tuple[str, ...]:
    extras: tuple[str, ...]
    if config.kind == "flatten":
        extras = (
            "wrong_overflow_panic",
            "wrong_valid_unchecked_multiplication",
            "invalid_non_zst_overflow",
        )
    elif config.kind == "singleton":
        extras = ("wrong_singleton_unsizing",)
    else:
        extras = ("wrong_array_projection",)
    return INVALID_PROBES + COMMON_SEMANTIC_PROBES + extras


def _invalid_case(
    config: MutableViewTarget,
    name: str,
) -> tuple[SourceCase, bool]:
    case = next(
        item
        for item in source_cases(config).values()
        if evaluate_source(config, item)["kind"] == "some"
        and item.element_size > 0
        and evaluate_source(config, item)["length"] > 0
    )
    mismatch = False
    if name == "invalid_null":
        case = replace(case, address=0)
    elif name == "invalid_misaligned":
        case = replace(case, address=case.address + 1)
    elif name == "invalid_allocation":
        case = replace(case, allocation=0)
    elif name == "invalid_provenance":
        case = replace(case, provenance=0)
    elif name == "invalid_alias_permission":
        case = replace(case, alias_exclusive=False)
    elif name == "invalid_root_borrow":
        case = replace(case, root_borrow=0, borrow_alive=False)
    elif name == "invalid_allocation_range":
        case = replace(
            case,
            allocation_base=case.address,
            allocation_bytes=1,
        )
    elif name == "invalid_platform_limit":
        case = replace(case, usize_max=63, isize_max=31)
    elif name == "boundary_memory_mismatch":
        mismatch = True
    elif name == "invalid_non_zst_overflow":
        case = SourceCase(
            _values(8),
            4,
            2,
            address=4,
            allocation_base=0,
            allocation_bytes=7,
            usize_max=7,
            isize_max=7,
        )
    else:
        raise ValueError(f"{config.target}: unknown invalid probe {name}")
    return case, mismatch


def negative_probe_text(
    config: MutableViewTarget,
    name: str,
) -> str:
    if name not in negative_probe_names(config):
        raise ValueError(f"{config.target}: unknown negative probe {name}")
    if name in INVALID_PROBES or name == "invalid_non_zst_overflow":
        case, mismatch = _invalid_case(config, name)
        contradiction = None
    elif name == "wrong_overflow_panic":
        case = source_cases(config)["zst_checked_mul_overflow"]
        mismatch = False
        contradiction = "(not (y_panicked y1))"
    else:
        case = next(
            item
            for item in source_cases(config).values()
            if evaluate_source(config, item)["kind"] == "some"
            and evaluate_source(config, item)["length"] > 0
        )
        mismatch = False
        expected = evaluate_source(config, case)
        reconstructed = _reconstructed_input(
            config,
            "(s_return_final s1)",
        )
        contradictions = {
            "wrong_branch": "(not (y_is_some y1))",
            "wrong_range": (
                f"(or (distinct (y_start y1) 0) "
                f"(distinct (y_length y1) {expected['length']}))"
            ),
            "wrong_address": (
                "(distinct (y_address y1) (x_address x))"
            ),
            "wrong_allocation_identity": (
                "(distinct (y_allocation y1) (x_allocation x))"
            ),
            "wrong_provenance": (
                "(distinct (y_provenance y1) (x_provenance x))"
            ),
            "wrong_borrow_identity": (
                "(distinct (y_root_borrow y1) (x_root_borrow x))"
            ),
            "wrong_return_values": (
                f"(distinct (y_values y1) {_seq(expected['values'])})"
            ),
            "wrong_final_frame": (
                "(or "
                "(distinct (seq.len (s_return_final s1)) (y_length y1)) "
                "(distinct (s_input_final s1) "
                f"{reconstructed}) "
                "(distinct (s_backing_address s1) (x_address x)) "
                "(distinct (s_backing_allocation s1) (x_allocation x)) "
                "(distinct (s_backing_provenance s1) (x_provenance x)) "
                "(distinct (s_backing_root_borrow s1) (x_root_borrow x)) "
                "(not (s_frame_unchanged s1)) "
                f"(distinct (s_panic_before_borrow s1) {_panics(config)}))"
            ),
            "wrong_outside_frame": (
                "(distinct (s_outside_final s1) (x_outside_frame x))"
            ),
            "answer_laundered_length": (
                "(= (y_length y1) (b_usize_max b))"
            ),
            "wrong_valid_unchecked_multiplication": (
                f"(distinct (y_length y1) {_product()})"
            ),
            "wrong_singleton_unsizing": (
                "(or (distinct (y_length y1) 1) "
                "(distinct (y_projection y1) 3))"
            ),
            "wrong_array_projection": (
                "(distinct (y_projection y1) 2)"
            ),
        }
        contradiction = contradictions[name]
    assertions = [
        f"(assert (= x {_input_expression(case)}))",
        f"(assert (= b {_boundary_expression(case, memory_mismatch=mismatch)}))",
        "(assert (Requires_T x))",
        "(assert (Boundary_T x b))",
        "(assert (Spec_T x b y1 s1))",
    ]
    if contradiction:
        assertions.append(f"(assert {contradiction})")
    return (
        model_text(config, PRIMARY)
        + "\n"
        + "\n".join(assertions)
        + "\n(check-sat)\n"
    )


def boundary_manifest(config: MutableViewTarget) -> dict[str, Any]:
    return {
        "schema_version": 2,
        "target": config.target,
        "input_order": config.input_order,
        "active_contract_sha256": config.active_contract_sha256,
        "boundary_narrower_than_target": True,
        "proof_boundary_assumption": (
            "Both executions share one valid x and one b containing only "
            "initial memory, address/allocation/provenance, root-borrow "
            "liveness and exclusivity, element layout, platform limits, and "
            "outside-frame memory. Every branch, returned identity/range, "
            "projection, and borrow-lifetime frame constraint is derived "
            "after Boundary_T."
        ),
        "shared_boundary_observations": [
            {
                "fields": ["b_initial_memory", "b_outside_frame"],
                "kind": "initial memory and outside frame",
            },
            {
                "fields": [
                    "b_address",
                    "b_allocation",
                    "b_provenance",
                    "b_root_borrow",
                    "b_allocation_base",
                    "b_allocation_bytes",
                    "b_alias_exclusive",
                    "b_borrow_alive",
                ],
                "kind": "initial reference representation and borrow",
            },
            {
                "fields": [
                    "b_element_size",
                    "b_element_alignment",
                    "b_usize_max",
                    "b_isize_max",
                ],
                "kind": "layout and platform",
            },
        ],
        "source_backed_replacements": obligation_metadata(
            config, PRIMARY
        )["source_backed_replacements"],
        "admitted_trust_site_ids": list(config.admitted_trust_site_ids),
        "context_only_trust_site_ids": list(
            config.context_only_trust_site_ids
        ),
        "excluded_retained_trust_site_ids": list(
            config.excluded_trust_site_ids
        ),
        "all_audited_trust_site_ids": list(config.all_trust_site_ids),
        "excluded_from_boundary": [
            "checked or unchecked length result and overflow branch",
            "option discriminant",
            "returned values, range, pointer identity, or borrow",
            "array/slice projection and singleton unsizing result",
            "input, returned-view, or outside-memory final state",
            "answer encodings and full execution traces",
        ],
    }


def verus_text(config: MutableViewTarget) -> str:
    function = config.function_name
    kind = config.kind
    panic_expression = (
        "input.element_size == 0\n"
        "        && input.container_length * input.n > input.usize_max"
        if kind == "flatten"
        else "false"
    )
    success_expression = (
        "!panics(input)"
        if kind == "flatten"
        else "input.container_length == input.n"
        if kind == "whole_array"
        else "input.n <= input.container_length"
        if kind == "prefix_array"
        else "true"
    )
    length_expression = (
        "input.container_length * input.n"
        if kind == "flatten"
        else "input.n"
        if kind in {"whole_array", "prefix_array"}
        else "1"
    )
    values_expression = (
        "input.source.subrange(0, input.n as int)"
        if kind == "prefix_array"
        else "input.source"
    )
    final_input_expression = (
        "return_final\n"
        "                + input.source.subrange(\n"
        "                    input.n as int,\n"
        "                    input.container_length as int,\n"
        "                )"
        if kind == "prefix_array"
        else "return_final"
    )
    projection = _projection(config)
    if kind == "flatten":
        active = """\
    if !panics(input) {
        output.values == input.source
            && state.input_final == state.return_final
    } else {
        output.panicked
    }"""
    elif kind == "whole_array":
        active = """\
    if input.container_length == input.n {
        output.is_some
            && output.values == input.source
            && state.input_final == state.return_final
    } else {
        !output.is_some && state.input_final == input.source
    }"""
    elif kind == "prefix_array":
        active = """\
    if input.n <= input.container_length {
        output.is_some
            && output.values == input.source.subrange(0, input.n as int)
            && state.input_final
                == state.return_final
                    + input.source.subrange(
                        input.n as int,
                        input.container_length as int,
                    )
    } else {
        !output.is_some && state.input_final == input.source
    }"""
    else:
        active = """\
    output.is_some
        && output.values == input.source
        && output.length == 1
        && state.return_final == state.input_final"""
    return f"""\
#![allow(dead_code, unused_imports, unused_variables)]
// Trusted-free source transition for {config.target}.

use vstd::prelude::*;
use vstd::seq::*;

verus! {{

pub ghost struct Input {{
    pub source: Seq<int>,
    pub container_length: nat,
    pub n: nat,
    pub address: int,
    pub allocation: int,
    pub provenance: int,
    pub root_borrow: int,
    pub element_size: nat,
    pub element_alignment: nat,
    pub usize_max: nat,
    pub outside_frame: Seq<int>,
}}

pub ghost struct Boundary {{
    pub initial_memory: Seq<int>,
    pub address: int,
    pub allocation: int,
    pub provenance: int,
    pub root_borrow: int,
    pub element_size: nat,
    pub element_alignment: nat,
    pub usize_max: nat,
    pub outside_frame: Seq<int>,
}}

pub ghost struct PointerIdentity {{
    pub address: int,
    pub allocation: int,
    pub provenance: int,
    pub root_borrow: int,
}}

pub ghost struct Output {{
    pub panicked: bool,
    pub is_some: bool,
    pub values: Seq<int>,
    pub start: int,
    pub length: nat,
    pub pointer: PointerIdentity,
    pub element_size: nat,
    pub element_alignment: nat,
    pub projection: nat,
    pub unique: bool,
}}

pub ghost struct FinalState {{
    pub input_final: Seq<int>,
    pub return_final: Seq<int>,
    pub outside_final: Seq<int>,
    pub pointer: PointerIdentity,
    pub frame_unchanged: bool,
    pub panic_before_borrow: bool,
}}

pub open spec fn empty_pointer() -> PointerIdentity {{
    PointerIdentity {{
        address: 0,
        allocation: 0,
        provenance: 0,
        root_borrow: 0,
    }}
}}

pub open spec fn checked_length_multiplication(
    input: Input,
) -> (bool, nat) {{
    if panics(input) {{
        (true, 0)
    }} else {{
        (false, {length_expression})
    }}
}}

pub open spec fn panics(input: Input) -> bool {{
    {panic_expression}
}}

pub open spec fn branch_succeeds(input: Input) -> bool {{
    {success_expression}
}}

pub open spec fn mutable_pointer_extraction(
    input: Input,
) -> PointerIdentity {{
    PointerIdentity {{
        address: input.address,
        allocation: input.allocation,
        provenance: input.provenance,
        root_borrow: input.root_borrow,
    }}
}}

pub open spec fn pointer_cast(
    pointer: PointerIdentity,
) -> PointerIdentity {{
    pointer
}}

pub open spec fn raw_slice_or_array_reference(
    input: Input,
    pointer: PointerIdentity,
) -> Output {{
    Output {{
        panicked: false,
        is_some: true,
        values: {values_expression},
        start: 0,
        length: {length_expression},
        pointer,
        element_size: input.element_size,
        element_alignment: input.element_alignment,
        projection: {projection},
        unique: true,
    }}
}}

pub open spec fn singleton_array_unsize(output: Output) -> Output {{
    output
}}

pub open spec fn source_output(input: Input) -> Output {{
    if branch_succeeds(input) {{
        let multiplication = checked_length_multiplication(input);
        let pointer = pointer_cast(mutable_pointer_extraction(input));
        singleton_array_unsize(raw_slice_or_array_reference(input, pointer))
    }} else {{
        Output {{
            panicked: panics(input),
            is_some: false,
            values: Seq::empty(),
            start: 0,
            length: 0,
            pointer: empty_pointer(),
            element_size: 0,
            element_alignment: 0,
            projection: 0,
            unique: false,
        }}
    }}
}}

pub open spec fn borrow_lifetime_state(
    input: Input,
    return_final: Seq<int>,
) -> FinalState {{
    FinalState {{
        input_final:
            if branch_succeeds(input) {{
                {final_input_expression}
            }} else {{
                input.source
            }},
        return_final:
            if branch_succeeds(input) {{ return_final }}
            else {{ Seq::empty() }},
        outside_final: input.outside_frame,
        pointer: mutable_pointer_extraction(input),
        frame_unchanged: true,
        panic_before_borrow: panics(input),
    }}
}}

pub open spec fn borrow_lifetime_final_frame(
    input: Input,
    state: FinalState,
) -> bool {{
    state.return_final.len()
        == if branch_succeeds(input) {{
            ({length_expression}) as int
        }} else {{
            0
        }}
        && state == borrow_lifetime_state(input, state.return_final)
}}

pub open spec fn boundary_holds(
    input: Input,
    boundary: Boundary,
) -> bool {{
    boundary.initial_memory == input.source
        && boundary.address == input.address
        && boundary.allocation == input.allocation
        && boundary.provenance == input.provenance
        && boundary.root_borrow == input.root_borrow
        && boundary.element_size == input.element_size
        && boundary.element_alignment == input.element_alignment
        && boundary.usize_max == input.usize_max
        && boundary.outside_frame == input.outside_frame
}}

pub open spec fn active_generated_contract(
    input: Input,
    output: Output,
    state: FinalState,
) -> bool {{
{active}
}}

pub open spec fn target_transition(
    input: Input,
    boundary: Boundary,
    output: Output,
    state: FinalState,
) -> bool {{
    boundary_holds(input, boundary)
        && output == source_output(input)
        && borrow_lifetime_final_frame(input, state)
        && active_generated_contract(input, output, state)
}}

pub open spec fn same_pointer(
    left: PointerIdentity,
    right: PointerIdentity,
) -> bool {{
    left.address == right.address
        && left.allocation == right.allocation
        && left.provenance == right.provenance
        && left.root_borrow == right.root_borrow
}}

pub open spec fn same_output(left: Output, right: Output) -> bool {{
    left.panicked == right.panicked
        && left.is_some == right.is_some
        && left.values == right.values
        && left.start == right.start
        && left.length == right.length
        && same_pointer(left.pointer, right.pointer)
        && left.element_size == right.element_size
        && left.element_alignment == right.element_alignment
        && left.projection == right.projection
        && left.unique == right.unique
}}

pub open spec fn same_state(
    left: FinalState,
    right: FinalState,
) -> bool {{
    left.input_final == right.input_final
        && left.return_final == right.return_final
        && left.outside_final == right.outside_final
        && same_pointer(left.pointer, right.pointer)
        && left.frame_unchanged == right.frame_unchanged
        && left.panic_before_borrow == right.panic_before_borrow
}}

pub proof fn exact_output_conditional_complete_{function}(
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
    reveal(same_pointer);
}}

pub proof fn full_state_conditional_incomplete_{function}(
    input: Input,
    boundary: Boundary,
    first: Seq<int>,
    second: Seq<int>,
)
    requires
        boundary_holds(input, boundary),
        branch_succeeds(input),
        first.len() == ({length_expression}) as int,
        second.len() == ({length_expression}) as int,
        first != second,
    ensures
        target_transition(
            input,
            boundary,
            source_output(input),
            borrow_lifetime_state(input, first),
        ),
        target_transition(
            input,
            boundary,
            source_output(input),
            borrow_lifetime_state(input, second),
        ),
        !same_state(
            borrow_lifetime_state(input, first),
            borrow_lifetime_state(input, second),
        ),
{{
    reveal(target_transition);
    reveal(borrow_lifetime_final_frame);
    reveal(borrow_lifetime_state);
    reveal(active_generated_contract);
    reveal(source_output);
    reveal(branch_succeeds);
    reveal(panics);
    reveal(same_state);
    reveal(same_pointer);
}}

}} // verus!
"""
