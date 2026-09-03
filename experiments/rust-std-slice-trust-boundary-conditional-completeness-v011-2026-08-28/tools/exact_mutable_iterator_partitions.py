#!/usr/bin/env python3
"""Source-backed exact-partition models for mutable Slice iterators."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from checker_guards import GuardError, parse_smt, validate_obligation


PRIMARY = "completeness-modulo-reviewed-equivalence"
EXACT_OUTPUT = "exact-output-determinism"
PURPOSES = (PRIMARY, EXACT_OUTPUT)

CANONICAL_ITER_PATH = "core/src/slice/iter.rs"
CANONICAL_ITER_SHA256 = (
    "c309e04ca3da2fc4220ee3f93b4466c578ea7f3f2ef52cca6a3fdf8ac28e53d3"
)
VOCABULARY_RANGES = ((793, 866),)


@dataclass(frozen=True)
class SourceCase:
    length: int
    chunk_size: int
    element_size: int
    assertions: tuple[str, ...] = ()


@dataclass(frozen=True)
class ExactPartitionTarget:
    target: str
    input_order: str
    artifact_id: str
    active_contract_sha256: str
    active_contract_text: str
    reverse: bool
    public_source_start: int
    public_source_end: int
    public_fragment: str
    private_source_start: int
    private_source_end: int
    private_fragments: tuple[str, ...]
    docs_reference: str
    all_trust_site_ids: tuple[str, ...]

    @property
    def source_reference(self) -> str:
        return (
            f"core/src/slice/mod.rs:{self.public_source_start}-"
            f"{self.public_source_end}"
        )

    @property
    def private_source_reference(self) -> str:
        return (
            f"{CANONICAL_ITER_PATH}:{self.private_source_start}-"
            f"{self.private_source_end}"
        )

    @property
    def private_source_filename(self) -> str:
        return f"{self.target.rsplit('::', 1)[-1]}_new.rs"

    @property
    def dependency_trust_site_ids(self) -> tuple[str, ...]:
        return tuple(site for site in self.all_trust_site_ids if "-D" in site)

    @property
    def context_only_trust_site_ids(self) -> tuple[str, ...]:
        return tuple(site for site in self.all_trust_site_ids if "-C" in site)

    @property
    def boundary_trust_site_ids(self) -> tuple[str, ...]:
        return (
            f"TS-{int(self.input_order):03d}-D001",
            f"TS-{int(self.input_order):03d}-D003",
        )

    @property
    def split_transition(self) -> str:
        return (
            "ReverseSplitAtRemainderTransition"
            if self.reverse
            else "ForwardSplitAtLengthMinusRemainderTransition"
        )

    @property
    def partition_transition(self) -> str:
        return (
            "ReverseExactPartitionTransition"
            if self.reverse
            else "ForwardExactPartitionTransition"
        )

    @property
    def source_transitions(self) -> tuple[str, ...]:
        return (
            "ModuloRemainderTransition",
            self.split_transition,
            self.partition_transition,
            "MutableRegionIdentityTransition",
            "DisjointMutableRegionsTransition",
            "PrivateConstructorStateTransition",
            "ImmediateFinalStateTransition",
        )

    @property
    def active_conjuncts(self) -> tuple[str, ...]:
        return (
            "ActiveSourceConjunct",
            "ActiveYieldedEmptyConjunct",
            "ActiveChunkSizeConjunct",
            "ActiveReverseConjunct",
            "ActiveChunkPartitionConjunct",
        )


TARGETS = (
    ExactPartitionTarget(
        target="core::slice::chunks_exact_mut",
        input_order="35",
        artifact_id="035_core_slice_chunks_exact_mut",
        active_contract_sha256=(
            "c4e09211e598b511902feb1f0fd0207e386dd8e7077da17462c9ba20c1944c68"
        ),
        active_contract_text=(
            "pub assume_specification<'a, T>[ <[T]>::chunks_exact_mut ]( "
            "slice: &'a mut [T], chunk_size: usize, ) -> (iter: "
            "core::slice::ChunksExactMut<'a, T>) requires chunk_size != 0, "
            "ensures slice_iterator_view::<core::slice::ChunksExactMut<'a, "
            "T>, T>(iter).source == old(slice)@, "
            "slice_iterator_view::<core::slice::ChunksExactMut<'a, T>, "
            "T>(iter).yielded_prefix == Seq::empty(), "
            "slice_iterator_view::<core::slice::ChunksExactMut<'a, T>, "
            "T>(iter).chunk_size == chunk_size as int, "
            "!slice_iterator_view::<core::slice::ChunksExactMut<'a, T>, "
            "T>(iter).reverse, slice_chunk_partition::<T>("
            "slice_iterator_view::<core::slice::ChunksExactMut<'a, T>, "
            "T>(iter)), ;"
        ),
        reverse=False,
        public_source_start=1290,
        public_source_end=1293,
        public_fragment="ChunksExactMut::new(self, chunk_size)",
        private_source_start=2028,
        private_source_end=2033,
        private_fragments=(
            "let rem = slice.len() % chunk_size;",
            "let fst_len = slice.len() - rem;",
            "slice.split_at_mut_unchecked(fst_len)",
            "Self { v: fst, rem: snd, chunk_size, _marker: PhantomData }",
        ),
        docs_reference="core/src/slice/mod.rs:1230-1289",
        all_trust_site_ids=(
            "TS-035-D001",
            "TS-035-D002",
            "TS-035-D003",
            "TS-035-D004",
            "TS-035-D005",
            "TS-035-C001",
        ),
    ),
    ExactPartitionTarget(
        target="core::slice::rchunks_exact_mut",
        input_order="68",
        artifact_id="068_core_slice_rchunks_exact_mut",
        active_contract_sha256=(
            "64f0260c2044e5b2b440a7c66eb354d3685862070f8ad8979838a571fbe47afe"
        ),
        active_contract_text=(
            "pub assume_specification<'a, T>[ <[T]>::rchunks_exact_mut ]( "
            "slice: &'a mut [T], chunk_size: usize, ) -> (iter: "
            "core::slice::RChunksExactMut<'a, T>) requires chunk_size != 0, "
            "ensures slice_iterator_view::<core::slice::RChunksExactMut<'a, "
            "T>, T>(iter).source == old(slice)@, "
            "slice_iterator_view::<core::slice::RChunksExactMut<'a, T>, "
            "T>(iter).yielded_prefix == Seq::empty(), "
            "slice_iterator_view::<core::slice::RChunksExactMut<'a, T>, "
            "T>(iter).chunk_size == chunk_size as int, "
            "slice_iterator_view::<core::slice::RChunksExactMut<'a, T>, "
            "T>(iter).reverse, slice_chunk_partition::<T>("
            "slice_iterator_view::<core::slice::RChunksExactMut<'a, T>, "
            "T>(iter)), ;"
        ),
        reverse=True,
        public_source_start=1824,
        public_source_end=1827,
        public_fragment="RChunksExactMut::new(self, chunk_size)",
        private_source_start=2844,
        private_source_end=2848,
        private_fragments=(
            "let rem = slice.len() % chunk_size;",
            "slice.split_at_mut_unchecked(rem)",
            "Self { v: snd, rem: fst, chunk_size }",
        ),
        docs_reference="core/src/slice/mod.rs:1763-1823",
        all_trust_site_ids=(
            "TS-068-D001",
            "TS-068-D002",
            "TS-068-D003",
            "TS-068-D004",
            "TS-068-D005",
            "TS-068-C001",
        ),
    ),
)

TARGET_BY_ARTIFACT = {target.artifact_id: target for target in TARGETS}
TARGET_BY_KEY = {
    (target.target, target.input_order): target for target in TARGETS
}
TARGET_KEYS = tuple(TARGET_BY_KEY)

SOURCE_CASES = {
    "empty": SourceCase(0, 3, 8),
    "unit_chunk": SourceCase(4, 1, 8),
    "shorter_than_chunk": SourceCase(2, 3, 8),
    "divisible": SourceCase(6, 3, 8),
    "nondivisible": SourceCase(7, 3, 8),
    "zst_equal_address_disjoint": SourceCase(
        5,
        3,
        0,
        (
            "(= (y_remaining_address y1) (y_remainder_address y1))",
            "(> (y_remaining_length y1) 0)",
            "(> (y_remainder_length y1) 0)",
            "(or (<= (+ (y_remaining_start y1) (y_remaining_length y1)) "
            "(y_remainder_start y1)) "
            "(<= (+ (y_remainder_start y1) (y_remainder_length y1)) "
            "(y_remaining_start y1)))",
        ),
    ),
}

NEGATIVE_PROBES = (
    "zero_chunk",
    "incorrect_modulo",
    "incorrect_split_index",
    "swapped_remainder_placement",
    "incorrect_concatenation_order",
    "provenance_loss",
    "borrow_loss",
    "zst_unequal_region_addresses",
)

INPUT_FIELDS = (
    ("x_source_sequence", "Int"),
    ("x_source_start", "Int"),
    ("x_length", "Int"),
    ("x_address", "Int"),
    ("x_allocation", "Int"),
    ("x_provenance", "Int"),
    ("x_borrow", "Int"),
    ("x_element_size", "Int"),
    ("x_chunk_size", "Int"),
)

BOUNDARY_FIELDS = (
    ("b_input_address", "Int"),
    ("b_input_allocation", "Int"),
    ("b_input_provenance", "Int"),
    ("b_input_borrow", "Int"),
    ("b_element_size", "Int"),
)

OUTPUT_FIELDS = (
    ("y_source_sequence", "Int"),
    ("y_source_start", "Int"),
    ("y_source_length", "Int"),
    ("y_source_address", "Int"),
    ("y_source_allocation", "Int"),
    ("y_source_provenance", "Int"),
    ("y_source_borrow", "Int"),
    ("y_remaining_sequence", "Int"),
    ("y_remaining_start", "Int"),
    ("y_remaining_length", "Int"),
    ("y_remaining_address", "Int"),
    ("y_remaining_allocation", "Int"),
    ("y_remaining_provenance", "Int"),
    ("y_remaining_parent_borrow", "Int"),
    ("y_yielded_sequence", "Int"),
    ("y_yielded_start", "Int"),
    ("y_yielded_length", "Int"),
    ("y_remainder_sequence", "Int"),
    ("y_remainder_start", "Int"),
    ("y_remainder_length", "Int"),
    ("y_remainder_address", "Int"),
    ("y_remainder_allocation", "Int"),
    ("y_remainder_provenance", "Int"),
    ("y_remainder_parent_borrow", "Int"),
    ("y_raw_v_address", "Int"),
    ("y_raw_v_length", "Int"),
    ("y_raw_v_allocation", "Int"),
    ("y_raw_v_provenance", "Int"),
    ("y_marker_borrow", "Int"),
    ("y_element_size", "Int"),
    ("y_chunk_size", "Int"),
    ("y_reverse", "Bool"),
    ("y_mod_remainder", "Int"),
    ("y_split_index", "Int"),
)

STATE_FIELDS = (
    ("s_backing_sequence", "Int"),
    ("s_backing_start", "Int"),
    ("s_backing_length", "Int"),
    ("s_backing_address", "Int"),
    ("s_backing_allocation", "Int"),
    ("s_backing_provenance", "Int"),
    ("s_backing_borrow", "Int"),
    ("s_element_size", "Int"),
    ("s_borrow_owned_by_iterator", "Bool"),
    ("s_elements_unchanged", "Bool"),
)


def _record_fields(fields: tuple[tuple[str, str], ...]) -> str:
    return "\n".join(f"      ({name} {sort})" for name, sort in fields)


def _normalized_source(text: str) -> str:
    return " ".join(text.split())


def validate_source_anchors(
    config: ExactPartitionTarget,
    public_source: str,
    private_source: str,
) -> None:
    public = _normalized_source(public_source)
    private = _normalized_source(private_source)
    if _normalized_source(config.public_fragment) not in public:
        raise GuardError(f"{config.target}: public constructor call changed")
    for fragment in config.private_fragments:
        if _normalized_source(fragment) not in private:
            raise GuardError(
                f"{config.target}: private constructor fragment changed: "
                f"{fragment}"
            )
    forbidden = (
        "slice_chunk_partition",
        "slice_iterator_view",
        "assume_specification",
    )
    if any(token in private for token in forbidden):
        raise GuardError(
            f"{config.target}: private source anchor repeats specification"
        )


def _input_identity() -> str:
    return """\
