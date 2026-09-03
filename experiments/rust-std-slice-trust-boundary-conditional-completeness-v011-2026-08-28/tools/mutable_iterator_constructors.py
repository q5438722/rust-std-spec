#!/usr/bin/env python3
"""Source-backed constructor models for seven mutable Slice iterators."""

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
class PrivateSource:
    name: str
    start: int
    end: int

    @property
    def citation(self) -> str:
        return f"{CANONICAL_ITER_PATH}:{self.start}-{self.end}"

    @property
    def filename(self) -> str:
        normalized = self.name.replace("::", "_").replace(" ", "_").lower()
        return f"{normalized}.rs"


@dataclass(frozen=True)
class ConstructorTarget:
    target: str
    input_order: str
    artifact_id: str
    active_contract_sha256: str
    active_contract_text: str
    family: str
    callback_kind: str
    reverse: bool
    inclusive: bool
    limit_kind: str
    finished_kind: str
    constructor_name: str
    constructor_chain: tuple[str, ...]
    private_sources: tuple[PrivateSource, ...]
    source_reference: str
    docs_reference: str
    all_trust_site_ids: tuple[str, ...]

    @property
    def callback(self) -> bool:
        return self.callback_kind != "none"

    @property
    def context_only_trust_site_ids(self) -> tuple[str, ...]:
        return tuple(
            site for site in self.all_trust_site_ids if "-C" in site
        )

    @property
    def dependency_trust_site_ids(self) -> tuple[str, ...]:
        return tuple(
            site for site in self.all_trust_site_ids if "-D" in site
        )

    @property
    def data_trust_site_ids(self) -> tuple[str, ...]:
        return tuple(
            site
            for site in self.dependency_trust_site_ids
            if not (self.family == "chunks" and site.endswith("D003"))
        )

    @property
    def callback_trust_site_ids(self) -> tuple[str, ...]:
        return tuple(
            site
            for site in self.dependency_trust_site_ids
            if site.endswith("D003")
        )

    @property
    def output_fields(self) -> tuple[tuple[str, str], ...]:
        fields: list[tuple[str, str]] = [
            ("y_source_sequence", "Int"),
            ("y_source_start", "Int"),
            ("y_source_length", "Int"),
            ("y_remaining_sequence", "Int"),
            ("y_remaining_start", "Int"),
            ("y_remaining_length", "Int"),
            ("y_yielded_sequence", "Int"),
            ("y_yielded_start", "Int"),
            ("y_yielded_length", "Int"),
            ("y_remainder_sequence", "Int"),
            ("y_remainder_start", "Int"),
            ("y_remainder_length", "Int"),
            ("y_address", "Int"),
            ("y_allocation", "Int"),
            ("y_provenance", "Int"),
            ("y_borrow", "Int"),
            ("y_element_size", "Int"),
            ("y_chunk_size", "Int"),
            ("y_reverse", "Bool"),
        ]
        if self.family == "chunks":
            fields.extend(
                (
                    ("y_raw_address", "Int"),
                    ("y_raw_length", "Int"),
                    ("y_raw_allocation", "Int"),
                    ("y_raw_provenance", "Int"),
                    ("y_marker_borrow", "Int"),
                )
            )
        if self.callback:
            fields.extend(
                (
                    ("y_predicate_identity", "Int"),
                    ("y_predicate_state", "Int"),
                    ("y_callback_calls", "Int"),
                )
            )
        if self.family == "predicate":
            fields.extend(
                (
                    ("y_finished", "Bool"),
                    ("y_inclusive", "Bool"),
                )
            )
            if self.limit_kind == "n":
                fields.append(("y_count", "Int"))
        return tuple(fields)

    @property
    def state_fields(self) -> tuple[tuple[str, str], ...]:
        fields: list[tuple[str, str]] = [
            ("s_final_slice_sequence", "Int"),
            ("s_final_slice_start", "Int"),
            ("s_final_slice_length", "Int"),
            ("s_final_address", "Int"),
            ("s_final_allocation", "Int"),
            ("s_final_provenance", "Int"),
            ("s_final_borrow", "Int"),
            ("s_final_element_size", "Int"),
        ]
        if self.callback:
            fields.extend(
                (
                    ("s_callback_identity", "Int"),
                    ("s_callback_state", "Int"),
                    ("s_callback_calls", "Int"),
                )
            )
        return tuple(fields)

    @property
    def top_transition(self) -> str:
        return f"{self.constructor_name}Transition"

    @property
    def source_transitions(self) -> tuple[str, ...]:
        transitions = ["StoredSliceTransition"]
        if self.callback:
            transitions.append("StoredPredicateTransition")
        if self.family == "chunks":
            transitions.append("MutableRawSliceCastTransition")
        transitions.extend(
            f"{name}Transition" for name in self.constructor_chain
        )
        transitions.append("ConstructorFinalStateTransition")
        return tuple(dict.fromkeys(transitions))

    @property
    def active_conjuncts(self) -> tuple[str, ...]:
        conjuncts = [
            "ActiveWellFormedConjunct",
            "ActiveSourceConjunct",
            "ActiveRemainingConjunct",
            "ActiveYieldedEmptyConjunct",
            "ActiveRemainderEmptyConjunct",
            "ActiveChunkSizeConjunct",
            "ActiveReverseConjunct",
            "ActiveCompositionConjunct",
        ]
        if self.family == "chunks":
            conjuncts.insert(0, "ActiveChunkDomainConjunct")
        elif self.callback_kind == "adjacent":
            conjuncts.append("ActiveAdjacentPredicateTotalityConjunct")
        elif self.callback_kind == "unary":
            conjuncts.extend(
                (
                    "ActiveLimitNonnegativeConjunct",
                    "ActivePredicateTotalityConjunct",
                )
            )
        return tuple(conjuncts)


@dataclass(frozen=True)
class PrivateSourceAnchor:
    operation: str
    citation: str
    fragment: str


@dataclass(frozen=True)
class SourceModelAnchor:
    public_reference: str
    public_fragment: str
    constructor_chain: tuple[str, ...]
    private_sources: tuple[PrivateSourceAnchor, ...]
    finished_kind: str
    limit_kind: str
    reverse: bool


