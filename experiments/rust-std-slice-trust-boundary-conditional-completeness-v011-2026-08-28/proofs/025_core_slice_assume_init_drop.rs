#![allow(dead_code, unused_imports, unused_variables)]
// Experiment-local source model for core::slice::assume_init_drop.

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub ghost struct PointerIdentity {
    pub allocation: int,
    pub address: nat,
    pub provenance: int,
}

pub ghost struct DropInput {
    pub values: Seq<int>,
    pub pointer: PointerIdentity,
    pub borrow: int,
    pub destruct_initial_state: int,
    pub element_size: nat,
    pub element_alignment: nat,
    pub frame_token: int,
}

pub ghost struct Boundary {
    pub values: Seq<int>,
    pub pointer: PointerIdentity,
    pub borrow: int,
    pub destruct_state_before: Seq<int>,
    pub destruct_state_after: Seq<int>,
    pub destruct_completed: Seq<bool>,
    pub element_size: nat,
    pub element_alignment: nat,
    pub frame_token: int,
}

pub ghost struct FinalState {
    pub initialized: Seq<bool>,
    pub pointer: PointerIdentity,
    pub borrow: int,
    pub destruct_state_after: Seq<int>,
    pub element_size: nat,
    pub element_alignment: nat,
    pub frame_token: int,
}

pub open spec fn valid_input(input: DropInput) -> bool {
    input.pointer.address > 0
        && input.pointer.allocation >= 0
        && input.pointer.provenance >= 0
        && input.borrow > 0
        && input.element_alignment > 0
        && (input.element_size == 0
            || (input.element_size >= input.element_alignment
                && input.element_size % input.element_alignment == 0))
}

pub open spec fn destruct_chain(input: DropInput, boundary: Boundary) -> bool {
    boundary.destruct_state_before.len() == input.values.len()
        && boundary.destruct_state_after.len() == input.values.len()
        && boundary.destruct_completed.len() == input.values.len()
        && forall|i: int| 0 <= i < input.values.len() ==> (
            boundary.destruct_completed[i]
                && boundary.destruct_state_before[i]
                    == if i == 0 {
                        input.destruct_initial_state
                    } else {
                        boundary.destruct_state_after[i - 1]
                    }
        )
}

pub open spec fn boundary_observed(input: DropInput, boundary: Boundary) -> bool {
    boundary.values == input.values
        && boundary.pointer == input.pointer
        && boundary.borrow == input.borrow
        && boundary.element_size == input.element_size
        && boundary.element_alignment == input.element_alignment
        && boundary.frame_token == input.frame_token
        && destruct_chain(input, boundary)
}

pub open spec fn source_final_state(
    input: DropInput,
    boundary: Boundary,
) -> FinalState {
    FinalState {
        initialized: Seq::new(input.values.len(), |i: int| false),
        pointer: input.pointer,
        borrow: input.borrow,
        destruct_state_after: boundary.destruct_state_after,
        element_size: input.element_size,
        element_alignment: input.element_alignment,
        frame_token: input.frame_token,
    }
}

pub open spec fn target_definition(
    input: DropInput,
    boundary: Boundary,
    output: bool,
    state: FinalState,
) -> bool {
    boundary_observed(input, boundary)
        && output
        && state == source_final_state(input, boundary)
}

pub proof fn every_source_slot_is_dropped(
    input: DropInput,
    boundary: Boundary,
    index: int,
)
    requires
        valid_input(input),
        boundary_observed(input, boundary),
        0 <= index < input.values.len(),
    ensures
        !source_final_state(input, boundary).initialized[index],
        boundary.destruct_completed[index],
{
    reveal(source_final_state);
    reveal(boundary_observed);
    reveal(destruct_chain);
}

pub proof fn exact_output_and_state_determinism(
    input: DropInput,
    boundary: Boundary,
    output1: bool,
    state1: FinalState,
    output2: bool,
    state2: FinalState,
)
    requires
        valid_input(input),
        boundary_observed(input, boundary),
        target_definition(input, boundary, output1, state1),
        target_definition(input, boundary, output2, state2),
    ensures
        output1 == output2,
        state1 == state2,
{
    reveal(target_definition);
}

}