(define-fun InputIdentityObserved ((x Input) (b Boundary)) Bool
  (and (= (b_input_address b) (x_address x))
       (= (b_input_allocation b) (x_allocation x))
       (= (b_input_provenance b) (x_provenance x))
       (= (b_input_borrow b) (x_borrow x))
       (= (b_element_size b) (x_element_size x))))"""


def _modulo_transition() -> str:
    return """\
(define-fun ModuloRemainderTransition ((x Input) (y Output)) Bool
  (and (= (y_mod_remainder y) (mod (x_length x) (x_chunk_size x)))
       (>= (y_mod_remainder y) 0)
       (< (y_mod_remainder y) (x_chunk_size x))
       (<= (y_mod_remainder y) (x_length x))))"""


def _split_transition(config: ExactPartitionTarget) -> str:
    split = (
        "(y_mod_remainder y)"
        if config.reverse
        else "(- (x_length x) (y_mod_remainder y))"
    )
    return f"""\
(define-fun {config.split_transition} ((x Input) (y Output)) Bool
  (and (= (y_split_index y) {split})
       (>= (y_split_index y) 0)
       (<= (y_split_index y) (x_length x))))"""


def _partition_transition(config: ExactPartitionTarget) -> str:
    if config.reverse:
        ranges = """\
       (= (y_remainder_start y) (x_source_start x))
       (= (y_remainder_length y) (y_mod_remainder y))
       (= (y_remaining_start y)
          (+ (x_source_start x) (y_mod_remainder y)))
       (= (y_remaining_length y)
          (- (x_length x) (y_mod_remainder y)))"""
        reverse = "true"
    else:
        ranges = """\
       (= (y_remaining_start y) (x_source_start x))
       (= (y_remaining_length y)
          (- (x_length x) (y_mod_remainder y)))
       (= (y_remainder_start y)
          (+ (x_source_start x) (y_remaining_length y)))
       (= (y_remainder_length y) (y_mod_remainder y))"""
        reverse = "false"
    return f"""\
