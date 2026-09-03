#![allow(dead_code, unused_imports, unused_variables)]
// Constructive composition of the accepted key/Ord/Drop adapter with
// Rust 1.96 insert_tail and CopyOnDrop.

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
    boundary.b_key_result[state][value]
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

pub open spec fn adapter_transition(
    boundary: KeyOrdDropBoundary,
    state: int,
    left: int,
    right: int,
) -> AdapterFrame {
    adapter_drop_left(
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
    )
}

pub ghost struct InsertTailState {
    pub e_sequence: Seq<int>,
    pub e_callback_state: int,
    pub e_panicked: bool,
    pub e_aborted: bool,
}

pub open spec fn callback_frame(
    state: InsertTailState,
    boundary: KeyOrdDropBoundary,
    left: int,
    right: int,
) -> AdapterFrame {
    adapter_transition(
        boundary,
        state.e_callback_state,
        left,
        right,
    )
}

pub open spec fn adapter_callback(
    state: InsertTailState,
    boundary: KeyOrdDropBoundary,
    left: int,
    right: int,
) -> InsertTailState {
    let frame = callback_frame(state, boundary, left, right);
    InsertTailState {
        e_sequence: state.e_sequence,
        e_callback_state: frame.af_state,
        e_panicked: frame.af_termination != 0,
        e_aborted: frame.af_termination == 2,
    }
}

pub open spec fn target_adapter_is_less(
    state: InsertTailState,
    boundary: KeyOrdDropBoundary,
    left: int,
    right: int,
) -> bool {
    callback_frame(state, boundary, left, right).af_left_live
}

pub open spec fn shifted_state(
    state: InsertTailState,
    sift: int,
    gap: int,
) -> InsertTailState {
    InsertTailState {
        e_sequence: state.e_sequence.update(
            gap,
            state.e_sequence[sift],
        ),
        e_callback_state: state.e_callback_state,
        e_panicked: false,
        e_aborted: false,
    }
}

pub open spec fn restored_state(
    state: InsertTailState,
    destination: int,
    temporary: int,
    panicked: bool,
) -> InsertTailState {
    if state.e_aborted {
        state
    } else {
        InsertTailState {
            e_sequence: state.e_sequence.update(destination, temporary),
            e_callback_state: state.e_callback_state,
            e_panicked: panicked,
            e_aborted: false,
        }
    }
}

pub open spec fn restored_sequence(
    state: InsertTailState,
    gap: int,
    temporary: int,
) -> Seq<int> {
    state.e_sequence.update(gap, temporary)
}

pub open spec fn valid_insert_tail_input(
    state: InsertTailState,
    begin: int,
    tail: int,
) -> bool {
    !state.e_panicked
        && !state.e_aborted
        && 0 <= begin
        && begin < tail
        && tail < state.e_sequence.len()
}

pub open spec fn valid_insert_tail_loop_input(
    state: InsertTailState,
    begin: int,
    sift: int,
    gap: int,
) -> bool {
    !state.e_panicked
        && !state.e_aborted
        && 0 <= begin
        && begin <= sift
        && gap == sift + 1
        && gap < state.e_sequence.len()
}

pub open spec fn insert_tail_loop(
    state: InsertTailState,
    boundary: KeyOrdDropBoundary,
    begin: int,
    sift: int,
    gap: int,
    temporary: int,
) -> InsertTailState
    decreases sift - begin,
{
    if state.e_panicked || state.e_aborted {
        state
    } else {
        let shifted = shifted_state(state, sift, gap);
        if sift <= begin {
            restored_state(shifted, sift, temporary, false)
        } else {
            let next_sift = sift - 1;
            let right = shifted.e_sequence[next_sift];
            let called = adapter_callback(
                shifted,
                boundary,
                temporary,
                right,
            );
            let less = target_adapter_is_less(
                shifted,
                boundary,
                temporary,
                right,
            );
            if called.e_panicked {
                restored_state(called, sift, temporary, true)
            } else if less {
                insert_tail_loop(
                    called,
                    boundary,
                    begin,
                    next_sift,
                    sift,
                    temporary,
                )
            } else {
                restored_state(called, sift, temporary, false)
            }
        }
    }
}

