#!/usr/bin/env python3
"""Source-backed obligations for four mutable Slice edge operations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from checker_guards import GuardError, parse_smt, validate_obligation


PRIMARY = "completeness-modulo-reviewed-equivalence"
EXACT_OUTPUT = "exact-output-determinism"
PURPOSES = (PRIMARY, EXACT_OUTPUT)

CANONICAL_SOURCE_PATH = "core/src/slice/mod.rs"
CANONICAL_SOURCE_SHA256 = (
    "58901fa6437dbd4d77c68427bbced0fc3a91a10fdb8bd2e233adf6a9ba27d2d5"
)
VOCABULARY_RANGES = ((887, 903),)

EMPTY_SEQ = "(as seq.empty (Seq Int))"


@dataclass(frozen=True)
class EdgeTarget:
    target: str
    input_order: str
    artifact_id: str
    active_contract_sha256: str
    active_contract_text: str
    edge: str
    wrapper: bool
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

    @property
    def function_name(self) -> str:
        return self.target.rsplit("::", 1)[-1]

    @property
    def source_reference(self) -> str:
        return (
            f"{CANONICAL_SOURCE_PATH}:{self.source_start}-{self.source_end}"
        )

    @property
    def docs_reference(self) -> str:
        return f"{CANONICAL_SOURCE_PATH}:{self.docs_start}-{self.docs_end}"

    @property
    def vocabulary_name(self) -> str | None:
        if not self.wrapper:
            return None
        return f"slice_split_off_{self.edge}_result"

    @property
    def selected_index(self) -> str:
        if self.edge == "first":
            return "0"
        return "(- (x_length x) 1)"

    @property
    def remainder_offset(self) -> str:
        return "1" if self.edge == "first" else "0"

    @property
    def frame_order(self) -> str:
        return "selected-then-remainder" if self.edge == "first" else (
            "remainder-then-selected"
        )

    @property
    def output_fields(self) -> tuple[tuple[str, str], ...]:
        fields: list[tuple[str, str]] = [
            ("y_is_some", "Bool"),
            ("y_selected_index", "Int"),
            ("y_selected_start", "Int"),
            ("y_selected_value", "Int"),
            ("y_selected_address", "Int"),
            ("y_selected_allocation", "Int"),
            ("y_selected_provenance", "Int"),
            ("y_selected_parent_borrow", "Int"),
            ("y_selected_element_size", "Int"),
            ("y_selected_projection", "Int"),
        ]
        if not self.wrapper:
            fields.extend(
                (
                    ("y_tuple_selected_first", "Bool"),
                    ("y_remainder_sequence", "(Seq Int)"),
                    ("y_remainder_start", "Int"),
                    ("y_remainder_length", "Int"),
                    ("y_remainder_address", "Int"),
                    ("y_remainder_allocation", "Int"),
                    ("y_remainder_provenance", "Int"),
                    ("y_remainder_parent_borrow", "Int"),
                    ("y_remainder_element_size", "Int"),
                    ("y_remainder_projection", "Int"),
                )
            )
        return tuple(fields)

    @property
    def state_fields(self) -> tuple[tuple[str, str], ...]:
        return (
            ("s_receiver_sequence", "(Seq Int)"),
            ("s_receiver_start", "Int"),
            ("s_receiver_length", "Int"),
            ("s_receiver_address", "Int"),
            ("s_receiver_allocation", "Int"),
            ("s_receiver_provenance", "Int"),
            ("s_receiver_borrow", "Int"),
            ("s_receiver_element_size", "Int"),
            ("s_receiver_projection", "Int"),
            ("s_backing_sequence", "(Seq Int)"),
            ("s_selected_final_value", "Int"),
            ("s_remainder_final_sequence", "(Seq Int)"),
        )

    @property
    def boundary_fields(self) -> tuple[tuple[str, str], ...]:
        fields: list[tuple[str, str]] = [
            ("b_input_address", "Int"),
            ("b_input_allocation", "Int"),
            ("b_input_provenance", "Int"),
            ("b_input_borrow", "Int"),
            ("b_element_size", "Int"),
        ]
        if self.wrapper:
            fields.extend(
                (
                    ("b_empty_address", "Int"),
                    ("b_empty_allocation", "Int"),
                    ("b_empty_provenance", "Int"),
                    ("b_empty_borrow", "Int"),
                )
            )
        return tuple(fields)

    @property
    def active_conjuncts(self) -> tuple[str, ...]:
        common = (
            "ActiveEmptyTagConjunct",
            "ActiveEmptyReceiverConjunct",
            "ActiveNonemptyTagConjunct",
            "ActiveSelectedValueConjunct",
        )
        if self.wrapper:
            return common + (
                "ActiveVocabularyConjunct",
                "ActiveLengthCompositionConjunct",
                "ActiveDisjointnessConjunct",
            )
        return common + (
            "ActiveRemainderConjunct",
            "ActiveFinalFrameConjunct",
            "ActiveDisjointnessConjunct",
        )

    @property
    def source_transitions(self) -> tuple[str, ...]:
        if self.wrapper:
            split = (
                "SplitFirstTransition"
                if self.edge == "first"
                else "SplitLastTransition"
            )
            return (
                "ReplaceWithEmptyTransition",
                split,
                "ReceiverAssignmentTransition",
                "OrderedWrapperTransition",
                "TargetSourceTransition",
            )
        split = (
            "SplitFirstMutTransition"
            if self.edge == "first"
            else "SplitLastMutTransition"
        )
        return (split, "TargetSourceTransition")

    @property
    def dependency_trust_site_ids(self) -> tuple[str, ...]:
        return tuple(site for site in self.all_trust_site_ids if "-D" in site)


TARGETS = (
    EdgeTarget(
        target="core::slice::split_first_mut",
        input_order="91",
        artifact_id="091_core_slice_split_first_mut",
        active_contract_sha256=(
            "ba139fadbde88d928fe18d330586ce8184d3de7a0d45938733e7231bd1320b11"
        ),
        active_contract_text=(
            "pub assume_specification<T>[ <[T]>::split_first_mut ]( slice: "
            "&mut [T], ) -> (ret: Option<(&mut T, &mut [T])>) ensures "
            "old(slice)@.len() == 0 ==> ret.is_none() && final(slice)@ == "
            "old(slice)@, old(slice)@.len() != 0 ==> ret.is_some() && "
            "*ret.unwrap().0 == old(slice)@[0] && ret.unwrap().1@ == "
            "old(slice)@.subrange(1, old(slice)@.len() as int) && "
            "final(slice)@ == seq![*final(ret.unwrap().0)] + "
            "final(ret.unwrap().1)@, ;"
        ),
        edge="first",
        wrapper=False,
        source_start=220,
        source_end=222,
        docs_start=202,
        docs_end=215,
        source_item_sha256=(
            "8d6d5b36d373d9e4556d437c6945a36066ed634bd2931a95cbb07d5197b5c3b4"
        ),
        generated_declaration_sha256=(
            "7f1740919cbe99b92c55225e25bb5c77610e261ee105411c0d3f0943360ca68d"
        ),
        harness_sha256=(
            "22105e1da4c34b18a1bfe597e3426d90da1321e6ef82dab1d6643ff75755de8a"
        ),
        source_body_manifest_sha256=(
            "45f129d73e7ffe7f3a6f2d32411dd504529e07d0093624e32ccc7d448c255e29"
        ),
        transformation_manifest_sha256=(
            "3cff008c6c01e0b652035043b6e15e294df35700ab395c71fa68904e1f3eccb9"
        ),
        dependency_manifest_sha256=(
            "27730e9ae50e859c6d6b3982c73d0f0da30da64004413e2e02fa17f68126d49d"
        ),
        all_trust_site_ids=("TS-091-D001",),
    ),
    EdgeTarget(
        target="core::slice::split_last_mut",
        input_order="97",
        artifact_id="097_core_slice_split_last_mut",
        active_contract_sha256=(
            "3039d0b8c54beb0cb99102305eb5e9b69b95dbbfd6839f26a149c9198ca962d6"
        ),
        active_contract_text=(
            "pub assume_specification<T>[ <[T]>::split_last_mut ]( slice: "
            "&mut [T], ) -> (ret: Option<(&mut T, &mut [T])>) ensures "
            "old(slice)@.len() == 0 ==> ret.is_none() && final(slice)@ == "
            "old(slice)@, old(slice)@.len() != 0 ==> ret.is_some() && "
            "*ret.unwrap().0 == old(slice)@[(old(slice)@.len() - 1) as int] "
            "&& ret.unwrap().1@ == old(slice)@.subrange(0, "
            "(old(slice)@.len() - 1) as int) && final(slice)@ == "
            "final(ret.unwrap().1)@ + seq![*final(ret.unwrap().0)], ;"
        ),
        edge="last",
        wrapper=False,
        source_start=262,
        source_end=264,
        docs_start=244,
        docs_end=257,
        source_item_sha256=(
            "bea57e99b1e178d9176ff0b1a6f78a83dafce93f1f7485844e6275ac07ab2005"
        ),
        generated_declaration_sha256=(
            "76df58761b95f470374b35994693219ee30cc860c14587a16ed6596514e9d0c6"
        ),
        harness_sha256=(
            "79cde36bfa903f2f82536655e821781d4fd39e5d1bced66048094f3511dd5614"
        ),
        source_body_manifest_sha256=(
            "28f1f351cfe548e9cac218a94db73737117e741929bf0485866be814720d6136"
        ),
        transformation_manifest_sha256=(
            "432c69053621895e294019161a109c9df2ac16a2f3ff67cd269fe63310437768"
        ),
        dependency_manifest_sha256=(
            "54f5812946dd268034191e872b844778c9d210b5d136e797d5040478d326d0a2"
        ),
        all_trust_site_ids=("TS-097-D001",),
    ),
    EdgeTarget(
        target="core::slice::split_off_first_mut",
        input_order="101",
        artifact_id="101_core_slice_split_off_first_mut",
        active_contract_sha256=(
            "fb2805dd3aa3b506b48de88fdc75518d217820aceb32543f31d6d0ef40446728"
        ),
        active_contract_text=(
            "pub assume_specification<'a, T>[ <[T]>::split_off_first_mut ]( "
            "slice_ref: &mut &'a mut [T], ) -> (ret: Option<&'a mut T>) "
            "ensures (*old(slice_ref))@.len() == 0 ==> ret.is_none() && "
            "(*final(slice_ref))@ == (*old(slice_ref))@, "
            "(*old(slice_ref))@.len() != 0 ==> ret.is_some() && "
            "slice_split_off_first_result::<T>( (*old(slice_ref))@, "
            "(*final(slice_ref))@, *ret.unwrap(), ) && "
            "(seq![*final(ret.unwrap())] + (*final(slice_ref))@).len() == "
            "(*old(slice_ref))@.len(), ;"
        ),
        edge="first",
        wrapper=True,
        source_start=5035,
        source_end=5041,
        docs_start=5017,
        docs_end=5031,
        source_item_sha256=(
            "bd916b533cd3fed622062b911bb1ad18889d4240f66d45311415d0673e52c374"
        ),
        generated_declaration_sha256=(
            "7156077b16e2da259dafa573de211f7d47496f59b32bd7fb956881b5fcd9b745"
        ),
        harness_sha256=(
            "bd62ceb407a801d1660ae2b27c47bc3f290cdc7c72f847a6a713372462d929a8"
        ),
        source_body_manifest_sha256=(
            "1147483268ee210b895d4699681728739e6ac4419c458b9cc532be2e4fb1bfc3"
        ),
        transformation_manifest_sha256=(
            "a9ce2165e086573f4a920b8a667ab08304ac788713f5578a438c788743ad71ac"
        ),
        dependency_manifest_sha256=(
            "a871e0a39b42c1c6a9a48478d512d4ede677f64576823c84253a648cd69138ee"
        ),
        all_trust_site_ids=(
            "TS-101-D001",
            "TS-101-D002",
            "TS-101-D003",
        ),
    ),
    EdgeTarget(
        target="core::slice::split_off_last_mut",
        input_order="103",
        artifact_id="103_core_slice_split_off_last_mut",
        active_contract_sha256=(
            "1f03e74ea8d7d4c774711bb8af028cbed32e1401810479f58803a6de7a426f4d"
        ),
        active_contract_text=(
            "pub assume_specification<'a, T>[ <[T]>::split_off_last_mut ]( "
            "slice_ref: &mut &'a mut [T], ) -> (ret: Option<&'a mut T>) "
            "ensures (*old(slice_ref))@.len() == 0 ==> ret.is_none() && "
            "(*final(slice_ref))@ == (*old(slice_ref))@, "
            "(*old(slice_ref))@.len() != 0 ==> ret.is_some() && "
            "slice_split_off_last_result::<T>( (*old(slice_ref))@, "
            "(*final(slice_ref))@, *ret.unwrap(), ) && "
            "((*final(slice_ref))@ + seq![*final(ret.unwrap())]).len() == "
            "(*old(slice_ref))@.len(), ;"
        ),
        edge="last",
        wrapper=True,
        source_start=5085,
        source_end=5091,
        docs_start=5067,
        docs_end=5081,
        source_item_sha256=(
            "8a7346f07fcf4cf6ee992be7812103b22dbed089118e0b60902114b2f63cf6aa"
        ),
        generated_declaration_sha256=(
            "bd6cd48029fd8c19e8f605de2ea3789bb5f40bd059781463ca0c0b8d3d20ca94"
        ),
        harness_sha256=(
            "2b11db639ed9a38e09c3c9f9c2695ddba318d667b524ad76aeadf271d7eebab9"
        ),
        source_body_manifest_sha256=(
            "a5ca19f854205c69818371342f690528e46e28f0b574b5edbae47ddfed40dcc3"
        ),
        transformation_manifest_sha256=(
            "704b976063e1bd8554f6f7de9813eadc4db699ed033b5fdbc9bd5ee4677005ee"
        ),
        dependency_manifest_sha256=(
            "d4a310757aa508f4ea9866dd4b136919a813b130f87c86f423765942649ddd01"
        ),
        all_trust_site_ids=(
            "TS-103-D001",
            "TS-103-D002",
            "TS-103-D003",
        ),
    ),
)

TARGET_BY_ARTIFACT = {target.artifact_id: target for target in TARGETS}
TARGET_BY_KEY = {
    (target.target, target.input_order): target for target in TARGETS
}
TARGET_KEYS = tuple(TARGET_BY_KEY)


def _normalize(text: str) -> str:
    return " ".join(text.split())


def validate_source_anchors(
    config: EdgeTarget,
    source_item: str,
    vocabulary: str,
) -> None:
    if config.edge == "first":
        pattern = "if let [first, tail @ ..] = self { Some((first, tail)) } else { None }"
        wrapper = (
            "let Some((first, rem)) = mem::replace(self, &mut []).split_first_mut() "
            "else { return None }; *self = rem; Some(first)"
        )
        vocabulary_fragment = (
            "source.len() != 0 && value == source[0] && remaining == "
            "source.subrange(1, source.len() as int)"
        )
    else:
        pattern = "if let [init @ .., last] = self { Some((last, init)) } else { None }"
        wrapper = (
            "let Some((last, rem)) = mem::replace(self, &mut []).split_last_mut() "
            "else { return None }; *self = rem; Some(last)"
        )
        vocabulary_fragment = (
            "source.len() != 0 && value == source[(source.len() - 1) as int] "
            "&& remaining == source.subrange(0, (source.len() - 1) as int)"
        )
    required = wrapper if config.wrapper else pattern
    if _normalize(required) not in _normalize(source_item):
        raise GuardError(
            f"{config.target}: canonical source transition/order changed"
        )
    if config.wrapper and _normalize(vocabulary_fragment) not in _normalize(
        vocabulary
    ):
        raise GuardError(
            f"{config.target}: shared result vocabulary changed"
        )


def _record_fields(fields: tuple[tuple[str, str], ...]) -> str:
    return "\n".join(f"      ({name} {sort})" for name, sort in fields)


INPUT_FIELDS = (
    ("x_source", "(Seq Int)"),
    ("x_start", "Int"),
    ("x_length", "Int"),
    ("x_address", "Int"),
    ("x_allocation", "Int"),
    ("x_provenance", "Int"),
    ("x_borrow", "Int"),
    ("x_element_size", "Int"),
)


def _state_declarations(config: EdgeTarget, purpose: str) -> str:
    frame = f"""\
