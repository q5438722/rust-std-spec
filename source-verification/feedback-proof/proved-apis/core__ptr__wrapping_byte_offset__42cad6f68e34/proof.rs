#![feature(set_ptr_value)]
#![feature(sized_hierarchy)]
#![allow(dead_code)]
#![allow(internal_features)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::layout::size_of;

verus! {

pub assume_specification<T: core::marker::PointeeSized, U>[
    <*const T>::cast::<U>
](ptr: *const T) -> (result: *const U)
    ensures
        result == ptr as *const U,
;

pub assume_specification<T: core::marker::PointeeSized>[<*const T>::wrapping_offset](
    ptr: *const T,
    count: isize,
) -> (result: *const T)
    where
        T: Sized,
    ensures
        size_of::<T>() == 1 ==> result@.addr == ptr@.addr.wrapping_add_signed(count),
        result@.provenance == ptr@.provenance,
        result@.metadata == ptr@.metadata,
;

pub assume_specification<
    T: core::marker::PointeeSized,
    U: core::marker::PointeeSized,
>[<*const T>::with_metadata_of::<U>](
    ptr: *const T,
    meta: *const U,
) -> (result: *const U)
    ensures
        result@.addr == ptr@.addr,
        result@.provenance == ptr@.provenance,
        result@.metadata == meta@.metadata,
;

pub fn source_core_ptr_wrapping_byte_offset<T: core::marker::PointeeSized>(
    ptr: *const T,
    count: isize,
) -> (result: *const T)
    ensures
        result@.addr == ptr@.addr.wrapping_add_signed(count),
        result@.provenance == ptr@.provenance,
        result@.metadata == ptr@.metadata,
{
    ptr.cast::<u8>().wrapping_offset(count).with_metadata_of(ptr)
}

} // verus!

fn main() {}