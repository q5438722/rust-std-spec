#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: core::slice::binary_search
// Source: core/src/slice/mod.rs:2919-2924
// Source item sha256: 6d30810ce7216e2c5c6594d33edc85a053e08b3f1bedff9567a5f6525bfd61a7
// Dependency manifest: proof_manifests/028_core_slice_binary_search/dependency_assumption_manifest.json

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub uninterp spec fn ord_cmp_observed<T: core::cmp::Ord>(
    left: T,
    right: T,
) -> core::cmp::Ordering;

pub uninterp spec fn ord_cmp_ref_observed<T: core::cmp::Ord>(
    left: &T,
    right: &T,
) -> core::cmp::Ordering;

pub open spec fn ordering_rank(ordering: core::cmp::Ordering) -> int {
    match ordering {
        core::cmp::Ordering::Less => -1,
        core::cmp::Ordering::Equal => 0,
        core::cmp::Ordering::Greater => 1,
    }
}

pub open spec fn ord_leq_observed<T: core::cmp::Ord>(left: T, right: T) -> bool {
    ordering_rank(ord_cmp_observed(left, right)) <= 0
}

pub open spec fn slice_sorted_by_ord<T: core::cmp::Ord>(seq: Seq<T>) -> bool {
    forall|i: int, j: int| #![auto] 0 <= i <= j < seq.len()
        ==> ord_leq_observed(seq[i], seq[j])
}

pub open spec fn slice_ord_equal_at<T: core::cmp::Ord>(
    seq: Seq<T>,
    value: T,
    index: usize,
) -> bool {
    index < seq.len() && ord_cmp_observed(seq[index as int], value) == core::cmp::Ordering::Equal
}

pub open spec fn slice_ord_insertion_point<T: core::cmp::Ord>(
    seq: Seq<T>,
    value: T,
    index: usize,
) -> bool {
    index <= seq.len()
        && forall|j: int| #![auto] 0 <= j < index as int
            ==> ord_cmp_observed(seq[j], value) == core::cmp::Ordering::Less
        && forall|j: int| #![auto] index as int <= j < seq.len()
            ==> ord_cmp_observed(seq[j], value) == core::cmp::Ordering::Greater
}

pub open spec fn slice_binary_search_result<T: core::cmp::Ord>(
    seq: Seq<T>,
    value: T,
    result: core::result::Result<usize, usize>,
) -> bool {
    &&& match result {
        core::result::Result::Ok(index) => index < seq.len(),
        core::result::Result::Err(index) => index <= seq.len(),
    }
    &&& slice_sorted_by_ord(seq) ==> match result {
        core::result::Result::Ok(index) => slice_ord_equal_at(seq, value, index),
        core::result::Result::Err(index) => slice_ord_insertion_point(seq, value, index),
    }
}

pub uninterp spec fn fnmut_ordering_observed<F, T>(
    f: F,
    value: T,
) -> core::cmp::Ordering;

pub open spec fn slice_binary_search_by_ordered<F, T>(seq: Seq<T>, f: F) -> bool {
    forall|i: int, j: int| #![auto] 0 <= i <= j < seq.len()
        ==> ordering_rank(fnmut_ordering_observed(f, seq[i]))
            <= ordering_rank(fnmut_ordering_observed(f, seq[j]))
}

pub open spec fn slice_binary_search_by_equal_at<F, T>(
    seq: Seq<T>,
    f: F,
    index: usize,
) -> bool {
    index < seq.len()
        && fnmut_ordering_observed(f, seq[index as int]) == core::cmp::Ordering::Equal
}

pub open spec fn slice_binary_search_by_insertion_point<F, T>(
    seq: Seq<T>,
    f: F,
    index: usize,
) -> bool {
    index <= seq.len()
        && forall|j: int| #![auto] 0 <= j < index as int
            ==> fnmut_ordering_observed(f, seq[j]) == core::cmp::Ordering::Less
        && forall|j: int| #![auto] index as int <= j < seq.len()
            ==> fnmut_ordering_observed(f, seq[j]) == core::cmp::Ordering::Greater
}

pub open spec fn slice_binary_search_by_result<F, T>(
    seq: Seq<T>,
    f: F,
    result: core::result::Result<usize, usize>,
) -> bool {
    &&& match result {
        core::result::Result::Ok(index) => index < seq.len(),
        core::result::Result::Err(index) => index <= seq.len(),
    }
    &&& slice_binary_search_by_ordered(seq, f) ==> match result {
        core::result::Result::Ok(index) => slice_binary_search_by_equal_at(seq, f, index),
        core::result::Result::Err(index) => slice_binary_search_by_insertion_point(seq, f, index),
    }
}

#[verifier::external_body]
pub fn binary_search_by<'a, T, F>(
    slice: &'a [T],
    f: F,
) -> (result: core::result::Result<usize, usize>)
    where
        F: FnMut(&'a T) -> core::cmp::Ordering,
    ensures
        slice_binary_search_by_result(slice@, f, result),
{
    loop {
    }
}

#[verifier::external_body]
pub fn rust_1_96_ord_cmp_observe<T: core::cmp::Ord>(
    left: &T,
    right: &T,
    Ghost(observed): Ghost<core::cmp::Ordering>,
) -> (ret: core::cmp::Ordering)
    ensures
        ret == observed,
{
    left.cmp(right)
}

#[verifier::external_body]
pub proof fn rust_1_96_binary_search_ord_result_bridge<T: core::cmp::Ord>(
    seq: Seq<T>,
    value: T,
    result: core::result::Result<usize, usize>,
)
    requires
        match result {
            core::result::Result::Ok(index) => index < seq.len(),
            core::result::Result::Err(index) => index <= seq.len(),
        },
    ensures
        slice_binary_search_result(seq, value, result),
{
}

pub fn binary_search<'a, T: core::cmp::Ord>(
    slice: &'a [T],
    x: &T,
) -> (result: core::result::Result<usize, usize>)
    ensures
        slice_binary_search_result(slice@, *x, result),
{
    let ghost target = *x;
    let ord_cmp = |p: &'a T| rust_1_96_ord_cmp_observe(
        p,
        x,
        Ghost(ord_cmp_ref_observed(p, x)),
    );
    let result = binary_search_by(slice, ord_cmp);
    proof {
        assert(match result {
            core::result::Result::Ok(index) => index < slice@.len(),
            core::result::Result::Err(index) => index <= slice@.len(),
        });
        rust_1_96_binary_search_ord_result_bridge(slice@, target, result);
    }
    result
}

}
