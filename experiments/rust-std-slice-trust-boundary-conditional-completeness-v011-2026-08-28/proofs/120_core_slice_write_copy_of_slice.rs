#![allow(dead_code, unused_imports, unused_variables)]
// Experiment-local per-slot source model for core::slice::write_copy_of_slice.

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub ghost struct PointerIdentity {
    pub allocation: int,
    pub address: nat,
    pub provenance: int,
}

pub ghost struct InitialDestination {
    pub initialized: Seq<bool>,
    pub initialized_values: Seq<int>,
}

pub ghost struct CopyInput {
    pub destination: InitialDestination,
    pub source_values: Seq<int>,
    pub destination_pointer: PointerIdentity,
    pub source_pointer: PointerIdentity,
    pub destination_borrow: int,
    pub destination_allocation_base: nat,
    pub destination_allocation_bytes: nat,
    pub source_allocation_base: nat,
    pub source_allocation_bytes: nat,
    pub element_size: nat,
    pub element_alignment: nat,
    pub isize_max: nat,
    pub address_space_limit: nat,
    pub frame_token: int,
}

pub ghost struct Boundary {
    pub destination_initialized: Seq<bool>,
    pub destination_initialized_values: Seq<int>,
    pub source_values: Seq<int>,
    pub destination_pointer: PointerIdentity,
    pub source_pointer: PointerIdentity,
    pub destination_borrow: int,
    pub destination_allocation_base: nat,
    pub destination_allocation_bytes: nat,
    pub source_allocation_base: nat,
    pub source_allocation_bytes: nat,
    pub element_size: nat,
    pub element_alignment: nat,
    pub isize_max: nat,
    pub address_space_limit: nat,
    pub frame_token: int,
}

pub ghost struct InitializedStorage {
    pub initialized: Seq<bool>,
    pub values: Seq<int>,
}

pub ghost struct ReturnedSlice {
    pub pointer: PointerIdentity,
    pub borrow: int,
    pub values: Seq<int>,
}

pub ghost struct FinalState {
    pub destination: InitializedStorage,
    pub destination_pointer: PointerIdentity,
    pub destination_borrow: int,
    pub destination_allocation_base: nat,
    pub destination_allocation_bytes: nat,
    pub source_values: Seq<int>,
    pub source_pointer: PointerIdentity,
    pub source_allocation_base: nat,
    pub source_allocation_bytes: nat,
    pub returned: ReturnedSlice,
    pub element_size: nat,
    pub element_alignment: nat,
    pub isize_max: nat,
    pub address_space_limit: nat,
    pub frame_token: int,
}

pub open spec fn byte_count(input: CopyInput) -> nat {
    input.source_values.len() * input.element_size
}

pub open spec fn valid_input(input: CopyInput) -> bool {
    input.destination.initialized.len() == input.source_values.len()
        && input.destination.initialized_values.len() == input.source_values.len()
        && input.destination_pointer.address > 0
        && input.source_pointer.address > 0
        && input.destination_borrow > 0
        && input.destination_pointer.allocation >= 0
        && input.destination_pointer.provenance >= 0
        && input.source_pointer.allocation >= 0
        && input.source_pointer.provenance >= 0
        && input.element_alignment > 0
        && input.destination_pointer.address % input.element_alignment == 0
        && input.source_pointer.address % input.element_alignment == 0
        && (input.element_size == 0
            || (input.element_size >= input.element_alignment
                && input.element_size % input.element_alignment == 0))
        && byte_count(input) <= input.isize_max
        && input.destination_pointer.address + byte_count(input)
            <= input.address_space_limit
        && input.source_pointer.address + byte_count(input)
            <= input.address_space_limit
        && (byte_count(input) == 0
            || (input.destination_pointer.allocation > 0
                && input.destination_pointer.provenance > 0
                && input.source_pointer.allocation > 0
                && input.source_pointer.provenance > 0
                && input.destination_allocation_base <= input.destination_pointer.address
                && input.destination_pointer.address + byte_count(input)
                    <= input.destination_allocation_base
                        + input.destination_allocation_bytes
                && input.source_allocation_base <= input.source_pointer.address
                && input.source_pointer.address + byte_count(input)
                    <= input.source_allocation_base + input.source_allocation_bytes
                && (input.destination_pointer.allocation
                        != input.source_pointer.allocation
                    || input.destination_pointer.address + byte_count(input)
                        <= input.source_pointer.address
                    || input.source_pointer.address + byte_count(input)
                        <= input.destination_pointer.address)))
}

