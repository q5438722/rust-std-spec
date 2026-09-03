#!/usr/bin/env python3
"""Source-backed conditional-completeness obligations for align_to{,_mut}."""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass, replace
from typing import Any

from checker_guards import GuardError, validate_obligation


PRIMARY = "completeness-modulo-reviewed-equivalence"
EXACT_OUTPUT = "exact-output-determinism"
PURPOSES = (PRIMARY, EXACT_OUTPUT)

SLICE_SOURCE_PATH = "core/src/slice/mod.rs"
SLICE_SOURCE_SHA256 = (
    "58901fa6437dbd4d77c68427bbced0fc3a91a10fdb8bd2e233adf6a9ba27d2d5"
)
PTR_SOURCE_PATH = "core/src/ptr/mod.rs"
PTR_SOURCE_SHA256 = (
    "1fd4ecb1650cfc995f29a172ad3f72ffa378702ea55493eabf6a80355b38035e"
)
PTR_DOCS_PATH = "core/src/ptr/const_ptr.rs"
PTR_DOCS_SHA256 = (
    "c73503de1e8cba8cc409ccd56fba77a6ecd43ddede9591deedb061fba1491f11"
)
PTR_SOURCE_RANGE = (2190, 2374)
PTR_DOCS_RANGE = (1257, 1310)
VOCABULARY_RANGES = ((1051, 1096),)
VERUS_EXPECTED_SUMMARY = "verification results:: 6 verified, 0 errors"

BRANCH_ZST = 0
BRANCH_OFFSET_FALLBACK = 1
BRANCH_ALIGNED = 2
EMPTY_SEQ = "(as seq.empty (Seq Int))"


@dataclass(frozen=True)
class AlignTarget:
    target: str
    input_order: str
    artifact_id: str
    mutable: bool
    active_contract_sha256: str
    active_contract_text: str
    generated_declaration_sha256: str
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
    admitted_trust_site_ids: tuple[str, ...]
    excluded_trust_site_ids: tuple[str, ...]

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
    def expected_solver_results(self) -> dict[str, str]:
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

    @property
    def replacement_id(self) -> str:
        return f"SRC-{int(self.input_order):03d}-ALIGN-TO-SOURCE-TRANSITIONS"


TARGETS = (
    AlignTarget(
        target="core::slice::align_to",
        input_order="8",
        artifact_id="008_core_slice_align_to",
        mutable=False,
        active_contract_sha256=(
            "ecdec7dc102f8a00f610ae369191cf306fabe2a435b651d7cc69d2775d75e321"
        ),
        active_contract_text=(
            "pub assume_specification<T, U>[ <[T]>::align_to::<U> ]( "
            "slice: &[T], ) -> (ret: (&[T], &[U], &[T])) requires "
            "slice_align_to_domain::<T, U>(slice@), ensures "
            "slice_align_to_result::<T, U>(slice@, ret.0@, ret.1@, "
            "ret.2@), ;"
        ),
        generated_declaration_sha256=(
            "a18a1f81c64ecab30a7f332372dc68f21f4c6350636ba8f7845c7bbcefa12069"
        ),
        source_start=4499,
        source_end=4532,
        source_item_sha256=(
            "38394f129cf389381904f8fea0ae93d1d1059f79b4a8505a540992907e485706"
        ),
        docs_start=4469,
        docs_end=4496,
        public_docs_sha256=(
            "5449c5d4d86040933c1064183eba9a9cc3dfceb49334739afaca790e0eb79a0d"
        ),
        harness_sha256=(
            "059ff7a8fd6b7ee2c1167e9ce34dd245447273c8d6a1afe87d1ded981df64162"
        ),
        source_body_manifest_sha256=(
            "dbbdd57c88e28e940b2622120777f2f294c7cad57320b1b3937186aac5411676"
        ),
        transformation_manifest_sha256=(
            "e0a6210b244b72ef4199cb02dfe4b0924630727e661d376149e84e50dd89c51e"
        ),
        dependency_manifest_sha256=(
            "bbbb4df5e8d2e9dc13f9cc75066b46581b615584afa4bfc965120788b67cda2e"
        ),
        trust_record_sha256=(
            ("TS-008-D001", "3a438de1c20b15f7f22a80d9dc72716d8a3f2047368d9358ae55162e3167779a"),
            ("TS-008-D002", "5d3fb4ad6c69358ae220b9a8f02b1b5c677ee41a8192971b7c9aee48d4377faa"),
            ("TS-008-D003", "6f1b865f4a578dfde8e4b3d989cf7b3bac7125c1f4c3ab2b871ad5f866f51576"),
            ("TS-008-D004", "285eae8b4c209fdbc5a2acea787c66e5ffc30e84a3bec15c43a15fdd4c368da0"),
            ("TS-008-C001", "7e17fbd4f5a967bfc1d48509ec13e182219000ade200713e93ac1fc44bfb5344"),
            ("TS-008-E001", "bcb13da304fb426891a9507fc2677b0b274950156b5cad6f2faed44723ca352f"),
            ("TS-008-E002", "3872630fcee6f7fb66e87be379a80fcaf17d91d4d8a288ce7bb35b7a393a1029"),
            ("TS-008-E003", "46ff040b28311f3299281c4b89f1ddc02088acd2e6495e47789dacba974c59c6"),
            ("TS-008-E004", "959579ea2bd2b0799b2ffc7dd3f17b87562f0904eb986502592b61a74d297545"),
            ("TS-008-E005", "983f0fecae7503971735f67ac3bde00dd8f1762bb77732ede29548f2750ae5b8"),
            ("TS-008-E006", "e7dd3be72c9be210018c0f31d308f4850bca615de6bd439b35dd91ce21d5c24c"),
        ),
        context_only_trust_site_ids=("TS-008-D001", "TS-008-C001"),
        admitted_trust_site_ids=(
            "TS-008-D002",
            "TS-008-D003",
            "TS-008-E001",
            "TS-008-E002",
            "TS-008-E003",
            "TS-008-E004",
        ),
        excluded_trust_site_ids=(
            "TS-008-D004",
            "TS-008-E005",
            "TS-008-E006",
        ),
    ),
    AlignTarget(
        target="core::slice::align_to_mut",
        input_order="9",
        artifact_id="009_core_slice_align_to_mut",
        mutable=True,
        active_contract_sha256=(
            "d3f3080fe88dd4be74e095f3d06df2b686c52dd000e8bba962feaa71695cd330"
        ),
        active_contract_text=(
            "pub assume_specification<T, U>[ <[T]>::align_to_mut::<U> ]( "
            "slice: &mut [T], ) -> (ret: (&mut [T], &mut [U], &mut "
            "[T])) requires slice_align_to_domain::<T, U>(old(slice)@), "
            "ensures slice_align_to_mut_result::<T, U>( old(slice)@, "
            "ret.0@, ret.1@, ret.2@, final(ret.0)@, final(ret.1)@, "
            "final(ret.2)@, final(slice)@, ), ;"
        ),
        generated_declaration_sha256=(
            "544155c98fb4c6154eb41466dbd23924202ab1d72c14261a778a88a5ed47d771"
        ),
        source_start=4564,
        source_end=4605,
        source_item_sha256=(
            "79bc07c28c34e853de5c1bbc49ebb8f27b4e8837109fc51c6a15eef97565ec27"
        ),
        docs_start=4534,
        docs_end=4561,
        public_docs_sha256=(
            "c17a8e1c3a33f3c6c8105c9df7e7a2e3221b44c818b14ee2debe35958974b234"
        ),
        harness_sha256=(
            "27f0152fe8fbc5f0ddee8324f6ce96dd547673f2b229e095a57d191fa2dedb43"
        ),
        source_body_manifest_sha256=(
            "f7d8bcba4dccc6a5eca616f0a0a15f6d476e6460150e503e2df180c3087fba2d"
        ),
        transformation_manifest_sha256=(
            "cec4cf204fa42d4fc154edf21b41b97d709e9e55bd7a047c917e4fd80a75d229"
        ),
        dependency_manifest_sha256=(
            "8bd80759ceec3be97eefa5f2f15742016fc83faac0d893621bfad79fb1e775ed"
        ),
        trust_record_sha256=(
            ("TS-009-D001", "dd8226f3eb4f760fd4d0f9c0af0a88a57210edef9b91f453c1fbd88e41042cca"),
            ("TS-009-D002", "855ab60ef9cbb0bc683de45f5c34f8d4da53ee10ac6c0d2c88c29d7913e22cfd"),
            ("TS-009-D003", "efe7c6c6672d3d2cd4d1404006750a9e074bcde4ce16e89d2574824dcbbb8693"),
            ("TS-009-D004", "b0f37b9657967129be4eb8003cc7d0a54d3c4f1d8649db4bf3fa6e32c16cce53"),
            ("TS-009-C001", "7a69996b28090b568e736e33e9b171b1c3ce2269f83d4530bcd3719acb7cac4e"),
            ("TS-009-E001", "e512546313e1dffdf4bd6d4d7591e6b1c9d26f732f19d2547549969ec2a491f7"),
            ("TS-009-E002", "525ff5329e1e9664760391b37cafb248277caeb18d9c0cf5d23029762aa125b6"),
            ("TS-009-E003", "35375abfeec47050f4de421f65b3dea181b34c953894bb7c3f2ffbdad38d0c1f"),
            ("TS-009-E004", "912702020b44cfe8c7475ead74066c5876185a5e2a497fe11dbfd4dd0d3d24b9"),
        ),
        context_only_trust_site_ids=("TS-009-D001", "TS-009-C001"),
        admitted_trust_site_ids=(
            "TS-009-D002",
            "TS-009-D003",
            "TS-009-E001",
            "TS-009-E002",
        ),
        excluded_trust_site_ids=(
            "TS-009-D004",
            "TS-009-E003",
            "TS-009-E004",
        ),
    ),
)

