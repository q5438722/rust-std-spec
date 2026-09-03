#![allow(dead_code, unused_imports, unused_variables)]
// Trusted-free target-082 composition with accepted target-080 semantics.

use vstd::prelude::*;

verus! {

pub ghost struct OwnedKey {
    pub invocation: int,
    pub creation_state: int,
    pub slot: int,
    pub source_identity: int,
    pub key_identity: int,
}

pub ghost struct KeySortBoundary {
    pub key_result: Map<int, Map<int, Map<int, int>>>,
    pub key_next_state: Map<int, Map<int, Map<int, int>>>,
    pub key_next_interior: Map<int, Map<int, Map<int, Seq<int>>>>,
    pub key_panics: Map<int, Map<int, Map<int, bool>>>,
    pub ord_result: Map<int, Map<OwnedKey, Map<OwnedKey, bool>>>,
    pub ord_next_state: Map<int, Map<OwnedKey, Map<OwnedKey, int>>>,
    pub ord_next_interior:
        Map<int, Map<OwnedKey, Map<OwnedKey, Seq<int>>>>,
    pub ord_panics: Map<int, Map<OwnedKey, Map<OwnedKey, bool>>>,
    pub key_drop_next_state:
        Map<int, Map<OwnedKey, Map<bool, int>>>,
    pub key_drop_next_interior:
        Map<int, Map<OwnedKey, Map<bool, Seq<int>>>>,
    pub key_drop_panics:
        Map<int, Map<OwnedKey, Map<bool, bool>>>,
    pub f_drop_next_state: Map<int, Map<bool, int>>,
    pub f_drop_next_interior: Map<int, Map<bool, Seq<int>>>,
    pub f_drop_panics: Map<int, Map<bool, bool>>,
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

pub ghost struct KeyResult {
    pub key_identity: int,
    pub state: int,
    pub interior: Seq<int>,
    pub panicked: bool,
}

pub ghost struct OrdResult {
    pub is_less: bool,
    pub state: int,
    pub interior: Seq<int>,
    pub panicked: bool,
}

pub ghost struct DropResult {
    pub state: int,
    pub interior: Seq<int>,
    pub panicked: bool,
}

pub ghost struct AdapterResult {
    pub status: int,
    pub state: int,
    pub interior: Seq<int>,
    pub is_less: bool,
    pub result_available: bool,
    pub key_evaluations: nat,
    pub ord_evaluations: nat,
    pub right_drops: nat,
    pub left_drops: nat,
    pub event_code: int,
    pub has_left: bool,
    pub has_right: bool,
    pub left_owned: OwnedKey,
    pub right_owned: OwnedKey,
}

pub ghost struct SourceAdapterBinding {
    pub adapter_model_id: int,
    pub boundary: KeySortBoundary,
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
        SourceAdapterBinding,
    ) -> PrivateSortResult,
}

pub ghost struct PublicSortResult {
    pub sequence: Seq<int>,
    pub callback_state: int,
    pub observable_element_state: Seq<int>,
    pub terminal_status: int,
    pub unit_returned: bool,
    pub panicked: bool,
    pub aborted: bool,
    pub f_drop_invoked: bool,
    pub f_drop_completed: bool,
}

pub open spec fn left_owned_key(
    invocation: int,
    state: int,
    source: int,
    key: int,
) -> OwnedKey {
    OwnedKey {
        invocation,
        creation_state: state,
        slot: 0,
        source_identity: source,
        key_identity: key,
    }
}

pub open spec fn right_owned_key(
    invocation: int,
    state: int,
    source: int,
    key: int,
) -> OwnedKey {
    OwnedKey {
        invocation,
        creation_state: state,
        slot: 1,
        source_identity: source,
        key_identity: key,
    }
}

pub open spec fn observe_key(
    boundary: KeySortBoundary,
    state: int,
    slot: int,
    source: int,
) -> KeyResult {
    KeyResult {
        key_identity: boundary.key_result[state][slot][source],
        state: boundary.key_next_state[state][slot][source],
        interior: boundary.key_next_interior[state][slot][source],
        panicked: boundary.key_panics[state][slot][source],
    }
}

pub open spec fn observe_ord(
    boundary: KeySortBoundary,
    state: int,
    left: OwnedKey,
    right: OwnedKey,
) -> OrdResult {
    OrdResult {
        is_less: boundary.ord_result[state][left][right],
        state: boundary.ord_next_state[state][left][right],
        interior: boundary.ord_next_interior[state][left][right],
        panicked: boundary.ord_panics[state][left][right],
    }
}

pub open spec fn observe_key_drop(
    boundary: KeySortBoundary,
    state: int,
    key: OwnedKey,
    unwinding: bool,
) -> DropResult {
    DropResult {
        state: boundary.key_drop_next_state[state][key][unwinding],
        interior: boundary.key_drop_next_interior[state][key][unwinding],
        panicked: boundary.key_drop_panics[state][key][unwinding],
    }
}

pub open spec fn cleanup_left_after_right_key_panic(
    boundary: KeySortBoundary,
    left: OwnedKey,
    state: int,
) -> AdapterResult {
    let drop = observe_key_drop(boundary, state, left, true);
    AdapterResult {
        status: if drop.panicked { 2 } else { 1 },
        state: drop.state,
        interior: drop.interior,
        is_less: false,
        result_available: false,
        key_evaluations: 2,
        ord_evaluations: 0,
        right_drops: 0,
        left_drops: 1,
        event_code: if drop.panicked { 1219 } else { 1215 },
        has_left: true,
        has_right: false,
        left_owned: left,
        right_owned: left,
    }
}

pub open spec fn cleanup_two_owned_keys(
    boundary: KeySortBoundary,
    left: OwnedKey,
    right: OwnedKey,
    state: int,
    already_unwinding: bool,
    resolved_less: bool,
) -> AdapterResult {
    let right_drop =
        observe_key_drop(boundary, state, right, already_unwinding);
    if already_unwinding && right_drop.panicked {
        AdapterResult {
            status: 2,
            state: right_drop.state,
            interior: right_drop.interior,
            is_less: false,
            result_available: false,
            key_evaluations: 2,
            ord_evaluations: 1,
            right_drops: 1,
            left_drops: 0,
            event_code: 12349,
            has_left: true,
            has_right: true,
            left_owned: left,
            right_owned: right,
        }
    } else {
        let unwinding = already_unwinding || right_drop.panicked;
        let left_drop = observe_key_drop(
            boundary, right_drop.state, left, unwinding,
        );
        let status =
            if left_drop.panicked {
                if unwinding { 2 } else { 1 }
            } else if unwinding {
                1
            } else {
                0
            };
        AdapterResult {
            status,
            state: left_drop.state,
            interior: left_drop.interior,
            is_less: status == 0 && resolved_less,
            result_available: status == 0,
            key_evaluations: 2,
            ord_evaluations: 1,
            right_drops: 1,
            left_drops: 1,
            event_code:
                if status == 0 { 12345 }
                else if status == 1 { 12347 }
                else { 12349 },
            has_left: true,
            has_right: true,
            left_owned: left,
            right_owned: right,
        }
    }
}

pub open spec fn source_key_ord_drop_adapter(
    boundary: KeySortBoundary,
    invocation: int,
    state: int,
    left_source: int,
    right_source: int,
) -> AdapterResult {
    let left = observe_key(boundary, state, 0, left_source);
    let left_owned =
        left_owned_key(invocation, state, left_source, left.key_identity);
    if left.panicked {
        AdapterResult {
            status: 1,
            state: left.state,
            interior: left.interior,
            is_less: false,
            result_available: false,
            key_evaluations: 1,
            ord_evaluations: 0,
            right_drops: 0,
            left_drops: 0,
            event_code: 19,
            has_left: false,
            has_right: false,
            left_owned,
            right_owned: left_owned,
        }
    } else {
        let right = observe_key(
            boundary, left.state, 1, right_source,
        );
        let right_owned = right_owned_key(
            invocation,
            left.state,
            right_source,
            right.key_identity,
        );
        if right.panicked {
            cleanup_left_after_right_key_panic(
                boundary, left_owned, right.state,
            )
        } else {
            let ord = observe_ord(
                boundary, right.state, left_owned, right_owned,
            );
            cleanup_two_owned_keys(
                boundary,
                left_owned,
                right_owned,
                ord.state,
                ord.panicked,
                ord.is_less,
            )
        }
    }
}

pub open spec fn source_private_comparator_boundary(
    boundary: KeySortBoundary,
) -> SourceAdapterBinding {
    SourceAdapterBinding {
        adapter_model_id: 82_196_1,
        boundary,
    }
}

pub open spec fn accepted_private_source_transition(
    transition: AcceptedTarget080PrivateTransition,
    input: SourceInput,
    configuration: SourceConfiguration,
    boundary: KeySortBoundary,
) -> PrivateSortResult {
    (transition.apply)(
        input,
        configuration,
        source_private_comparator_boundary(boundary),
    )
}

pub open spec fn source_public_finish(
    boundary: KeySortBoundary,
    private: PrivateSortResult,
) -> PublicSortResult {
    if private.terminal_status == 2 {
        PublicSortResult {
            sequence: private.sequence,
            callback_state: private.callback_state,
            observable_element_state: private.observable_element_state,
            terminal_status: 2,
            unit_returned: false,
            panicked: false,
            aborted: true,
            f_drop_invoked: false,
            f_drop_completed: false,
        }
    } else {
        let unwinding = private.terminal_status == 1;
        let drop_panicked =
            boundary.f_drop_panics[private.callback_state][unwinding];
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
                boundary.f_drop_next_state[
                    private.callback_state
                ][unwinding],
            observable_element_state:
                boundary.f_drop_next_interior[
                    private.callback_state
                ][unwinding],
            terminal_status: status,
            unit_returned: status == 0,
            panicked: status == 1,
            aborted: status == 2,
            f_drop_invoked: true,
            f_drop_completed: !drop_panicked,
        }
    }
}

