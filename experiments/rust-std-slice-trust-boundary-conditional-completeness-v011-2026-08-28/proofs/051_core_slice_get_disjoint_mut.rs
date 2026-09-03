#![allow(dead_code, unused_imports, unused_variables)]
// Experiment-local source and contract model for core::slice::get_disjoint_mut.

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub ghost struct SliceInput {
    pub values: Seq<int>,
    pub index0: nat,
    pub index1: nat,
    pub allocation: int,
    pub address: nat,
    pub provenance: int,
    pub parent_borrow: int,
    pub element_size: nat,
}

pub ghost struct Boundary {
    pub values: Seq<int>,
    pub allocation: int,
    pub address: nat,
    pub provenance: int,
    pub parent_borrow: int,
    pub element_size: nat,
}

pub ghost struct BorrowRef {
    pub index: nat,
    pub allocation: int,
    pub address: nat,
    pub provenance: int,
    pub parent_borrow: int,
    pub value: int,
}

pub ghost struct BorrowArray {
    pub first: BorrowRef,
    pub second: BorrowRef,
}

pub ghost struct FinalState {
    pub values: Seq<int>,
}

pub open spec fn valid_input(input: SliceInput) -> bool {
    input.values.len() == 3
        && input.allocation > 0
        && input.address > 0
        && input.provenance > 0
        && input.parent_borrow > 0
        && input.element_size > 0
}

pub open spec fn boundary_observed(input: SliceInput, boundary: Boundary) -> bool {
    boundary.values == input.values
        && boundary.allocation == input.allocation
        && boundary.address == input.address
        && boundary.provenance == input.provenance
        && boundary.parent_borrow == input.parent_borrow
        && boundary.element_size == input.element_size
}

pub open spec fn index_in_bounds(input: SliceInput, index: nat) -> bool {
    index < input.values.len()
}

pub open spec fn indices_overlap(input: SliceInput) -> bool {
    input.index0 == input.index1
}

// 0 is Ok, 1 is IndexOutOfBounds, and 2 is OverlappingIndices.
pub open spec fn validation_loop_error(input: SliceInput) -> int {
    if !index_in_bounds(input, input.index0) {
        1
    } else if !index_in_bounds(input, input.index1) {
        1
    } else if indices_overlap(input) {
        2
    } else {
        0
    }
}

pub open spec fn validation_loop_valid(input: SliceInput) -> bool {
    validation_loop_error(input) == 0
}

pub open spec fn borrow_at(input: SliceInput, index: nat) -> BorrowRef
    recommends
        index_in_bounds(input, index),
{
    BorrowRef {
        index,
        allocation: input.allocation,
        address: input.address + index * input.element_size,
        provenance: input.provenance,
        parent_borrow: input.parent_borrow,
        value: input.values[index as int],
    }
}

pub open spec fn borrow_well_formed(
    input: SliceInput,
    borrow: BorrowRef,
) -> bool {
    index_in_bounds(input, borrow.index)
        && borrow == borrow_at(input, borrow.index)
}

pub open spec fn borrow_array_well_formed(
    input: SliceInput,
    borrows: BorrowArray,
) -> bool {
    borrow_well_formed(input, borrows.first)
        && borrow_well_formed(input, borrows.second)
        && borrows.first.index != borrows.second.index
}

pub open spec fn canonical_after_first_write(input: SliceInput) -> BorrowArray
    recommends
        index_in_bounds(input, input.index0),
        index_in_bounds(input, input.index1),
{
    BorrowArray {
        first: borrow_at(input, input.index0),
        second: borrow_at(input, input.index1),
    }
}

pub open spec fn canonical_after_second_write(input: SliceInput) -> BorrowArray
    recommends
        validation_loop_valid(input),
{
    let prior = canonical_after_first_write(input);
    BorrowArray {
        first: prior.first,
        second: borrow_at(input, input.index1),
    }
}

pub open spec fn ok_contract(
    input: SliceInput,
    borrows: BorrowArray,
    state: FinalState,
) -> bool {
    validation_loop_valid(input)
        && borrow_array_well_formed(input, borrows)
        && state.values.len() == input.values.len()
}

pub open spec fn err_contract(
    input: SliceInput,
    error_kind: int,
    state: FinalState,
) -> bool {
    !validation_loop_valid(input)
        && (error_kind == 1 || error_kind == 2)
        && state.values == input.values
}

pub proof fn validation_loop_selects_out_of_bounds(
    input: SliceInput,
)
    requires
        index_in_bounds(input, input.index0),
        !index_in_bounds(input, input.index1),
    ensures
        validation_loop_error(input) == 1,
        !validation_loop_valid(input),
{
    reveal(validation_loop_error);
    reveal(validation_loop_valid);
}

pub proof fn validation_loop_selects_overlap(
    input: SliceInput,
)
    requires
        index_in_bounds(input, input.index0),
        index_in_bounds(input, input.index1),
        indices_overlap(input),
    ensures
        validation_loop_error(input) == 2,
        !validation_loop_valid(input),
{
    reveal(validation_loop_error);
    reveal(validation_loop_valid);
}

pub proof fn canonical_construction_is_disjoint_and_preserves_first(
    input: SliceInput,
)
    requires
        validation_loop_valid(input),
    ensures
        borrow_array_well_formed(input, canonical_after_second_write(input)),
        canonical_after_second_write(input).first
            == canonical_after_first_write(input).first,
        canonical_after_second_write(input).first.index == input.index0,
        canonical_after_second_write(input).second.index == input.index1,
{
    reveal(validation_loop_valid);
    reveal(validation_loop_error);
    reveal(indices_overlap);
    reveal(canonical_after_second_write);
    reveal(canonical_after_first_write);
    reveal(borrow_array_well_formed);
    reveal(borrow_well_formed);
    reveal(borrow_at);
}

pub proof fn out_of_bounds_contract_admits_both_error_variants(
    input: SliceInput,
    state: FinalState,
)
    requires
        index_in_bounds(input, input.index0),
        !index_in_bounds(input, input.index1),
        state.values == input.values,
    ensures
        err_contract(input, 1, state),
        err_contract(input, 2, state),
        1 != 2,
{
    validation_loop_selects_out_of_bounds(input);
    reveal(err_contract);
}

pub proof fn valid_contract_admits_distinct_well_formed_borrows(
    input: SliceInput,
    state: FinalState,
)
    requires
        valid_input(input),
        input.index0 == 0,
        input.index1 == 2,
        state.values == input.values,
    ensures
        ok_contract(
            input,
            BorrowArray {
                first: borrow_at(input, 0),
                second: borrow_at(input, 2),
            },
            state,
        ),
        ok_contract(
            input,
            BorrowArray {
                first: borrow_at(input, 1),
                second: borrow_at(input, 2),
            },
            state,
        ),
        borrow_at(input, 0).index != borrow_at(input, 1).index,
{
    reveal(valid_input);
    reveal(index_in_bounds);
    reveal(indices_overlap);
    reveal(validation_loop_error);
    reveal(validation_loop_valid);
    reveal(ok_contract);
    reveal(borrow_array_well_formed);
    reveal(borrow_well_formed);
    reveal(borrow_at);
}

}
