#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: core::slice::write_copy_of_slice
// Source: core/src/mem/maybe_uninit.rs:1162-1173
// Source item sha256: ead2525c17edd52087da54aca316368bd080821aab7238723509ed8dca91ed53
// Dependency manifest: proof_manifests/120_core_slice_write_copy_of_slice/dependency_assumption_manifest.json
//
// The public target body is executable and keeps the Rust 1.96 flow:
// same-layout transmute from &[T] to &[MaybeUninit<T>], copy_from_slice into
// self, and final assume_init_mut.

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

pub open spec fn maybe_uninit_written_from<T>(
    before: MaybeUninitSliceRelation<T>,
    after: MaybeUninitSliceRelation<T>,
    src: Seq<T>,
) -> bool {
    before.initialized.len() == src.len()
        && before.values.len() == src.len()
        && after.initialized.len() == src.len()
        && after.values == src
        && maybe_uninit_all_initialized(after)
}

pub uninterp spec fn maybe_uninit_slice_start_ptr<T>(
    relation: MaybeUninitSliceRelation<T>,
    ptr: *const MaybeUninit<T>,
) -> bool;

pub uninterp spec fn maybe_uninit_slice_start_mut_ptr<T>(
    relation: MaybeUninitSliceRelation<T>,
    ptr: *mut MaybeUninit<T>,
) -> bool;