(declare-datatypes ((FrameState 0))
  (((mkFrameState
{_record_fields(tuple(
    (name.replace("s_", "f_", 1), sort)
    for name, sort in config.state_fields
))}))))"""
    if purpose == EXACT_OUTPUT:
        return (
            "(declare-datatypes ((State 0)) (((mkState))))\n"
            + frame
        )
    return f"""\
(declare-datatypes ((State 0))
  (((mkState
{_record_fields(config.state_fields)}))))"""


def _frame_selector(selector: str, purpose: str) -> str:
    if purpose == PRIMARY:
        return selector
    return selector.replace("s_", "f_", 1)


def _frame_sort(purpose: str) -> str:
    return "State" if purpose == PRIMARY else "FrameState"


def _input_boundary_observed(config: EdgeTarget) -> str:
    clauses = [
        "(= (b_input_address b) (x_address x))",
        "(= (b_input_allocation b) (x_allocation x))",
        "(= (b_input_provenance b) (x_provenance x))",
        "(= (b_input_borrow b) (x_borrow x))",
        "(= (b_element_size b) (x_element_size x))",
    ]
    return """\
(define-fun InputBoundaryObserved ((x Input) (b Boundary)) Bool
  (and %s))""" % "\n       ".join(clauses)


def _selected_equalities(config: EdgeTarget, prefix: str = "y") -> list[str]:
    idx = config.selected_index
    return [
        f"(= ({prefix}_is_some {prefix}) true)",
        f"(= ({prefix}_selected_index {prefix}) {idx})",
        f"(= ({prefix}_selected_start {prefix}) (+ (x_start x) {idx}))",
        f"(= ({prefix}_selected_value {prefix}) (seq.nth (x_source x) {idx}))",
        (
            f"(= ({prefix}_selected_address {prefix}) "
            f"(+ (x_address x) (* {idx} (x_element_size x))))"
        ),
        (
            f"(= ({prefix}_selected_allocation {prefix}) "
            "(x_allocation x))"
        ),
        (
            f"(= ({prefix}_selected_provenance {prefix}) "
            "(x_provenance x))"
        ),
        (
            f"(= ({prefix}_selected_parent_borrow {prefix}) "
            "(x_borrow x))"
        ),
        (
            f"(= ({prefix}_selected_element_size {prefix}) "
            "(x_element_size x))"
        ),
        f"(= ({prefix}_selected_projection {prefix}) 1)",
    ]


def _empty_output_equalities(config: EdgeTarget) -> list[str]:
    clauses = [
        "(= (y_is_some y) false)",
        "(= (y_selected_index y) (- 1))",
        "(= (y_selected_start y) 0)",
        "(= (y_selected_value y) 0)",
        "(= (y_selected_address y) 0)",
        "(= (y_selected_allocation y) 0)",
        "(= (y_selected_provenance y) 0)",
        "(= (y_selected_parent_borrow y) 0)",
        "(= (y_selected_element_size y) 0)",
        "(= (y_selected_projection y) 0)",
    ]
    if not config.wrapper:
        clauses.extend(
            (
                "(= (y_tuple_selected_first y) false)",
                f"(= (y_remainder_sequence y) {EMPTY_SEQ})",
                "(= (y_remainder_start y) 0)",
                "(= (y_remainder_length y) 0)",
                "(= (y_remainder_address y) 0)",
                "(= (y_remainder_allocation y) 0)",
                "(= (y_remainder_provenance y) 0)",
                "(= (y_remainder_parent_borrow y) 0)",
                "(= (y_remainder_element_size y) 0)",
                "(= (y_remainder_projection y) 0)",
            )
        )
    return clauses


def _remainder_equalities(config: EdgeTarget) -> list[str]:
    offset = config.remainder_offset
    length = "(- (x_length x) 1)"
    return [
        "(= (y_tuple_selected_first y) true)",
        (
            "(= (y_remainder_sequence y) "
            f"(seq.extract (x_source x) {offset} {length}))"
        ),
        f"(= (y_remainder_start y) (+ (x_start x) {offset}))",
        f"(= (y_remainder_length y) {length})",
        (
            "(= (y_remainder_address y) "
            f"(+ (x_address x) (* {offset} (x_element_size x))))"
        ),
        "(= (y_remainder_allocation y) (x_allocation x))",
        "(= (y_remainder_provenance y) (x_provenance x))",
        "(= (y_remainder_parent_borrow y) (x_borrow x))",
        "(= (y_remainder_element_size y) (x_element_size x))",
        "(= (y_remainder_projection y) 2)",
    ]


def _frame_equalities(
    config: EdgeTarget,
    purpose: str,
    *,
    empty: bool,
) -> list[str]:
    sel = lambda name: _frame_selector(f"s_{name}", purpose)
    state = "s" if purpose == PRIMARY else "f"
    if empty:
        receiver_sequence = "(x_source x)" if not config.wrapper else EMPTY_SEQ
        receiver_start = "(x_start x)" if not config.wrapper else "0"
        receiver_address = (
            "(x_address x)"
            if not config.wrapper
            else "(b_empty_address b)"
        )
        receiver_allocation = (
            "(x_allocation x)"
            if not config.wrapper
            else "(b_empty_allocation b)"
        )
        receiver_provenance = (
            "(x_provenance x)"
            if not config.wrapper
            else "(b_empty_provenance b)"
        )
        receiver_borrow = (
            "(x_borrow x)"
            if not config.wrapper
            else "(b_empty_borrow b)"
        )
        receiver_projection = "0" if not config.wrapper else "3"
        selected = "0"
        remainder = EMPTY_SEQ
    else:
        offset = config.remainder_offset
        length = "(- (x_length x) 1)"
        if config.wrapper:
            receiver_sequence = (
                f"(seq.extract (x_source x) {offset} {length})"
            )
            receiver_start = f"(+ (x_start x) {offset})"
            receiver_address = (
                f"(+ (x_address x) "
                f"(* {offset} (x_element_size x)))"
            )
            receiver_projection = "2"
        else:
            receiver_sequence = "(x_source x)"
            receiver_start = "(x_start x)"
            receiver_address = "(x_address x)"
            receiver_projection = "0"
        receiver_allocation = "(x_allocation x)"
        receiver_provenance = "(x_provenance x)"
        receiver_borrow = "(x_borrow x)"
        selected = f"(seq.nth (x_source x) {config.selected_index})"
        remainder = f"(seq.extract (x_source x) {offset} {length})"
    return [
        f"(= ({sel('receiver_sequence')} {state}) {receiver_sequence})",
        f"(= ({sel('receiver_start')} {state}) {receiver_start})",
        (
            f"(= ({sel('receiver_length')} {state}) "
            f"{'0' if empty else ('(- (x_length x) 1)' if config.wrapper else '(x_length x)')})"
        ),
        f"(= ({sel('receiver_address')} {state}) {receiver_address})",
        f"(= ({sel('receiver_allocation')} {state}) {receiver_allocation})",
        f"(= ({sel('receiver_provenance')} {state}) {receiver_provenance})",
        f"(= ({sel('receiver_borrow')} {state}) {receiver_borrow})",
        (
            f"(= ({sel('receiver_element_size')} {state}) "
            "(x_element_size x))"
        ),
        f"(= ({sel('receiver_projection')} {state}) {receiver_projection})",
        f"(= ({sel('backing_sequence')} {state}) (x_source x))",
        f"(= ({sel('selected_final_value')} {state}) {selected})",
        f"(= ({sel('remainder_final_sequence')} {state}) {remainder})",
    ]


def _direct_transitions(config: EdgeTarget, purpose: str) -> str:
    split_name = (
        "SplitFirstMutTransition"
        if config.edge == "first"
        else "SplitLastMutTransition"
    )
    frame_sort = _frame_sort(purpose)
    frame = "s" if purpose == PRIMARY else "f"
    empty = "\n       ".join(
        _empty_output_equalities(config)
        + _frame_equalities(config, purpose, empty=True)
    )
    nonempty = "\n       ".join(
        _selected_equalities(config)
        + _remainder_equalities(config)
        + _frame_equalities(config, purpose, empty=False)
    )
    return f"""\
