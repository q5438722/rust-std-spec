#![allow(dead_code, unused_imports, unused_variables)]
// Target-specific Verus implementation harness.
// Target: core::slice::is_sorted_by_key
// Source: core/src/slice/mod.rs:4795-4801
// Source item sha256: e3b02a9c38338889be9bba5f3eacb2c6f20766070881944f14b52cbefaf41978
// Dependency manifest: proof_manifests/059_core_slice_is_sorted_by_key/dependency_assumption_manifest.json

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub uninterp spec fn partial_eq_observed<T: core::cmp::PartialEq>(left: T, right: T) -> bool;

pub uninterp spec fn partial_ord_leq_observed<T: core::cmp::PartialOrd>(
    left: T,
    right: T,
) -> bool;

pub uninterp spec fn fnmut_adjacent_key_outputs<F, T, K>(
    f: F,
    source: Seq<T>,
) -> Seq<K>;

pub open spec fn fnmut_adjacent_key_trace_valid<F, T, K: core::cmp::PartialOrd>(
    seq: Seq<T>,
    f: F,
) -> bool {
    let outputs = fnmut_adjacent_key_outputs::<F, T, K>(f, seq);
    outputs.len() <= seq.len()
        && (seq.len() == 0 ==> outputs.len() == 0)
        && (seq.len() > 0 ==> outputs.len() > 0)
        && (outputs.len() < seq.len() ==> outputs.len() >= 2)
        && (outputs.len() < seq.len() ==> !partial_ord_leq_observed(
            outputs[outputs.len() as int - 2],
            outputs[outputs.len() as int - 1],
        ))
        && forall|i: int| 0 <= i && i + 2 < outputs.len() ==> #[trigger] partial_ord_leq_observed(
            outputs[i],
            outputs[i + 1],
        )
}

pub open spec fn slice_sorted_by_partial_key<F, T, K: core::cmp::PartialOrd>(
    seq: Seq<T>,
    f: F,
) -> bool {
    let outputs = fnmut_adjacent_key_outputs::<F, T, K>(f, seq);
    &&& fnmut_adjacent_key_trace_valid::<F, T, K>(seq, f)
    &&& outputs.len() == seq.len()
    &&& forall|i: int| 0 <= i && i + 1 < outputs.len() ==> #[trigger] partial_ord_leq_observed(
        outputs[i],
        outputs[i + 1],
    )
}

pub open spec fn slice_sorted_by_partial_key_result<F, T, K: core::cmp::PartialOrd>(
    seq: Seq<T>,
    f: F,
    ret: bool,
) -> bool {
    fnmut_adjacent_key_trace_valid::<F, T, K>(seq, f)
        && (ret <==> slice_sorted_by_partial_key::<F, T, K>(seq, f))
}

pub struct SliceReceiver<'a, T: 'a> {
    slice: &'a [T],
}

pub struct Iter<'a, T: 'a> {
    slice: &'a [T],
}

pub closed spec fn slice_receiver_source<'a, T>(receiver: SliceReceiver<'a, T>) -> Seq<T> {
    receiver.slice@
}

pub closed spec fn slice_iter_source<'a, T>(iter: Iter<'a, T>) -> Seq<T> {
    iter.slice@
}

impl<'a, T> SliceReceiver<'a, T> {
    pub fn iter(self) -> (iter: Iter<'a, T>)
        ensures
            slice_iter_source(iter) == slice_receiver_source(self),
    {
        let iter = Iter { slice: self.slice };
        proof {
            reveal(slice_receiver_source);
            reveal(slice_iter_source);
        }
        iter
    }
}

impl<'a, T> Iter<'a, T> {
    #[verifier::external_body]
    pub fn is_sorted_by_key<F, K: core::cmp::PartialOrd>(self, f: F) -> (ret: bool)
        where
            F: FnMut(&'a T) -> K,
        ensures
            slice_sorted_by_partial_key_result::<F, T, K>(slice_iter_source(self), f, ret),
    {
        false
    }
}

pub fn is_sorted_by_key<'a, T: 'a, F, K: core::cmp::PartialOrd>(
    slice: &'a [T],
    f: F,
) -> (ret: bool)
    where
        F: FnMut(&'a T) -> K,
    ensures
        slice_sorted_by_partial_key_result::<F, T, K>(slice@, f, ret),
{
    let self_slice = SliceReceiver { slice };
    let iter = self_slice.iter();
    proof {
        reveal(slice_receiver_source);
        reveal(slice_iter_source);
    }
    iter.is_sorted_by_key(f)
}

}