TARGET_BY_ARTIFACT = {config.artifact_id: config for config in TARGETS}
TARGET_KEYS = tuple((config.target, config.input_order) for config in TARGETS)


INPUT_FIELDS = (
    ("x_source", "(Seq Int)"),
    ("x_length", "Int"),
    ("x_address", "Int"),
    ("x_allocation", "Int"),
    ("x_provenance", "Int"),
    ("x_root_borrow", "Int"),
    ("x_allocation_base", "Int"),
    ("x_allocation_bytes", "Int"),
    ("x_t_size", "Int"),
    ("x_t_alignment", "Int"),
    ("x_u_size", "Int"),
    ("x_u_alignment", "Int"),
    ("x_usize_max", "Int"),
    ("x_isize_max", "Int"),
    ("x_transmute_valid", "Bool"),
    ("x_alias_exclusive", "Bool"),
    ("x_borrow_alive", "Bool"),
    ("x_outside_frame", "(Seq Int)"),
)

BOUNDARY_FIELDS = (
    ("b_memory", "(Array Int Int)", "input_memory"),
    ("b_initialized", "(Array Int Bool)", "input_memory"),
    ("b_input_length", "Int", "input_memory"),
    ("b_address", "Int", "input_provenance"),
    ("b_allocation", "Int", "input_provenance"),
    ("b_provenance", "Int", "input_provenance"),
    ("b_root_borrow", "Int", "input_provenance"),
    ("b_allocation_base", "Int", "input_provenance"),
    ("b_allocation_bytes", "Int", "input_provenance"),
    ("b_t_size", "Int", "input_layout"),
    ("b_t_alignment", "Int", "input_layout"),
    ("b_u_size", "Int", "input_layout"),
    ("b_u_alignment", "Int", "input_layout"),
    ("b_usize_max", "Int", "input_layout"),
    ("b_isize_max", "Int", "input_layout"),
    ("b_transmute_valid", "Bool", "input_layout"),
    ("b_alias_exclusive", "Bool", "input_provenance"),
    ("b_borrow_alive", "Bool", "input_provenance"),
    ("b_outside_frame", "(Seq Int)", "input_memory"),
)

OUTPUT_FIELDS = (
    ("y_branch", "Int"),
    ("y_alignment_offset", "Int"),
    ("y_prefix_values", "(Seq Int)"),
    ("y_middle_values", "(Seq Int)"),
    ("y_suffix_values", "(Seq Int)"),
    ("y_prefix_length", "Int"),
    ("y_middle_length", "Int"),
    ("y_suffix_length", "Int"),
    ("y_prefix_address", "Int"),
    ("y_middle_address", "Int"),
    ("y_suffix_address", "Int"),
    ("y_prefix_allocation", "Int"),
    ("y_middle_allocation", "Int"),
    ("y_suffix_allocation", "Int"),
    ("y_prefix_provenance", "Int"),
    ("y_middle_provenance", "Int"),
    ("y_suffix_provenance", "Int"),
    ("y_prefix_borrow", "Int"),
    ("y_middle_borrow", "Int"),
    ("y_suffix_borrow", "Int"),
    ("y_mutable", "Bool"),
    ("y_disjoint", "Bool"),
)

STATE_FIELDS = (
    ("s_final_bytes", "(Seq Int)"),
    ("s_final_source", "(Seq Int)"),
    ("s_final_prefix", "(Seq Int)"),
    ("s_final_middle", "(Seq Int)"),
    ("s_final_suffix", "(Seq Int)"),
    ("s_outside_final", "(Seq Int)"),
    ("s_allocation", "Int"),
    ("s_address", "Int"),
    ("s_provenance", "Int"),
    ("s_root_borrow", "Int"),
    ("s_alias_exclusive", "Bool"),
    ("s_frame_unchanged", "Bool"),
    ("s_partitions_disjoint", "Bool"),
)


def canonical_json_sha256(record: dict[str, str]) -> str:
    payload = json.dumps(
        record, sort_keys=True, separators=(",", ":")
    ).encode()
    return hashlib.sha256(payload).hexdigest()


def _normalized(text: str) -> str:
    return " ".join(text.split())


def validate_source_anchors(
    config: AlignTarget,
    source_item: str,
    public_docs: str,
    vocabulary: str,
    pointer_source: str,
    pointer_docs: str,
) -> None:
    source = _normalized(source_item)
    docs = _normalized(public_docs)
    for fragment in (
        "if U::IS_ZST || T::IS_ZST",
        "crate::ptr::align_offset(ptr, align_of::<U>())",
        "if offset > self.len()",
        "align_to_offsets::<U>()",
        (
            "from_raw_parts_mut(mut_ptr as *mut U, us_len)"
            if config.mutable
            else "from_raw_parts(rest.as_ptr() as *const U, us_len)"
        ),
    ):
        if _normalized(fragment) not in source:
            raise GuardError(
                f"{config.target}: canonical source fragment absent: {fragment}"
            )
    for fragment in (
        "prefix, correctly aligned middle slice of a new type, and the suffix",
        "middle part will be as big as possible",
        "zero-sized",
        "transmute",
    ):
        if _normalized(fragment) not in docs:
            raise GuardError(
                f"{config.target}: public docs fragment absent: {fragment}"
            )
    for fragment in (
        "slice_align_to_domain",
        "slice_aligned_middle",
        "slice_align_to_result",
        (
            "slice_align_to_mut_result"
            if config.mutable
            else "slice_align_to_result"
        ),
    ):
        if fragment not in vocabulary:
            raise GuardError(
                f"{config.target}: active vocabulary fragment absent: {fragment}"
            )
    normalized_pointer_source = _normalized(pointer_source)
    for fragment in (
        "let stride = size_of::<T>()",
        "if stride == 0",
        "let a_mod_stride",
        "let gcdpow",
        "Cannot be aligned at all",
        "usize::MAX",
    ):
        if _normalized(fragment) not in normalized_pointer_source:
            raise GuardError(
                f"{config.target}: align_offset source fragment absent: {fragment}"
            )
    normalized_pointer_docs = _normalized(pointer_docs)
    for fragment in (
        "If it is not possible to align the pointer",
        "`usize::MAX`",
        "number of `T` elements",
        "used with the `wrapping_add` method",
    ):
        if _normalized(fragment) not in normalized_pointer_docs:
            raise GuardError(
                f"{config.target}: align_offset docs fragment absent: {fragment}"
            )
    prohibited = (
        "TargetDefinition_T",
        "Equivalent_T",
        "Provenance::null()",
        "null::<",
        "null_mut::<",
    )
    if any(
        token in text
        for token in prohibited
        for text in (source_item, pointer_source, pointer_docs)
    ):
        raise GuardError(f"{config.target}: synthetic source model detected")


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
        ("b_input_length", "x_length"),
        ("b_address", "x_address"),
        ("b_allocation", "x_allocation"),
        ("b_provenance", "x_provenance"),
        ("b_root_borrow", "x_root_borrow"),
        ("b_allocation_base", "x_allocation_base"),
        ("b_allocation_bytes", "x_allocation_bytes"),
        ("b_t_size", "x_t_size"),
        ("b_t_alignment", "x_t_alignment"),
        ("b_u_size", "x_u_size"),
        ("b_u_alignment", "x_u_alignment"),
        ("b_usize_max", "x_usize_max"),
        ("b_isize_max", "x_isize_max"),
        ("b_transmute_valid", "x_transmute_valid"),
        ("b_alias_exclusive", "x_alias_exclusive"),
        ("b_borrow_alive", "x_borrow_alive"),
        ("b_outside_frame", "x_outside_frame"),
    )
    return "\n       ".join(
        f"(= ({boundary} b) ({input_field} x))"
        for boundary, input_field in mapping
    )


