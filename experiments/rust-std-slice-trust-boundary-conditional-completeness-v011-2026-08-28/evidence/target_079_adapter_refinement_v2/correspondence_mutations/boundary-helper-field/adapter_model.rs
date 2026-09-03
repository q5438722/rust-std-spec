#![allow(dead_code, unused_imports, unused_variables)]
// Constructive refinement of the target-079 key/Ord/Drop adapter.

use vstd::prelude::*;

verus! {

pub ghost struct OwnedKey {
    pub owned_creation_state: int,
    pub owned_slot: int,
    pub owned_source_identity: int,
    pub owned_key_identity: int,
}

pub ghost struct KeyOrdDropBoundary {
    pub b_callback_identity: int,
    pub b_key_function_identity: int,
    pub b_ord_function_identity: int,
    pub b_drop_function_identity: int,
    pub b_initial_state: int,
    pub b_contract_key: Map<int, int>,
    pub b_contract_ordering: Map<int, Map<int, int>>,
    pub b_key_result: Map<int, Map<int, int>>,
    pub b_key_next_state: Map<int, Map<int, int>>,
    pub b_key_panics: Map<int, Map<int, bool>>,
    pub b_ord_lt_result: Map<int, Map<OwnedKey, Map<OwnedKey, bool>>>,
    pub b_ord_lt_next_state: Map<int, Map<OwnedKey, Map<OwnedKey, int>>>,
    pub b_ord_lt_panics: Map<int, Map<OwnedKey, Map<OwnedKey, bool>>>,
    pub b_drop_next_state: Map<int, Map<OwnedKey, int>>,
    pub b_drop_panics: Map<int, Map<OwnedKey, bool>>,
}

pub ghost struct AdapterFrame {
    pub af_state: int,
    pub af_termination: int,
    pub af_is_less: bool,
    pub af_panic_origin: int,
    pub af_left_owned: OwnedKey,
    pub af_right_owned: OwnedKey,
    pub af_left_live: bool,
    pub af_right_live: bool,
}

pub open spec fn key_result(
    boundary: KeyOrdDropBoundary,
    state: int,
    value: int,
) -> int {
    boundary.b_key_next_state[state][value]
}

pub open spec fn key_next_state(
    boundary: KeyOrdDropBoundary,
    state: int,
    value: int,
) -> int {
    boundary.b_key_next_state[state][value]
}

pub open spec fn key_panics(
    boundary: KeyOrdDropBoundary,
    state: int,
    value: int,
) -> bool {
    boundary.b_key_panics[state][value]
}

pub open spec fn ord_lt_result(
    boundary: KeyOrdDropBoundary,
    state: int,
    left: OwnedKey,
    right: OwnedKey,
) -> bool {
    boundary.b_ord_lt_result[state][left][right]
}

pub open spec fn ord_lt_next_state(
    boundary: KeyOrdDropBoundary,
    state: int,
    left: OwnedKey,
    right: OwnedKey,
) -> int {
    boundary.b_ord_lt_next_state[state][left][right]
}

pub open spec fn ord_lt_panics(
    boundary: KeyOrdDropBoundary,
    state: int,
    left: OwnedKey,
    right: OwnedKey,
) -> bool {
    boundary.b_ord_lt_panics[state][left][right]
}

pub open spec fn drop_next_state(
    boundary: KeyOrdDropBoundary,
    state: int,
    key: OwnedKey,
) -> int {
    boundary.b_drop_next_state[state][key]
}

pub open spec fn drop_panics(
    boundary: KeyOrdDropBoundary,
    state: int,
    key: OwnedKey,
) -> bool {
    boundary.b_drop_panics[state][key]
}

pub open spec fn owned_key(
    creation_state: int,
    slot: int,
    source_identity: int,
    key_identity: int,
) -> OwnedKey {
    OwnedKey {
        owned_creation_state: creation_state,
        owned_slot: slot,
        owned_source_identity: source_identity,
        owned_key_identity: key_identity,
    }
}

pub open spec fn adapter_initial(state: int) -> AdapterFrame {
    AdapterFrame {
        af_state: state,
        af_termination: 0,
        af_is_less: false,
        af_panic_origin: 0,
        af_left_owned: owned_key(0, 0, 0, 0),
        af_right_owned: owned_key(0, 1, 0, 0),
        af_left_live: false,
        af_right_live: false,
    }
}

pub open spec fn adapter_key_left(
    frame: AdapterFrame,
    boundary: KeyOrdDropBoundary,
    left: int,
) -> AdapterFrame {
    if frame.af_termination == 0 {
        let state = frame.af_state;
        let key = key_result(boundary, state, left);
        let next = key_next_state(boundary, state, left);
        let panics = key_panics(boundary, state, left);
        AdapterFrame {
            af_state: next,
            af_termination: if panics { 1 } else { 0 },
            af_is_less: false,
            af_panic_origin: if panics { 1 } else { 0 },
            af_left_owned: owned_key(state, 0, left, key),
            af_right_owned: frame.af_right_owned,
            af_left_live: !panics,
            af_right_live: false,
        }
    } else {
        frame
    }
}

pub open spec fn adapter_key_right(
    frame: AdapterFrame,
    boundary: KeyOrdDropBoundary,
    right: int,
) -> AdapterFrame {
    if frame.af_termination == 0 {
        let state = frame.af_state;
        let key = key_result(boundary, state, right);
        let next = key_next_state(boundary, state, right);
        let panics = key_panics(boundary, state, right);
        AdapterFrame {
            af_state: next,
            af_termination: if panics { 1 } else { 0 },
            af_is_less: false,
            af_panic_origin: if panics { 2 } else { 0 },
            af_left_owned: frame.af_left_owned,
            af_right_owned: owned_key(state, 1, right, key),
            af_left_live: frame.af_left_live,
            af_right_live: !panics,
        }
    } else {
        frame
    }
}

pub open spec fn adapter_ord_lt(
    frame: AdapterFrame,
    boundary: KeyOrdDropBoundary,
) -> AdapterFrame {
    if frame.af_termination == 0 {
        let state = frame.af_state;
        let left = frame.af_left_owned;
        let right = frame.af_right_owned;
        let less = ord_lt_result(boundary, state, left, right);
        let next = ord_lt_next_state(boundary, state, left, right);
        let panics = ord_lt_panics(boundary, state, left, right);
        AdapterFrame {
            af_state: next,
            af_termination: if panics { 1 } else { 0 },
            af_is_less: less,
            af_panic_origin: if panics { 3 } else { 0 },
            af_left_owned: left,
            af_right_owned: right,
            af_left_live: frame.af_left_live,
            af_right_live: frame.af_right_live,
        }
    } else {
        frame
    }
}

pub open spec fn adapter_drop_right(
    frame: AdapterFrame,
    boundary: KeyOrdDropBoundary,
) -> AdapterFrame {
    if frame.af_right_live && frame.af_termination != 2 {
        let state = frame.af_state;
        let key = frame.af_right_owned;
        let old_termination = frame.af_termination;
        let next = drop_next_state(boundary, state, key);
        let panics = drop_panics(boundary, state, key);
        AdapterFrame {
            af_state: next,
            af_termination: if panics {
                if old_termination == 1 { 2 } else { 1 }
            } else {
                old_termination
            },
            af_is_less: frame.af_is_less,
            af_panic_origin: if panics {
                4
            } else {
                frame.af_panic_origin
            },
            af_left_owned: frame.af_left_owned,
            af_right_owned: key,
            af_left_live: frame.af_left_live,
            af_right_live: false,
        }
    } else {
        frame
    }
}

pub open spec fn adapter_drop_left(
    frame: AdapterFrame,
    boundary: KeyOrdDropBoundary,
) -> AdapterFrame {
    if frame.af_left_live && frame.af_termination != 2 {
        let state = frame.af_state;
        let key = frame.af_left_owned;
        let old_termination = frame.af_termination;
        let next = drop_next_state(boundary, state, key);
        let panics = drop_panics(boundary, state, key);
        AdapterFrame {
            af_state: next,
            af_termination: if panics {
                if old_termination == 1 { 2 } else { 1 }
            } else {
                old_termination
            },
            af_is_less: frame.af_is_less,
            af_panic_origin: if panics {
                5
            } else {
                frame.af_panic_origin
            },
            af_left_owned: key,
            af_right_owned: frame.af_right_owned,
            af_left_live: false,
            af_right_live: frame.af_right_live,
        }
    } else {
        frame
    }
}

pub open spec fn frame_after_key_left(
    boundary: KeyOrdDropBoundary,
    state: int,
    left: int,
) -> AdapterFrame {
    adapter_key_left(adapter_initial(state), boundary, left)
}

pub open spec fn frame_after_key_right(
    boundary: KeyOrdDropBoundary,
    state: int,
    left: int,
    right: int,
) -> AdapterFrame {
    adapter_key_right(
        frame_after_key_left(boundary, state, left),
        boundary,
        right,
    )
}

pub open spec fn frame_after_ord_lt(
    boundary: KeyOrdDropBoundary,
    state: int,
    left: int,
    right: int,
) -> AdapterFrame {
    adapter_ord_lt(
        frame_after_key_right(boundary, state, left, right),
        boundary,
    )
}

pub open spec fn frame_after_drop_right(
    boundary: KeyOrdDropBoundary,
    state: int,
    left: int,
    right: int,
) -> AdapterFrame {
    adapter_drop_right(
        frame_after_ord_lt(boundary, state, left, right),
        boundary,
    )
}

pub open spec fn adapter_transition(
    boundary: KeyOrdDropBoundary,
    state: int,
    left: int,
    right: int,
) -> AdapterFrame {
    adapter_drop_left(
        frame_after_drop_right(boundary, state, left, right),
        boundary,
    )
}

pub open spec fn left_state(
    boundary: KeyOrdDropBoundary,
    state: int,
    left: int,
) -> int {
    key_next_state(boundary, state, left)
}

pub open spec fn left_owned(
    boundary: KeyOrdDropBoundary,
    state: int,
    left: int,
) -> OwnedKey {
    owned_key(state, 0, left, key_result(boundary, state, left))
}

pub open spec fn right_state(
    boundary: KeyOrdDropBoundary,
    state: int,
    left: int,
    right: int,
) -> int {
    key_next_state(boundary, left_state(boundary, state, left), right)
}

pub open spec fn right_owned(
    boundary: KeyOrdDropBoundary,
    state: int,
    left: int,
    right: int,
) -> OwnedKey {
    owned_key(
        left_state(boundary, state, left),
        1,
        right,
        key_result(boundary, left_state(boundary, state, left), right),
    )
}

pub open spec fn ord_state(
    boundary: KeyOrdDropBoundary,
    state: int,
    left: int,
    right: int,
) -> int {
    ord_lt_next_state(
        boundary,
        right_state(boundary, state, left, right),
        left_owned(boundary, state, left),
        right_owned(boundary, state, left, right),
    )
}

pub open spec fn right_drop_state(
    boundary: KeyOrdDropBoundary,
    state: int,
    left: int,
    right: int,
) -> int {
    drop_next_state(
        boundary,
        ord_state(boundary, state, left, right),
        right_owned(boundary, state, left, right),
    )
}

pub open spec fn left_drop_state(
    boundary: KeyOrdDropBoundary,
    state: int,
    left: int,
    right: int,
) -> int {
    drop_next_state(
        boundary,
        right_drop_state(boundary, state, left, right),
        left_owned(boundary, state, left),
    )
}

pub proof fn transition_is_the_smt_constructor_chain(
    boundary: KeyOrdDropBoundary,
    state: int,
    left: int,
    right: int,
)
    ensures
        adapter_transition(boundary, state, left, right)
            == adapter_drop_left(
                adapter_drop_right(
                    adapter_ord_lt(
                        adapter_key_right(
                            adapter_key_left(
                                adapter_initial(state),
                                boundary,
                                left,
                            ),
                            boundary,
                            right,
                        ),
                        boundary,
                    ),
                    boundary,
                ),
                boundary,
            ),
{
}

pub proof fn owned_key_identity_tracks_creation_slot_and_source(
    boundary: KeyOrdDropBoundary,
    state: int,
    left: int,
    right: int,
)
    ensures
        left_owned(boundary, state, left).owned_creation_state == state,
        left_owned(boundary, state, left).owned_slot == 0,
        left_owned(boundary, state, left).owned_source_identity == left,
        left_owned(boundary, state, left).owned_key_identity
            == key_result(boundary, state, left),
        right_owned(boundary, state, left, right).owned_creation_state
            == left_state(boundary, state, left),
        right_owned(boundary, state, left, right).owned_slot == 1,
        right_owned(boundary, state, left, right).owned_source_identity
            == right,
        right_owned(boundary, state, left, right).owned_key_identity
            == key_result(
                boundary,
                left_state(boundary, state, left),
                right,
            ),
        left_owned(boundary, state, left)
            != right_owned(boundary, state, left, right),
{
}

pub proof fn normal_execution_threads_all_callback_states(
    boundary: KeyOrdDropBoundary,
    state: int,
    left: int,
    right: int,
)
    requires
        !key_panics(boundary, state, left),
        !key_panics(
            boundary,
            left_state(boundary, state, left),
            right,
        ),
        !ord_lt_panics(
            boundary,
            right_state(boundary, state, left, right),
            left_owned(boundary, state, left),
            right_owned(boundary, state, left, right),
        ),
        !drop_panics(
            boundary,
            ord_state(boundary, state, left, right),
            right_owned(boundary, state, left, right),
        ),
        !drop_panics(
            boundary,
            right_drop_state(boundary, state, left, right),
            left_owned(boundary, state, left),
        ),
    ensures
        frame_after_key_left(boundary, state, left).af_state
            == left_state(boundary, state, left),
        frame_after_key_right(boundary, state, left, right).af_state
            == right_state(boundary, state, left, right),
        frame_after_ord_lt(boundary, state, left, right).af_state
            == ord_state(boundary, state, left, right),
        frame_after_drop_right(boundary, state, left, right).af_state
            == right_drop_state(boundary, state, left, right),
        adapter_transition(boundary, state, left, right).af_state
            == left_drop_state(boundary, state, left, right),
        adapter_transition(boundary, state, left, right).af_termination
            == 0,
        adapter_transition(boundary, state, left, right).af_is_less
            == ord_lt_result(
                boundary,
                right_state(boundary, state, left, right),
                left_owned(boundary, state, left),
                right_owned(boundary, state, left, right),
            ),
        adapter_transition(boundary, state, left, right).af_panic_origin
            == 0,
        !adapter_transition(boundary, state, left, right).af_left_live,
        !adapter_transition(boundary, state, left, right).af_right_live,
{
}

pub proof fn first_key_panic_stops_before_owned_cleanup(
    boundary: KeyOrdDropBoundary,
    state: int,
    left: int,
    right: int,
)
    requires
        key_panics(boundary, state, left),
    ensures
        adapter_transition(boundary, state, left, right).af_state
            == left_state(boundary, state, left),
        adapter_transition(boundary, state, left, right).af_termination
            == 1,
        adapter_transition(boundary, state, left, right).af_panic_origin
            == 1,
        !adapter_transition(boundary, state, left, right).af_left_live,
        !adapter_transition(boundary, state, left, right).af_right_live,
{
}

pub proof fn second_key_panic_cleans_up_only_left(
    boundary: KeyOrdDropBoundary,
    state: int,
    left: int,
    right: int,
)
    requires
        !key_panics(boundary, state, left),
        key_panics(
            boundary,
            left_state(boundary, state, left),
            right,
        ),
        !drop_panics(
            boundary,
            right_state(boundary, state, left, right),
            left_owned(boundary, state, left),
        ),
    ensures
        adapter_transition(boundary, state, left, right).af_state
            == drop_next_state(
                boundary,
                right_state(boundary, state, left, right),
                left_owned(boundary, state, left),
            ),
        adapter_transition(boundary, state, left, right).af_termination
            == 1,
        adapter_transition(boundary, state, left, right).af_panic_origin
            == 2,
        adapter_transition(boundary, state, left, right).af_left_owned
            == left_owned(boundary, state, left),
        !adapter_transition(boundary, state, left, right).af_left_live,
        !adapter_transition(boundary, state, left, right).af_right_live,
{
}

pub proof fn second_key_panic_and_left_destructor_panic_aborts(
    boundary: KeyOrdDropBoundary,
    state: int,
    left: int,
    right: int,
)
    requires
        !key_panics(boundary, state, left),
        key_panics(
            boundary,
            left_state(boundary, state, left),
            right,
        ),
        drop_panics(
            boundary,
            right_state(boundary, state, left, right),
            left_owned(boundary, state, left),
        ),
    ensures
        adapter_transition(boundary, state, left, right).af_state
            == drop_next_state(
                boundary,
                right_state(boundary, state, left, right),
                left_owned(boundary, state, left),
            ),
        adapter_transition(boundary, state, left, right).af_termination
            == 2,
        adapter_transition(boundary, state, left, right).af_panic_origin
            == 5,
        !adapter_transition(boundary, state, left, right).af_left_live,
        !adapter_transition(boundary, state, left, right).af_right_live,
{
}

pub proof fn ord_panic_cleans_right_then_left(
    boundary: KeyOrdDropBoundary,
    state: int,
    left: int,
    right: int,
)
    requires
        !key_panics(boundary, state, left),
        !key_panics(
            boundary,
            left_state(boundary, state, left),
            right,
        ),
        ord_lt_panics(
            boundary,
            right_state(boundary, state, left, right),
            left_owned(boundary, state, left),
            right_owned(boundary, state, left, right),
        ),
        !drop_panics(
            boundary,
            ord_state(boundary, state, left, right),
            right_owned(boundary, state, left, right),
        ),
        !drop_panics(
            boundary,
            right_drop_state(boundary, state, left, right),
            left_owned(boundary, state, left),
        ),
    ensures
        frame_after_drop_right(boundary, state, left, right).af_state
            == right_drop_state(boundary, state, left, right),
        frame_after_drop_right(boundary, state, left, right).af_left_live,
        !frame_after_drop_right(boundary, state, left, right).af_right_live,
        adapter_transition(boundary, state, left, right).af_state
            == left_drop_state(boundary, state, left, right),
        adapter_transition(boundary, state, left, right).af_termination
            == 1,
        adapter_transition(boundary, state, left, right).af_panic_origin
            == 3,
        !adapter_transition(boundary, state, left, right).af_left_live,
        !adapter_transition(boundary, state, left, right).af_right_live,
{
}

pub proof fn ord_panic_and_right_destructor_panic_aborts_before_left(
    boundary: KeyOrdDropBoundary,
    state: int,
    left: int,
    right: int,
)
    requires
        !key_panics(boundary, state, left),
        !key_panics(
            boundary,
            left_state(boundary, state, left),
            right,
        ),
        ord_lt_panics(
            boundary,
            right_state(boundary, state, left, right),
            left_owned(boundary, state, left),
            right_owned(boundary, state, left, right),
        ),
        drop_panics(
            boundary,
            ord_state(boundary, state, left, right),
            right_owned(boundary, state, left, right),
        ),
    ensures
        adapter_transition(boundary, state, left, right).af_state
            == right_drop_state(boundary, state, left, right),
        adapter_transition(boundary, state, left, right).af_termination
            == 2,
        adapter_transition(boundary, state, left, right).af_panic_origin
            == 4,
        adapter_transition(boundary, state, left, right).af_left_live,
        !adapter_transition(boundary, state, left, right).af_right_live,
{
}

pub proof fn ord_panic_and_left_destructor_panic_after_right_cleanup_aborts(
    boundary: KeyOrdDropBoundary,
    state: int,
    left: int,
    right: int,
)
    requires
        !key_panics(boundary, state, left),
        !key_panics(
            boundary,
            left_state(boundary, state, left),
            right,
        ),
        ord_lt_panics(
            boundary,
            right_state(boundary, state, left, right),
            left_owned(boundary, state, left),
            right_owned(boundary, state, left, right),
        ),
        !drop_panics(
            boundary,
            ord_state(boundary, state, left, right),
            right_owned(boundary, state, left, right),
        ),
        drop_panics(
            boundary,
            right_drop_state(boundary, state, left, right),
            left_owned(boundary, state, left),
        ),
    ensures
        adapter_transition(boundary, state, left, right).af_state
            == left_drop_state(boundary, state, left, right),
        adapter_transition(boundary, state, left, right).af_termination
            == 2,
        adapter_transition(boundary, state, left, right).af_panic_origin
            == 5,
        !adapter_transition(boundary, state, left, right).af_left_live,
        !adapter_transition(boundary, state, left, right).af_right_live,
{
}

pub proof fn normal_right_destructor_panic_unwinds_left(
    boundary: KeyOrdDropBoundary,
    state: int,
    left: int,
    right: int,
)
    requires
        !key_panics(boundary, state, left),
        !key_panics(
            boundary,
            left_state(boundary, state, left),
            right,
        ),
        !ord_lt_panics(
            boundary,
            right_state(boundary, state, left, right),
            left_owned(boundary, state, left),
            right_owned(boundary, state, left, right),
        ),
        drop_panics(
            boundary,
            ord_state(boundary, state, left, right),
            right_owned(boundary, state, left, right),
        ),
        !drop_panics(
            boundary,
            right_drop_state(boundary, state, left, right),
            left_owned(boundary, state, left),
        ),
    ensures
        adapter_transition(boundary, state, left, right).af_state
            == left_drop_state(boundary, state, left, right),
        adapter_transition(boundary, state, left, right).af_termination
            == 1,
        adapter_transition(boundary, state, left, right).af_panic_origin
            == 4,
        !adapter_transition(boundary, state, left, right).af_left_live,
        !adapter_transition(boundary, state, left, right).af_right_live,
{
}

pub proof fn normal_right_and_unwind_left_destructor_panics_abort(
    boundary: KeyOrdDropBoundary,
    state: int,
    left: int,
    right: int,
)
    requires
        !key_panics(boundary, state, left),
        !key_panics(
            boundary,
            left_state(boundary, state, left),
            right,
        ),
        !ord_lt_panics(
            boundary,
            right_state(boundary, state, left, right),
            left_owned(boundary, state, left),
            right_owned(boundary, state, left, right),
        ),
        drop_panics(
            boundary,
            ord_state(boundary, state, left, right),
            right_owned(boundary, state, left, right),
        ),
        drop_panics(
            boundary,
            right_drop_state(boundary, state, left, right),
            left_owned(boundary, state, left),
        ),
    ensures
        adapter_transition(boundary, state, left, right).af_state
            == left_drop_state(boundary, state, left, right),
        adapter_transition(boundary, state, left, right).af_termination
            == 2,
        adapter_transition(boundary, state, left, right).af_panic_origin
            == 5,
        !adapter_transition(boundary, state, left, right).af_left_live,
        !adapter_transition(boundary, state, left, right).af_right_live,
{
}

pub proof fn normal_left_destructor_panic_is_single_panic(
    boundary: KeyOrdDropBoundary,
    state: int,
    left: int,
    right: int,
)
    requires
        !key_panics(boundary, state, left),
        !key_panics(
            boundary,
            left_state(boundary, state, left),
            right,
        ),
        !ord_lt_panics(
            boundary,
            right_state(boundary, state, left, right),
            left_owned(boundary, state, left),
            right_owned(boundary, state, left, right),
        ),
        !drop_panics(
            boundary,
            ord_state(boundary, state, left, right),
            right_owned(boundary, state, left, right),
        ),
        drop_panics(
            boundary,
            right_drop_state(boundary, state, left, right),
            left_owned(boundary, state, left),
        ),
    ensures
        adapter_transition(boundary, state, left, right).af_state
            == left_drop_state(boundary, state, left, right),
        adapter_transition(boundary, state, left, right).af_termination
            == 1,
        adapter_transition(boundary, state, left, right).af_panic_origin
            == 5,
        !adapter_transition(boundary, state, left, right).af_left_live,
        !adapter_transition(boundary, state, left, right).af_right_live,
{
}

pub proof fn initial_callback_state_is_the_transition_entry(
    boundary: KeyOrdDropBoundary,
    left: int,
    right: int,
)
    ensures
        adapter_transition(
            boundary,
            boundary.b_initial_state,
            left,
            right,
        ) == adapter_drop_left(
            frame_after_drop_right(
                boundary,
                boundary.b_initial_state,
                left,
                right,
            ),
            boundary,
        ),
{
}

}
