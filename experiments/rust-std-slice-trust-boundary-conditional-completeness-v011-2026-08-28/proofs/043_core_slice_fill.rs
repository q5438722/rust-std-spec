#![allow(dead_code, unused_imports, unused_variables)]
// Trusted-free source-transition model for core::slice::fill.

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub ghost enum TypeKind {
    GenericClone,
    TrivialClone,
    U8,
    I8,
    Integer,
}

pub ghost struct Input {
    pub destination: Seq<int>,
    pub value: int,
    pub kind: TypeKind,
    pub miri: bool,
    pub value_has_uniform_bytes: bool,
    pub clone_initial_state: int,
}

pub ghost struct Boundary {
    pub clone_argument: Seq<int>,
    pub clone_result: Seq<int>,
    pub clone_state_before: Seq<int>,
    pub clone_state_after: Seq<int>,
    pub clone_completed: Seq<bool>,
    pub clone_panicked: Seq<bool>,
    pub clone_panic_value: Seq<int>,
    pub static_known: bool,
}

pub ghost struct Output {
    pub final_values: Seq<int>,
}

pub ghost struct FinalState {
    pub destination: Seq<int>,
    pub clone_state: int,
    pub clone_call_count: nat,
    pub write_count: nat,
    pub intrinsic_call_count: nat,
    pub assignment_count: nat,
    pub selected_path: int,
    pub final_slot_moved: bool,
}

pub open spec fn callback_count(input: Input) -> nat {
    match input.kind {
        TypeKind::GenericClone =>
            if input.destination.len() == 0 {
                0nat
            } else {
                (input.destination.len() - 1) as nat
            },
        _ => 0nat,
    }
}

pub open spec fn selected_path(input: Input, boundary: Boundary) -> int {
    match input.kind {
        TypeKind::GenericClone => 20int,
        TypeKind::TrivialClone => 21int,
        TypeKind::U8 => 22int,
        TypeKind::I8 => 23int,
        TypeKind::Integer =>
            if ((input.miri && input.destination.len() > 32nat)
                    || boundary.static_known)
                && input.value_has_uniform_bytes
            {
                24int
            } else {
                25int
            },
    }
}

pub open spec fn intrinsic_call_count(
    input: Input,
    boundary: Boundary,
) -> nat {
    match input.kind {
        TypeKind::U8 | TypeKind::I8 => 1nat,
        TypeKind::Integer =>
            (if input.miri && input.destination.len() > 32nat {
                0nat
            } else {
                1nat
            })
            + (if selected_path(input, boundary)
                    == 24int {
                1nat
            } else {
                0nat
            }),
        _ => 0nat,
    }
}

pub open spec fn assignment_count(
    input: Input,
    boundary: Boundary,
) -> nat {
    match input.kind {
        TypeKind::GenericClone =>
            if input.destination.len() == 0 { 0nat } else { 1nat },
        TypeKind::TrivialClone => input.destination.len(),
        TypeKind::Integer =>
            if selected_path(input, boundary) == 25int {
                input.destination.len()
            } else {
                0nat
            },
        _ => 0nat,
    }
}

pub open spec fn index_uses_clone(input: Input, index: int) -> bool {
    matches!(input.kind, TypeKind::GenericClone)
        && 0 <= index < callback_count(input)
}

pub open spec fn cloned_relation_at(
    input: Input,
    boundary: Boundary,
    index: int,
    source: int,
    result: int,
) -> bool {
    if index_uses_clone(input, index) {
        boundary.clone_argument[index] == source
            && boundary.clone_result[index] == result
    } else {
        result == source
    }
}

pub open spec fn source_result_at(
    input: Input,
    boundary: Boundary,
    index: int,
) -> int {
    if index_uses_clone(input, index) {
        boundary.clone_result[index]
    } else {
        input.value
    }
}

pub open spec fn source_values(
    input: Input,
    boundary: Boundary,
) -> Seq<int> {
    Seq::new(input.destination.len(), |index: int|
        source_result_at(input, boundary, index))
}

