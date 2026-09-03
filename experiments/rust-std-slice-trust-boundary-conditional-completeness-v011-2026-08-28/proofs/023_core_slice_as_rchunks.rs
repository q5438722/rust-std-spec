#![allow(dead_code, unused_imports, unused_variables)]
// Source-transition model for core::slice::as_rchunks.

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
    pub one_allocation: bool,
    pub initialized: bool,
    pub borrow: int,
}

pub ghost struct Boundary {
    pub allocation: int,
    pub address: nat,
    pub provenance: int,
    pub element_size: nat,
    pub alignment: nat,
    pub one_allocation: bool,
    pub initialized: bool,
    pub borrow: int,
}

pub ghost struct Range {
    pub allocation: int,
    pub address: nat,
    pub provenance: int,
    pub parent_borrow: int,
    pub start: nat,
    pub span: nat,
    pub width: nat,
}

pub ghost struct Output {
    pub chunks: Range,
    pub chunks_len: nat,
    pub chunks_source: int,
    pub chunks_start: nat,
    pub chunks_width: nat,
    pub remainder: Range,
    pub remainder_len: nat,
    pub remainder_source: int,
    pub remainder_start: nat,
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

pub open spec fn valid_input(input: Input) -> bool {
    input.n > 0
        && input.address > 0
        && input.alignment > 0
        && input.address % input.alignment == 0
        && input.one_allocation
        && input.initialized
        && input.borrow > 0
}

pub open spec fn boundary_observed(input: Input, boundary: Boundary) -> bool {
    boundary.allocation == input.allocation
        && boundary.address == input.address
        && boundary.provenance == input.provenance
        && boundary.element_size == input.element_size
        && boundary.alignment == input.alignment
        && boundary.one_allocation == input.one_allocation
        && boundary.initialized == input.initialized
        && boundary.borrow == input.borrow
}

pub open spec fn chunk_count(input: Input) -> nat {
    input.len / input.n
}

pub open spec fn remainder_length(input: Input) -> nat {
    input.len % input.n
}

pub open spec fn split_front(input: Input) -> Range {
    Range {
        allocation: input.allocation,
        address: input.address,
        provenance: input.provenance,
        parent_borrow: input.borrow,
        start: 0,
        span: remainder_length(input),
        width: 1,
    }
}

pub open spec fn split_rear(input: Input) -> Range {
    Range {
        allocation: input.allocation,
        address: input.address + remainder_length(input) * input.element_size,
        provenance: input.provenance,
        parent_borrow: input.borrow,
        start: remainder_length(input),
        span: chunk_count(input) * input.n,
        width: 1,
    }
}

pub open spec fn lower_as_chunks_unchecked(input: Input) -> Range {
    Range {
        width: input.n,
        ..split_rear(input)
    }
}

pub open spec fn source_output(input: Input) -> Output {
    Output {
        chunks: lower_as_chunks_unchecked(input),
        chunks_len: chunk_count(input),
        chunks_source: input.sequence,
        chunks_start: remainder_length(input),
        chunks_width: input.n,
        remainder: split_front(input),
        remainder_len: remainder_length(input),
        remainder_source: input.sequence,
        remainder_start: 0,
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
    output.chunks_len == input.len / input.n
        && output.remainder_len == input.len % input.n
        && output.chunks_len * input.n + output.remainder_len == input.len
        && output.remainder_len < input.n
        && output.remainder_source == input.sequence
        && output.remainder_start == 0
        && output.chunks_source == input.sequence
        && output.chunks_start == output.remainder_len
        && output.chunks_width == input.n
}

pub open spec fn target_definition(
    input: Input,
    boundary: Boundary,
    output: Output,
    state: FinalState,
) -> bool {
    boundary_observed(input, boundary)
        && output == source_output(input)
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