(define-fun {split_name}
  ((x Input) (b Boundary) (y Output) ({frame} {frame_sort})) Bool
  (ite (= (x_length x) 0)
       (and {empty})
       (and {nonempty})))"""


REPLACEMENT_FIELDS = (
    ("r_held_source", "(Seq Int)"),
    ("r_held_start", "Int"),
    ("r_held_length", "Int"),
    ("r_held_address", "Int"),
    ("r_held_allocation", "Int"),
    ("r_held_provenance", "Int"),
    ("r_held_borrow", "Int"),
    ("r_element_size", "Int"),
    ("r_slot_address", "Int"),
    ("r_slot_allocation", "Int"),
    ("r_slot_provenance", "Int"),
    ("r_slot_borrow", "Int"),
    ("r_phase", "Int"),
)

SPLIT_FIELDS = (
    ("p_is_some", "Bool"),
    ("p_selected_index", "Int"),
    ("p_selected_start", "Int"),
    ("p_selected_value", "Int"),
    ("p_selected_address", "Int"),
    ("p_selected_allocation", "Int"),
    ("p_selected_provenance", "Int"),
    ("p_selected_parent_borrow", "Int"),
    ("p_selected_element_size", "Int"),
    ("p_selected_projection", "Int"),
    ("p_remainder_sequence", "(Seq Int)"),
    ("p_remainder_start", "Int"),
    ("p_remainder_length", "Int"),
    ("p_remainder_address", "Int"),
    ("p_remainder_allocation", "Int"),
    ("p_remainder_provenance", "Int"),
    ("p_remainder_parent_borrow", "Int"),
    ("p_remainder_element_size", "Int"),
    ("p_remainder_projection", "Int"),
    ("p_slot_address", "Int"),
    ("p_slot_allocation", "Int"),
    ("p_slot_provenance", "Int"),
    ("p_slot_borrow", "Int"),
    ("p_phase", "Int"),
)


def _wrapper_datatypes() -> str:
    return f"""\
