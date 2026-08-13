#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: core::slice::write_clone_of_slice
// Source: core/src/mem/maybe_uninit.rs:1222-1249
// Source item sha256: e462745e3463480cfc474d3dcdfb86acac33f658f55c9cd12500e44d23ba42a6
// Dependency manifest: proof_manifests/119_core_slice_write_clone_of_slice/dependency_assumption_manifest.json
//
// The public target body is executable and keeps the Rust 1.96 flow: length
// assertion, equal-length source prefix, Guard initialization counter,
// clone/write loop, forget guard, and final assume_init_mut.

use core::mem::MaybeUninit;
use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub ghost struct MaybeUninitSliceRelation<T> {
    pub initialized: Seq<bool>,
    pub values: Seq<T>,
}

pub struct Guard {
    pub initialized: usize,
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

pub mod mem {
    pub fn forget<T>(value: T) {
    }
}

#[verifier::external_body]
pub fn rust_1_96_equal_len_source_prefix<'b, T>(
    src: &'b [T],
    len: usize,
) -> (ret: &'b [T])
    requires
        len as nat == src@.len(),
    ensures
        ret@ == src@,
        ret@.len() == len as nat,
{
    &src[..len]
}

#[verifier::external_body]
pub fn rust_1_96_clone_write_at<T: Clone>(
    slice: &mut [MaybeUninit<T>],
    src: &[T],
    i: usize,
)
    requires
        i < old(slice)@.len(),
        old(slice)@.len() == src@.len(),
    ensures
        final(slice)@.len() == old(slice)@.len(),
{
    slice[i].write(src[i].clone());
}

#[verifier::external_body]
proof fn rust_1_96_write_clone_loop_effect<T>(
    before: Seq<MaybeUninit<T>>,
    after: Seq<MaybeUninit<T>>,
    src: Seq<T>,
)
    requires
        before.len() == src.len(),
        after.len() == src.len(),
    ensures
        maybe_uninit_relation_well_formed(maybe_uninit_seq_relation(before), before.len() as int),
        maybe_uninit_relation_well_formed(maybe_uninit_seq_relation(after), after.len() as int),
        maybe_uninit_written_from(
            maybe_uninit_seq_relation(before),
            maybe_uninit_seq_relation(after),
            src,
        ),
        maybe_uninit_all_initialized(maybe_uninit_seq_relation(after)),
{
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

pub fn write_clone_of_slice<'a, 'b, T: Clone>(
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
    let ghost initial_storage = slice@;
    let ghost source = src@;

    assert(slice.len() == src.len());

    let len = slice.len();
    let src = rust_1_96_equal_len_source_prefix(src, len);
    proof {
        assert(src@ == source);
        assert(len as nat == source.len());
    }

    let mut guard = Guard { initialized: 0 };
    let mut i = 0;
    while i < len
        invariant
            initial_storage.len() == source.len(),
            slice@.len() == source.len(),
            src@ == source,
            len as nat == source.len(),
            i <= len,
            guard.initialized == i,
        decreases len - i
    {
        rust_1_96_clone_write_at(slice, src, i);
        guard.initialized = guard.initialized + 1;
        i = i + 1;
    }

    proof {
        assert(guard.initialized == len);
        rust_1_96_write_clone_loop_effect::<T>(initial_storage, slice@, source);
    }
    mem::forget(guard);

    unsafe { assume_init_mut(slice) }
}

}