TARGETS = (
    ConstructorTarget(
        target="core::slice::chunk_by_mut",
        input_order="32",
        artifact_id="032_core_slice_chunk_by_mut",
        active_contract_sha256=(
            "f4d113c638ecee678916c7446e3e173c3e3b16486104fea5a2d623e9cd82646a"
        ),
        active_contract_text=(
            "pub assume_specification<'a, T, F: core::ops::FnMut(&T, &T) -> "
            "bool>[ <[T]>::chunk_by_mut::<F> ]( slice: &'a mut [T], pred: F, ) "
            "-> (iter: core::slice::ChunkByMut<'a, T, F>) ensures "
            "slice_adjacent_chunk_view::<core::slice::ChunkByMut<'a, T, F>, "
            "F, T>( iter, old(slice)@, pred, ), ;"
        ),
        family="adjacent",
        callback_kind="adjacent",
        reverse=False,
        inclusive=False,
        limit_kind="zero",
        finished_kind="absent",
        constructor_name="ChunkByMutNew",
        constructor_chain=("ChunkByMutNew",),
        private_sources=(PrivateSource("ChunkByMut::new", 3109, 3118),),
        source_reference="core/src/slice/mod.rs:1909",
        docs_reference="core/src/slice/mod.rs:1871-1902",
        all_trust_site_ids=(
            "TS-032-D001",
            "TS-032-D002",
            "TS-032-D003",
            "TS-032-D004",
            "TS-032-C001",
        ),
    ),
    ConstructorTarget(
        target="core::slice::chunks_mut",
        input_order="36",
        artifact_id="036_core_slice_chunks_mut",
        active_contract_sha256=(
            "2dab70b28fb6d950965db60214651aa3ebdd8bcdd55acbc04be541086ac2d091"
        ),
        active_contract_text=(
            "pub assume_specification<'a, T>[ <[T]>::chunks_mut ]( slice: &'a "
            "mut [T], chunk_size: usize, ) -> (iter: "
            "core::slice::ChunksMut<'a, T>) requires chunk_size != 0, ensures "
            "slice_iterator_view::<core::slice::ChunksMut<'a, T>, "
            "T>(iter).source == old(slice)@, "
            "slice_iterator_view::<core::slice::ChunksMut<'a, T>, "
            "T>(iter).remaining == old(slice)@, "
            "slice_iterator_view::<core::slice::ChunksMut<'a, T>, "
            "T>(iter).yielded_prefix == Seq::empty(), "
            "slice_iterator_view::<core::slice::ChunksMut<'a, T>, "
            "T>(iter).remainder == Seq::empty(), "
            "slice_iterator_view::<core::slice::ChunksMut<'a, T>, "
            "T>(iter).chunk_size == chunk_size as int, "
            "!slice_iterator_view::<core::slice::ChunksMut<'a, T>, "
            "T>(iter).reverse, ;"
        ),
        family="chunks",
        callback_kind="none",
        reverse=False,
        inclusive=False,
        limit_kind="chunk",
        finished_kind="absent",
        constructor_name="ChunksMutNew",
        constructor_chain=("ChunksMutNew",),
        private_sources=(PrivateSource("ChunksMut::new", 1656, 1672),),
        source_reference="core/src/slice/mod.rs:1202",
        docs_reference="core/src/slice/mod.rs:1160-1194",
        all_trust_site_ids=(
            "TS-036-D001",
            "TS-036-D002",
            "TS-036-D003",
            "TS-036-D004",
            "TS-036-C001",
        ),
    ),
    ConstructorTarget(
        target="core::slice::rchunks_mut",
        input_order="69",
        artifact_id="069_core_slice_rchunks_mut",
        active_contract_sha256=(
            "d486130bfa74afb7939ee7ea71e97c4eeda6d17e9c9ded51d0a48b9aff81736c"
        ),
        active_contract_text=(
            "pub assume_specification<'a, T>[ <[T]>::rchunks_mut ]( slice: &'a "
            "mut [T], chunk_size: usize, ) -> (iter: "
            "core::slice::RChunksMut<'a, T>) requires chunk_size != 0, ensures "
            "slice_iterator_view::<core::slice::RChunksMut<'a, T>, "
            "T>(iter).source == old(slice)@, "
            "slice_iterator_view::<core::slice::RChunksMut<'a, T>, "
            "T>(iter).remaining == old(slice)@, "
            "slice_iterator_view::<core::slice::RChunksMut<'a, T>, "
            "T>(iter).yielded_prefix == Seq::empty(), "
            "slice_iterator_view::<core::slice::RChunksMut<'a, T>, "
            "T>(iter).remainder == Seq::empty(), "
            "slice_iterator_view::<core::slice::RChunksMut<'a, T>, "
            "T>(iter).chunk_size == chunk_size as int, "
            "slice_iterator_view::<core::slice::RChunksMut<'a, T>, "
            "T>(iter).reverse, ;"
        ),
        family="chunks",
        callback_kind="none",
        reverse=True,
        inclusive=False,
        limit_kind="chunk",
        finished_kind="absent",
        constructor_name="RChunksMutNew",
        constructor_chain=("RChunksMutNew",),
        private_sources=(PrivateSource("RChunksMut::new", 2471, 2487),),
        source_reference="core/src/slice/mod.rs:1733",
        docs_reference="core/src/slice/mod.rs:1691-1725",
        all_trust_site_ids=(
            "TS-069-D001",
            "TS-069-D002",
            "TS-069-D003",
            "TS-069-D004",
            "TS-069-C001",
        ),
    ),
    ConstructorTarget(
        target="core::slice::rsplit_mut",
        input_order="74",
        artifact_id="074_core_slice_rsplit_mut",
        active_contract_sha256=(
            "949691a0b75b3e64a19af9ef95077e0bbdd4530b19a01d6742a38be652431148"
        ),
        active_contract_text=(
            "pub assume_specification<'a, T, F: core::ops::FnMut(&T) -> bool>[ "
            "<[T]>::rsplit_mut::<F> ]( slice: &'a mut [T], pred: F, ) -> "
            "(iter: core::slice::RSplitMut<'a, T, F>) ensures "
            "slice_predicate_split_view::<core::slice::RSplitMut<'a, T, F>, "
            "F, T>( iter, old(slice)@, pred, false, true, 0, ), ;"
        ),
        family="predicate",
        callback_kind="unary",
        reverse=True,
        inclusive=False,
        limit_kind="zero",
        finished_kind="false",
        constructor_name="RSplitMutNew",
        constructor_chain=("SplitMutNewStorage", "RSplitMutNew"),
        private_sources=(
            PrivateSource("SplitMut::new", 678, 690),
            PrivateSource("RSplitMut::new", 1031, 1042),
        ),
        source_reference="core/src/slice/mod.rs:2391",
        docs_reference="core/src/slice/mod.rs:2369-2385",
        all_trust_site_ids=(
            "TS-074-D001",
            "TS-074-D002",
            "TS-074-D003",
            "TS-074-D004",
            "TS-074-C001",
            "TS-074-C002",
        ),
    ),
    ConstructorTarget(
        target="core::slice::rsplitn_mut",
        input_order="76",
        artifact_id="076_core_slice_rsplitn_mut",
        active_contract_sha256=(
            "c7b8151e61d9ad4d7b0ba9c3669fcee75ca3acc98ea2741f3b162df19efe113f"
        ),
        active_contract_text=(
            "pub assume_specification<'a, T, F: core::ops::FnMut(&T) -> bool>[ "
            "<[T]>::rsplitn_mut::<F> ]( slice: &'a mut [T], n: usize, pred: "
            "F, ) -> (iter: core::slice::RSplitNMut<'a, T, F>) ensures "
            "slice_predicate_split_view::<core::slice::RSplitNMut<'a, T, F>, "
            "F, T>( iter, old(slice)@, pred, false, true, n as int, ), ;"
        ),
        family="predicate",
        callback_kind="unary",
        reverse=True,
        inclusive=False,
        limit_kind="n",
        finished_kind="false",
        constructor_name="RSplitNMutNew",
        constructor_chain=(
            "SplitMutNewStorage",
            "RSplitMutNewStorage",
            "RSplitNMutNew",
        ),
        private_sources=(
            PrivateSource("SplitMut::new", 678, 690),
            PrivateSource("RSplitMut::new", 1031, 1042),
            PrivateSource("RSplitNMut::new", 1289, 1293),
        ),
        source_reference="core/src/slice/mod.rs:2501",
        docs_reference="core/src/slice/mod.rs:2478-2495",
        all_trust_site_ids=(
            "TS-076-D001",
            "TS-076-D002",
            "TS-076-D003",
            "TS-076-D004",
            "TS-076-C001",
            "TS-076-C002",
            "TS-076-C003",
        ),
    ),
    ConstructorTarget(
        target="core::slice::split_inclusive_mut",
        input_order="93",
        artifact_id="093_core_slice_split_inclusive_mut",
        active_contract_sha256=(
            "d0f84cc808519d278a4020ddeff02c6979d9d3e9e06d6880ec28c354d0e57fe5"
        ),
        active_contract_text=(
            "pub assume_specification<'a, T, F: core::ops::FnMut(&T) -> bool>[ "
            "<[T]>::split_inclusive_mut::<F> ]( slice: &'a mut [T], pred: F, "
            ") -> (iter: core::slice::SplitInclusiveMut<'a, T, F>) ensures "
            "slice_predicate_split_view::<core::slice::SplitInclusiveMut<'a, "
            "T, F>, F, T>( iter, old(slice)@, pred, true, false, 0, ), ;"
        ),
        family="predicate",
        callback_kind="unary",
        reverse=False,
        inclusive=True,
        limit_kind="zero",
        finished_kind="empty",
        constructor_name="SplitInclusiveMutNew",
        constructor_chain=("SplitInclusiveMutNew",),
        private_sources=(
            PrivateSource("SplitInclusiveMut::new", 807, 821),
        ),
        source_reference="core/src/slice/mod.rs:2329",
        docs_reference="core/src/slice/mod.rs:2309-2323",
        all_trust_site_ids=(
            "TS-093-D001",
            "TS-093-D002",
            "TS-093-D003",
            "TS-093-D004",
            "TS-093-C001",
        ),
    ),
    ConstructorTarget(
        target="core::slice::split_mut",
        input_order="98",
        artifact_id="098_core_slice_split_mut",
        active_contract_sha256=(
            "81cedd197710c3392a77bf21e9d0efe0bf6919c268ccbddebf0d3898ab138879"
        ),
        active_contract_text=(
            "pub assume_specification<'a, T, F: core::ops::FnMut(&T) -> bool>[ "
            "<[T]>::split_mut::<F> ]( slice: &'a mut [T], pred: F, ) -> "
            "(iter: core::slice::SplitMut<'a, T, F>) ensures "
            "slice_predicate_split_view::<core::slice::SplitMut<'a, T, F>, "
            "F, T>( iter, old(slice)@, pred, false, false, 0, ), ;"
        ),
        family="predicate",
        callback_kind="unary",
        reverse=False,
        inclusive=False,
        limit_kind="zero",
        finished_kind="false",
        constructor_name="SplitMutNew",
        constructor_chain=("SplitMutNew",),
        private_sources=(PrivateSource("SplitMut::new", 678, 690),),
        source_reference="core/src/slice/mod.rs:2269",
        docs_reference="core/src/slice/mod.rs:2251-2263",
        all_trust_site_ids=(
            "TS-098-D001",
            "TS-098-D002",
            "TS-098-D003",
            "TS-098-D004",
            "TS-098-C001",
        ),
    ),
)

