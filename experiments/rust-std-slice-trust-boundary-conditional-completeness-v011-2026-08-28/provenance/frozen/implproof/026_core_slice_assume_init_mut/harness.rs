#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: core::slice::assume_init_mut
// Source: core/src/mem/maybe_uninit.rs:1527-1531
// Source item sha256: beb997b66dd7cca2818667bddfe1e1ade51676cdf0ea4f32cf6253af1c0234f4
// Dependency manifest: proof_manifests/026_core_slice_assume_init_mut/dependency_assumption_manifest.json

use core::mem::MaybeUninit;
use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub ghost struct MaybeUninitSliceRelation<T> {
    pub initialized: Seq<bool>,
    pub values: Seq<T>,
}

pub uninterp spec fn maybe_uninit_initialized_at<T>(
    storage: Seq<MaybeUninit<T>>,
    index: int,
) -> bool;

pub uninterp spec fn maybe_uninit_value_at<T>(
    storage: Seq<MaybeUninit<T>>,
    index: int,
) -> T;

pub open spec fn maybe_uninit_seq_relation<T>(
    storage: Seq<MaybeUninit<T>>,
) -> MaybeUninitSliceRelation<T> {
    MaybeUninitSliceRelation {
        initialized: Seq::new(storage.len(), |i: int| maybe_uninit_initialized_at(storage, i)),
        values: Seq::new(storage.len(), |i: int| maybe_uninit_value_at(storage, i)),
    }
}

pub open spec fn maybe_uninit_relation_well_formed<T>(
    relation: MaybeUninitSliceRelation<T>,
    len: int,
) -> bool {
    0 <= len && relation.initialized.len() == len && relation.values.len() == len
}

pub open spec fn maybe_uninit_all_initialized<T>(
    relation: MaybeUninitSliceRelation<T>,
) -> bool {
    relation.initialized.len() == relation.values.len()
        && forall|i: int| 0 <= i < relation.initialized.len() ==> relation.initialized[i]
}

#[verifier::external_body]
pub unsafe fn rust_1_96_assume_init_mut_raw_cast<'a, T>(
    slice: &'a mut [MaybeUninit<T>],
) -> (ret: &'a mut [T])
    requires
        maybe_uninit_all_initialized(maybe_uninit_seq_relation(old(slice)@)),
    ensures
        maybe_uninit_relation_well_formed(
            maybe_uninit_seq_relation(old(slice)@),
            old(slice)@.len() as int,
        ),
        maybe_uninit_relation_well_formed(
            maybe_uninit_seq_relation(final(slice)@),
            final(slice)@.len() as int,
        ),
        final(slice)@.len() == old(slice)@.len(),
        ret@ == maybe_uninit_seq_relation(old(slice)@).values,
        ret@.len() == old(slice)@.len(),
        final(ret)@.len() == final(slice)@.len(),
        maybe_uninit_all_initialized(maybe_uninit_seq_relation(final(slice)@)),
        maybe_uninit_seq_relation(final(slice)@).values == final(ret)@,
{
    unsafe { &mut *(slice as *mut [MaybeUninit<T>] as *mut [T]) }
}

pub unsafe fn assume_init_mut<'a, T>(
    slice: &'a mut [MaybeUninit<T>],
) -> (ret: &'a mut [T])
    requires
        maybe_uninit_all_initialized(maybe_uninit_seq_relation(old(slice)@)),
    ensures
        maybe_uninit_relation_well_formed(
            maybe_uninit_seq_relation(old(slice)@),
            old(slice)@.len() as int,
        ),
        maybe_uninit_relation_well_formed(
            maybe_uninit_seq_relation(final(slice)@),
            final(slice)@.len() as int,
        ),
        final(slice)@.len() == old(slice)@.len(),
        ret@ == maybe_uninit_seq_relation(old(slice)@).values,
        ret@.len() == old(slice)@.len(),
        final(ret)@.len() == final(slice)@.len(),
        maybe_uninit_all_initialized(maybe_uninit_seq_relation(final(slice)@)),
        maybe_uninit_seq_relation(final(slice)@).values == final(ret)@,
{
    unsafe { rust_1_96_assume_init_mut_raw_cast(slice) }
}

}
