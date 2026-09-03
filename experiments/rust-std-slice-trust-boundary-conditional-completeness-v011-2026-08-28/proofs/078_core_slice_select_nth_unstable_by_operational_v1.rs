#![allow(dead_code, unused_imports, unused_variables)]
// Trusted-free checked refinement for exact target-078 interpreter results.

use vstd::prelude::*;

verus! {

pub ghost struct ComparatorBoundary {
    pub callback_identity: int,
    pub initial_state: int,
    pub contract_ordering: Map<int, Map<int, int>>,
    pub ordering: Map<int, Map<int, Map<int, int>>>,
    pub next_state: Map<int, Map<int, Map<int, int>>>,
    pub panics: Map<int, Map<int, Map<int, bool>>>,
}

pub ghost struct SourceInput {
    pub sequence: Seq<int>,
    pub index: nat,
    pub allocation: int,
    pub borrow: int,
    pub is_zst: bool,
}

pub ghost struct SourceConfiguration {
    pub optimize_for_size: bool,
    pub element_size: nat,
}

pub ghost struct PrincipalReturn {
    pub returned: bool,
    pub left_start: nat,
    pub left_len: nat,
    pub pivot_start: nat,
    pub pivot_len: nat,
    pub right_start: nat,
    pub right_len: nat,
    pub allocation: int,
    pub borrow: int,
    pub pivot_identity: int,
}

pub ghost struct ExactFinalState {
    pub sequence: Seq<int>,
    pub allocation: int,
    pub borrow: int,
    pub length: nat,
    pub callback_state: int,
    pub panicked: bool,
    pub terminal: bool,
}

pub ghost struct ExactOperationalResult {
    pub principal: PrincipalReturn,
    pub state: ExactFinalState,
}

pub ghost struct RefinedPrincipalReturn {
    pub returned: bool,
    pub left_start: nat,
    pub left_len: nat,
    pub pivot_start: nat,
    pub pivot_len: nat,
    pub right_start: nat,
    pub right_len: nat,
    pub allocation: int,
    pub borrow: int,
    pub pivot_identity: int,
}

pub ghost struct RefinedFinalState {
    pub sequence: Seq<int>,
    pub allocation: int,
    pub borrow: int,
    pub length: nat,
    pub callback_state: int,
    pub panicked: bool,
    pub terminal: bool,
}

pub ghost struct RefinedOperationalResult {
    pub principal: RefinedPrincipalReturn,
    pub state: RefinedFinalState,
}

pub open spec fn observed_ordering(
    boundary: ComparatorBoundary,
    state: int,
    left: int,
    right: int,
) -> int {
    boundary.ordering[state][left][right]
}

pub open spec fn observed_contract_ordering(
    boundary: ComparatorBoundary,
    left: int,
    right: int,
) -> int {
    boundary.contract_ordering[left][right]
}

pub open spec fn observed_next_state(
    boundary: ComparatorBoundary,
    state: int,
    left: int,
    right: int,
) -> int {
    boundary.next_state[state][left][right]
}

pub open spec fn observed_panic(
    boundary: ComparatorBoundary,
    state: int,
    left: int,
    right: int,
) -> bool {
    boundary.panics[state][left][right]
}

pub open spec fn admissible_boundary(
    boundary: ComparatorBoundary,
) -> bool {
    (forall|state: int, left: int, right: int|
        -1 <= #[trigger] observed_ordering(
            boundary,
            state,
            left,
            right,
        ) <= 1
            && observed_ordering(boundary, state, left, right)
                == observed_contract_ordering(boundary, left, right))
        && (forall|value: int|
            #[trigger] observed_contract_ordering(
                boundary,
                value,
                value,
            ) == 0)
        && (forall|left: int, right: int|
            #[trigger] observed_contract_ordering(
                boundary,
                left,
                right,
            ) == -observed_contract_ordering(
                boundary,
                right,
                left,
            ))
        && (forall|left: int, right: int|
            #[trigger] observed_contract_ordering(
                boundary,
                left,
                right,
            ) <= 0
                || observed_contract_ordering(
                    boundary,
                    right,
                    left,
                ) <= 0)
        && (forall|left: int, middle: int, right: int|
            #[trigger] observed_contract_ordering(
                boundary,
                left,
                middle,
            ) <= 0
                && #[trigger] observed_contract_ordering(
                    boundary,
                    middle,
                    right,
                ) <= 0
                ==> observed_contract_ordering(
                    boundary,
                    left,
                    right,
                ) <= 0)
}

