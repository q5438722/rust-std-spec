#![allow(dead_code, unused_imports, unused_variables)]
// Trusted-free source model for core::slice::from_raw_parts_mut.

use vstd::prelude::*;
use vstd::map::*;
use vstd::seq::*;

verus! {

pub ghost struct Input {
    pub length: int,
    pub allocation: int,
    pub address: int,
    pub provenance: int,
    pub root_borrow: int,
    pub single_allocation: bool,
    pub allocation_base: int,
    pub allocation_bytes: int,
    pub element_size: int,
    pub element_alignment: int,
    pub usize_max: int,
    pub isize_max: int,
    pub address_space_limit: int,
    pub alias_readers: int,
    pub alias_writers: int,
    pub frame_token: int,
}

pub ghost struct Boundary {
    pub memory: Map<int, int>,
    pub initialized: Map<int, bool>,
    pub allocation: int,
    pub address: int,
    pub provenance: int,
    pub root_borrow: int,
    pub single_allocation: bool,
    pub allocation_base: int,
    pub allocation_bytes: int,
    pub element_size: int,
    pub element_alignment: int,
    pub usize_max: int,
    pub isize_max: int,
    pub address_space_limit: int,
    pub alias_readers: int,
    pub alias_writers: int,
    pub frame_token: int,
}

pub ghost struct Output {
    pub memory: Seq<int>,
    pub length: int,
    pub allocation: int,
    pub address: int,
    pub provenance: int,
    pub borrow: int,
    pub mutable: bool,
}

pub ghost struct FinalState {
    pub memory: Seq<int>,
    pub length: int,
    pub allocation: int,
    pub address: int,
    pub provenance: int,
    pub borrow: int,
    pub mutable: bool,
    pub alias_readers: int,
    pub alias_writers: int,
    pub frame_token: int,
}

pub open spec fn byte_count(input: Input) -> int {
    input.length * input.element_size
}

pub open spec fn endpoint(input: Input) -> int {
    input.address + byte_count(input)
}

pub open spec fn allocation_end(input: Input) -> int {
    input.allocation_base + input.allocation_bytes
}

pub open spec fn returned_index(input: Input, index: int) -> bool {
    0 <= index < input.length
}

pub open spec fn element_address(input: Input, index: int) -> int {
    if input.element_size == 0 {
        input.address
    } else {
        input.address + index * input.element_size
    }
}

pub open spec fn addressed_range_initialized(
    input: Input,
    boundary: Boundary,
) -> bool {
    forall|i: int| #![auto] returned_index(input, i) ==> (
        boundary.memory.dom().contains(element_address(input, i))
            && boundary.initialized.dom().contains(element_address(input, i))
            && boundary.initialized[element_address(input, i)]
    )
}

pub open spec fn returned_view(
    input: Input,
    boundary: Boundary,
) -> Seq<int> {
    Seq::new(
        if input.length >= 0 { input.length as nat } else { 0 },
        |i: int| boundary.memory[element_address(input, i)],
    )
}

pub open spec fn valid_input(input: Input) -> bool {
    0 <= input.length <= input.usize_max
        && input.address > 0
        && input.root_borrow > 0
        && input.single_allocation
        && input.allocation >= 0
        && input.provenance >= 0
        && input.allocation_base >= 0
        && input.allocation_bytes >= 0
        && input.element_size >= 0
        && input.element_alignment > 0
        && input.usize_max > 0
        && input.isize_max > 0
        && input.address_space_limit > 0
        && input.address % input.element_alignment == 0
        && (input.element_size == 0
            || (input.element_size >= input.element_alignment
                && input.element_size % input.element_alignment == 0))
        && byte_count(input) <= input.isize_max
        && endpoint(input) <= input.address_space_limit
        && ((byte_count(input) == 0
            && ((input.allocation == 0 && input.provenance == 0)
                || (input.allocation > 0
                    && input.provenance > 0
                    && input.allocation_base <= input.address
                    && input.address <= allocation_end(input)
                    && allocation_end(input) <= input.address_space_limit)))
            || (byte_count(input) > 0
                && input.allocation > 0
                && input.provenance > 0
                && input.allocation_base <= input.address
                && endpoint(input) <= allocation_end(input)
                && allocation_end(input) <= input.address_space_limit))
        && (true
            ==> (input.alias_readers == 0 && input.alias_writers == 0))
        && (!true ==> input.alias_readers >= 0 && input.alias_writers == 0)
        && input.frame_token > 0
}

