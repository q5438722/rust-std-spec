#![allow(dead_code)]
#![allow(unused_imports)]
#![feature(allocator_api)]

extern crate alloc;

use alloc::boxed::Box;
use alloc::vec::Vec;
use core::alloc::Allocator;
use vstd::prelude::*;
use vstd::slice::*;
use vstd::std_specs::smart_ptrs::*;

verus! {

pub uninterp spec fn box_raw_token<U: ?Sized, A: Allocator>(b: &Box<U, A>) -> int;

pub uninterp spec fn ptr_raw_token<U: ?Sized>(ptr: *mut U) -> int;

pub uninterp spec fn raw_box_allocation<U: ?Sized, A: Allocator>(
    ptr: *mut U,
    alloc: &A,
) -> bool;

pub assume_specification<U: ?Sized, A: Allocator>[
    Box::<U, A>::into_raw_with_allocator
](
    b: Box<U, A>,
) -> (parts: (*mut U, A))
    ensures
        raw_box_allocation(parts.0, &parts.1),
        ptr_raw_token(parts.0) == box_raw_token(&b),
;

pub uninterp spec fn slice_token_view<T>(token: int) -> Seq<T>;

pub uninterp spec fn raw_vec_view<T>(ptr: *mut T, len: usize) -> Seq<T>;

pub uninterp spec fn raw_vec_parts_valid<T, A: Allocator>(
    ptr: *mut T,
    length: usize,
    capacity: usize,
    alloc: &A,
) -> bool;

pub axiom fn axiom_box_slice_token_view<T, A: Allocator>(b: &Box<[T], A>)
    ensures
        slice_token_view::<T>(box_raw_token(b)) == b@,
;

pub axiom fn axiom_box_slice_into_vec_parts<T, A: Allocator>(
    ptr: *mut [T],
    alloc: &A,
    len: usize,
)
    requires
        raw_box_allocation(ptr, alloc),
        len == slice_token_view::<T>(ptr_raw_token(ptr)).len(),
    ensures
        raw_vec_parts_valid(ptr as *mut T, len, len, alloc),
        raw_vec_view(ptr as *mut T, len) == slice_token_view::<T>(ptr_raw_token(ptr)),
;

pub assume_specification<T, A: Allocator>[
    Vec::<T, A>::from_raw_parts_in
](
    ptr: *mut T,
    length: usize,
    capacity: usize,
    alloc: A,
) -> (v: Vec<T, A>)
    requires
        raw_vec_parts_valid(ptr, length, capacity, &alloc),
    ensures
        v@ == raw_vec_view(ptr, length),
;

fn source_slice_into_vec<T, A: Allocator>(b: Box<[T], A>) -> (v: Vec<T, A>)
    ensures
        v@ == b@,
{
    unsafe {
        let len = b.len();
        proof {
            axiom_box_slice_token_view(&b);
        }
        let ghost original = b@;
        let ghost token = box_raw_token(&b);
        let (ptr, alloc) = Box::into_raw_with_allocator(b);
        proof {
            assert(ptr_raw_token(ptr) == token);
            assert(slice_token_view::<T>(ptr_raw_token(ptr)) == original);
            axiom_box_slice_into_vec_parts(ptr, &alloc, len);
        }
        Vec::from_raw_parts_in(ptr as *mut T, len, len, alloc)
    }
}

} // verus!

fn main() {}