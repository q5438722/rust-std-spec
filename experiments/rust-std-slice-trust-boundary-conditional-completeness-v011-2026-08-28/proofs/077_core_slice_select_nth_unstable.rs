#![allow(dead_code, unused_imports, unused_variables)]
// Experiment-local source-backed model for core::slice::select_nth_unstable.

use vstd::prelude::*;

verus! {

pub ghost struct Five {
    pub e0: int,
    pub e1: int,
    pub e2: int,
    pub e3: int,
    pub e4: int,
}

pub ghost struct OrdBoundary {
    pub class10: int,
    pub class11: int,
    pub class20: int,
    pub class21: int,
    pub class30: int,
    pub class31: int,
}

pub open spec fn ord_class(boundary: OrdBoundary, identity: int) -> int {
    if identity == 10 {
        boundary.class10
    } else if identity == 11 {
        boundary.class11
    } else if identity == 20 {
        boundary.class20
    } else if identity == 21 {
        boundary.class21
    } else if identity == 30 {
        boundary.class30
    } else {
        boundary.class31
    }
}

pub open spec fn multiplicity(sequence: Five, identity: int) -> int {
    (if sequence.e0 == identity { 1int } else { 0int })
        + (if sequence.e1 == identity { 1int } else { 0int })
        + (if sequence.e2 == identity { 1int } else { 0int })
        + (if sequence.e3 == identity { 1int } else { 0int })
        + (if sequence.e4 == identity { 1int } else { 0int })
}

pub open spec fn class_count(
    boundary: OrdBoundary,
    sequence: Five,
    class: int,
) -> int {
    (if ord_class(boundary, sequence.e0) == class { 1int } else { 0int })
        + (if ord_class(boundary, sequence.e1) == class { 1int } else { 0int })
        + (if ord_class(boundary, sequence.e2) == class { 1int } else { 0int })
        + (if ord_class(boundary, sequence.e3) == class { 1int } else { 0int })
        + (if ord_class(boundary, sequence.e4) == class { 1int } else { 0int })
}

pub open spec fn less_count(
    boundary: OrdBoundary,
    sequence: Five,
    class: int,
) -> int {
    (if ord_class(boundary, sequence.e0) < class { 1int } else { 0int })
        + (if ord_class(boundary, sequence.e1) < class { 1int } else { 0int })
        + (if ord_class(boundary, sequence.e2) < class { 1int } else { 0int })
        + (if ord_class(boundary, sequence.e3) < class { 1int } else { 0int })
        + (if ord_class(boundary, sequence.e4) < class { 1int } else { 0int })
}

pub open spec fn greater_count(
    boundary: OrdBoundary,
    sequence: Five,
    class: int,
) -> int {
    (if ord_class(boundary, sequence.e0) > class { 1int } else { 0int })
        + (if ord_class(boundary, sequence.e1) > class { 1int } else { 0int })
        + (if ord_class(boundary, sequence.e2) > class { 1int } else { 0int })
        + (if ord_class(boundary, sequence.e3) > class { 1int } else { 0int })
        + (if ord_class(boundary, sequence.e4) > class { 1int } else { 0int })
}

pub open spec fn exact_multiplicities(left: Five, right: Five) -> bool {
    multiplicity(left, left.e0) == multiplicity(right, left.e0)
        && multiplicity(left, left.e1) == multiplicity(right, left.e1)
        && multiplicity(left, left.e2) == multiplicity(right, left.e2)
        && multiplicity(left, left.e3) == multiplicity(right, left.e3)
        && multiplicity(left, left.e4) == multiplicity(right, left.e4)
        && multiplicity(left, right.e0) == multiplicity(right, right.e0)
        && multiplicity(left, right.e1) == multiplicity(right, right.e1)
        && multiplicity(left, right.e2) == multiplicity(right, right.e2)
        && multiplicity(left, right.e3) == multiplicity(right, right.e3)
        && multiplicity(left, right.e4) == multiplicity(right, right.e4)
}

pub open spec fn left_class_count(
    boundary: OrdBoundary,
    sequence: Five,
    class: int,
) -> int {
    (if ord_class(boundary, sequence.e0) == class { 1int } else { 0int })
        + (if ord_class(boundary, sequence.e1) == class { 1int } else { 0int })
}

pub open spec fn right_class_count(
    boundary: OrdBoundary,
    sequence: Five,
    class: int,
) -> int {
    (if ord_class(boundary, sequence.e3) == class { 1int } else { 0int })
        + (if ord_class(boundary, sequence.e4) == class { 1int } else { 0int })
}

pub open spec fn bounds_transition(len: int, index: int) -> bool {
    0 < len && 0 <= index < len
}

pub open spec fn source_branch(is_zst: bool, len: int, index: int) -> int {
    if is_zst {
        0
    } else if index == len - 1 {
        1
    } else if index == 0 {
        2
    } else {
        3
    }
}

pub open spec fn rank_selected(
    boundary: OrdBoundary,
    sequence: Five,
    index: int,
    class: int,
) -> bool {
    less_count(boundary, sequence, class) <= index
        < less_count(boundary, sequence, class)
            + class_count(boundary, sequence, class)
}

pub open spec fn zst_transition(
    is_zst: bool,
    boundary: OrdBoundary,
    sequence: Five,
    class: int,
) -> bool {
    is_zst ==> less_count(boundary, sequence, class) == 0
        && class_count(boundary, sequence, class) == 5
        && greater_count(boundary, sequence, class) == 0
}

pub open spec fn min_max_transition(
    is_zst: bool,
    boundary: OrdBoundary,
    sequence: Five,
    index: int,
    class: int,
) -> bool {
    (!is_zst && index == 4 ==>
        greater_count(boundary, sequence, class) == 0)
        && (!is_zst && index != 4 && index == 0 ==>
            less_count(boundary, sequence, class) == 0)
}

pub open spec fn swap_transition(before: Five, after: Five) -> bool {
    exact_multiplicities(before, after)
}

pub open spec fn partition_transition(
    boundary: OrdBoundary,
    sequence: Five,
) -> bool {
    ord_class(boundary, sequence.e0) <= ord_class(boundary, sequence.e2)
        && ord_class(boundary, sequence.e1) <= ord_class(boundary, sequence.e2)
        && ord_class(boundary, sequence.e3) >= ord_class(boundary, sequence.e2)
        && ord_class(boundary, sequence.e4) >= ord_class(boundary, sequence.e2)
}

pub open spec fn sorted_transition(
    boundary: OrdBoundary,
    sequence: Five,
) -> bool {
    ord_class(boundary, sequence.e0) <= ord_class(boundary, sequence.e1)
        && ord_class(boundary, sequence.e1) <= ord_class(boundary, sequence.e2)
        && ord_class(boundary, sequence.e2) <= ord_class(boundary, sequence.e3)
        && ord_class(boundary, sequence.e3) <= ord_class(boundary, sequence.e4)
}

pub open spec fn source_window_valid(
    len: int,
    index: int,
    start: int,
    end: int,
) -> bool {
    0 <= start <= index < end <= len
}

pub open spec fn source_reachable_window(
    len: int,
    index: int,
    narrowings: int,
    start: int,
    end: int,
) -> bool {
    0 <= narrowings <= 16
        && source_window_valid(len, index, start, end)
        && (narrowings == 0 ==> start == 0 && end == len)
        && (narrowings > 0 ==> end - start <= len - narrowings)
}

pub open spec fn fallback_reachable_window(
    index: int,
    initial_start: int,
    initial_end: int,
    narrowings: int,
    start: int,
    end: int,
) -> bool {
    0 <= narrowings < initial_end - initial_start
        && initial_start <= start <= index < end <= initial_end
        && (narrowings == 0 ==>
            start == initial_start && end == initial_end)
        && (narrowings > 0 ==>
            end - start <= initial_end - initial_start - narrowings)
}

pub open spec fn recursive_or_fallback_transition(
    boundary: OrdBoundary,
    final_sequence: Five,
    len: int,
    index: int,
    main_narrowings: int,
    current_start: int,
    current_end: int,
    fallback_narrowings: int,
    fallback_start: int,
    fallback_end: int,
) -> bool {
    source_reachable_window(
        len,
        index,
        main_narrowings,
        current_start,
        current_end,
    )
        && (0 < index < len - 1 ==>
            if main_narrowings < 16 {
                if current_end - current_start <= 16 {
                    sorted_transition(boundary, final_sequence)
                } else {
                    partition_transition(boundary, final_sequence)
                }
            } else if current_end - current_start <= 16 {
                sorted_transition(boundary, final_sequence)
            } else {
                fallback_reachable_window(
                    index,
                    current_start,
                    current_end,
                    fallback_narrowings,
                    fallback_start,
                    fallback_end,
                ) && if fallback_end - fallback_start <= 16 {
                    sorted_transition(boundary, final_sequence)
                } else {
                    partition_transition(boundary, final_sequence)
                }
            })
}

pub open spec fn final_subslice_transition(
    len: int,
    index: int,
    left_len: int,
    pivot_start: int,
    right_start: int,
    right_len: int,
) -> bool {
    left_len == index
        && pivot_start == index
        && right_start == index + 1
        && right_len == len - index - 1
        && left_len + 1 + right_len == len
}

pub open spec fn active_contract(
    input: Five,
    boundary: OrdBoundary,
    final_sequence: Five,
) -> bool {
    bounds_transition(5, 2)
        && swap_transition(input, final_sequence)
        && partition_transition(boundary, final_sequence)
        && recursive_or_fallback_transition(
            boundary,
            final_sequence,
            5,
            2,
            0,
            0,
            5,
            0,
            0,
            5,
        )
        && final_subslice_transition(5, 2, 2, 2, 3, 2)
}

pub open spec fn reviewed_selection_equivalent(
    boundary: OrdBoundary,
    left: Five,
    right: Five,
) -> bool {
    exact_multiplicities(left, right)
        && ord_class(boundary, left.e2) == ord_class(boundary, right.e2)
        && left_class_count(boundary, left, 0)
            == left_class_count(boundary, right, 0)
        && left_class_count(boundary, left, 1)
            == left_class_count(boundary, right, 1)
        && left_class_count(boundary, left, 2)
            == left_class_count(boundary, right, 2)
        && right_class_count(boundary, left, 0)
            == right_class_count(boundary, right, 0)
        && right_class_count(boundary, left, 1)
            == right_class_count(boundary, right, 1)
        && right_class_count(boundary, left, 2)
            == right_class_count(boundary, right, 2)
}

pub proof fn derived_rank_class_is_unique(
    boundary: OrdBoundary,
    sequence: Five,
    index: int,
    left_class: int,
    right_class: int,
)
    requires
        rank_selected(boundary, sequence, index, left_class),
        rank_selected(boundary, sequence, index, right_class),
        left_class < right_class ==>
            less_count(boundary, sequence, left_class)
                + class_count(boundary, sequence, left_class)
                <= less_count(boundary, sequence, right_class),
        right_class < left_class ==>
            less_count(boundary, sequence, right_class)
                + class_count(boundary, sequence, right_class)
                <= less_count(boundary, sequence, left_class),
    ensures
        left_class == right_class,
{
    if left_class < right_class {
        assert(
            index
                < less_count(boundary, sequence, left_class)
                    + class_count(boundary, sequence, left_class)
                <= less_count(boundary, sequence, right_class)
                <= index
        );
        assert(false);
    } else if right_class < left_class {
        assert(
            index
                < less_count(boundary, sequence, right_class)
                    + class_count(boundary, sequence, right_class)
                <= less_count(boundary, sequence, left_class)
                <= index
        );
        assert(false);
    }
}

pub proof fn source_branch_conditions_are_exhaustive(
    is_zst: bool,
    len: int,
    index: int,
)
    requires
        bounds_transition(len, index),
    ensures
        0 <= source_branch(is_zst, len, index) <= 3,
        source_branch(is_zst, len, index) == 0 ==> is_zst,
        source_branch(is_zst, len, index) == 1 ==> !is_zst && index == len - 1,
        source_branch(is_zst, len, index) == 2 ==>
            !is_zst && index != len - 1 && index == 0,
        source_branch(is_zst, len, index) == 3 ==>
            !is_zst && index != len - 1 && index != 0,
{
}

pub proof fn side_reordering_is_reviewed_equivalent() {
    let input = Five { e0: 10, e1: 11, e2: 20, e3: 30, e4: 31 };
    let boundary = OrdBoundary {
        class10: 0,
        class11: 0,
        class20: 1,
        class21: 1,
        class30: 2,
        class31: 2,
    };
    let first = Five { e0: 10, e1: 11, e2: 20, e3: 30, e4: 31 };
    let second = Five { e0: 11, e1: 10, e2: 20, e3: 31, e4: 30 };
    assert(active_contract(input, boundary, first));
    assert(active_contract(input, boundary, second));
    assert(reviewed_selection_equivalent(boundary, first, second));
    assert(first.e0 != second.e0);
}

pub proof fn equal_class_pivot_identity_is_reviewed_equivalent() {
    let input = Five { e0: 10, e1: 11, e2: 20, e3: 21, e4: 30 };
    let boundary = OrdBoundary {
        class10: 0,
        class11: 0,
        class20: 1,
        class21: 1,
        class30: 2,
        class31: 2,
    };
    let first = Five { e0: 10, e1: 11, e2: 20, e3: 21, e4: 30 };
    let second = Five { e0: 11, e1: 10, e2: 21, e3: 20, e4: 30 };
    assert(active_contract(input, boundary, first));
    assert(active_contract(input, boundary, second));
    assert(first.e2 != second.e2);
    assert(ord_class(boundary, first.e2) == ord_class(boundary, second.e2));
    assert(reviewed_selection_equivalent(boundary, first, second));
}

pub proof fn invalid_selection_observations_are_rejected() {
    let input = Five { e0: 10, e1: 11, e2: 20, e3: 30, e4: 31 };
    let boundary = OrdBoundary {
        class10: 0,
        class11: 0,
        class20: 1,
        class21: 1,
        class30: 2,
        class31: 2,
    };
    let foreign = Five { e0: 10, e1: 11, e2: 20, e3: 30, e4: 21 };
    let crossing = Five { e0: 30, e1: 11, e2: 20, e3: 10, e4: 31 };
    assert(!swap_transition(input, foreign));
    assert(!partition_transition(boundary, crossing));
    assert(!final_subslice_transition(5, 2, 1, 2, 3, 2));
}

}
