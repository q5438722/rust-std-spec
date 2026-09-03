#![allow(dead_code, unused_imports, unused_variables)]
// Source-backed arbitrary-length model for core::slice::split_first_mut.

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub ghost struct Input {
    pub source: Seq<int>,
    pub start: int,
    pub address: int,
    pub allocation: int,
    pub provenance: int,
    pub borrow: int,
    pub element_size: nat,
}

pub ghost struct RefIdentity {
    pub address: int,
    pub allocation: int,
    pub provenance: int,
    pub parent_borrow: int,
    pub start: int,
    pub length: int,
    pub element_size: nat,
    pub projection: int,
}

pub ghost struct SliceIdentity {
    pub source: Seq<int>,
    pub start: int,
    pub address: int,
    pub allocation: int,
    pub provenance: int,
    pub borrow: int,
    pub element_size: nat,
    pub projection: int,
}

pub ghost struct Boundary {
    pub input_address: int,
    pub input_allocation: int,
    pub input_provenance: int,
    pub input_borrow: int,
    pub element_size: nat,

}

pub ghost struct Output {
    pub is_some: bool,
    pub selected_index: int,
    pub selected_start: int,
    pub selected_value: int,
    pub selected_identity: RefIdentity,
    pub tuple_selected_first: bool,
    pub remainder: Seq<int>,
    pub remainder_start: int,
    pub remainder_length: int,
    pub remainder_identity: RefIdentity,
}

pub ghost struct FinalState {
    pub receiver: SliceIdentity,
    pub backing: Seq<int>,
    pub selected_final_value: int,
    pub remainder_final: Seq<int>,
}

pub open spec fn empty_ref_identity() -> RefIdentity {
    RefIdentity {
        address: 0,
        allocation: 0,
        provenance: 0,
        parent_borrow: 0,
        start: 0,
        length: 0,
        element_size: 0,
        projection: 0,
    }
}

pub open spec fn input_identity(input: Input) -> SliceIdentity {
    SliceIdentity {
        source: input.source,
        start: input.start,
        address: input.address,
        allocation: input.allocation,
        provenance: input.provenance,
        borrow: input.borrow,
        element_size: input.element_size,
        projection: 0,
    }
}

pub open spec fn same_ref(left: RefIdentity, right: RefIdentity) -> bool {
    left.address == right.address
        && left.allocation == right.allocation
        && left.provenance == right.provenance
        && left.parent_borrow == right.parent_borrow
        && left.start == right.start
        && left.length == right.length
        && left.element_size == right.element_size
        && left.projection == right.projection
}

pub open spec fn same_slice(left: SliceIdentity, right: SliceIdentity) -> bool {
    left.source == right.source
        && left.start == right.start
        && left.address == right.address
        && left.allocation == right.allocation
        && left.provenance == right.provenance
        && left.borrow == right.borrow
        && left.element_size == right.element_size
        && left.projection == right.projection
}

pub open spec fn boundary_holds(input: Input, boundary: Boundary) -> bool {
    boundary.input_address == input.address
        && boundary.input_allocation == input.allocation
        && boundary.input_provenance == input.provenance
        && boundary.input_borrow == input.borrow
        && boundary.element_size == input.element_size

}

pub open spec fn source_output(input: Input) -> Output {
    if input.source.len() == 0 {
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
        }
    } else {
        Output {
            is_some: true,
            selected_index: 0,
            selected_start: input.start + 0,
            selected_value: input.source[0],
            selected_identity: RefIdentity {
                address: input.address + 0 * input.element_size as int,
                allocation: input.allocation,
                provenance: input.provenance,
                parent_borrow: input.borrow,
                start: input.start + 0,
                length: 1,
                element_size: input.element_size,
                projection: 1,
            },
            tuple_selected_first: true,
            remainder: input.source.subrange(1, input.source.len() as int),
            remainder_start: input.start + 1,
            remainder_length: input.source.len() - 1,
            remainder_identity: RefIdentity {
                address: input.address + 1 * input.element_size as int,
                allocation: input.allocation,
                provenance: input.provenance,
                parent_borrow: input.borrow,
                start: input.start + 1,
                length: input.source.len() - 1,
                element_size: input.element_size,
                projection: 2,
            },
        }
    }
}

pub open spec fn source_state(
    input: Input,
    boundary: Boundary,
) -> FinalState {
    if input.source.len() == 0 {
        FinalState {
            receiver: input_identity(input),
            backing: input.source,
            selected_final_value: 0,
            remainder_final: Seq::empty(),
        }
    } else {
        FinalState {
            receiver: input_identity(input),
            backing: input.source,
            selected_final_value: input.source[0],
            remainder_final: input.source.subrange(1, input.source.len() as int),
        }
    }
}

pub open spec fn pattern_split_transition(
    input: Input,
    boundary: Boundary,
    output: Output,
    state: FinalState,
) -> bool {
    output == source_output(input)
        && state == source_state(input, boundary)
}


pub open spec fn direct_edge_result(
    input: Input,
    output: Output,
    state: FinalState,
) -> bool {
    if input.source.len() == 0 {
        !output.is_some && state.receiver.source == input.source
    } else {
        output.is_some
            && output.selected_value == input.source[0]
            && output.remainder == input.source.subrange(1, input.source.len() as int)
            && output.tuple_selected_first
            && state.receiver.source == seq![state.selected_final_value] + state.remainder_final
            && output.selected_start + 1 <= output.remainder_identity.start
    }
}

pub open spec fn source_transition(
    input: Input,
    boundary: Boundary,
    output: Output,
    state: FinalState,
) -> bool {
    output == source_output(input)
        && state == source_state(input, boundary)
        && pattern_split_transition(input, boundary, output, state)
}

pub open spec fn target_transition(
    input: Input,
    boundary: Boundary,
    output: Output,
    state: FinalState,
) -> bool {
    boundary_holds(input, boundary)
        && source_transition(input, boundary, output, state)
        && direct_edge_result(input, output, state)
}

pub open spec fn exact_equivalent(
    left: Output,
    left_state: FinalState,
    right: Output,
    right_state: FinalState,
) -> bool {
    left.is_some == right.is_some
        && left.selected_index == right.selected_index
        && left.selected_start == right.selected_start
        && left.selected_value == right.selected_value
        && same_ref(left.selected_identity, right.selected_identity)
        && left.tuple_selected_first == right.tuple_selected_first
        && left.remainder == right.remainder
        && left.remainder_start == right.remainder_start
        && left.remainder_length == right.remainder_length
        && same_ref(left.remainder_identity, right.remainder_identity)
        && same_slice(left_state.receiver, right_state.receiver)
        && left_state.backing == right_state.backing
        && left_state.selected_final_value == right_state.selected_final_value
        && left_state.remainder_final == right_state.remainder_final
}

pub proof fn conditional_complete_split_first_mut(
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
{
    reveal(target_transition);
    reveal(source_transition);
    reveal(exact_equivalent);
    reveal(same_ref);
    reveal(same_slice);
}

} // verus!