(define-fun {config.partition_transition} ((x Input) (y Output)) Bool
  (and (= (y_source_sequence y) (x_source_sequence x))
       (= (y_source_start y) (x_source_start x))
       (= (y_source_length y) (x_length x))
       (= (y_remaining_sequence y) (x_source_sequence x))
       (= (y_remainder_sequence y) (x_source_sequence x))
       (= (y_yielded_sequence y) 0)
       (= (y_yielded_start y) 0)
       (= (y_yielded_length y) 0)
{ranges}
       (= (y_chunk_size y) (x_chunk_size x))
       (= (y_reverse y) {reverse})))"""


def _region_identity_transition() -> str:
    return """\
(define-fun MutableRegionIdentityTransition ((x Input) (y Output)) Bool
  (and (= (y_source_address y) (x_address x))
       (= (y_source_allocation y) (x_allocation x))
       (= (y_source_provenance y) (x_provenance x))
       (= (y_source_borrow y) (x_borrow x))
       (= (y_remaining_address y)
          (+ (x_address x)
             (* (- (y_remaining_start y) (x_source_start x))
                (x_element_size x))))
       (= (y_remaining_allocation y) (x_allocation x))
       (= (y_remaining_provenance y) (x_provenance x))
       (= (y_remaining_parent_borrow y) (x_borrow x))
       (= (y_remainder_address y)
          (+ (x_address x)
             (* (- (y_remainder_start y) (x_source_start x))
                (x_element_size x))))
       (= (y_remainder_allocation y) (x_allocation x))
       (= (y_remainder_provenance y) (x_provenance x))
       (= (y_remainder_parent_borrow y) (x_borrow x))
       (= (y_raw_v_address y) (y_remaining_address y))
       (= (y_raw_v_length y) (y_remaining_length y))
       (= (y_raw_v_allocation y) (y_remaining_allocation y))
       (= (y_raw_v_provenance y) (y_remaining_provenance y))
       (= (y_marker_borrow y) (x_borrow x))
       (= (y_element_size y) (x_element_size x))))"""


def _disjoint_transition() -> str:
    return """\
(define-fun DisjointMutableRegionsTransition ((x Input) (y Output)) Bool
  (and (= (+ (y_remaining_length y) (y_remainder_length y))
          (x_length x))
       (or
         (= (y_remaining_length y) 0)
         (= (y_remainder_length y) 0)
         (<= (+ (y_remaining_start y) (y_remaining_length y))
             (y_remainder_start y))
         (<= (+ (y_remainder_start y) (y_remainder_length y))
             (y_remaining_start y)))))"""


def _private_state_transition(config: ExactPartitionTarget) -> str:
    reverse = "true" if config.reverse else "false"
    return f"""\
(define-fun PrivateConstructorStateTransition ((x Input) (y Output)) Bool
  (and (= (y_chunk_size y) (x_chunk_size x))
       (= (y_reverse y) {reverse})
       (= (y_raw_v_length y) (- (x_length x) (y_mod_remainder y)))
       (= (y_remainder_length y) (y_mod_remainder y))))"""


def _state_declaration(purpose: str) -> str:
    if purpose == EXACT_OUTPUT:
        return "(declare-datatypes ((State 0)) (((mkState))))"
    return f"""\