def _source_definitions(config: AlignTarget, purpose: str) -> str:
    mutable = "true" if config.mutable else "false"
    immutable_final = (
        "(= (s_final_bytes s) (InitialBytes x b))"
        if not config.mutable and purpose == PRIMARY
        else "true"
    )
    final_frame = ""
    if purpose == PRIMARY:
        final_frame = f"""\
(define-fun RelationalFinalFrameTransition
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and (= (seq.len (s_final_bytes s)) (ByteCount x))
       (AllSequenceBytesValid (s_final_bytes s) 0)
       {immutable_final}
       (= (s_final_source s)
          (DecodeElements
            (s_final_bytes s) 0 (x_t_size x) (x_length x)))
       (= (s_final_prefix s)
          (ite (= (BranchKind x) {BRANCH_ALIGNED})
               (DecodeElements
                 (s_final_bytes s) 0 (x_t_size x) (PrefixLength x))
               (s_final_source s)))
       (= (s_final_middle s)
          (ite (= (BranchKind x) {BRANCH_ALIGNED})
               (DecodeElements
                 (s_final_bytes s)
                 (* (PrefixLength x) (x_t_size x))
                 (x_u_size x)
                 (MiddleLength x))
               {EMPTY_SEQ}))
       (= (s_final_suffix s)
          (ite (= (BranchKind x) {BRANCH_ALIGNED})
               (DecodeElements
                 (s_final_bytes s)
                 (* (- (x_length x) (SuffixLength x))
                    (x_t_size x))
                 (x_t_size x)
                 (SuffixLength x))
               {EMPTY_SEQ}))
       (= (s_outside_final s) (x_outside_frame x))
       (= (s_allocation s) (x_allocation x))
       (= (s_address s) (x_address x))
       (= (s_provenance s) (x_provenance x))
       (= (s_root_borrow s) (x_root_borrow x))
       (= (s_alias_exclusive s) (x_alias_exclusive x))
       (s_frame_unchanged s)
       (s_partitions_disjoint s)))"""
    return f"""\
(define-fun-rec PowerOfTwo ((n Int)) Bool
  (ite (= n 1)
       true
       (ite (or (< n 1) (= (mod n 2) 1))
            false
            (PowerOfTwo (div n 2)))))
(define-fun-rec Gcd ((a Int) (c Int)) Int
  (ite (= c 0) a (Gcd c (mod a c))))
(define-fun ByteCount ((x Input)) Int
  (* (x_length x) (x_t_size x)))
(define-fun AllocationEnd ((x Input)) Int
  (+ (x_allocation_base x) (x_allocation_bytes x)))
(define-fun InputEnd ((x Input)) Int
  (+ (x_address x) (ByteCount x)))
(define-fun-rec InitialBytesFrom
  ((b Boundary) (address Int) (remaining Int)) (Seq Int)
  (ite (<= remaining 0)
       {EMPTY_SEQ}
       (seq.++ (seq.unit (select (b_memory b) address))
               (InitialBytesFrom b (+ address 1) (- remaining 1)))))
(define-fun InitialBytes ((x Input) (b Boundary)) (Seq Int)
  (InitialBytesFrom b (x_address x) (ByteCount x)))
(define-fun-rec ByteRangeInitialized
  ((b Boundary) (address Int) (remaining Int)) Bool
  (ite (<= remaining 0)
       true
       (and (select (b_initialized b) address)
            (ByteRangeInitialized b (+ address 1) (- remaining 1)))))
(define-fun-rec ByteRangeValid
  ((b Boundary) (address Int) (remaining Int)) Bool
  (ite (<= remaining 0)
       true
       (and (<= 0 (select (b_memory b) address))
            (< (select (b_memory b) address) 256)
            (ByteRangeValid b (+ address 1) (- remaining 1)))))
(define-fun-rec AllSequenceBytesValid
  ((bytes (Seq Int)) (index Int)) Bool
  (ite (>= index (seq.len bytes))
       true
       (and (<= 0 (seq.nth bytes index))
            (< (seq.nth bytes index) 256)
            (AllSequenceBytesValid bytes (+ index 1)))))
(define-fun-rec DecodeWordFrom
  ((bytes (Seq Int)) (start Int) (remaining Int) (weight Int)) Int
  (ite (<= remaining 0)
       0
       (+ (* (seq.nth bytes start) weight)
          (DecodeWordFrom
            bytes (+ start 1) (- remaining 1) (* weight 256)))))
(define-fun DecodeWord
  ((bytes (Seq Int)) (start Int) (size Int)) Int
  (DecodeWordFrom bytes start size 1))
(define-fun-rec DecodeElements
  ((bytes (Seq Int)) (start Int) (size Int) (count Int)) (Seq Int)
  (ite (<= count 0)
       {EMPTY_SEQ}
       (seq.++ (seq.unit (DecodeWord bytes start size))
               (DecodeElements
                 bytes (+ start size) size (- count 1)))))
(define-fun-rec FirstAlignedOffset
  ((address Int) (stride Int) (alignment Int) (address_space Int)
   (candidate Int) (limit Int) (sentinel Int)) Int
  (ite (>= candidate limit)
       sentinel
       (ite (= (mod (mod (+ address (* candidate stride))
                         address_space)
                    alignment)
               0)
            candidate
            (FirstAlignedOffset
              address stride alignment address_space
              (+ candidate 1) limit sentinel))))
(define-fun PointerAlignOffset ((x Input)) Int
  (ite (= (x_t_size x) 0)
       (ite (= (mod (x_address x) (x_u_alignment x)) 0)
            0
            (x_usize_max x))
       (FirstAlignedOffset
         (x_address x)
         (x_t_size x)
         (x_u_alignment x)
         (+ (x_usize_max x) 1)
         0
         (div (x_u_alignment x)
              (Gcd (x_t_size x) (x_u_alignment x)))
         (x_usize_max x))))
(define-fun IsZstBranch ((x Input)) Bool
  (or (= (x_t_size x) 0) (= (x_u_size x) 0)))
(define-fun BranchKind ((x Input)) Int
  (ite (IsZstBranch x)
       {BRANCH_ZST}
       (ite (> (PointerAlignOffset x) (x_length x))
            {BRANCH_OFFSET_FALLBACK}
            {BRANCH_ALIGNED})))
(define-fun PrefixLength ((x Input)) Int
  (ite (= (BranchKind x) {BRANCH_ALIGNED})
       (PointerAlignOffset x)
       (x_length x)))
(define-fun RestLength ((x Input)) Int
  (ite (= (BranchKind x) {BRANCH_ALIGNED})
       (- (x_length x) (PrefixLength x))
       0))
(define-fun SizeGcd ((x Input)) Int
  (Gcd (x_t_size x) (x_u_size x)))
(define-fun TsPerBlock ((x Input)) Int
  (ite (= (SizeGcd x) 0)
       1
       (div (x_u_size x) (SizeGcd x))))
(define-fun UsPerBlock ((x Input)) Int
  (ite (= (SizeGcd x) 0)
       0
       (div (x_t_size x) (SizeGcd x))))
(define-fun MiddleLength ((x Input)) Int
  (ite (= (BranchKind x) {BRANCH_ALIGNED})
       (* (div (RestLength x) (TsPerBlock x)) (UsPerBlock x))
       0))
(define-fun SuffixLength ((x Input)) Int
  (ite (= (BranchKind x) {BRANCH_ALIGNED})
       (mod (RestLength x) (TsPerBlock x))
       0))
(define-fun EmptyReferenceAddress ((alignment Int)) Int
  alignment)
(define-fun MiddleAddress ((x Input)) Int
  (ite (= (BranchKind x) {BRANCH_ALIGNED})
       (+ (x_address x) (* (PrefixLength x) (x_t_size x)))
       (EmptyReferenceAddress (x_u_alignment x))))
(define-fun SuffixAddress ((x Input)) Int
  (ite (= (BranchKind x) {BRANCH_ALIGNED})
       (+ (x_address x)
          (* (- (x_length x) (SuffixLength x)) (x_t_size x)))
       (EmptyReferenceAddress (x_t_alignment x))))
(define-fun PrefixValues ((x Input)) (Seq Int)
  (ite (= (BranchKind x) {BRANCH_ALIGNED})
       (seq.extract (x_source x) 0 (PrefixLength x))
       (x_source x)))
(define-fun MiddleValues ((x Input) (b Boundary)) (Seq Int)
  (ite (= (BranchKind x) {BRANCH_ALIGNED})
       (DecodeElements
         (InitialBytes x b)
         (* (PrefixLength x) (x_t_size x))
         (x_u_size x)
         (MiddleLength x))
       {EMPTY_SEQ}))
(define-fun SuffixValues ((x Input)) (Seq Int)
  (ite (= (BranchKind x) {BRANCH_ALIGNED})
       (seq.extract
         (x_source x)
         (- (x_length x) (SuffixLength x))
         (x_length x))
       {EMPTY_SEQ}))
(define-fun ReturnedRegionsDisjoint ((x Input) (y Output)) Bool
  (ite (= (y_branch y) {BRANCH_ALIGNED})
       (and (= (+ (y_prefix_address y)
                  (* (y_prefix_length y) (x_t_size x)))
               (y_middle_address y))
            (= (+ (y_middle_address y)
                  (* (y_middle_length y) (x_u_size x)))
               (y_suffix_address y))
            (= (+ (y_suffix_address y)
                  (* (y_suffix_length y) (x_t_size x)))
               (InputEnd x)))
       (and (= (y_prefix_length y) (x_length x))
            (= (y_middle_length y) 0)
            (= (y_suffix_length y) 0))))
(define-fun InputBoundaryObserved ((x Input) (b Boundary)) Bool
  (and {_boundary_equalities()}))
(define-fun InitialMemoryInterpretationTransition
  ((x Input) (b Boundary)) Bool
  (and (ByteRangeInitialized b (x_address x) (ByteCount x))
       (ByteRangeValid b (x_address x) (ByteCount x))
       (= (x_source x)
          (DecodeElements
            (InitialBytes x b) 0 (x_t_size x) (x_length x)))))
(define-fun SlicePointerExtractionTransition
  ((x Input) (b Boundary) (y Output)) Bool
  (and (InputBoundaryObserved x b)
       (= (y_prefix_address y) (x_address x))
       (= (y_prefix_allocation y) (x_allocation x))
       (= (y_prefix_provenance y) (x_provenance x))
       (= (y_prefix_borrow y) (x_root_borrow x))))
(define-fun AlignOffsetTransition ((x Input) (y Output)) Bool
  (= (y_alignment_offset y)
     (ite (IsZstBranch x) 0 (PointerAlignOffset x))))
(define-fun ZstAndOffsetBranchTransition
  ((x Input) (y Output)) Bool
  (= (y_branch y) (BranchKind x)))
(define-fun AlignToOffsetsArithmeticTransition
  ((x Input) (y Output)) Bool
  (and (= (y_prefix_length y) (PrefixLength x))
       (= (y_middle_length y) (MiddleLength x))
       (= (y_suffix_length y) (SuffixLength x))
       (= (* (y_middle_length y) (x_u_size x))
          (* (- (RestLength x) (y_suffix_length y))
             (x_t_size x)))))
(define-fun SplitRangeTransition ((x Input) (y Output)) Bool
  (and (= (y_prefix_values y) (PrefixValues x))
       (= (y_suffix_values y) (SuffixValues x))
       (= (y_prefix_length y) (seq.len (y_prefix_values y)))
       (= (y_suffix_length y) (seq.len (y_suffix_values y)))))
(define-fun PointerCastAndAdditionTransition
  ((x Input) (y Output)) Bool
  (and (= (y_middle_address y) (MiddleAddress x))
       (= (y_suffix_address y) (SuffixAddress x))
       (= (y_middle_allocation y)
          (ite (= (BranchKind x) {BRANCH_ALIGNED})
               (x_allocation x) 0))
       (= (y_suffix_allocation y)
          (ite (= (BranchKind x) {BRANCH_ALIGNED})
               (x_allocation x) 0))
       (= (y_middle_provenance y)
          (ite (= (BranchKind x) {BRANCH_ALIGNED})
               (x_provenance x) 0))
       (= (y_suffix_provenance y)
          (ite (= (BranchKind x) {BRANCH_ALIGNED})
               (x_provenance x) 0))))
(define-fun RawSliceConstructionAndTypedInterpretationTransition
  ((x Input) (b Boundary) (y Output)) Bool
  (and (= (y_middle_values y) (MiddleValues x b))
       (= (y_middle_length y) (seq.len (y_middle_values y)))))
(define-fun ReferenceIdentityAndDisjointBorrowTransition
  ((x Input) (y Output)) Bool
  (and (= (y_middle_borrow y)
          (ite (= (BranchKind x) {BRANCH_ALIGNED})
               (x_root_borrow x) 0))
       (= (y_suffix_borrow y)
          (ite (= (BranchKind x) {BRANCH_ALIGNED})
               (x_root_borrow x) 0))
       (= (y_mutable y) {mutable})
       (= (y_disjoint y) (ReturnedRegionsDisjoint x y))
       (y_disjoint y)))
(define-fun ActiveSliceAlignedMiddleConjunct
  ((x Input) (b Boundary) (y Output)) Bool
  (and (= (y_middle_values y) (MiddleValues x b))
       (= (* (y_middle_length y) (x_u_size x))
          (* (- (x_length x)
                (y_prefix_length y)
                (y_suffix_length y))
             (x_t_size x)))))
(define-fun ActiveSliceAlignToResultConjunct
  ((x Input) (b Boundary) (y Output)) Bool
  (and (<= (y_prefix_length y) (x_length x))
       (<= (y_suffix_length y) (x_length x))
       (<= (+ (y_prefix_length y) (y_suffix_length y))
           (x_length x))
       (= (y_prefix_values y)
          (seq.extract (x_source x) 0 (y_prefix_length y)))
       (= (y_suffix_values y)
          (seq.extract
            (x_source x)
            (- (x_length x) (y_suffix_length y))
            (x_length x)))
       (ActiveSliceAlignedMiddleConjunct x b y)))
{final_frame}
"""