(declare-datatypes ((ReplacementState 0))
  (((mkReplacementState
{_record_fields(REPLACEMENT_FIELDS)}))))
(declare-datatypes ((SplitState 0))
  (((mkSplitState
{_record_fields(SPLIT_FIELDS)}))))"""


def _replace_transition() -> str:
    return """\
(define-fun ReplaceWithEmptyTransition
  ((x Input) (b Boundary) (r ReplacementState)) Bool
  (and (= (r_held_source r) (x_source x))
       (= (r_held_start r) (x_start x))
       (= (r_held_length r) (x_length x))
       (= (r_held_address r) (b_input_address b))
       (= (r_held_allocation r) (b_input_allocation b))
       (= (r_held_provenance r) (b_input_provenance b))
       (= (r_held_borrow r) (b_input_borrow b))
       (= (r_element_size r) (b_element_size b))
       (= (r_slot_address r) (b_empty_address b))
       (= (r_slot_allocation r) (b_empty_allocation b))
       (= (r_slot_provenance r) (b_empty_provenance b))
       (= (r_slot_borrow r) (b_empty_borrow b))
       (= (r_phase r) 1)))"""


def _split_transition(config: EdgeTarget) -> str:
    name = (
        "SplitFirstTransition"
        if config.edge == "first"
        else "SplitLastTransition"
    )
    idx = "0" if config.edge == "first" else "(- (r_held_length r) 1)"
    offset = "1" if config.edge == "first" else "0"
    length = "(- (r_held_length r) 1)"
    empty = [
        "(= (p_is_some p) false)",
        "(= (p_selected_index p) (- 1))",
        "(= (p_selected_start p) 0)",
        "(= (p_selected_value p) 0)",
        "(= (p_selected_address p) 0)",
        "(= (p_selected_allocation p) 0)",
        "(= (p_selected_provenance p) 0)",
        "(= (p_selected_parent_borrow p) 0)",
        "(= (p_selected_element_size p) 0)",
        "(= (p_selected_projection p) 0)",
        f"(= (p_remainder_sequence p) {EMPTY_SEQ})",
        "(= (p_remainder_start p) 0)",
        "(= (p_remainder_length p) 0)",
        "(= (p_remainder_address p) 0)",
        "(= (p_remainder_allocation p) 0)",
        "(= (p_remainder_provenance p) 0)",
        "(= (p_remainder_parent_borrow p) 0)",
        "(= (p_remainder_element_size p) 0)",
        "(= (p_remainder_projection p) 0)",
    ]
    nonempty = [
        "(= (p_is_some p) true)",
        f"(= (p_selected_index p) {idx})",
        f"(= (p_selected_start p) (+ (r_held_start r) {idx}))",
        (
            f"(= (p_selected_value p) "
            f"(seq.nth (r_held_source r) {idx}))"
        ),
        (
            f"(= (p_selected_address p) "
            f"(+ (r_held_address r) (* {idx} (r_element_size r))))"
        ),
        "(= (p_selected_allocation p) (r_held_allocation r))",
        "(= (p_selected_provenance p) (r_held_provenance r))",
        "(= (p_selected_parent_borrow p) (r_held_borrow r))",
        "(= (p_selected_element_size p) (r_element_size r))",
        "(= (p_selected_projection p) 1)",
        (
            f"(= (p_remainder_sequence p) "
            f"(seq.extract (r_held_source r) {offset} {length}))"
        ),
        f"(= (p_remainder_start p) (+ (r_held_start r) {offset}))",
        f"(= (p_remainder_length p) {length})",
        (
            f"(= (p_remainder_address p) "
            f"(+ (r_held_address r) (* {offset} (r_element_size r))))"
        ),
        "(= (p_remainder_allocation p) (r_held_allocation r))",
        "(= (p_remainder_provenance p) (r_held_provenance r))",
        "(= (p_remainder_parent_borrow p) (r_held_borrow r))",
        "(= (p_remainder_element_size p) (r_element_size r))",
        "(= (p_remainder_projection p) 2)",
    ]
    propagated = [
        "(= (p_slot_address p) (r_slot_address r))",
        "(= (p_slot_allocation p) (r_slot_allocation r))",
        "(= (p_slot_provenance p) (r_slot_provenance r))",
        "(= (p_slot_borrow p) (r_slot_borrow r))",
        "(= (p_phase p) 2)",
    ]
    return f"""\
