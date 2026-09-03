#![allow(dead_code, unused_imports, unused_variables)]
// Trusted-free exhaustive Rust 1.96 SliceIndex model for get_unchecked.

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub ghost enum IndexKind {
    Usize,
    OpsIndexRange,
    OpsRange,
    RangeRange,
    OpsRangeTo,
    OpsRangeFrom,
    RangeRangeFrom,
    OpsRangeFull,
    OpsRangeInclusive,
    RangeRangeInclusive,
    OpsRangeToInclusive,
    RangeRangeToInclusive,
    OpsBoundPair,
    ClampUsize,
    ClampRangeRange,
    ClampOpsRange,
    ClampRangeRangeInclusive,
    ClampOpsRangeInclusive,
    ClampRangeRangeFrom,
    ClampOpsRangeFrom,
    ClampOpsRangeTo,
    ClampRangeRangeToInclusive,
    ClampOpsRangeToInclusive,
    ClampOpsRangeFull,
    Last,
}

pub ghost struct Index {
    pub kind: IndexKind,
    pub a: int,
    pub b: int,
    pub exhausted: bool,
    pub start_bound_kind: int,
    pub end_bound_kind: int,
}

pub ghost struct Input {
    pub values: Seq<int>,
    pub index: Index,
    pub allocation: int,
    pub address: int,
    pub provenance: int,
    pub root_borrow: int,
    pub element_size: int,
    pub frame_token: int,
}

pub ghost struct Boundary {
    pub values: Seq<int>,
    pub allocation: int,
    pub address: int,
    pub provenance: int,
    pub root_borrow: int,
    pub element_size: int,
    pub frame_token: int,
}

pub ghost struct NormalizedIndex {
    pub element: bool,
    pub start: int,
    pub end: int,
}

pub ghost struct Output {
    pub element: bool,
    pub start: int,
    pub length: int,
    pub values: Seq<int>,
    pub allocation: int,
    pub address: int,
    pub provenance: int,
    pub parent_borrow: int,
}

pub ghost struct FinalState {
    pub values: Seq<int>,
    pub allocation: int,
    pub address: int,
    pub provenance: int,
    pub root_borrow: int,
    pub element_size: int,
    pub frame_token: int,
}

pub open spec fn min_int(left: int, right: int) -> int {
    if left <= right { left } else { right }
}

pub open spec fn bound_start(index: Index) -> int {
    if index.start_bound_kind == 0 {
        0
    } else if index.start_bound_kind == 1 {
        index.a
    } else {
        index.a + 1
    }
}

pub open spec fn bound_end(length: int, index: Index) -> int {
    if index.end_bound_kind == 0 {
        length
    } else if index.end_bound_kind == 1 {
        index.b + 1
    } else {
        index.b
    }
}

pub open spec fn normalize(length: int, index: Index) -> NormalizedIndex {
    match index.kind {
        IndexKind::Usize =>
            NormalizedIndex { element: true, start: index.a, end: index.a + 1 },
        IndexKind::OpsIndexRange | IndexKind::OpsRange | IndexKind::RangeRange =>
            NormalizedIndex { element: false, start: index.a, end: index.b },
        IndexKind::OpsRangeTo =>
            NormalizedIndex { element: false, start: 0, end: index.b },
        IndexKind::OpsRangeFrom | IndexKind::RangeRangeFrom =>
            NormalizedIndex { element: false, start: index.a, end: length },
        IndexKind::OpsRangeFull =>
            NormalizedIndex { element: false, start: 0, end: length },
        IndexKind::OpsRangeInclusive =>
            NormalizedIndex {
                element: false,
                start: if index.exhausted { index.b + 1 } else { index.a },
                end: index.b + 1,
            },
        IndexKind::RangeRangeInclusive =>
            NormalizedIndex { element: false, start: index.a, end: index.b + 1 },
        IndexKind::OpsRangeToInclusive | IndexKind::RangeRangeToInclusive =>
            NormalizedIndex { element: false, start: 0, end: index.b + 1 },
        IndexKind::OpsBoundPair =>
            NormalizedIndex {
                element: false,
                start: bound_start(index),
                end: bound_end(length, index),
            },
        IndexKind::ClampUsize => {
            let start = min_int(index.a, length - 1);
            NormalizedIndex { element: true, start, end: start + 1 }
        },
        IndexKind::ClampRangeRange | IndexKind::ClampOpsRange =>
            NormalizedIndex {
                element: false,
                start: min_int(index.a, length),
                end: min_int(index.b, length),
            },
        IndexKind::ClampRangeRangeInclusive
        | IndexKind::ClampOpsRangeInclusive =>
            NormalizedIndex {
                element: false,
                start: min_int(index.a, length - 1),
                end: min_int(index.b, length - 1) + 1,
            },
        IndexKind::ClampRangeRangeFrom | IndexKind::ClampOpsRangeFrom =>
            NormalizedIndex {
                element: false,
                start: min_int(index.a, length),
                end: length,
            },
        IndexKind::ClampOpsRangeTo =>
            NormalizedIndex {
                element: false,
                start: 0,
                end: min_int(index.b, length),
            },
        IndexKind::ClampRangeRangeToInclusive
        | IndexKind::ClampOpsRangeToInclusive =>
            NormalizedIndex {
                element: false,
                start: 0,
                end: min_int(index.b, length - 1) + 1,
            },
        IndexKind::ClampOpsRangeFull =>
            NormalizedIndex { element: false, start: 0, end: length },
        IndexKind::Last =>
            NormalizedIndex { element: true, start: length - 1, end: length },
    }
}