pub open spec fn insert_tail(
    state: InsertTailState,
    boundary: KeyOrdDropBoundary,
    begin: int,
    tail: int,
) -> InsertTailState {
    if state.e_panicked || state.e_aborted {
        state
    } else {
        let temporary = state.e_sequence[tail];
        let right = state.e_sequence[tail - 1];
        let called = adapter_callback(
            state,
            boundary,
            temporary,
            right,
        );
        let less = target_adapter_is_less(
            state,
            boundary,
            temporary,
            right,
        );
        if called.e_panicked {
            called
        } else if less {
            insert_tail_loop(
                called,
                boundary,
                begin,
                tail - 1,
                tail,
                temporary,
            )
        } else {
            called
        }
    }
}

pub proof fn callback_is_derived_from_adapter_transition(
    state: InsertTailState,
    boundary: KeyOrdDropBoundary,
    left: int,
    right: int,
)
    ensures
        adapter_callback(
            state,
            boundary,
            left,
            right,
        ).e_sequence == state.e_sequence,
        adapter_callback(
            state,
            boundary,
            left,
            right,
        ).e_callback_state
            == adapter_transition(
                boundary,
                state.e_callback_state,
                left,
                right,
            ).af_state,
        adapter_callback(
            state,
            boundary,
            left,
            right,
        ).e_panicked
            == (
                adapter_transition(
                    boundary,
                    state.e_callback_state,
                    left,
                    right,
                ).af_termination != 0
            ),
        adapter_callback(
            state,
            boundary,
            left,
            right,
        ).e_aborted
            == (
                adapter_transition(
                    boundary,
                    state.e_callback_state,
                    left,
                    right,
                ).af_termination == 2
            ),
{
}

pub proof fn initial_adapter_panic_precedes_gap_creation(
    state: InsertTailState,
    boundary: KeyOrdDropBoundary,
    begin: int,
    tail: int,
)
    requires
        valid_insert_tail_input(state, begin, tail),
        callback_frame(
            state,
            boundary,
            state.e_sequence[tail],
            state.e_sequence[tail - 1],
        ).af_termination == 1,
    ensures
        insert_tail(state, boundary, begin, tail)
            == adapter_callback(
                state,
                boundary,
                state.e_sequence[tail],
                state.e_sequence[tail - 1],
            ),
        insert_tail(state, boundary, begin, tail).e_sequence
            == state.e_sequence,
        insert_tail(state, boundary, begin, tail).e_panicked,
        !insert_tail(state, boundary, begin, tail).e_aborted,
{
}

pub proof fn initial_adapter_abort_precedes_gap_creation(
    state: InsertTailState,
    boundary: KeyOrdDropBoundary,
    begin: int,
    tail: int,
)
    requires
        valid_insert_tail_input(state, begin, tail),
        callback_frame(
            state,
            boundary,
            state.e_sequence[tail],
            state.e_sequence[tail - 1],
        ).af_termination == 2,
    ensures
        insert_tail(state, boundary, begin, tail)
            == adapter_callback(
                state,
                boundary,
                state.e_sequence[tail],
                state.e_sequence[tail - 1],
            ),
        insert_tail(state, boundary, begin, tail).e_sequence
            == state.e_sequence,
        insert_tail(state, boundary, begin, tail).e_panicked,
        insert_tail(state, boundary, begin, tail).e_aborted,
{
}

pub proof fn no_shift_path_is_exact(
    state: InsertTailState,
    boundary: KeyOrdDropBoundary,
    begin: int,
    tail: int,
)
    requires
        valid_insert_tail_input(state, begin, tail),
        callback_frame(
            state,
            boundary,
            state.e_sequence[tail],
            state.e_sequence[tail - 1],
        ).af_termination == 0,
        !target_adapter_is_less(
            state,
            boundary,
            state.e_sequence[tail],
            state.e_sequence[tail - 1],
        ),
    ensures
        insert_tail(state, boundary, begin, tail)
            == adapter_callback(
                state,
                boundary,
                state.e_sequence[tail],
                state.e_sequence[tail - 1],
            ),
        insert_tail(state, boundary, begin, tail).e_sequence
            == state.e_sequence,
        !insert_tail(state, boundary, begin, tail).e_panicked,
        !insert_tail(state, boundary, begin, tail).e_aborted,
{
}