pub open spec fn callback_chain(input: Input, boundary: Boundary) -> bool {
    boundary.clone_argument.len() >= callback_count(input)
        && boundary.clone_result.len() >= callback_count(input)
        && boundary.clone_state_before.len() >= callback_count(input)
        && boundary.clone_state_after.len() >= callback_count(input)
        && boundary.clone_completed.len() >= callback_count(input)
        && boundary.clone_panicked.len() >= callback_count(input)
        && forall|index: int| #![auto] 0 <= index < callback_count(input) ==>
            boundary.clone_argument[index] == input.value
            && boundary.clone_completed[index]
            && !boundary.clone_panicked[index]
            && boundary.clone_state_before[index]
                == if index == 0 {
                    input.clone_initial_state
                } else {
                    boundary.clone_state_after[index - 1]
                }
}

pub open spec fn active_slice_filled_with_clone(
    input: Input,
    boundary: Boundary,
    output: Output,
) -> bool {
    output.final_values.len() == input.destination.len()
        && forall|index: int| #![auto] 0 <= index < input.destination.len() ==>
            cloned_relation_at(
                input,
                boundary,
                index,
                input.value,
                output.final_values[index],
            )
}

pub open spec fn source_transition(
    input: Input,
    boundary: Boundary,
    output: Output,
    state: FinalState,
) -> bool {
    callback_chain(input, boundary)
        && output.final_values == source_values(input, boundary)
        && state.destination == source_values(input, boundary)
        && state.clone_state
            == if callback_count(input) == 0 {
                input.clone_initial_state
            } else {
                boundary.clone_state_after[callback_count(input) - 1]
            }
        && state.clone_call_count == callback_count(input)
        && state.write_count == input.destination.len()
        && state.intrinsic_call_count
            == intrinsic_call_count(input, boundary)
        && state.assignment_count == assignment_count(input, boundary)
        && state.selected_path == selected_path(input, boundary)
        && state.final_slot_moved
            == (matches!(input.kind, TypeKind::GenericClone)
                && input.destination.len() > 0)
}

pub open spec fn panic_prefix(
    input: Input,
    boundary: Boundary,
    panic_index: int,
) -> bool {
    matches!(input.kind, TypeKind::GenericClone)
        && 0 <= panic_index < callback_count(input)
        && boundary.clone_panicked.len() > panic_index
        && boundary.clone_panic_value.len() > panic_index
        && boundary.clone_panicked[panic_index]
        && forall|index: int| #![auto] 0 <= index < panic_index ==>
            boundary.clone_completed[index]
            && !boundary.clone_panicked[index]
            &&
            cloned_relation_at(
                input,
                boundary,
                index,
                input.value,
                boundary.clone_result[index],
            )
}

pub open spec fn target_transition(
    input: Input,
    boundary: Boundary,
    output: Output,
    state: FinalState,
) -> bool {
    source_transition(input, boundary, output, state)
        && active_slice_filled_with_clone(input, boundary, output)
}

pub open spec fn exact_equivalent(
    left: Output,
    left_state: FinalState,
    right: Output,
    right_state: FinalState,
) -> bool {
    left.final_values == right.final_values
        && left_state.destination == right_state.destination
        && left_state.clone_state == right_state.clone_state
        && left_state.clone_call_count == right_state.clone_call_count
        && left_state.write_count == right_state.write_count
        && left_state.intrinsic_call_count == right_state.intrinsic_call_count
        && left_state.assignment_count == right_state.assignment_count
        && left_state.selected_path == right_state.selected_path
        && left_state.final_slot_moved == right_state.final_slot_moved
}

pub proof fn conditional_complete_fill(
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
        exact_equivalent(output1, state1, output2, state2),
{
    reveal(target_transition);
    reveal(source_transition);
    reveal(exact_equivalent);
}

} // verus!
