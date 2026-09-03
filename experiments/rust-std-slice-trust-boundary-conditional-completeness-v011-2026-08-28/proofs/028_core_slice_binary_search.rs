#![allow(dead_code, unused_imports, unused_variables)]
// Experiment-local length-two source-transition model for core::slice::binary_search.

use vstd::prelude::*;

verus! {

pub ghost struct SearchInput {
    pub element0: int,
    pub element1: int,
    pub search_value: int,
    pub callback_initial_state: int,
}

pub ghost struct SearchBoundary {
    pub read0: int,
    pub read1: int,
    pub cmp0: int,
    pub cmp1: int,
    pub state_delta0: int,
    pub state_delta1: int,
}

pub ghost struct SearchResult {
    pub is_ok: bool,
    pub index: int,
}

pub open spec fn ord_compare(left: int, right: int) -> int {
    if left < right {
        -1
    } else if left == right {
        0
    } else {
        1
    }
}

pub open spec fn boundary_observed(
    input: SearchInput,
    boundary: SearchBoundary,
) -> bool {
    boundary.read0 == input.element0
        && boundary.read1 == input.element1
        && boundary.cmp0 == ord_compare(boundary.read0, input.search_value)
        && boundary.cmp1 == ord_compare(boundary.read1, input.search_value)
        && -1 <= boundary.state_delta0 <= 1
        && -1 <= boundary.state_delta1 <= 1
}

pub open spec fn slice_sorted_by_ord(
    input: SearchInput,
    boundary: SearchBoundary,
) -> bool {
    boundary.read0 <= boundary.read1
}

pub open spec fn comparator_profile_ordered(boundary: SearchBoundary) -> bool {
    boundary.cmp0 <= boundary.cmp1
}

pub open spec fn result_in_bounds(result: SearchResult) -> bool {
    0 <= result.index && if result.is_ok {
        result.index < 2
    } else {
        result.index <= 2
    }
}

pub open spec fn equal_at(boundary: SearchBoundary, index: int) -> bool {
    0 <= index < 2 && if index == 0 {
        boundary.cmp0 == 0
    } else {
        boundary.cmp1 == 0
    }
}

pub open spec fn insertion_point(
    boundary: SearchBoundary,
    index: int,
) -> bool {
    0 <= index <= 2
        && (index > 0 ==> boundary.cmp0 == -1)
        && (index > 1 ==> boundary.cmp1 == -1)
        && (index <= 0 ==> boundary.cmp0 == 1)
        && (index <= 1 ==> boundary.cmp1 == 1)
}

pub open spec fn generated_binary_search_result(
    input: SearchInput,
    boundary: SearchBoundary,
    result: SearchResult,
) -> bool {
    result_in_bounds(result)
        && (slice_sorted_by_ord(input, boundary) ==> if result.is_ok {
                equal_at(boundary, result.index)
            } else {
                insertion_point(boundary, result.index)
            })
}

pub open spec fn reviewed_binary_search_by_lower_result(
    boundary: SearchBoundary,
    result: SearchResult,
) -> bool {
    result_in_bounds(result)
        && (comparator_profile_ordered(boundary) ==> if result.is_ok {
                equal_at(boundary, result.index)
            } else {
                insertion_point(boundary, result.index)
            })
}

pub open spec fn callback_state_after_two(
    input: SearchInput,
    boundary: SearchBoundary,
) -> int {
    input.callback_initial_state
        + boundary.state_delta0
        + boundary.state_delta1
}

pub open spec fn source_backed_binary_search_wrapper(
    input: SearchInput,
    boundary: SearchBoundary,
    result: SearchResult,
    callback_final_state: int,
) -> bool {
    boundary_observed(input, boundary)
        && generated_binary_search_result(input, boundary, result)
        && reviewed_binary_search_by_lower_result(boundary, result)
        && callback_final_state == callback_state_after_two(input, boundary)
}

pub proof fn ord_comparison_adapter_is_exact(
    input: SearchInput,
    boundary: SearchBoundary,
)
    requires
        boundary_observed(input, boundary),
    ensures
        boundary.cmp0 == ord_compare(input.element0, input.search_value),
        boundary.cmp1 == ord_compare(input.element1, input.search_value),
{
}

pub proof fn wrapper_uses_reviewed_lower_relation(
    input: SearchInput,
    boundary: SearchBoundary,
    result: SearchResult,
)
    requires
        source_backed_binary_search_wrapper(input, boundary, result, 0),
    ensures
        reviewed_binary_search_by_lower_result(boundary, result),
{
}

pub proof fn shared_wrapper_state_is_exact(
    input: SearchInput,
    boundary: SearchBoundary,
    left: SearchResult,
    right: SearchResult,
    left_state: int,
    right_state: int,
)
    requires
        source_backed_binary_search_wrapper(input, boundary, left, left_state),
        source_backed_binary_search_wrapper(input, boundary, right, right_state),
    ensures
        left_state == right_state,
{
}

}
