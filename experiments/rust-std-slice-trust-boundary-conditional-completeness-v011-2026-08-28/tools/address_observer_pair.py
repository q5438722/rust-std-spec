#!/usr/bin/env python3
"""Source-backed obligations for element_offset and subslice_range."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any

from checker_guards import GuardError, validate_obligation


PRIMARY = "completeness-modulo-reviewed-equivalence"
EXACT_OUTPUT = "exact-output-determinism"
PURPOSES = (PRIMARY, EXACT_OUTPUT)

SOURCE_PATH = "core/src/slice/mod.rs"
SOURCE_FILE_SHA256 = (
    "58901fa6437dbd4d77c68427bbced0fc3a91a10fdb8bd2e233adf6a9ba27d2d5"
)
VOCABULARY_RANGES = ((1097, 1128),)
VERUS_EXPECTED_SUMMARY = "verification results:: 2 verified, 0 errors"


@dataclass(frozen=True)
class AddressObserverTarget:
    target: str
    input_order: str
    artifact_id: str
    kind: str
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
    source_fragments: tuple[str, ...]
    docs_fragments: tuple[str, ...]

    @property
    def source_reference(self) -> str:
        return f"{SOURCE_PATH}:{self.source_start}-{self.source_end}"

    @property
    def docs_reference(self) -> str:
        return f"{SOURCE_PATH}:{self.docs_start}-{self.docs_end}"

    @property
    def output_sort(self) -> str:
        return "ElementReturn" if self.kind == "element" else "RangeReturn"

    @property
    def replacement_id(self) -> str:
        return (
            f"SRC-{int(self.input_order):03d}-RUST-ADDRESS-OPTION-TRANSITIONS"
        )

    @property
    def all_trust_site_ids(self) -> tuple[str, ...]:
        return tuple(record_id for record_id, _ in self.trust_record_sha256)

    @property
    def trust_hashes(self) -> dict[str, str]:
        return dict(self.trust_record_sha256)

    @property
    def context_only_trust_site_ids(self) -> tuple[str, ...]:
        prefix = f"TS-{int(self.input_order):03d}"
        return (
            f"{prefix}-D001",
            f"{prefix}-C001",
            f"{prefix}-C002",
            f"{prefix}-C003",
        )

    @property
    def excluded_trust_site_ids(self) -> tuple[str, ...]:
        prefix = f"TS-{int(self.input_order):03d}"
        if self.kind == "element":
            return (
                f"{prefix}-D006",
                f"{prefix}-E003",
                f"{prefix}-E004",
                f"{prefix}-E005",
            )
        return (
            f"{prefix}-D006",
            f"{prefix}-E002",
            f"{prefix}-E003",
            f"{prefix}-E004",
        )

    @property
    def admitted_trust_site_ids(self) -> tuple[str, ...]:
        excluded = set(self.excluded_trust_site_ids)
        context = set(self.context_only_trust_site_ids)
        return tuple(
            site
            for site in self.all_trust_site_ids
            if site not in excluded and site not in context
        )

    @property
    def expected_results(self) -> dict[str, str]:
        return {purpose: "unsat" for purpose in PURPOSES}

    @property
    def expected_classification(self) -> dict[str, str]:
        return {
            "exact_output_determinism_status": "conditional-complete",
            "completeness_modulo_reviewed_equivalence_status": (
                "conditional-complete"
            ),
        }


TARGETS = (
    AddressObserverTarget(
        target="core::slice::element_offset",
        input_order="39",
        artifact_id="039_core_slice_element_offset",
        kind="element",
        active_contract_sha256=(
            "6cb1971fc22b193456b858636b8e9d6ed1874cc9b7b9352f94eea2cf2a66960b"
        ),
        active_contract_text=(
            "pub assume_specification<T>[ <[T]>::element_offset ]( "
            "slice: &[T], element: &T, ) -> (ret: Option<usize>) ensures "
            "slice_element_offset_option_result(slice@, element, ret), ;"
        ),
        generated_declaration_sha256=(
            "d4c94c080a707b9a5d5bd01bd9076d582d1a3a54eb7a2327eb4e22fbd40845f6"
        ),
        source_start=5260,
        source_end=5277,
        source_item_sha256=(
            "2e1c40be6fe7b5b51032b7132000aa531f27957039e0545dee3811b6d36ad61a"
        ),
        docs_start=5222,
        docs_end=5257,
        public_docs_sha256=(
            "30ee6b398b71e14e84ab729f121cc2113bfb72e34d86f3fd91a6ac51a8e1f283"
        ),
        harness_sha256=(
            "fe56fa23d91ad8aff79dd80b1173f8338a49ce5690d8d5997a9601722bbf45e8"
        ),
        source_body_manifest_sha256=(
            "faf8660e4ef802d23ee53ac6ca5a9e8989e730f38978739411a377b5df426f8d"
        ),
        transformation_manifest_sha256=(
            "efbfe159b28ca6efaf93c68bbcf064d9a3ae4000a58c8a035ff5209bfb704069"
        ),
        dependency_manifest_sha256=(
            "02d43f3296572d4f45ae24db609e9e4d9c57993fc5fdcf20e24aa1a91cf7708b"
        ),
        trust_record_sha256=(
            ("TS-039-D001", "3c638be37dae5b2c68d30d94b2fbe4ce78bfc34fe11ec1669250384d5d32da4d"),
            ("TS-039-D002", "30da9f541f9474f82445151c0bad27e92988cf20a2ca08252f61d534f642c9de"),
            ("TS-039-D003", "36fd5fe87bd38362979cec733e55d3fdbf28eef1920236bae6de0d0d8b56cc4c"),
            ("TS-039-D004", "1e0463727f470c6f414df18b439b76ea90a8ac0db0e33cac11b5868d4cfccfb5"),
            ("TS-039-D005", "3405ee733a1fe3ec4792e5a0e7d18663507bbc70942b018211351caf0ea29000"),
            ("TS-039-D006", "17f02cd9026355447c46403b61b3ea8a863c8cd33f1cd11480c262c470016cfa"),
            ("TS-039-C001", "447741ce67d6fd2ef46462a282df2019f96aa46280036d8e7de30b8eb3246cc7"),
            ("TS-039-C002", "338a016e0a5be58b02c54238254a539aadec59cffa29b666d760f29114853642"),
            ("TS-039-C003", "6e8b46e6755a117f1ba4d1be5882c114dc701939fc08908d4271d9ff83d7aa5c"),
            ("TS-039-E001", "f10ab3d229563271317815c11fcdb97d939308c76cb09d13a30e91d8e75c6c2e"),
            ("TS-039-E002", "663ce172797379919a2efac223ed262d7f15d8888fd989e490e9c9c1ff2a507c"),
            ("TS-039-E003", "8b62a96f96d9305b6ae9a4ce2e94214db2820e94835d22e380a29769b5e3c852"),
            ("TS-039-E004", "97532fee27f092f3b5ff87e15921e42c283e1475f8cca1806610713bc195ca83"),
            ("TS-039-E005", "779ef84f2ee9cb8e973d96df8fb7829978a38c2f45c6f9ebc6307895a30d69bb"),
        ),
        source_fragments=(
            "if T::IS_ZST",
            "let self_start = self.as_ptr().addr();",
            "let elem_start = ptr::from_ref(element).addr();",
            "elem_start.wrapping_sub(self_start)",
            "byte_offset.is_multiple_of(size_of::<T>())",
            "byte_offset / size_of::<T>()",
            "if offset < self.len()",
        ),
        docs_fragments=(
            "Returns the index that an element reference points to.",
            "does not point to the start of an element within the slice",
            "uses pointer arithmetic and **does not compare elements**",
            "Panics if `T` is zero-sized.",
        ),
    ),
    AddressObserverTarget(
        target="core::slice::subslice_range",
        input_order="111",
        artifact_id="111_core_slice_subslice_range",
        kind="subslice",
        active_contract_sha256=(
            "efa221cefc2e3ffa897082292c658fd9163e1e151be34c08189360d0b01729bb"
        ),
        active_contract_text=(
            "pub assume_specification<T>[ <[T]>::subslice_range ]( "
            "slice: &[T], subslice: &[T], ) -> "
            "(ret: Option<core::range::Range<usize>>) ensures "
            "slice_subslice_range_option_result(slice@, subslice@, ret), ;"
        ),
        generated_declaration_sha256=(
            "c88fc80d677e29e5a2911e385b955122d3765a3b96f5e47504a7cd793ad224e6"
        ),
        source_start=5315,
        source_end=5337,
        source_item_sha256=(
            "a7deec2b313078cd2025212553c60d1578ed93aac7baa15a11c2749f97fd5421"
        ),
        docs_start=5279,
        docs_end=5312,
        public_docs_sha256=(
            "09f496da077aec0a201bf90a48a5e9e8a8b1f920eb4011fecda183d4b245fde3"
        ),
        harness_sha256=(
            "a146f50eddb3926853c4c17c18838063a647cb152fdee0b6e0cc940eb2b0d49c"
        ),
        source_body_manifest_sha256=(
            "381995b1450fd95956865d4ed37f0fc06178507a7037b4907cb4a80a5fbbf73c"
        ),
        transformation_manifest_sha256=(
            "72145732829e47d0051afe0fcd9dfc060445d65ec85d1d01cd7b8bc3796940b6"
        ),
        dependency_manifest_sha256=(
            "f6ef2d5982b62808440e3bfbe8ea024bbd01d17d8e00a1f2db7625be3b9caee1"
        ),
        trust_record_sha256=(
            ("TS-111-D001", "a4d149add9ade290fb978015609af57fdfb42595d8a23d8f0ef48bd1733b279b"),
            ("TS-111-D002", "21474c7707802d2d2f0b98371b550cc5361c87983ee10a34711666b6a8a16613"),
            ("TS-111-D003", "071a22ad7bb1b83c860536efcf76dcb17382e519f717ce7c57c11c67995a1aa1"),
            ("TS-111-D004", "694c929dc2717ccebbe04567097611072677f94509ae47b79b71d51ad29d6d2e"),
            ("TS-111-D005", "ebfd0e6a3326a6105df40f7a09ba8cbbebd9393eea52daccc18e84908419956c"),
            ("TS-111-D006", "4ad26a778906e159c3e12a9e011a167728a8e4eee4961fada6d9a136173b1601"),
            ("TS-111-C001", "f4f3cdacae57c8472517a7b737a081abd6861ce2a46b81f7980e005b207360ea"),
            ("TS-111-C002", "8fc7fd9de68b0215cd24ad9d68e70b4193203be3fb70f613fdd15c954b122b61"),
            ("TS-111-C003", "55c49ab8ea9667457219252f6604230e6feb2c7fffb23ae4229792686cdabce0"),
            ("TS-111-E001", "120f1f013bed866cfdcc8403f1def0615421180bcf7701f28fd5a952bdb4364e"),
            ("TS-111-E002", "1690ba7dd3625f77026eed1db6782348ab623f124272175f2e1c1e3ff5a1ac45"),
            ("TS-111-E003", "f709ca06f4d26465ed8d4f0989a88349a5fd9b0c448985d0c0fa9b5315b8b07d"),
            ("TS-111-E004", "1b7cbdb1cb8b80a9c8cbbd199225eab55c4d260573268c143de6498591123678"),
        ),
        source_fragments=(
            "if T::IS_ZST",
            "let self_start = self.as_ptr().addr();",
            "let subslice_start = subslice.as_ptr().addr();",
            "subslice_start.wrapping_sub(self_start)",
            "byte_start.is_multiple_of(size_of::<T>())",
            "byte_start / size_of::<T>()",
            "start.wrapping_add(subslice.len())",
            "Some(core::range::Range { start, end })",
        ),
        docs_fragments=(
            "Returns the range of indices that a subslice points to.",
            "does not point within the slice",
            "may return a false positive",
            "if `subslice` has a length of zero",
            "Panics if `T` is zero-sized.",
        ),
    ),
)

TARGET_BY_ARTIFACT = {config.artifact_id: config for config in TARGETS}
TARGET_KEYS = tuple((config.target, config.input_order) for config in TARGETS)

BOUNDARY_FIELDS = (
    ("b_receiver_address", "Int", "input_provenance"),
    ("b_receiver_allocation", "Int", "input_provenance"),
    ("b_receiver_provenance", "Int", "input_provenance"),
    ("b_receiver_allocation_base", "Int", "input_provenance"),
    ("b_receiver_allocation_bytes", "Int", "input_provenance"),
    ("b_receiver_alive", "Bool", "input_provenance"),
    ("b_subject_address", "Int", "input_provenance"),
    ("b_subject_allocation", "Int", "input_provenance"),
    ("b_subject_provenance", "Int", "input_provenance"),
    ("b_subject_allocation_base", "Int", "input_provenance"),
    ("b_subject_allocation_bytes", "Int", "input_provenance"),
    ("b_subject_alive", "Bool", "input_provenance"),
    ("b_element_size", "Int", "input_layout"),
    ("b_element_alignment", "Int", "input_layout"),
    ("b_usize_max", "Int", "input_layout"),
    ("b_isize_max", "Int", "input_layout"),
    ("b_memory_token", "Int", "input_memory"),
)


def canonical_json_sha256(record: dict[str, str]) -> str:
    payload = json.dumps(
        record, sort_keys=True, separators=(",", ":")
    ).encode()
    return hashlib.sha256(payload).hexdigest()


def _normalized(text: str) -> str:
    return " ".join(text.split())


def validate_source_anchors(
    config: AddressObserverTarget,
    source_item: str,
    public_docs: str,
    vocabulary: str,
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
                f"{config.target}: public documentation fragment absent: {fragment}"
            )
    vocabulary_fragments = (
        "pub uninterp spec fn slice_element_offset_result",
        "pub uninterp spec fn slice_element_in_domain",
        "pub open spec fn slice_element_offset_option_result",
    ) if config.kind == "element" else (
        "pub uninterp spec fn slice_subslice_range_result",
        "pub uninterp spec fn slice_subslice_in_domain",
        "pub open spec fn slice_subslice_range_option_result",
    )
    for fragment in vocabulary_fragments:
        if fragment not in vocabulary:
            raise GuardError(
                f"{config.target}: bound generated vocabulary is incomplete"
            )
    prohibited = (
        "TargetDefinition_T",
        "Equivalent_T",
        "assume_specification",
        "external_body",
    )
    if any(token in source_item for token in prohibited):
        raise GuardError(f"{config.target}: canonical source item is synthetic")


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


def _input_fields(
    config: AddressObserverTarget,
) -> tuple[tuple[str, str], ...]:
    fields: list[tuple[str, str]] = [
        ("x_receiver_length", "Int"),
    ]
    if config.kind == "subslice":
        fields.append(("x_subslice_length", "Int"))
    fields.append(("x_memory_token", "Int"))
    return tuple(fields)


def _state_declaration(purpose: str) -> str:
    if purpose == EXACT_OUTPUT:
        return "(declare-datatypes ((State 0)) (((mkState))))"
    return _datatype(
        "State",
        "mkState",
        (("s_final_memory_token", "Int"),),
    )


def _return_declaration(config: AddressObserverTarget) -> str:
    if config.kind == "element":
        return """\