def _active_mutable_contract() -> str:
    return """\
(define-fun ActiveSliceAlignToMutResultConjunct
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and (ActiveSliceAlignToResultConjunct x b y)
       (= (seq.len (s_final_source s)) (x_length x))
       (= (seq.len (s_final_prefix s)) (y_prefix_length y))
       (= (seq.len (s_final_middle s)) (y_middle_length y))
       (= (seq.len (s_final_suffix s)) (y_suffix_length y))
       (<= (+ (seq.len (s_final_prefix s))
              (seq.len (s_final_suffix s)))
           (seq.len (s_final_source s)))
       (= (s_final_prefix s)
          (seq.extract
            (s_final_source s) 0 (seq.len (s_final_prefix s))))
       (= (s_final_suffix s)
          (seq.extract
            (s_final_source s)
            (- (seq.len (s_final_source s))
               (seq.len (s_final_suffix s)))
            (seq.len (s_final_source s))))))
"""


def _requires(config: AlignTarget) -> str:
    alias = "(x_alias_exclusive x)" if config.mutable else "true"
    return f"""\
(define-fun Requires_T ((x Input)) Bool
  (and (= (seq.len (x_source x)) (x_length x))
       (>= (x_length x) 0)
       (> (x_address x) 0)
       (>= (x_allocation x) 0)
       (>= (x_provenance x) 0)
       (> (x_root_borrow x) 0)
       (>= (x_allocation_base x) 0)
       (>= (x_allocation_bytes x) 0)
       (>= (x_t_size x) 0)
       (> (x_t_alignment x) 0)
       (>= (x_u_size x) 0)
       (> (x_u_alignment x) 0)
       (PowerOfTwo (x_t_alignment x))
       (PowerOfTwo (x_u_alignment x))
       (or (= (x_t_size x) 0)
           (and (>= (x_t_size x) (x_t_alignment x))
                (= (mod (x_t_size x) (x_t_alignment x)) 0)))
       (or (= (x_u_size x) 0)
           (and (>= (x_u_size x) (x_u_alignment x))
                (= (mod (x_u_size x) (x_u_alignment x)) 0)))
       (> (x_usize_max x) 0)
       (> (x_isize_max x) 0)
       (<= (x_isize_max x) (x_usize_max x))
       (< (x_t_alignment x) (x_usize_max x))
       (< (x_u_alignment x) (x_usize_max x))
       (<= (x_length x) (x_usize_max x))
       (<= (x_address x) (x_usize_max x))
       (= (mod (x_address x) (x_t_alignment x)) 0)
       (<= (ByteCount x) (x_isize_max x))
       (<= (InputEnd x) (x_usize_max x))
       (or (= (ByteCount x) 0)
           (and (> (x_allocation x) 0)
                (> (x_provenance x) 0)
                (<= (x_allocation_base x) (x_address x))
                (<= (InputEnd x) (AllocationEnd x))
                (<= (AllocationEnd x) (x_usize_max x))))
       (or (> (ByteCount x) 0)
           (or (and (= (x_allocation x) 0)
                    (= (x_provenance x) 0))
               (and (> (x_allocation x) 0)
                    (> (x_provenance x) 0)
                    (<= (x_allocation_base x) (x_address x))
                    (<= (x_address x) (AllocationEnd x))
                    (<= (AllocationEnd x) (x_usize_max x)))))
       (x_transmute_valid x)
       {alias}
       (x_borrow_alive x)))"""


def _boundary() -> str:
    return """\
(define-fun Boundary_T ((x Input) (b Boundary)) Bool
  (and (InputBoundaryObserved x b)
       (ByteRangeInitialized b (x_address x) (ByteCount x))
       (ByteRangeValid b (x_address x) (ByteCount x))
       (= (x_source x)
          (DecodeElements
            (InitialBytes x b) 0 (x_t_size x) (x_length x)))))
"""