(define-fun {name}
  ((r ReplacementState) (p SplitState)) Bool
  (and (= (r_phase r) 1)
       (ite (= (r_held_length r) 0)
            (and {" ".join(empty)})
            (and {" ".join(nonempty)}))
       {" ".join(propagated)}))"""


def _wrapper_output_from_split() -> list[str]:
    return [
        "(= (y_is_some y) (p_is_some p))",
        "(= (y_selected_index y) (p_selected_index p))",
        "(= (y_selected_start y) (p_selected_start p))",
        "(= (y_selected_value y) (p_selected_value p))",
        "(= (y_selected_address y) (p_selected_address p))",
        "(= (y_selected_allocation y) (p_selected_allocation p))",
        "(= (y_selected_provenance y) (p_selected_provenance p))",
        (
            "(= (y_selected_parent_borrow y) "
            "(p_selected_parent_borrow p))"
        ),
        (
            "(= (y_selected_element_size y) "
            "(p_selected_element_size p))"
        ),
        "(= (y_selected_projection y) (p_selected_projection p))",
    ]


def _assignment_transition(config: EdgeTarget, purpose: str) -> str:
    frame_sort = _frame_sort(purpose)
    frame = "s" if purpose == PRIMARY else "f"
    sel = lambda name: _frame_selector(f"s_{name}", purpose)
    output = _wrapper_output_from_split()
    empty_frame = [
        f"(= ({sel('receiver_sequence')} {frame}) {EMPTY_SEQ})",
        f"(= ({sel('receiver_start')} {frame}) 0)",
        f"(= ({sel('receiver_length')} {frame}) 0)",
        f"(= ({sel('receiver_address')} {frame}) (p_slot_address p))",
        (
            f"(= ({sel('receiver_allocation')} {frame}) "
            "(p_slot_allocation p))"
        ),
        (
            f"(= ({sel('receiver_provenance')} {frame}) "
            "(p_slot_provenance p))"
        ),
        f"(= ({sel('receiver_borrow')} {frame}) (p_slot_borrow p))",
        (
            f"(= ({sel('receiver_element_size')} {frame}) "
            "(x_element_size x))"
        ),
        f"(= ({sel('receiver_projection')} {frame}) 3)",
        f"(= ({sel('selected_final_value')} {frame}) 0)",
        (
            f"(= ({sel('remainder_final_sequence')} {frame}) "
            f"{EMPTY_SEQ})"
        ),
    ]
    nonempty_frame = [
        (
            f"(= ({sel('receiver_sequence')} {frame}) "
            "(p_remainder_sequence p))"
        ),
        f"(= ({sel('receiver_start')} {frame}) (p_remainder_start p))",
        f"(= ({sel('receiver_length')} {frame}) (p_remainder_length p))",
        (
            f"(= ({sel('receiver_address')} {frame}) "
            "(p_remainder_address p))"
        ),
        (
            f"(= ({sel('receiver_allocation')} {frame}) "
            "(p_remainder_allocation p))"
        ),
        (
            f"(= ({sel('receiver_provenance')} {frame}) "
            "(p_remainder_provenance p))"
        ),
        (
            f"(= ({sel('receiver_borrow')} {frame}) "
            "(p_remainder_parent_borrow p))"
        ),
        (
            f"(= ({sel('receiver_element_size')} {frame}) "
            "(p_remainder_element_size p))"
        ),
        f"(= ({sel('receiver_projection')} {frame}) 2)",
        (
            f"(= ({sel('selected_final_value')} {frame}) "
            "(p_selected_value p))"
        ),
        (
            f"(= ({sel('remainder_final_sequence')} {frame}) "
            "(p_remainder_sequence p))"
        ),
    ]
    common = [
        f"(= ({sel('backing_sequence')} {frame}) (x_source x))",
    ]
    return f"""\
(define-fun ReceiverAssignmentTransition
  ((x Input) (b Boundary) (p SplitState) (y Output)
   ({frame} {frame_sort})) Bool
  (and (= (p_phase p) 2)
       {" ".join(output)}
       (ite (p_is_some p)
            (and {" ".join(nonempty_frame)})
            (and {" ".join(empty_frame)}))
       {" ".join(common)}))"""


def _active_definitions(config: EdgeTarget, purpose: str) -> str:
    frame_sort = _frame_sort(purpose)
    frame = "s" if purpose == PRIMARY else "f"
    sel = lambda name: _frame_selector(f"s_{name}", purpose)
    idx = config.selected_index
    offset = config.remainder_offset
    length = "(- (x_length x) 1)"
    definitions = [
        """\
(define-fun ActiveEmptyTagConjunct ((x Input) (y Output)) Bool
  (=> (= (x_length x) 0) (= (y_is_some y) false)))""",
        f"""\
(define-fun ActiveEmptyReceiverConjunct
  ((x Input) ({frame} {frame_sort})) Bool
  (=> (= (x_length x) 0)
      (= ({sel('receiver_sequence')} {frame}) (x_source x))))""",
        """\
(define-fun ActiveNonemptyTagConjunct ((x Input) (y Output)) Bool
  (=> (not (= (x_length x) 0)) (= (y_is_some y) true)))""",
        f"""\
(define-fun ActiveSelectedValueConjunct ((x Input) (y Output)) Bool
  (=> (not (= (x_length x) 0))
      (= (y_selected_value y) (seq.nth (x_source x) {idx}))))""",
    ]
    if config.wrapper:
        relation = (
            "SliceSplitOffFirstResult"
            if config.edge == "first"
            else "SliceSplitOffLastResult"
        )
        relation_index = (
            "0"
            if config.edge == "first"
            else "(- (seq.len source) 1)"
        )
        relation_offset = "1" if config.edge == "first" else "0"
        relation_length = "(- (seq.len source) 1)"
        concat = (
            f"(seq.++ (seq.unit ({sel('selected_final_value')} {frame})) "
            f"({sel('receiver_sequence')} {frame}))"
            if config.edge == "first"
            else (
                f"(seq.++ ({sel('receiver_sequence')} {frame}) "
                f"(seq.unit ({sel('selected_final_value')} {frame})))"
            )
        )
        definitions.extend(
            (
                f"""\
(define-fun {relation}
  ((source (Seq Int)) (remaining (Seq Int)) (value Int)) Bool
  (and (not (= (seq.len source) 0))
       (= value (seq.nth source {relation_index}))
       (= remaining
          (seq.extract source {relation_offset} {relation_length}))))""",
                f"""\
(define-fun ActiveVocabularyConjunct
  ((x Input) (y Output) ({frame} {frame_sort})) Bool
  (=> (not (= (x_length x) 0))
      ({relation}
        (x_source x)
        ({sel('receiver_sequence')} {frame})
        (y_selected_value y))))""",
                f"""\
(define-fun ActiveLengthCompositionConjunct
  ((x Input) ({frame} {frame_sort})) Bool
  (=> (not (= (x_length x) 0))
      (= (seq.len {concat}) (x_length x))))""",
                f"""\
(define-fun ActiveDisjointnessConjunct
  ((x Input) (y Output) ({frame} {frame_sort})) Bool
  (=> (not (= (x_length x) 0))
      (or
        (<= (+ (y_selected_start y) 1)
            ({sel('receiver_start')} {frame}))
        (<= (+ ({sel('receiver_start')} {frame})
               ({sel('receiver_length')} {frame}))
            (y_selected_start y)))))""",
            )
        )
    else:
        concat = (
            f"(seq.++ (seq.unit ({sel('selected_final_value')} {frame})) "
            f"({sel('remainder_final_sequence')} {frame}))"
            if config.edge == "first"
            else (
                f"(seq.++ ({sel('remainder_final_sequence')} {frame}) "
                f"(seq.unit ({sel('selected_final_value')} {frame})))"
            )
        )
        definitions.extend(
            (
                f"""\
(define-fun ActiveRemainderConjunct ((x Input) (y Output)) Bool
  (=> (not (= (x_length x) 0))
      (= (y_remainder_sequence y)
         (seq.extract (x_source x) {offset} {length}))))""",
                f"""\
(define-fun ActiveFinalFrameConjunct
  ((x Input) ({frame} {frame_sort})) Bool
  (=> (not (= (x_length x) 0))
      (= ({sel('receiver_sequence')} {frame}) {concat})))""",
                """\
(define-fun ActiveDisjointnessConjunct
  ((x Input) (y Output)) Bool
  (=> (not (= (x_length x) 0))
      (or
        (<= (+ (y_selected_start y) 1) (y_remainder_start y))
        (<= (+ (y_remainder_start y) (y_remainder_length y))
            (y_selected_start y)))))""",
            )
        )
    return "\n".join(definitions)


def _active_calls(config: EdgeTarget, purpose: str) -> list[str]:
    frame = "s" if purpose == PRIMARY else "f"
    calls = [
        "(ActiveEmptyTagConjunct x y)",
        f"(ActiveEmptyReceiverConjunct x {frame})",
        "(ActiveNonemptyTagConjunct x y)",
        "(ActiveSelectedValueConjunct x y)",
    ]
    if config.wrapper:
        calls.extend(
            (
                f"(ActiveVocabularyConjunct x y {frame})",
                f"(ActiveLengthCompositionConjunct x {frame})",
                f"(ActiveDisjointnessConjunct x y {frame})",
            )
        )
    else:
        calls.extend(
            (
                "(ActiveRemainderConjunct x y)",
                f"(ActiveFinalFrameConjunct x {frame})",
                "(ActiveDisjointnessConjunct x y)",
            )
        )
    return calls


def _target_source_transition(config: EdgeTarget, purpose: str) -> str:
    frame_sort = _frame_sort(purpose)
    frame = "s" if purpose == PRIMARY else "f"
    transition_name = (
        "TargetSourceTransition"
        if purpose == PRIMARY
        else "TargetSourceFrameTransition"
    )
    active = "\n       ".join(_active_calls(config, purpose))
    if config.wrapper:
        split = (
            "SplitFirstTransition"
            if config.edge == "first"
            else "SplitLastTransition"
        )
        stages = f"""\
