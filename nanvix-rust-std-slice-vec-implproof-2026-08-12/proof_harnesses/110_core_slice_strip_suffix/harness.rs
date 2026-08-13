#![allow(dead_code, unused_imports, unused_variables)]
// Target-specific Verus implementation harness.
// Target: core::slice::strip_suffix
// Source: core/src/slice/mod.rs:2718-2732 and slice PartialEq at core/src/slice/cmp.rs:15-141
// Source item sha256: 517595475ca76b58663611a50c279eec8e61de8b766685bd38c81d915dba7dfe
// Dependency manifest: proof_manifests/110_core_slice_strip_suffix/dependency_assumption_manifest.json

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub uninterp spec fn partial_eq_observed<T: core::cmp::PartialEq>(left: T, right: T) -> bool;

pub open spec fn slice_is_suffix<T: core::cmp::PartialEq>(seq: Seq<T>, suffix: Seq<T>) -> bool {
    suffix.len() <= seq.len()
        && forall|i: int| 0 <= i < suffix.len()
            ==> partial_eq_observed(seq[(seq.len() - suffix.len()) as int + i], suffix[i])
}

pub uninterp spec fn slice_pattern_view<P: ?Sized, T: core::cmp::PartialEq>(pattern: &P) -> Seq<T>;

pub open spec fn slice_strip_suffix_result<T: core::cmp::PartialEq>(
    seq: Seq<T>,
    suffix: Seq<T>,
    ret: Option<&[T]>,
) -> bool {
    if slice_is_suffix(seq, suffix) {
        ret.is_some() && ret.unwrap()@ == seq.subrange(0, seq.len() - suffix.len())
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
fn rust_1_96_tail_eq_suffix<T: core::cmp::PartialEq>(
    tail: &[T],
    suffix: &[T],
    slice: &[T],
    len: usize,
    n: usize,
) -> (b: bool)
    requires
        len as int == slice@.len(),
        n as int == suffix@.len(),
        n <= len,
        tail@ == slice@.subrange((len - n) as int, len as int),
    ensures
        b <==> slice_is_suffix(slice@, suffix@),
{
    tail == suffix
}

pub fn strip_suffix<'a, 'p, T, P>(
    slice: &'a [T],
    suffix_pattern: &'p P,
) -> (ret: Option<&'a [T]>)
    where
        T: core::cmp::PartialEq,
        P: SlicePattern<T> + ?Sized,
    ensures
        slice_strip_suffix_result(slice@, slice_pattern_view::<P, T>(suffix_pattern), ret),
{
    let suffix = suffix_pattern.as_slice();
    let (len, n) = (slice.len(), suffix.len());
    if n <= len {
        let ghost source = slice@;
        let (head, tail) = slice.split_at(len - n);
        proof {
            source.lemma_split_at((len - n) as int);
            assert(head@ =~= source.subrange(0, (len - n) as int));
            assert(tail@ =~= source.subrange((len - n) as int, source.len() as int));
            assert(len as int == source.len());
            assert(n as int == suffix@.len());
            assert(suffix@ == slice_pattern_view::<P, T>(suffix_pattern));
        }
        if rust_1_96_tail_eq_suffix(tail, suffix, slice, len, n) {
            proof {
                assert(slice_is_suffix(slice@, suffix@));
                assert(slice_is_suffix(slice@, slice_pattern_view::<P, T>(suffix_pattern)));
                assert(head@ =~= source.subrange(0, source.len() - suffix@.len()));
                assert(head@ =~= source.subrange(
                    0,
                    source.len() - slice_pattern_view::<P, T>(suffix_pattern).len(),
                ));
            }
            return Some(head);
        } else {
            proof {
                assert(!slice_is_suffix(slice@, suffix@));
                assert(!slice_is_suffix(slice@, slice_pattern_view::<P, T>(suffix_pattern)));
            }
        }
    } else {
        proof {
            assert(n as int == suffix@.len());
            assert(suffix@ == slice_pattern_view::<P, T>(suffix_pattern));
            assert(suffix@.len() > slice@.len());
            assert(!slice_is_suffix(slice@, suffix@));
            assert(!slice_is_suffix(slice@, slice_pattern_view::<P, T>(suffix_pattern)));
        }
    }
    None
}

}
