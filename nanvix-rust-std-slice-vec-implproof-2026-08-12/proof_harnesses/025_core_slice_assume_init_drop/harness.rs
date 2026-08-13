#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: core::slice::assume_init_drop
// Source: core/src/mem/maybe_uninit.rs:1486-1496
// Source item sha256: a07f771f6f96b6dd1b45e87e2496862f0ec8fc9578ee326cd1da6efb80c47b9f
// Dependency manifest: proof_manifests/025_core_slice_assume_init_drop/dependency_assumption_manifest.json

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

pub open spec fn maybe_uninit_drop_all<T>(
    before: MaybeUninitSliceRelation<T>,
    after: MaybeUninitSliceRelation<T>,
) -> bool {
    maybe_uninit_relation_well_formed(before, before.values.len() as int)
        && maybe_uninit_relation_well_formed(after, before.values.len() as int)
        && maybe_uninit_all_initialized(before)
        && forall|i: int| 0 <= i < after.initialized.len() ==> !after.initialized[i]
}

#[verifier::external_body]
pub unsafe fn rust_1_96_assume_init_drop_in_place<T>(slice: &mut [MaybeUninit<T>])
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
        maybe_uninit_drop_all(
            maybe_uninit_seq_relation(old(slice)@),
            maybe_uninit_seq_relation(final(slice)@),
        ),
{
    unsafe { core::ptr::drop_in_place(slice as *mut [MaybeUninit<T>] as *mut [T]) }
}

pub unsafe fn assume_init_drop<T>(slice: &mut [MaybeUninit<T>])
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
        maybe_uninit_drop_all(
            maybe_uninit_seq_relation(old(slice)@),
            maybe_uninit_seq_relation(final(slice)@),
        ),
{
    if !slice.is_empty() {
        unsafe { rust_1_96_assume_init_drop_in_place(slice) }
    }
}

}
