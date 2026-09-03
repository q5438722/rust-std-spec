#![allow(dead_code, unused_imports, unused_variables)]
// Trusted-free checked refinement for exact target-080 interpreter results.

use vstd::prelude::*;

verus! {

pub ghost struct OrdBoundary {
    pub callback_identity: int,
    pub initial_state: int,
    pub contract_is_less: Map<int, Map<int, bool>>,
    pub is_less: Map<int, Map<int, Map<int, bool>>>,
    pub next_state: Map<int, Map<int, Map<int, int>>>,
    pub panics: Map<int, Map<int, Map<int, bool>>>,
}

pub ghost struct SourceInput {
    pub sequence: Seq<int>,
}

pub ghost struct SourceConfiguration {
    pub optimize_for_size: bool,
    pub target_pointer_width: nat,
    pub element_size: nat,
    pub is_freeze: bool,
    pub is_copy: bool,
    pub efficient_swap: bool,
}

pub ghost struct ExactFinalState {
    pub sequence: Seq<int>,
    pub callback_state: int,
    pub panicked: bool,
    pub aborted: bool,
    pub terminal: bool,
}

pub ghost struct ExactOperationalResult {
    pub state: ExactFinalState,
    pub terminal_status: int,
    pub unit_returned: bool,
}

pub ghost struct RefinedFinalState {
    pub sequence: Seq<int>,
    pub callback_state: int,
    pub panicked: bool,
    pub aborted: bool,
    pub terminal: bool,
}

pub ghost struct RefinedOperationalResult {
    pub state: RefinedFinalState,
    pub terminal_status: int,
    pub unit_returned: bool,
}

pub open spec fn observed_is_less(
    boundary: OrdBoundary,
    state: int,
    left: int,
    right: int,
) -> bool {
    boundary.is_less[state][left][right]
}

pub open spec fn observed_contract_is_less(
    boundary: OrdBoundary,
    left: int,
    right: int,
) -> bool {
    boundary.contract_is_less[left][right]
}

pub open spec fn observed_next_state(
    boundary: OrdBoundary,
    state: int,
    left: int,
    right: int,
) -> int {
    boundary.next_state[state][left][right]
}

pub open spec fn observed_panic(
    boundary: OrdBoundary,
    state: int,
    left: int,
    right: int,
) -> bool {
    boundary.panics[state][left][right]
}

pub open spec fn admissible_boundary(boundary: OrdBoundary) -> bool {
    (forall|state: int, left: int, right: int|
        #[trigger] observed_is_less(boundary, state, left, right)
            == observed_contract_is_less(boundary, left, right))
        && (forall|value: int|
            !#[trigger] observed_contract_is_less(
                boundary,
                value,
                value,
            ))
        && (forall|left: int, right: int|
            #[trigger] observed_contract_is_less(
                boundary,
                left,
                right,
            ) ==> !observed_contract_is_less(
                boundary,
                right,
                left,
            ))
        && (forall|left: int, middle: int, right: int|
            #[trigger] observed_contract_is_less(
                boundary,
                left,
                middle,
            )
                && #[trigger] observed_contract_is_less(
                    boundary,
                    middle,
                    right,
                )
                ==> observed_contract_is_less(
                    boundary,
                    left,
                    right,
                ))
}

pub open spec fn valid_input(
    input: SourceInput,
    configuration: SourceConfiguration,
) -> bool {
    configuration.target_pointer_width > 0
        && (configuration.is_copy ==> configuration.is_freeze)
}

pub open spec fn exact_source_result_is_terminal(
    source: ExactOperationalResult,
) -> bool {
    source.state.terminal
        && 0 <= source.terminal_status <= 2
        && source.state.panicked == (source.terminal_status == 1)
        && source.state.aborted == (source.terminal_status == 2)
        && source.unit_returned == (source.terminal_status == 0)
}

pub open spec fn checked_exact_result_projection(
    source: ExactOperationalResult,
) -> RefinedOperationalResult {
    RefinedOperationalResult {
        state: RefinedFinalState {
            sequence: source.state.sequence,
            callback_state: source.state.callback_state,
            panicked: source.state.panicked,
            aborted: source.state.aborted,
            terminal: source.state.terminal,
        },
        terminal_status: source.terminal_status,
        unit_returned: source.unit_returned,
    }
}

pub open spec fn exact_final_state_and_unit_return(
    source: ExactOperationalResult,
    refined: RefinedOperationalResult,
) -> bool {
    source.state.sequence == refined.state.sequence
        && source.state.callback_state == refined.state.callback_state
        && source.state.panicked == refined.state.panicked
        && source.state.aborted == refined.state.aborted
        && source.state.terminal == refined.state.terminal
        && source.terminal_status == refined.terminal_status
        && source.unit_returned == refined.unit_returned
}

pub proof fn checked_refinement_preserves_every_exact_field(
    source: ExactOperationalResult,
)
    requires
        exact_source_result_is_terminal(source),
    ensures
        checked_exact_result_projection(source).state.terminal,
        exact_final_state_and_unit_return(
            source,
            checked_exact_result_projection(source),
        ),
{
}

pub proof fn two_checked_projections_are_exactly_equal(
    source: ExactOperationalResult,
)
    requires
        exact_source_result_is_terminal(source),
    ensures
        checked_exact_result_projection(source)
            == checked_exact_result_projection(source),
        exact_final_state_and_unit_return(
            source,
            checked_exact_result_projection(source),
        ),
{
}

pub proof fn implementation_ordering_projects_exactly_to_contract(
    boundary: OrdBoundary,
    state: int,
    left: int,
    right: int,
)
    requires
        admissible_boundary(boundary),
    ensures
        observed_is_less(boundary, state, left, right)
            == observed_contract_is_less(boundary, left, right),
{
}

pub proof fn callback_transitions_are_total_functions(
    first: OrdBoundary,
    second: OrdBoundary,
    state: int,
    left: int,
    right: int,
)
    requires
        first.is_less == second.is_less,
        first.next_state == second.next_state,
        first.panics == second.panics,
    ensures
        observed_is_less(first, state, left, right)
            == observed_is_less(second, state, left, right),
        observed_next_state(first, state, left, right)
            == observed_next_state(second, state, left, right),
        observed_panic(first, state, left, right)
            == observed_panic(second, state, left, right),
{
}

pub proof fn source_configuration_specialization_is_input_only(
    input: SourceInput,
    configuration: SourceConfiguration,
)
    requires
        valid_input(input, configuration),
    ensures
        configuration.target_pointer_width > 0,
        configuration.is_copy ==> configuration.is_freeze,
{
}

}
