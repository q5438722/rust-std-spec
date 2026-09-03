#![allow(dead_code, unused_imports, unused_variables)]
// Experiment-local length-three contract model for core::slice::sort_unstable_by.

use vstd::prelude::*;

verus! {

pub ghost struct Triple {
    pub e0: int,
    pub e1: int,
    pub e2: int,
}

pub ghost struct SortInput {
    pub elements: Triple,
    pub callback_initial_state: int,
}

pub ghost struct ComparatorBoundary {
    pub id0: int,
    pub id1: int,
    pub id2: int,
    pub c00: int,
    pub c01: int,
    pub c02: int,
    pub c10: int,
    pub c11: int,
    pub c12: int,
    pub c20: int,
    pub c21: int,
    pub c22: int,
    pub callback_state_delta: int,
}

pub open spec fn ordering_observed(ordering: int) -> bool {
    ordering == -1 || ordering == 0 || ordering == 1
}

pub open spec fn distinct_input(input: SortInput) -> bool {
    input.elements.e0 != input.elements.e1
        && input.elements.e0 != input.elements.e2
        && input.elements.e1 != input.elements.e2
}

pub open spec fn boundary_ids_match(
    input: SortInput,
    boundary: ComparatorBoundary,
) -> bool {
    boundary.id0 == input.elements.e0
        && boundary.id1 == input.elements.e1
        && boundary.id2 == input.elements.e2
}

pub open spec fn boundary_observed(
    input: SortInput,
    boundary: ComparatorBoundary,
) -> bool {
    boundary_ids_match(input, boundary)
        && ordering_observed(boundary.c00)
        && ordering_observed(boundary.c01)
        && ordering_observed(boundary.c02)
        && ordering_observed(boundary.c10)
        && ordering_observed(boundary.c11)
        && ordering_observed(boundary.c12)
        && ordering_observed(boundary.c20)
        && ordering_observed(boundary.c21)
        && ordering_observed(boundary.c22)
        && boundary.callback_state_delta == 0
}

pub open spec fn observed_ordering(
    boundary: ComparatorBoundary,
    left: int,
    right: int,
) -> int {
    if left == boundary.id0 {
        if right == boundary.id0 {
            boundary.c00
        } else if right == boundary.id1 {
            boundary.c01
        } else {
            boundary.c02
        }
    } else if left == boundary.id1 {
        if right == boundary.id0 {
            boundary.c10
        } else if right == boundary.id1 {
            boundary.c11
        } else {
            boundary.c12
        }
    } else {
        if right == boundary.id0 {
            boundary.c20
        } else if right == boundary.id1 {
            boundary.c21
        } else {
            boundary.c22
        }
    }
}

pub open spec fn comparator_leq(
    boundary: ComparatorBoundary,
    left: int,
    right: int,
) -> bool {
    observed_ordering(boundary, left, right) <= 0
}

pub open spec fn comparator_equivalent(
    boundary: ComparatorBoundary,
    left: int,
    right: int,
) -> bool {
    observed_ordering(boundary, left, right) == 0
        && observed_ordering(boundary, right, left) == 0
}

pub open spec fn multiplicity(sequence: Triple, identity: int) -> int {
    (if sequence.e0 == identity { 1int } else { 0int })
        + (if sequence.e1 == identity { 1int } else { 0int })
        + (if sequence.e2 == identity { 1int } else { 0int })
}

pub open spec fn exact_multiplicities(left: Triple, right: Triple) -> bool {
    multiplicity(left, left.e0) == multiplicity(right, left.e0)
        && multiplicity(left, left.e1) == multiplicity(right, left.e1)
        && multiplicity(left, left.e2) == multiplicity(right, left.e2)
        && multiplicity(left, right.e0) == multiplicity(right, right.e0)
        && multiplicity(left, right.e1) == multiplicity(right, right.e1)
        && multiplicity(left, right.e2) == multiplicity(right, right.e2)
}

pub open spec fn one_of_six_permutations(before: Triple, after: Triple) -> bool {
    (after.e0 == before.e0 && after.e1 == before.e1 && after.e2 == before.e2)
        || (after.e0 == before.e0 && after.e1 == before.e2 && after.e2 == before.e1)
        || (after.e0 == before.e1 && after.e1 == before.e0 && after.e2 == before.e2)
        || (after.e0 == before.e1 && after.e1 == before.e2 && after.e2 == before.e0)
        || (after.e0 == before.e2 && after.e1 == before.e0 && after.e2 == before.e1)
        || (after.e0 == before.e2 && after.e1 == before.e1 && after.e2 == before.e0)
}

pub open spec fn generated_permutation(before: Triple, after: Triple) -> bool {
    exact_multiplicities(before, after) && one_of_six_permutations(before, after)
}

pub open spec fn generated_comparator_sortedness(
    boundary: ComparatorBoundary,
    sequence: Triple,
) -> bool {
    comparator_leq(boundary, sequence.e0, sequence.e0)
        && comparator_leq(boundary, sequence.e0, sequence.e1)
        && comparator_leq(boundary, sequence.e0, sequence.e2)
        && comparator_leq(boundary, sequence.e1, sequence.e1)
        && comparator_leq(boundary, sequence.e1, sequence.e2)
        && comparator_leq(boundary, sequence.e2, sequence.e2)
}

pub open spec fn callback_state_after_sort(
    input: SortInput,
    boundary: ComparatorBoundary,
) -> int {
    input.callback_initial_state + boundary.callback_state_delta
}

pub open spec fn active_contract(
    input: SortInput,
    boundary: ComparatorBoundary,
    final_slice: Triple,
    callback_final_state: int,
) -> bool {
    generated_permutation(input.elements, final_slice)
        && generated_comparator_sortedness(boundary, final_slice)
        && callback_final_state == callback_state_after_sort(input, boundary)
}

pub open spec fn reviewed_equal_key_equivalent(
    boundary: ComparatorBoundary,
    left: Triple,
    left_callback_state: int,
    right: Triple,
    right_callback_state: int,
) -> bool {
    left_callback_state == right_callback_state
        && exact_multiplicities(left, right)
        && comparator_equivalent(boundary, left.e0, right.e0)
        && comparator_equivalent(boundary, left.e1, right.e1)
        && comparator_equivalent(boundary, left.e2, right.e2)
}

pub open spec fn exact_final_slice_equivalent(
    left: Triple,
    left_callback_state: int,
    right: Triple,
    right_callback_state: int,
) -> bool {
    left.e0 == right.e0
        && left.e1 == right.e1
        && left.e2 == right.e2
        && left_callback_state == right_callback_state
}

pub open spec fn dual(left: int, right: int) -> bool {
    (left == -1 && right == 1)
        || (left == 0 && right == 0)
        || (left == 1 && right == -1)
}

pub open spec fn leq_transitive(left_middle: int, middle_right: int, left_right: int) -> bool {
    (left_middle <= 0 && middle_right <= 0) ==> left_right <= 0
}

pub open spec fn total_order_profile(
    input: SortInput,
    boundary: ComparatorBoundary,
) -> bool {
    boundary_ids_match(input, boundary)
        && boundary.c00 == 0
        && boundary.c11 == 0
        && boundary.c22 == 0
        && dual(boundary.c01, boundary.c10)
        && dual(boundary.c02, boundary.c20)
        && dual(boundary.c12, boundary.c21)
        && leq_transitive(boundary.c00, boundary.c00, boundary.c00)
        && leq_transitive(boundary.c00, boundary.c01, boundary.c01)
        && leq_transitive(boundary.c00, boundary.c02, boundary.c02)
        && leq_transitive(boundary.c01, boundary.c10, boundary.c00)
        && leq_transitive(boundary.c01, boundary.c11, boundary.c01)
        && leq_transitive(boundary.c01, boundary.c12, boundary.c02)
        && leq_transitive(boundary.c02, boundary.c20, boundary.c00)
        && leq_transitive(boundary.c02, boundary.c21, boundary.c01)
        && leq_transitive(boundary.c02, boundary.c22, boundary.c02)
        && leq_transitive(boundary.c10, boundary.c00, boundary.c10)
        && leq_transitive(boundary.c10, boundary.c01, boundary.c11)
        && leq_transitive(boundary.c10, boundary.c02, boundary.c12)
        && leq_transitive(boundary.c11, boundary.c10, boundary.c10)
        && leq_transitive(boundary.c11, boundary.c11, boundary.c11)
        && leq_transitive(boundary.c11, boundary.c12, boundary.c12)
        && leq_transitive(boundary.c12, boundary.c20, boundary.c10)
        && leq_transitive(boundary.c12, boundary.c21, boundary.c11)
        && leq_transitive(boundary.c12, boundary.c22, boundary.c12)
        && leq_transitive(boundary.c20, boundary.c00, boundary.c20)
        && leq_transitive(boundary.c20, boundary.c01, boundary.c21)
        && leq_transitive(boundary.c20, boundary.c02, boundary.c22)
        && leq_transitive(boundary.c21, boundary.c10, boundary.c20)
        && leq_transitive(boundary.c21, boundary.c11, boundary.c21)
        && leq_transitive(boundary.c21, boundary.c12, boundary.c22)
        && leq_transitive(boundary.c22, boundary.c20, boundary.c20)
        && leq_transitive(boundary.c22, boundary.c21, boundary.c21)
        && leq_transitive(boundary.c22, boundary.c22, boundary.c22)
}

pub proof fn exact_final_slice_counterexample() {
    let input = SortInput {
        elements: Triple { e0: 10, e1: 11, e2: 20 },
        callback_initial_state: 7,
    };
    let boundary = ComparatorBoundary {
        id0: 10, id1: 11, id2: 20,
        c00: 0, c01: 0, c02: -1,
        c10: 0, c11: 0, c12: -1,
        c20: 1, c21: 1, c22: 0,
        callback_state_delta: 0,
    };
    let left = Triple { e0: 10, e1: 11, e2: 20 };
    let right = Triple { e0: 11, e1: 10, e2: 20 };
    assert(distinct_input(input));
    assert(boundary_observed(input, boundary));
    assert(active_contract(input, boundary, left, 7));
    assert(active_contract(input, boundary, right, 7));
    assert(reviewed_equal_key_equivalent(boundary, left, 7, right, 7));
    assert(!exact_final_slice_equivalent(left, 7, right, 7));
}

pub proof fn general_non_total_counterexample() {
    let input = SortInput {
        elements: Triple { e0: 10, e1: 11, e2: 20 },
        callback_initial_state: 7,
    };
    let boundary = ComparatorBoundary {
        id0: 10, id1: 11, id2: 20,
        c00: 0, c01: -1, c02: -1,
        c10: -1, c11: 0, c12: -1,
        c20: 1, c21: 1, c22: 0,
        callback_state_delta: 0,
    };
    let left = Triple { e0: 10, e1: 11, e2: 20 };
    let right = Triple { e0: 11, e1: 10, e2: 20 };
    assert(distinct_input(input));
    assert(boundary_observed(input, boundary));
    assert(!total_order_profile(input, boundary));
    assert(active_contract(input, boundary, left, 7));
    assert(active_contract(input, boundary, right, 7));
    assert(exact_multiplicities(left, right));
    assert(!reviewed_equal_key_equivalent(boundary, left, 7, right, 7));
}

pub proof fn shared_callback_transition_is_exact(
    input: SortInput,
    boundary: ComparatorBoundary,
)
    requires
        boundary_observed(input, boundary),
    ensures
        callback_state_after_sort(input, boundary) == input.callback_initial_state,
{
}

}
