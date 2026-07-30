#![feature(allocator_api)]
#![allow(dead_code)]
#![allow(unused_imports)]

extern crate alloc;

use alloc::vec::Vec;
use core::alloc::Allocator;
use vstd::prelude::*;
use vstd::std_specs::vec::*;

verus! {

pub uninterp spec fn raw_slice_view<T>(ptr: *mut T, len: usize) -> Seq<T>;

pub uninterp spec fn raw_slice_valid<T>(ptr: *mut T, len: usize) -> bool;

#[verifier::prophetic]
pub uninterp spec fn raw_slice_final_view<T>(ptr: *mut T, len: usize) -> Seq<T>;

pub uninterp spec fn spec_vec_as_mut_ptr<T, A: Allocator>(
    vec: Vec<T, A>,
) -> *mut T;

pub assume_specification<T, A: Allocator>[ Vec::<T, A>::as_mut_ptr ](
    vec: &mut Vec<T, A>,
) -> (ptr: *mut T)
    ensures
        ptr == spec_vec_as_mut_ptr(*old(vec)),
        raw_slice_valid(ptr, spec_vec_len(old(vec))),
        raw_slice_view(ptr, spec_vec_len(old(vec))) == old(vec)@,
        *final(vec) === *old(vec),
    no_unwind
;

pub assume_specification<'a, T>[ core::slice::from_raw_parts_mut::<T> ](
    data: *mut T,
    len: usize,
) -> (slice: &'a mut [T])
    requires
        raw_slice_valid(data, len),
    ensures
        slice@ == raw_slice_view(data, len),
        final(slice)@ == raw_slice_final_view(data, len),
    no_unwind
;

pub axiom fn axiom_vec_buffer_final<T, A: Allocator>(
    vec: &&mut Vec<T, A>,
    ptr: *mut T,
    len: usize,
)
    requires
        ptr == spec_vec_as_mut_ptr(**vec),
        raw_slice_valid(ptr, len),
        len == spec_vec_len(*vec),
    ensures
        final(*vec)@ == raw_slice_final_view(ptr, len),
;

fn source_vec_as_mut_slice<T, A: Allocator>(
    vec: &mut Vec<T, A>,
) -> (slice: &mut [T])
    ensures
        slice@ == old(vec)@,
        final(slice)@ == final(vec)@,
{
    let ptr = vec.as_mut_ptr();
    let len = vec.len();
    // The Rust source explicitly identifies this as the equivalent checked
    // raw-slice construction for its aggregate_raw_ptr intrinsic.
    let slice = unsafe {
        core::slice::from_raw_parts_mut(ptr, len)
    };
    proof {
        assert(ptr == spec_vec_as_mut_ptr(*vec));
        axiom_vec_buffer_final(&vec, ptr, len);
    }
    slice
}

} // verus!

fn main() {}