(declare-datatypes ((State 0))
  (((mkState
{_record_fields(STATE_FIELDS)}))))"""


def _final_state_transition(purpose: str) -> str:
    if purpose == EXACT_OUTPUT:
        return """\
(define-fun ImmediateFinalStateExists ((x Input)) Bool
  (exists
    ((backing_sequence Int)
     (backing_start Int)
     (backing_length Int)
     (backing_address Int)
     (backing_allocation Int)
     (backing_provenance Int)
     (backing_borrow Int)
     (element_size Int)
     (borrow_owned_by_iterator Bool)
     (elements_unchanged Bool))
    (and (= backing_sequence (x_source_sequence x))
         (= backing_start (x_source_start x))
         (= backing_length (x_length x))
         (= backing_address (x_address x))
         (= backing_allocation (x_allocation x))
         (= backing_provenance (x_provenance x))
         (= backing_borrow (x_borrow x))
         (= element_size (x_element_size x))
         borrow_owned_by_iterator
         elements_unchanged)))"""
    return """\
(define-fun ImmediateFinalStateTransition
  ((x Input) (s State)) Bool
  (and (= (s_backing_sequence s) (x_source_sequence x))
       (= (s_backing_start s) (x_source_start x))
       (= (s_backing_length s) (x_length x))
       (= (s_backing_address s) (x_address x))
       (= (s_backing_allocation s) (x_allocation x))
       (= (s_backing_provenance s) (x_provenance x))
       (= (s_backing_borrow s) (x_borrow x))
       (= (s_element_size s) (x_element_size x))
       (s_borrow_owned_by_iterator s)
       (s_elements_unchanged s)))"""


def _active_definitions(config: ExactPartitionTarget) -> str:
    reverse = "true" if config.reverse else "false"
    if config.reverse:
        composition = """\
(define-fun ActiveCompositionConjunct ((y Output)) Bool
  (and (= (y_remainder_sequence y) (y_source_sequence y))
       (= (y_remaining_sequence y) (y_source_sequence y))
       (= (y_remainder_start y) (y_source_start y))
       (= (y_remaining_start y)
          (+ (y_remainder_start y) (y_remainder_length y)))
       (= (+ (y_remainder_length y) (y_remaining_length y)
             (y_yielded_length y))
          (y_source_length y))))"""
    else:
        composition = """\
(define-fun ActiveCompositionConjunct ((y Output)) Bool
  (and (= (y_remaining_sequence y) (y_source_sequence y))
       (= (y_remainder_sequence y) (y_source_sequence y))
       (= (y_remaining_start y) (y_source_start y))
       (= (y_remainder_start y)
          (+ (y_remaining_start y) (y_remaining_length y)))
       (= (+ (y_yielded_length y) (y_remaining_length y)
             (y_remainder_length y))
          (y_source_length y))))"""
    return f"""\
(define-fun ActiveSourceConjunct ((x Input) (y Output)) Bool
  (and (= (y_source_sequence y) (x_source_sequence x))
       (= (y_source_start y) (x_source_start x))
       (= (y_source_length y) (x_length x))))
(define-fun ActiveYieldedEmptyConjunct ((y Output)) Bool
  (and (= (y_yielded_sequence y) 0)
       (= (y_yielded_start y) 0)
       (= (y_yielded_length y) 0)))
(define-fun ActiveChunkSizeConjunct ((x Input) (y Output)) Bool
  (= (y_chunk_size y) (x_chunk_size x)))
(define-fun ActiveReverseConjunct ((y Output)) Bool
  (= (y_reverse y) {reverse}))
(define-fun ActiveWellFormedConjunct ((y Output)) Bool
  (and (>= (y_chunk_size y) 0)
       (>= (y_remainder_length y) 0)
       (<= (y_remainder_length y) (y_source_length y))))
(define-fun ActivePositiveChunkConjunct ((y Output)) Bool
  (> (y_chunk_size y) 0))
(define-fun ActiveRemainderBoundConjunct ((y Output)) Bool
  (< (y_remainder_length y) (y_chunk_size y)))
(define-fun ActiveRemainingDivisibleConjunct ((y Output)) Bool
  (= (mod (y_remaining_length y) (y_chunk_size y)) 0))
(define-fun ActiveYieldedDivisibleConjunct ((y Output)) Bool
  (= (mod (y_yielded_length y) (y_chunk_size y)) 0))
{composition}
(define-fun ActiveChunkPartitionConjunct ((y Output)) Bool
  (and (ActiveWellFormedConjunct y)
       (ActivePositiveChunkConjunct y)
       (ActiveRemainderBoundConjunct y)
       (ActiveRemainingDivisibleConjunct y)
       (ActiveYieldedDivisibleConjunct y)
       (ActiveCompositionConjunct y)))"""


def _requires() -> str:
    return """\
(define-fun Requires_T ((x Input)) Bool
  (and (>= (x_source_sequence x) 0)
       (>= (x_source_start x) 0)
       (>= (x_length x) 0)
       (>= (x_address x) 0)
       (>= (x_allocation x) 0)
       (>= (x_provenance x) 0)
       (>= (x_borrow x) 0)
       (>= (x_element_size x) 0)
       (> (x_chunk_size x) 0)))"""


def _boundary() -> str:
    return """\
