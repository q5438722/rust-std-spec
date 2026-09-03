#![allow(dead_code, unused_imports, unused_variables)]
// Target-local length-four small-sort obligation for select_nth_unstable_by.

use vstd::prelude::*;

verus! {

pub ghost struct Quad {
    pub e0: int,
    pub e1: int,
    pub e2: int,
    pub e3: int,
}

pub ghost struct Input {
    pub initial: Quad,
    pub index: int,
    pub allocation: int,
    pub borrow: int,
}

pub ghost struct CompareBoundary {
    pub initial_state: int,
    pub ordering: int,
    pub next_delta: int,
    pub panicked: bool,
}

pub ghost struct Output {
    pub left_start: int,
    pub left_len: int,
    pub pivot_start: int,
    pub pivot_identity: int,
    pub right_start: int,
    pub right_len: int,
}

pub ghost struct State {
    pub final_sequence: Quad,
    pub allocation: int,
    pub borrow: int,
    pub callback_state: int,
    pub panicked: bool,
}

pub open spec fn requires_t(input: Input) -> bool {
    input.index == 1
        && input.allocation >= 0
        && input.borrow >= 0
        && input.initial.e0 == input.initial.e1
        && input.initial.e1 == input.initial.e2
        && input.initial.e2 == input.initial.e3
}

pub open spec fn boundary_t(
    input: Input,
    boundary: CompareBoundary,
) -> bool {
    boundary.initial_state >= 0
        && boundary.ordering == 0
        && boundary.next_delta > 0
        && !boundary.panicked
}

pub open spec fn compare_step(
    boundary: CompareBoundary,
    state: int,
    left: int,
    right: int,
    ordering: int,
    next_state: int,
    panicked: bool,
) -> bool {
    ordering == boundary.ordering
        && next_state == state + boundary.next_delta
        && panicked == boundary.panicked
}

pub open spec fn callback_adapter_transition(
    boundary: CompareBoundary,
    state: int,
    left: int,
    right: int,
    is_less: bool,
    next_state: int,
) -> bool {
    compare_step(
        boundary,
        state,
        left,
        right,
        boundary.ordering,
        next_state,
        false,
    ) && is_less == (boundary.ordering == -1)
}

pub open spec fn small_sort_mutable_slice_transition(
    input: Input,
    boundary: CompareBoundary,
    state: State,
) -> bool {
    callback_adapter_transition(
        boundary,
        boundary.initial_state,
        input.initial.e1,
        input.initial.e0,
        false,
        boundary.initial_state + boundary.next_delta,
    ) && callback_adapter_transition(
        boundary,
        boundary.initial_state + boundary.next_delta,
        input.initial.e2,
        input.initial.e1,
        false,
        boundary.initial_state + 2 * boundary.next_delta,
    ) && callback_adapter_transition(
        boundary,
        boundary.initial_state + 2 * boundary.next_delta,
        input.initial.e3,
        input.initial.e2,
        false,
        state.callback_state,
    ) && state.final_sequence == input.initial
        && state.allocation == input.allocation
        && state.borrow == input.borrow
        && !state.panicked
}

pub open spec fn partition_transition(
    input: Input,
    boundary: CompareBoundary,
    state: State,
) -> bool {
    boundary.ordering == 0
        && state.final_sequence.e0 == state.final_sequence.e1
        && state.final_sequence.e1 == state.final_sequence.e2
        && state.final_sequence.e2 == state.final_sequence.e3
}

pub open spec fn small_sort_threshold_transition(input: Input) -> bool {
    input.index == 1 && 4 <= 16
}

pub open spec fn bounded_model_scope_transition(input: Input) -> bool {
    input.index == 1
}

pub open spec fn panic_prefix_transition(state: State) -> bool {
    !state.panicked
}

pub open spec fn final_subslice_transition(
    input: Input,
    output: Output,
    state: State,
) -> bool {
    output.left_start == 0
        && output.left_len == input.index
        && output.pivot_start == input.index
        && output.pivot_identity == state.final_sequence.e1
        && output.right_start == input.index + 1
        && output.right_len == 4 - input.index - 1
}

pub open spec fn active_final_concat_conjunct(
    input: Input,
    output: Output,
    state: State,
) -> bool {
    output.left_start == 0
        && output.pivot_start == output.left_len
        && output.right_start == output.pivot_start + 1
        && output.left_len + 1 + output.right_len == 4
        && state.allocation == input.allocation
        && state.borrow == input.borrow
}

pub open spec fn active_left_length_conjunct(
    input: Input,
    output: Output,
) -> bool {
    output.left_len == input.index
}

pub open spec fn active_pivot_at_index_conjunct(
    output: Output,
    state: State,
) -> bool {
    output.pivot_start == 1
        && output.pivot_identity == state.final_sequence.e1
}

pub open spec fn active_right_length_conjunct(
    input: Input,
    output: Output,
) -> bool {
    output.right_len == 4 - input.index - 1
}

pub open spec fn active_permutation_conjunct(
    input: Input,
    state: State,
) -> bool {
    state.final_sequence == input.initial
}

pub open spec fn active_callback_partition_conjunct(
    boundary: CompareBoundary,
    state: State,
) -> bool {
    partition_transition(
        Input {
            initial: state.final_sequence,
            index: 1,
            allocation: state.allocation,
            borrow: state.borrow,
        },
        boundary,
        state,
    )
}

pub open spec fn target_definition_t(
    input: Input,
    boundary: CompareBoundary,
    output: Output,
    state: State,
) -> bool {
    small_sort_mutable_slice_transition(input, boundary, state)
        && partition_transition(input, boundary, state)
        && small_sort_threshold_transition(input)
        && bounded_model_scope_transition(input)
        && panic_prefix_transition(state)
        && final_subslice_transition(input, output, state)
        && active_final_concat_conjunct(input, output, state)
        && active_left_length_conjunct(input, output)
        && active_pivot_at_index_conjunct(output, state)
        && active_right_length_conjunct(input, output)
        && active_permutation_conjunct(input, state)
        && active_callback_partition_conjunct(boundary, state)
}

pub open spec fn spec_t(
    input: Input,
    boundary: CompareBoundary,
    output: Output,
    state: State,
) -> bool {
    target_definition_t(input, boundary, output, state)
}

pub open spec fn equivalent_t(
    left_output: Output,
    left_state: State,
    right_output: Output,
    right_state: State,
) -> bool {
    left_output == right_output && left_state == right_state
}

pub proof fn callback_transition_is_functional(
    boundary: CompareBoundary,
    state: int,
    left: int,
    right: int,
    ordering1: int,
    next_state1: int,
    panicked1: bool,
    ordering2: int,
    next_state2: int,
    panicked2: bool,
)
    requires
        compare_step(
            boundary, state, left, right,
            ordering1, next_state1, panicked1,
        ),
        compare_step(
            boundary, state, left, right,
            ordering2, next_state2, panicked2,
        ),
    ensures
        ordering1 == ordering2,
        next_state1 == next_state2,
        panicked1 == panicked2,
{
}

pub proof fn target_transition_implies_active_contract(
    input: Input,
    boundary: CompareBoundary,
    output: Output,
    state: State,
)
    requires
        requires_t(input),
        boundary_t(input, boundary),
        small_sort_mutable_slice_transition(input, boundary, state),
        final_subslice_transition(input, output, state),
    ensures
        active_final_concat_conjunct(input, output, state),
        active_left_length_conjunct(input, output),
        active_pivot_at_index_conjunct(output, state),
        active_right_length_conjunct(input, output),
        active_permutation_conjunct(input, state),
        active_callback_partition_conjunct(boundary, state),
{
}

pub proof fn shared_boundary_two_execution_theorem(
    input: Input,
    boundary: CompareBoundary,
    output1: Output,
    state1: State,
    output2: Output,
    state2: State,
)
    requires
        requires_t(input),
        boundary_t(input, boundary),
        spec_t(input, boundary, output1, state1),
        spec_t(input, boundary, output2, state2),
    ensures
        equivalent_t(output1, state1, output2, state2),
{
}

pub proof fn length_four_source_state_is_three_adapters(
    input: Input,
    boundary: CompareBoundary,
    state: State,
)
    requires
        requires_t(input),
        boundary_t(input, boundary),
        small_sort_mutable_slice_transition(input, boundary, state),
    ensures
        state.final_sequence == input.initial,
        state.callback_state
            == boundary.initial_state + 3 * boundary.next_delta,
{
}

pub proof fn length_four_one_or_two_adapters_is_impossible(
    input: Input,
    boundary: CompareBoundary,
    state: State,
)
    requires
        requires_t(input),
        boundary_t(input, boundary),
        small_sort_mutable_slice_transition(input, boundary, state),
        state.callback_state == boundary.initial_state + boundary.next_delta
            || state.callback_state
                == boundary.initial_state + 2 * boundary.next_delta,
    ensures
        false,
{
}

}
