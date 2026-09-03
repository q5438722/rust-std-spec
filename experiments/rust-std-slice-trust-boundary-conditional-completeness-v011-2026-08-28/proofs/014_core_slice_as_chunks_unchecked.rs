#![allow(dead_code, unused_imports, unused_variables)]
// Source-transition model for core::slice::as_chunks_unchecked.

use vstd::prelude::*;

verus! {

pub ghost struct Input {
    pub sequence: int,
    pub len: nat,
    pub n: nat,
    pub allocation: int,
    pub address: nat,
    pub provenance: int,
    pub element_size: nat,
    pub alignment: nat,
    pub allocation_base: nat,
    pub allocation_bytes: nat,
    pub one_allocation: bool,
    pub initialized: bool,
    pub isize_max: nat,
    pub address_space_limit: nat,
    pub borrow: int,
}

pub ghost struct Boundary {
    pub allocation: int,
    pub address: nat,
    pub provenance: int,
    pub element_size: nat,
    pub alignment: nat,
    pub allocation_base: nat,
    pub allocation_bytes: nat,
    pub one_allocation: bool,
    pub initialized: bool,
    pub isize_max: nat,
    pub address_space_limit: nat,
    pub borrow: int,
}

pub ghost struct Reference {
    pub allocation: int,
    pub address: nat,
    pub provenance: int,
    pub parent_borrow: int,
    pub start: nat,
    pub span: nat,
    pub width: nat,
}

pub ghost struct Output {
    pub reference: Reference,
    pub chunks_len: nat,
    pub source: int,
    pub start: nat,
    pub width: nat,
}

pub ghost struct FinalState {
    pub sequence: int,
    pub len: nat,
    pub allocation: int,
    pub address: nat,
    pub provenance: int,
    pub borrow: int,
    pub one_allocation: bool,
    pub initialized: bool,
}

pub open spec fn byte_span(input: Input) -> nat {
    input.len * input.element_size
}

pub open spec fn valid_input(input: Input) -> bool {
    input.n > 0
        && input.len % input.n == 0
        && input.address > 0
        && input.alignment > 0
        && input.address % input.alignment == 0
        && (input.element_size == 0
            || (input.element_size >= input.alignment
                && input.element_size % input.alignment == 0))
        && input.n * input.element_size <= input.isize_max
        && byte_span(input) <= input.isize_max
        && input.address + byte_span(input) <= input.address_space_limit
        && input.one_allocation
        && input.initialized
        && input.borrow > 0
        && (byte_span(input) == 0
            || (input.allocation > 0
                && input.provenance > 0
                && input.allocation_base <= input.address
                && input.address + byte_span(input)
                    <= input.allocation_base + input.allocation_bytes
                && input.allocation_base + input.allocation_bytes
                    <= input.address_space_limit))
}

pub open spec fn boundary_observed(input: Input, boundary: Boundary) -> bool {
    boundary.allocation == input.allocation
        && boundary.address == input.address
        && boundary.provenance == input.provenance
        && boundary.element_size == input.element_size
        && boundary.alignment == input.alignment
        && boundary.allocation_base == input.allocation_base
        && boundary.allocation_bytes == input.allocation_bytes
        && boundary.one_allocation == input.one_allocation
        && boundary.initialized == input.initialized
        && boundary.isize_max == input.isize_max
        && boundary.address_space_limit == input.address_space_limit
        && boundary.borrow == input.borrow
}

pub open spec fn slice_pointer_cast(input: Input) -> Reference {
    Reference {
        allocation: input.allocation,
        address: input.address,
        provenance: input.provenance,
        parent_borrow: input.borrow,
        start: 0,
        span: input.len,
        width: 1,
    }
}

pub open spec fn array_pointer_cast(input: Input) -> Reference {
    Reference {
        width: input.n,
        ..slice_pointer_cast(input)
    }
}

pub open spec fn from_raw_parts_array(input: Input) -> Output {
    Output {
        reference: array_pointer_cast(input),
        chunks_len: input.len / input.n,
        source: input.sequence,
        start: 0,
        width: input.n,
    }
}

pub open spec fn unchanged_state(input: Input) -> FinalState {
    FinalState {
        sequence: input.sequence,
        len: input.len,
        allocation: input.allocation,
        address: input.address,
        provenance: input.provenance,
        borrow: input.borrow,
        one_allocation: input.one_allocation,
        initialized: input.initialized,
    }
}

pub open spec fn active_contract(input: Input, output: Output) -> bool {
    output.source == input.sequence
        && output.start == 0
        && output.width == input.n
        && output.chunks_len == input.len / input.n
        && output.chunks_len * input.n == input.len
}

pub open spec fn target_definition(
    input: Input,
    boundary: Boundary,
    output: Output,
    state: FinalState,
) -> bool {
    boundary_observed(input, boundary)
        && output == from_raw_parts_array(input)
        && state == unchanged_state(input)
        && active_contract(input, output)
}

pub proof fn exact_output_and_state(
    input: Input,
    boundary: Boundary,
    output1: Output,
    state1: FinalState,
    output2: Output,
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
