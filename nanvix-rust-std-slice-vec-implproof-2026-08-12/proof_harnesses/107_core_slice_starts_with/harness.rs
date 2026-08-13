#![allow(dead_code, unused_imports, unused_variables)]
// Target-specific Verus implementation harness.
// Target: core::slice::starts_with
// Source: core/src/slice/mod.rs:2619-2625 and slice PartialEq at core/src/slice/cmp.rs:15-141
// Source item sha256: 9a120d4acce55ba9b7468313ef3db74e272a271fd9d49bd03b04daa3260f4ca3
// Dependency manifest: proof_manifests/107_core_slice_starts_with/dependency_assumption_manifest.json

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub uninterp spec fn partial_eq_observed<T: core::cmp::PartialEq>(left: T, right: T) -> bool;

pub open spec fn slice_is_prefix<T: core::cmp::PartialEq>(seq: Seq<T>, prefix: Seq<T>) -> bool {
    prefix.len() <= seq.len()
        && forall|i: int| 0 <= i < prefix.len() ==> partial_eq_observed(seq[i], prefix[i])
}

#[verifier::external_body]
fn rust_1_96_needle_eq_slice_prefix<T: core::cmp::PartialEq>(
    needle: &[T],
    slice: &[T],
    n: usize,
) -> (b: bool)
    requires
        n as int == needle@.len(),
        n <= slice@.len(),
    ensures
        b <==> slice_is_prefix(slice@, needle@),
{
    needle == &slice[..n]
}

pub fn starts_with<T: core::cmp::PartialEq>(slice: &[T], needle: &[T]) -> (b: bool)
    ensures
        b <==> slice_is_prefix(slice@, needle@),
{
    let n = needle.len();
    let b = slice.len() >= n && rust_1_96_needle_eq_slice_prefix(needle, slice, n);
    proof {
        if !(slice.len() >= n) {
            assert(n as int > slice@.len());
            assert(needle@.len() > slice@.len());
            assert(!slice_is_prefix(slice@, needle@));
        }
    }
    b
}

}