def _target_definition(config: AlignTarget, purpose: str) -> str:
    calls = [
        "(InitialMemoryInterpretationTransition x b)",
        "(SlicePointerExtractionTransition x b y)",
        "(AlignOffsetTransition x y)",
        "(ZstAndOffsetBranchTransition x y)",
        "(AlignToOffsetsArithmeticTransition x y)",
        "(SplitRangeTransition x y)",
        "(PointerCastAndAdditionTransition x y)",
        "(RawSliceConstructionAndTypedInterpretationTransition x b y)",
        "(ReferenceIdentityAndDisjointBorrowTransition x y)",
        "(ActiveSliceAlignToResultConjunct x b y)",
    ]
    if purpose == PRIMARY:
        calls.append("(RelationalFinalFrameTransition x b y s)")
        if config.mutable:
            calls.append("(ActiveSliceAlignToMutResultConjunct x b y s)")
    return """\
(define-fun TargetDefinition_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and %s))""" % "\n       ".join(calls)


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
    config: AlignTarget,
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
; Boundary_T contains only initial address-indexed bytes and initialization,
; allocation/provenance, layouts, borrow/alias state, and outside frame.
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
{_source_definitions(config, purpose)}
{_active_mutable_contract() if config.mutable and purpose == PRIMARY else ""}
{_requires(config)}
{_boundary()}
{_target_definition(config, purpose)}
(define-fun Spec_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (TargetDefinition_T x b y s))
{_equivalence(purpose)}
{theorem}"""


def obligation_text(config: AlignTarget, purpose: str) -> str:
    return model_text(config, purpose, include_theorem=True)


def _source_transition_names(purpose: str) -> list[str]:
    names = [
        "SlicePointerExtractionTransition",
        "AlignOffsetTransition",
        "ZstAndOffsetBranchTransition",
        "AlignToOffsetsArithmeticTransition",
        "SplitRangeTransition",
        "PointerCastAndAdditionTransition",
        "RawSliceConstructionAndTypedInterpretationTransition",
        "ReferenceIdentityAndDisjointBorrowTransition",
    ]
    if purpose == PRIMARY:
        names.append("RelationalFinalFrameTransition")
    return names


def _source_semantics(config: AlignTarget, purpose: str) -> list[str]:
    names = [
        "InitialMemoryInterpretationTransition",
        *_source_transition_names(purpose),
        "ActiveSliceAlignedMiddleConjunct",
        "ActiveSliceAlignToResultConjunct",
    ]
    if config.mutable and purpose == PRIMARY:
        names.append("ActiveSliceAlignToMutResultConjunct")
    return names


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
    config: AlignTarget,
    purpose: str,
) -> dict[str, Any]:
    if purpose not in PURPOSES:
        raise ValueError(f"{config.target}: unknown purpose {purpose}")
    citations = [
        config.source_reference,
        config.docs_reference,
        f"{SLICE_SOURCE_PATH}:4433-4464",
        f"{PTR_SOURCE_PATH}:{PTR_SOURCE_RANGE[0]}-{PTR_SOURCE_RANGE[1]}",
        f"{PTR_DOCS_PATH}:{PTR_DOCS_RANGE[0]}-{PTR_DOCS_RANGE[1]}",
    ]
    return {
        "schema_version": 3,
        "target": config.target,
        "input_order": config.input_order,
        "obligation_purpose": purpose,
        "active_contract_sha256": config.active_contract_sha256,
        "active_contract_text": config.active_contract_text,
        "domain": {
            "source_model_complete": True,
            "input": (
                "valid Slice reference plus the public unsafe transmute "
                "precondition; empty and ZST representations are included"
            ),
            "align_offset": (
                "minimal element offset over wrapping pointer addresses, with "
                "usize::MAX exactly when the stride/alignment congruence has "
                "no solution"
            ),
            "memory": (
                "initial bytes are initialized and address-indexed; T and U "
                "views are little-endian finite decodings of the same bytes"
            ),
            "mutable_final_state": (
                "returned mutable partitions may write their covered bytes; "
                "all final T/U views are re-decoded from one final byte frame"
                if config.mutable
                else "shared output preserves the complete initial byte frame"
            ),
        },
        "contract_translation": {
            "active_contract_preserved": True,
            "opaque_vocabulary_declared_to_solver": False,
            "canonical_answer_conjoined_outside_active_contract": False,
            "source_flow": [
                "extract the Slice thin pointer without a null-provenance proxy",
                "evaluate canonical align_offset including ZST and no-solution",
                "select ZST, offset fallback, or aligned branch",
                "evaluate gcd-based align_to_offsets arithmetic",
                "derive prefix/rest/middle/suffix byte ranges",
                "perform pointer casts and element additions with provenance",
                "construct raw slices and decode the typed middle from bytes",
                "preserve returned-reference identity and mutable disjointness",
                "derive relational final T/U views from one final byte frame",
                "check every literal generated result/final-frame conjunct",
            ],
        },
        "boundary_scope": {
            "shared_observations": [
                "initial address-indexed bytes and initialization",
                "input length, allocation bounds, address, and provenance",
                "T/U size, alignment, ZST, and platform limits",
                "root borrow, liveness, alias permission, and outside frame",
                "public unsafe transmute-validity precondition",
            ],
            "excluded_observations": [
                "slice_aligned_middle or slice_align_to_domain oracle",
                "alignment offset, branch answer, or gcd result",
                "returned partitions, ranges, references, or decoded U values",
                "final bytes, final views, or target truth",
                "answer encoding or complete execution trace",
            ],
            "admitted_trust_site_ids": list(config.admitted_trust_site_ids),
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
        "source_backed_replacements": [
            {
                "replacement_id": config.replacement_id,
                "operation": (
                    "canonical Slice pointer extraction, ptr::align_offset, "
                    "ZST/overflow branch, align_to_offsets gcd arithmetic, "
                    "split ranges, pointer casts/addition, raw-slice typed "
                    "interpretation, reference identity, provenance, disjoint "
                    "mutable borrows, and relational final frame"
                ),
                "symbols": _source_transition_names(purpose),
                "source_citations": citations,
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
        "source_transition_definitions": _source_transition_names(purpose),
        "source_semantics": _source_semantics(config, purpose),
        "principal_observations": _principal_observations(purpose),
        "equivalence_kind": "exact",
        "equivalence_review": {
            "principal_return": (
                "exact branch, offset, three values/lengths, all returned "
                "addresses/allocation/provenance/borrow identities, mutability, "
                "and disjointness"
            ),
            "final_state": (
                "not projected by exact-output obligation"
                if purpose == EXACT_OUTPUT
                else (
                    "exact final bytes, T/U partition views, outside frame, "
                    "allocation/provenance/root borrow, aliasing, and frame"
                )
            ),
            "weakened_observations": [],
        },
        "expected_solver_result": config.expected_solver_results[purpose],
    }


def obligation(
    config: AlignTarget,
    purpose: str,
) -> tuple[str, dict[str, Any]]:
    return obligation_text(config, purpose), obligation_metadata(config, purpose)


def validate_target_obligation(
    config: AlignTarget,
    text: str,
    metadata: dict[str, Any],
) -> None:
    purpose = metadata.get("obligation_purpose")
    if purpose not in PURPOSES:
        raise GuardError(f"{config.target}: invalid obligation purpose")
    if text != obligation_text(config, str(purpose)):
        raise GuardError(f"{config.target}: reviewed SMT text changed")
    if metadata != obligation_metadata(config, str(purpose)):
        raise GuardError(f"{config.target}: reviewed metadata changed")
    prohibited = (
        "(declare-fun",
        "b_output",
        "b_result",
        "b_return",
        "b_final",
        "b_trace",
        "b_alignment_offset",
        "b_branch",
        "b_middle_values",
        "slice_align_to_domain (",
        "slice_aligned_middle (",
    )
    if any(token in text for token in prohibited):
        raise GuardError(f"{config.target}: answer-bearing or opaque model")
    for symbol in _source_semantics(config, str(purpose)):
        if symbol not in text:
            raise GuardError(
                f"{config.target}: source transition absent: {symbol}"
            )
    if (
        purpose == PRIMARY
        and "RelationalFinalFrameTransition" not in text
    ):
        raise GuardError(f"{config.target}: relational final frame absent")
    validate_obligation(text, metadata)


@dataclass(frozen=True)
class SourceCase:
    memory: tuple[int, ...]
    length: int
    address: int = 64
    allocation: int = 7
    provenance: int = 11
    root_borrow: int = 17
    allocation_base: int = 32
    allocation_bytes: int = 192
    t_size: int = 1
    t_alignment: int = 1
    u_size: int = 2
    u_alignment: int = 2
    usize_max: int = 255
    isize_max: int = 127
    transmute_valid: bool = True
    alias_exclusive: bool = True
    borrow_alive: bool = True
    outside_frame: tuple[int, ...] = (90, 91)
    uninitialized_indices: tuple[int, ...] = ()


def _bytes(length: int, start: int = 1) -> tuple[int, ...]:
    return tuple((start + index) % 251 for index in range(length))


def source_cases(config: AlignTarget) -> dict[str, SourceCase]:
    del config
    return {
        "empty": SourceCase((), 0),
        "zst_source": SourceCase(
            (),
            3,
            address=65,
            t_size=0,
            t_alignment=1,
            u_size=2,
            u_alignment=2,
        ),
        "zst_destination": SourceCase(
            _bytes(4),
            4,
            address=65,
            t_size=1,
            t_alignment=1,
            u_size=0,
            u_alignment=1,
        ),
        "already_aligned_byte_reinterpretation": SourceCase(
            _bytes(7), 7
        ),
        "misaligned_finite_offset": SourceCase(
            _bytes(8),
            8,
            address=65,
            u_size=4,
            u_alignment=4,
        ),
        "offset_equals_length": SourceCase(
            _bytes(3),
            3,
            address=65,
            u_size=4,
            u_alignment=4,
        ),
        "offset_greater_than_length": SourceCase(
            _bytes(2),
            2,
            address=65,
            u_size=4,
            u_alignment=4,
        ),
        "offset_usize_max": SourceCase(
            _bytes(16),
            2,
            address=66,
            t_size=8,
            t_alignment=1,
            u_size=4,
            u_alignment=4,
        ),
        "nontrivial_size_gcd": SourceCase(
            _bytes(80),
            5,
            address=64,
            allocation_base=32,
            allocation_bytes=192,
            t_size=16,
            t_alignment=8,
            u_size=24,
            u_alignment=8,
        ),
        "allocation_provenance": SourceCase(
            _bytes(8, 31),
            4,
            address=80,
            allocation=19,
            provenance=29,
            root_borrow=39,
            allocation_base=64,
            allocation_bytes=64,
            t_size=2,
            t_alignment=2,
            u_size=4,
            u_alignment=4,
        ),
    }


def _decode_word(memory: tuple[int, ...], start: int, size: int) -> int:
    return sum(
        memory[start + index] * (256**index)
        for index in range(size)
    )


def _decode_elements(
    memory: tuple[int, ...],
    start: int,
    size: int,
    count: int,
) -> tuple[int, ...]:
    if size == 0:
        return tuple(0 for _ in range(count))
    return tuple(
        _decode_word(memory, start + index * size, size)
        for index in range(count)
    )


def _align_offset(case: SourceCase) -> int:
    if case.t_size == 0:
        return (
            0
            if case.address % case.u_alignment == 0
            else case.usize_max
        )
    period = case.u_alignment // math.gcd(
        case.t_size, case.u_alignment
    )
    address_space = case.usize_max + 1
    for offset in range(period):
        address = (
            case.address + offset * case.t_size
        ) % address_space
        if address % case.u_alignment == 0:
            return offset
    return case.usize_max


def evaluate_source(case: SourceCase) -> dict[str, Any]:
    source = _decode_elements(case.memory, 0, case.t_size, case.length)
    if case.t_size == 0 or case.u_size == 0:
        branch = BRANCH_ZST
        offset = 0
    else:
        offset = _align_offset(case)
        branch = (
            BRANCH_OFFSET_FALLBACK
            if offset > case.length
            else BRANCH_ALIGNED
        )
    if branch == BRANCH_ALIGNED:
        prefix_length = offset
        rest_length = case.length - prefix_length
        size_gcd = math.gcd(case.t_size, case.u_size)
        ts = case.u_size // size_gcd
        us = case.t_size // size_gcd
        middle_length = rest_length // ts * us
        suffix_length = rest_length % ts
        prefix = source[:prefix_length]
        middle = _decode_elements(
            case.memory,
            prefix_length * case.t_size,
            case.u_size,
            middle_length,
        )
        suffix = source[case.length - suffix_length :]
        middle_address = case.address + prefix_length * case.t_size
        suffix_address = (
            case.address
            + (case.length - suffix_length) * case.t_size
        )
    else:
        prefix_length = case.length
        middle_length = 0
        suffix_length = 0
        prefix = source
        middle = ()
        suffix = ()
        middle_address = case.u_alignment
        suffix_address = case.t_alignment
    return {
        "branch": branch,
        "offset": offset,
        "source": source,
        "prefix": prefix,
        "middle": middle,
        "suffix": suffix,
        "prefix_length": prefix_length,
        "middle_length": middle_length,
        "suffix_length": suffix_length,
        "prefix_address": case.address,
        "middle_address": middle_address,
        "suffix_address": suffix_address,
    }


def _seq(values: tuple[int, ...]) -> str:
    if not values:
        return EMPTY_SEQ
    expression = EMPTY_SEQ
    for value in values:
        expression = f"(seq.++ {expression} (seq.unit {value}))"
    return expression


def _bool(value: bool) -> str:
    return str(value).lower()


def _memory_array(case: SourceCase) -> str:
    expression = "((as const (Array Int Int)) 0)"
    for index, value in enumerate(case.memory):
        expression = f"(store {expression} {case.address + index} {value})"
    return expression


def _initialized_array(case: SourceCase) -> str:
    expression = "((as const (Array Int Bool)) false)"
    missing = set(case.uninitialized_indices)
    for index in range(len(case.memory)):
        if index not in missing:
            expression = (
                f"(store {expression} {case.address + index} true)"
            )
    return expression


def _input_expression(case: SourceCase) -> str:
    source = evaluate_source(case)["source"]
    values: tuple[Any, ...] = (
        _seq(source),
        case.length,
        case.address,
        case.allocation,
        case.provenance,
        case.root_borrow,
        case.allocation_base,
        case.allocation_bytes,
        case.t_size,
        case.t_alignment,
        case.u_size,
        case.u_alignment,
        case.usize_max,
        case.isize_max,
        _bool(case.transmute_valid),
        _bool(case.alias_exclusive),
        _bool(case.borrow_alive),
        _seq(case.outside_frame),
    )
    return "(mkInput " + " ".join(map(str, values)) + ")"


def _boundary_expression(
    case: SourceCase,
    *,
    address_mismatch: bool = False,
) -> str:
    values: tuple[Any, ...] = (
        _memory_array(case),
        _initialized_array(case),
        case.length,
        case.address + (1 if address_mismatch else 0),
        case.allocation,
        case.provenance,
        case.root_borrow,
        case.allocation_base,
        case.allocation_bytes,
        case.t_size,
        case.t_alignment,
        case.u_size,
        case.u_alignment,
        case.usize_max,
        case.isize_max,
        _bool(case.transmute_valid),
        _bool(case.alias_exclusive),
        _bool(case.borrow_alive),
        _seq(case.outside_frame),
    )
    return "(mkBoundary " + " ".join(map(str, values)) + ")"


def _model_query(purpose: str) -> str:
    fields = [f"({selector} y1)" for selector, _ in OUTPUT_FIELDS]
    if purpose == PRIMARY:
        fields.extend(f"({selector} s1)" for selector, _ in STATE_FIELDS)
    return "(get-value (\n  " + "\n  ".join(fields) + "))\n"


def source_instance_text(config: AlignTarget, name: str) -> str:
    try:
        case = source_cases(config)[name]
    except KeyError as exc:
        raise ValueError(f"{config.target}: unknown source case {name}") from exc
    expected = evaluate_source(case)
    assertions = [
        f"(assert (= x {_input_expression(case)}))",
        f"(assert (= b {_boundary_expression(case)}))",
        "(assert (Requires_T x))",
        "(assert (Boundary_T x b))",
        "(assert (Spec_T x b y1 s1))",
        f"(assert (= (y_branch y1) {expected['branch']}))",
        f"(assert (= (y_alignment_offset y1) {expected['offset']}))",
        f"(assert (= (y_prefix_values y1) {_seq(expected['prefix'])}))",
        f"(assert (= (y_middle_values y1) {_seq(expected['middle'])}))",
        f"(assert (= (y_suffix_values y1) {_seq(expected['suffix'])}))",
        f"(assert (= (y_prefix_length y1) {expected['prefix_length']}))",
        f"(assert (= (y_middle_length y1) {expected['middle_length']}))",
        f"(assert (= (y_suffix_length y1) {expected['suffix_length']}))",
        f"(assert (= (y_middle_address y1) {expected['middle_address']}))",
        f"(assert (= (y_suffix_address y1) {expected['suffix_address']}))",
    ]
    return (
        model_text(config, PRIMARY)
        + "\n"
        + "\n".join(assertions)
        + "\n(check-sat)\n"
        + _model_query(PRIMARY)
    )


COMMON_NEGATIVE_PROBES = (
    "invalid_null",
    "invalid_misaligned_input",
    "invalid_allocation",
    "invalid_provenance",
    "invalid_uninitialized_byte",
    "invalid_byte_value",
    "invalid_dead_borrow",
    "invalid_transmute",
    "boundary_memory_mismatch",
    "wrong_align_offset",
    "wrong_zst_branch",
    "wrong_offset_fallback_branch",
    "wrong_gcd_lengths",
    "wrong_split_ranges",
    "wrong_pointer_cast",
    "wrong_middle_decode",
    "wrong_reference_identity",
    "wrong_disjointness",
    "wrong_final_frame",
    "answer_laundered_branch",
    "answer_laundered_middle",
)


def negative_probe_names(config: AlignTarget) -> tuple[str, ...]:
    return COMMON_NEGATIVE_PROBES + (
        ("invalid_alias_permission",) if config.mutable else ()
    )


def _negative_case(
    config: AlignTarget,
    name: str,
) -> tuple[SourceCase, bool, str | None]:
    base = source_cases(config)["already_aligned_byte_reinterpretation"]
    mismatch = False
    contradiction: str | None = None
    invalid = name.startswith("invalid_") or name == "boundary_memory_mismatch"
    if name == "invalid_null":
        base = replace(base, address=0, allocation_base=0)
    elif name == "invalid_misaligned_input":
        base = SourceCase(
            _bytes(12),
            3,
            address=65,
            t_size=4,
            t_alignment=4,
            u_size=2,
            u_alignment=2,
        )
    elif name == "invalid_allocation":
        base = replace(base, allocation=0)
    elif name == "invalid_provenance":
        base = replace(base, provenance=0)
    elif name == "invalid_uninitialized_byte":
        base = replace(base, uninitialized_indices=(1,))
    elif name == "invalid_byte_value":
        base = replace(base, memory=(300, *base.memory[1:]))
    elif name == "invalid_dead_borrow":
        base = replace(base, borrow_alive=False)
    elif name == "invalid_transmute":
        base = replace(base, transmute_valid=False)
    elif name == "invalid_alias_permission":
        base = replace(base, alias_exclusive=False)
    elif name == "boundary_memory_mismatch":
        mismatch = True
    else:
        invalid = False
        if name == "wrong_align_offset":
            base = source_cases(config)["misaligned_finite_offset"]
            expected = evaluate_source(base)
            contradiction = (
                f"(distinct (y_alignment_offset y1) {expected['offset']})"
            )
        elif name == "wrong_zst_branch":
            base = source_cases(config)["zst_source"]
            contradiction = f"(distinct (y_branch y1) {BRANCH_ZST})"
        elif name == "wrong_offset_fallback_branch":
            base = source_cases(config)["offset_greater_than_length"]
            contradiction = (
                f"(distinct (y_branch y1) {BRANCH_OFFSET_FALLBACK})"
            )
        elif name == "wrong_gcd_lengths":
            base = source_cases(config)["nontrivial_size_gcd"]
            expected = evaluate_source(base)
            contradiction = (
                "(or "
                f"(distinct (y_middle_length y1) {expected['middle_length']}) "
                f"(distinct (y_suffix_length y1) {expected['suffix_length']}))"
            )
        elif name == "wrong_split_ranges":
            expected = evaluate_source(base)
            contradiction = (
                f"(= (y_suffix_values y1) {_seq((999,))})"
            )
            assert expected["suffix"]
        elif name == "wrong_pointer_cast":
            expected = evaluate_source(base)
            contradiction = (
                f"(distinct (y_middle_address y1) "
                f"{expected['middle_address']})"
            )
        elif name == "wrong_middle_decode":
            expected = evaluate_source(base)
            contradiction = (
                f"(distinct (y_middle_values y1) "
                f"{_seq(expected['middle'])})"
            )
        elif name == "wrong_reference_identity":
            contradiction = (
                "(distinct (y_middle_allocation y1) (x_allocation x))"
            )
        elif name == "wrong_disjointness":
            contradiction = "(not (y_disjoint y1))"
        elif name == "wrong_final_frame":
            contradiction = (
                "(distinct (s_final_source s1) "
                "(DecodeElements (s_final_bytes s1) 0 "
                "(x_t_size x) (x_length x)))"
            )
        elif name == "answer_laundered_branch":
            contradiction = "(= (y_branch y1) (b_root_borrow b))"
        elif name == "answer_laundered_middle":
            contradiction = (
                "(= (y_middle_values y1) "
                "(seq.unit (b_usize_max b)))"
            )
        else:
            raise ValueError(f"{config.target}: unknown negative probe {name}")
    return base, mismatch, None if invalid else contradiction


def negative_probe_text(config: AlignTarget, name: str) -> str:
    if name not in negative_probe_names(config):
        raise ValueError(f"{config.target}: unknown negative probe {name}")
    case, mismatch, contradiction = _negative_case(config, name)
    assertions = [
        f"(assert (= x {_input_expression(case)}))",
        f"(assert (= b {_boundary_expression(case, address_mismatch=mismatch)}))",
        "(assert (Requires_T x))",
        "(assert (Boundary_T x b))",
    ]
    if contradiction is not None:
        assertions.extend(
            ("(assert (Spec_T x b y1 s1))", f"(assert {contradiction})")
        )
    return (
        model_text(config, PRIMARY)
        + "\n"
        + "\n".join(assertions)
        + "\n(check-sat)\n"
    )


def witness_payload(config: AlignTarget) -> dict[str, Any]:
    if not config.mutable:
        raise ValueError("only align_to_mut has a full-state witness")
    case = source_cases(config)["already_aligned_byte_reinterpretation"]
    first = case.memory
    second = (99, *case.memory[1:])
    return {
        "schema_version": 1,
        "target": config.target,
        "input_order": config.input_order,
        "active_contract_sha256": config.active_contract_sha256,
        "source_case": "already_aligned_byte_reinterpretation",
        "shared_input": {
            field: list(value) if isinstance(value, tuple) else value
            for field, value in vars(case).items()
        },
        "shared_boundary": {
            "initial_bytes": list(case.memory),
            "address": case.address,
            "allocation": case.allocation,
            "provenance": case.provenance,
            "root_borrow": case.root_borrow,
            "same_for_both_executions": True,
        },
        "execution1": {"final_bytes": list(first)},
        "execution2": {"final_bytes": list(second)},
        "enforced_relational_frame": {
            "final_source": "decoded as T from final_bytes",
            "final_prefix": "decoded T prefix",
            "final_middle": "decoded U middle",
            "final_suffix": "decoded T suffix",
            "outside_frame_unchanged": True,
            "allocation_provenance_root_borrow_unchanged": True,
        },
        "expected": {
            "both_executions_satisfy_every_active_conjunct": True,
            "exact_output_equal": True,
            "full_state_equal": False,
            "full_exact_equivalent": False,
        },
    }


def fixed_full_state_witness_text(config: AlignTarget) -> str:
    if not config.mutable:
        raise ValueError("only align_to_mut has a full-state witness")
    case = source_cases(config)["already_aligned_byte_reinterpretation"]
    first = case.memory
    second = (99, *case.memory[1:])
    return model_text(config, PRIMARY) + f"""\
