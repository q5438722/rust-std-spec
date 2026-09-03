#![allow(dead_code, unused_imports, unused_variables)]
// Experiment-local source-backed model for core::slice::sort_unstable_by_key.

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

pub ghost struct KeyBoundary {
    pub key0: int,
    pub key1: int,
    pub key2: int,
    pub key0_class: int,
    pub key1_class: int,
    pub key2_class: int,
    pub callback_state_delta: int,
}

pub open spec fn observed_key(boundary: KeyBoundary, identity: int) -> int {
    if identity == 10 {
        boundary.key0
    } else if identity == 11 {
        boundary.key1
    } else {
        boundary.key2
    }
}

pub open spec fn ord_class_of_key(boundary: KeyBoundary, key: int) -> int {
    if key == boundary.key0 {
        boundary.key0_class
    } else if key == boundary.key1 {
        boundary.key1_class
    } else {
        boundary.key2_class
    }
}

pub open spec fn observed_class(boundary: KeyBoundary, identity: int) -> int {
    ord_class_of_key(boundary, observed_key(boundary, identity))
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

pub open spec fn sorted_by_key_class(
    boundary: KeyBoundary,
    sequence: Triple,
) -> bool {
    observed_class(boundary, sequence.e0) <= observed_class(boundary, sequence.e1)
        && observed_class(boundary, sequence.e0) <= observed_class(boundary, sequence.e2)
        && observed_class(boundary, sequence.e1) <= observed_class(boundary, sequence.e2)
}

pub open spec fn active_contract(
    input: SortInput,
    boundary: KeyBoundary,
    final_slice: Triple,
    callback_final_state: int,
) -> bool {
    exact_multiplicities(input.elements, final_slice)
        && sorted_by_key_class(boundary, final_slice)
        && callback_final_state
            == input.callback_initial_state + boundary.callback_state_delta
}

pub open spec fn reviewed_equal_key_equivalent(
    boundary: KeyBoundary,
    left: Triple,
    left_callback_state: int,
    right: Triple,
    right_callback_state: int,
) -> bool {
    left_callback_state == right_callback_state
        && exact_multiplicities(left, right)
        && observed_class(boundary, left.e0) == observed_class(boundary, right.e0)
        && observed_class(boundary, left.e1) == observed_class(boundary, right.e1)
        && observed_class(boundary, left.e2) == observed_class(boundary, right.e2)
}

pub proof fn arbitrary_length_order_statistic_classes_are_unique(
    len: int,
    position: int,
    left_class: int,
    right_class: int,
    left_count_before: int,
    left_count_through: int,
    right_count_before: int,
    right_count_through: int,
)
    requires
        0 < len,
        0 <= position < len,
        0 <= left_class < len,
        0 <= right_class < len,
        left_count_before <= position < left_count_through,
        right_count_before <= position < right_count_through,
        left_class < right_class ==> left_count_through <= right_count_before,
        right_class < left_class ==> right_count_through <= left_count_before,
    ensures
        left_class == right_class,
{
    if left_class < right_class {
        assert(left_count_through <= right_count_before);
        assert(position < left_count_through);
        assert(right_count_before <= position);
        assert(false);
    } else if right_class < left_class {
        assert(right_count_through <= left_count_before);
        assert(position < right_count_through);
        assert(left_count_before <= position);
        assert(false);
    }
}

pub proof fn exact_final_slice_counterexample() {
    let input = SortInput {
        elements: Triple { e0: 10, e1: 11, e2: 20 },
        callback_initial_state: 7,
    };
    let boundary = KeyBoundary {
        key0: 100,
        key1: 100,
        key2: 200,
        key0_class: 0,
        key1_class: 0,
        key2_class: 1,
        callback_state_delta: 0,
    };
    let left = Triple { e0: 10, e1: 11, e2: 20 };
    let right = Triple { e0: 11, e1: 10, e2: 20 };
    assert(active_contract(input, boundary, left, 7));
    assert(active_contract(input, boundary, right, 7));
    assert(reviewed_equal_key_equivalent(boundary, left, 7, right, 7));
    assert(left.e0 != right.e0);
}

pub proof fn unequal_key_class_reordering_is_rejected() {
    let boundary = KeyBoundary {
        key0: 100,
        key1: 100,
        key2: 200,
        key0_class: 0,
        key1_class: 0,
        key2_class: 1,
        callback_state_delta: 0,
    };
    let left = Triple { e0: 10, e1: 11, e2: 20 };
    let right = Triple { e0: 20, e1: 11, e2: 10 };
    assert(exact_multiplicities(left, right));
    assert(!reviewed_equal_key_equivalent(boundary, left, 7, right, 7));
}

}
