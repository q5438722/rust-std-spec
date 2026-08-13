#![allow(dead_code, unused_imports, unused_variables)]
// Target-specific Verus implementation harness.
// Target: core::slice::ends_with
// Source: core/src/slice/mod.rs:2650-2656 and slice PartialEq at core/src/slice/cmp.rs:15-141
// Source item sha256: 6a17b701400fc0fdbc72078c3d1aacb5815500e39b414cf67197241c67d8a286
// Dependency manifest: proof_manifests/040_core_slice_ends_with/dependency_assumption_manifest.json

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub uninterp spec fn partial_eq_observed<T: core::cmp::PartialEq>(left: T, right: T) -> bool;

pub open spec fn slice_is_suffix<T: core::cmp::PartialEq>(seq: Seq<T>, suffix: Seq<T>) -> bool {
    suffix.len() <= seq.len()
        && forall|i: int| 0 <= i < suffix.len()
            ==> partial_eq_observed(seq[(seq.len() - suffix.len()) as int + i], suffix[i])
}

#[verifier::external_body]
fn rust_1_96_needle_eq_slice_suffix<T: core::cmp::PartialEq>(
    needle: &[T],
    slice: &[T],
    m: usize,
    n: usize,
) -> (b: bool)
    requires
        m as int == slice@.len(),
        n as int == needle@.len(),
        n <= m,
    ensures
        b <==> slice_is_suffix(slice@, needle@),
{
    needle == &slice[m - n..]
}

pub fn ends_with<T: core::cmp::PartialEq>(slice: &[T], needle: &[T]) -> (b: bool)
    ensures
        b <==> slice_is_suffix(slice@, needle@),
{
    let (m, n) = (slice.len(), needle.len());
    let b = m >= n && rust_1_96_needle_eq_slice_suffix(needle, slice, m, n);
    proof {
        if !(m >= n) {
            assert(n as int > m as int);
            assert(needle@.len() > slice@.len());
            assert(!slice_is_suffix(slice@, needle@));
        }
    }
    b
}

}