(define-fun OrderedWrapperTransition
  ((x Input) (b Boundary) (y Output) ({frame} {frame_sort})) Bool
  (exists ((r ReplacementState) (p SplitState))
    (and (ReplaceWithEmptyTransition x b r)
         ({split} r p)
         (ReceiverAssignmentTransition x b p y {frame}))))"""
        top_body = f"(OrderedWrapperTransition x b y {frame})"
    else:
        split = (
            "SplitFirstMutTransition"
            if config.edge == "first"
            else "SplitLastMutTransition"
        )
        stages = ""
        top_body = f"({split} x b y {frame})"
    top = f"""\
(define-fun {transition_name}
  ((x Input) (b Boundary) (y Output) ({frame} {frame_sort})) Bool
  (and (InputBoundaryObserved x b)
       (= (y_is_some y) (not (= (x_length x) 0)))
       {top_body}
       {active}))"""
    if purpose == PRIMARY:
        return (stages + "\n" + top).strip()
    erased = """\
(define-fun TargetSourceTransition
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (and (= (y_is_some y) (not (= (x_length x) 0)))
       (exists ((f FrameState))
         (TargetSourceFrameTransition x b y f))))"""
    return (stages + "\n" + top + "\n" + erased).strip()


def _requires() -> str:
    return """\
(define-fun Requires_T ((x Input)) Bool
  (and (= (x_length x) (seq.len (x_source x)))
       (>= (x_length x) 0)
       (>= (x_start x) 0)
       (>= (x_address x) 0)
       (>= (x_allocation x) 0)
       (>= (x_provenance x) 0)
       (>= (x_borrow x) 0)
       (>= (x_element_size x) 0)))"""


def _boundary(config: EdgeTarget) -> str:
    clauses = [
        "(>= (b_input_address b) 0)",
        "(>= (b_input_allocation b) 0)",
        "(>= (b_input_provenance b) 0)",
        "(>= (b_input_borrow b) 0)",
        "(>= (b_element_size b) 0)",
    ]
    if config.wrapper:
        clauses.extend(
            (
                "(>= (b_empty_address b) 0)",
                "(>= (b_empty_allocation b) 0)",
                "(>= (b_empty_provenance b) 0)",
                "(>= (b_empty_borrow b) 0)",
            )
        )
    clauses.append("(InputBoundaryObserved x b)")
    return """\
(define-fun Boundary_T ((x Input) (b Boundary)) Bool
  (and %s))""" % "\n       ".join(clauses)


def _target_definition(config: EdgeTarget, purpose: str) -> str:
    return f"""\
(define-fun TargetDefinition_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (TargetSourceTransition x b y s))"""


def _equivalence(config: EdgeTarget, purpose: str) -> str:
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
    config: EdgeTarget,
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
    wrapper_datatypes = _wrapper_datatypes() if config.wrapper else ""
    transition_definitions = [
        _input_boundary_observed(config),
    ]
    if config.wrapper:
        transition_definitions.extend(
            (
                _replace_transition(),
                _split_transition(config),
                _assignment_transition(config, purpose),
            )
        )
    else:
        transition_definitions.append(_direct_transitions(config, purpose))
    transition_definitions.extend(
        (
            _active_definitions(config, purpose),
            _target_source_transition(config, purpose),
        )
    )
    return f"""\
; Target: {config.target}
; Active contract SHA-256: {config.active_contract_sha256}
; Purpose: {purpose}
; Arbitrary valid length, including empty and ZST slices.
(set-logic ALL)
(declare-datatypes ((Input 0))
  (((mkInput
{_record_fields(INPUT_FIELDS)}))))
(declare-datatypes ((Boundary 0))
  (((mkBoundary
{_record_fields(config.boundary_fields)}))))
(declare-datatypes ((Output 0))
  (((mkOutput
{_record_fields(config.output_fields)}))))
{_state_declarations(config, purpose)}
{wrapper_datatypes}
(declare-const x Input)
(declare-const b Boundary)
(declare-const y1 Output)
(declare-const s1 State)
(declare-const y2 Output)
(declare-const s2 State)
{"\n".join(transition_definitions)}
{_requires()}
{_boundary(config)}
{_target_definition(config, purpose)}
(define-fun Spec_T
  ((x Input) (b Boundary) (y Output) (s State)) Bool
  (TargetDefinition_T x b y s))
{_equivalence(config, purpose)}
{theorem}"""


def obligation_text(config: EdgeTarget, purpose: str) -> str:
    return _model_text(config, purpose, include_theorem=True)


def _principal_observations(
    config: EdgeTarget, purpose: str
) -> list[dict[str, str]]:
    observations = [
        {
            "selector": selector,
            "left": "output1",
            "right": "output2",
            "sort": sort.strip("()"),
        }
        for selector, sort in config.output_fields
    ]
    if purpose == PRIMARY:
        observations.extend(
            {
                "selector": selector,
                "left": "state1",
                "right": "state2",
                "sort": sort.strip("()"),
            }
            for selector, sort in config.state_fields
        )
    return observations


def _boundary_metadata(config: EdgeTarget) -> list[dict[str, Any]]:
    meanings = {
        "b_input_address": ("input_memory", "input data address"),
        "b_input_allocation": (
            "input_provenance",
            "input allocation identity",
        ),
        "b_input_provenance": (
            "input_provenance",
            "input reference provenance",
        ),
        "b_input_borrow": (
            "input_provenance",
            "input mutable-borrow identity",
        ),
        "b_element_size": (
            "input_layout",
            "element size, including zero",
        ),
        "b_empty_address": (
            "source_helper_observation",
            "pre-result empty literal data address",
        ),
        "b_empty_allocation": (
            "source_helper_observation",
            "pre-result empty literal allocation identity",
        ),
        "b_empty_provenance": (
            "source_helper_observation",
            "pre-result empty literal provenance",
        ),
        "b_empty_borrow": (
            "source_helper_observation",
            "pre-result empty literal mutable-borrow identity",
        ),
    }
    return [
        {
            "selector": selector,
            "role": meanings[selector][0],
            "meaning": meanings[selector][1],
            "source_citations": [config.source_reference],
            "trust_site_ids": list(config.dependency_trust_site_ids),
            "source_backed_replacement_ids": [],
        }
        for selector, _ in config.boundary_fields
    ]


def obligation_metadata(
    config: EdgeTarget, purpose: str
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
            "source_sequence": "arbitrary integer sequence of the same length",
            "element_size": (
                "arbitrary nonnegative integer; zero-sized types are included"
            ),
            "source_model_complete": True,
        },
        "active_contract_conjuncts": list(config.active_conjuncts),
        "boundary_scope": {
            "shared_observations": [
                field["selector"] for field in _boundary_metadata(config)
            ],
            "admitted_trust_site_ids": list(
                config.dependency_trust_site_ids
            ),
            "excluded_retained_trust_site_ids": [],
            "context_only_trust_site_ids": [],
            "all_audited_trust_site_ids": list(config.all_trust_site_ids),
            "source_backed_replacement_ids": [],
            "excluded_observations": [
                "result tag",
                "selected first or last index and range",
                "returned element or remainder reference",
                "final receiver reference or storage",
                "answer-equivalent encoding",
                "partial or complete execution trace",
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
        "source_backed_replacements": [],
        "unresolved_source_model_trust_site_ids": [],
        "source_transition_definitions": ["TargetSourceTransition"],
        "source_transition_bindings": {
            "ordered_operations": list(config.source_transitions),
            "public_source": config.source_reference,
            "public_docs": config.docs_reference,
            "shared_vocabulary_relation": config.vocabulary_name,
            "trust_site_ids": list(config.all_trust_site_ids),
            "frame_order": config.frame_order,
            "empty_path_receiver_identity": (
                "the pre-result empty-literal observation from Boundary_T"
                if config.wrapper
                else "the unchanged input receiver identity"
            ),
        },
        "equivalence_kind": "exact",
        "equivalence_scope": (
            "every principal return/reference identity and every immediate "
            "receiver/backing-storage observation"
            if purpose == PRIMARY
            else "every principal return/reference identity"
        ),
        "principal_observations": _principal_observations(config, purpose),
        "expected_solver_result": "unsat",
    }


def obligation(
    config: EdgeTarget, purpose: str
) -> tuple[str, dict[str, Any]]:
    return obligation_text(config, purpose), obligation_metadata(config, purpose)


def validate_target_obligation(
    config: EdgeTarget, text: str, metadata: dict[str, Any]
) -> None:
    validate_obligation(text, metadata)
    purpose = metadata.get("obligation_purpose")
    if purpose not in PURPOSES:
        raise GuardError(f"{config.target}: unknown obligation purpose")
    expected_text, expected_metadata = obligation(config, str(purpose))
    if metadata != expected_metadata:
        raise GuardError(
            f"{config.target}: metadata differs from reviewed edge model"
        )
    if parse_smt(text) != parse_smt(expected_text):
        raise GuardError(
            f"{config.target}: SMT differs from reviewed edge model"
        )


def source_instance_text(
    config: EdgeTarget,
    *,
    length: int,
    element_size: int,
    extra_assertions: tuple[str, ...] = (),
) -> str:
    if length < 0 or element_size < 0:
        raise ValueError("length and element size must be nonnegative")
    assertions = [
        "(assert (Requires_T x))",
        "(assert (Boundary_T x b))",
        "(assert (Spec_T x b y1 s1))",
        f"(assert (= (x_length x) {length}))",
        f"(assert (= (x_element_size x) {element_size}))",
    ]
    assertions.extend(f"(assert {item})" for item in extra_assertions)
    return (
        _model_text(config, PRIMARY, include_theorem=False)
        + "\n"
        + "\n".join(assertions)
        + "\n(check-sat)\n"
    )


def boundary_manifest(config: EdgeTarget) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "target": config.target,
        "input_order": config.input_order,
        "boundary_narrower_than_target": True,
        "proof_boundary_assumption": (
            "The shared boundary fixes only the input storage address, "
            "allocation, provenance, mutable-borrow identity, and element "
            "layout"
            + (
                ", plus the pre-result empty-slice literal identity consumed "
                "by mem::replace"
                if config.wrapper
                else ""
            )
            + "."
        ),
        "shared_boundary_observations": _boundary_metadata(config),
        "source_transition": {
            "operations_in_order": list(config.source_transitions),
            "canonical_source": config.source_reference,
            "public_docs": config.docs_reference,
            "shared_vocabulary_relation": config.vocabulary_name,
            "edge": config.edge,
            "frame_order": config.frame_order,
            "empty_receiver_identity": (
                "pre-result empty literal"
                if config.wrapper
                else "unchanged input receiver"
            ),
            "zero_sized_element_addressing": (
                "address + index * element_size; range disjointness remains "
                "index-based when element_size is zero"
            ),
        },
        "dependency_trust_site_ids": list(config.dependency_trust_site_ids),
        "all_audited_trust_site_ids": list(config.all_trust_site_ids),
        "excluded_from_boundary": [
            "result tags",
            "selected first/last indices or ranges",
            "returned element/remainder references",
            "final receiver identity or storage",
            "answer-equivalent encodings",
            "execution traces",
        ],
        "inactive_option_fields": (
            "The SMT record canonically zeros fields hidden by None; these "
            "are representation padding, not boundary observations."
        ),
    }


def _verus_output_fields(config: EdgeTarget) -> str:
    remainder = ""
    if not config.wrapper:
        remainder = """\
    pub tuple_selected_first: bool,
    pub remainder: Seq<int>,
    pub remainder_start: int,
    pub remainder_length: int,
    pub remainder_identity: RefIdentity,
