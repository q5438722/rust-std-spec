#![allow(dead_code, unused_imports, unused_variables)]
// Experiment-local source model for core::slice::assume_init_mut.

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub ghost struct PointerIdentity {
    pub allocation: int,
    pub address: nat,
    pub provenance: int,
}

pub ghost struct InitializedStorage {
    pub initialized: Seq<bool>,
    pub values: Seq<int>,
}

pub ghost struct CastInput {
    pub storage: InitializedStorage,
    pub pointer: PointerIdentity,
    pub borrow: int,
    pub element_size: nat,
    pub element_alignment: nat,
    pub frame_token: int,
}

pub ghost struct Boundary {
    pub initialized: Seq<bool>,
    pub values: Seq<int>,
    pub pointer: PointerIdentity,
    pub borrow: int,
    pub element_size: nat,
    pub element_alignment: nat,
    pub frame_token: int,
}

pub ghost struct ReturnedSlice {
    pub pointer: PointerIdentity,
    pub borrow: int,
    pub values: Seq<int>,
}

pub ghost struct FinalState {
    pub storage: InitializedStorage,
    pub pointer: PointerIdentity,
    pub borrow: int,
    pub returned: ReturnedSlice,
    pub element_size: nat,
    pub element_alignment: nat,
    pub frame_token: int,
}

pub open spec fn all_initialized(storage: InitializedStorage) -> bool {
    storage.initialized.len() == storage.values.len()
        && forall|i: int| 0 <= i < storage.initialized.len() ==> storage.initialized[i]
}

pub open spec fn valid_input(input: CastInput) -> bool {
    all_initialized(input.storage)
        && input.pointer.address > 0
        && input.pointer.allocation >= 0
        && input.pointer.provenance >= 0
        && input.borrow > 0
        && input.element_alignment > 0
        && (input.element_size == 0
            || (input.element_size >= input.element_alignment
                && input.element_size % input.element_alignment == 0))
}

pub open spec fn boundary_observed(input: CastInput, boundary: Boundary) -> bool {
    boundary.initialized == input.storage.initialized
        && boundary.values == input.storage.values
        && boundary.pointer == input.pointer
        && boundary.borrow == input.borrow
        && boundary.element_size == input.element_size
        && boundary.element_alignment == input.element_alignment
        && boundary.frame_token == input.frame_token
}

pub open spec fn layout_preserving_mutable_cast(input: CastInput) -> ReturnedSlice {
    ReturnedSlice {
        pointer: input.pointer,
        borrow: input.borrow,
        values: input.storage.values,
    }
}

pub open spec fn target_definition(
    input: CastInput,
    boundary: Boundary,
    output: ReturnedSlice,
    state: FinalState,
) -> bool {
    boundary_observed(input, boundary)
        && output == layout_preserving_mutable_cast(input)
        && state.pointer == input.pointer
        && state.borrow == input.borrow
        && state.returned.pointer == input.pointer
        && state.returned.borrow == input.borrow
        && state.storage.initialized.len() == input.storage.initialized.len()
        && state.storage.values.len() == input.storage.values.len()
        && all_initialized(state.storage)
        && state.returned.values == state.storage.values
        && state.element_size == input.element_size
        && state.element_alignment == input.element_alignment
        && state.frame_token == input.frame_token
}

pub proof fn returned_slice_preserves_layout_and_identity(
    input: CastInput,
)
    requires
        valid_input(input),
    ensures
        layout_preserving_mutable_cast(input).pointer == input.pointer,
        layout_preserving_mutable_cast(input).borrow == input.borrow,
        layout_preserving_mutable_cast(input).values == input.storage.values,
{
    reveal(layout_preserving_mutable_cast);
}

pub proof fn exact_output_determinism(
    input: CastInput,
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

}
