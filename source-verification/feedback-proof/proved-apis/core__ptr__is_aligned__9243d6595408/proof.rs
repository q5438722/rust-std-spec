#![feature(pointer_is_aligned_to)]
#![feature(sized_hierarchy)]
#![allow(dead_code)]
#![allow(internal_features)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::layout::align_of;

verus! {

pub assume_specification<T: core::marker::PointeeSized>[
    <*const T>::is_aligned_to
](ptr: *const T, align: usize) -> (result: bool)
    ensures
        result <==> ptr@.addr as nat % align as nat == 0,
;

pub fn source_core_ptr_is_aligned<T: core::marker::PointeeSized>(
    ptr: *const T,
) -> (result: bool)
    where
        T: Sized,
    ensures
        result <==> ptr@.addr as nat % align_of::<T>() == 0,
{
    ptr.is_aligned_to(core::mem::align_of::<T>())
}

} // verus!

fn main() {}