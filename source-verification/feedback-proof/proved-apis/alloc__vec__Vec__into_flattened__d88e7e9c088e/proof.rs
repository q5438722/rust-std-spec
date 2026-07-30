#![allow(dead_code)]
#![allow(unused_imports)]
#![feature(allocator_api)]

extern crate alloc;

use alloc::vec::Vec;
use core::alloc::Allocator;
use vstd::prelude::*;
use vstd::seq_lib::*;

verus! {

pub uninterp spec fn raw_vec_parts_valid<T, A: Allocator>(
    ptr: *mut T,
    length: usize,
    capacity: usize,
    alloc: &A,
) -> bool;

pub uninterp spec fn raw_vec_view<T>(ptr: *mut T, length: usize) -> Seq<T>;

pub assume_specification<T, A: Allocator>[
    Vec::<T, A>::into_raw_parts_with_alloc
](
    vec: Vec<T, A>,
) -> (parts: (*mut T, usize, usize, A))
    ensures
        raw_vec_parts_valid(parts.0, parts.1, parts.2, &parts.3),
        raw_vec_view(parts.0, parts.1) == vec@,
        parts.1 == vec@.len(),
        parts.1 <= parts.2,
;

pub assume_specification[
    usize::unchecked_mul
](
    lhs: usize,
    rhs: usize,
) -> (product: usize)
    requires
        (lhs as int) * (rhs as int) <= usize::MAX as int,
    ensures
        product as int == (lhs as int) * (rhs as int),
;

pub assume_specification<T, A: Allocator>[
    Vec::<T, A>::from_raw_parts_in
](
    ptr: *mut T,
    length: usize,
    capacity: usize,
    alloc: A,
) -> (vec: Vec<T, A>)
    requires
        raw_vec_parts_valid(ptr, length, capacity, &alloc),
    ensures
        vec@ == raw_vec_view(ptr, length),
;

pub axiom fn axiom_raw_array_capacity_fits<T, A: Allocator, const N: usize>(
    ptr: *mut [T; N],
    length: usize,
    capacity: usize,
    alloc: &A,
)
    requires
        raw_vec_parts_valid(ptr, length, capacity, alloc),
        core::mem::size_of::<T>() != 0,
    ensures
        (capacity as int) * (N as int) <= usize::MAX as int,
;

pub axiom fn axiom_raw_array_reinterpretation<T, A: Allocator, const N: usize>(
    ptr: *mut [T; N],
    length: usize,
    capacity: usize,
    new_length: usize,
    new_capacity: usize,
    alloc: &A,
)
    requires
        raw_vec_parts_valid(ptr, length, capacity, alloc),
        new_length as int == (length as int) * (N as int),
        core::mem::size_of::<T>() == 0 ==> new_capacity == usize::MAX,
        core::mem::size_of::<T>() != 0
            ==> new_capacity as int == (capacity as int) * (N as int),
    ensures
        raw_vec_parts_valid(
            ptr as *mut T,
            new_length,
            new_capacity,
            alloc,
        ),
        raw_vec_view(ptr as *mut T, new_length)
            == raw_vec_view(ptr, length)
                .map_values(|array: [T; N]| array@)
                .flatten(),
;

pub fn source_into_flattened<T, A: Allocator, const N: usize>(
    vec: Vec<[T; N], A>,
) -> (flattened: Vec<T, A>)
    requires
        (usize::MAX as int) >= vec@.len() * (N as int),
    ensures
        flattened@ == vec@.map_values(|array: [T; N]| array@).flatten(),
{
    let ghost original = vec@;
    let (ptr, len, cap, alloc) = vec.into_raw_parts_with_alloc();
    // `SizedTypeProperties::IS_ZST` defaults to this expression.
    let (new_len, new_cap) = if core::mem::size_of::<T>() == 0 {
        (len.checked_mul(N).expect("vec len overflow"), usize::MAX)
    } else {
        proof {
            axiom_raw_array_capacity_fits(ptr, len, cap, &alloc);
        }
        unsafe { (len.unchecked_mul(N), cap.unchecked_mul(N)) }
    };
    proof {
        axiom_raw_array_reinterpretation(
            ptr,
            len,
            cap,
            new_len,
            new_cap,
            &alloc,
        );
    }
    unsafe {
        // The body of `*mut T::cast` is `self as _`.
        Vec::<T, A>::from_raw_parts_in(
            ptr as *mut T,
            new_len,
            new_cap,
            alloc,
        )
    }
}

} // verus!

fn main() {}