"""
    return f"""\
pub ghost struct Output {{
    pub is_some: bool,
    pub selected_index: int,
    pub selected_start: int,
    pub selected_value: int,
    pub selected_identity: RefIdentity,
{remainder}}}"""


def verus_text(config: EdgeTarget) -> str:
    index = "0" if config.edge == "first" else "input.source.len() as int - 1"
    offset = "1" if config.edge == "first" else "0"
    remainder_end = "input.source.len() as int"
    if config.edge == "last":
        remainder_end = "input.source.len() as int - 1"
    remainder = (
        f"input.source.subrange({offset}, {remainder_end})"
    )
    selected_identity = f"""\
RefIdentity {{
                address: input.address + {index} * input.element_size as int,
                allocation: input.allocation,
                provenance: input.provenance,
                parent_borrow: input.borrow,
                start: input.start + {index},
                length: 1,
                element_size: input.element_size,
                projection: 1,
            }}"""
    if config.wrapper:
        output_nonempty = f"""\
Output {{
            is_some: true,
            selected_index: {index},
            selected_start: input.start + {index},
            selected_value: input.source[{index}],
            selected_identity: {selected_identity},
        }}"""
        output_empty = """\
Output {
            is_some: false,
            selected_index: -1,
            selected_start: 0,
            selected_value: 0,
            selected_identity: empty_ref_identity(),
        }"""
    else:
        output_nonempty = f"""\
Output {{
            is_some: true,
            selected_index: {index},
            selected_start: input.start + {index},
            selected_value: input.source[{index}],
            selected_identity: {selected_identity},
            tuple_selected_first: true,
            remainder: {remainder},
            remainder_start: input.start + {offset},
            remainder_length: input.source.len() - 1,
            remainder_identity: RefIdentity {{
                address: input.address + {offset} * input.element_size as int,
                allocation: input.allocation,
                provenance: input.provenance,
                parent_borrow: input.borrow,
                start: input.start + {offset},
                length: input.source.len() - 1,
                element_size: input.element_size,
                projection: 2,
            }},
        }}"""
        output_empty = """\
Output {
            is_some: false,
            selected_index: -1,
            selected_start: 0,
            selected_value: 0,
            selected_identity: empty_ref_identity(),
            tuple_selected_first: false,
            remainder: Seq::empty(),
            remainder_start: 0,
            remainder_length: 0,
            remainder_identity: empty_ref_identity(),
        }"""
    receiver_nonempty = (
        f"""\
SliceIdentity {{
            source: {remainder},
            start: input.start + {offset},
            address: input.address + {offset} * input.element_size as int,
            allocation: input.allocation,
            provenance: input.provenance,
            borrow: input.borrow,
            element_size: input.element_size,
            projection: 2,
        }}"""
        if config.wrapper
        else "input_identity(input)"
    )
    receiver_empty = (
        "boundary.empty_literal"
        if config.wrapper
        else "input_identity(input)"
    )
    active_remainder = ""
    exact_remainder = ""
    if not config.wrapper:
        active_remainder = f"""\
            && output.remainder == {remainder}
            && output.tuple_selected_first"""
        exact_remainder = """\
        && left.tuple_selected_first == right.tuple_selected_first
        && left.remainder == right.remainder
        && left.remainder_start == right.remainder_start
        && left.remainder_length == right.remainder_length
        && same_ref(left.remainder_identity, right.remainder_identity)"""
    relation_name = (
        f"slice_split_off_{config.edge}_result"
        if config.wrapper
        else "direct_edge_result"
    )
    boundary_empty_field = (
        "    pub empty_literal: SliceIdentity,\n"
        if config.wrapper
        else ""
    )
    boundary_empty_clause = (
        "\n        && boundary.empty_literal.source == Seq::<int>::empty()"
        if config.wrapper
        else ""
    )
    frame = (
        "seq![state.selected_final_value] + state.remainder_final"
        if config.edge == "first"
        else "state.remainder_final + seq![state.selected_final_value]"
    )
    range_owner = "state.receiver" if config.wrapper else "output.remainder_identity"
    disjoint = (
        f"output.selected_start + 1 <= {range_owner}.start"
        if config.edge == "first"
        else (
            f"{range_owner}.start + {range_owner}.length "
            "<= output.selected_start"
            if not config.wrapper
            else (
                "state.receiver.start + state.receiver.source.len() "
                "<= output.selected_start"
            )
        )
    )
    if config.wrapper:
        ordered_state = f"""\
