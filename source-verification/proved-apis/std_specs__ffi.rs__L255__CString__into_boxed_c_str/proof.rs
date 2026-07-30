#![feature(allocator_api)]
#![allow(dead_code)]
#![allow(unused_imports)]

extern crate alloc;

use alloc::boxed::Box;
use alloc::ffi::CString;
use alloc::vec::Vec;
use core::alloc::Allocator;
use core::ffi::CStr;
use vstd::prelude::*;
use vstd::std_specs::ffi::*;

verus! {

pub uninterp spec fn boxed_slice_contents<T, A: Allocator>(value: &Box<[T], A>) -> Seq<T>;
pub uninterp spec fn box_raw_token<T: ?Sized>(value: &Box<T>) -> int;
pub uninterp spec fn ptr_raw_token<T: ?Sized>(ptr: *mut T) -> int;
pub uninterp spec fn raw_box_allocation<T: ?Sized>(ptr: *mut T) -> bool;
pub uninterp spec fn slice_token_view(token: int) -> Seq<u8>;
pub uninterp spec fn c_str_token_view(token: int) -> Seq<u8>;
pub uninterp spec fn transmute_relation<S, D>(source: S, destination: D) -> bool;

pub assume_specification<T, A: Allocator>[
    Vec::<T, A>::into_boxed_slice
](value: Vec<T, A>) -> (result: Box<[T], A>)
    ensures boxed_slice_contents(&result) == value@,
;

pub assume_specification<T: ?Sized>[Box::<T>::into_raw](value: Box<T>) -> (result: *mut T)
    ensures
        raw_box_allocation(result),
        ptr_raw_token(result) == box_raw_token(&value),
;

pub assume_specification<T: ?Sized>[Box::<T>::from_raw](ptr: *mut T) -> (result: Box<T>)
    requires raw_box_allocation(ptr),
    ensures box_raw_token(&result) == ptr_raw_token(ptr),
;

pub assume_specification<S, D>[
    core::mem::transmute::<S, D>
](source: S) -> (destination: D)
    ensures transmute_relation(source, destination),
;

pub axiom fn axiom_cstring_view_valid(value: &CString)
    ensures c_string_bytes_valid(value@),
;

pub axiom fn axiom_boxed_slice_token_view(value: &Box<[u8]>)
    ensures slice_token_view(box_raw_token(value)) == boxed_slice_contents(value),
;

pub axiom fn axiom_boxed_c_str_token_view(value: &Box<CStr>)
    ensures c_str_token_view(box_raw_token(value)) == (**value)@,
;

pub axiom fn axiom_boxed_bytes_cast_to_c_str(
    bytes_ptr: *mut [u8],
    c_str_ptr: *mut CStr,
)
    requires
        raw_box_allocation(bytes_ptr),
        transmute_relation(bytes_ptr, c_str_ptr),
        c_string_bytes_with_nul_valid(slice_token_view(ptr_raw_token(bytes_ptr))),
    ensures
        raw_box_allocation(c_str_ptr),
        ptr_raw_token(c_str_ptr) == ptr_raw_token(bytes_ptr),
        c_str_token_view(ptr_raw_token(c_str_ptr))
            == slice_token_view(ptr_raw_token(bytes_ptr)).drop_last(),
;

fn source_cstring_into_boxed_c_str(value: CString) -> (result: Box<CStr>)
    ensures (*result)@ == value@,
{
    proof {
        axiom_cstring_view_valid(&value);
    }
    let ghost original = value@;
    let bytes = value.into_bytes_with_nul();
    let inner = bytes.into_boxed_slice();
    proof {
        axiom_boxed_slice_token_view(&inner);
    }
    unsafe {
        let ptr = Box::into_raw(inner);
        let c_str_ptr = core::mem::transmute::<*mut [u8], *mut CStr>(ptr);
        proof {
            assert(c_string_bytes_with_nul_valid(slice_token_view(ptr_raw_token(ptr))));
            axiom_boxed_bytes_cast_to_c_str(ptr, c_str_ptr);
        }
        let result = Box::from_raw(c_str_ptr);
        proof {
            axiom_boxed_c_str_token_view(&result);
        }
        result
    }
}

} // verus!

fn main() {}