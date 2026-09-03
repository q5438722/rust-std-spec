#![allow(dead_code, unused_imports, unused_variables)]
// Source-backed two-execution model for core::slice::split_off_mut.

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub ghost struct SliceIdentity {
    pub source: Seq<int>,
    pub start: int,
    pub address: int,
    pub allocation: int,
    pub provenance: int,
    pub parent_borrow: int,
    pub element_size: nat,
    pub element_alignment: nat,
}

pub ghost struct RegionIdentity {
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
}

pub ghost struct Input {
    pub slice: SliceIdentity,
    pub range_kind: int,
    pub range_index: nat,
}

pub ghost struct Boundary {
    pub input_address: int,
    pub input_allocation: int,
    pub input_provenance: int,
    pub parent_borrow: int,
    pub element_size: nat,
    pub element_alignment: nat,
}

pub ghost struct Output {
    pub is_some: bool,
    pub returned: RegionIdentity,
}

pub ghost struct FinalState {
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
}

pub open spec fn empty_region() -> RegionIdentity {
    RegionIdentity {
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
    }
}

pub open spec fn input_region(input: Input) -> RegionIdentity {
    RegionIdentity {
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
        unique: true,
    }
}

pub open spec fn make_region(
    input: Input,
    offset: int,
    length: int,
    projection: int,
) -> RegionIdentity {
    RegionIdentity {
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
        unique: true,
    }
}

pub open spec fn helper_has_split(input: Input) -> bool {
    !(input.range_kind == 2
        && input.range_index == 18446744073709551615)
}

pub open spec fn helper_direction(input: Input) -> int {
    if helper_has_split(input) {
        if input.range_kind == 0 { 1 } else { 0 }
    } else {
        -1
    }
}

pub open spec fn helper_split_index(input: Input) -> int {
    if helper_has_split(input) {
        if input.range_kind == 2 {
            input.range_index as int + 1
        } else {
            input.range_index as int
        }
    } else {
        -1
    }
}

pub open spec fn branch_succeeds(input: Input) -> bool {
    helper_has_split(input)
        && helper_split_index(input) <= input.slice.source.len() as int
}

pub open spec fn front_region(input: Input) -> RegionIdentity
    recommends branch_succeeds(input)
{
    make_region(input, 0, helper_split_index(input), 1)
}

pub open spec fn back_region(input: Input) -> RegionIdentity
    recommends branch_succeeds(input)
{
    make_region(
        input,
        helper_split_index(input),
        input.slice.source.len() as int - helper_split_index(input),
        2,
    )
}

pub open spec fn source_output(input: Input) -> Output {
    if branch_succeeds(input) {
        Output {
            is_some: true,
            returned: if helper_direction(input) == 0 {
                front_region(input)
            } else {
                back_region(input)
            },
        }
    } else {
        Output { is_some: false, returned: empty_region() }
    }
}

pub open spec fn source_state(input: Input) -> FinalState {
    if branch_succeeds(input) {
        let front = front_region(input);
        let back = back_region(input);
        let returned = if helper_direction(input) == 0 { front } else { back };
        let receiver = if helper_direction(input) == 0 { back } else { front };
        FinalState {
            helper_has_split: true,
            direction: helper_direction(input),
            split_index: helper_split_index(input),
            bounds_ok: true,
            take_performed: true,
            receiver_empty_after_take: true,
            taken: if true { input_region(input) } else { empty_region() },
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
        }
    } else {
        FinalState {
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
        }
    }
}

pub open spec fn split_partition(
    source: Seq<int>,
    remaining: Seq<int>,
    removed: Seq<int>,
) -> bool {
    removed + remaining == source || remaining + removed == source
}

pub open spec fn valid_input(input: Input) -> bool {
    0 <= input.range_kind <= 2
        && input.range_index <= 18446744073709551615
        && input.slice.element_alignment > 0
}

pub open spec fn boundary_holds(
    input: Input,
    boundary: Boundary,
) -> bool {
    boundary.input_address == input.slice.address
        && boundary.input_allocation == input.slice.allocation
        && boundary.input_provenance == input.slice.provenance
        && boundary.parent_borrow == input.slice.parent_borrow
        && boundary.element_size == input.slice.element_size
        && boundary.element_alignment == input.slice.element_alignment
}

pub open spec fn active_contract(
    input: Input,
    output: Output,
    state: FinalState,
) -> bool {
    if output.is_some {
        split_partition(
            input.slice.source,
            state.receiver.values,
            output.returned.values,
        )
            && split_partition(
                input.slice.source,
                state.receiver.values,
                state.returned_final.values,
            )
    } else {
        state.receiver.values == input.slice.source
    }
}

pub open spec fn target_transition(
    input: Input,
    boundary: Boundary,
    output: Output,
    state: FinalState,
) -> bool {
    valid_input(input)
        && boundary_holds(input, boundary)
        && output == source_output(input)
        && state == source_state(input)
        && active_contract(input, output, state)
}

pub open spec fn same_output(left: Output, right: Output) -> bool {
    left == right
}

pub open spec fn same_state(left: FinalState, right: FinalState) -> bool {
    left == right
}

pub proof fn conditional_complete_split_off_mut(
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
{
    reveal(target_transition);
    reveal(same_output);
    reveal(same_state);
}

pub proof fn conditional_complete_exact_output_split_off_mut(
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
{
    reveal(target_transition);
    reveal(same_output);
}

} // verus!