pub ghost struct ReplacementState {{
    pub held: SliceIdentity,
    pub slot: SliceIdentity,
    pub phase: nat,
}}

pub ghost struct SplitState {{
    pub output: Output,
    pub assigned_receiver: SliceIdentity,
    pub slot: SliceIdentity,
    pub phase: nat,
}}

pub open spec fn remainder_identity(input: Input) -> SliceIdentity {{
    {receiver_nonempty}
}}

pub open spec fn replace_with_empty_transition(
    input: Input,
    boundary: Boundary,
    replaced: ReplacementState,
) -> bool {{
    replaced.held == input_identity(input)
        && replaced.slot == boundary.empty_literal
        && replaced.phase == 1
}}

pub open spec fn split_{config.edge}_transition(
    input: Input,
    replaced: ReplacementState,
    split: SplitState,
) -> bool {{
    replaced.phase == 1
        && split.output == source_output(input)
        && split.slot == replaced.slot
        && split.assigned_receiver
            == if input.source.len() == 0 {{
                replaced.slot
            }} else {{
                remainder_identity(input)
            }}
        && split.phase == 2
}}

pub open spec fn receiver_assignment_transition(
    input: Input,
    boundary: Boundary,
    split: SplitState,
    output: Output,
    state: FinalState,
) -> bool {{
    split.phase == 2
        && output == split.output
        && state == source_state(input, boundary)
        && state.receiver == split.assigned_receiver
}}

pub open spec fn ordered_wrapper_transition(
    input: Input,
    boundary: Boundary,
    output: Output,
    state: FinalState,
) -> bool {{
    exists|replaced: ReplacementState, split: SplitState|
        replace_with_empty_transition(input, boundary, replaced)
        && split_{config.edge}_transition(input, replaced, split)
        && receiver_assignment_transition(
            input, boundary, split, output, state,
        )
}}
"""
        source_transition_body = (
            "ordered_wrapper_transition(input, boundary, output, state)"
        )
    else:
        ordered_state = """\
pub open spec fn pattern_split_transition(
    input: Input,
    boundary: Boundary,
    output: Output,
    state: FinalState,
) -> bool {
    output == source_output(input)
        && state == source_state(input, boundary)
}
"""
        source_transition_body = (
            "output == source_output(input)\n"
            "        && state == source_state(input, boundary)\n"
            "        && pattern_split_transition("
            "input, boundary, output, state)"
        )
    return f"""\
#![allow(dead_code, unused_imports, unused_variables)]
// Source-backed arbitrary-length model for {config.target}.

use vstd::prelude::*;
use vstd::seq::*;

verus! {{

pub ghost struct Input {{
    pub source: Seq<int>,
    pub start: int,
    pub address: int,
    pub allocation: int,
    pub provenance: int,
    pub borrow: int,
    pub element_size: nat,
}}

pub ghost struct RefIdentity {{
    pub address: int,
    pub allocation: int,
    pub provenance: int,
    pub parent_borrow: int,
    pub start: int,
    pub length: int,
    pub element_size: nat,
    pub projection: int,
}}

pub ghost struct SliceIdentity {{
    pub source: Seq<int>,
    pub start: int,
    pub address: int,
    pub allocation: int,
    pub provenance: int,
    pub borrow: int,
    pub element_size: nat,
    pub projection: int,
}}

pub ghost struct Boundary {{
    pub input_address: int,
    pub input_allocation: int,
    pub input_provenance: int,
    pub input_borrow: int,
    pub element_size: nat,
{boundary_empty_field}
}}

{_verus_output_fields(config)}

pub ghost struct FinalState {{
    pub receiver: SliceIdentity,
    pub backing: Seq<int>,
    pub selected_final_value: int,
    pub remainder_final: Seq<int>,
}}

pub open spec fn empty_ref_identity() -> RefIdentity {{
    RefIdentity {{
        address: 0,
        allocation: 0,
        provenance: 0,
        parent_borrow: 0,
        start: 0,
        length: 0,
        element_size: 0,
        projection: 0,
    }}
}}

pub open spec fn input_identity(input: Input) -> SliceIdentity {{
    SliceIdentity {{
        source: input.source,
        start: input.start,
        address: input.address,
        allocation: input.allocation,
        provenance: input.provenance,
        borrow: input.borrow,
        element_size: input.element_size,
        projection: 0,
    }}
}}

pub open spec fn same_ref(left: RefIdentity, right: RefIdentity) -> bool {{
    left.address == right.address
        && left.allocation == right.allocation
        && left.provenance == right.provenance
        && left.parent_borrow == right.parent_borrow
        && left.start == right.start
        && left.length == right.length
        && left.element_size == right.element_size
        && left.projection == right.projection
}}

pub open spec fn same_slice(left: SliceIdentity, right: SliceIdentity) -> bool {{
    left.source == right.source
        && left.start == right.start
        && left.address == right.address
        && left.allocation == right.allocation
        && left.provenance == right.provenance
        && left.borrow == right.borrow
        && left.element_size == right.element_size
        && left.projection == right.projection
}}

pub open spec fn boundary_holds(input: Input, boundary: Boundary) -> bool {{
    boundary.input_address == input.address
        && boundary.input_allocation == input.allocation
        && boundary.input_provenance == input.provenance
        && boundary.input_borrow == input.borrow
        && boundary.element_size == input.element_size
{boundary_empty_clause}
}}

pub open spec fn source_output(input: Input) -> Output {{
    if input.source.len() == 0 {{
        {output_empty}
    }} else {{
        {output_nonempty}
    }}
}}

pub open spec fn source_state(
    input: Input,
    boundary: Boundary,
) -> FinalState {{
    if input.source.len() == 0 {{
        FinalState {{
            receiver: {receiver_empty},
            backing: input.source,
            selected_final_value: 0,
            remainder_final: Seq::empty(),
        }}
    }} else {{
        FinalState {{
            receiver: {receiver_nonempty},
            backing: input.source,
            selected_final_value: input.source[{index}],
            remainder_final: {remainder},
        }}
    }}
}}

{ordered_state}

pub open spec fn {relation_name}(
    input: Input,
    output: Output,
    state: FinalState,
) -> bool {{
    if input.source.len() == 0 {{
        !output.is_some && state.receiver.source == input.source
    }} else {{
        output.is_some
            && output.selected_value == input.source[{index}]
{active_remainder}
            && state.receiver.source == {frame}
            && {disjoint}
    }}
}}

pub open spec fn source_transition(
    input: Input,
    boundary: Boundary,
    output: Output,
    state: FinalState,
) -> bool {{
    {source_transition_body}
}}

pub open spec fn target_transition(
    input: Input,
    boundary: Boundary,
    output: Output,
    state: FinalState,
) -> bool {{
    boundary_holds(input, boundary)
        && source_transition(input, boundary, output, state)
        && {relation_name}(input, output, state)
}}

pub open spec fn exact_equivalent(
    left: Output,
    left_state: FinalState,
    right: Output,
    right_state: FinalState,
) -> bool {{
    left.is_some == right.is_some
        && left.selected_index == right.selected_index
        && left.selected_start == right.selected_start
        && left.selected_value == right.selected_value
        && same_ref(left.selected_identity, right.selected_identity)
{exact_remainder}
        && same_slice(left_state.receiver, right_state.receiver)
        && left_state.backing == right_state.backing
        && left_state.selected_final_value == right_state.selected_final_value
        && left_state.remainder_final == right_state.remainder_final
}}

pub proof fn conditional_complete_{config.function_name}(
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
        exact_equivalent(output1, state1, output2, state2),
{{
    reveal(target_transition);
    reveal(source_transition);
    reveal(exact_equivalent);
    reveal(same_ref);
    reveal(same_slice);
}}

}} // verus!
"""
