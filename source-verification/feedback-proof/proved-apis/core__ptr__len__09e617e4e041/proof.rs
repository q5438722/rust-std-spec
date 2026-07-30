#![feature(ptr_metadata, sized_hierarchy)]
#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;

verus! {

pub assume_specification<V: core::marker::PointeeSized>[
    core::ptr::metadata::<V>
](ptr: *const V) -> (metadata: <V as core::ptr::Pointee>::Metadata)
    ensures
        metadata == ptr@.metadata,
    opens_invariants none
    no_unwind
;

pub fn source_core_ptr_len<T>(
    ptr: *const [T],
) -> (result: usize)
    ensures
        result == ptr@.metadata,
{
    core::ptr::metadata(ptr)
}

} // verus!

fn main() {}