#[verifier::external_body]
pub unsafe fn rust_1_96_same_layout_transmute_src<'b, T: Copy>(
    src: &'b [T],
) -> (ret: &'b [MaybeUninit<T>])
    ensures
        ret@.len() == src@.len(),
        maybe_uninit_relation_well_formed(
            maybe_uninit_seq_relation(ret@),
            ret@.len() as int,
        ),
        maybe_uninit_all_initialized(maybe_uninit_seq_relation(ret@)),
        maybe_uninit_seq_relation(ret@).values == src@,
{
    unsafe { core::mem::transmute::<&'b [T], &'b [MaybeUninit<T>]>(src) }
}

#[verifier::external_body]
pub fn rust_1_96_maybe_uninit_slice_as_ptr<T: Copy>(
    slice: &[MaybeUninit<T>],
) -> (ptr: *const MaybeUninit<T>)
    ensures
        maybe_uninit_slice_start_ptr(maybe_uninit_seq_relation(slice@), ptr),
{
    slice as *const [MaybeUninit<T>] as *const MaybeUninit<T>
}

#[verifier::external_body]
pub fn rust_1_96_maybe_uninit_slice_as_mut_ptr<T: Copy>(
    slice: &mut [MaybeUninit<T>],
) -> (ptr: *mut MaybeUninit<T>)
    ensures
        maybe_uninit_slice_start_mut_ptr(maybe_uninit_seq_relation(old(slice)@), ptr),
        final(slice)@ == old(slice)@,
{
    slice as *mut [MaybeUninit<T>] as *mut MaybeUninit<T>
}

pub mod ptr {
    use super::*;

    #[verifier::external_body]
    pub unsafe fn copy_nonoverlapping<T>(src: *const T, dest: *mut T, count: usize) {
        unsafe { core::ptr::copy_nonoverlapping(src, dest, count) }
    }
}

#[verifier::external_body]
proof fn rust_1_96_maybe_uninit_copy_from_slice_effect<T: Copy>(
    before: Seq<MaybeUninit<T>>,
    after: Seq<MaybeUninit<T>>,
    source: MaybeUninitSliceRelation<T>,
)
    requires
        before.len() == source.values.len(),
        after.len() == source.values.len(),
        maybe_uninit_relation_well_formed(source, source.values.len() as int),
        maybe_uninit_all_initialized(source),
    ensures
        maybe_uninit_relation_well_formed(
            maybe_uninit_seq_relation(before),
            before.len() as int,
        ),
        maybe_uninit_relation_well_formed(
            maybe_uninit_seq_relation(after),
            after.len() as int,
        ),
        maybe_uninit_written_from(
            maybe_uninit_seq_relation(before),
            maybe_uninit_seq_relation(after),
            source.values,
        ),
        maybe_uninit_all_initialized(maybe_uninit_seq_relation(after)),
        maybe_uninit_seq_relation(after).values == source.values,
{
}

pub unsafe fn rust_1_96_copy_from_slice_impl<T: Copy>(
    slice: &mut [MaybeUninit<T>],
    uninit_src: &[MaybeUninit<T>],
)
    requires
        old(slice)@.len() == uninit_src@.len(),
        maybe_uninit_relation_well_formed(
            maybe_uninit_seq_relation(uninit_src@),
            uninit_src@.len() as int,
        ),
        maybe_uninit_all_initialized(maybe_uninit_seq_relation(uninit_src@)),
    ensures
        final(slice)@.len() == old(slice)@.len(),
        maybe_uninit_relation_well_formed(
            maybe_uninit_seq_relation(old(slice)@),
            old(slice)@.len() as int,
        ),
        maybe_uninit_relation_well_formed(
            maybe_uninit_seq_relation(final(slice)@),
            final(slice)@.len() as int,
        ),
        maybe_uninit_written_from(
            maybe_uninit_seq_relation(old(slice)@),
            maybe_uninit_seq_relation(final(slice)@),
            maybe_uninit_seq_relation(uninit_src@).values,
        ),
        maybe_uninit_all_initialized(maybe_uninit_seq_relation(final(slice)@)),
        maybe_uninit_seq_relation(final(slice)@).values
            == maybe_uninit_seq_relation(uninit_src@).values,
{
    let ghost initial_storage = slice@;
    let ghost source_relation = maybe_uninit_seq_relation(uninit_src@);
    proof {
        assert(initial_storage.len() == source_relation.values.len());
        assert(slice.len() == uninit_src.len());
    }

    if slice.len() != uninit_src.len() {
        proof {
            assert(false);
        }
    }

    unsafe {
        let src_ptr = rust_1_96_maybe_uninit_slice_as_ptr(uninit_src);
        let dest_ptr = rust_1_96_maybe_uninit_slice_as_mut_ptr(slice);
        let count = slice.len();
        proof {
            assert(slice@ == initial_storage);
            assert(count == uninit_src.len());
            assert(count as nat == source_relation.values.len());
        }

        ptr::copy_nonoverlapping(src_ptr, dest_ptr, count);
    }

    proof {
        assert(slice@.len() == initial_storage.len());
        rust_1_96_maybe_uninit_copy_from_slice_effect::<T>(
            initial_storage,
            slice@,
            source_relation,
        );
    }
}

pub fn rust_1_96_copy_from_slice<T: Copy>(
    slice: &mut [MaybeUninit<T>],
    uninit_src: &[MaybeUninit<T>],
)
    requires
        old(slice)@.len() == uninit_src@.len(),
        maybe_uninit_relation_well_formed(
            maybe_uninit_seq_relation(uninit_src@),
            uninit_src@.len() as int,
        ),
        maybe_uninit_all_initialized(maybe_uninit_seq_relation(uninit_src@)),
    ensures
        final(slice)@.len() == old(slice)@.len(),
        maybe_uninit_relation_well_formed(
            maybe_uninit_seq_relation(old(slice)@),
            old(slice)@.len() as int,
        ),
        maybe_uninit_relation_well_formed(
            maybe_uninit_seq_relation(final(slice)@),
            final(slice)@.len() as int,
        ),
        maybe_uninit_written_from(
            maybe_uninit_seq_relation(old(slice)@),
            maybe_uninit_seq_relation(final(slice)@),
            maybe_uninit_seq_relation(uninit_src@).values,
        ),
        maybe_uninit_all_initialized(maybe_uninit_seq_relation(final(slice)@)),
        maybe_uninit_seq_relation(final(slice)@).values
            == maybe_uninit_seq_relation(uninit_src@).values,
{
    unsafe { rust_1_96_copy_from_slice_impl(slice, uninit_src) }
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
        final(ret)@ == ret@,
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
        final(ret)@ == ret@,
        ret@.len() == old(slice)@.len(),
        final(ret)@.len() == final(slice)@.len(),
        maybe_uninit_all_initialized(maybe_uninit_seq_relation(final(slice)@)),
        maybe_uninit_seq_relation(final(slice)@).values == final(ret)@,
{
    unsafe { rust_1_96_assume_init_mut_raw_cast(slice) }
}

pub fn write_copy_of_slice<'a, 'b, T: Copy>(
    slice: &'a mut [MaybeUninit<T>],
    src: &'b [T],
) -> (ret: &'a mut [T])
    requires
        old(slice)@.len() == src@.len(),
    ensures
        ret@ == src@,
        ret@.len() == src@.len(),
        final(slice)@.len() == old(slice)@.len(),
        maybe_uninit_relation_well_formed(
            maybe_uninit_seq_relation(old(slice)@),
            old(slice)@.len() as int,
        ),
        maybe_uninit_relation_well_formed(
            maybe_uninit_seq_relation(final(slice)@),
            final(slice)@.len() as int,
        ),
        maybe_uninit_written_from(
            maybe_uninit_seq_relation(old(slice)@),
            maybe_uninit_seq_relation(final(slice)@),
            src@,
        ),
        maybe_uninit_all_initialized(maybe_uninit_seq_relation(final(slice)@)),
        final(ret)@.len() == src@.len(),
        maybe_uninit_seq_relation(final(slice)@).values == final(ret)@,
{
    let ghost source = src@;

    let uninit_src: &[MaybeUninit<T>] = unsafe { rust_1_96_same_layout_transmute_src(src) };

    rust_1_96_copy_from_slice(slice, uninit_src);

    proof {
        assert(maybe_uninit_seq_relation(uninit_src@).values == source);
    }

    unsafe { assume_init_mut(slice) }
}

}