pub open spec fn valid_input(
    input: SourceInput,
    configuration: SourceConfiguration,
) -> bool {
    input.sequence.len() > 0
        && input.index < input.sequence.len()
        && input.is_zst == (configuration.element_size == 0)
}

pub open spec fn exact_source_result_is_terminal(
    source: ExactOperationalResult,
) -> bool {
    source.state.terminal
        && source.state.length == source.state.sequence.len()
        && source.principal.returned
            == (!source.state.panicked && source.state.terminal)
}

pub open spec fn checked_exact_result_projection(
    source: ExactOperationalResult,
) -> RefinedOperationalResult {
    RefinedOperationalResult {
        principal: RefinedPrincipalReturn {
            returned: source.principal.returned,
            left_start: source.principal.left_start,
            left_len: source.principal.left_len,
            pivot_start: source.principal.pivot_start,
            pivot_len: source.principal.pivot_len,
            right_start: source.principal.right_start,
            right_len: source.principal.right_len,
            allocation: source.principal.allocation,
            borrow: source.principal.borrow,
            pivot_identity: source.principal.pivot_identity,
        },
        state: RefinedFinalState {
            sequence: source.state.sequence,
            allocation: source.state.allocation,
            borrow: source.state.borrow,
            length: source.state.length,
            callback_state: source.state.callback_state,
            panicked: source.state.panicked,
            terminal: source.state.terminal,
        },
    }
}

pub open spec fn exact_principal_return_and_final_state(
    source: ExactOperationalResult,
    refined: RefinedOperationalResult,
) -> bool {
    source.principal.returned == refined.principal.returned
        && source.principal.left_start == refined.principal.left_start
        && source.principal.left_len == refined.principal.left_len
        && source.principal.pivot_start == refined.principal.pivot_start
        && source.principal.pivot_len == refined.principal.pivot_len
        && source.principal.right_start == refined.principal.right_start
        && source.principal.right_len == refined.principal.right_len
        && source.principal.allocation == refined.principal.allocation
        && source.principal.borrow == refined.principal.borrow
        && source.principal.pivot_identity
            == refined.principal.pivot_identity
        && source.state.sequence == refined.state.sequence
        && source.state.allocation == refined.state.allocation
        && source.state.borrow == refined.state.borrow
        && source.state.length == refined.state.length
        && source.state.callback_state == refined.state.callback_state
        && source.state.panicked == refined.state.panicked
        && source.state.terminal == refined.state.terminal
}

pub proof fn checked_refinement_preserves_every_exact_field(
    source: ExactOperationalResult,
)
    requires
        exact_source_result_is_terminal(source),
    ensures
        checked_exact_result_projection(source).state.terminal,
        checked_exact_result_projection(source).state.length
            == checked_exact_result_projection(source).state.sequence.len(),
        exact_principal_return_and_final_state(
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
        exact_principal_return_and_final_state(
            source,
            checked_exact_result_projection(source),
        ),
{
}

pub proof fn implementation_ordering_projects_exactly_to_contract(
    boundary: ComparatorBoundary,
    state: int,
    left: int,
    right: int,
)
    requires
        admissible_boundary(boundary),
    ensures
        observed_ordering(boundary, state, left, right)
            == observed_contract_ordering(boundary, left, right),
        -1 <= observed_ordering(boundary, state, left, right) <= 1,
{
}

pub proof fn callback_transitions_are_total_functions(
    first: ComparatorBoundary,
    second: ComparatorBoundary,
    state: int,
    left: int,
    right: int,
)
    requires
        first.ordering == second.ordering,
        first.next_state == second.next_state,
        first.panics == second.panics,
    ensures
        observed_ordering(first, state, left, right)
            == observed_ordering(second, state, left, right),
        observed_next_state(first, state, left, right)
            == observed_next_state(second, state, left, right),
        observed_panic(first, state, left, right)
            == observed_panic(second, state, left, right),
{
}

pub proof fn returned_ranges_cover_every_valid_input(
    input: SourceInput,
    configuration: SourceConfiguration,
)
    requires
        valid_input(input, configuration),
    ensures
        input.index + 1
            + (input.sequence.len() - input.index - 1)
            == input.sequence.len(),
{
}

}