(define-fun Boundary_T ((x Input) (b Boundary)) Bool
  (and (>= (b_input_address b) 0)
       (>= (b_input_allocation b) 0)
       (>= (b_input_provenance b) 0)
       (>= (b_input_borrow b) 0)
       (>= (b_element_size b) 0)
       (InputIdentityObserved x b)))"""


def _target_definition(
    config: ExactPartitionTarget,
    purpose: str,
) -> str:
    calls = [
        "(InputIdentityObserved x b)",
        "(ModuloRemainderTransition x y)",
        f"({config.split_transition} x y)",
        f"({config.partition_transition} x y)",
        "(MutableRegionIdentityTransition x y)",
        "(DisjointMutableRegionsTransition x y)",
        "(PrivateConstructorStateTransition x y)",
    ]
    if purpose == PRIMARY:
        calls.append("(ImmediateFinalStateTransition x s)")
    else:
        calls.append("(ImmediateFinalStateExists x)")
    calls.extend(
        (
            "(ActiveSourceConjunct x y)",
            "(ActiveYieldedEmptyConjunct y)",
            "(ActiveChunkSizeConjunct x y)",
            "(ActiveReverseConjunct y)",
            "(ActiveChunkPartitionConjunct y)",
        )
    )
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
    config: ExactPartitionTarget,
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
    return f"""\