(declare-datatypes ((ElementReturn 0))
  (((ElementPanicked)
    (ElementNone)
    (ElementSome (element_index Int)))))"""
    return """\
(declare-datatypes ((RangeReturn 0))
  (((RangePanicked)
    (RangeNone)
    (RangeSome (range_start Int) (range_end Int)))))"""


def _subject_length(config: AddressObserverTarget) -> str:
    return "1" if config.kind == "element" else "(x_subslice_length x)"


def _reference_definitions(config: AddressObserverTarget) -> str:
    subject_length = _subject_length(config)
    return f"""\
(define-fun MachineModulus ((b Boundary)) Int
  (+ (b_usize_max b) 1))
(define-fun ByteCount ((length Int) (b Boundary)) Int
  (* length (b_element_size b)))
(define-fun AllocationEnd ((base Int) (bytes Int)) Int
  (+ base bytes))
(define-fun AllocationRecordValid
  ((allocation Int) (provenance Int) (base Int) (bytes Int)
   (b Boundary)) Bool
  (and (>= allocation 0)
       (>= provenance 0)
       (>= base 0)
       (>= bytes 0)
       (<= (AllocationEnd base bytes) (b_usize_max b))
       (ite (= allocation 0)
            (and (= provenance 0) (= base 0) (= bytes 0))
            (> provenance 0))))