pub open spec fn boundary_observed(input: CopyInput, boundary: Boundary) -> bool {
    boundary.destination_initialized == input.destination.initialized
        && boundary.destination_initialized_values.len()
            == input.destination.initialized_values.len()
        && (forall|i: int| #![auto]
            0 <= i < input.destination.initialized.len()
                && input.destination.initialized[i] ==>
                    boundary.destination_initialized_values[i]
                        == input.destination.initialized_values[i])
        && boundary.source_values == input.source_values
        && boundary.destination_pointer == input.destination_pointer
        && boundary.source_pointer == input.source_pointer
        && boundary.destination_borrow == input.destination_borrow
        && boundary.destination_allocation_base
            == input.destination_allocation_base
        && boundary.destination_allocation_bytes
            == input.destination_allocation_bytes
        && boundary.source_allocation_base == input.source_allocation_base
        && boundary.source_allocation_bytes == input.source_allocation_bytes
        && boundary.element_size == input.element_size
        && boundary.element_alignment == input.element_alignment
        && boundary.isize_max == input.isize_max
        && boundary.address_space_limit == input.address_space_limit
        && boundary.frame_token == input.frame_token
}

pub open spec fn transmuted_source_initialized_at(
    input: CopyInput,
    index: int,
) -> bool {
    0 <= index < input.source_values.len()
}

pub open spec fn transmuted_source_value_at(
    input: CopyInput,
    index: int,
) -> int
    recommends
        transmuted_source_initialized_at(input, index),
{
    input.source_values[index]
}

pub open spec fn copy_nonoverlapping_initialized_at(
    input: CopyInput,
    index: int,
) -> bool {
    transmuted_source_initialized_at(input, index)
}

pub open spec fn copy_nonoverlapping_value_at(
    input: CopyInput,
    index: int,
) -> int
    recommends
        copy_nonoverlapping_initialized_at(input, index),
{
    transmuted_source_value_at(input, index)
}

pub open spec fn copied_destination(input: CopyInput) -> InitializedStorage {
    InitializedStorage {
        initialized: Seq::new(input.source_values.len(), |i: int|
            copy_nonoverlapping_initialized_at(input, i)),
        values: Seq::new(input.source_values.len(), |i: int|
            copy_nonoverlapping_value_at(input, i)),
    }
}

pub open spec fn assume_init_return(input: CopyInput) -> ReturnedSlice {
    ReturnedSlice {
        pointer: input.destination_pointer,
        borrow: input.destination_borrow,
        values: copied_destination(input).values,
    }
}

pub open spec fn source_final_state(input: CopyInput) -> FinalState {
    FinalState {
        destination: copied_destination(input),
        destination_pointer: input.destination_pointer,
        destination_borrow: input.destination_borrow,
        destination_allocation_base: input.destination_allocation_base,
        destination_allocation_bytes: input.destination_allocation_bytes,
        source_values: input.source_values,
        source_pointer: input.source_pointer,
        source_allocation_base: input.source_allocation_base,
        source_allocation_bytes: input.source_allocation_bytes,
        returned: assume_init_return(input),
        element_size: input.element_size,
        element_alignment: input.element_alignment,
        isize_max: input.isize_max,
        address_space_limit: input.address_space_limit,
        frame_token: input.frame_token,
    }
}

pub open spec fn target_definition(
    input: CopyInput,
    boundary: Boundary,
    output: ReturnedSlice,
    state: FinalState,
) -> bool {
    boundary_observed(input, boundary)
        && output == assume_init_return(input)
        && state == source_final_state(input)
}

pub proof fn copied_slot_is_initialized_and_equal(
    input: CopyInput,
    index: int,
)
    requires
        valid_input(input),
        0 <= index < input.source_values.len(),
    ensures
        copied_destination(input).initialized[index],
        copied_destination(input).values[index] == input.source_values[index],
{
    reveal(copied_destination);
    reveal(copy_nonoverlapping_initialized_at);
    reveal(copy_nonoverlapping_value_at);
    reveal(transmuted_source_initialized_at);
    reveal(transmuted_source_value_at);
}

pub proof fn exact_output_determinism(
    input: CopyInput,
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
{
    reveal(target_definition);
}

pub proof fn full_exact_equivalence(
    input: CopyInput,
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

}
