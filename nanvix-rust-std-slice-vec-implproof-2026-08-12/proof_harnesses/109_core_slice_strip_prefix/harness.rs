#![allow(dead_code, unused_imports, unused_variables)]
// Target-specific Verus implementation harness.
// Target: core::slice::strip_prefix
// Source: core/src/slice/mod.rs:2682-2696 and slice PartialEq at core/src/slice/cmp.rs:15-141
// Source item sha256: cfc16172d92c4c0822978d8c4fe04790a3a74a48caf9ee68198518b17e1c2500
// Dependency manifest: proof_manifests/109_core_slice_strip_prefix/dependency_assumption_manifest.json

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub uninterp spec fn partial_eq_observed<T: core::cmp::PartialEq>(left: T, right: T) -> bool;

pub open spec fn slice_is_prefix<T: core::cmp::PartialEq>(seq: Seq<T>, prefix: Seq<T>) -> bool {
    prefix.len() <= seq.len()
        && forall|i: int| 0 <= i < prefix.len() ==> partial_eq_observed(seq[i], prefix[i])
}

pub uninterp spec fn slice_pattern_view<P: ?Sized, T: core::cmp::PartialEq>(pattern: &P) -> Seq<T>;

pub open spec fn slice_strip_prefix_result<T: core::cmp::PartialEq>(
    seq: Seq<T>,
    prefix: Seq<T>,
    ret: Option<&[T]>,
) -> bool {
    if slice_is_prefix(seq, prefix) {
        ret.is_some() && ret.unwrap()@ == seq.subrange(prefix.len() as int, seq.len() as int)
    } else {
        ret.is_none()
    }
}

pub trait SlicePattern<T: core::cmp::PartialEq> {
    fn as_slice<'a>(&'a self) -> (ret: &'a [T])
        ensures
            ret@ == slice_pattern_view::<Self, T>(self);
}

#[verifier::external_body]
fn rust_1_96_head_eq_prefix<T: core::cmp::PartialEq>(
    head: &[T],
    prefix: &[T],
    slice: &[T],
    n: usize,
) -> (b: bool)
    requires
        n as int == prefix@.len(),
        n <= slice@.len(),
        head@ == slice@.subrange(0, n as int),
    ensures
        b <==> slice_is_prefix(slice@, prefix@),
{
    head == prefix
}

pub fn strip_prefix<'a, 'p, T, P>(
    slice: &'a [T],
    prefix_pattern: &'p P,
) -> (ret: Option<&'a [T]>)
    where
        T: core::cmp::PartialEq,
        P: SlicePattern<T> + ?Sized,
    ensures
        slice_strip_prefix_result(slice@, slice_pattern_view::<P, T>(prefix_pattern), ret),
{
    let prefix = prefix_pattern.as_slice();
    let n = prefix.len();
    if n <= slice.len() {
        let ghost source = slice@;
        let (head, tail) = slice.split_at(n);
        proof {
            source.lemma_split_at(n as int);
            assert(head@ =~= source.subrange(0, n as int));
            assert(tail@ =~= source.subrange(n as int, source.len() as int));
            assert(n as int == prefix@.len());
            assert(prefix@ == slice_pattern_view::<P, T>(prefix_pattern));
        }
        if rust_1_96_head_eq_prefix(head, prefix, slice, n) {
            proof {
                assert(slice_is_prefix(slice@, prefix@));
                assert(slice_is_prefix(slice@, slice_pattern_view::<P, T>(prefix_pattern)));
                assert(tail@ =~= source.subrange(prefix@.len() as int, source.len() as int));
                assert(tail@ =~= source.subrange(
                    slice_pattern_view::<P, T>(prefix_pattern).len() as int,
                    source.len() as int,
                ));
            }
            return Some(tail);
        } else {
            proof {
                assert(!slice_is_prefix(slice@, prefix@));
                assert(!slice_is_prefix(slice@, slice_pattern_view::<P, T>(prefix_pattern)));
            }
        }
    } else {
        proof {
            assert(n as int == prefix@.len());
            assert(prefix@ == slice_pattern_view::<P, T>(prefix_pattern));
            assert(prefix@.len() > slice@.len());
            assert(!slice_is_prefix(slice@, prefix@));
            assert(!slice_is_prefix(slice@, slice_pattern_view::<P, T>(prefix_pattern)));
        }
    }
    None
}

}
