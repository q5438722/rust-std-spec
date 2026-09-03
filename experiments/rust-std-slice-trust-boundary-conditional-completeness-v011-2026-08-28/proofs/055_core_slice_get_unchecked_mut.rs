#![allow(dead_code, unused_imports, unused_variables)]
// Trusted-free bounded source and active-contract model for get_unchecked_mut.

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub ghost struct Input {
    pub values: Seq<int>,
    pub index: int,
    pub allocation: int,
    pub address: int,
    pub provenance: int,
    pub root_borrow: int,
    pub element_size: int,
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

pub ghost struct BorrowRef {
    pub index: int,
    pub allocation: int,
    pub address: int,
    pub provenance: int,
    pub parent_borrow: int,
    pub value: int,
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

pub open spec fn valid_input(input: Input) -> bool {
    input.values.len() == 3
        && input.index == 0
        && input.allocation > 0
        && input.address > 0
        && input.provenance > 0
        && input.root_borrow > 0
        && input.element_size >= 0
}

pub open spec fn boundary_t(input: Input, boundary: Boundary) -> bool {
    boundary.values == input.values
        && boundary.allocation == input.allocation
        && boundary.address == input.address
        && boundary.provenance == input.provenance
        && boundary.root_borrow == input.root_borrow
        && boundary.element_size == input.element_size
        && boundary.frame_token > 0
}

pub open spec fn index_in_range(input: Input) -> bool {
    0 <= input.index < input.values.len()
}

pub open spec fn element_address(input: Input, index: int) -> int {
    input.address
        + if input.element_size == 0 {
            0
        } else {
            index * input.element_size
        }
}

pub open spec fn reference_at(input: Input, index: int) -> BorrowRef
    recommends
        0 <= index < input.values.len(),
{
    BorrowRef {
        index,
        allocation: input.allocation,
        address: element_address(input, index),
        provenance: input.provenance,
        parent_borrow: input.root_borrow,
        value: input.values[index],
    }
}

pub open spec fn returned_reference_well_formed(
    input: Input,
    output: BorrowRef,
) -> bool {
    0 <= output.index < input.values.len()
        && output == reference_at(input, output.index)
}

pub open spec fn mutable_frame(
    input: Input,
    boundary: Boundary,
    state: FinalState,
) -> bool {
    state.values.len() == input.values.len()
        && state.values[1] == input.values[1]
        && state.values[2] == input.values[2]
        && state.allocation == input.allocation
        && state.address == input.address
        && state.provenance == input.provenance
        && state.root_borrow == input.root_borrow
        && state.element_size == input.element_size
        && state.frame_token == boundary.frame_token
}

pub open spec fn active_contract(
    input: Input,
    boundary: Boundary,
    output: BorrowRef,
    state: FinalState,
) -> bool {
    valid_input(input)
        && boundary_t(input, boundary)
        && index_in_range(input)
        && returned_reference_well_formed(input, output)
        && mutable_frame(input, boundary, state)
}

pub open spec fn source_output(input: Input) -> BorrowRef {
    reference_at(input, input.index)
}

pub open spec fn alternative_output(input: Input) -> BorrowRef {
    reference_at(input, 1)
}

pub open spec fn unchanged_state(
    input: Input,
    boundary: Boundary,
) -> FinalState {
    FinalState {
        values: input.values,
        allocation: input.allocation,
        address: input.address,
        provenance: input.provenance,
        root_borrow: input.root_borrow,
        element_size: input.element_size,
        frame_token: boundary.frame_token,
    }
}

pub proof fn usize_source_transition_satisfies_active_contract(
    input: Input,
    boundary: Boundary,
)
    requires
        valid_input(input),
        boundary_t(input, boundary),
    ensures
        active_contract(
            input,
            boundary,
            source_output(input),
            unchanged_state(input, boundary),
        ),
{
    reveal(valid_input);
    reveal(boundary_t);
    reveal(index_in_range);
    reveal(source_output);
    reveal(returned_reference_well_formed);
    reveal(reference_at);
    reveal(element_address);
    reveal(unchanged_state);
    reveal(mutable_frame);
    reveal(active_contract);
}

pub proof fn active_contract_admits_distinct_usize_references(
    input: Input,
    boundary: Boundary,
)
    requires
        valid_input(input),
        boundary_t(input, boundary),
    ensures
        active_contract(
            input,
            boundary,
            source_output(input),
            unchanged_state(input, boundary),
        ),
        active_contract(
            input,
            boundary,
            alternative_output(input),
            unchanged_state(input, boundary),
        ),
        source_output(input) != alternative_output(input),
{
    reveal(valid_input);
    reveal(boundary_t);
    reveal(index_in_range);
    reveal(source_output);
    reveal(alternative_output);
    reveal(returned_reference_well_formed);
    reveal(reference_at);
    reveal(element_address);
    reveal(unchanged_state);
    reveal(mutable_frame);
    reveal(active_contract);
}

}
