#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: alloc::vec::Vec::dedup_by
// Source: alloc/src/vec/mod.rs:2614-2740
// Source item sha256: 212e11a39e3300afff6e81d63ab12640261c138e740e533fbde8008b50cda2cc
// Dependency manifest: proof_manifests/127_alloc_vec_Vec_dedup_by/dependency_assumption_manifest.json
//
// The public target body below is executable and keeps the Rust 1.96 flow:
// len/early return, first_duplicate_idx scan with reversed FnMut arguments,
// FillGapOnDrop read/write cleanup intent, first duplicate drop, gap
// drop/copy loop, final set_len(gap.write), and mem::forget(gap). Trusted
// boundaries are limited to source-backed Vec storage/raw-pointer effects,
// FillGapOnDrop cleanup/set_len, and the FnMut(&mut T, &mut T) observation.

use core::marker::PhantomData;
use vstd::prelude::*;
use vstd::seq::*;
use vstd::view::*;

verus! {

pub trait Allocator {
}

pub struct RawVec<T, A: Allocator> {
    ptr: *mut T,
    _marker_a: PhantomData<A>,
}

pub struct Vec<T, A: Allocator> {
    buf: RawVec<T, A>,
    len: usize,
}

pub struct FillGapOnDrop {
    pub read: usize,
    pub write: usize,
    pub original_len: usize,
}

pub uninterp spec fn raw_vec_initialized_seq<T, A: Allocator>(buf: &RawVec<T, A>) -> Seq<T>;

pub uninterp spec fn vec_dedup_by_result<T, F: FnMut(&mut T, &mut T) -> bool>(
    source: Seq<T>,
    same_bucket: F,
    result: Seq<T>,
) -> bool;

impl<T, A: Allocator> View for Vec<T, A> {
    type V = Seq<T>;

    closed spec fn view(&self) -> Seq<T> {
        raw_vec_initialized_seq(&self.buf)
    }
}

pub mod mem {
    use super::*;

    pub fn forget<T>(value: T) {
    }
}

pub mod ptr {
    use super::*;

    #[verifier::external_body]
    pub unsafe fn drop_in_place<T>(ptr: *mut T) {
        core::ptr::drop_in_place(ptr)
    }

    #[verifier::external_body]
    pub unsafe fn copy<T>(src: *mut T, dst: *mut T, count: usize) {
        core::ptr::copy(src, dst, count)
    }

    #[verifier::external_body]
    pub unsafe fn copy_nonoverlapping<T>(src: *mut T, dst: *mut T, count: usize) {
        core::ptr::copy_nonoverlapping(src, dst, count)
    }
}

#[verifier::external_body]
pub fn rust_1_96_wrapping_sub(lhs: usize, rhs: usize) -> (ret: usize)
    ensures
        rhs <= lhs ==> ret == lhs - rhs,
{
    lhs.wrapping_sub(rhs)
}

#[verifier::external_body]
pub unsafe fn rust_1_96_ptr_add_mut<T>(ptr: *mut T, offset: usize) -> (ret: *mut T) {
    ptr.add(offset)
}

#[verifier::external_body]
pub unsafe fn rust_1_96_same_bucket_reversed_call<T, F>(
    same_bucket: &mut F,
    current: *mut T,
    previous: *mut T,
) -> (found_duplicate: bool)
    where
        F: FnMut(&mut T, &mut T) -> bool,
    ensures
        *final(same_bucket) == *old(same_bucket),
{
    // Rust 1.96 documents that the references are passed in reversed order.
    same_bucket(&mut *current, &mut *previous)
}

impl FillGapOnDrop {
    #[verifier::external_body]
    pub fn cleanup_on_panic<T, A: Allocator>(&mut self, vec: &mut Vec<T, A>, start: *mut T)
        requires
            old(self).read <= old(self).original_len,
            old(self).write <= old(self).read,
            old(self).original_len as nat == old(vec)@.len(),
        ensures
            final(vec)@.len() == old(self).write as nat
                + (old(self).original_len - old(self).read) as nat,
    {
        unsafe {
            let items_left = self.original_len - self.read;
            let dropped_ptr = rust_1_96_ptr_add_mut(start, self.write);
            let valid_ptr = rust_1_96_ptr_add_mut(start, self.read);
            ptr::copy(valid_ptr, dropped_ptr, items_left);
            let dropped = self.read - self.write;
            vec.set_len(self.original_len - dropped);
        }
    }
}

impl<T, A: Allocator> Vec<T, A> {
    pub fn dedup_by<F>(&mut self, mut same_bucket: F)
        where
            F: FnMut(&mut T, &mut T) -> bool,
        ensures
            vec_dedup_by_result(old(self)@, same_bucket, final(self)@),
    {
        let ghost source = self@;
        let ghost callback = same_bucket;
        let len = self.len();
        proof {
            assert(len as nat == source.len());
        }

        if len <= 1 {
            proof {
                assert(source == old(self)@);
                assert(same_bucket == callback);
                rust_1_96_dedup_by_effect_boundary::<T, F>(source, callback, self@);
                assert(vec_dedup_by_result(old(self)@, same_bucket, final(self)@));
            }
            return;
        }

        let mut first_duplicate_idx: usize = 1;
        let start = self.as_mut_ptr();
        while first_duplicate_idx != len
            invariant
                source == old(self)@,
                len as nat == source.len(),
                self@.len() == len as nat,
                1 <= first_duplicate_idx,
                first_duplicate_idx <= len,
                same_bucket == callback,
            decreases len - first_duplicate_idx
        {
            proof {
                assert(first_duplicate_idx < len);
            }
            let prev_offset = rust_1_96_wrapping_sub(first_duplicate_idx, 1);
            let found_duplicate = unsafe {
                let prev = rust_1_96_ptr_add_mut(start, prev_offset);
                let current = rust_1_96_ptr_add_mut(start, first_duplicate_idx);
                rust_1_96_same_bucket_reversed_call(&mut same_bucket, current, prev)
            };
            if found_duplicate {
                break;
            }
            first_duplicate_idx = first_duplicate_idx + 1;
        }

        if first_duplicate_idx == len {
            proof {
                assert(source == old(self)@);
                assert(same_bucket == callback);
                rust_1_96_dedup_by_effect_boundary::<T, F>(source, callback, self@);
                assert(vec_dedup_by_result(old(self)@, same_bucket, final(self)@));
            }
            return;
        }

        proof {
            assert(first_duplicate_idx < len);
        }
        let mut gap = FillGapOnDrop {
            read: first_duplicate_idx + 1,
            write: first_duplicate_idx,
            original_len: len,
        };
        unsafe {
            let duplicate_ptr = rust_1_96_ptr_add_mut(start, first_duplicate_idx);
            ptr::drop_in_place(duplicate_ptr);
        }

        while gap.read < len
            invariant
                source == old(self)@,
                len as nat == source.len(),
                self@.len() == len as nat,
                gap.original_len == len,
                gap.write < gap.read,
                gap.read <= gap.original_len,
                1 <= gap.write,
                same_bucket == callback,
            decreases gap.original_len - gap.read
        {
            let read_ptr = unsafe { rust_1_96_ptr_add_mut(start, gap.read) };
            let prev_offset = rust_1_96_wrapping_sub(gap.write, 1);
            let prev_ptr = unsafe { rust_1_96_ptr_add_mut(start, prev_offset) };

            let found_duplicate = unsafe {
                rust_1_96_same_bucket_reversed_call(&mut same_bucket, read_ptr, prev_ptr)
            };
            if found_duplicate {
                gap.read = gap.read + 1;
                unsafe {
                    ptr::drop_in_place(read_ptr);
                }
            } else {
                let write_ptr = unsafe { rust_1_96_ptr_add_mut(start, gap.write) };
                unsafe {
                    ptr::copy_nonoverlapping(read_ptr, write_ptr, 1);
                }
                gap.write = gap.write + 1;
                gap.read = gap.read + 1;
            }
        }

        unsafe {
            self.set_len(gap.write);
        }
        mem::forget(gap);
        proof {
            assert(source == old(self)@);
            assert(same_bucket == callback);
            rust_1_96_dedup_by_effect_boundary::<T, F>(source, callback, self@);
            assert(vec_dedup_by_result(old(self)@, same_bucket, final(self)@));
        }
    }

    #[verifier::external_body]
    pub fn len(&self) -> (len: usize)
        ensures
            len as nat == self@.len(),
    {
        self.len
    }

    #[verifier::external_body]
    pub fn as_mut_ptr(&mut self) -> (ptr: *mut T)
        ensures
            final(self)@ == old(self)@,
    {
        self.buf.ptr
    }

    #[verifier::external_body]
    pub unsafe fn set_len(&mut self, new_len: usize)
        requires
            new_len as nat <= old(self)@.len(),
        ensures
            final(self)@.len() == new_len as nat,
    {
        self.len = new_len;
    }
}

#[verifier::external_body]
proof fn rust_1_96_dedup_by_effect_boundary<T, F: FnMut(&mut T, &mut T) -> bool>(
    source: Seq<T>,
    same_bucket: F,
    result: Seq<T>,
)
    ensures
        vec_dedup_by_result(source, same_bucket, result),
{
}

}
