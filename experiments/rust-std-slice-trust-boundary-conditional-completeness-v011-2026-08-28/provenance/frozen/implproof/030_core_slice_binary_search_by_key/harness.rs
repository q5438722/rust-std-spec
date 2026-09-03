#![allow(dead_code, unused_imports, unused_variables, unused_mut)]
// Target-specific Verus implementation harness.
// Target: core::slice::binary_search_by_key
// Source: core/src/slice/mod.rs:3071-3077
// Source item sha256: 93926d7471959bd2dca6f11321a73a445294b73af7c3748212f85ed08d5c31ae
// Dependency manifest: proof_manifests/030_core_slice_binary_search_by_key/dependency_assumption_manifest.json

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub open spec fn ordering_rank(ordering: core::cmp::Ordering) -> int {
    match ordering {
        core::cmp::Ordering::Less => -1,
        core::cmp::Ordering::Equal => 0,
        core::cmp::Ordering::Greater => 1,
    }
}

pub uninterp spec fn ord_cmp_observed<T: core::cmp::Ord>(
    left: T,
    right: T,
) -> core::cmp::Ordering;

pub uninterp spec fn ord_cmp_ref_observed<T: core::cmp::Ord>(
    left: &T,
    right: &T,
) -> core::cmp::Ordering;

pub open spec fn ord_leq_observed<T: core::cmp::Ord>(left: T, right: T) -> bool {
    ordering_rank(ord_cmp_observed(left, right)) <= 0
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

pub uninterp spec fn fnmut_key_observed<F, T, B>(f: F, value: T) -> B;

pub open spec fn slice_binary_search_by_key_ordered<F, T, B: core::cmp::Ord>(
    seq: Seq<T>,
    f: F,
) -> bool {
    forall|i: int, j: int| #![auto] 0 <= i <= j < seq.len()
        ==> ord_leq_observed(
            fnmut_key_observed::<F, T, B>(f, seq[i]),
            fnmut_key_observed::<F, T, B>(f, seq[j]),
        )
}

pub open spec fn slice_binary_search_by_key_equal_at<F, T, B: core::cmp::Ord>(
    seq: Seq<T>,
    key: B,
    f: F,
    index: usize,
) -> bool {
    index < seq.len()
        && ord_cmp_observed(fnmut_key_observed::<F, T, B>(f, seq[index as int]), key)
            == core::cmp::Ordering::Equal
}

pub open spec fn slice_binary_search_by_key_insertion_point<F, T, B: core::cmp::Ord>(
    seq: Seq<T>,
    key: B,
    f: F,
    index: usize,
) -> bool {
    index <= seq.len()
        && forall|j: int| #![auto] 0 <= j < index as int
            ==> ord_cmp_observed(fnmut_key_observed::<F, T, B>(f, seq[j]), key)
                == core::cmp::Ordering::Less
        && forall|j: int| #![auto] index as int <= j < seq.len()
            ==> ord_cmp_observed(fnmut_key_observed::<F, T, B>(f, seq[j]), key)
                == core::cmp::Ordering::Greater
}

pub open spec fn slice_binary_search_by_key_result<F, T, B: core::cmp::Ord>(
    seq: Seq<T>,
    key: B,
    f: F,
    result: core::result::Result<usize, usize>,
) -> bool {
    &&& match result {
        core::result::Result::Ok(index) => index < seq.len(),
        core::result::Result::Err(index) => index <= seq.len(),
    }
    &&& slice_binary_search_by_key_ordered::<F, T, B>(seq, f) ==> match result {
        core::result::Result::Ok(index) => {
            slice_binary_search_by_key_equal_at::<F, T, B>(seq, key, f, index)
        },
        core::result::Result::Err(index) => {
            slice_binary_search_by_key_insertion_point::<F, T, B>(seq, key, f, index)
        },
    }
}

#[verifier::external_body]
pub fn rust_1_96_binary_search_by_key_delegate<'a, T, B: core::cmp::Ord, F>(
    slice: &'a [T],
    b: &B,
    f: F,
) -> (result: core::result::Result<usize, usize>)
    where
        F: FnMut(&'a T) -> B,
    ensures
        match result {
            core::result::Result::Ok(index) => index < slice@.len(),
            core::result::Result::Err(index) => index <= slice@.len(),
        },
{
    loop {
    }
}

#[verifier::external_body]
pub proof fn rust_1_96_binary_search_by_key_result_bridge<F, T, B: core::cmp::Ord>(
    seq: Seq<T>,
    key: B,
    f: F,
    result: core::result::Result<usize, usize>,
)
    requires
        match result {
            core::result::Result::Ok(index) => index < seq.len(),
            core::result::Result::Err(index) => index <= seq.len(),
        },
    ensures
        slice_binary_search_by_key_result::<F, T, B>(seq, key, f, result),
{
}

pub fn binary_search_by_key<'a, T, B: core::cmp::Ord, F>(
    slice: &'a [T],
    b: &B,
    f: F,
) -> (result: core::result::Result<usize, usize>)
    where
        F: FnMut(&'a T) -> B,
    ensures
        slice_binary_search_by_key_result::<F, T, B>(slice@, *b, f, result),
{
    let ghost callback = f;
    let ghost key = *b;
    let result = rust_1_96_binary_search_by_key_delegate(slice, b, f);
    proof {
        assert(match result {
            core::result::Result::Ok(index) => index < slice@.len(),
            core::result::Result::Err(index) => index <= slice@.len(),
        });
        rust_1_96_binary_search_by_key_result_bridge(slice@, key, callback, result);
    }
    result
}

}
