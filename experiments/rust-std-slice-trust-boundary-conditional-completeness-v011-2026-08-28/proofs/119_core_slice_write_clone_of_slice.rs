#![allow(dead_code, unused_imports, unused_variables)]
// Experiment-local source model for core::slice::write_clone_of_slice.

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub ghost struct PointerIdentity {
    pub allocation: int,
    pub address: nat,
    pub provenance: int,
}

pub ghost struct CloneInput {
    pub destination_initialized: Seq<bool>,
    pub destination_values: Seq<int>,
    pub source_values: Seq<int>,
    pub destination_pointer: PointerIdentity,
    pub source_pointer: PointerIdentity,
    pub destination_borrow: int,
    pub clone_initial_state: int,
    pub destruct_initial_state: int,
    pub frame_token: int,
}

pub ghost struct Boundary {
    pub destination_initialized: Seq<bool>,
    pub destination_values: Seq<int>,
    pub source_values: Seq<int>,
    pub destination_pointer: PointerIdentity,
    pub source_pointer: PointerIdentity,
    pub destination_borrow: int,
    pub clone_results: Seq<int>,
    pub clone_state_before: Seq<int>,
    pub clone_state_after: Seq<int>,
    pub clone_completed: Seq<bool>,
    pub clone_initial_state: int,
    pub destruct_initial_state: int,
    pub frame_token: int,
}

pub ghost struct ReturnedSlice {
    pub pointer: PointerIdentity,
    pub borrow: int,
    pub values: Seq<int>,
}

pub ghost struct FinalState {
    pub destination_initialized: Seq<bool>,
    pub destination_values: Seq<int>,
    pub destination_pointer: PointerIdentity,
    pub source_values: Seq<int>,
    pub source_pointer: PointerIdentity,
    pub returned: ReturnedSlice,
    pub clone_state_after: Seq<int>,
    pub destruct_state: int,
    pub frame_token: int,
}

pub open spec fn valid_input(input: CloneInput) -> bool {
    input.destination_initialized.len() == input.source_values.len()
        && input.destination_values.len() == input.source_values.len()
        && input.destination_pointer.address > 0
        && input.source_pointer.address > 0
        && input.destination_borrow > 0
}

pub open spec fn clone_chain(input: CloneInput, boundary: Boundary) -> bool {
    boundary.clone_results.len() == input.source_values.len()
        && boundary.clone_state_before.len() == input.source_values.len()
        && boundary.clone_state_after.len() == input.source_values.len()
        && boundary.clone_completed.len() == input.source_values.len()
        && forall|i: int| 0 <= i < input.source_values.len() ==> (
            boundary.clone_completed[i]
                && boundary.clone_state_before[i]
                    == if i == 0 {
                        input.clone_initial_state
                    } else {
                        boundary.clone_state_after[i - 1]
                    }
        )
}

pub open spec fn boundary_observed(input: CloneInput, boundary: Boundary) -> bool {
    boundary.destination_initialized == input.destination_initialized
        && boundary.destination_values == input.destination_values
        && boundary.source_values == input.source_values
        && boundary.destination_pointer == input.destination_pointer
        && boundary.source_pointer == input.source_pointer
        && boundary.destination_borrow == input.destination_borrow
        && boundary.clone_initial_state == input.clone_initial_state
        && boundary.destruct_initial_state == input.destruct_initial_state
        && boundary.frame_token == input.frame_token
        && clone_chain(input, boundary)
}

pub open spec fn source_ordered_clone_writes(
    input: CloneInput,
    boundary: Boundary,
) -> bool {
    boundary.clone_results == input.source_values
}

pub open spec fn initialized_destination(input: CloneInput) -> Seq<bool> {
    Seq::new(input.source_values.len(), |i: int| true)
}

pub open spec fn assume_init_mut_return(input: CloneInput) -> ReturnedSlice {
    ReturnedSlice {
        pointer: input.destination_pointer,
        borrow: input.destination_borrow,
        values: input.source_values,
    }
}

pub open spec fn source_final_state(
    input: CloneInput,
    boundary: Boundary,
) -> FinalState {
    FinalState {
        destination_initialized: initialized_destination(input),
        destination_values: input.source_values,
        destination_pointer: input.destination_pointer,
        source_values: input.source_values,
        source_pointer: input.source_pointer,
        returned: assume_init_mut_return(input),
        clone_state_after: boundary.clone_state_after,
        destruct_state: input.destruct_initial_state,
        frame_token: input.frame_token,
    }
}

pub open spec fn target_definition(
    input: CloneInput,
    boundary: Boundary,
    output: ReturnedSlice,
    state: FinalState,
) -> bool {
    boundary_observed(input, boundary)
        && source_ordered_clone_writes(input, boundary)
        && output == assume_init_mut_return(input)
        && state == source_final_state(input, boundary)
}

pub proof fn every_slot_is_written_in_source_order(
    input: CloneInput,
    boundary: Boundary,
    index: int,
)
    requires
        valid_input(input),
        boundary_observed(input, boundary),
        source_ordered_clone_writes(input, boundary),
        0 <= index < input.source_values.len(),
    ensures
        initialized_destination(input)[index],
        boundary.clone_results[index] == input.source_values[index],
        boundary.clone_completed[index],
{
    reveal(initialized_destination);
    reveal(source_ordered_clone_writes);
    reveal(boundary_observed);
    reveal(clone_chain);
}

pub proof fn exact_output_and_state_determinism(
    input: CloneInput,
    boundary: Boundary,
    output1: ReturnedSlice,
    state1: FinalState,
    output2: ReturnedSlice,
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

pub proof fn panic_guard_counts_initialized_prefix(
    source_length: nat,
    panic_index: nat,
)
    requires
        panic_index < source_length,
    ensures
        panic_index <= source_length,
        panic_index + 1 <= source_length,
{
}

}