TARGET_BY_ARTIFACT = {target.artifact_id: target for target in TARGETS}
TARGET_BY_KEY = {
    (target.target, target.input_order): target for target in TARGETS
}
TARGET_KEYS = tuple(TARGET_BY_KEY)

SOURCE_MODEL_ANCHORS = {
    "074_core_slice_rsplit_mut": SourceModelAnchor(
        public_reference="core/src/slice/mod.rs:2391",
        public_fragment="RSplitMut::new(self, pred)",
        constructor_chain=("SplitMutNewStorage", "RSplitMutNew"),
        private_sources=(
            PrivateSourceAnchor(
                operation="SplitMut::new",
                citation="core/src/slice/iter.rs:678-690",
                fragment="Self { v: slice, pred, finished: false }",
            ),
            PrivateSourceAnchor(
                operation="RSplitMut::new",
                citation="core/src/slice/iter.rs:1031-1042",
                fragment="Self { inner: SplitMut::new(slice, pred) }",
            ),
        ),
        finished_kind="false",
        limit_kind="zero",
        reverse=True,
    ),
    "076_core_slice_rsplitn_mut": SourceModelAnchor(
        public_reference="core/src/slice/mod.rs:2501",
        public_fragment="RSplitNMut::new(self.rsplit_mut(pred), n)",
        constructor_chain=(
            "SplitMutNewStorage",
            "RSplitMutNewStorage",
            "RSplitNMutNew",
        ),
        private_sources=(
            PrivateSourceAnchor(
                operation="SplitMut::new",
                citation="core/src/slice/iter.rs:678-690",
                fragment="Self { v: slice, pred, finished: false }",
            ),
            PrivateSourceAnchor(
                operation="RSplitMut::new",
                citation="core/src/slice/iter.rs:1031-1042",
                fragment="Self { inner: SplitMut::new(slice, pred) }",
            ),
            PrivateSourceAnchor(
                operation="RSplitNMut::new",
                citation="core/src/slice/iter.rs:1289-1293",
                fragment=(
                    "Self { inner: GenericSplitN { iter: s, count: n } }"
                ),
            ),
        ),
        finished_kind="false",
        limit_kind="n",
        reverse=True,
    ),
    "098_core_slice_split_mut": SourceModelAnchor(
        public_reference="core/src/slice/mod.rs:2269",
        public_fragment="SplitMut::new(self, pred)",
        constructor_chain=("SplitMutNew",),
        private_sources=(
            PrivateSourceAnchor(
                operation="SplitMut::new",
                citation="core/src/slice/iter.rs:678-690",
                fragment="Self { v: slice, pred, finished: false }",
            ),
        ),
        finished_kind="false",
        limit_kind="zero",
        reverse=False,
    ),
}


def _normalized_source(text: str) -> str:
    return " ".join(text.split())


def validate_source_anchors(
    config: ConstructorTarget,
    public_source: str,
    private_sources: dict[str, str],
) -> None:
    anchor = SOURCE_MODEL_ANCHORS.get(config.artifact_id)
    if anchor is None:
        return

    expected_private = tuple(
        (source.operation, source.citation)
        for source in anchor.private_sources
    )
    observed_private = tuple(
        (source.name, source.citation) for source in config.private_sources
    )
    if (
        config.source_reference != anchor.public_reference
        or config.constructor_chain != anchor.constructor_chain
        or observed_private != expected_private
        or config.finished_kind != anchor.finished_kind
        or config.limit_kind != anchor.limit_kind
        or config.reverse != anchor.reverse
    ):
        raise GuardError(
            f"{config.target}: constructor configuration differs from "
            "canonical source anchors"
        )

    if _normalized_source(anchor.public_fragment) not in _normalized_source(
        public_source
    ):
        raise GuardError(
            f"{config.target}: public wrapper does not preserve constructor order"
        )
    if set(private_sources) != {
        source.operation for source in anchor.private_sources
    }:
        raise GuardError(
            f"{config.target}: canonical private constructor set is incomplete"
        )
    for source in anchor.private_sources:
        if _normalized_source(source.fragment) not in _normalized_source(
            private_sources[source.operation]
        ):
            raise GuardError(
                f"{config.target}: {source.operation} does not match its "
                "canonical source default"
            )


def _record_fields(fields: tuple[tuple[str, str], ...]) -> str:
    return "\n".join(f"      ({name} {sort})" for name, sort in fields)


def _input_fields(config: ConstructorTarget) -> tuple[tuple[str, str], ...]:
    fields: list[tuple[str, str]] = [
        ("x_source_sequence", "Int"),
        ("x_source_start", "Int"),
        ("x_length", "Int"),
        ("x_address", "Int"),
        ("x_allocation", "Int"),
        ("x_provenance", "Int"),
        ("x_borrow", "Int"),
        ("x_element_size", "Int"),
    ]
    if config.callback:
        fields.extend(
            (
                ("x_predicate_identity", "Int"),
                ("x_predicate_state", "Int"),
            )
        )
    if config.limit_kind in {"chunk", "n"}:
        fields.append(("x_parameter", "Int"))
    return tuple(fields)


def _boundary_fields(config: ConstructorTarget) -> tuple[tuple[str, str], ...]:
    fields: list[tuple[str, str]] = [
        ("b_input_address", "Int"),
        ("b_input_allocation", "Int"),
        ("b_input_provenance", "Int"),
        ("b_input_borrow", "Int"),
        ("b_element_size", "Int"),
    ]
    if config.callback:
        fields.append(("b_predicate_identity", "Int"))
    return tuple(fields)