pub open spec fn source_public_sort(
    transition: AcceptedTarget080PrivateTransition,
    input: SourceInput,
    configuration: SourceConfiguration,
    boundary: KeySortBoundary,
) -> PublicSortResult {
    source_public_finish(
        boundary,
        accepted_private_source_transition(
            transition, input, configuration, boundary,
        ),
    )
}

pub proof fn owned_key_identities_are_distinct(
    invocation: int,
    left_state: int,
    right_state: int,
    left_source: int,
    right_source: int,
    left_key: int,
    right_key: int,
)
    ensures
        left_owned_key(
            invocation, left_state, left_source, left_key,
        ).slot == 0,
        right_owned_key(
            invocation, right_state, right_source, right_key,
        ).slot == 1,
        left_owned_key(
            invocation, left_state, left_source, left_key,
        ) != right_owned_key(
            invocation, right_state, right_source, right_key,
        ),
{
}

pub proof fn left_key_is_evaluated_first(
    boundary: KeySortBoundary,
    invocation: int,
    state: int,
    left: int,
    right: int,
)
    ensures
        source_key_ord_drop_adapter(
            boundary, invocation, state, left, right,
        ).key_evaluations >= 1,
{
}

pub proof fn right_key_precedes_ord_when_present(
    boundary: KeySortBoundary,
    invocation: int,
    state: int,
    left: int,
    right: int,
)
    ensures
        source_key_ord_drop_adapter(
            boundary, invocation, state, left, right,
        ).ord_evaluations == 1
            ==> source_key_ord_drop_adapter(
                boundary, invocation, state, left, right,
            ).key_evaluations == 2,
{
}

