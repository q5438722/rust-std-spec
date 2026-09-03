#![allow(dead_code, unused_imports, unused_variables)]
// Experiment-local length-two source-transition model for partition_point.

use vstd::prelude::*;

verus! {

pub ghost struct SearchInput {
    pub element0: int,
    pub element1: int,
    pub callback_initial_state: int,
}

pub ghost struct SearchBoundary {
    pub read0: int,
    pub read1: int,
    pub pred0: bool,
    pub pred1: bool,
    pub state_delta0: int,
    pub state_delta1: int,
}

pub ghost struct LowerResult {
    pub is_ok: bool,
    pub index: int,
}

pub open spec fn predicate_to_ordering(value: bool) -> int {
    if value {
        -1
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
        && -1 <= boundary.state_delta0 <= 1
        && -1 <= boundary.state_delta1 <= 1
}

pub open spec fn predicate_profile_partitioned(
    boundary: SearchBoundary,
) -> bool {
    boundary.pred1 ==> boundary.pred0
}

pub open spec fn partition_point_at(
    boundary: SearchBoundary,
    index: int,
) -> bool {
    0 <= index <= 2
        && (index > 0 ==> boundary.pred0)
        && (index > 1 ==> boundary.pred1)
        && (index <= 0 ==> !boundary.pred0)
        && (index <= 1 ==> !boundary.pred1)
}

pub open spec fn generated_partition_point_result(
    boundary: SearchBoundary,
    index: int,
) -> bool {
    0 <= index <= 2
        && (predicate_profile_partitioned(boundary)
            ==> partition_point_at(boundary, index))
}

pub open spec fn lower_equal_at(
    boundary: SearchBoundary,
    index: int,
) -> bool {
    0 <= index < 2
        && if index == 0 {
            predicate_to_ordering(boundary.pred0) == 0
        } else {
            predicate_to_ordering(boundary.pred1) == 0
        }
}

pub open spec fn lower_insertion_point(
    boundary: SearchBoundary,
    index: int,
) -> bool {
    0 <= index <= 2
        && (index > 0 ==> predicate_to_ordering(boundary.pred0) == -1)
        && (index > 1 ==> predicate_to_ordering(boundary.pred1) == -1)
        && (index <= 0 ==> predicate_to_ordering(boundary.pred0) == 1)
        && (index <= 1 ==> predicate_to_ordering(boundary.pred1) == 1)
}

pub open spec fn reviewed_binary_search_by_lower_result(
    boundary: SearchBoundary,
    result: LowerResult,
) -> bool {
    0 <= result.index
        && (if result.is_ok { result.index < 2 } else { result.index <= 2 })
        && (predicate_profile_partitioned(boundary) ==> if result.is_ok {
                lower_equal_at(boundary, result.index)
            } else {
                lower_insertion_point(boundary, result.index)
            })
}

pub open spec fn unwrap_or_else_identity(result: LowerResult) -> int {
    result.index
}

pub open spec fn callback_state_after_two(
    input: SearchInput,
    boundary: SearchBoundary,
) -> int {
    input.callback_initial_state
        + boundary.state_delta0
        + boundary.state_delta1
}

pub open spec fn source_backed_partition_point_wrapper(
    input: SearchInput,
    boundary: SearchBoundary,
    lower: LowerResult,
    index: int,
    callback_final_state: int,
) -> bool {
    boundary_observed(input, boundary)
        && reviewed_binary_search_by_lower_result(boundary, lower)
        && index == unwrap_or_else_identity(lower)
        && generated_partition_point_result(boundary, index)
        && callback_final_state == callback_state_after_two(input, boundary)
}

pub proof fn predicate_adapter_never_returns_equal(value: bool)
    ensures
        predicate_to_ordering(value) != 0,
{
}

pub proof fn unwrap_or_else_is_identity(result: LowerResult)
    ensures
        unwrap_or_else_identity(result) == result.index,
{
}

pub proof fn shared_wrapper_state_is_exact(
    input: SearchInput,
    boundary: SearchBoundary,
    left_lower: LowerResult,
    right_lower: LowerResult,
    left_index: int,
    right_index: int,
    left_state: int,
    right_state: int,
)
    requires
        source_backed_partition_point_wrapper(
            input,
            boundary,
            left_lower,
            left_index,
            left_state,
        ),
        source_backed_partition_point_wrapper(
            input,
            boundary,
            right_lower,
            right_index,
            right_state,
        ),
    ensures
        left_state == right_state,
{
}

}