(define-fun ReferenceSpanValid
  ((length Int) (address Int) (allocation Int) (provenance Int)
   (base Int) (allocation_bytes Int) (alive Bool)
   (b Boundary)) Bool
  (and (>= length 0)
       (<= length (b_usize_max b))
       alive
       (> address 0)
       (<= address (b_usize_max b))
       (= (mod address (b_element_alignment b)) 0)
       (<= (ByteCount length b) (b_isize_max b))
       (<= (+ address (ByteCount length b)) (b_usize_max b))
       (AllocationRecordValid
         allocation provenance base allocation_bytes b)
       (ite (= (ByteCount length b) 0)
            (or
              (= allocation 0)
              (and (> allocation 0)
                   (<= base address)
                   (<= address (AllocationEnd base allocation_bytes))))
            (and (> allocation 0)
                 (> provenance 0)
                 (<= base address)
                 (<= (+ address (ByteCount length b))
                     (AllocationEnd base allocation_bytes))))))
(define-fun AllocationIdentityConsistent ((b Boundary)) Bool
  (and
    (=> (= (b_receiver_allocation b) (b_subject_allocation b))
        (and
          (= (b_receiver_provenance b) (b_subject_provenance b))
          (= (b_receiver_allocation_base b)
             (b_subject_allocation_base b))
          (= (b_receiver_allocation_bytes b)
             (b_subject_allocation_bytes b))))
    (=> (and (> (b_receiver_allocation b) 0)
             (> (b_subject_allocation b) 0)
             (not (= (b_receiver_allocation b)
                     (b_subject_allocation b))))
        (and
          (not (= (b_receiver_provenance b)
                  (b_subject_provenance b)))
          (or
            (= (b_receiver_allocation_bytes b) 0)
            (= (b_subject_allocation_bytes b) 0)
            (<=
              (AllocationEnd
                (b_receiver_allocation_base b)
                (b_receiver_allocation_bytes b))
              (b_subject_allocation_base b))
            (<=
              (AllocationEnd
                (b_subject_allocation_base b)
                (b_subject_allocation_bytes b))
              (b_receiver_allocation_base b)))))))
(define-fun LayoutAndPlatformValid ((x Input) (b Boundary)) Bool
  (and (>= (x_receiver_length x) 0)
       (<= (x_receiver_length x) (b_usize_max b))
       {("(>= (x_subslice_length x) 0)" if config.kind == "subslice" else "true")}
       {("(<= (x_subslice_length x) (b_usize_max b))" if config.kind == "subslice" else "true")}
       (>= (b_element_size b) 0)
       (> (b_element_alignment b) 0)
       (= (mod (b_element_size b) (b_element_alignment b)) 0)
       (> (b_usize_max b) 0)
       (> (b_isize_max b) 0)
       (= (b_usize_max b) (+ (* 2 (b_isize_max b)) 1))
       (= (b_memory_token b) (x_memory_token x))
       (>= (x_memory_token x) 0)))
(define-fun ReceiverAsPtrTransition ((x Input) (b Boundary)) Bool
  (ReferenceSpanValid
    (x_receiver_length x)
    (b_receiver_address b)
    (b_receiver_allocation b)
    (b_receiver_provenance b)
    (b_receiver_allocation_base b)
    (b_receiver_allocation_bytes b)
    (b_receiver_alive b)
    b))
(define-fun SubjectPointerTransition ((x Input) (b Boundary)) Bool
  (ReferenceSpanValid
    {subject_length}
    (b_subject_address b)
    (b_subject_allocation b)
    (b_subject_provenance b)
    (b_subject_allocation_base b)
    (b_subject_allocation_bytes b)
    (b_subject_alive b)
    b))
(define-fun InitialReferenceObservations
  ((x Input) (b Boundary)) Bool
  (and (LayoutAndPlatformValid x b)
       (ReceiverAsPtrTransition x b)
       (SubjectPointerTransition x b)
       (AllocationIdentityConsistent b)))
(define-fun ReceiverExposedAddress ((b Boundary)) Int
  (b_receiver_address b))
(define-fun SubjectExposedAddress ((b Boundary)) Int
  (b_subject_address b))
(define-fun WrappingByteOffset ((x Input) (b Boundary)) Int
  (mod (- (SubjectExposedAddress b) (ReceiverExposedAddress b))
       (MachineModulus b)))
(define-fun OffsetIsElementAligned ((x Input) (b Boundary)) Bool
  (and (> (b_element_size b) 0)
       (= (mod (WrappingByteOffset x b) (b_element_size b)) 0)))
(define-fun ComputedStart ((x Input) (b Boundary)) Int
  (div (WrappingByteOffset x b) (b_element_size b)))
"""


def _element_contract_definitions() -> str:
    return """\
(define-fun ElementInDomainTransition ((x Input) (b Boundary)) Bool
  (and (OffsetIsElementAligned x b)
       (< (ComputedStart x b) (x_receiver_length x))))
