#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: core::slice::assume_init_ref
// Source: core/src/mem/maybe_uninit.rs:1508-1514
// Source item sha256: fdb02d51c886afa919c86bdca3a8a1fee74db6c50bef1f0df89364c1a468febd
// Dependency manifest: proof_manifests/027_core_slice_assume_init_ref/dependency_assumption_manifest.json

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
pub unsafe fn rust_1_96_assume_init_ref_raw_cast<'a, T>(
    slice: &'a [MaybeUninit<T>],
) -> (ret: &'a [T])
    requires
        maybe_uninit_all_initialized(maybe_uninit_seq_relation(slice@)),
    ensures
        maybe_uninit_relation_well_formed(
            maybe_uninit_seq_relation(slice@),
            slice@.len() as int,
        ),
        ret@ == maybe_uninit_seq_relation(slice@).values,
        ret@.len() == slice@.len(),
{
    unsafe { &*(slice as *const [MaybeUninit<T>] as *const [T]) }
}

pub unsafe fn assume_init_ref<'a, T>(
    slice: &'a [MaybeUninit<T>],
) -> (ret: &'a [T])
    requires
        maybe_uninit_all_initialized(maybe_uninit_seq_relation(slice@)),
    ensures
        maybe_uninit_relation_well_formed(
            maybe_uninit_seq_relation(slice@),
            slice@.len() as int,
        ),
        ret@ == maybe_uninit_seq_relation(slice@).values,
        ret@.len() == slice@.len(),
{
    unsafe { rust_1_96_assume_init_ref_raw_cast(slice) }
}

}