pub open spec fn boundary_holds(input: Input, boundary: Boundary) -> bool {
    boundary.allocation == input.allocation
        && boundary.address == input.address
        && boundary.provenance == input.provenance
        && boundary.root_borrow == input.root_borrow
        && boundary.single_allocation == input.single_allocation
        && boundary.allocation_base == input.allocation_base
        && boundary.allocation_bytes == input.allocation_bytes
        && boundary.element_size == input.element_size
        && boundary.element_alignment == input.element_alignment
        && boundary.usize_max == input.usize_max
        && boundary.isize_max == input.isize_max
        && boundary.address_space_limit == input.address_space_limit
        && boundary.alias_readers == input.alias_readers
        && boundary.alias_writers == input.alias_writers
        && boundary.frame_token == input.frame_token
        && addressed_range_initialized(input, boundary)
}

pub open spec fn source_output(input: Input, boundary: Boundary) -> Output {
    Output {
        memory: returned_view(input, boundary),
        length: input.length,
        allocation: input.allocation,
        address: input.address,
        provenance: input.provenance,
        borrow: input.root_borrow,
        mutable: true,
    }
}

pub open spec fn framed_state(
    input: Input,
    boundary: Boundary,
    final_memory: Seq<int>,
) -> FinalState {
    FinalState {
        memory: final_memory,
        length: input.length,
        allocation: input.allocation,
        address: input.address,
        provenance: input.provenance,
        borrow: input.root_borrow,
        mutable: true,
        alias_readers: input.alias_readers,
        alias_writers: input.alias_writers,
        frame_token: input.frame_token,
    }
}

pub open spec fn state_frame(
    input: Input,
    boundary: Boundary,
    state: FinalState,
) -> bool {
    state.memory.len() == input.length
        && state == framed_state(
            input,
            boundary,
            if true {
                state.memory
            } else {
                returned_view(input, boundary)
            },
        )
}

pub open spec fn active_contract(
    input: Input,
    boundary: Boundary,
    output: Output,
) -> bool {
    valid_input(input)
        && output.length == input.length
        && output.memory == returned_view(input, boundary)
        && output.allocation == input.allocation
        && output.address == input.address
        && output.provenance == input.provenance
        && output.borrow == input.root_borrow
        && output.mutable == true
}

pub open spec fn target_transition(
    input: Input,
    boundary: Boundary,
    output: Output,
    state: FinalState,
) -> bool {
    valid_input(input)
        && boundary_holds(input, boundary)
        && output == source_output(input, boundary)
        && state_frame(input, boundary, state)
        && active_contract(input, boundary, output)
}

pub proof fn conditional_complete_exact_output_from_raw_parts_mut(
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
{
    reveal(target_transition);
}


pub proof fn mutable_distinct_final_memory_witness(
    input: Input,
    boundary: Boundary,
    first: Seq<int>,
    second: Seq<int>,
)
    requires
        valid_input(input),
        boundary_holds(input, boundary),
        first.len() == input.length,
        second.len() == input.length,
        first != second,
    ensures
        target_transition(
            input,
            boundary,
            source_output(input, boundary),
            framed_state(input, boundary, first),
        ),
        target_transition(
            input,
            boundary,
            source_output(input, boundary),
            framed_state(input, boundary, second),
        ),
        framed_state(input, boundary, first)
            != framed_state(input, boundary, second),
{
    reveal(target_transition);
    reveal(active_contract);
    reveal(state_frame);
}

} // verus!
