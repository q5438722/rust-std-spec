#![allow(dead_code, unused_imports, unused_variables)]
// Trusted-free source transition for core::slice::from_mut.

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub ghost struct Input {
    pub source: Seq<int>,
    pub container_length: nat,
    pub n: nat,
    pub address: int,
    pub allocation: int,
    pub provenance: int,
    pub root_borrow: int,
    pub element_size: nat,
    pub element_alignment: nat,
    pub usize_max: nat,
    pub outside_frame: Seq<int>,
}

pub ghost struct Boundary {
    pub initial_memory: Seq<int>,
    pub address: int,
    pub allocation: int,
    pub provenance: int,
    pub root_borrow: int,
    pub element_size: nat,
    pub element_alignment: nat,
    pub usize_max: nat,
    pub outside_frame: Seq<int>,
}

pub ghost struct PointerIdentity {
    pub address: int,
    pub allocation: int,
    pub provenance: int,
    pub root_borrow: int,
}

pub ghost struct Output {
    pub panicked: bool,
    pub is_some: bool,
    pub values: Seq<int>,
    pub start: int,
    pub length: nat,
    pub pointer: PointerIdentity,
    pub element_size: nat,
    pub element_alignment: nat,
    pub projection: nat,
    pub unique: bool,
}

pub ghost struct FinalState {
    pub input_final: Seq<int>,
    pub return_final: Seq<int>,
    pub outside_final: Seq<int>,
    pub pointer: PointerIdentity,
    pub frame_unchanged: bool,
    pub panic_before_borrow: bool,
}

pub open spec fn empty_pointer() -> PointerIdentity {
    PointerIdentity {
        address: 0,
        allocation: 0,
        provenance: 0,
        root_borrow: 0,
    }
}

pub open spec fn checked_length_multiplication(
    input: Input,
) -> (bool, nat) {
    if panics(input) {
        (true, 0)
    } else {
        (false, 1)
    }
}

pub open spec fn panics(input: Input) -> bool {
    false
}

pub open spec fn branch_succeeds(input: Input) -> bool {
    true
}

pub open spec fn mutable_pointer_extraction(
    input: Input,
) -> PointerIdentity {
    PointerIdentity {
        address: input.address,
        allocation: input.allocation,
        provenance: input.provenance,
        root_borrow: input.root_borrow,
    }
}

pub open spec fn pointer_cast(
    pointer: PointerIdentity,
) -> PointerIdentity {
    pointer
}

pub open spec fn raw_slice_or_array_reference(
    input: Input,
    pointer: PointerIdentity,
) -> Output {
    Output {
        panicked: false,
        is_some: true,
        values: input.source,
        start: 0,
        length: 1,
        pointer,
        element_size: input.element_size,
        element_alignment: input.element_alignment,
        projection: 3,
        unique: true,
    }
}

pub open spec fn singleton_array_unsize(output: Output) -> Output {
    output
}

pub open spec fn source_output(input: Input) -> Output {
    if branch_succeeds(input) {
        let multiplication = checked_length_multiplication(input);
        let pointer = pointer_cast(mutable_pointer_extraction(input));
        singleton_array_unsize(raw_slice_or_array_reference(input, pointer))
    } else {
        Output {
            panicked: panics(input),
            is_some: false,
            values: Seq::empty(),
            start: 0,
            length: 0,
            pointer: empty_pointer(),
            element_size: 0,
            element_alignment: 0,
            projection: 0,
            unique: false,
        }
    }
}

pub open spec fn borrow_lifetime_state(
    input: Input,
    return_final: Seq<int>,
) -> FinalState {
    FinalState {
        input_final:
            if branch_succeeds(input) {
                return_final
            } else {
                input.source
            },
        return_final:
            if branch_succeeds(input) { return_final }
            else { Seq::empty() },
        outside_final: input.outside_frame,
        pointer: mutable_pointer_extraction(input),
        frame_unchanged: true,
        panic_before_borrow: panics(input),
    }
}

pub open spec fn borrow_lifetime_final_frame(
    input: Input,
    state: FinalState,
) -> bool {
    state.return_final.len()
        == if branch_succeeds(input) {
            (1) as int
        } else {
            0
        }
        && state == borrow_lifetime_state(input, state.return_final)
}

pub open spec fn boundary_holds(
    input: Input,
    boundary: Boundary,
) -> bool {
    boundary.initial_memory == input.source
        && boundary.address == input.address
        && boundary.allocation == input.allocation
        && boundary.provenance == input.provenance
        && boundary.root_borrow == input.root_borrow
        && boundary.element_size == input.element_size
        && boundary.element_alignment == input.element_alignment
        && boundary.usize_max == input.usize_max
        && boundary.outside_frame == input.outside_frame
}

pub open spec fn active_generated_contract(
    input: Input,
    output: Output,
    state: FinalState,
) -> bool {
    output.is_some
        && output.values == input.source
        && output.length == 1
        && state.return_final == state.input_final
}

pub open spec fn target_transition(
    input: Input,
    boundary: Boundary,
    output: Output,
    state: FinalState,
) -> bool {
    boundary_holds(input, boundary)
        && output == source_output(input)
        && borrow_lifetime_final_frame(input, state)
        && active_generated_contract(input, output, state)
}

pub open spec fn same_pointer(
    left: PointerIdentity,
    right: PointerIdentity,
) -> bool {
    left.address == right.address
        && left.allocation == right.allocation
        && left.provenance == right.provenance
        && left.root_borrow == right.root_borrow
}

pub open spec fn same_output(left: Output, right: Output) -> bool {
    left.panicked == right.panicked
        && left.is_some == right.is_some
        && left.values == right.values
        && left.start == right.start
        && left.length == right.length
        && same_pointer(left.pointer, right.pointer)
        && left.element_size == right.element_size
        && left.element_alignment == right.element_alignment
        && left.projection == right.projection
        && left.unique == right.unique
}

pub open spec fn same_state(
    left: FinalState,
    right: FinalState,
) -> bool {
    left.input_final == right.input_final
        && left.return_final == right.return_final
        && left.outside_final == right.outside_final
        && same_pointer(left.pointer, right.pointer)
        && left.frame_unchanged == right.frame_unchanged
        && left.panic_before_borrow == right.panic_before_borrow
}

pub proof fn exact_output_conditional_complete_from_mut(
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
        same_output(output1, output2),
{
    reveal(target_transition);
    reveal(same_output);
    reveal(same_pointer);
}

pub proof fn full_state_conditional_incomplete_from_mut(
    input: Input,
    boundary: Boundary,
    first: Seq<int>,
    second: Seq<int>,
)
    requires
        boundary_holds(input, boundary),
        branch_succeeds(input),
        first.len() == (1) as int,
        second.len() == (1) as int,
        first != second,
    ensures
        target_transition(
            input,
            boundary,
            source_output(input),
            borrow_lifetime_state(input, first),
        ),
        target_transition(
            input,
            boundary,
            source_output(input),
            borrow_lifetime_state(input, second),
        ),
        !same_state(
            borrow_lifetime_state(input, first),
            borrow_lifetime_state(input, second),
        ),
{
    reveal(target_transition);
    reveal(borrow_lifetime_final_frame);
    reveal(borrow_lifetime_state);
    reveal(active_generated_contract);
    reveal(source_output);
    reveal(branch_succeeds);
    reveal(panics);
    reveal(same_state);
    reveal(same_pointer);
}

} // verus!