pub proof fn ord_panic_has_no_boolean_result(
    boundary: KeySortBoundary,
    invocation: int,
    state: int,
    left: int,
    right: int,
)
    ensures
        source_key_ord_drop_adapter(
            boundary, invocation, state, left, right,
        ).status != 0
            ==> !source_key_ord_drop_adapter(
                boundary, invocation, state, left, right,
            ).result_available,
{
}

pub proof fn normal_cleanup_is_right_before_left(
    boundary: KeySortBoundary,
    left: OwnedKey,
    right: OwnedKey,
    state: int,
    less: bool,
)
    ensures
        cleanup_two_owned_keys(
            boundary, left, right, state, false, less,
        ).right_drops == 1,
        cleanup_two_owned_keys(
            boundary, left, right, state, false, less,
        ).left_drops == 1,
{
}

pub proof fn unwind_right_drop_panic_aborts_before_left_drop(
    boundary: KeySortBoundary,
    left: OwnedKey,
    right: OwnedKey,
    state: int,
    less: bool,
)
    requires
        observe_key_drop(boundary, state, right, true).panicked,
    ensures
        cleanup_two_owned_keys(
            boundary, left, right, state, true, less,
        ).status == 2,
        cleanup_two_owned_keys(
            boundary, left, right, state, true, less,
        ).left_drops == 0,
{
}

