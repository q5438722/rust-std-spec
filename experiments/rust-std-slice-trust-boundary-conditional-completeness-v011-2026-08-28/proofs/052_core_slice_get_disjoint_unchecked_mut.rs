#![allow(dead_code, unused_imports, unused_variables)]
// Experiment-local source and contract model for
// core::slice::get_disjoint_unchecked_mut.

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

pub ghost struct MaybeUninitBorrowArray {
    pub slot0_initialized: bool,
    pub slot0: BorrowRef,
    pub slot1_initialized: bool,
    pub slot1: BorrowRef,
}

pub ghost struct FinalState {
    pub values: Seq<int>,
}

pub open spec fn valid_input(input: SliceInput) -> bool {
    input.values.len() == 3
        && input.index0 == 0
        && input.index1 == 2
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

pub open spec fn indices_valid(input: SliceInput) -> bool {
    index_in_bounds(input, input.index0)
        && index_in_bounds(input, input.index1)
        && input.index0 != input.index1
}

pub open spec fn clone_usize(index: nat) -> nat {
    index
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

pub open spec fn uninitialized_storage() -> MaybeUninitBorrowArray {
    let placeholder = BorrowRef {
        index: 0,
        allocation: 0,
        address: 0,
        provenance: 0,
        parent_borrow: 0,
        value: 0,
    };
    MaybeUninitBorrowArray {
        slot0_initialized: false,
        slot0: placeholder,
        slot1_initialized: false,
        slot1: placeholder,
    }
}

pub open spec fn write_slot0(
    storage: MaybeUninitBorrowArray,
    value: BorrowRef,
) -> MaybeUninitBorrowArray {
    MaybeUninitBorrowArray {
        slot0_initialized: true,
        slot0: value,
        slot1_initialized: storage.slot1_initialized,
        slot1: storage.slot1,
    }
}

pub open spec fn write_slot1(
    storage: MaybeUninitBorrowArray,
    value: BorrowRef,
) -> MaybeUninitBorrowArray {
    MaybeUninitBorrowArray {
        slot0_initialized: storage.slot0_initialized,
        slot0: storage.slot0,
        slot1_initialized: true,
        slot1: value,
    }
}

pub open spec fn source_after_first_write(
    input: SliceInput,
) -> MaybeUninitBorrowArray {
    write_slot0(
        uninitialized_storage(),
        borrow_at(input, clone_usize(input.index0)),
    )
}

pub open spec fn source_after_second_write(
    input: SliceInput,
) -> MaybeUninitBorrowArray {
    write_slot1(
        source_after_first_write(input),
        borrow_at(input, clone_usize(input.index1)),
    )
}

pub open spec fn completely_initialized(
    storage: MaybeUninitBorrowArray,
) -> bool {
    storage.slot0_initialized && storage.slot1_initialized
}

pub open spec fn assume_init(
    storage: MaybeUninitBorrowArray,
) -> BorrowArray
    recommends
        completely_initialized(storage),
{
    BorrowArray {
        first: storage.slot0,
        second: storage.slot1,
    }
}

pub open spec fn active_contract(
    input: SliceInput,
    output: BorrowArray,
    state: FinalState,
) -> bool {
    indices_valid(input)
        && borrow_array_well_formed(input, output)
        && state.values.len() == input.values.len()
}

pub proof fn usize_clone_is_identity(input: SliceInput)
    ensures
        clone_usize(input.index0) == input.index0,
        clone_usize(input.index1) == input.index1,
{
    reveal(clone_usize);
}

pub proof fn two_slot_loop_initializes_without_prior_mutation(input: SliceInput)
    requires
        valid_input(input),
    ensures
        !uninitialized_storage().slot0_initialized,
        !uninitialized_storage().slot1_initialized,
        source_after_first_write(input).slot0_initialized,
        !source_after_first_write(input).slot1_initialized,
        source_after_second_write(input).slot0_initialized,
        source_after_second_write(input).slot1_initialized,
        source_after_second_write(input).slot0
            == source_after_first_write(input).slot0,
        completely_initialized(source_after_second_write(input)),
        !completely_initialized(source_after_first_write(input)),
{
    reveal(valid_input);
    reveal(source_after_second_write);
    reveal(source_after_first_write);
    reveal(write_slot1);
    reveal(write_slot0);
    reveal(uninitialized_storage);
    reveal(completely_initialized);
}

pub proof fn assume_init_returns_canonical_array(input: SliceInput)
    requires
        valid_input(input),
    ensures
        indices_valid(input),
        completely_initialized(source_after_second_write(input)),
        assume_init(source_after_second_write(input)).first
            == borrow_at(input, input.index0),
        assume_init(source_after_second_write(input)).second
            == borrow_at(input, input.index1),
        borrow_array_well_formed(
            input,
            assume_init(source_after_second_write(input)),
        ),
{
    usize_clone_is_identity(input);
    two_slot_loop_initializes_without_prior_mutation(input);
    reveal(valid_input);
    reveal(indices_valid);
    reveal(index_in_bounds);
    reveal(clone_usize);
    reveal(source_after_second_write);
    reveal(source_after_first_write);
    reveal(write_slot1);
    reveal(write_slot0);
    reveal(uninitialized_storage);
    reveal(assume_init);
    reveal(borrow_array_well_formed);
    reveal(borrow_well_formed);
    reveal(borrow_at);
}

pub proof fn active_contract_admits_distinct_well_formed_arrays(
    input: SliceInput,
    state: FinalState,
)
    requires
        valid_input(input),
        state.values == input.values,
    ensures
        active_contract(
            input,
            BorrowArray {
                first: borrow_at(input, 0),
                second: borrow_at(input, 2),
            },
            state,
        ),
        active_contract(
            input,
            BorrowArray {
                first: borrow_at(input, 1),
                second: borrow_at(input, 2),
            },
            state,
        ),
        (BorrowArray {
            first: borrow_at(input, 0),
            second: borrow_at(input, 2),
        }) != (BorrowArray {
            first: borrow_at(input, 1),
            second: borrow_at(input, 2),
        }),
{
    reveal(valid_input);
    reveal(indices_valid);
    reveal(index_in_bounds);
    reveal(active_contract);
    reveal(borrow_array_well_formed);
    reveal(borrow_well_formed);
    reveal(borrow_at);
}

}