pub open spec fn index_in_range(input: Input) -> bool {
    let normalized = normalize(input.values.len() as int, input.index);
    0 <= normalized.start
        && normalized.start <= normalized.end
        && normalized.end <= input.values.len()
}

pub open spec fn valid_input(input: Input) -> bool {
    input.values.len() <= 3
        && input.index.a >= 0
        && input.index.b >= 0
        && input.allocation > 0
        && input.address > 0
        && input.provenance > 0
        && input.root_borrow > 0
        && input.element_size >= 0
        && input.frame_token > 0
        && index_in_range(input)
}

pub open spec fn boundary_t(input: Input, boundary: Boundary) -> bool {
    boundary.values == input.values
        && boundary.allocation == input.allocation
        && boundary.address == input.address
        && boundary.provenance == input.provenance
        && boundary.root_borrow == input.root_borrow
        && boundary.element_size == input.element_size
        && boundary.frame_token == input.frame_token
}

pub open spec fn returned_address(input: Input) -> int {
    let start = normalize(input.values.len() as int, input.index).start;
    input.address
        + if input.element_size == 0 {
            0
        } else {
            start * input.element_size
        }
}

pub open spec fn source_output(input: Input) -> Output {
    let normalized = normalize(input.values.len() as int, input.index);
    Output {
        element: normalized.element,
        start: normalized.start,
        length: normalized.end - normalized.start,
        values: input.values.subrange(normalized.start, normalized.end),
        allocation: input.allocation,
        address: returned_address(input),
        provenance: input.provenance,
        parent_borrow: input.root_borrow,
    }
}

pub open spec fn source_state(input: Input) -> FinalState {
    FinalState {
        values: input.values,
        allocation: input.allocation,
        address: input.address,
        provenance: input.provenance,
        root_borrow: input.root_borrow,
        element_size: input.element_size,
        frame_token: input.frame_token,
    }
}

pub open spec fn target_transition(
    input: Input,
    boundary: Boundary,
    output: Output,
    state: FinalState,
) -> bool {
    valid_input(input)
        && boundary_t(input, boundary)
        && output == source_output(input)
        && state == source_state(input)
}

pub proof fn every_sealed_rust_1_96_kind_is_normalized(input: Input)
    ensures
        normalize(input.values.len() as int, input.index)
            == normalize(input.values.len() as int, input.index),
{
    match input.index.kind {
        IndexKind::Usize => {},
        IndexKind::OpsIndexRange => {},
        IndexKind::OpsRange => {},
        IndexKind::RangeRange => {},
        IndexKind::OpsRangeTo => {},
        IndexKind::OpsRangeFrom => {},
        IndexKind::RangeRangeFrom => {},
        IndexKind::OpsRangeFull => {},
        IndexKind::OpsRangeInclusive => {},
        IndexKind::RangeRangeInclusive => {},
        IndexKind::OpsRangeToInclusive => {},
        IndexKind::RangeRangeToInclusive => {},
        IndexKind::OpsBoundPair => {},
        IndexKind::ClampUsize => {},
        IndexKind::ClampRangeRange => {},
        IndexKind::ClampOpsRange => {},
        IndexKind::ClampRangeRangeInclusive => {},
        IndexKind::ClampOpsRangeInclusive => {},
        IndexKind::ClampRangeRangeFrom => {},
        IndexKind::ClampOpsRangeFrom => {},
        IndexKind::ClampOpsRangeTo => {},
        IndexKind::ClampRangeRangeToInclusive => {},
        IndexKind::ClampOpsRangeToInclusive => {},
        IndexKind::ClampOpsRangeFull => {},
        IndexKind::Last => {},
    }
}

pub proof fn conditional_complete_for_every_sealed_sliceindex(
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
}

}