pub proof fn initial_less_enters_loop_with_tail_gap(
    state: InsertTailState,
    boundary: KeyOrdDropBoundary,
    begin: int,
    tail: int,
)
    requires
        valid_insert_tail_input(state, begin, tail),
        callback_frame(
            state,
            boundary,
            state.e_sequence[tail],
            state.e_sequence[tail - 1],
        ).af_termination == 0,
        target_adapter_is_less(
            state,
            boundary,
            state.e_sequence[tail],
            state.e_sequence[tail - 1],
        ),
    ensures
        insert_tail(state, boundary, begin, tail)
            == insert_tail_loop(
                adapter_callback(
                    state,
                    boundary,
                    state.e_sequence[tail],
                    state.e_sequence[tail - 1],
                ),
                boundary,
                begin,
                tail - 1,
                tail,
                state.e_sequence[tail],
            ),
{
}

pub proof fn loop_at_begin_restores_temporary(
    state: InsertTailState,
    boundary: KeyOrdDropBoundary,
    begin: int,
    gap: int,
    temporary: int,
)
    requires
        valid_insert_tail_loop_input(state, begin, begin, gap),
    ensures
        insert_tail_loop(
            state,
            boundary,
            begin,
            begin,
            gap,
            temporary,
        )
            == restored_state(
                shifted_state(state, begin, gap),
                begin,
                temporary,
                false,
            ),
{
}

pub proof fn loop_normal_stop_restores_temporary(
    state: InsertTailState,
    boundary: KeyOrdDropBoundary,
    begin: int,
    sift: int,
    gap: int,
    temporary: int,
)
    requires
        valid_insert_tail_loop_input(state, begin, sift, gap),
        begin < sift,
        callback_frame(
            shifted_state(state, sift, gap),
            boundary,
            temporary,
            state.e_sequence[sift - 1],
        ).af_termination == 0,
        !target_adapter_is_less(
            shifted_state(state, sift, gap),
            boundary,
            temporary,
            state.e_sequence[sift - 1],
        ),
    ensures
        insert_tail_loop(
            state,
            boundary,
            begin,
            sift,
            gap,
            temporary,
        )
            == restored_state(
                adapter_callback(
                    shifted_state(state, sift, gap),
                    boundary,
                    temporary,
                    state.e_sequence[sift - 1],
                ),
                sift,
                temporary,
                false,
            ),
{
}

pub proof fn loop_ordinary_panic_restores_active_gap(
    state: InsertTailState,
    boundary: KeyOrdDropBoundary,
    begin: int,
    sift: int,
    gap: int,
    temporary: int,
)
    requires
        valid_insert_tail_loop_input(state, begin, sift, gap),
        begin < sift,
        callback_frame(
            shifted_state(state, sift, gap),
            boundary,
            temporary,
            state.e_sequence[sift - 1],
        ).af_termination == 1,
    ensures
        insert_tail_loop(
            state,
            boundary,
            begin,
            sift,
            gap,
            temporary,
        )
            == restored_state(
                adapter_callback(
                    shifted_state(state, sift, gap),
                    boundary,
                    temporary,
                    state.e_sequence[sift - 1],
                ),
                sift,
                temporary,
                true,
            ),
        insert_tail_loop(
            state,
            boundary,
            begin,
            sift,
            gap,
            temporary,
        ).e_sequence
            == state.e_sequence
                .update(gap, state.e_sequence[sift])
                .update(sift, temporary),
        insert_tail_loop(
            state,
            boundary,
            begin,
            sift,
            gap,
            temporary,
        ).e_callback_state
            == callback_frame(
                shifted_state(state, sift, gap),
                boundary,
                temporary,
                state.e_sequence[sift - 1],
            ).af_state,
        insert_tail_loop(
            state,
            boundary,
            begin,
            sift,
            gap,
            temporary,
        ).e_panicked,
        !insert_tail_loop(
            state,
            boundary,
            begin,
            sift,
            gap,
            temporary,
        ).e_aborted,
{
}

