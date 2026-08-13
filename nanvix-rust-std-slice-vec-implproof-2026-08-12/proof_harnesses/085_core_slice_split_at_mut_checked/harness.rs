#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: core::slice::split_at_mut_checked
// Source: core/src/slice/mod.rs:2192-2200
// Source item sha256: abfee0fdb5817382bcc578ea7e47395312bd55464b5fb9a4ba5cd32cfd090110
// Dependency manifest: proof_manifests/085_core_slice_split_at_mut_checked/dependency_assumption_manifest.json
//
// The public target body below preserves the Rust 1.96 flow: compare mid with
// self.len(), return Some(unsafe { self.split_at_mut_unchecked(mid) }) when the
// split point is in range, and return None otherwise. The unchecked split's
// final-frame relation is reused as the reviewed source-backed dependency.

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub open spec fn split_point_in_range<T>(source: Seq<T>, mid: usize) -> bool {
    (mid as int) <= source.len()
}

pub open spec fn split_at_mut_unchecked_result<T>(
    source: Seq<T>,
    mid: usize,
    left: Seq<T>,
    right: Seq<T>,
    final_source: Seq<T>,
    final_left: Seq<T>,
    final_right: Seq<T>,
) -> bool {
    left == source.subrange(0, mid as int)
        && right == source.subrange(mid as int, source.len() as int)
        && final_source == final_left + final_right
}

#[verifier::external_body]
pub unsafe fn split_at_mut_unchecked<'a, T>(
    slice: &'a mut [T],
    mid: usize,
) -> (ret: (&'a mut [T], &'a mut [T]))
    requires
        split_point_in_range(old(slice)@, mid),
    ensures
        split_at_mut_unchecked_result(
            old(slice)@,
            mid,
            ret.0@,
            ret.1@,
            final(slice)@,
            final(ret.0)@,
            final(ret.1)@,
        ),
{
    unsafe { slice.split_at_mut_unchecked(mid) }
}

pub fn split_at_mut_checked<'a, T>(
    slice: &'a mut [T],
    mid: usize,
) -> (ret: Option<(&'a mut [T], &'a mut [T])>)
    ensures
        (mid as int) <= old(slice)@.len() ==> ret.is_some()
            && ret.unwrap().0@ == old(slice)@.subrange(0, mid as int)
            && ret.unwrap().1@ == old(slice)@.subrange(mid as int, old(slice)@.len() as int)
            && final(slice)@ == final(ret.unwrap().0)@ + final(ret.unwrap().1)@,
        (mid as int) > old(slice)@.len() ==> ret.is_none()
            && final(slice)@ == old(slice)@,
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
        Some(unsafe { split_at_mut_unchecked(slice, mid) })
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