def _input_identity(config: ConstructorTarget) -> str:
    equalities = [
        "(= (b_input_address b) (x_address x))",
        "(= (b_input_allocation b) (x_allocation x))",
        "(= (b_input_provenance b) (x_provenance x))",
        "(= (b_input_borrow b) (x_borrow x))",
        "(= (b_element_size b) (x_element_size x))",
    ]
    if config.callback:
        equalities.append(
            "(= (b_predicate_identity b) (x_predicate_identity x))"
        )
    return "  (and " + "\n       ".join(equalities) + "))"


def _stored_slice_transition() -> str:
    return """\
(define-fun StoredSliceTransition ((x Input) (y Output)) Bool
  (and (= (y_source_sequence y) (x_source_sequence x))
       (= (y_source_start y) (x_source_start x))
       (= (y_source_length y) (x_length x))
       (= (y_remaining_sequence y) (x_source_sequence x))
       (= (y_remaining_start y) (x_source_start x))
       (= (y_remaining_length y) (x_length x))
       (= (y_yielded_sequence y) 0)
       (= (y_yielded_start y) 0)
       (= (y_yielded_length y) 0)
       (= (y_remainder_sequence y) 0)
       (= (y_remainder_start y) 0)
       (= (y_remainder_length y) 0)
       (= (y_address y) (x_address x))
       (= (y_allocation y) (x_allocation x))
       (= (y_provenance y) (x_provenance x))
       (= (y_borrow y) (x_borrow x))
       (= (y_element_size y) (x_element_size x))))"""


def _stored_predicate_transition() -> str:
    return """\
(define-fun StoredPredicateTransition ((x Input) (y Output)) Bool
  (and (= (y_predicate_identity y) (x_predicate_identity x))
       (= (y_predicate_state y) (x_predicate_state x))
       (= (y_callback_calls y) 0)))"""


def _raw_slice_transition() -> str:
    return """\
(define-fun MutableRawSliceCastTransition ((x Input) (y Output)) Bool
  (and (= (y_raw_address y) (x_address x))
       (= (y_raw_length y) (x_length x))
       (= (y_raw_allocation y) (x_allocation x))
       (= (y_raw_provenance y) (x_provenance x))
       (= (y_marker_borrow y) (x_borrow x))))"""


def _constructor_transitions(config: ConstructorTarget) -> str:
    reverse = "true" if config.reverse else "false"
    inclusive = "true" if config.inclusive else "false"
    limit = "(x_parameter x)" if config.limit_kind in {"chunk", "n"} else "0"
    if config.family == "adjacent":
        return f"""\
(define-fun {config.top_transition} ((x Input) (y Output)) Bool
  (and (StoredSliceTransition x y)
       (StoredPredicateTransition x y)
       (= (y_chunk_size y) 0)
       (= (y_reverse y) false)))"""
    if config.family == "chunks":
        return f"""\
(define-fun {config.top_transition} ((x Input) (y Output)) Bool
  (and (StoredSliceTransition x y)
       (MutableRawSliceCastTransition x y)
       (= (y_chunk_size y) {limit})
       (= (y_reverse y) {reverse})))"""

    finished = (
        "(= (x_length x) 0)"
        if config.finished_kind == "empty"
        else "false"
    )
    common = f"""\
       (= (y_chunk_size y) {limit})
       (= (y_reverse y) {reverse})
       (= (y_inclusive y) {inclusive})"""
    if config.constructor_name == "SplitMutNew":
        return f"""\
(define-fun SplitMutNewTransition ((x Input) (y Output)) Bool
  (and (StoredSliceTransition x y)
       (StoredPredicateTransition x y)
       (= (y_finished y) false)
{common}))"""
    if config.constructor_name == "SplitInclusiveMutNew":
        return f"""\
(define-fun SplitInclusiveMutNewTransition ((x Input) (y Output)) Bool
  (and (StoredSliceTransition x y)
       (StoredPredicateTransition x y)
       (= (y_finished y) {finished})
{common}))"""
    if config.constructor_name == "RSplitMutNew":
        return f"""\
(define-fun SplitMutNewStorageTransition ((x Input) (y Output)) Bool
  (and (StoredSliceTransition x y)
       (StoredPredicateTransition x y)
       (= (y_finished y) false)))
(define-fun RSplitMutNewTransition ((x Input) (y Output)) Bool
  (and (SplitMutNewStorageTransition x y)
{common}))"""
    if config.constructor_name == "RSplitNMutNew":
        return f"""\
(define-fun SplitMutNewStorageTransition ((x Input) (y Output)) Bool
  (and (StoredSliceTransition x y)
       (StoredPredicateTransition x y)
       (= (y_finished y) false)))
(define-fun RSplitMutNewStorageTransition ((x Input) (y Output)) Bool
  (and (SplitMutNewStorageTransition x y)
       (= (y_borrow y) (x_borrow x))))
(define-fun RSplitNMutNewTransition ((x Input) (y Output)) Bool
  (and (RSplitMutNewStorageTransition x y)
{common}
       (= (y_count y) (x_parameter x))))"""
    raise ValueError(f"unsupported predicate constructor: {config.target}")


def _state_declaration(
    config: ConstructorTarget, purpose: str
) -> str:
    if purpose == EXACT_OUTPUT:
        return "(declare-datatypes ((State 0)) (((mkState))))"
    return f"""\
(declare-datatypes ((State 0))
  (((mkState
{_record_fields(config.state_fields)}))))"""


def _final_state_transition(
    config: ConstructorTarget, purpose: str
) -> str:
    equalities = [
        "(= (s_final_slice_sequence s) (x_source_sequence x))",
        "(= (s_final_slice_start s) (x_source_start x))",
        "(= (s_final_slice_length s) (x_length x))",
        "(= (s_final_address s) (x_address x))",
        "(= (s_final_allocation s) (x_allocation x))",
        "(= (s_final_provenance s) (x_provenance x))",
        "(= (s_final_borrow s) (x_borrow x))",
        "(= (s_final_element_size s) (x_element_size x))",
    ]
    if config.callback:
        equalities.extend(
            (
                "(= (s_callback_identity s) (x_predicate_identity x))",
                "(= (s_callback_state s) (x_predicate_state x))",
                "(= (s_callback_calls s) 0)",
            )
        )
    if purpose == EXACT_OUTPUT:
        local_fields = [
            ("final_slice_sequence", "Int", "(x_source_sequence x)"),
            ("final_slice_start", "Int", "(x_source_start x)"),
            ("final_slice_length", "Int", "(x_length x)"),
            ("final_address", "Int", "(x_address x)"),
            ("final_allocation", "Int", "(x_allocation x)"),
            ("final_provenance", "Int", "(x_provenance x)"),
            ("final_borrow", "Int", "(x_borrow x)"),
            ("final_element_size", "Int", "(x_element_size x)"),
        ]
        if config.callback:
            local_fields.extend(
                (
                    (
                        "callback_identity",
                        "Int",
                        "(x_predicate_identity x)",
                    ),
                    ("callback_state", "Int", "(x_predicate_state x)"),
                    ("callback_calls", "Int", "0"),
                )
            )
        declarations = "\n     ".join(
            f"({name} {sort})" for name, sort, _ in local_fields
        )
        witnesses = "\n         ".join(
            f"(= {name} {value})" for name, _, value in local_fields
        )
        return f"""\
(define-fun ConstructorFinalStateExists ((x Input)) Bool
  (exists
    ({declarations})
    (and {witnesses})))"""
    return """\
(define-fun ConstructorFinalStateTransition
  ((x Input) (s State)) Bool
  (and %s))""" % "\n       ".join(equalities)


