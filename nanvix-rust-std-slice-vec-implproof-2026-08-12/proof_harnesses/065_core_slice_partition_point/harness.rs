#![allow(dead_code, unused_imports, unused_variables, unused_mut)]
// Target-specific Verus implementation harness.
// Target: core::slice::partition_point
// Source: core/src/slice/mod.rs:4854-4859
// Source item sha256: 989bce474e90ae13596dd90fece85ddea4a8f612de8833a19f06e60087c06066
// Dependency manifest: proof_manifests/065_core_slice_partition_point/dependency_assumption_manifest.json

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub uninterp spec fn fnmut_predicate_observed<F, T>(pred: F, value: T) -> bool;

pub open spec fn slice_partitioned_by_predicate<F, T>(seq: Seq<T>, pred: F) -> bool {
    forall|i: int, j: int| #![auto] 0 <= i <= j < seq.len()
        ==> fnmut_predicate_observed(pred, seq[j]) ==> fnmut_predicate_observed(pred, seq[i])
}

pub open spec fn slice_partition_point_result<F, T>(seq: Seq<T>, pred: F, index: usize) -> bool {
    &&& index <= seq.len()
    &&& slice_partitioned_by_predicate(seq, pred) ==> {
        &&& forall|j: int| #![auto] 0 <= j < index as int ==> fnmut_predicate_observed(pred, seq[j])
        &&& forall|j: int| #![auto] index as int <= j < seq.len() ==> !fnmut_predicate_observed(pred, seq[j])
    }
}

pub open spec fn slice_partition_point_binary_search_result<F, T>(
    seq: Seq<T>,
    pred: F,
    result: core::result::Result<usize, usize>,
) -> bool {
    &&& match result {
        core::result::Result::Ok(index) => index < seq.len(),
        core::result::Result::Err(index) => index <= seq.len(),
    }
    &&& slice_partitioned_by_predicate(seq, pred) ==> match result {
        core::result::Result::Ok(_index) => false,
        core::result::Result::Err(index) => {
            &&& forall|j: int| #![auto] 0 <= j < index as int ==> fnmut_predicate_observed(pred, seq[j])
            &&& forall|j: int| #![auto] index as int <= j < seq.len() ==> !fnmut_predicate_observed(pred, seq[j])
        },
    }
}

#[verifier::external_body]
pub fn rust_1_96_fnmut_predicate_observe<'a, T, P>(
    pred: &mut P,
    value: &'a T,
    Ghost(observed): Ghost<bool>,
) -> (ret: bool)
    where
        P: FnMut(&'a T) -> bool,
    ensures
        ret == observed,
{
    pred(value)
}

#[verifier::external_body]
pub fn rust_1_96_partition_point_binary_search_by_predicate<'a, T, P>(
    slice: &'a [T],
    pred: P,
) -> (result: core::result::Result<usize, usize>)
    where
        P: FnMut(&'a T) -> bool,
    ensures
        slice_partition_point_binary_search_result(slice@, pred, result),
{
    loop {
    }
}

#[verifier::external_body]
pub proof fn rust_1_96_partition_point_result_bridge<F, T>(
    seq: Seq<T>,
    pred: F,
    result: core::result::Result<usize, usize>,
    index: usize,
)
    requires
        slice_partition_point_binary_search_result(seq, pred, result),
        match result {
            core::result::Result::Ok(found) => index == found,
            core::result::Result::Err(insertion) => index == insertion,
        },
    ensures
        slice_partition_point_result(seq, pred, index),
{
}

pub fn partition_point<'a, T, P>(
    slice: &'a [T],
    pred: P,
) -> (index: usize)
    where
        P: FnMut(&'a T) -> bool,
    ensures
        slice_partition_point_result(slice@, pred, index),
{
    let ghost callback = pred;
    let result = rust_1_96_partition_point_binary_search_by_predicate(slice, pred);
    let index = match result {
        core::result::Result::Ok(found) => found,
        core::result::Result::Err(insertion) => insertion,
    };
    proof {
        rust_1_96_partition_point_result_bridge(slice@, callback, result, index);
    }
    index
}

}
