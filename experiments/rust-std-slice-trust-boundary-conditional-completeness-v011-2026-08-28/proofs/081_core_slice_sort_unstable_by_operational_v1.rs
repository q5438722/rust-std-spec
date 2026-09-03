#![allow(dead_code, unused_imports, unused_variables)]
// Trusted-free composition of target 081 with the accepted target-080 transition.

use vstd::prelude::*;

verus! {

pub ghost struct ComparatorDropBoundary {
    pub ordering: Map<int, Map<int, Map<int, int>>>,
    pub next_state: Map<int, Map<int, Map<int, int>>>,
    pub next_observable_element_state:
        Map<int, Map<int, Map<int, Seq<int>>>>,
    pub panics: Map<int, Map<int, Map<int, bool>>>,
    pub drop_next_state: Map<int, Map<bool, int>>,
    pub drop_next_observable_element_state:
        Map<int, Map<bool, Seq<int>>>,
    pub drop_panics: Map<int, Map<bool, bool>>,
}

pub ghost struct SourceInput {
    pub sequence: Seq<int>,
    pub callback_state: int,
    pub observable_element_state: Seq<int>,
}

pub ghost struct SourceConfiguration {
    pub optimize_for_size: bool,
    pub target_pointer_width: nat,
    pub element_size: nat,
    pub is_freeze: bool,
    pub is_copy: bool,
    pub efficient_swap: bool,
}

pub ghost struct PrivateComparatorBoundary {
    pub adapter_model_id: int,
    pub ordering: Map<int, Map<int, Map<int, int>>>,
    pub next_state: Map<int, Map<int, Map<int, int>>>,
    pub next_observable_element_state:
        Map<int, Map<int, Map<int, Seq<int>>>>,
    pub panics: Map<int, Map<int, Map<int, bool>>>,
}

pub ghost struct AdapterResult {
    pub ordering: int,
    pub state: int,
    pub observable_element_state: Seq<int>,
    pub panicked: bool,
    pub callback_evaluations: nat,
    pub less_tested: bool,
    pub is_less: bool,
    pub comparator_observation: int,
}

pub ghost struct PrivateSortResult {
    pub sequence: Seq<int>,
    pub callback_state: int,
    pub observable_element_state: Seq<int>,
    pub terminal_status: int,
}

pub ghost struct AcceptedTarget080PrivateTransition {
    pub source_model_id: int,
    pub apply: spec_fn(
        SourceInput,
        SourceConfiguration,
        PrivateComparatorBoundary,
    ) -> PrivateSortResult,
}

pub ghost struct PublicSortResult {
    pub sequence: Seq<int>,
    pub callback_state: int,
    pub observable_element_state: Seq<int>,
    pub panicked: bool,
    pub aborted: bool,
    pub terminal: bool,
    pub terminal_status: int,
    pub unit_returned: bool,
    pub callback_drop_invoked: bool,
    pub callback_drop_completed: bool,
}

pub open spec fn ordering_valid(ordering: int) -> bool {
    -1 <= ordering <= 1
}

pub open spec fn accepted_target_080_private_transition(
    transition: AcceptedTarget080PrivateTransition,
) -> bool {
    transition.source_model_id == 80_196_1
}

pub open spec fn comparator_observation(
    boundary: ComparatorDropBoundary,
    state: int,
    left: int,
    right: int,
) -> int {
    boundary.ordering[state][left][right]
}

pub open spec fn source_ordering_to_less_adapter(
    boundary: ComparatorDropBoundary,
    state: int,
    left: int,
    right: int,
) -> AdapterResult {
    let ordering = comparator_observation(boundary, state, left, right);
    let panicked = boundary.panics[state][left][right];
    AdapterResult {
        ordering,
        state: boundary.next_state[state][left][right],
        observable_element_state:
            boundary.next_observable_element_state[state][left][right],
        panicked,
        callback_evaluations: 1,
        less_tested: !panicked,
        is_less: !panicked && ordering == -1,
        comparator_observation: ordering,
    }
}

pub open spec fn source_private_comparator_boundary(
    boundary: ComparatorDropBoundary,
) -> PrivateComparatorBoundary {
    PrivateComparatorBoundary {
        adapter_model_id: 81_196_1,
        ordering: boundary.ordering,
        next_state: boundary.next_state,
        next_observable_element_state:
            boundary.next_observable_element_state,
        panics: boundary.panics,
    }
}

pub open spec fn accepted_private_source_transition(
    transition: AcceptedTarget080PrivateTransition,
    input: SourceInput,
    configuration: SourceConfiguration,
    boundary: ComparatorDropBoundary,
) -> PrivateSortResult {
    (transition.apply)(
        input,
        configuration,
        source_private_comparator_boundary(boundary),
    )
}

pub open spec fn source_public_finish(
    boundary: ComparatorDropBoundary,
    private: PrivateSortResult,
) -> PublicSortResult {
    if private.terminal_status == 2 {
        PublicSortResult {
            sequence: private.sequence,
            callback_state: private.callback_state,
            observable_element_state: private.observable_element_state,
            panicked: false,
            aborted: true,
            terminal: true,
            terminal_status: 2,
            unit_returned: false,
            callback_drop_invoked: false,
            callback_drop_completed: false,
        }
    } else {
        let unwinding = private.terminal_status == 1;
        let drop_panicked =
            boundary.drop_panics[private.callback_state][unwinding];
        let status =
            if drop_panicked {
                if unwinding { 2 } else { 1 }
            } else if unwinding {
                1
            } else {
                0
            };
        PublicSortResult {
            sequence: private.sequence,
            callback_state:
                boundary.drop_next_state[private.callback_state][unwinding],
            observable_element_state:
                boundary.drop_next_observable_element_state[
                    private.callback_state
                ][unwinding],
            panicked: status == 1,
            aborted: status == 2,
            terminal: true,
            terminal_status: status,
            unit_returned: status == 0,
            callback_drop_invoked: true,
            callback_drop_completed: !drop_panicked,
        }
    }
}

pub open spec fn source_public_sort(
    transition: AcceptedTarget080PrivateTransition,
    input: SourceInput,
    configuration: SourceConfiguration,
    boundary: ComparatorDropBoundary,
) -> PublicSortResult {
    source_public_finish(
        boundary,
        accepted_private_source_transition(
            transition,
            input,
            configuration,
            boundary,
        ),
    )
}

pub proof fn adapter_evaluates_compare_exactly_once(
    boundary: ComparatorDropBoundary,
    state: int,
    left: int,
    right: int,
)
    ensures
        source_ordering_to_less_adapter(
            boundary, state, left, right,
        ).callback_evaluations == 1,
{
}

pub proof fn adapter_propagates_all_observable_state_and_panic(
    boundary: ComparatorDropBoundary,
    state: int,
    left: int,
    right: int,
)
    ensures
        source_ordering_to_less_adapter(
            boundary, state, left, right,
        ).state == boundary.next_state[state][left][right],
        source_ordering_to_less_adapter(
            boundary, state, left, right,
        ).observable_element_state
            == boundary.next_observable_element_state[state][left][right],
        source_ordering_to_less_adapter(
            boundary, state, left, right,
        ).panicked == boundary.panics[state][left][right],
        source_ordering_to_less_adapter(
            boundary, state, left, right,
        ).comparator_observation
            == comparator_observation(boundary, state, left, right),
{
}

pub proof fn less_is_tested_only_after_successful_callback(
    boundary: ComparatorDropBoundary,
    state: int,
    left: int,
    right: int,
)
    ensures
        source_ordering_to_less_adapter(
            boundary, state, left, right,
        ).less_tested
            == !boundary.panics[state][left][right],
        source_ordering_to_less_adapter(
            boundary, state, left, right,
        ).is_less
            == (
                !boundary.panics[state][left][right]
                && comparator_observation(boundary, state, left, right) == -1
            ),
{
}

pub proof fn private_boundary_is_exact_ordering_to_less_lowering(
    boundary: ComparatorDropBoundary,
)
    ensures
        source_private_comparator_boundary(boundary).adapter_model_id
            == 81_196_1,
        source_private_comparator_boundary(boundary).ordering
            == boundary.ordering,
        source_private_comparator_boundary(boundary).next_state
            == boundary.next_state,
        source_private_comparator_boundary(
            boundary,
        ).next_observable_element_state
            == boundary.next_observable_element_state,
        source_private_comparator_boundary(boundary).panics
            == boundary.panics,
{
}

pub proof fn normal_finish_drops_callback_after_private_sort(
    transition: AcceptedTarget080PrivateTransition,
    input: SourceInput,
    configuration: SourceConfiguration,
    boundary: ComparatorDropBoundary,
)
    requires
        accepted_target_080_private_transition(transition),
        accepted_private_source_transition(
            transition, input, configuration, boundary,
        ).terminal_status == 0,
        !boundary.drop_panics[
            accepted_private_source_transition(
                transition, input, configuration, boundary,
            ).callback_state
        ][false],
    ensures
        source_public_sort(
            transition, input, configuration, boundary,
        ).terminal_status == 0,
        source_public_sort(
            transition, input, configuration, boundary,
        ).unit_returned,
        source_public_sort(
            transition, input, configuration, boundary,
        ).callback_drop_invoked,
        source_public_sort(
            transition, input, configuration, boundary,
        ).callback_drop_completed,
{
}

pub proof fn normal_drop_panic_becomes_target_panic(
    transition: AcceptedTarget080PrivateTransition,
    input: SourceInput,
    configuration: SourceConfiguration,
    boundary: ComparatorDropBoundary,
)
    requires
        accepted_target_080_private_transition(transition),
        accepted_private_source_transition(
            transition, input, configuration, boundary,
        ).terminal_status == 0,
        boundary.drop_panics[
            accepted_private_source_transition(
                transition, input, configuration, boundary,
            ).callback_state
        ][false],
    ensures
        source_public_sort(
            transition, input, configuration, boundary,
        ).terminal_status == 1,
        source_public_sort(
            transition, input, configuration, boundary,
        ).panicked,
        !source_public_sort(
            transition, input, configuration, boundary,
        ).aborted,
        !source_public_sort(
            transition, input, configuration, boundary,
        ).callback_drop_completed,
{
}

pub proof fn unwind_drop_completion_preserves_comparator_panic(
    transition: AcceptedTarget080PrivateTransition,
    input: SourceInput,
    configuration: SourceConfiguration,
    boundary: ComparatorDropBoundary,
)
    requires
        accepted_target_080_private_transition(transition),
        accepted_private_source_transition(
            transition, input, configuration, boundary,
        ).terminal_status == 1,
        !boundary.drop_panics[
            accepted_private_source_transition(
                transition, input, configuration, boundary,
            ).callback_state
        ][true],
    ensures
        source_public_sort(
            transition, input, configuration, boundary,
        ).terminal_status == 1,
        source_public_sort(
            transition, input, configuration, boundary,
        ).panicked,
        source_public_sort(
            transition, input, configuration, boundary,
        ).callback_drop_completed,
{
}

pub proof fn unwind_drop_panic_is_abort(
    transition: AcceptedTarget080PrivateTransition,
    input: SourceInput,
    configuration: SourceConfiguration,
    boundary: ComparatorDropBoundary,
)
    requires
        accepted_target_080_private_transition(transition),
        accepted_private_source_transition(
            transition, input, configuration, boundary,
        ).terminal_status == 1,
        boundary.drop_panics[
            accepted_private_source_transition(
                transition, input, configuration, boundary,
            ).callback_state
        ][true],
    ensures
        source_public_sort(
            transition, input, configuration, boundary,
        ).terminal_status == 2,
        source_public_sort(
            transition, input, configuration, boundary,
        ).aborted,
        !source_public_sort(
            transition, input, configuration, boundary,
        ).panicked,
        !source_public_sort(
            transition, input, configuration, boundary,
        ).callback_drop_completed,
{
}

pub proof fn preexisting_abort_does_not_run_drop_glue(
    transition: AcceptedTarget080PrivateTransition,
    input: SourceInput,
    configuration: SourceConfiguration,
    boundary: ComparatorDropBoundary,
)
    requires
        accepted_target_080_private_transition(transition),
        accepted_private_source_transition(
            transition, input, configuration, boundary,
        ).terminal_status == 2,
    ensures
        source_public_sort(
            transition, input, configuration, boundary,
        ).terminal_status == 2,
        source_public_sort(
            transition, input, configuration, boundary,
        ).aborted,
        !source_public_sort(
            transition, input, configuration, boundary,
        ).callback_drop_invoked,
        source_public_sort(
            transition, input, configuration, boundary,
        ).observable_element_state
            == accepted_private_source_transition(
                transition, input, configuration, boundary,
            ).observable_element_state,
{
}

pub proof fn public_sort_preserves_private_sequence_and_uses_drop_state(
    transition: AcceptedTarget080PrivateTransition,
    input: SourceInput,
    configuration: SourceConfiguration,
    boundary: ComparatorDropBoundary,
)
    requires
        accepted_target_080_private_transition(transition),
        0 <= accepted_private_source_transition(
            transition, input, configuration, boundary,
        ).terminal_status <= 2,
    ensures
        source_public_sort(
            transition, input, configuration, boundary,
        ).sequence
            == accepted_private_source_transition(
                transition, input, configuration, boundary,
            ).sequence,
        source_public_sort(
            transition, input, configuration, boundary,
        ).terminal,
        source_public_sort(
            transition, input, configuration, boundary,
        ).callback_drop_invoked
            == (
                accepted_private_source_transition(
                    transition, input, configuration, boundary,
                ).terminal_status != 2
            ),
{
}

pub proof fn fixed_boundary_accepted_transition_is_deterministic(
    first: AcceptedTarget080PrivateTransition,
    second: AcceptedTarget080PrivateTransition,
    input: SourceInput,
    configuration: SourceConfiguration,
    boundary: ComparatorDropBoundary,
)
    requires
        accepted_target_080_private_transition(first),
        accepted_target_080_private_transition(second),
        first.apply == second.apply,
    ensures
        source_public_sort(first, input, configuration, boundary)
            == source_public_sort(second, input, configuration, boundary),
{
}

}
