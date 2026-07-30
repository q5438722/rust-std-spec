#![allow(dead_code)]
#![allow(unused_imports)]
#![feature(sized_hierarchy)]

use core::slice::from_raw_parts;
use vstd::prelude::*;

verus! {

pub uninterp spec fn raw_slice_valid<T>(ptr: *const T, len: usize) -> bool;
pub uninterp spec fn raw_slice_view<T>(ptr: *const T, len: usize) -> Seq<T>;

pub assume_specification<T>[ <[T]>::as_ptr ](
    slice: &[T],
) -> (ptr: *const T)
    ensures
        raw_slice_valid(ptr, slice.len()),
        raw_slice_view(ptr, slice.len()) == slice@,
    opens_invariants none
    no_unwind
;

pub assume_specification<T: core::marker::PointeeSized, U>[
    <*const T>::cast::<U>
](ptr: *const T) -> (result: *const U)
    ensures result == ptr as *const U,
    opens_invariants none
    no_unwind
;

pub assume_specification[usize::unchecked_mul](
    lhs: usize,
    rhs: usize,
) -> (product: usize)
    requires (lhs as int) * (rhs as int) <= usize::MAX as int,
    ensures product as int == (lhs as int) * (rhs as int),
    opens_invariants none
    no_unwind
;

pub assume_specification<'a, T>[core::slice::from_raw_parts::<T>](
    data: *const T,
    len: usize,
) -> (slice: &'a [T])
    requires raw_slice_valid(data, len),
    ensures
        slice@.len() == len,
        slice@ == raw_slice_view(data, len),
    opens_invariants none
    no_unwind
;

pub axiom fn axiom_array_slice_flattened_length_fits<T, const N: usize>(
    slice: &[[T; N]],
)
    requires core::mem::size_of::<T>() > 0,
    ensures slice@.len() * (N as int) <= usize::MAX as int,
;

pub axiom fn axiom_raw_array_slice_reinterpretation<T, const N: usize>(
    ptr: *const [T; N],
    length: usize,
    new_length: usize,
)
    requires
        raw_slice_valid(ptr, length),
        new_length as int == (length as int) * (N as int),
    ensures
        raw_slice_valid(ptr as *const T, new_length),
        raw_slice_view(ptr as *const T, new_length)
            == raw_slice_view(ptr, length).flat_map(|array: [T; N]| array@),
;

pub const fn source_core_slice_as_flattened<T, const N: usize>(
    slice: &[[T; N]],
) -> (ret: &[T])
    requires
        core::mem::size_of::<T>() > 0 || usize::MAX >= slice@.len() * N,
    ensures
        ret@.len() == slice@.len() * N,
        ret@ == slice@.flat_map(|a: [T; N]| a@),
{
    // `SizedTypeProperties::IS_ZST` defaults to this expression.
    let len = if core::mem::size_of::<T>() == 0 {
        slice.len().checked_mul(N).expect("slice len overflow")
    } else {
        proof {
            axiom_array_slice_flattened_length_fits::<T, N>(slice);
        }
        unsafe { slice.len().unchecked_mul(N) }
    };
    let array_ptr = slice.as_ptr();
    let ptr = array_ptr.cast();
    proof {
        assert(len as int == slice@.len() * (N as int));
        axiom_raw_array_slice_reinterpretation::<T, N>(array_ptr, slice.len(), len);
    }
    unsafe { from_raw_parts(ptr, len) }
}

} // verus!

fn main() {}