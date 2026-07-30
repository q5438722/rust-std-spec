#![feature(allocator_api)]
#![allow(dead_code)]
#![allow(unused_imports)]

extern crate alloc;

use alloc::vec::Vec;
use core::alloc::Allocator;
use vstd::prelude::*;
use vstd::std_specs::vec::*;

verus! {

pub uninterp spec fn raw_slice_view<T>(ptr: *const T, len: usize) -> Seq<T>;

pub uninterp spec fn raw_slice_valid<T>(ptr: *const T, len: usize) -> bool;

pub assume_specification<T, A: Allocator>[ Vec::<T, A>::as_ptr ](
    vec: &Vec<T, A>,
) -> (ptr: *const T)
    ensures
        raw_slice_valid(ptr, spec_vec_len(vec)),
        raw_slice_view(ptr, spec_vec_len(vec)) == vec@,
    no_unwind
;

pub assume_specification<'a, T>[ core::slice::from_raw_parts::<T> ](
    data: *const T,
    len: usize,
) -> (slice: &'a [T])
    requires
        raw_slice_valid(data, len),
    ensures
        slice@ == raw_slice_view(data, len),
    no_unwind
;

fn source_vec_as_slice<T, A: Allocator>(vec: &Vec<T, A>) -> (slice: &[T])
    ensures
        slice@ == vec@,
{
    unsafe {
        // Rust 1.96 explicitly identifies this as the equivalent raw-slice construction.
        core::slice::from_raw_parts(vec.as_ptr(), vec.len())
    }
}

} // verus!

fn main() {}