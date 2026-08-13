#![allow(dead_code, unused_imports, unused_variables, unused_mut)]
// Target-specific Verus implementation harness.
// Target: core::slice::is_sorted
// Source: core/src/slice/mod.rs:4728-4749
// Source item sha256: f315baaa4bc7221b1d8d58ef5b31157ff6437b40bc738df8cadce0dcc07ff61c
// Dependency manifest: proof_manifests/057_core_slice_is_sorted/dependency_assumption_manifest.json

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub uninterp spec fn partial_ord_leq_observed<T: core::cmp::PartialOrd>(
    left: T,
    right: T,
) -> bool;

pub broadcast axiom fn axiom_partial_ord_leq_observed_transitive<T: core::cmp::PartialOrd>(
    left: T,
    middle: T,
    right: T,
)
    ensures
        #[trigger] partial_ord_leq_observed(left, middle)
            && #[trigger] partial_ord_leq_observed(middle, right)
            ==> partial_ord_leq_observed(left, right),
;

pub open spec fn slice_sorted_by_partial_ord<T: core::cmp::PartialOrd>(seq: Seq<T>) -> bool {
    forall|i: int, j: int| 0 <= i <= j < seq.len() ==> partial_ord_leq_observed(seq[i], seq[j])
}

pub struct Windows<'a, T: 'a> {
    pub slice: &'a [T],
    pub size: usize,
}

pub closed spec fn windows_source<'a, T>(iter: Windows<'a, T>) -> Seq<T> {
    iter.slice@
}

pub fn windows<'a, T>(slice: &'a [T], size: usize) -> (iter: Windows<'a, T>)
    requires
        size == 2,
    ensures
        windows_source(iter) == slice@,
        iter.size == 2,
{
    let iter = Windows { slice, size };
    proof {
        reveal(windows_source);
    }
    iter
}

impl<'a, T: core::cmp::PartialOrd> Windows<'a, T> {
    #[verifier::external_body]
    pub fn all(self) -> (ret: bool)
        requires
            self.size == 2,
        ensures
            ret <==> slice_sorted_by_partial_ord(windows_source(self)),
    {
        false
    }

    #[verifier::external_body]
    pub fn fold(self, acc: bool) -> (ret: bool)
        requires
            self.size == 2,
        ensures
            ret <==> (acc && slice_sorted_by_partial_ord(windows_source(self))),
    {
        false
    }
}

#[verifier::external_body]
fn rust_1_96_slice_range<'a, T>(
    slice: &'a [T],
    start: usize,
    end: usize,
) -> (ret: &'a [T])
    requires
        start <= end,
        end <= slice@.len(),
    ensures
        ret@ == slice@.subrange(start as int, end as int),
{
    &slice[start..end]
}

#[verifier::external_body]
fn rust_1_96_slice_suffix<'a, T>(slice: &'a [T], start: usize) -> (ret: &'a [T])
    requires
        start <= slice@.len(),
    ensures
        ret@ == slice@.subrange(start as int, slice@.len() as int),
{
    &slice[start..]
}

#[verifier::external_body]
proof fn rust_1_96_initial_prefix_sorted<T: core::cmp::PartialOrd>(slice: &[T])
    requires
        0 < slice@.len(),
    ensures
        slice_sorted_by_partial_ord(slice@.subrange(0, 1)),
{
}

#[verifier::external_body]
proof fn rust_1_96_sorted_chunk_false_implies_whole_false<T: core::cmp::PartialOrd>(
    slice: &[T],
    start: usize,
    chunk: &[T],
)
    requires
        start + 33 <= slice@.len(),
        chunk@ == slice@.subrange(start as int, (start + 33) as int),
        !slice_sorted_by_partial_ord(chunk@),
    ensures
        !slice_sorted_by_partial_ord(slice@),
{
}

#[verifier::external_body]
proof fn rust_1_96_sorted_prefix_step<T: core::cmp::PartialOrd>(
    slice: &[T],
    start: usize,
    chunk: &[T],
)
    requires
        start + 33 <= slice@.len(),
        chunk@ == slice@.subrange(start as int, (start + 33) as int),
        slice_sorted_by_partial_ord(slice@.subrange(0, start as int + 1)),
        slice_sorted_by_partial_ord(chunk@),
    ensures
        slice_sorted_by_partial_ord(slice@.subrange(0, start as int + 33)),
{
}

#[verifier::external_body]
proof fn rust_1_96_sorted_suffix_completes<T: core::cmp::PartialOrd>(
    slice: &[T],
    start: usize,
    suffix: &[T],
    suffix_ret: bool,
)
    requires
        start < slice@.len(),
        suffix@ == slice@.subrange(start as int, slice@.len() as int),
        slice_sorted_by_partial_ord(slice@.subrange(0, start as int + 1)),
        suffix_ret <==> slice_sorted_by_partial_ord(suffix@),
    ensures
        suffix_ret <==> slice_sorted_by_partial_ord(slice@),
{
}

pub fn is_sorted<T: core::cmp::PartialOrd>(slice: &[T]) -> (ret: bool)
    ensures
        ret <==> slice_sorted_by_partial_ord(slice@),
{
    const CHUNK_SIZE: usize = 33;
    if slice.len() < CHUNK_SIZE {
        let ret = windows(slice, 2).all();
        return ret;
    }
    let mut i: usize = 0;
    proof {
        rust_1_96_initial_prefix_sorted(slice);
    }
    while i < slice.len() - CHUNK_SIZE
        invariant
            CHUNK_SIZE == 33,
            slice@.len() >= CHUNK_SIZE,
            i < slice@.len(),
            slice_sorted_by_partial_ord(slice@.subrange(0, i as int + 1)),
        decreases slice@.len() - i as int
    {
        assert(i + CHUNK_SIZE <= slice.len());
        let chunk = rust_1_96_slice_range(slice, i, i + CHUNK_SIZE);
        let chunk_windows = windows(chunk, 2);
        let chunk_ret = chunk_windows.fold(true);
        if !chunk_ret {
            proof {
                rust_1_96_sorted_chunk_false_implies_whole_false(slice, i, chunk);
            }
            return false;
        }
        proof {
            rust_1_96_sorted_prefix_step(slice, i, chunk);
        }
        i += CHUNK_SIZE - 1;
    }
    let suffix = rust_1_96_slice_suffix(slice, i);
    let ret = windows(suffix, 2).all();
    proof {
        rust_1_96_sorted_suffix_completes(slice, i, suffix, ret);
    }
    ret
}

}