def _active_definitions(config: ConstructorTarget) -> str:
    limit = "(x_parameter x)" if config.limit_kind in {"chunk", "n"} else "0"
    reverse = "true" if config.reverse else "false"
    definitions = [
        """\
(define-fun ActiveWellFormedConjunct ((y Output)) Bool
  (and (>= (y_chunk_size y) 0)
       (>= (y_remainder_length y) 0)
       (<= (y_remainder_length y) (y_source_length y))))""",
        """\
(define-fun ActiveSourceConjunct ((x Input) (y Output)) Bool
  (and (= (y_source_sequence y) (x_source_sequence x))
       (= (y_source_start y) (x_source_start x))
       (= (y_source_length y) (x_length x))))""",
        """\
(define-fun ActiveRemainingConjunct ((y Output)) Bool
  (and (= (y_remaining_sequence y) (y_source_sequence y))
       (= (y_remaining_start y) (y_source_start y))
       (= (y_remaining_length y) (y_source_length y))))""",
        """\
(define-fun ActiveYieldedEmptyConjunct ((y Output)) Bool
  (and (= (y_yielded_sequence y) 0)
       (= (y_yielded_start y) 0)
       (= (y_yielded_length y) 0)))""",
        """\
(define-fun ActiveRemainderEmptyConjunct ((y Output)) Bool
  (and (= (y_remainder_sequence y) 0)
       (= (y_remainder_start y) 0)
       (= (y_remainder_length y) 0)))""",
        f"""\
(define-fun ActiveChunkSizeConjunct ((x Input) (y Output)) Bool
  (= (y_chunk_size y) {limit}))""",
        f"""\
(define-fun ActiveReverseConjunct ((y Output)) Bool
  (= (y_reverse y) {reverse}))""",
        """\
(define-fun ActiveCompositionConjunct ((y Output)) Bool
  (and (= (y_yielded_length y) 0)
       (= (y_remaining_sequence y) (y_source_sequence y))
       (= (y_remaining_start y) (y_source_start y))
       (= (y_remaining_length y) (y_source_length y))))""",
    ]
    if config.family == "chunks":
        definitions.insert(
            0,
            """\
(define-fun ActiveChunkDomainConjunct ((x Input)) Bool
  (> (x_parameter x) 0))""",
        )
    elif config.callback_kind == "adjacent":
        definitions.append(
            """\
(define-fun ActiveAdjacentPredicateTotalityConjunct ((x Input)) Bool
  (forall ((i Int))
    (=>
      (and (>= i 0) (< (+ i 1) (x_length x)))
      (or (= i i) (not (= i i))))))"""
        )
    else:
        definitions.extend(
            (
                """\
(define-fun ActiveLimitNonnegativeConjunct ((y Output)) Bool
  (>= (y_chunk_size y) 0))""",
                """\
(define-fun ActivePredicateTotalityConjunct ((x Input)) Bool
  (forall ((i Int))
    (=>
      (and (>= i 0) (< i (x_length x)))
      (or (= i i) (not (= i i))))))""",
            )
        )
    return "\n".join(definitions)


def _requires(config: ConstructorTarget) -> str:
    clauses = [
        "(>= (x_source_sequence x) 0)",
        "(>= (x_source_start x) 0)",
        "(>= (x_length x) 0)",
        "(>= (x_address x) 0)",
        "(>= (x_allocation x) 0)",
        "(>= (x_provenance x) 0)",
        "(>= (x_borrow x) 0)",
        "(>= (x_element_size x) 0)",
    ]
    if config.callback:
        clauses.append("(>= (x_predicate_identity x) 0)")
    if config.limit_kind == "chunk":
        clauses.append("(ActiveChunkDomainConjunct x)")
    elif config.limit_kind == "n":
        clauses.append("(>= (x_parameter x) 0)")
    return "  (and " + "\n       ".join(clauses) + "))"


def _boundary(config: ConstructorTarget) -> str:
    clauses = [
        "(>= (b_input_address b) 0)",
        "(>= (b_input_allocation b) 0)",
        "(>= (b_input_provenance b) 0)",
        "(>= (b_input_borrow b) 0)",
        "(>= (b_element_size b) 0)",
    ]
    if config.callback:
        clauses.append("(>= (b_predicate_identity b) 0)")
    clauses.append("(InputIdentityObserved x b)")
    return "  (and " + "\n       ".join(clauses) + "))"


def _target_definition(
    config: ConstructorTarget, purpose: str
) -> str:
    calls = ["(InputIdentityObserved x b)"]
    for transition in config.source_transitions:
        if transition == "ConstructorFinalStateTransition":
            if purpose == PRIMARY:
                calls.append("(ConstructorFinalStateTransition x s)")
            continue
        calls.append(f"({transition} x y)")
    if purpose == EXACT_OUTPUT:
        calls.append("(ConstructorFinalStateExists x)")
    for conjunct in config.active_conjuncts:
        args = "(x y)" if conjunct in {
            "ActiveSourceConjunct",
            "ActiveChunkSizeConjunct",
        } else "(x)" if conjunct in {
            "ActiveChunkDomainConjunct",
            "ActiveAdjacentPredicateTotalityConjunct",
            "ActivePredicateTotalityConjunct",
        } else "(y)"
        calls.append(f"({conjunct} {args[1:-1]})")
    return """\
(define-fun TargetDefinition_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and %s))""" % "\n       ".join(calls)


def _equivalence(config: ConstructorTarget, purpose: str) -> str:
    equalities = [
        f"(= ({selector} y1) ({selector} y2))"
        for selector, _ in config.output_fields
    ]
    if purpose == PRIMARY:
        equalities.extend(
            f"(= ({selector} s1) ({selector} s2))"
            for selector, _ in config.state_fields
        )
    return """\
(define-fun Equivalent_T
  ((x Input) (b Boundary)
   (y1 Output) (s1 State) (y2 Output) (s2 State)) Bool
  (and %s))""" % "\n       ".join(equalities)