; Target: {config.target}
; Active contract SHA-256: {config.active_contract_sha256}
; Purpose: {purpose}
; Shared boundary contains only initial slice identity/provenance/layout.
(set-logic ALL)
(declare-datatypes ((Input 0))
  (((mkInput
{_record_fields(INPUT_FIELDS)}))))
(declare-datatypes ((Boundary 0))
  (((mkBoundary
{_record_fields(BOUNDARY_FIELDS)}))))
(declare-datatypes ((Output 0))
  (((mkOutput
{_record_fields(OUTPUT_FIELDS)}))))
{_state_declaration(purpose)}
(declare-const x Input)
(declare-const b Boundary)
(declare-const y1 Output)
(declare-const s1 State)
(declare-const y2 Output)
(declare-const s2 State)
{_input_identity()}
{_modulo_transition()}
{_split_transition(config)}
{_partition_transition(config)}
{_region_identity_transition()}
{_disjoint_transition()}
{_private_state_transition(config)}
{_final_state_transition(purpose)}
{_active_definitions(config)}
{_requires()}
{_boundary()}
{_target_definition(config, purpose)}
(define-fun Spec_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (TargetDefinition_T x b y s))
{_equivalence(purpose)}
{theorem}"""


def obligation_text(config: ExactPartitionTarget, purpose: str) -> str:
    return _model_text(config, purpose, include_theorem=True)


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


def _boundary_metadata(
    config: ExactPartitionTarget,
) -> list[dict[str, Any]]:
    citations = [
        config.source_reference,
        config.private_source_reference,
    ]
    roles = {
        "b_input_address": "input_memory",
        "b_input_allocation": "input_provenance",
        "b_input_provenance": "input_provenance",
        "b_input_borrow": "input_provenance",
        "b_element_size": "input_layout",
    }
    return [
        {
            "selector": selector,
            "role": roles[selector],
            "source_citations": citations,
            "trust_site_ids": list(config.boundary_trust_site_ids),
        }
        for selector, _ in BOUNDARY_FIELDS
    ]


def obligation_metadata(
    config: ExactPartitionTarget,
    purpose: str,
) -> dict[str, Any]:
    if purpose not in PURPOSES:
        raise ValueError(f"{config.target}: unknown purpose {purpose}")
    return {
        "schema_version": 2,
        "target": config.target,
        "input_order": config.input_order,
        "obligation_purpose": purpose,
        "active_contract_sha256": config.active_contract_sha256,
        "active_contract_text": config.active_contract_text,
        "domain": {
            "slice_length": "arbitrary nonnegative integer",
            "chunk_size": "arbitrary positive integer",
            "element_size": (
                "arbitrary nonnegative integer; zero-sized types are included"
            ),
        },
        "active_contract_conjuncts": list(config.active_conjuncts),
        "contract_translation": {
            "remainder": "slice length modulo positive chunk size",
            "split_index": (
                "remainder"
                if config.reverse
                else "slice length minus remainder"
            ),
            "remaining_region": (
                "suffix after the remainder prefix"
                if config.reverse
                else "prefix before the remainder suffix"
            ),
            "remainder_region": (
                "prefix before the divisible suffix"
                if config.reverse
                else "suffix after the divisible prefix"
            ),
            "reverse": config.reverse,
            "yielded_prefix": "empty at construction",
            "constructor_callback_invocations": 0,
        },
        "boundary_scope": {
            "shared_observations": [
                selector for selector, _ in BOUNDARY_FIELDS
            ],
            "admitted_trust_site_ids": list(
                config.boundary_trust_site_ids
            ),
            "source_support_trust_site_ids": list(
                config.dependency_trust_site_ids
            ),
            "context_only_trust_site_ids": list(
                config.context_only_trust_site_ids
            ),
            "excluded_observations": [
                "modulo remainder or split index",
                "remaining or remainder ranges and identities",
                "returned iterator and private state",
                "yielded prefix, chunk size, or direction",
                "aggregate final state",
                "answer-equivalent encodings",
                "partial or complete execution traces",
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
        "declared_functions": [],
        "source_transition_definitions": [
            transition
            for transition in config.source_transitions
            if purpose == PRIMARY
            or transition != "ImmediateFinalStateTransition"
        ],
        "source_transition_bindings": {
            "public_wrapper": {
                "operation": config.target,
                "source_citations": [config.source_reference],
                "trust_site_ids": [
                    f"TS-{int(config.input_order):03d}-D004"
                ],
            },
            "private_constructor": {
                "operation": config.target.rsplit("::", 1)[-1] + "::new",
                "source_citations": [config.private_source_reference],
                "trust_site_ids": list(config.all_trust_site_ids),
            },
            "split_at_mut_unchecked": {
                "operation": "split_at_mut_unchecked at a proved valid index",
                "source_citations": [config.private_source_reference],
                "trust_site_ids": [
                    f"TS-{int(config.input_order):03d}-D003"
                ],
            },
            "immediate_final_state": {
                "operation": "ImmediateFinalStateTransition",
                "semantics": (
                    "the constructor moves the mutable borrow into disjoint "
                    "iterator/remainder regions without reading or mutating "
                    "elements"
                ),
                "source_citations": [
                    config.source_reference,
                    config.private_source_reference,
                ],
                "trust_site_ids": list(
                    config.dependency_trust_site_ids
                ),
            },
        },
        "equivalence_kind": "exact",
        "equivalence_scope": (
            "every iterator, region/reference identity, private-state, and "
            "immediate final-state observation"
            if purpose == PRIMARY
            else "every iterator, region/reference identity, and private-state observation"
        ),
        "principal_observations": _principal_observations(purpose),
        "expected_solver_result": "unsat",
    }


def obligation(
    config: ExactPartitionTarget,
    purpose: str,
) -> tuple[str, dict[str, Any]]:
    return obligation_text(config, purpose), obligation_metadata(config, purpose)


def validate_target_obligation(
    config: ExactPartitionTarget,
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
            f"{config.target}: metadata differs from reviewed exact-partition model"
        )
    if parse_smt(text) != parse_smt(expected_text):
        raise GuardError(
            f"{config.target}: SMT differs from reviewed exact-partition model"
        )


def _fixed_input_assertions(case: SourceCase) -> list[str]:
    return [
        "(assert (= (x_source_sequence x) 101))",
        "(assert (= (x_source_start x) 7))",
        f"(assert (= (x_length x) {case.length}))",
        "(assert (= (x_address x) 1000))",
        "(assert (= (x_allocation x) 11))",
        "(assert (= (x_provenance x) 13))",
        "(assert (= (x_borrow x) 17))",
        f"(assert (= (x_element_size x) {case.element_size}))",
        f"(assert (= (x_chunk_size x) {case.chunk_size}))",
    ]


def _model_query() -> str:
    terms = [
        "(x_length x)",
        "(x_chunk_size x)",
        "(x_element_size x)",
        *(f"({selector} y1)" for selector, _ in OUTPUT_FIELDS),
        *(f"({selector} s1)" for selector, _ in STATE_FIELDS),
    ]
    return "(get-value (\n  %s))" % "\n  ".join(terms)


def source_instance_text(
    config: ExactPartitionTarget,
    case: SourceCase,
    *,
    extra_assertions: tuple[str, ...] = (),
) -> str:
    if (
        case.length < 0
        or case.chunk_size <= 0
        or case.element_size < 0
    ):
        raise ValueError("source cases require nonnegative layout and positive chunks")
    assertions = [
        *_fixed_input_assertions(case),
        "(assert (Requires_T x))",
        "(assert (Boundary_T x b))",
        "(assert (Spec_T x b y1 s1))",
        *(f"(assert {item})" for item in case.assertions),
        *(f"(assert {item})" for item in extra_assertions),
    ]
    return (
        _model_text(config, PRIMARY, include_theorem=False)
        + "\n"
        + "\n".join(assertions)
        + "\n(check-sat)\n"
        + _model_query()
        + "\n"
    )


def negative_probe_text(
    config: ExactPartitionTarget,
    name: str,
) -> str:
    if name not in NEGATIVE_PROBES:
        raise ValueError(f"unknown exact-partition negative probe: {name}")
    element_size = 0 if name == "zst_unequal_region_addresses" else 8
    case = SourceCase(5, 3, element_size)
    if name == "zero_chunk":
        assertions = _fixed_input_assertions(
            SourceCase(case.length, 0, case.element_size)
        )
        assertions.extend(
            (
                "(assert (Requires_T x))",
                "(assert (Boundary_T x b))",
                "(assert (Spec_T x b y1 s1))",
            )
        )
    else:
        contradictions = {
            "incorrect_modulo": (
                "(not (= (y_mod_remainder y1) "
                "(mod (x_length x) (x_chunk_size x))))"
            ),
            "incorrect_split_index": (
                "(not (= (y_split_index y1) "
                + (
                    "(y_mod_remainder y1)))"
                    if config.reverse
                    else "(- (x_length x) (y_mod_remainder y1))))"
                )
            ),
            "swapped_remainder_placement": (
                "(= (y_remainder_start y1) "
                + (
                    "(+ (x_source_start x) (y_remaining_length y1)))"
                    if config.reverse
                    else "(x_source_start x))"
                )
            ),
            "incorrect_concatenation_order": (
                "(not (= (+ (y_remaining_length y1) "
                "(y_remainder_length y1)) (x_length x)))"
            ),
            "provenance_loss": (
                "(not (= (y_raw_v_provenance y1) (x_provenance x)))"
            ),
            "borrow_loss": (
                "(not (= (y_remainder_parent_borrow y1) (x_borrow x)))"
            ),
            "zst_unequal_region_addresses": (
                "(not (= (y_remaining_address y1) "
                "(y_remainder_address y1)))"
            ),
        }
        assertions = [
            *_fixed_input_assertions(case),
            "(assert (Requires_T x))",
            "(assert (Boundary_T x b))",
            "(assert (Spec_T x b y1 s1))",
            f"(assert {contradictions[name]})",
        ]
    return (
        _model_text(config, PRIMARY, include_theorem=False)
        + "\n"
        + "\n".join(assertions)
        + "\n(check-sat)\n"
    )


def boundary_manifest(config: ExactPartitionTarget) -> dict[str, Any]:
    meanings = {
        "b_input_address": "initial slice data address",
        "b_input_allocation": "allocation identity backing the initial slice",
        "b_input_provenance": "initial slice provenance",
        "b_input_borrow": "initial unique mutable-borrow identity",
        "b_element_size": "element layout size, including zero",
    }
    return {
        "schema_version": 1,
        "target": config.target,
        "input_order": config.input_order,
        "boundary_narrower_than_target": True,
        "shared_boundary_observations": [
            {
                "field": selector,
                "meaning": meanings[selector],
                "trust_site_ids": list(config.boundary_trust_site_ids),
            }
            for selector, _ in BOUNDARY_FIELDS
        ],
        "deterministic_source_transition": {
            "remainder": "length modulo positive chunk size",
            "split_index": (
                "remainder"
                if config.reverse
                else "length minus remainder"
            ),
            "partition_orientation": (
                "remainder then divisible remaining region"
                if config.reverse
                else "divisible remaining region then remainder"
            ),
            "preserves_allocation_provenance_and_parent_borrow": True,
            "zst_disjointness": (
                "range-based; disjoint mutable regions may have equal addresses"
            ),
            "yielded_prefix": "empty",
            "reverse": config.reverse,
            "elements_mutated": False,
        },
        "source_support_trust_site_ids": list(
            config.dependency_trust_site_ids
        ),
        "context_only_trust_site_ids": list(
            config.context_only_trust_site_ids
        ),
        "all_audited_trust_site_ids": list(config.all_trust_site_ids),
        "excluded_from_boundary": [
            "modulo remainder and split index",
            "partition ranges and orientation",
            "returned iterator and private constructor state",
            "raw-v and remainder-reference identities",
            "yielded prefix, chunk size, and direction",
            "immediate final state",
            "answer encodings and execution traces",
        ],
    }


def _verus_header(config: ExactPartitionTarget) -> str:
    return f"""\