pub proof fn loop_abort_bypasses_copy_on_drop(
    state: InsertTailState,
    boundary: KeyOrdDropBoundary,
    begin: int,
    sift: int,
    gap: int,
    temporary: int,
)
    requires
        valid_insert_tail_loop_input(state, begin, sift, gap),
        begin < sift,
        callback_frame(
            shifted_state(state, sift, gap),
            boundary,
            temporary,
            state.e_sequence[sift - 1],
        ).af_termination == 2,
    ensures
        insert_tail_loop(
            state,
            boundary,
            begin,
            sift,
            gap,
            temporary,
        )
            == adapter_callback(
                shifted_state(state, sift, gap),
                boundary,
                temporary,
                state.e_sequence[sift - 1],
            ),
        insert_tail_loop(
            state,
            boundary,
            begin,
            sift,
            gap,
            temporary,
        ).e_sequence
            == state.e_sequence.update(gap, state.e_sequence[sift]),
        insert_tail_loop(
            state,
            boundary,
            begin,
            sift,
            gap,
            temporary,
        ).e_callback_state
            == callback_frame(
                shifted_state(state, sift, gap),
                boundary,
                temporary,
                state.e_sequence[sift - 1],
            ).af_state,
        insert_tail_loop(
            state,
            boundary,
            begin,
            sift,
            gap,
            temporary,
        ).e_panicked,
        insert_tail_loop(
            state,
            boundary,
            begin,
            sift,
            gap,
            temporary,
        ).e_aborted,
{
}

pub proof fn loop_less_advances_sift_and_gap(
    state: InsertTailState,
    boundary: KeyOrdDropBoundary,
    begin: int,
    sift: int,
    gap: int,
    temporary: int,
)
    requires
        valid_insert_tail_loop_input(state, begin, sift, gap),
        begin < sift,
        callback_frame(
            shifted_state(state, sift, gap),
            boundary,
            temporary,
            state.e_sequence[sift - 1],
        ).af_termination == 0,
        target_adapter_is_less(
            shifted_state(state, sift, gap),
            boundary,
            temporary,
            state.e_sequence[sift - 1],
        ),
    ensures
        insert_tail_loop(
            state,
            boundary,
            begin,
            sift,
            gap,
            temporary,
        )
            == insert_tail_loop(
                adapter_callback(
                    shifted_state(state, sift, gap),
                    boundary,
                    temporary,
                    state.e_sequence[sift - 1],
                ),
                boundary,
                begin,
                sift - 1,
                sift,
                temporary,
            ),
{
}

pub proof fn shift_then_restore_preserves_identity_multiplicity(
    sequence: Seq<int>,
    sift: int,
    gap: int,
    temporary: int,
)
    requires
        0 <= sift,
        gap == sift + 1,
        gap < sequence.len(),
    ensures
        sequence
            .update(gap, sequence[sift])
            .update(sift, temporary)
            .to_multiset()
            =~= sequence.update(gap, temporary).to_multiset(),
{
    broadcast use vstd::seq_lib::group_to_multiset_ensures;
    broadcast use vstd::multiset::group_multiset_axioms;
}

pub proof fn insert_tail_loop_preserves_length_and_outside_frame(
    state: InsertTailState,
    boundary: KeyOrdDropBoundary,
    begin: int,
    sift: int,
    gap: int,
    temporary: int,
)
    requires
        valid_insert_tail_loop_input(state, begin, sift, gap),
    ensures
        insert_tail_loop(
            state,
            boundary,
            begin,
            sift,
            gap,
            temporary,
        ).e_sequence.len() == state.e_sequence.len(),
        forall|index: int|
            0 <= index < state.e_sequence.len()
                && (index < begin || gap < index)
                ==> #[trigger] insert_tail_loop(
                    state,
                    boundary,
                    begin,
                    sift,
                    gap,
                    temporary,
                ).e_sequence[index]
                    == state.e_sequence[index],
    decreases sift - begin,
{
    reveal(insert_tail_loop);
    broadcast use vstd::seq_lib::group_seq_properties;

    let shifted = shifted_state(state, sift, gap);
    if sift <= begin {
        assert(sift == begin);
    } else {
        let next_sift = sift - 1;
        let right = shifted.e_sequence[next_sift];
        let called = adapter_callback(
            shifted,
            boundary,
            temporary,
            right,
        );
        let less = target_adapter_is_less(
            shifted,
            boundary,
            temporary,
            right,
        );
        if called.e_panicked {
        } else if less {
            insert_tail_loop_preserves_length_and_outside_frame(
                called,
                boundary,
                begin,
                next_sift,
                sift,
                temporary,
            );
            assert forall|index: int|
                0 <= index < state.e_sequence.len()
                    && (index < begin || gap < index)
                    implies #[trigger] insert_tail_loop(
                        called,
                        boundary,
                        begin,
                        next_sift,
                        sift,
                        temporary,
                    ).e_sequence[index]
                        == state.e_sequence[index] by {
                assert(index < begin || sift < index);
                assert(index != gap);
                assert(index != sift);
            }
        }
    }
}