def _model_text(
    config: ConstructorTarget,
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
; Arbitrary valid slice length; boundary contains input identities only.
(set-logic ALL)
(declare-datatypes ((Input 0))
  (((mkInput
{_record_fields(_input_fields(config))}))))
(declare-datatypes ((Boundary 0))
  (((mkBoundary
{_record_fields(_boundary_fields(config))}))))
(declare-datatypes ((Output 0))
  (((mkOutput
{_record_fields(config.output_fields)}))))
{_state_declaration(config, purpose)}
(declare-const x Input)
(declare-const b Boundary)
(declare-const y1 Output)
(declare-const s1 State)
(declare-const y2 Output)
(declare-const s2 State)
(define-fun InputIdentityObserved ((x Input) (b Boundary)) Bool
{_input_identity(config)}
{_stored_slice_transition()}
{_stored_predicate_transition() if config.callback else ""}
{_raw_slice_transition() if config.family == "chunks" else ""}
{_constructor_transitions(config)}
{_final_state_transition(config, purpose)}
{_active_definitions(config)}
(define-fun Requires_T ((x Input)) Bool
{_requires(config)}
(define-fun Boundary_T ((x Input) (b Boundary)) Bool
{_boundary(config)}
{_target_definition(config, purpose)}
(define-fun Spec_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (TargetDefinition_T x b y s))
{_equivalence(config, purpose)}
{theorem}"""


def obligation_text(config: ConstructorTarget, purpose: str) -> str:
    return _model_text(config, purpose, include_theorem=True)


def _principal_observations(
    config: ConstructorTarget, purpose: str
) -> list[dict[str, str]]:
    observations = [
        {
            "selector": selector,
            "left": "output1",
            "right": "output2",
            "sort": sort,
        }
        for selector, sort in config.output_fields
    ]
    if purpose == PRIMARY:
        observations.extend(
            {
                "selector": selector,
                "left": "state1",
                "right": "state2",
                "sort": sort,
            }
            for selector, sort in config.state_fields
        )
    return observations


def _boundary_metadata(config: ConstructorTarget) -> list[dict[str, Any]]:
    citations = [
        config.source_reference,
        *(source.citation for source in config.private_sources),
    ]
    fields = [
        ("b_input_address", "input_memory"),
        ("b_input_allocation", "input_provenance"),
        ("b_input_provenance", "input_provenance"),
        ("b_input_borrow", "input_provenance"),
        ("b_element_size", "input_layout"),
    ]
    result = [
        {
            "selector": selector,
            "role": role,
            "source_citations": citations,
            "trust_site_ids": list(config.data_trust_site_ids),
        }
        for selector, role in fields
    ]
    if config.callback:
        result.append(
            {
                "selector": "b_predicate_identity",
                "role": "callback_argument",
                "source_citations": citations,
                "trust_site_ids": list(config.callback_trust_site_ids),
            }
        )
    return result


def obligation_metadata(
    config: ConstructorTarget, purpose: str
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
            "element_size": (
                "arbitrary nonnegative integer; zero-sized types are included"
            ),
            "chunk_size": (
                "arbitrary positive integer"
                if config.limit_kind == "chunk"
                else "not applicable"
            ),
            "n": (
                "arbitrary nonnegative integer"
                if config.limit_kind == "n"
                else "not applicable"
            ),
            "callback": (
                "arbitrary callable identity and initial state; zero calls"
                if config.callback
                else "not applicable"
            ),
        },
        "active_contract_conjuncts": list(config.active_conjuncts),
        "contract_translation": {
            "constructor_chain": list(config.constructor_chain),
            "reverse": config.reverse,
            "inclusive": config.inclusive,
            "limit_kind": config.limit_kind,
            "finished_kind": config.finished_kind,
            "constructor_callback_invocations": 0,
            "callback_totality": (
                "The generated callback formula is classical totality only; "
                "no callback result or transition is observed at construction."
                if config.callback
                else "not applicable"
            ),
        },
        "boundary_scope": {
            "shared_observations": [
                field["selector"] for field in _boundary_metadata(config)
            ],
            "admitted_trust_site_ids": list(config.dependency_trust_site_ids),
            "context_only_trust_site_ids": list(
                config.context_only_trust_site_ids
            ),
            "excluded_observations": [
                "returned iterator or private state",
                "selected source, remaining, yielded, or remainder ranges",
                "chunk-size, direction, inclusive, count, or finished defaults",
                "callback results or constructor-time state transitions",
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
            or transition != "ConstructorFinalStateTransition"
        ],
        "source_transition_bindings": {
            "public_wrapper": {
                "operation": config.target,
                "source_citations": [config.source_reference],
                "trust_site_ids": list(config.dependency_trust_site_ids),
            },
            "private_constructor_chain": {
                "operations": list(config.constructor_chain),
                "source_citations": [
                    source.citation for source in config.private_sources
                ],
                "trust_site_ids": list(config.all_trust_site_ids),
            },
            "immediate_final_state": {
                "operation": "ConstructorFinalStateTransition",
                "semantics": (
                    "constructor moves the borrow/callable into the iterator "
                    "without reading or mutating elements and performs zero calls"
                    if config.callback
                    else "constructor casts/stores the input slice without "
                    "reading or mutating elements"
                ),
                "source_citations": [
                    config.source_reference,
                    *(source.citation for source in config.private_sources),
                ],
                "trust_site_ids": list(config.dependency_trust_site_ids),
            },
        },
        "equivalence_kind": "exact",
        "equivalence_scope": (
            "every returned view/private iterator/reference identity and "
            "immediate final-state observation"
            if purpose == PRIMARY
            else "every returned view/private iterator/reference identity"
        ),
        "principal_observations": _principal_observations(config, purpose),
        "expected_solver_result": "unsat",
    }


def obligation(
    config: ConstructorTarget, purpose: str
) -> tuple[str, dict[str, Any]]:
    return obligation_text(config, purpose), obligation_metadata(config, purpose)


def validate_target_obligation(
    config: ConstructorTarget, text: str, metadata: dict[str, Any]
) -> None:
    validate_obligation(text, metadata)
    purpose = metadata.get("obligation_purpose")
    if purpose not in PURPOSES:
        raise GuardError(f"{config.target}: unknown obligation purpose")
    expected_text, expected_metadata = obligation(config, str(purpose))
    if metadata != expected_metadata:
        raise GuardError(
            f"{config.target}: metadata differs from reviewed constructor model"
        )
    if parse_smt(text) != parse_smt(expected_text):
        raise GuardError(
            f"{config.target}: SMT differs from reviewed constructor model"
        )


def source_instance_text(
    config: ConstructorTarget,
    *,
    length: int,
    element_size: int,
    extra_assertions: tuple[str, ...] = (),
) -> str:
    if length < 0 or element_size < 0:
        raise ValueError("source instance length and element size must be nonnegative")
    assertions = [
        "(assert (Requires_T x))",
        "(assert (Boundary_T x b))",
        "(assert (Spec_T x b y1 s1))",
        f"(assert (= (x_length x) {length}))",
        f"(assert (= (x_element_size x) {element_size}))",
    ]
    if config.limit_kind == "chunk":
        assertions.append("(assert (= (x_parameter x) 3))")
    elif config.limit_kind == "n":
        assertions.append("(assert (= (x_parameter x) 4))")
    assertions.extend(f"(assert {assertion})" for assertion in extra_assertions)
    return (
        _model_text(config, PRIMARY, include_theorem=False)
        + "\n"
        + "\n".join(assertions)
        + "\n(check-sat)\n"
    )


def boundary_manifest(config: ConstructorTarget) -> dict[str, Any]:
    observations = []
    meanings = {
        "b_input_address": "input slice data address",
        "b_input_allocation": "allocation identity backing the input slice",
        "b_input_provenance": "raw/reference provenance of the input slice",
        "b_input_borrow": "input mutable-borrow identity",
        "b_element_size": "input element layout size, including zero",
        "b_predicate_identity": "callable identity moved into the iterator",
    }
    for field in _boundary_metadata(config):
        observations.append(
            {
                "field": field["selector"],
                "meaning": meanings[field["selector"]],
                "role": field["role"],
                "trust_site_ids": field["trust_site_ids"],
            }
        )
    return {
        "schema_version": 1,
        "target": config.target,
        "input_order": config.input_order,
        "boundary_narrower_than_target": True,
        "shared_boundary_observations": observations,
        "private_constructor_chain": [
            {
                "operation": name,
                "source": source.citation,
            }
            for name, source in zip(
                config.constructor_chain, config.private_sources
            )
        ],
        "deterministic_source_transition": {
            "symbol": config.top_transition,
            "preserves_address_allocation_provenance_and_borrow": True,
            "preserves_input_sequence_and_length": True,
            "chunk_size": config.limit_kind,
            "reverse": config.reverse,
            "inclusive": config.inclusive,
            "finished": config.finished_kind,
            "constructor_callback_invocations": 0,
        },
        "dependency_trust_site_ids": list(config.dependency_trust_site_ids),
        "context_only_trust_site_ids": list(
            config.context_only_trust_site_ids
        ),
        "all_audited_trust_site_ids": list(config.all_trust_site_ids),
        "excluded_from_boundary": [
            "returned iterator and private iterator state",
            "source/remaining/yielded/remainder view values",
            "raw pointer returned-state fields",
            "callback results and final callback state",
            "direction, inclusive, count, chunk-size, and finished defaults",
            "final slice state",
            "answer-equivalent values and execution traces",
        ],
    }


def _verus_common(config: ConstructorTarget) -> str:
    target_name = config.target.rsplit("::", 1)[-1]
    return f"""\
#![allow(dead_code, unused_imports, unused_variables)]
// Generated source-backed constructor model for {config.target}.

use vstd::prelude::*;
use vstd::seq::*;

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

pub open spec fn same_slice(left: SliceIdentity, right: SliceIdentity) -> bool {{
    left.source == right.source
        && left.start == right.start
        && left.address == right.address
        && left.allocation == right.allocation
        && left.provenance == right.provenance
        && left.borrow == right.borrow
        && left.element_size == right.element_size
}}

// Target proof prefix: {target_name}
"""


def _verus_chunks(config: ConstructorTarget) -> str:
    reverse = "true" if config.reverse else "false"
    function = config.target.rsplit("::", 1)[-1]
    return _verus_common(config) + f"""\
pub ghost struct Input {{
    pub slice: SliceIdentity,
    pub chunk_size: nat,
}}

pub ghost struct RawSliceIdentity {{
    pub address: int,
    pub length: nat,
    pub allocation: int,
    pub provenance: int,
}}

pub ghost struct ChunkIterator {{
    pub raw: RawSliceIdentity,
    pub marker_borrow: int,
    pub source: Seq<int>,
    pub remaining: Seq<int>,
    pub yielded_prefix: Seq<int>,
    pub remainder: Seq<int>,
    pub chunk_size: nat,
    pub reverse: bool,
    pub element_size: nat,
}}

pub ghost struct FinalState {{
    pub slice: SliceIdentity,
}}

pub open spec fn mutable_raw_slice_cast(
    slice: SliceIdentity,
) -> RawSliceIdentity {{
    RawSliceIdentity {{
        address: slice.address,
        length: slice.source.len(),
        allocation: slice.allocation,
        provenance: slice.provenance,
    }}
}}

pub open spec fn output_transition(input: Input, iter: ChunkIterator) -> bool {{
    iter.raw.address == input.slice.address
        && iter.raw.length == input.slice.source.len()
        && iter.raw.allocation == input.slice.allocation
        && iter.raw.provenance == input.slice.provenance
        && iter.marker_borrow == input.slice.borrow
        && iter.source == input.slice.source
        && iter.remaining == input.slice.source
        && iter.yielded_prefix == Seq::<int>::empty()
        && iter.remainder == Seq::<int>::empty()
        && iter.chunk_size == input.chunk_size
        && iter.reverse == {reverse}
        && iter.element_size == input.slice.element_size
}}

pub open spec fn active_contract(input: Input, iter: ChunkIterator) -> bool {{
    input.chunk_size > 0
        && iter.source == input.slice.source
        && iter.remaining == input.slice.source
        && iter.yielded_prefix == Seq::<int>::empty()
        && iter.remainder == Seq::<int>::empty()
        && iter.chunk_size == input.chunk_size
        && iter.reverse == {reverse}
}}

pub open spec fn final_state_transition(
    input: Input,
    state: FinalState,
) -> bool {{
    same_slice(state.slice, input.slice)
}}

pub open spec fn target_transition(
    input: Input,
    iter: ChunkIterator,
    state: FinalState,
) -> bool {{
    output_transition(input, iter)
        && active_contract(input, iter)
        && final_state_transition(input, state)
}}

pub proof fn {function}_constructor(
    input: Input,
) -> (ret: ChunkIterator)
    requires
        input.chunk_size > 0,
    ensures
        output_transition(input, ret),
        active_contract(input, ret),
{{
    let raw = mutable_raw_slice_cast(input.slice);
    ChunkIterator {{
        raw,
        marker_borrow: input.slice.borrow,
        source: input.slice.source,
        remaining: input.slice.source,
        yielded_prefix: Seq::empty(),
        remainder: Seq::empty(),
        chunk_size: input.chunk_size,
        reverse: {reverse},
        element_size: input.slice.element_size,
    }}
}}

pub open spec fn exact_equivalent(
    left: ChunkIterator,
    left_state: FinalState,
    right: ChunkIterator,
    right_state: FinalState,
) -> bool {{
    left.raw.address == right.raw.address
        && left.raw.length == right.raw.length
        && left.raw.allocation == right.raw.allocation
        && left.raw.provenance == right.raw.provenance
        && left.marker_borrow == right.marker_borrow
        && left.source == right.source
        && left.remaining == right.remaining
        && left.yielded_prefix == right.yielded_prefix
        && left.remainder == right.remainder
        && left.chunk_size == right.chunk_size
        && left.reverse == right.reverse
        && left.element_size == right.element_size
        && same_slice(left_state.slice, right_state.slice)
}}

pub proof fn conditional_complete_{function}(
    input: Input,
    iter1: ChunkIterator,
    state1: FinalState,
    iter2: ChunkIterator,
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
}}

}} // verus!
"""


def _verus_nested_reverse_model(
    config: ConstructorTarget,
) -> tuple[str, str]:
    if config.artifact_id == "074_core_slice_rsplit_mut":
        return (
            """\
pub ghost struct SplitMutStorage {
    pub slice: SliceIdentity,
    pub predicate: PredicateSnapshot,
    pub finished: bool,
}

pub ghost struct RSplitMutStorage {
    pub inner: SplitMutStorage,
}

pub open spec fn split_mut_new(input: Input) -> SplitMutStorage {
    SplitMutStorage {
        slice: input.slice,
        predicate: input.predicate,
        finished: false,
    }
}

pub open spec fn rsplit_mut_new(input: Input) -> RSplitMutStorage {
    RSplitMutStorage {
        inner: split_mut_new(input),
    }
}

pub open spec fn project_rsplit_mut(
    storage: RSplitMutStorage,
) -> MutableIterator {
    MutableIterator {
        slice: storage.inner.slice,
        predicate: storage.inner.predicate,
        source: storage.inner.slice.source,
        remaining: storage.inner.slice.source,
        yielded_prefix: Seq::empty(),
        remainder: Seq::empty(),
        limit: 0,
        reverse: true,
        finished: storage.inner.finished,
        inclusive: false,
        callback_calls: 0,
    }
}

pub proof fn rsplit_mut_flat_projection(input: Input)
    ensures
        output_transition(
            input,
            project_rsplit_mut(rsplit_mut_new(input)),
        ),
{
    reveal(output_transition);
    reveal(same_slice);
    reveal(same_predicate);
}
""",
            """\
    rsplit_mut_flat_projection(input);
    let ret = project_rsplit_mut(rsplit_mut_new(input));""",
        )
    if config.artifact_id == "076_core_slice_rsplitn_mut":
        return (
            """\
pub ghost struct SplitMutStorage {
    pub slice: SliceIdentity,
    pub predicate: PredicateSnapshot,
    pub finished: bool,
}

pub ghost struct RSplitMutStorage {
    pub inner: SplitMutStorage,
}

pub ghost struct GenericSplitNStorage {
    pub iter: RSplitMutStorage,
    pub count: nat,
}

pub ghost struct RSplitNMutStorage {
    pub inner: GenericSplitNStorage,
}

pub open spec fn split_mut_new(input: Input) -> SplitMutStorage {
    SplitMutStorage {
        slice: input.slice,
        predicate: input.predicate,
        finished: false,
    }
}

pub open spec fn rsplit_mut_new(input: Input) -> RSplitMutStorage {
    RSplitMutStorage {
        inner: split_mut_new(input),
    }
}

pub open spec fn rsplitn_mut_new(input: Input) -> RSplitNMutStorage {
    RSplitNMutStorage {
        inner: GenericSplitNStorage {
            iter: rsplit_mut_new(input),
            count: input.n,
        },
    }
}

pub open spec fn project_rsplitn_mut(
    storage: RSplitNMutStorage,
) -> MutableIterator {
    MutableIterator {
        slice: storage.inner.iter.inner.slice,
        predicate: storage.inner.iter.inner.predicate,
        source: storage.inner.iter.inner.slice.source,
        remaining: storage.inner.iter.inner.slice.source,
        yielded_prefix: Seq::empty(),
        remainder: Seq::empty(),
        limit: storage.inner.count,
        reverse: true,
        finished: storage.inner.iter.inner.finished,
        inclusive: false,
        callback_calls: 0,
    }
}

pub proof fn rsplitn_mut_flat_projection(input: Input)
    ensures
        output_transition(
            input,
            project_rsplitn_mut(rsplitn_mut_new(input)),
        ),
{
    reveal(output_transition);
    reveal(same_slice);
    reveal(same_predicate);
}
""",
            """\
    rsplitn_mut_flat_projection(input);
    let ret = project_rsplitn_mut(rsplitn_mut_new(input));""",
        )
    return "", ""


def _verus_callback(config: ConstructorTarget) -> str:
    reverse = "true" if config.reverse else "false"
    inclusive = "true" if config.inclusive else "false"
    function = config.target.rsplit("::", 1)[-1]
    adjacent = config.callback_kind == "adjacent"
    has_limit = config.limit_kind == "n"
    parameter = "    pub n: nat,\n" if has_limit else ""
    limit = "input.n" if has_limit else "0"
    finished = (
        "(input.slice.source.len() == 0)"
        if config.finished_kind == "empty"
        else "false"
    )
    extra_struct = (
        ""
        if adjacent
        else """\
    pub finished: bool,
    pub inclusive: bool,
"""
    )
    extra_transition = (
        ""
        if adjacent
        else f"""\
        && iter.finished == {finished}
        && iter.inclusive == {inclusive}
"""
    )
    exact_extra = (
        ""
        if adjacent
        else """\
        && left.finished == right.finished
        && left.inclusive == right.inclusive
"""
    )
    extra_initializer = (
        ""
        if adjacent
        else f"""\
        finished: {finished},
        inclusive: {inclusive},
"""
    )
    nested_model, constructor_setup = _verus_nested_reverse_model(config)
    if not constructor_setup:
        constructor_setup = f"""\
    let ret = MutableIterator {{
        slice: input.slice,
        predicate: input.predicate,
        source: input.slice.source,
        remaining: input.slice.source,
        yielded_prefix: Seq::empty(),
        remainder: Seq::empty(),
        limit: {limit},
        reverse: {reverse},
{extra_initializer}        callback_calls: 0,
    }};"""
    if adjacent:
        observation_declaration = """\
pub uninterp spec fn adjacent_predicate_observed(
    predicate_identity: int,
    left: int,
    right: int,
) -> bool;
"""
        callback_totality = """\
        && forall|i: int|
            #![trigger adjacent_predicate_observed(
                input.predicate.identity,
                input.slice.source[i],
                input.slice.source[i + 1],
            )]
            0 <= i && i + 1 < input.slice.source.len()
            ==> (adjacent_predicate_observed(
                    input.predicate.identity,
                    input.slice.source[i],
                    input.slice.source[i + 1],
                )
                || !adjacent_predicate_observed(
                    input.predicate.identity,
                    input.slice.source[i],
                    input.slice.source[i + 1],
                ))