#![allow(dead_code, unused_imports, unused_variables)]
// Generated source-backed exact-partition model for {config.target}.

use vstd::arithmetic::div_mod::*;
use vstd::arithmetic::mul::*;
use vstd::prelude::*;
use vstd::seq::*;
use vstd::seq_lib::*;

verus! {{

pub ghost struct SliceIdentity {{
    pub source: Seq<int>,
    pub start: int,
    pub address: int,
    pub allocation: int,
    pub provenance: int,
    pub borrow: int,
    pub element_size: nat,
}}

pub ghost struct RegionIdentity {{
    pub values: Seq<int>,
    pub start: int,
    pub length: nat,
    pub address: int,
    pub allocation: int,
    pub provenance: int,
    pub parent_borrow: int,
    pub element_size: nat,
}}

pub ghost struct RawSliceIdentity {{
    pub address: int,
    pub length: nat,
    pub allocation: int,
    pub provenance: int,
}}

pub ghost struct Input {{
    pub slice: SliceIdentity,
    pub chunk_size: nat,
}}

pub ghost struct ExactChunkIterator {{
    pub source: SliceIdentity,
    pub remaining: RegionIdentity,
    pub yielded_prefix: Seq<int>,
    pub remainder: RegionIdentity,
    pub raw_v: RawSliceIdentity,
    pub marker_borrow: int,
    pub chunk_size: nat,
    pub reverse: bool,
    pub modulo_remainder: nat,
    pub split_index: nat,
}}

pub ghost struct FinalState {{
    pub backing: SliceIdentity,
    pub borrow_owned_by_iterator: bool,
    pub elements_unchanged: bool,
}}

pub open spec fn make_region(
    slice: SliceIdentity,
    offset: nat,
    length: nat,
) -> RegionIdentity
    recommends
        offset + length <= slice.source.len(),
{{
    RegionIdentity {{
        values: slice.source.subrange(
            offset as int,
            (offset + length) as int,
        ),
        start: slice.start + offset as int,
        length,
        address: slice.address
            + (offset as int) * (slice.element_size as int),
        allocation: slice.allocation,
        provenance: slice.provenance,
        parent_borrow: slice.borrow,
        element_size: slice.element_size,
    }}
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
        && left.borrow == right.borrow
        && left.element_size == right.element_size
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
}}

pub open spec fn same_raw(
    left: RawSliceIdentity,
    right: RawSliceIdentity,
) -> bool {{
    left.address == right.address
        && left.length == right.length
        && left.allocation == right.allocation
        && left.provenance == right.provenance
}}
"""


def _verus_body(config: ExactPartitionTarget) -> str:
    function = config.target.rsplit("::", 1)[-1]
    reverse = "true" if config.reverse else "false"
    if config.reverse:
        split = "rem"
        remaining_offset = "rem"
        remaining_length = "(n - rem) as nat"
        remainder_offset = "0"
        remainder_length = "rem"
        composition = (
            "iter.remainder.values + iter.remaining.values "
            "+ iter.yielded_prefix == iter.source.source"
        )
        split_lemma = "input.slice.source.lemma_split_at(rem as int);"
        composition_assert = (
            "assert(remainder.values + remaining.values == input.slice.source);"
        )
    else:
        split = "(n - rem) as nat"
        remaining_offset = "0"
        remaining_length = "(n - rem) as nat"
        remainder_offset = "(n - rem) as nat"
        remainder_length = "rem"
        composition = (
            "iter.yielded_prefix + iter.remaining.values "
            "+ iter.remainder.values == iter.source.source"
        )
        split_lemma = "input.slice.source.lemma_split_at(split as int);"
        composition_assert = (
            "assert(remaining.values + remainder.values == input.slice.source);"
        )
    return f"""\
pub open spec fn output_transition(
    input: Input,
    iter: ExactChunkIterator,
) -> bool {{
    let n = input.slice.source.len();
    let rem = n % input.chunk_size;
    let split = {split};
    let remaining = make_region(
        input.slice,
        {remaining_offset},
        {remaining_length},
    );
    let remainder = make_region(
        input.slice,
        {remainder_offset},
        {remainder_length},
    );
    same_slice(iter.source, input.slice)
        && same_region(iter.remaining, remaining)
        && iter.yielded_prefix == Seq::<int>::empty()
        && same_region(iter.remainder, remainder)
        && iter.raw_v.address == remaining.address
        && iter.raw_v.length == remaining.length
        && iter.raw_v.allocation == remaining.allocation
        && iter.raw_v.provenance == remaining.provenance
        && iter.marker_borrow == input.slice.borrow
        && iter.chunk_size == input.chunk_size
        && iter.reverse == {reverse}
        && iter.modulo_remainder == rem
        && iter.split_index == split
}}

pub open spec fn active_contract(
    input: Input,
    iter: ExactChunkIterator,
) -> bool {{
    input.chunk_size > 0
        && iter.source.source == input.slice.source
        && iter.yielded_prefix == Seq::<int>::empty()
        && iter.chunk_size == input.chunk_size
        && iter.reverse == {reverse}
        && iter.remainder.length < iter.chunk_size
        && iter.remaining.length % iter.chunk_size == 0
        && iter.yielded_prefix.len() % iter.chunk_size == 0
        && {composition}
}}

pub open spec fn final_state_transition(
    input: Input,
    state: FinalState,
) -> bool {{
    same_slice(state.backing, input.slice)
        && state.borrow_owned_by_iterator
        && state.elements_unchanged
}}

pub open spec fn target_transition(
    input: Input,
    iter: ExactChunkIterator,
    state: FinalState,
) -> bool {{
    input.chunk_size > 0
        && output_transition(input, iter)
        && active_contract(input, iter)
        && final_state_transition(input, state)
}}

pub proof fn {function}_constructor(
    input: Input,
) -> (ret: ExactChunkIterator)
    requires
        input.chunk_size > 0,
    ensures
        output_transition(input, ret),
        active_contract(input, ret),
{{
    let n = input.slice.source.len();
    let rem = n % input.chunk_size;
    lemma_mod_decreases(n as nat, input.chunk_size as nat);
    assert(rem <= n);
    let split = {split};
    let remaining = make_region(
        input.slice,
        {remaining_offset},
        {remaining_length},
    );
    let remainder = make_region(
        input.slice,
        {remainder_offset},
        {remainder_length},
    );
    let ret = ExactChunkIterator {{
        source: input.slice,
        remaining,
        yielded_prefix: Seq::empty(),
        remainder,
        raw_v: RawSliceIdentity {{
            address: remaining.address,
            length: remaining.length,
            allocation: remaining.allocation,
            provenance: remaining.provenance,
        }},
        marker_borrow: input.slice.borrow,
        chunk_size: input.chunk_size,
        reverse: {reverse},
        modulo_remainder: rem,
        split_index: split,
    }};
    let ni = n as int;
    let ci = input.chunk_size as int;
    lemma_mod_division_less_than_divisor(ni, ci);
    lemma_fundamental_div_mod(ni, ci);
    lemma_mod_multiples_basic(ni / ci, ci);
    lemma_mul_is_commutative(ci, ni / ci);
    assert((rem as int) == ni % ci);
    assert(ni == ci * (ni / ci) + (ni % ci));
    assert((((n - rem) as nat) as int) == ci * (ni / ci));
    assert(ci * (ni / ci) == (ni / ci) * ci);
    assert((((n - rem) as nat) as int) % ci == 0);
    {split_lemma}
    {composition_assert}
    assert(ret.remainder.length < ret.chunk_size);
    assert(ret.remaining.length % ret.chunk_size == 0);
    lemma_small_mod(0nat, input.chunk_size as nat);
    assert(ret.yielded_prefix.len() % ret.chunk_size == 0);
    assert(active_contract(input, ret));
    ret
}}

pub open spec fn same_iterator(
    left: ExactChunkIterator,
    right: ExactChunkIterator,
) -> bool {{
    same_slice(left.source, right.source)
        && same_region(left.remaining, right.remaining)
        && left.yielded_prefix == right.yielded_prefix
        && same_region(left.remainder, right.remainder)
        && same_raw(left.raw_v, right.raw_v)
        && left.marker_borrow == right.marker_borrow
        && left.chunk_size == right.chunk_size
        && left.reverse == right.reverse
        && left.modulo_remainder == right.modulo_remainder
        && left.split_index == right.split_index
}}

pub open spec fn exact_equivalent(
    left: ExactChunkIterator,
    left_state: FinalState,
    right: ExactChunkIterator,
    right_state: FinalState,
) -> bool {{
    same_iterator(left, right)
        && same_slice(left_state.backing, right_state.backing)
        && left_state.borrow_owned_by_iterator
            == right_state.borrow_owned_by_iterator
        && left_state.elements_unchanged == right_state.elements_unchanged
}}

pub open spec fn exact_output_equivalent(
    left: ExactChunkIterator,
    right: ExactChunkIterator,
) -> bool {{
    same_iterator(left, right)
}}

pub proof fn conditional_complete_{function}(
    input: Input,
    iter1: ExactChunkIterator,
    state1: FinalState,
    iter2: ExactChunkIterator,
    state2: FinalState,
)
    requires
        target_transition(input, iter1, state1),
        target_transition(input, iter2, state2),
    ensures
        exact_equivalent(iter1, state1, iter2, state2),
{{
    reveal(target_transition);
    reveal(output_transition);
    reveal(final_state_transition);
    reveal(exact_equivalent);
    reveal(same_iterator);
    reveal(same_slice);
    reveal(same_region);
    reveal(same_raw);
}}

pub proof fn conditional_complete_exact_output_{function}(
    input: Input,
    iter1: ExactChunkIterator,
    state1: FinalState,
    iter2: ExactChunkIterator,
    state2: FinalState,
)
    requires
        target_transition(input, iter1, state1),
        target_transition(input, iter2, state2),
    ensures
        exact_output_equivalent(iter1, iter2),
{{
    reveal(target_transition);
    reveal(output_transition);
    reveal(exact_output_equivalent);
    reveal(same_iterator);
    reveal(same_slice);
    reveal(same_region);
    reveal(same_raw);
}}

}} // verus!
"""


def verus_text(config: ExactPartitionTarget) -> str:
    return _verus_header(config) + _verus_body(config)
