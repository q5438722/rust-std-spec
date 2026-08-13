#![allow(dead_code, unused_imports, unused_variables)]
// Target-specific Verus implementation harness.
// Target: core::slice::strip_circumfix
// Source: core/src/slice/mod.rs:2757-2764
// Source item sha256: fe5c9c316e6874a5d08bcb30fbae3ff7c6441e3c725b6b64b15cf5bac2daf953
// Dependency manifest: proof_manifests/108_core_slice_strip_circumfix/dependency_assumption_manifest.json
//
// The public target below is the Verus explicit-return lowering of the Rust
// 1.96 body `self.strip_prefix(prefix)?.strip_suffix(suffix)`.

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub uninterp spec fn partial_eq_observed<T: core::cmp::PartialEq>(left: T, right: T) -> bool;

pub open spec fn slice_is_prefix<T: core::cmp::PartialEq>(seq: Seq<T>, prefix: Seq<T>) -> bool {
    prefix.len() <= seq.len()
        && forall|i: int| 0 <= i < prefix.len() ==> partial_eq_observed(seq[i], prefix[i])
}

pub open spec fn slice_is_suffix<T: core::cmp::PartialEq>(seq: Seq<T>, suffix: Seq<T>) -> bool {
    suffix.len() <= seq.len()
        && forall|i: int| 0 <= i < suffix.len()
            ==> partial_eq_observed(seq[(seq.len() - suffix.len()) as int + i], suffix[i])
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

pub open spec fn slice_strip_suffix_result<T: core::cmp::PartialEq>(
    seq: Seq<T>,
    suffix: Seq<T>,
    ret: Option<&[T]>,
) -> bool {
    if slice_is_suffix(seq, suffix) {
        ret.is_some() && ret.unwrap()@ == seq.subrange(0, (seq.len() - suffix.len()) as int)
    } else {
        ret.is_none()
    }
}

pub open spec fn slice_strip_circumfix_result<T: core::cmp::PartialEq>(
    seq: Seq<T>,
    prefix: Seq<T>,
    suffix: Seq<T>,
    ret: Option<&[T]>,
) -> bool {
    if slice_is_prefix(seq, prefix)
        && slice_is_suffix(seq.subrange(prefix.len() as int, seq.len() as int), suffix)
    {
        ret.is_some()
            && ret.unwrap()@
                == seq.subrange(prefix.len() as int, (seq.len() - suffix.len()) as int)
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

pub fn strip_circumfix<'a, 'p, 's, T, S, P>(
    slice: &'a [T],
    prefix_pattern: &'p P,
    suffix_pattern: &'s S,
) -> (ret: Option<&'a [T]>)
    where
        T: core::cmp::PartialEq,
        S: SlicePattern<T> + ?Sized,
        P: SlicePattern<T> + ?Sized,
    ensures
        slice_strip_circumfix_result(
            slice@,
            slice_pattern_view::<P, T>(prefix_pattern),
            slice_pattern_view::<S, T>(suffix_pattern),
            ret,
        ),
{
    let ghost source = slice@;
    let prefix_ret = strip_prefix(slice, prefix_pattern);
    let Some(stripped) = prefix_ret else {
        proof {
            let prefix = slice_pattern_view::<P, T>(prefix_pattern);
            assert(slice_strip_prefix_result(source, prefix, prefix_ret));
            if slice_is_prefix(source, prefix) {
                assert(prefix_ret.is_some());
                assert(false);
            }
            assert(!slice_is_prefix(source, prefix));
        }
        return None;
    };
    proof {
        let prefix = slice_pattern_view::<P, T>(prefix_pattern);
        assert(slice_strip_prefix_result(source, prefix, prefix_ret));
        if !slice_is_prefix(source, prefix) {
            assert(prefix_ret.is_none());
            assert(false);
        }
        assert(slice_is_prefix(source, prefix));
        assert(stripped@ == source.subrange(prefix.len() as int, source.len() as int));
    }

    let suffix_ret = strip_suffix(stripped, suffix_pattern);
    proof {
        let prefix = slice_pattern_view::<P, T>(prefix_pattern);
        let suffix = slice_pattern_view::<S, T>(suffix_pattern);
        assert(stripped@ == source.subrange(prefix.len() as int, source.len() as int));
        assert(slice_strip_suffix_result(stripped@, suffix, suffix_ret));
        if slice_is_suffix(stripped@, suffix) {
            assert(suffix_ret.is_some());
            assert(suffix_ret.unwrap()@ == stripped@.subrange(0, stripped@.len() - suffix.len()));
            assert(stripped@.len() == source.len() - prefix.len());
            assert(stripped@.subrange(0, stripped@.len() - suffix.len()) =~= source.subrange(
                prefix.len() as int,
                source.len() - suffix.len(),
            ));
            assert(suffix_ret.unwrap()@ =~= source.subrange(
                prefix.len() as int,
                source.len() - suffix.len(),
            ));
            assert(slice_is_suffix(source.subrange(prefix.len() as int, source.len() as int), suffix));
        } else {
            assert(suffix_ret.is_none());
            assert(!slice_is_suffix(source.subrange(prefix.len() as int, source.len() as int), suffix));
        }
        assert(slice_strip_circumfix_result(source, prefix, suffix, suffix_ret));
    }
    suffix_ret
}

}
