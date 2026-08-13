#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: core::slice::split_at_checked
// Source: core/src/slice/mod.rs:2153-2161
// Source item sha256: e2f2b49e45a17f5f57ca814cb48944f5a0ac28cb34064a4baa59151c6837ff20
// Dependency manifest: proof_manifests/084_core_slice_split_at_checked/dependency_assumption_manifest.json
//
// The public target body below preserves the Rust 1.96 flow: compare mid with
// self.len(), return Some(unsafe { self.split_at_unchecked(mid) }) when the
// split point is in range, and return None otherwise. The unchecked split
// relation is reused as the reviewed source-backed dependency.

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub open spec fn split_point_in_range<T>(source: Seq<T>, mid: usize) -> bool {
    (mid as int) <= source.len()
}

#[verifier::external_body]
pub unsafe fn split_at_unchecked<'a, T>(
    slice: &'a [T],
    mid: usize,
) -> (ret: (&'a [T], &'a [T]))
    requires
        split_point_in_range(slice@, mid),
    ensures
        ret.0@ == slice@.subrange(0, mid as int),
        ret.1@ == slice@.subrange(mid as int, slice@.len() as int),
{
    unsafe { slice.split_at_unchecked(mid) }
}

pub fn split_at_checked<'a, T>(
    slice: &'a [T],
    mid: usize,
) -> (ret: Option<(&'a [T], &'a [T])>)
    ensures
        (mid as int) <= slice@.len() ==> ret.is_some()
            && ret.unwrap().0@ == slice@.subrange(0, mid as int)
            && ret.unwrap().1@ == slice@.subrange(mid as int, slice@.len() as int),
        (mid as int) > slice@.len() ==> ret.is_none(),
{
    let ghost source = slice@;
    let len = slice.len();
    proof {
        assert(len as int == source.len());
    }

    if mid <= len {
        proof {
            assert((mid as int) <= (len as int));
            assert((mid as int) <= source.len());
            assert(slice@ == source);
            assert(split_point_in_range(slice@, mid));
        }
        Some(unsafe { split_at_unchecked(slice, mid) })
    } else {
        proof {
            assert(!(mid <= len));
            assert((mid as int) > (len as int));
            assert((mid as int) > source.len());
            assert(slice@ == source);
        }
        None
    }
}

}