"""
        proof_quantifier = """\
    assert forall|i: int|
        #![trigger adjacent_predicate_observed(
            input.predicate.identity,
            input.slice.source[i],
            input.slice.source[i + 1],
        )]
        0 <= i && i + 1 < input.slice.source.len() implies
        (adjacent_predicate_observed(
                input.predicate.identity,
                input.slice.source[i],
                input.slice.source[i + 1],
            )
            || !adjacent_predicate_observed(
                input.predicate.identity,
                input.slice.source[i],
                input.slice.source[i + 1],
            )) by {{}}
"""
    else:
        observation_declaration = """\
pub uninterp spec fn predicate_observed(
    predicate_identity: int,
    value: int,
) -> bool;
"""
        callback_totality = """\
        && forall|i: int|
            #![trigger predicate_observed(
                input.predicate.identity,
                input.slice.source[i],
            )]
            0 <= i < input.slice.source.len()
            ==> (predicate_observed(
                    input.predicate.identity,
                    input.slice.source[i],
                )
                || !predicate_observed(
                    input.predicate.identity,
                    input.slice.source[i],
                ))
"""
        proof_quantifier = """\
    assert forall|i: int|
        #![trigger predicate_observed(
            input.predicate.identity,
            input.slice.source[i],
        )]
        0 <= i < input.slice.source.len() implies
        (predicate_observed(
                input.predicate.identity,
                input.slice.source[i],
            )
            || !predicate_observed(
                input.predicate.identity,
                input.slice.source[i],
            )) by {{}}