(assert (= x {_input_expression(case)}))
(assert (= b {_boundary_expression(case)}))
(assert (Requires_T x))
(assert (Boundary_T x b))
(assert (Spec_T x b y1 s1))
(assert (Spec_T x b y2 s2))
(assert (= (s_final_bytes s1) {_seq(first)}))
(assert (= (s_final_bytes s2) {_seq(second)}))
(assert (not (Equivalent_T x b y1 s1 y2 s2)))
(check-sat)
(get-value (
  (y_middle_values y1)
  (y_middle_values y2)
  (s_final_bytes s1)
  (s_final_bytes s2)
  (s_final_source s1)
  (s_final_source s2)
  (s_final_middle s1)
  (s_final_middle s2)
  (s_outside_final s1)
  (s_outside_final s2)
  (Equivalent_T x b y1 s1 y2 s2)))
"""


def boundary_manifest(config: AlignTarget) -> dict[str, Any]:
    return {
        "schema_version": 2,
        "target": config.target,
        "input_order": config.input_order,
        "active_contract_sha256": config.active_contract_sha256,
        "boundary_narrower_than_target": True,
        "proof_boundary_assumption": (
            "Both executions share one valid Slice input and one Boundary_T "
            "containing only initial address-indexed bytes/initialization, "
            "allocation/provenance, input length, T/U layout and platform "
            "facts, root borrow/alias/liveness, and outside frame. Offset, "
            "branch, partition, typed middle, returned identities, and final "
            "state are all derived after Boundary_T."
        ),
        "shared_boundary_observations": [
            {
                "fields": ["b_memory", "b_initialized"],
                "kind": "initial address-indexed byte memory",
            },
            {
                "fields": [
                    "b_input_length",
                    "b_address",
                    "b_allocation",
                    "b_provenance",
                    "b_allocation_base",
                    "b_allocation_bytes",
                ],
                "kind": "input Slice representation and allocation",
            },
            {
                "fields": [
                    "b_t_size",
                    "b_t_alignment",
                    "b_u_size",
                    "b_u_alignment",
                    "b_usize_max",
                    "b_isize_max",
                    "b_transmute_valid",
                ],
                "kind": "type layout, platform, and unsafe precondition",
            },
            {
                "fields": [
                    "b_root_borrow",
                    "b_alias_exclusive",
                    "b_borrow_alive",
                    "b_outside_frame",
                ],
                "kind": "initial borrow, aliasing, liveness, and outside frame",
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
            "slice_align_to_domain or slice_aligned_middle oracle",
            "offset, gcd result, ZST/overflow branch, or partition lengths",
            "returned partitions, decoded middle, or reference identities",
            "final bytes, final T/U views, or target truth",
            "answer encodings and complete execution traces",
        ],
    }


def verus_text(config: AlignTarget) -> str:
    mutable = "true" if config.mutable else "false"
    full_proof = (
        """