(define-fun ElementOffsetResultTransition
  ((x Input) (b Boundary) (index Int)) Bool
  (and (ElementInDomainTransition x b)
       (= index (ComputedStart x b))))
(define-fun ElementOptionConstruction
  ((x Input) (b Boundary) (ret ElementReturn)) Bool
  (and
    (not ((_ is ElementPanicked) ret))
    (=>
      ((_ is ElementSome) ret)
      (and
        (< (element_index ret) (x_receiver_length x))
        (ElementInDomainTransition x b)
        (ElementOffsetResultTransition x b (element_index ret))))
    (=>
      ((_ is ElementNone) ret)
      (not (ElementInDomainTransition x b)))))
"""


def _subslice_contract_definitions() -> str:
    return """\
(define-fun WrappingRangeEnd ((x Input) (b Boundary)) Int
  (mod (+ (ComputedStart x b) (x_subslice_length x))
       (MachineModulus b)))
(define-fun SubsliceInDomainTransition ((x Input) (b Boundary)) Bool
  (and (OffsetIsElementAligned x b)
       (<= (ComputedStart x b) (x_receiver_length x))
       (<= (WrappingRangeEnd x b) (x_receiver_length x))))
(define-fun SubsliceRangeResultTransition
  ((x Input) (b Boundary) (start Int) (end Int)) Bool
  (and (SubsliceInDomainTransition x b)
       (= start (ComputedStart x b))
       (= end (WrappingRangeEnd x b))))
(define-fun RangeOptionConstruction
  ((x Input) (b Boundary) (ret RangeReturn)) Bool
  (and
    (not ((_ is RangePanicked) ret))
    (=>
      ((_ is RangeSome) ret)
      (and
        (SubsliceRangeResultTransition
          x b (range_start ret) (range_end ret))
        (<= (x_subslice_length x) (x_receiver_length x))))
    (=>
      ((_ is RangeNone) ret)
      (not (SubsliceInDomainTransition x b)))))
"""


def _target_transition(
    config: AddressObserverTarget,
    purpose: str,
) -> str:
    if config.kind == "element":
        option = """\
(ite (= (b_element_size b) 0)
            (= (y_return y) ElementPanicked)
            (ElementOptionConstruction x b (y_return y)))"""
    else:
        option = """\
(ite (= (b_element_size b) 0)
            (= (y_return y) RangePanicked)
            (RangeOptionConstruction x b (y_return y)))"""
    state = (
        "true"
        if purpose == EXACT_OUTPUT
        else "(= (s_final_memory_token s) (x_memory_token x))"
    )
    return f"""\
(define-fun AddressObserverContractTransition
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and (InitialReferenceObservations x b)
       {option}
       {state}))
"""


def _requires_body(config: AddressObserverTarget) -> str:
    clauses = [
        "(>= (x_receiver_length x) 0)",
        "(>= (x_memory_token x) 0)",
    ]
    if config.kind == "subslice":
        clauses.insert(1, "(>= (x_subslice_length x) 0)")
    return "  (and " + "\n       ".join(clauses) + ")"


def _equivalence_body(purpose: str) -> str:
    clauses = ["(= (y_return y1) (y_return y2))"]
    if purpose == PRIMARY:
        clauses.append(
            "(= (s_final_memory_token s1) (s_final_memory_token s2))"
        )
    return "  (and " + "\n       ".join(clauses) + "))"


def model_text(config: AddressObserverTarget, purpose: str) -> str:
    if purpose not in PURPOSES:
        raise ValueError(f"{config.target}: unknown purpose {purpose}")
    boundary_fields = tuple(
        (selector, sort) for selector, sort, _ in BOUNDARY_FIELDS
    )
    contract = (
        _element_contract_definitions()
        if config.kind == "element"
        else _subslice_contract_definitions()
    )
    return f"""\
; Target: {config.target}
; Active contract SHA-256: {config.active_contract_sha256}
; Purpose: {purpose}
; The boundary has only initial reference representation, memory, liveness,
; allocation/provenance, layout, and machine-width observations.
(set-logic ALL)
{_return_declaration(config)}
{_datatype("Input", "mkInput", _input_fields(config))}
{_datatype("Boundary", "mkBoundary", boundary_fields)}
{_datatype("Output", "mkOutput", (("y_return", config.output_sort),))}
{_state_declaration(purpose)}
(declare-const x Input)
(declare-const b Boundary)
(declare-const y1 Output)
(declare-const s1 State)
(declare-const y2 Output)
(declare-const s2 State)
{_reference_definitions(config)}
{contract}
{_target_transition(config, purpose)}
(define-fun Requires_T ((x Input)) Bool
{_requires_body(config)})
(define-fun Boundary_T ((x Input) (b Boundary)) Bool
  (InitialReferenceObservations x b))
