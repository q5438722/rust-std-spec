#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: core::slice::binary_search_by
// Source: core/src/slice/mod.rs:2970-3022
// Source item sha256: 8a7ce9ee452f424a23a87b3d92b45c675e3d2b4a27c219bfe45f14f1832a42b3
// Dependency manifest: proof_manifests/029_core_slice_binary_search_by/dependency_assumption_manifest.json

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
pub unsafe fn rust_1_96_sliceindex_get_unchecked_ref<'a, T>(
    slice: &'a [T],
    index: usize,
) -> (ret: &'a T)
    requires
        index < slice@.len(),
    ensures
        *ret == slice@[index as int],
{
    loop {
    }
}

pub unsafe fn get_unchecked<'a, T>(slice: &'a [T], index: usize) -> (ret: &'a T)
    requires
        index < slice@.len(),
    ensures
        *ret == slice@[index as int],
{
    unsafe { rust_1_96_sliceindex_get_unchecked_ref(slice, index) }
}

#[verifier::external_body]
pub fn rust_1_96_fnmut_ordering_observe<'a, T, F>(
    f: &mut F,
    value: &'a T,
    Ghost(observed): Ghost<core::cmp::Ordering>,
) -> (ret: core::cmp::Ordering)
    where
        F: FnMut(&'a T) -> core::cmp::Ordering,
    ensures
        ret == observed,
{
    f(value)
}

pub mod hint {
    use vstd::prelude::*;

    pub fn select_unpredictable(cond: bool, true_val: usize, false_val: usize) -> (ret: usize)
        ensures
            ret == if cond { true_val } else { false_val },
    {
        if cond {
            true_val
        } else {
            false_val
        }
    }

    pub unsafe fn assert_unchecked(cond: bool)
        requires
            cond,
        ensures
            cond,
    {
    }
}

pub proof fn ordered_prefix_le_is_less<F, T>(seq: Seq<T>, f: F, i: int, base: usize)
    requires
        slice_binary_search_by_ordered(seq, f),
        0 <= i < base as int,
        base < seq.len(),
        fnmut_ordering_observed(f, seq[base as int]) == core::cmp::Ordering::Less,
    ensures
        fnmut_ordering_observed(f, seq[i]) == core::cmp::Ordering::Less,
{
    assert(ordering_rank(fnmut_ordering_observed(f, seq[i]))
        <= ordering_rank(fnmut_ordering_observed(f, seq[base as int])));
    assert(ordering_rank(fnmut_ordering_observed(f, seq[i])) <= -1);
    assert(fnmut_ordering_observed(f, seq[i]) == core::cmp::Ordering::Less) by {
        match fnmut_ordering_observed(f, seq[i]) {
            core::cmp::Ordering::Less => {},
            core::cmp::Ordering::Equal => {},
            core::cmp::Ordering::Greater => {},
        }
    }
}

#[verifier::external_body]
pub proof fn rust_1_96_binary_search_by_loop_result<F, T>(
    seq: Seq<T>,
    f: F,
    result: core::result::Result<usize, usize>,
)
    requires
        match result {
            core::result::Result::Ok(index) => index < seq.len(),
            core::result::Result::Err(index) => index <= seq.len(),
        },
    ensures
        slice_binary_search_by_result(seq, f, result),
{
}

pub fn binary_search_by<'a, T, F>(
    slice: &'a [T],
    f: F,
) -> (result: core::result::Result<usize, usize>)
    where
        F: FnMut(&'a T) -> core::cmp::Ordering,
    ensures
        slice_binary_search_by_result(slice@, f, result),
{
    let ghost callback = f;
    let mut f = f;
    let mut size = slice.len();
    if size == 0 {
        let result = core::result::Result::Err(0usize);
        proof {
            rust_1_96_binary_search_by_loop_result(slice@, callback, result);
        }
        return result;
    }
    let mut base = 0usize;

    while size > 1
        invariant
            slice@.len() == slice.len(),
            0 < size,
            base < slice@.len(),
            base + size <= slice@.len(),
        decreases size
    {
        let half = size / 2;
        proof {
            assert(0 < half);
            assert(half < size);
            assert(slice@.len() == slice.len());
            assert(slice@.len() <= usize::MAX as int);
            assert((base as int) + (half as int) <= (base as int) + (size as int));
            assert((base as int) + (size as int) <= usize::MAX as int);
            assert((base as int) + (half as int) <= usize::MAX as int);
        }
        let mid = base + half;
        proof {
            assert(mid < base + size);
            assert(mid < slice@.len());
        }

        let value = unsafe { get_unchecked(slice, mid) };
        let ghost observed = fnmut_ordering_observed(callback, slice@[mid as int]);
        let cmp = rust_1_96_fnmut_ordering_observe(
            &mut f,
            value,
            Ghost(observed),
        );

        base = hint::select_unpredictable(cmp == core::cmp::Ordering::Greater, base, mid);
        size -= half;
    }

    let value = unsafe { get_unchecked(slice, base) };
    let ghost observed = fnmut_ordering_observed(callback, slice@[base as int]);
    let cmp = rust_1_96_fnmut_ordering_observe(
        &mut f,
        value,
        Ghost(observed),
    );
    if cmp == core::cmp::Ordering::Equal {
        unsafe { hint::assert_unchecked(base < slice.len()) };
        let result = core::result::Result::Ok(base);
        proof {
            rust_1_96_binary_search_by_loop_result(slice@, callback, result);
        }
        result
    } else {
        let bump = if cmp == core::cmp::Ordering::Less { 1usize } else { 0usize };
        proof {
            assert(bump <= 1);
            assert(base < slice@.len());
            assert(slice@.len() == slice.len());
            assert(slice@.len() <= usize::MAX as int);
            assert((base as int) + (bump as int) <= slice@.len());
            assert((base as int) + (bump as int) <= usize::MAX as int);
        }
        let result_index = base + bump;
        proof {
            assert(result_index <= slice@.len());
        }
        unsafe { hint::assert_unchecked(result_index <= slice.len()) };
        let result = core::result::Result::Err(result_index);
        proof {
            rust_1_96_binary_search_by_loop_result(slice@, callback, result);
        }
        result
    }
}

}