"""
    return _verus_common(config) + f"""\
pub ghost struct PredicateSnapshot {{
    pub identity: int,
    pub state: int,
}}

{observation_declaration}
pub ghost struct Input {{
    pub slice: SliceIdentity,
    pub predicate: PredicateSnapshot,
{parameter}}}

pub ghost struct MutableIterator {{
    pub slice: SliceIdentity,
    pub predicate: PredicateSnapshot,
    pub source: Seq<int>,
    pub remaining: Seq<int>,
    pub yielded_prefix: Seq<int>,
    pub remainder: Seq<int>,
    pub limit: nat,
    pub reverse: bool,
{extra_struct}    pub callback_calls: nat,
}}

pub ghost struct FinalState {{
    pub slice: SliceIdentity,
    pub predicate_identity: int,
    pub predicate_state: int,
    pub callback_calls: nat,
}}

pub open spec fn same_predicate(
    left: PredicateSnapshot,
    right: PredicateSnapshot,
) -> bool {{
    left.identity == right.identity && left.state == right.state
}}

pub open spec fn output_transition(input: Input, iter: MutableIterator) -> bool {{
    same_slice(iter.slice, input.slice)
        && same_predicate(iter.predicate, input.predicate)
        && iter.source == input.slice.source
        && iter.remaining == input.slice.source
        && iter.yielded_prefix == Seq::<int>::empty()
        && iter.remainder == Seq::<int>::empty()
        && iter.limit == {limit}
        && iter.reverse == {reverse}
{extra_transition}        && iter.callback_calls == 0
}}

{nested_model}
pub open spec fn active_contract(input: Input, iter: MutableIterator) -> bool {{
    iter.source == input.slice.source
        && iter.remaining == input.slice.source
        && iter.yielded_prefix == Seq::<int>::empty()
        && iter.remainder == Seq::<int>::empty()
        && iter.limit == {limit}
        && iter.reverse == {reverse}
        && iter.yielded_prefix + iter.remaining == input.slice.source
{callback_totality}}}

pub open spec fn final_state_transition(
    input: Input,
    state: FinalState,
) -> bool {{
    same_slice(state.slice, input.slice)
        && state.predicate_identity == input.predicate.identity
        && state.predicate_state == input.predicate.state
        && state.callback_calls == 0
}}

pub open spec fn target_transition(
    input: Input,
    iter: MutableIterator,
    state: FinalState,
) -> bool {{
    output_transition(input, iter)
        && active_contract(input, iter)
        && final_state_transition(input, state)
}}

pub proof fn {function}_constructor(
    input: Input,
) -> (ret: MutableIterator)
    ensures
        output_transition(input, ret),
        active_contract(input, ret),
{{
{constructor_setup}
    reveal(active_contract);
    assert(Seq::<int>::empty() + input.slice.source == input.slice.source);
{proof_quantifier}
    ret
}}

pub open spec fn exact_equivalent(
    left: MutableIterator,
    left_state: FinalState,
    right: MutableIterator,
    right_state: FinalState,
) -> bool {{
    same_slice(left.slice, right.slice)
        && same_predicate(left.predicate, right.predicate)
        && left.source == right.source
        && left.remaining == right.remaining
        && left.yielded_prefix == right.yielded_prefix
        && left.remainder == right.remainder
        && left.limit == right.limit
        && left.reverse == right.reverse
{exact_extra}        && left.callback_calls == right.callback_calls
        && same_slice(left_state.slice, right_state.slice)
        && left_state.predicate_identity == right_state.predicate_identity
        && left_state.predicate_state == right_state.predicate_state
        && left_state.callback_calls == right_state.callback_calls
}}

pub proof fn conditional_complete_{function}(
    input: Input,
    iter1: MutableIterator,
    state1: FinalState,
    iter2: MutableIterator,
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
}}

}} // verus!
"""


def verus_text(config: ConstructorTarget) -> str:
    if config.family == "chunks":
        return _verus_chunks(config)
    return _verus_callback(config)
