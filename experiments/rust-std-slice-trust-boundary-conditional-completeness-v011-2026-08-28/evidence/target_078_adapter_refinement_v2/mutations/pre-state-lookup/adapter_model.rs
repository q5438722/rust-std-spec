#![allow(dead_code, unused_imports, unused_variables)]
// Constructive refinement of the target-078 comparator-to-Less adapter.

use vstd::prelude::*;

verus! {

pub ghost struct ComparatorBoundary {
    pub b_callback_identity: int,
    pub b_initial_state: int,
    pub b_contract_ordering: Map<int, Map<int, int>>,
    pub b_ordering: Map<int, Map<int, Map<int, int>>>,
    pub b_next_state: Map<int, Map<int, Map<int, int>>>,
    pub b_panics: Map<int, Map<int, Map<int, bool>>>,
}

pub ghost struct ComparatorAdapterFrame {
    pub caf_callback_identity: int,
    pub caf_lookup_state: int,
    pub caf_left_identity: int,
    pub caf_right_identity: int,
    pub caf_ordering: int,
    pub caf_next_state: int,
    pub caf_panicked: bool,
    pub caf_returned: bool,
    pub caf_is_less: bool,
}

pub open spec fn boundary_ordering(
    boundary: ComparatorBoundary,
    state: int,
    left: int,
    right: int,
) -> int {
    boundary.b_ordering[state][left][right]
}

pub open spec fn boundary_next_state(
    boundary: ComparatorBoundary,
    state: int,
    left: int,
    right: int,
) -> int {
    boundary.b_next_state[state][left][right]
}

pub open spec fn boundary_panics(
    boundary: ComparatorBoundary,
    state: int,
    left: int,
    right: int,
) -> bool {
    boundary.b_panics[state][left][right]
}

pub open spec fn target_adapter_is_less(
    boundary: ComparatorBoundary,
    state: int,
    left: int,
    right: int,
) -> bool {
    boundary_ordering(boundary, state, left, right) == -1
}

pub open spec fn comparator_adapter_transition(
    boundary: ComparatorBoundary,
    state: int,
    left: int,
    right: int,
) -> ComparatorAdapterFrame {
    let ordering = boundary_ordering(boundary, boundary.b_initial_state, left, right);
    let next = boundary_next_state(boundary, boundary.b_initial_state, left, right);
    let panics = boundary_panics(boundary, boundary.b_initial_state, left, right);
    let returned = !panics;
    ComparatorAdapterFrame {
        caf_callback_identity: boundary.b_callback_identity,
        caf_lookup_state: state,
        caf_left_identity: left,
        caf_right_identity: right,
        caf_ordering: ordering,
        caf_next_state: next,
        caf_panicked: panics,
        caf_returned: returned,
        caf_is_less: returned
            && target_adapter_is_less(boundary, boundary.b_initial_state, left, right),
    }
}

pub proof fn transition_records_ordered_operands_and_pre_state(
    boundary: ComparatorBoundary,
    state: int,
    left: int,
    right: int,
)
    ensures
        comparator_adapter_transition(
            boundary,
            state,
            left,
            right,
        ).caf_lookup_state == state,
        comparator_adapter_transition(
            boundary,
            state,
            left,
            right,
        ).caf_left_identity == left,
        comparator_adapter_transition(
            boundary,
            state,
            left,
            right,
        ).caf_right_identity == right,
        comparator_adapter_transition(
            boundary,
            state,
            left,
            right,
        ).caf_ordering
            == boundary_ordering(boundary, state, left, right),
{
}

pub proof fn callback_next_state_threads_on_normal_return(
    boundary: ComparatorBoundary,
    state: int,
    left: int,
    right: int,
)
    requires
        !boundary_panics(boundary, state, left, right),
    ensures
        comparator_adapter_transition(
            boundary,
            state,
            left,
            right,
        ).caf_next_state
            == boundary_next_state(boundary, state, left, right),
        comparator_adapter_transition(
            boundary,
            state,
            left,
            right,
        ).caf_returned,
{
}

pub proof fn callback_next_state_threads_before_panic_propagation(
    boundary: ComparatorBoundary,
    state: int,
    left: int,
    right: int,
)
    requires
        boundary_panics(boundary, state, left, right),
    ensures
        comparator_adapter_transition(
            boundary,
            state,
            left,
            right,
        ).caf_next_state
            == boundary_next_state(boundary, state, left, right),
        comparator_adapter_transition(
            boundary,
            state,
            left,
            right,
        ).caf_panicked,
{
}

pub proof fn panic_flag_matches_boundary_observation(
    boundary: ComparatorBoundary,
    state: int,
    left: int,
    right: int,
)
    ensures
        comparator_adapter_transition(
            boundary,
            state,
            left,
            right,
        ).caf_panicked
            == boundary_panics(boundary, state, left, right),
{
}

pub proof fn normal_less_returns_true(
    boundary: ComparatorBoundary,
    state: int,
    left: int,
    right: int,
)
    requires
        !boundary_panics(boundary, state, left, right),
        boundary_ordering(boundary, state, left, right) == -1,
    ensures
        comparator_adapter_transition(
            boundary,
            state,
            left,
            right,
        ).caf_returned,
        comparator_adapter_transition(
            boundary,
            state,
            left,
            right,
        ).caf_is_less,
{
}

pub proof fn normal_equal_returns_false(
    boundary: ComparatorBoundary,
    state: int,
    left: int,
    right: int,
)
    requires
        !boundary_panics(boundary, state, left, right),
        boundary_ordering(boundary, state, left, right) == 0,
    ensures
        comparator_adapter_transition(
            boundary,
            state,
            left,
            right,
        ).caf_returned,
        !comparator_adapter_transition(
            boundary,
            state,
            left,
            right,
        ).caf_is_less,
{
}

pub proof fn normal_greater_returns_false(
    boundary: ComparatorBoundary,
    state: int,
    left: int,
    right: int,
)
    requires
        !boundary_panics(boundary, state, left, right),
        boundary_ordering(boundary, state, left, right) == 1,
    ensures
        comparator_adapter_transition(
            boundary,
            state,
            left,
            right,
        ).caf_returned,
        !comparator_adapter_transition(
            boundary,
            state,
            left,
            right,
        ).caf_is_less,
{
}

pub proof fn panic_suppresses_returned_boolean(
    boundary: ComparatorBoundary,
    state: int,
    left: int,
    right: int,
)
    requires
        boundary_panics(boundary, state, left, right),
    ensures
        !comparator_adapter_transition(
            boundary,
            state,
            left,
            right,
        ).caf_returned,
        !comparator_adapter_transition(
            boundary,
            state,
            left,
            right,
        ).caf_is_less,
{
}

pub proof fn normal_boolean_equals_target_adapter_is_less(
    boundary: ComparatorBoundary,
    state: int,
    left: int,
    right: int,
)
    requires
        !boundary_panics(boundary, state, left, right),
    ensures
        comparator_adapter_transition(
            boundary,
            state,
            left,
            right,
        ).caf_is_less
            == target_adapter_is_less(
                boundary,
                state,
                left,
                right,
            ),
{
}

pub proof fn callback_state_update_is_retained_on_panic(
    boundary: ComparatorBoundary,
    state: int,
    left: int,
    right: int,
)
    requires
        boundary_panics(boundary, state, left, right),
    ensures
        comparator_adapter_transition(
            boundary,
            state,
            left,
            right,
        ).caf_next_state
            == boundary_next_state(boundary, state, left, right),
        comparator_adapter_transition(
            boundary,
            state,
            left,
            right,
        ).caf_lookup_state == state,
{
}

pub proof fn boundary_initial_state_selects_entry_lookup(
    boundary: ComparatorBoundary,
    left: int,
    right: int,
)
    ensures
        comparator_adapter_transition(
            boundary,
            boundary.b_initial_state,
            left,
            right,
        ).caf_lookup_state == boundary.b_initial_state,
        comparator_adapter_transition(
            boundary,
            boundary.b_initial_state,
            left,
            right,
        ).caf_next_state
            == boundary_next_state(
                boundary,
                boundary.b_initial_state,
                left,
                right,
            ),
{
}

}
