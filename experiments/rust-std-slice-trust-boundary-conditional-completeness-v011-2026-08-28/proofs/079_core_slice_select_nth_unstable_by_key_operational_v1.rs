#![allow(dead_code, unused_imports, unused_variables)]
// Trusted-free checked refinement for exact target-079 interpreter results.

use vstd::prelude::*;

verus! {

pub ghost struct OwnedKey {
    pub creation_state: int,
    pub slot: int,
    pub source_identity: int,
    pub key_identity: int,
}

pub ghost struct KeyOrdDropBoundary {
    pub callback_identity: int,
    pub key_function_identity: int,
    pub ord_function_identity: int,
    pub drop_function_identity: int,
    pub initial_state: int,
    pub contract_key: Map<int, int>,
    pub contract_ordering: Map<int, Map<int, int>>,
    pub key_result: Map<int, Map<int, int>>,
    pub key_next_state: Map<int, Map<int, int>>,
    pub key_panics: Map<int, Map<int, bool>>,
    pub ord_lt_result: Map<int, Map<OwnedKey, Map<OwnedKey, bool>>>,
    pub ord_lt_next_state: Map<int, Map<OwnedKey, Map<OwnedKey, int>>>,
    pub ord_lt_panics: Map<int, Map<OwnedKey, Map<OwnedKey, bool>>>,
    pub drop_next_state: Map<int, Map<OwnedKey, int>>,
    pub drop_panics: Map<int, Map<OwnedKey, bool>>,
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
    pub termination: int,
    pub panicked: bool,
    pub aborted: bool,
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
    pub termination: int,
    pub panicked: bool,
    pub aborted: bool,
    pub terminal: bool,
}

pub ghost struct RefinedOperationalResult {
    pub principal: RefinedPrincipalReturn,
    pub state: RefinedFinalState,
}

pub open spec fn observed_contract_key(
    boundary: KeyOrdDropBoundary,
    value: int,
) -> int {
    boundary.contract_key[value]
}

pub open spec fn observed_contract_ordering(
    boundary: KeyOrdDropBoundary,
    left_key: int,
    right_key: int,
) -> int {
    boundary.contract_ordering[left_key][right_key]
}

pub open spec fn observed_key_result(
    boundary: KeyOrdDropBoundary,
    state: int,
    value: int,
) -> int {
    boundary.key_result[state][value]
}

pub open spec fn observed_key_next_state(
    boundary: KeyOrdDropBoundary,
    state: int,
    value: int,
) -> int {
    boundary.key_next_state[state][value]
}

pub open spec fn observed_key_panic(
    boundary: KeyOrdDropBoundary,
    state: int,
    value: int,
) -> bool {
    boundary.key_panics[state][value]
}

pub open spec fn observed_ord_lt(
    boundary: KeyOrdDropBoundary,
    state: int,
    left: OwnedKey,
    right: OwnedKey,
) -> bool {
    boundary.ord_lt_result[state][left][right]
}

pub open spec fn observed_ord_next_state(
    boundary: KeyOrdDropBoundary,
    state: int,
    left: OwnedKey,
    right: OwnedKey,
) -> int {
    boundary.ord_lt_next_state[state][left][right]
}

pub open spec fn observed_ord_panic(
    boundary: KeyOrdDropBoundary,
    state: int,
    left: OwnedKey,
    right: OwnedKey,
) -> bool {
    boundary.ord_lt_panics[state][left][right]
}

pub open spec fn observed_drop_next_state(
    boundary: KeyOrdDropBoundary,
    state: int,
    key: OwnedKey,
) -> int {
    boundary.drop_next_state[state][key]
}

pub open spec fn observed_drop_panic(
    boundary: KeyOrdDropBoundary,
    state: int,
    key: OwnedKey,
) -> bool {
    boundary.drop_panics[state][key]
}

pub open spec fn left_owned_key(
    state: int,
    source_identity: int,
    key_identity: int,
) -> OwnedKey {
    OwnedKey {
        creation_state: state,
        slot: 0,
        source_identity,
        key_identity,
    }
}

pub open spec fn right_owned_key(
    state: int,
    source_identity: int,
    key_identity: int,
) -> OwnedKey {
    OwnedKey {
        creation_state: state,
        slot: 1,
        source_identity,
        key_identity,
    }
}

pub open spec fn admissible_boundary(
    boundary: KeyOrdDropBoundary,
) -> bool {
    (forall|state: int, value: int|
        #[trigger] observed_key_result(boundary, state, value)
            == observed_contract_key(boundary, value))
        && (forall|state: int, left: OwnedKey, right: OwnedKey|
            #[trigger] observed_ord_lt(boundary, state, left, right)
                == (observed_contract_ordering(
                    boundary,
                    left.key_identity,
                    right.key_identity,
                ) == -1))
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
        && 0 <= source.state.termination <= 2
        && source.state.aborted == (source.state.termination == 2)
        && source.state.panicked == (source.state.termination != 0)
        && source.principal.returned
            == (source.state.termination == 0 && source.state.terminal)
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
            termination: source.state.termination,
            panicked: source.state.panicked,
            aborted: source.state.aborted,
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
        && source.state.termination == refined.state.termination
        && source.state.panicked == refined.state.panicked
        && source.state.aborted == refined.state.aborted
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

pub proof fn runtime_key_projects_to_contract(
    boundary: KeyOrdDropBoundary,
    state: int,
    value: int,
)
    requires
        admissible_boundary(boundary),
    ensures
        observed_key_result(boundary, state, value)
            == observed_contract_key(boundary, value),
{
}

pub proof fn runtime_ord_projects_to_contract(
    boundary: KeyOrdDropBoundary,
    state: int,
    left: OwnedKey,
    right: OwnedKey,
)
    requires
        admissible_boundary(boundary),
    ensures
        observed_ord_lt(boundary, state, left, right)
            == (observed_contract_ordering(
                boundary,
                left.key_identity,
                right.key_identity,
            ) == -1),
{
}

pub proof fn total_state_effects_are_functional(
    first: KeyOrdDropBoundary,
    second: KeyOrdDropBoundary,
    state: int,
    value: int,
    left: OwnedKey,
    right: OwnedKey,
)
    requires
        first.key_next_state == second.key_next_state,
        first.key_panics == second.key_panics,
        first.ord_lt_next_state == second.ord_lt_next_state,
        first.ord_lt_panics == second.ord_lt_panics,
        first.drop_next_state == second.drop_next_state,
        first.drop_panics == second.drop_panics,
    ensures
        observed_key_next_state(first, state, value)
            == observed_key_next_state(second, state, value),
        observed_key_panic(first, state, value)
            == observed_key_panic(second, state, value),
        observed_ord_next_state(first, state, left, right)
            == observed_ord_next_state(second, state, left, right),
        observed_ord_panic(first, state, left, right)
            == observed_ord_panic(second, state, left, right),
        observed_drop_next_state(first, state, left)
            == observed_drop_next_state(second, state, left),
        observed_drop_panic(first, state, left)
            == observed_drop_panic(second, state, left),
{
}

pub proof fn owned_key_slots_are_distinct(
    state: int,
    source_identity: int,
    key_identity: int,
)
    ensures
        left_owned_key(state, source_identity, key_identity)
            != right_owned_key(state, source_identity, key_identity),
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