(define-fun TargetDefinition_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (AddressObserverContractTransition x b y s))
(define-fun Spec_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (TargetDefinition_T x b y s))
(define-fun Equivalent_T
  ((x Input) (b Boundary)
   (y1 Output) (s1 State) (y2 Output) (s2 State)) Bool
{_equivalence_body(purpose)}
"""


def obligation_text(config: AddressObserverTarget, purpose: str) -> str:
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


def _field_trust_sites(
    config: AddressObserverTarget,
    selector: str,
) -> list[str]:
    prefix = f"TS-{int(config.input_order):03d}"
    if selector.startswith("b_subject_"):
        if config.kind == "element":
            return [f"{prefix}-D004", f"{prefix}-E002"]
        return [f"{prefix}-D002"]
    if selector in {
        "b_element_size",
        "b_element_alignment",
        "b_usize_max",
        "b_isize_max",
    }:
        return [f"{prefix}-D003", f"{prefix}-D005", f"{prefix}-E001"]
    return [f"{prefix}-D002"]


def _boundary_metadata(
    config: AddressObserverTarget,
) -> list[dict[str, Any]]:
    replacement_backed = {
        "b_receiver_address",
        "b_subject_address",
        "b_element_size",
        "b_element_alignment",
        "b_usize_max",
        "b_isize_max",
    }
    citations = [
        config.source_reference,
        config.docs_reference,
        "core/src/slice/mod.rs:726-728",
        "Rust 1.96 reference validity invariants for &[T] and &T",
    ]
    return [
        {
            "selector": selector,
            "role": role,
            "source_citations": citations,
            "trust_site_ids": _field_trust_sites(config, selector),
            "source_backed_replacement_ids": (
                [config.replacement_id]
                if selector in replacement_backed
                else []
            ),
        }
        for selector, _, role in BOUNDARY_FIELDS
    ]


def _principal_observations(
    config: AddressObserverTarget,
    purpose: str,
) -> list[dict[str, str]]:
    observations = [
        {
            "selector": "y_return",
            "left": "output1",
            "right": "output2",
            "sort": config.output_sort,
        }
    ]
    if purpose == PRIMARY:
        observations.append(
            {
                "selector": "s_final_memory_token",
                "left": "state1",
                "right": "state2",
                "sort": "Int",
            }
        )
    return observations


def obligation_metadata(
    config: AddressObserverTarget,
    purpose: str,
) -> dict[str, Any]:
    if purpose not in PURPOSES:
        raise ValueError(f"{config.target}: unknown purpose {purpose}")
    source_flow = [
        "extract the receiver thin pointer with allocation and provenance",
        (
            "apply ptr::from_ref to the element reference"
            if config.kind == "element"
            else "extract the subslice thin pointer"
        ),
        "observe both exposed addresses",
        "perform machine-usize wrapping subtraction",
        "test byte-offset divisibility by size_of::<T>()",
        "divide the aligned byte offset into an element start",
    ]
    if config.kind == "subslice":
        source_flow.append(
            "perform machine-usize wrapping addition for the range end"
        )
    source_flow.extend(
        [
            "apply the exact Rust bounds decisions",
            "construct panic, None, or Some with the computed scalar fields",
            "preserve the initial memory token because the target is read-only",
        ]
    )
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
                "none beyond Rust reference/type validity; nonnegative Int "
                "encodings are the only Requires_T clauses"
            ),
            "zst": (
                "valid zero-sized references are included and deterministically "
                "take the documented panic path before address division"
            ),
            "addressing": (
                "all exposed addresses are machine-usize values; subtraction "
                "and the subslice end addition use modulus usize::MAX + 1"
            ),
            "allocation": (
                "valid references are live, aligned, non-null, non-wrapping, "
                "and contained in one allocation when their byte span is nonzero"
            ),
        },
        "contract_translation": {
            "active_contract_preserved": True,
            "normal_return_relation": (
                "ElementOptionConstruction"
                if config.kind == "element"
                else "RangeOptionConstruction"
            ),
            "opaque_relations_replaced_by": (
                [
                    "ElementInDomainTransition",
                    "ElementOffsetResultTransition",
                ]
                if config.kind == "element"
                else [
                    "SubsliceInDomainTransition",
                    "SubsliceRangeResultTransition",
                ]
            ),
            "source_flow": source_flow,
            "canonical_answer_conjoined_outside_active_contract": False,
        },
        "boundary_scope": {
            "shared_observations": [
                "initial memory identity token",
                "receiver and subject addresses, allocations, and provenance",
                "allocation bases/extents and liveness",
                "element size/alignment and usize/isize platform limits",
            ],
            "excluded_observations": [
                "computed byte offset, element offset, or range",
                "alignment or bounds branch truth",
                "panic/None/Some output",
                "final state or an equivalent answer encoding",
                "selected or complete target trace",
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
                    "Rust 1.96 pointer extraction, ptr::from_ref where "
                    "applicable, exposed-address observation, usize wrapping "
                    "arithmetic, alignment, division, bounds, ZST panic, and "
                    "Option construction"
                ),
                "symbols": ["AddressObserverContractTransition"],
                "source_citations": [
                    config.source_reference,
                    config.docs_reference,
                ],
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
        "source_transition_definitions": [
            "AddressObserverContractTransition"
        ],
        "source_semantics": [
            "ReceiverAsPtrTransition",
            "SubjectPointerTransition",
            "ReceiverExposedAddress",
            "SubjectExposedAddress",
            "WrappingByteOffset",
            "OffsetIsElementAligned",
            "ComputedStart",
            (
                "ElementOptionConstruction"
                if config.kind == "element"
                else "WrappingRangeEnd"
            ),
            (
                "ElementInDomainTransition"
                if config.kind == "element"
                else "SubsliceInDomainTransition"
            ),
            (
                "ElementOffsetResultTransition"
                if config.kind == "element"
                else "SubsliceRangeResultTransition"
            ),
            (
                "ElementOptionConstruction"
                if config.kind == "element"
                else "RangeOptionConstruction"
            ),
        ],
        "principal_observations": _principal_observations(config, purpose),
        "equivalence_kind": "exact",
        "equivalence_review": {
            "principal_return": "exact algebraic panic/None/Some equality",
            "final_state": (
                "not projected by exact-output obligation"
                if purpose == EXACT_OUTPUT
                else "exact final memory-token equality"
            ),
            "weakened_observations": [],
        },
    }


def obligation(
    config: AddressObserverTarget,
    purpose: str,
) -> tuple[str, dict[str, Any]]:
    return obligation_text(config, purpose), obligation_metadata(config, purpose)


def validate_target_obligation(
    config: AddressObserverTarget,
    text: str,
    metadata: dict[str, Any],
) -> None:
    purpose = metadata.get("obligation_purpose")
    if purpose not in PURPOSES:
        raise GuardError(f"{config.target}: invalid obligation purpose")
    if text != obligation_text(config, purpose):
        raise GuardError(f"{config.target}: reviewed SMT text changed")
    if metadata != obligation_metadata(config, purpose):
        raise GuardError(f"{config.target}: reviewed obligation metadata changed")
    if "(declare-fun" in text:
        raise GuardError(f"{config.target}: opaque functionality relation present")
    prohibited = (
        "b_computed",
        "b_offset",
        "b_range",
        "b_branch",
        "b_output",
        "b_result",
        "b_final",
        "b_trace",
        "CanonicalAnswer",
    )
    if any(token in text for token in prohibited):
        raise GuardError(f"{config.target}: answer-bearing boundary/model field")
    required = (
        "ReceiverAsPtrTransition",
        "SubjectPointerTransition",
        "WrappingByteOffset",
        "OffsetIsElementAligned",
        "ComputedStart",
        "AddressObserverContractTransition",
    )
    if any(token not in text for token in required):
        raise GuardError(f"{config.target}: source transition is incomplete")
    if config.kind == "element":
        required_target = (
            "ElementInDomainTransition",
            "ElementOffsetResultTransition",
            "ElementOptionConstruction",
            "ElementPanicked",
        )
    else:
        required_target = (
            "WrappingRangeEnd",
            "SubsliceInDomainTransition",
            "SubsliceRangeResultTransition",
            "RangeOptionConstruction",
            "RangePanicked",
        )
    if any(token not in text for token in required_target):
        raise GuardError(f"{config.target}: target-specific transition incomplete")
    validate_obligation(text, metadata)


def boundary_manifest(config: AddressObserverTarget) -> dict[str, Any]:
    return {
        "schema_version": 2,
        "target": config.target,
        "input_order": config.input_order,
        "active_contract_sha256": config.active_contract_sha256,
        "boundary_narrower_than_target": True,
        "proof_boundary_assumption": (
            "Both executions share x and exactly one Boundary_T containing only "
            "initial memory identity, exposed reference addresses, allocation "
            "identity/extents, provenance, liveness, element layout, and "
            "machine usize/isize limits. All offsets, ranges, branches, "
            "outcomes, final state, and traces are derived after the boundary."
        ),
        "shared_boundary_observations": [
            {
                "fields": ["b_memory_token"],
                "kind": "initial memory identity",
            },
            {
                "fields": [
                    "b_receiver_address",
                    "b_receiver_allocation",
                    "b_receiver_provenance",
                    "b_receiver_allocation_base",
                    "b_receiver_allocation_bytes",
                    "b_receiver_alive",
                    "b_subject_address",
                    "b_subject_allocation",
                    "b_subject_provenance",
                    "b_subject_allocation_base",
                    "b_subject_allocation_bytes",
                    "b_subject_alive",
                ],
                "kind": "initial reference, allocation, provenance, and liveness",
            },
            {
                "fields": [
                    "b_element_size",
                    "b_element_alignment",
                    "b_usize_max",
                    "b_isize_max",
                ],
                "kind": "type layout and platform limits",
            },
        ],
        "deterministic_source_transitions": {
            "pointer_extraction": (
                "receiver as_ptr and "
                + (
                    "ptr::from_ref(element)"
                    if config.kind == "element"
                    else "subslice as_ptr"
                )
            ),
            "address_arithmetic": (
                "exposed addresses; wrapping_sub; divisibility; division"
                + (
                    ""
                    if config.kind == "element"
                    else "; wrapping_add range end"
                )
            ),
            "decision_and_construction": (
                "documented ZST panic followed by exact alignment/bounds "
                "decisions and algebraic None/Some construction"
            ),
            "state": "read-only target preserves initial memory identity",
        },
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
            "computed byte offset, element offset, start, or end",
            "alignment, bounds, or panic branch truth",
            "panic/None/Some output or an equivalent encoding",
            "final memory/state",
            "selected or complete execution trace",
        ],
    }


def base_case(config: AddressObserverTarget) -> dict[str, Any]:
    return {
        "receiver_length": 4,
        "subject_length": 1 if config.kind == "element" else 2,
        "memory_token": 9,
        "receiver_address": 64,
        "receiver_allocation": 1,
        "receiver_provenance": 11,
        "receiver_allocation_base": 32,
        "receiver_allocation_bytes": 128,
        "receiver_alive": True,
        "subject_address": 72 if config.kind == "element" else 68,
        "subject_allocation": 1,
        "subject_provenance": 11,
        "subject_allocation_base": 32,
        "subject_allocation_bytes": 128,
        "subject_alive": True,
        "element_size": 4,
        "element_alignment": 4,
        "usize_max": 255,
        "isize_max": 127,
    }


def _same_allocation(
    case: dict[str, Any],
    *,
    receiver_address: int | None = None,
) -> dict[str, Any]:
    result = dict(case)
    if receiver_address is not None:
        result["receiver_address"] = receiver_address
    result.update(
        {
            "subject_allocation": result["receiver_allocation"],
            "subject_provenance": result["receiver_provenance"],
            "subject_allocation_base": result["receiver_allocation_base"],
            "subject_allocation_bytes": result["receiver_allocation_bytes"],
        }
    )
    return result


def source_cases(
    config: AddressObserverTarget,
) -> dict[str, dict[str, Any]]:
    base = base_case(config)
    if config.kind == "element":
        return {
            "same_allocation_start": {
                **_same_allocation(base),
                "subject_address": 64,
            },
            "same_allocation_interior": dict(base),
            "distinct_allocation": {
                **base,
                "subject_address": 176,
                "subject_allocation": 2,
                "subject_provenance": 22,
                "subject_allocation_base": 176,
                "subject_allocation_bytes": 32,
            },
            "element_stride_misalignment": {
                **_same_allocation(base),
                "receiver_length": 3,
                "subject_address": 68,
                "element_size": 8,
                "element_alignment": 4,
            },
            "pointer_before_receiver_wrapping": {
                **_same_allocation(base, receiver_address=128),
                "receiver_length": 3,
                "subject_address": 124,
            },
            "exact_end": {
                **_same_allocation(base),
                "receiver_length": 3,
                "subject_address": 76,
            },
            "out_of_bounds_after_end": {
                **_same_allocation(base),
                "receiver_length": 3,
                "subject_address": 80,
            },
            "usize_wrapping_limit": {
                **_same_allocation(base, receiver_address=240),
                "receiver_length": 3,
                "subject_address": 236,
                "receiver_allocation_base": 160,
                "receiver_allocation_bytes": 95,
                "subject_allocation_base": 160,
                "subject_allocation_bytes": 95,
            },
            "zst_panic": {
                **base,
                "receiver_address": 8,
                "receiver_allocation": 0,
                "receiver_provenance": 0,
                "receiver_allocation_base": 0,
                "receiver_allocation_bytes": 0,
                "subject_address": 8,
                "subject_allocation": 0,
                "subject_provenance": 0,
                "subject_allocation_base": 0,
                "subject_allocation_bytes": 0,
                "element_size": 0,
                "element_alignment": 8,
            },
        }
    return {
        "same_allocation_full": {
            **_same_allocation(base),
            "subject_address": 64,
            "subject_length": 4,
        },
        "same_allocation_interior": dict(base),
        "same_allocation_empty_start": {
            **_same_allocation(base),
            "subject_address": 64,
            "subject_length": 0,
        },
        "same_allocation_empty_end": {
            **_same_allocation(base),
            "subject_address": 80,
            "subject_length": 0,
        },
        "distinct_allocation_nonempty": {
            **base,
            "subject_address": 176,
            "subject_length": 1,
            "subject_allocation": 2,
            "subject_provenance": 22,
            "subject_allocation_base": 176,
            "subject_allocation_bytes": 32,
        },
        "element_stride_misalignment": {
            **_same_allocation(base),
            "receiver_length": 3,
            "subject_address": 68,
            "subject_length": 1,
            "element_size": 8,
            "element_alignment": 4,
        },
        "pointer_before_receiver_wrapping": {
            **_same_allocation(base, receiver_address=128),
            "receiver_length": 3,
            "subject_address": 124,
            "subject_length": 1,
        },
        "exact_end_nonempty": {
            **_same_allocation(base),
            "receiver_length": 3,
            "subject_address": 76,
            "subject_length": 1,
        },
        "out_of_bounds_after_end": {
            **_same_allocation(base),
            "receiver_length": 3,
            "subject_address": 80,
            "subject_length": 1,
        },
        "separate_empty_false_positive_start": {
            **base,
            "subject_address": 64,
            "subject_length": 0,
            "subject_allocation": 2,
            "subject_provenance": 22,
            "subject_allocation_base": 64,
            "subject_allocation_bytes": 0,
        },
        "separate_empty_false_positive_end": {
            **base,
            "subject_address": 80,
            "subject_length": 0,
            "subject_allocation": 2,
            "subject_provenance": 22,
            "subject_allocation_base": 80,
            "subject_allocation_bytes": 0,
        },
        "usize_limit_valid_no_wrap": {
            **_same_allocation(base, receiver_address=32),
            "receiver_length": 100,
            "subject_address": 100,
            "subject_length": 32,
            "receiver_allocation_base": 16,
            "receiver_allocation_bytes": 200,
            "subject_allocation_base": 16,
            "subject_allocation_bytes": 200,
            "element_size": 1,
            "element_alignment": 1,
        },
        "zst_panic": {
            **base,
            "receiver_address": 8,
            "receiver_allocation": 0,
            "receiver_provenance": 0,
            "receiver_allocation_base": 0,
            "receiver_allocation_bytes": 0,
            "subject_address": 8,
            "subject_allocation": 0,
            "subject_provenance": 0,
            "subject_allocation_base": 0,
            "subject_allocation_bytes": 0,
            "element_size": 0,
            "element_alignment": 8,
        },
    }


def evaluate_source(
    config: AddressObserverTarget,
    case: dict[str, Any],
) -> dict[str, Any]:
    if int(case["element_size"]) == 0:
        return {
            "kind": "panic",
            "byte_offset": None,
            "start": None,
            "end": None,
        }
    modulus = int(case["usize_max"]) + 1
    byte_offset = (
        int(case["subject_address"]) - int(case["receiver_address"])
    ) % modulus
    size = int(case["element_size"])
    if byte_offset % size:
        return {
            "kind": "none",
            "byte_offset": byte_offset,
            "start": None,
            "end": None,
        }
    start = byte_offset // size
    receiver_length = int(case["receiver_length"])
    if config.kind == "element":
        return {
            "kind": "some" if start < receiver_length else "none",
            "byte_offset": byte_offset,
            "start": start if start < receiver_length else None,
            "end": None,
        }
    end = (start + int(case["subject_length"])) % modulus
    in_bounds = start <= receiver_length and end <= receiver_length
    return {
        "kind": "some" if in_bounds else "none",
        "byte_offset": byte_offset,
        "start": start if in_bounds else None,
        "end": end if in_bounds else None,
    }


def _input_expression(
    config: AddressObserverTarget,
    case: dict[str, Any],
) -> str:
    values = [case["receiver_length"]]
    if config.kind == "subslice":
        values.append(case["subject_length"])
    values.append(case["memory_token"])
    return "(mkInput " + " ".join(map(str, values)) + ")"


def _boundary_expression(
    case: dict[str, Any],
    *,
    memory_mismatch: bool = False,
) -> str:
    values = [
        case["receiver_address"],
        case["receiver_allocation"],
        case["receiver_provenance"],
        case["receiver_allocation_base"],
        case["receiver_allocation_bytes"],
        str(bool(case["receiver_alive"])).lower(),
        case["subject_address"],
        case["subject_allocation"],
        case["subject_provenance"],
        case["subject_allocation_base"],
        case["subject_allocation_bytes"],
        str(bool(case["subject_alive"])).lower(),
        case["element_size"],
        case["element_alignment"],
        case["usize_max"],
        case["isize_max"],
        int(case["memory_token"]) + (1 if memory_mismatch else 0),
    ]
    return "(mkBoundary " + " ".join(map(str, values)) + ")"


def _return_expression(
    config: AddressObserverTarget,
    outcome: dict[str, Any],
) -> str:
    if config.kind == "element":
        if outcome["kind"] == "panic":
            return "ElementPanicked"
        if outcome["kind"] == "none":
            return "ElementNone"
        return f"(ElementSome {outcome['start']})"
    if outcome["kind"] == "panic":
        return "RangePanicked"
    if outcome["kind"] == "none":
        return "RangeNone"
    return f"(RangeSome {outcome['start']} {outcome['end']})"


def source_instance_text(
    config: AddressObserverTarget,
    name: str,
) -> str:
    try:
        case = source_cases(config)[name]
    except KeyError as exc:
        raise ValueError(f"{config.target}: unknown source case {name}") from exc
    expected = _return_expression(config, evaluate_source(config, case))
    state_query = " (s_final_memory_token s1)"
    return model_text(config, PRIMARY) + f"""\
(assert (= x {_input_expression(config, case)}))
(assert (= b {_boundary_expression(case)}))
(assert (Requires_T x))
(assert (Boundary_T x b))
(assert (Spec_T x b y1 s1))
(assert (= (y_return y1) {expected}))
(check-sat)
(get-value (
  (y_return y1){state_query}
  (WrappingByteOffset x b)
  (ComputedStart x b)))
"""


INVALID_PROBES = (
    "invalid_null_receiver",
    "invalid_null_subject",
    "invalid_pointer_alignment",
    "invalid_dead_receiver",
    "invalid_dead_subject",
    "invalid_span_wrap",
    "invalid_isize_span",
    "invalid_allocation_overlap",
    "invalid_platform_width",
    "invalid_length_usize",
    "invalid_nonzero_dangling_subject",
    "boundary_memory_mismatch",
)

ELEMENT_SEMANTIC_PROBES = (
    "wrong_same_allocation_index",
    "wrong_same_allocation_none",
    "wrong_distinct_allocation_some",
    "wrong_stride_misalignment_some",
    "wrong_pointer_before_wrapping_some",
    "wrong_exact_end_some",
    "wrong_out_of_bounds_some",
    "wrong_usize_limit_some",
    "wrong_zst_normal_return",
    "wrong_final_state",
)

SUBSLICE_SEMANTIC_PROBES = (
    "wrong_interior_range",
    "wrong_interior_none",
    "wrong_distinct_allocation_some",
    "wrong_stride_misalignment_some",
    "wrong_pointer_before_wrapping_some",
    "wrong_exact_end_some",
    "wrong_out_of_bounds_some",
    "wrong_false_positive_start_none",
    "wrong_false_positive_end_none",
    "wrong_usize_limit_range",
    "wrong_zst_normal_return",
    "wrong_final_state",
)


def negative_probe_names(
    config: AddressObserverTarget,
) -> tuple[str, ...]:
    return INVALID_PROBES + (
        ELEMENT_SEMANTIC_PROBES
        if config.kind == "element"
        else SUBSLICE_SEMANTIC_PROBES
    )


def _invalid_case(
    config: AddressObserverTarget,
    name: str,
) -> tuple[dict[str, Any], bool]:
    case = base_case(config)
    memory_mismatch = False
    if name == "invalid_null_receiver":
        case["receiver_address"] = 0
    elif name == "invalid_null_subject":
        case["subject_address"] = 0
    elif name == "invalid_pointer_alignment":
        case["subject_address"] = 70
    elif name == "invalid_dead_receiver":
        case["receiver_alive"] = False
    elif name == "invalid_dead_subject":
        case["subject_alive"] = False
    elif name == "invalid_span_wrap":
        case.update(
            receiver_address=252,
            receiver_length=2,
            receiver_allocation_base=200,
            receiver_allocation_bytes=55,
            subject_allocation_base=200,
            subject_allocation_bytes=55,
        )
    elif name == "invalid_isize_span":
        case.update(
            receiver_length=40,
            receiver_allocation_bytes=200,
            subject_allocation_bytes=200,
        )
    elif name == "invalid_allocation_overlap":
        case.update(
            subject_address=64,
            subject_allocation=2,
            subject_provenance=22,
            subject_allocation_base=64,
            subject_allocation_bytes=16,
        )
    elif name == "invalid_platform_width":
        case["isize_max"] = 126
    elif name == "invalid_length_usize":
        case["receiver_length"] = 256
    elif name == "invalid_nonzero_dangling_subject":
        case.update(
            subject_allocation=0,
            subject_provenance=0,
            subject_allocation_base=0,
            subject_allocation_bytes=0,
        )
    elif name == "boundary_memory_mismatch":
        memory_mismatch = True
    else:
        raise ValueError(f"{config.target}: unknown invalid probe {name}")
    return case, memory_mismatch


def _semantic_probe(
    config: AddressObserverTarget,
    name: str,
) -> tuple[dict[str, Any], str | None]:
    cases = source_cases(config)
    if config.kind == "element":
        mapping = {
            "wrong_same_allocation_index": (
                "same_allocation_interior",
                "(ElementSome 1)",
            ),
            "wrong_same_allocation_none": (
                "same_allocation_interior",
                "ElementNone",
            ),
            "wrong_distinct_allocation_some": (
                "distinct_allocation",
                "(ElementSome 0)",
            ),
            "wrong_stride_misalignment_some": (
                "element_stride_misalignment",
                "(ElementSome 0)",
            ),
            "wrong_pointer_before_wrapping_some": (
                "pointer_before_receiver_wrapping",
                "(ElementSome 0)",
            ),
            "wrong_exact_end_some": ("exact_end", "(ElementSome 0)"),
            "wrong_out_of_bounds_some": (
                "out_of_bounds_after_end",
                "(ElementSome 0)",
            ),
            "wrong_usize_limit_some": (
                "usize_wrapping_limit",
                "(ElementSome 0)",
            ),
            "wrong_zst_normal_return": ("zst_panic", "ElementNone"),
            "wrong_final_state": ("same_allocation_interior", None),
        }
    else:
        mapping = {
            "wrong_interior_range": (
                "same_allocation_interior",
                "(RangeSome 0 2)",
            ),
            "wrong_interior_none": (
                "same_allocation_interior",
                "RangeNone",
            ),
            "wrong_distinct_allocation_some": (
                "distinct_allocation_nonempty",
                "(RangeSome 0 1)",
            ),
            "wrong_stride_misalignment_some": (
                "element_stride_misalignment",
                "(RangeSome 0 1)",
            ),
            "wrong_pointer_before_wrapping_some": (
                "pointer_before_receiver_wrapping",
                "(RangeSome 0 1)",
            ),
            "wrong_exact_end_some": (
                "exact_end_nonempty",
                "(RangeSome 3 4)",
            ),
            "wrong_out_of_bounds_some": (
                "out_of_bounds_after_end",
                "(RangeSome 0 1)",
            ),
            "wrong_false_positive_start_none": (
                "separate_empty_false_positive_start",
                "RangeNone",
            ),
            "wrong_false_positive_end_none": (
                "separate_empty_false_positive_end",
                "RangeNone",
            ),
            "wrong_usize_limit_range": (
                "usize_limit_valid_no_wrap",
                "(RangeSome 68 99)",
            ),
            "wrong_zst_normal_return": ("zst_panic", "RangeNone"),
            "wrong_final_state": ("same_allocation_interior", None),
        }
    case_name, wrong = mapping[name]
    return cases[case_name], wrong


def negative_probe_text(
    config: AddressObserverTarget,
    name: str,
) -> str:
    if name not in negative_probe_names(config):
        raise ValueError(f"{config.target}: unknown negative probe {name}")
    if name in INVALID_PROBES:
        case, mismatch = _invalid_case(config, name)
        assertions = [
            f"(= x {_input_expression(config, case)})",
            f"(= b {_boundary_expression(case, memory_mismatch=mismatch)})",
            "(Requires_T x)",
            "(Boundary_T x b)",
        ]
    else:
        case, wrong_return = _semantic_probe(config, name)
        assertions = [
            f"(= x {_input_expression(config, case)})",
            f"(= b {_boundary_expression(case)})",
            "(Requires_T x)",
            "(Boundary_T x b)",
            "(Spec_T x b y1 s1)",
        ]
        if wrong_return is None:
            assertions.append(
                f"(not (= (s_final_memory_token s1) {case['memory_token']}))"
            )
        else:
            assertions.append(f"(= (y_return y1) {wrong_return})")
    body = "\n       ".join(assertions)
    return model_text(config, PRIMARY) + f"""\
(assert
  (and {body}))
(check-sat)
"""


def false_positive_assessment(config: AddressObserverTarget) -> dict[str, Any]:
    if config.kind != "subslice":
        raise ValueError("empty-subslice assessment belongs only to target 111")
    cases = source_cases(config)
    witnesses = []
    for name in (
        "separate_empty_false_positive_start",
        "separate_empty_false_positive_end",
    ):
        case = cases[name]
        outcome = evaluate_source(config, case)
        witnesses.append(
            {
                "case": name,
                "receiver_allocation": case["receiver_allocation"],
                "subslice_allocation": case["subject_allocation"],
                "allocations_distinct": (
                    case["receiver_allocation"]
                    != case["subject_allocation"]
                ),
                "subslice_length": case["subject_length"],
                "shared_numeric_address": case["subject_address"],
                "source_outcome": {
                    "kind": outcome["kind"],
                    "start": outcome["start"],
                    "end": outcome["end"],
                },
            }
        )
    return {
        "schema_version": 1,
        "target": config.target,
        "docs_reference": config.docs_reference,
        "finding": (
            "The documented false positives are deterministic address "
            "collisions, not multiple outcomes under one fixed boundary."
        ),
        "witnesses": witnesses,
        "exact_output_effect": "none; both executions return the same range",
        "full_state_effect": "none; the read-only frame is unchanged",
    }


def verus_text(config: AddressObserverTarget) -> str:
    subject_length = (
        "input.subject_length" if config.kind == "subslice" else "1"
    )
    end_definition = (
        "let end = (start + input.subject_length) % modulus;\n"
        "        if start <= input.receiver_length && "
        "end <= input.receiver_length {\n"
        "            Output { tag: 2, start, end }\n"
        "        } else {\n"
        "            Output { tag: 1, start: 0, end: 0 }\n"
        "        }"
        if config.kind == "subslice"
        else (
            "if start < input.receiver_length {\n"
            "            Output { tag: 2, start, end: 0 }\n"
            "        } else {\n"
            "            Output { tag: 1, start: 0, end: 0 }\n"
            "        }"
        )
    )
    return f"""\
use vstd::prelude::*;

verus! {{

pub struct Input {{
    pub receiver_length: int,
    pub subject_length: int,
    pub memory_token: int,
}}

pub struct Boundary {{
    pub receiver_address: int,
    pub subject_address: int,
    pub element_size: int,
    pub usize_max: int,
}}

pub struct Output {{
    pub tag: int,
    pub start: int,
    pub end: int,
}}

pub struct FinalState {{
    pub memory_token: int,
}}

pub open spec fn source_output(
    input: Input,
    boundary: Boundary,
) -> Output {{
    if boundary.element_size == 0 {{
        Output {{ tag: 0, start: 0, end: 0 }}
    }} else {{
        let modulus = boundary.usize_max + 1;
        let byte_offset =
            (boundary.subject_address - boundary.receiver_address) % modulus;
        if byte_offset % boundary.element_size != 0 {{
            Output {{ tag: 1, start: 0, end: 0 }}
        }} else {{
            let start = byte_offset / boundary.element_size;
            {end_definition}
        }}
    }}
}}

pub open spec fn target_transition(
    input: Input,
    boundary: Boundary,
    output: Output,
    state: FinalState,
) -> bool {{
    output.tag == source_output(input, boundary).tag
        && output.start == source_output(input, boundary).start
        && output.end == source_output(input, boundary).end
        && state.memory_token == input.memory_token
        && {subject_length} >= 0
}}

pub proof fn exact_output_conditional_complete(
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
        output1.tag == output2.tag,
        output1.start == output2.start,
        output1.end == output2.end,
{{
    reveal(target_transition);
}}

pub proof fn full_state_conditional_complete(
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
        output1.tag == output2.tag,
        output1.start == output2.start,
        output1.end == output2.end,
        state1.memory_token == state2.memory_token,
{{
    reveal(target_transition);
}}

}}
"""
