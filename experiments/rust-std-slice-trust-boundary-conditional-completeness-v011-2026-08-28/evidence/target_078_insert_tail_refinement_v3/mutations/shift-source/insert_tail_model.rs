#![allow(dead_code, unused_imports, unused_variables)]
// Constructive refinement of Rust 1.96 insert_tail and CopyOnDrop.

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

pub ghost struct InsertTailState {
    pub e_sequence: Seq<int>,
    pub e_callback_state: int,
    pub e_panicked: bool,
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

pub open spec fn comparator_callback(
    state: InsertTailState,
    boundary: ComparatorBoundary,
    left: int,
    right: int,
) -> InsertTailState {
    InsertTailState {
        e_sequence: state.e_sequence,
        e_callback_state: boundary_next_state(
            boundary,
            state.e_callback_state,
            left,
            right,
        ),
        e_panicked: boundary_panics(
            boundary,
            state.e_callback_state,
            left,
            right,
        ),
    }
}

pub open spec fn shifted_state(
    state: InsertTailState,
    sift: int,
    gap: int,
) -> InsertTailState {
    InsertTailState {
        e_sequence: state.e_sequence.update(
            gap,
            state.e_sequence[gap],
        ),
        e_callback_state: state.e_callback_state,
        e_panicked: false,
    }
}

pub open spec fn restored_state(
    state: InsertTailState,
    destination: int,
    temporary: int,
    panicked: bool,
) -> InsertTailState {
    InsertTailState {
        e_sequence: state.e_sequence.update(destination, temporary),
        e_callback_state: state.e_callback_state,
        e_panicked: panicked,
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
        && 0 <= begin
        && begin <= sift
        && gap == sift + 1
        && gap < state.e_sequence.len()
}

pub open spec fn insert_tail_loop(
    state: InsertTailState,
    boundary: ComparatorBoundary,
    begin: int,
    sift: int,
    gap: int,
    temporary: int,
) -> InsertTailState
    decreases sift - begin,
{
    if state.e_panicked {
        state
    } else {
        let shifted = shifted_state(state, sift, gap);
        if sift <= begin {
            restored_state(shifted, sift, temporary, false)
        } else {
            let next_sift = sift - 1;
            let right = shifted.e_sequence[next_sift];
            let called = comparator_callback(
                shifted,
                boundary,
                temporary,
                right,
            );
            let less = target_adapter_is_less(
                boundary,
                shifted.e_callback_state,
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
    boundary: ComparatorBoundary,
    begin: int,
    tail: int,
) -> InsertTailState {
    if state.e_panicked {
        state
    } else {
        let temporary = state.e_sequence[tail];
        let right = state.e_sequence[tail - 1];
        let called = comparator_callback(
            state,
            boundary,
            temporary,
            right,
        );
        let less = target_adapter_is_less(
            boundary,
            state.e_callback_state,
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

pub open spec fn panic_state_is_boundary_observed(
    boundary: ComparatorBoundary,
    callback_state: int,
) -> bool {
    exists|lookup_state: int, left: int, right: int|
        boundary_panics(boundary, lookup_state, left, right)
            && callback_state
                == boundary_next_state(
                    boundary,
                    lookup_state,
                    left,
                    right,
                )
}

pub proof fn callback_uses_ordered_operands_and_pre_state(
    state: InsertTailState,
    boundary: ComparatorBoundary,
    left: int,
    right: int,
)
    ensures
        comparator_callback(
            state,
            boundary,
            left,
            right,
        ).e_sequence == state.e_sequence,
        comparator_callback(
            state,
            boundary,
            left,
            right,
        ).e_callback_state
            == boundary_next_state(
                boundary,
                state.e_callback_state,
                left,
                right,
            ),
        comparator_callback(
            state,
            boundary,
            left,
            right,
        ).e_panicked
            == boundary_panics(
                boundary,
                state.e_callback_state,
                left,
                right,
            ),
{
}

pub proof fn initial_comparison_panic_is_exact(
    state: InsertTailState,
    boundary: ComparatorBoundary,
    begin: int,
    tail: int,
)
    requires
        valid_insert_tail_input(state, begin, tail),
        boundary_panics(
            boundary,
            state.e_callback_state,
            state.e_sequence[tail],
            state.e_sequence[tail - 1],
        ),
    ensures
        insert_tail(state, boundary, begin, tail)
            == comparator_callback(
                state,
                boundary,
                state.e_sequence[tail],
                state.e_sequence[tail - 1],
            ),
        insert_tail(state, boundary, begin, tail).e_sequence
            == state.e_sequence,
        insert_tail(state, boundary, begin, tail).e_callback_state
            == boundary_next_state(
                boundary,
                state.e_callback_state,
                state.e_sequence[tail],
                state.e_sequence[tail - 1],
            ),
        insert_tail(state, boundary, begin, tail).e_panicked,
{
}

pub proof fn no_shift_path_is_exact(
    state: InsertTailState,
    boundary: ComparatorBoundary,
    begin: int,
    tail: int,
)
    requires
        valid_insert_tail_input(state, begin, tail),
        !boundary_panics(
            boundary,
            state.e_callback_state,
            state.e_sequence[tail],
            state.e_sequence[tail - 1],
        ),
        !target_adapter_is_less(
            boundary,
            state.e_callback_state,
            state.e_sequence[tail],
            state.e_sequence[tail - 1],
        ),
    ensures
        insert_tail(state, boundary, begin, tail)
            == comparator_callback(
                state,
                boundary,
                state.e_sequence[tail],
                state.e_sequence[tail - 1],
            ),
        insert_tail(state, boundary, begin, tail).e_sequence
            == state.e_sequence,
        !insert_tail(state, boundary, begin, tail).e_panicked,
{
}

pub proof fn initial_less_enters_loop_with_tail_gap(
    state: InsertTailState,
    boundary: ComparatorBoundary,
    begin: int,
    tail: int,
)
    requires
        valid_insert_tail_input(state, begin, tail),
        !boundary_panics(
            boundary,
            state.e_callback_state,
            state.e_sequence[tail],
            state.e_sequence[tail - 1],
        ),
        target_adapter_is_less(
            boundary,
            state.e_callback_state,
            state.e_sequence[tail],
            state.e_sequence[tail - 1],
        ),
    ensures
        insert_tail(state, boundary, begin, tail)
            == insert_tail_loop(
                comparator_callback(
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
    boundary: ComparatorBoundary,
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
    boundary: ComparatorBoundary,
    begin: int,
    sift: int,
    gap: int,
    temporary: int,
)
    requires
        valid_insert_tail_loop_input(state, begin, sift, gap),
        begin < sift,
        !boundary_panics(
            boundary,
            state.e_callback_state,
            temporary,
            state.e_sequence[sift - 1],
        ),
        !target_adapter_is_less(
            boundary,
            state.e_callback_state,
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
                comparator_callback(
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

pub proof fn loop_panic_restores_gap_and_retains_callback_state(
    state: InsertTailState,
    boundary: ComparatorBoundary,
    begin: int,
    sift: int,
    gap: int,
    temporary: int,
)
    requires
        valid_insert_tail_loop_input(state, begin, sift, gap),
        begin < sift,
        boundary_panics(
            boundary,
            state.e_callback_state,
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
                comparator_callback(
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
        ).e_callback_state
            == boundary_next_state(
                boundary,
                state.e_callback_state,
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
        ).e_panicked,
{
}

pub proof fn loop_less_advances_sift_and_gap(
    state: InsertTailState,
    boundary: ComparatorBoundary,
    begin: int,
    sift: int,
    gap: int,
    temporary: int,
)
    requires
        valid_insert_tail_loop_input(state, begin, sift, gap),
        begin < sift,
        !boundary_panics(
            boundary,
            state.e_callback_state,
            temporary,
            state.e_sequence[sift - 1],
        ),
        target_adapter_is_less(
            boundary,
            state.e_callback_state,
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
                comparator_callback(
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

pub proof fn insert_tail_loop_preserves_restored_sequence_properties(
    state: InsertTailState,
    boundary: ComparatorBoundary,
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
        insert_tail_loop(
            state,
            boundary,
            begin,
            sift,
            gap,
            temporary,
        ).e_sequence.to_multiset()
            =~= restored_sequence(state, gap, temporary).to_multiset(),
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
        let called = comparator_callback(
            shifted,
            boundary,
            temporary,
            right,
        );
        let less = target_adapter_is_less(
            boundary,
            shifted.e_callback_state,
            temporary,
            right,
        );
        if called.e_panicked {
        } else if less {
            insert_tail_loop_preserves_restored_sequence_properties(
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

pub proof fn insert_tail_preserves_length_multiplicity_and_frame(
    state: InsertTailState,
    boundary: ComparatorBoundary,
    begin: int,
    tail: int,
)
    requires
        valid_insert_tail_input(state, begin, tail),
    ensures
        insert_tail(state, boundary, begin, tail).e_sequence.len()
            == state.e_sequence.len(),
        insert_tail(
            state,
            boundary,
            begin,
            tail,
        ).e_sequence.to_multiset() =~= state.e_sequence.to_multiset(),
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
{
    reveal(insert_tail);
    broadcast use vstd::seq_lib::group_seq_properties;
    broadcast use vstd::seq_lib::group_to_multiset_ensures;

    let temporary = state.e_sequence[tail];
    let right = state.e_sequence[tail - 1];
    let called = comparator_callback(state, boundary, temporary, right);
    let less = target_adapter_is_less(
        boundary,
        state.e_callback_state,
        temporary,
        right,
    );
    if called.e_panicked {
    } else if less {
        insert_tail_loop_preserves_restored_sequence_properties(
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

pub proof fn insert_tail_loop_retains_callback_state_on_panic(
    state: InsertTailState,
    boundary: ComparatorBoundary,
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
        ).e_panicked
            ==> panic_state_is_boundary_observed(
                boundary,
                insert_tail_loop(
                    state,
                    boundary,
                    begin,
                    sift,
                    gap,
                    temporary,
                ).e_callback_state,
            ),
    decreases sift - begin,
{
    reveal(insert_tail_loop);
    let shifted = shifted_state(state, sift, gap);
    if sift > begin {
        let next_sift = sift - 1;
        let right = shifted.e_sequence[next_sift];
        let called = comparator_callback(
            shifted,
            boundary,
            temporary,
            right,
        );
        let less = target_adapter_is_less(
            boundary,
            shifted.e_callback_state,
            temporary,
            right,
        );
        if called.e_panicked {
            assert(panic_state_is_boundary_observed(
                boundary,
                called.e_callback_state,
            )) by {
                let lookup_state = state.e_callback_state;
                assert(boundary_panics(
                    boundary,
                    lookup_state,
                    temporary,
                    right,
                ));
            }
        } else if less {
            insert_tail_loop_retains_callback_state_on_panic(
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

pub proof fn insert_tail_retains_callback_state_on_panic(
    state: InsertTailState,
    boundary: ComparatorBoundary,
    begin: int,
    tail: int,
)
    requires
        valid_insert_tail_input(state, begin, tail),
    ensures
        insert_tail(state, boundary, begin, tail).e_panicked
            ==> panic_state_is_boundary_observed(
                boundary,
                insert_tail(
                    state,
                    boundary,
                    begin,
                    tail,
                ).e_callback_state,
            ),
{
    reveal(insert_tail);
    let temporary = state.e_sequence[tail];
    let right = state.e_sequence[tail - 1];
    let called = comparator_callback(state, boundary, temporary, right);
    let less = target_adapter_is_less(
        boundary,
        state.e_callback_state,
        temporary,
        right,
    );
    if called.e_panicked {
        assert(panic_state_is_boundary_observed(
            boundary,
            called.e_callback_state,
        )) by {
            let lookup_state = state.e_callback_state;
            assert(boundary_panics(
                boundary,
                lookup_state,
                temporary,
                right,
            ));
        }
    } else if less {
        insert_tail_loop_retains_callback_state_on_panic(
            called,
            boundary,
            begin,
            tail - 1,
            tail,
            temporary,
        );
    }
}

}