pub proof fn insert_tail_loop_nonabort_preserves_identity_multiplicity(
    state: InsertTailState,
    boundary: KeyOrdDropBoundary,
    begin: int,
    sift: int,
    gap: int,
    temporary: int,
)
    requires
        valid_insert_tail_loop_input(state, begin, sift, gap),
    ensures
        !insert_tail_loop(
            state,
            boundary,
            begin,
            sift,
            gap,
            temporary,
        ).e_aborted
            ==> insert_tail_loop(
                state,
                boundary,
                begin,
                sift,
                gap,
                temporary,
            ).e_sequence.to_multiset()
                =~= restored_sequence(
                    state,
                    gap,
                    temporary,
                ).to_multiset(),
    decreases sift - begin,
{
    reveal(insert_tail_loop);
    broadcast use vstd::seq_lib::group_seq_properties;
    broadcast use vstd::seq_lib::group_to_multiset_ensures;
    broadcast use vstd::multiset::group_multiset_axioms;

    let shifted = shifted_state(state, sift, gap);
    shift_then_restore_preserves_identity_multiplicity(
        state.e_sequence,
        sift,
        gap,
        temporary,
    );
    if sift <= begin {
        assert(sift == begin);
    } else {
        let next_sift = sift - 1;
        let right = shifted.e_sequence[next_sift];
        let called = adapter_callback(
            shifted,
            boundary,
            temporary,
            right,
        );
        let less = target_adapter_is_less(
            shifted,
            boundary,
            temporary,
            right,
        );
        if called.e_panicked {
        } else if less {
            insert_tail_loop_nonabort_preserves_identity_multiplicity(
                called,
                boundary,
                begin,
                next_sift,
                sift,
                temporary,
            );
        }
    }
}

pub proof fn insert_tail_preserves_length_frame_and_nonabort_multiplicity(
    state: InsertTailState,
    boundary: KeyOrdDropBoundary,
    begin: int,
    tail: int,
)
    requires
        valid_insert_tail_input(state, begin, tail),
    ensures
        insert_tail(state, boundary, begin, tail).e_sequence.len()
            == state.e_sequence.len(),
        forall|index: int|
            0 <= index < state.e_sequence.len()
                && (index < begin || tail < index)
                ==> #[trigger] insert_tail(
                    state,
                    boundary,
                    begin,
                    tail,
                ).e_sequence[index]
                    == state.e_sequence[index],
        !insert_tail(state, boundary, begin, tail).e_aborted
            ==> insert_tail(
                state,
                boundary,
                begin,
                tail,
            ).e_sequence.to_multiset()
                =~= state.e_sequence.to_multiset(),
{
    reveal(insert_tail);
    broadcast use vstd::seq_lib::group_seq_properties;
    broadcast use vstd::seq_lib::group_to_multiset_ensures;

    let temporary = state.e_sequence[tail];
    let right = state.e_sequence[tail - 1];
    let called = adapter_callback(
        state,
        boundary,
        temporary,
        right,
    );
    let less = target_adapter_is_less(
        state,
        boundary,
        temporary,
        right,
    );
    if called.e_panicked {
    } else if less {
        insert_tail_loop_preserves_length_and_outside_frame(
            called,
            boundary,
            begin,
            tail - 1,
            tail,
            temporary,
        );
        insert_tail_loop_nonabort_preserves_identity_multiplicity(
            called,
            boundary,
            begin,
            tail - 1,
            tail,
            temporary,
        );
        assert(state.e_sequence.update(tail, temporary)
            == state.e_sequence);
    }
}

}