pub proof fn full_state_conditional_complete_align_to(
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
    reveal(final_state_relation);
}
"""
        if not config.mutable
        else """
pub proof fn full_state_conditional_incomplete_align_to_mut(
    input: Input,
    boundary: Boundary,
    first: Seq<int>,
    second: Seq<int>,
)
    requires
        boundary_holds(input, boundary),
        first.len() == input.length * input.t_size,
        second.len() == input.length * input.t_size,
        first != second,
    ensures
        target_transition(
            input,
            boundary,
            source_output(input, boundary),
            source_state(input, boundary, first),
        ),
        target_transition(
            input,
            boundary,
            source_output(input, boundary),
            source_state(input, boundary, second),
        ),
        source_state(input, boundary, first)
            != source_state(input, boundary, second),
{
    reveal(target_transition);
    reveal(final_state_relation);
    reveal(source_state);
}
"""
    )
    return f"""\
#![allow(dead_code, unused_imports, unused_variables)]
// Trusted-free source-transition model for {config.target}.

use vstd::prelude::*;
use vstd::seq::*;

verus! {{

pub ghost struct Input {{
    pub source: Seq<int>,
    pub length: nat,
    pub address: nat,
    pub allocation: int,
    pub provenance: int,
    pub root_borrow: int,
    pub t_size: nat,
    pub u_size: nat,
    pub u_alignment: nat,
    pub usize_max: nat,
    pub outside_frame: Seq<int>,
}}

pub ghost struct Boundary {{
    pub initial_bytes: Seq<int>,
    pub address: nat,
    pub allocation: int,
    pub provenance: int,
    pub root_borrow: int,
    pub t_size: nat,
    pub u_size: nat,
    pub u_alignment: nat,
    pub outside_frame: Seq<int>,
}}

pub ghost struct Output {{
    pub branch: nat,
    pub offset: nat,
    pub prefix: Seq<int>,
    pub middle: Seq<int>,
    pub suffix: Seq<int>,
    pub prefix_length: nat,
    pub middle_length: nat,
    pub suffix_length: nat,
    pub prefix_address: nat,
    pub middle_address: nat,
    pub suffix_address: nat,
    pub prefix_allocation: int,
    pub middle_allocation: int,
    pub suffix_allocation: int,
    pub prefix_provenance: int,
    pub middle_provenance: int,
    pub suffix_provenance: int,
    pub prefix_borrow: int,
    pub middle_borrow: int,
    pub suffix_borrow: int,
    pub mutable: bool,
    pub disjoint: bool,
}}

pub ghost struct FinalState {{
    pub final_bytes: Seq<int>,
    pub final_source: Seq<int>,
    pub final_prefix: Seq<int>,
    pub final_middle: Seq<int>,
    pub final_suffix: Seq<int>,
    pub outside_final: Seq<int>,
}}

pub open spec fn gcd(a: nat, c: nat) -> nat
    decreases c
{{
    if c == 0 {{ a }} else {{ gcd(c, a % c) }}
}}

pub open spec fn first_aligned_offset(
    address: nat,
    stride: nat,
    alignment: nat,
    address_space: nat,
    candidate: nat,
    remaining: nat,
) -> Option<nat>
    decreases remaining
{{
    if remaining == 0 {{
        None
    }} else if ((address + candidate * stride) % address_space)
        % alignment == 0 {{
        Some(candidate)
    }} else {{
        first_aligned_offset(
            address,
            stride,
            alignment,
            address_space,
            candidate + 1,
            (remaining - 1) as nat,
        )
    }}
}}

pub open spec fn align_offset(input: Input) -> nat {{
    if input.t_size == 0 {{
        if input.address % input.u_alignment == 0 {{
            0
        }} else {{
            input.usize_max
        }}
    }} else {{
        match first_aligned_offset(
            input.address,
            input.t_size,
            input.u_alignment,
            input.usize_max + 1,
            0,
            input.u_alignment,
        ) {{
            Some(offset) => offset,
            None => input.usize_max,
        }}
    }}
}}

pub open spec fn decode_word(
    bytes: Seq<int>,
    start: nat,
    size: nat,
) -> int
    decreases size
{{
    if size == 0 {{
        0
    }} else {{
        bytes[start as int]
            + 256 * decode_word(bytes, start + 1, (size - 1) as nat)
    }}
}}

pub open spec fn decode_elements(
    bytes: Seq<int>,
    start: nat,
    size: nat,
    count: nat,
) -> Seq<int>
    decreases count
{{
    if count == 0 {{
        Seq::empty()
    }} else {{
        seq![decode_word(bytes, start, size)]
            + decode_elements(
                bytes,
                start + size,
                size,
                (count - 1) as nat,
            )
    }}
}}

pub open spec fn source_output(input: Input, boundary: Boundary) -> Output {{
    let zst = input.t_size == 0 || input.u_size == 0;
    let offset = if zst {{ 0 }} else {{ align_offset(input) }};
    let aligned = !zst && offset <= input.length;
    let prefix_length = if aligned {{ offset }} else {{ input.length }};
    let rest_length: nat = (input.length - prefix_length) as nat;
    let size_gcd = gcd(input.t_size, input.u_size);
    let ts: nat =
        if size_gcd == 0 {{ 1 }}
        else {{ (input.u_size / size_gcd) as nat }};
    let us: nat =
        if size_gcd == 0 {{ 0 }}
        else {{ (input.t_size / size_gcd) as nat }};
    let middle_length: nat =
        if aligned {{
            ((rest_length / ts) * us) as nat
        }} else {{
            0
        }};
    let suffix_length: nat =
        if aligned {{ (rest_length % ts) as nat }} else {{ 0 }};
    let prefix =
        if aligned {{
            input.source.subrange(0, prefix_length as int)
        }} else {{
            input.source
        }};
    let middle =
        if aligned {{
            decode_elements(
                boundary.initial_bytes,
                prefix_length * input.t_size,
                input.u_size,
                middle_length,
            )
        }} else {{
            Seq::empty()
        }};
    let suffix =
        if aligned {{
            input.source.subrange(
                (input.length - suffix_length) as int,
                input.length as int,
            )
        }} else {{
            Seq::empty()
        }};
    Output {{
        branch: if zst {{ {BRANCH_ZST} }}
            else if !aligned {{ {BRANCH_OFFSET_FALLBACK} }}
            else {{ {BRANCH_ALIGNED} }},
        offset,
        prefix,
        middle,
        suffix,
        prefix_length,
        middle_length,
        suffix_length,
        prefix_address: input.address,
        middle_address: input.address + prefix_length * input.t_size,
        suffix_address:
            input.address
                + ((input.length - suffix_length) as nat) * input.t_size,
        prefix_allocation: input.allocation,
        middle_allocation: if aligned {{ input.allocation }} else {{ 0 }},
        suffix_allocation: if aligned {{ input.allocation }} else {{ 0 }},
        prefix_provenance: input.provenance,
        middle_provenance: if aligned {{ input.provenance }} else {{ 0 }},
        suffix_provenance: if aligned {{ input.provenance }} else {{ 0 }},
        prefix_borrow: input.root_borrow,
        middle_borrow: if aligned {{ input.root_borrow }} else {{ 0 }},
        suffix_borrow: if aligned {{ input.root_borrow }} else {{ 0 }},
        mutable: {mutable},
        disjoint: true,
    }}
}}

pub open spec fn source_state(
    input: Input,
    boundary: Boundary,
    final_bytes: Seq<int>,
) -> FinalState {{
    let output = source_output(input, boundary);
    let final_source =
        decode_elements(final_bytes, 0, input.t_size, input.length);
    FinalState {{
        final_bytes,
        final_source,
        final_prefix:
            if output.branch == {BRANCH_ALIGNED} {{
                decode_elements(
                    final_bytes,
                    0,
                    input.t_size,
                    output.prefix_length,
                )
            }} else {{
                final_source
            }},
        final_middle:
            if output.branch == {BRANCH_ALIGNED} {{
                decode_elements(
                    final_bytes,
                    output.prefix_length * input.t_size,
                    input.u_size,
                    output.middle_length,
                )
            }} else {{
                Seq::empty()
            }},
        final_suffix:
            if output.branch == {BRANCH_ALIGNED} {{
                decode_elements(
                    final_bytes,
                    ((input.length - output.suffix_length) as nat)
                        * input.t_size,
                    input.t_size,
                    output.suffix_length,
                )
            }} else {{
                Seq::empty()
            }},
        outside_final: input.outside_frame,
    }}
}}

pub open spec fn boundary_holds(input: Input, boundary: Boundary) -> bool {{
    boundary.address == input.address
        && boundary.allocation == input.allocation
        && boundary.provenance == input.provenance
        && boundary.root_borrow == input.root_borrow
        && boundary.t_size == input.t_size
        && boundary.u_size == input.u_size
        && boundary.u_alignment == input.u_alignment
        && boundary.outside_frame == input.outside_frame
}}

pub open spec fn final_state_relation(
    input: Input,
    boundary: Boundary,
    state: FinalState,
) -> bool {{
    state.final_bytes.len() == input.length * input.t_size
        && state == source_state(input, boundary, state.final_bytes)
        && (!{mutable} ==> state.final_bytes == boundary.initial_bytes)
}}

pub open spec fn target_transition(
    input: Input,
    boundary: Boundary,
    output: Output,
    state: FinalState,
) -> bool {{
    boundary_holds(input, boundary)
        && output == source_output(input, boundary)
        && final_state_relation(input, boundary, state)
}}

pub proof fn exact_output_conditional_complete_{config.function_name}(
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