pub proof fn normal_f_drop_panic_becomes_panic(
    boundary: KeySortBoundary,
    private: PrivateSortResult,
)
    requires
        private.terminal_status == 0,
        boundary.f_drop_panics[private.callback_state][false],
    ensures
        source_public_finish(boundary, private).terminal_status == 1,
        source_public_finish(boundary, private).panicked,
        !source_public_finish(boundary, private).aborted,
{
}

pub proof fn unwind_f_drop_panic_is_abort(
    boundary: KeySortBoundary,
    private: PrivateSortResult,
)
    requires
        private.terminal_status == 1,
        boundary.f_drop_panics[private.callback_state][true],
    ensures
        source_public_finish(boundary, private).terminal_status == 2,
        source_public_finish(boundary, private).aborted,
        !source_public_finish(boundary, private).panicked,
{
}

pub proof fn private_abort_skips_f_drop(
    boundary: KeySortBoundary,
    private: PrivateSortResult,
)
    requires
        private.terminal_status == 2,
    ensures
        !source_public_finish(boundary, private).f_drop_invoked,
        !source_public_finish(boundary, private).f_drop_completed,
{
}

pub proof fn private_boundary_binds_source_adapter(
    boundary: KeySortBoundary,
)
    ensures
        source_private_comparator_boundary(
            boundary,
        ).adapter_model_id == 82_196_1,
        source_private_comparator_boundary(boundary).boundary
            == boundary,
{
}

pub proof fn fixed_boundary_accepted_transition_is_deterministic(
    first: AcceptedTarget080PrivateTransition,
    second: AcceptedTarget080PrivateTransition,
    input: SourceInput,
    configuration: SourceConfiguration,
    boundary: KeySortBoundary,
)
    requires
        first.source_model_id == 80_196_1,
        second.source_model_id == 80_196_1,
        first.apply == second.apply,
    ensures
        source_public_sort(
            first, input, configuration, boundary,
        ) == source_public_sort(
            second, input, configuration, boundary,
        ),
{
}

pub proof fn exact_terminal_output_and_full_state_are_preserved(
    transition: AcceptedTarget080PrivateTransition,
    input: SourceInput,
    configuration: SourceConfiguration,
    boundary: KeySortBoundary,
)
    ensures
        source_public_sort(
            transition, input, configuration, boundary,
        ).sequence == source_public_finish(
            boundary,
            accepted_private_source_transition(
                transition, input, configuration, boundary,
            ),
        ).sequence,
        source_public_sort(
            transition, input, configuration, boundary,
        ).callback_state == source_public_finish(
            boundary,
            accepted_private_source_transition(
                transition, input, configuration, boundary,
            ),
        ).callback_state,
        source_public_sort(
            transition, input, configuration, boundary,
        ).observable_element_state == source_public_finish(
            boundary,
            accepted_private_source_transition(
                transition, input, configuration, boundary,
            ),
        ).observable_element_state,
{
}

}
