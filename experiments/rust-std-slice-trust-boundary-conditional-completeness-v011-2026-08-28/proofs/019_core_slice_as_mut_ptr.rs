#![allow(dead_code, unused_imports, unused_variables)]
// Source-transition model for core::slice::as_mut_ptr.

use vstd::prelude::*;

verus! {

pub ghost struct SliceInput {
    pub sequence: int,
    pub len: nat,
    pub allocation: int,
    pub address: nat,
    pub provenance: int,
    pub element_size: nat,
    pub element_alignment: nat,
    pub allocation_base: nat,
    pub allocation_bytes: nat,
    pub isize_max: nat,
    pub address_space_limit: nat,
    pub mutable_identity: int,
    pub frame_token: int,
}

pub ghost struct Boundary {
    pub allocation: int,
    pub address: nat,
    pub provenance: int,
    pub element_size: nat,
    pub element_alignment: nat,
    pub allocation_base: nat,
    pub allocation_bytes: nat,
    pub isize_max: nat,
    pub address_space_limit: nat,
    pub mutable_identity: int,
    pub frame_token: int,
}

pub ghost struct Pointer {
    pub allocation: int,
    pub address: nat,
    pub provenance: int,
}

pub ghost struct FinalState {
    pub sequence: int,
    pub len: nat,
    pub allocation: int,
    pub address: nat,
    pub provenance: int,
    pub element_size: nat,
    pub element_alignment: nat,
    pub allocation_base: nat,
    pub allocation_bytes: nat,
    pub mutable_identity: int,
    pub frame_token: int,
}

pub open spec fn byte_span(input: SliceInput) -> nat {
    input.len * input.element_size
}

pub open spec fn valid_input(input: SliceInput) -> bool {
    input.allocation >= 0
        && input.provenance >= 0
        && input.address > 0
        && input.element_alignment > 0
        && input.address % input.element_alignment == 0
        && (input.element_size == 0
            || (input.element_size >= input.element_alignment
                && input.element_size % input.element_alignment == 0))
        && byte_span(input) <= input.isize_max
        && input.address + byte_span(input) <= input.address_space_limit
        && input.mutable_identity > 0
        && (byte_span(input) == 0
            || (input.allocation > 0
                && input.provenance > 0
                && input.allocation_base + input.allocation_bytes
                    <= input.address_space_limit
                && input.allocation_base <= input.address
                && input.address + byte_span(input)
                    <= input.allocation_base + input.allocation_bytes))
}

pub proof fn rejects_misaligned_regression_input(input: SliceInput)
    requires
        input.address == 1026,
        input.element_alignment == 4,
    ensures
        !valid_input(input),
{
    reveal(valid_input);
}

pub open spec fn boundary_observed(input: SliceInput, boundary: Boundary) -> bool {
    boundary.allocation == input.allocation
        && boundary.address == input.address
        && boundary.provenance == input.provenance
        && boundary.element_size == input.element_size
        && boundary.element_alignment == input.element_alignment
        && boundary.allocation_base == input.allocation_base
        && boundary.allocation_bytes == input.allocation_bytes
        && boundary.isize_max == input.isize_max
        && boundary.address_space_limit == input.address_space_limit
        && boundary.mutable_identity == input.mutable_identity
        && boundary.frame_token == input.frame_token
}

pub open spec fn slice_to_thin_mut_pointer(input: SliceInput) -> Pointer {
    Pointer {
        allocation: input.allocation,
        address: input.address,
        provenance: input.provenance,
    }
}

pub open spec fn unchanged_state(input: SliceInput) -> FinalState {
    FinalState {
        sequence: input.sequence,
        len: input.len,
        allocation: input.allocation,
        address: input.address,
        provenance: input.provenance,
        element_size: input.element_size,
        element_alignment: input.element_alignment,
        allocation_base: input.allocation_base,
        allocation_bytes: input.allocation_bytes,
        mutable_identity: input.mutable_identity,
        frame_token: input.frame_token,
    }
}

pub open spec fn target_definition(
    input: SliceInput,
    boundary: Boundary,
    output: Pointer,
    state: FinalState,
) -> bool {
    boundary_observed(input, boundary)
        && output == slice_to_thin_mut_pointer(input)
        && state == unchanged_state(input)
}

pub open spec fn exact_pointer(left: Pointer, right: Pointer) -> bool {
    left.allocation == right.allocation
        && left.address == right.address
        && left.provenance == right.provenance
}

pub open spec fn exact_state(left: FinalState, right: FinalState) -> bool {
    left.sequence == right.sequence
        && left.len == right.len
        && left.allocation == right.allocation
        && left.address == right.address
        && left.provenance == right.provenance
        && left.element_size == right.element_size
        && left.element_alignment == right.element_alignment
        && left.allocation_base == right.allocation_base
        && left.allocation_bytes == right.allocation_bytes
        && left.mutable_identity == right.mutable_identity
        && left.frame_token == right.frame_token
}

pub proof fn exact_output_determinism(
    input: SliceInput,
    boundary: Boundary,
    output1: Pointer,
    state1: FinalState,
    output2: Pointer,
    state2: FinalState,
)
    requires
        valid_input(input),
        boundary_observed(input, boundary),
        target_definition(input, boundary, output1, state1),
        target_definition(input, boundary, output2, state2),
    ensures
        exact_pointer(output1, output2),
{
    reveal(target_definition);
    reveal(slice_to_thin_mut_pointer);
    reveal(exact_pointer);
}

pub proof fn full_exact_equivalence(
    input: SliceInput,
    boundary: Boundary,
    output1: Pointer,
    state1: FinalState,
    output2: Pointer,
    state2: FinalState,
)
    requires
        valid_input(input),
        boundary_observed(input, boundary),
        target_definition(input, boundary, output1, state1),
        target_definition(input, boundary, output2, state2),
    ensures
        exact_pointer(output1, output2),
        exact_state(state1, state2),
{
    reveal(target_definition);
    reveal(slice_to_thin_mut_pointer);
    reveal(unchanged_state);
    reveal(exact_pointer);
    reveal(exact_state);
}

}
