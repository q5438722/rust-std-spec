#![feature(ptr_metadata, sized_hierarchy)]
#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::raw_ptr::*;

verus! {

pub assume_specification<U>[ core::ptr::without_provenance::<U> ](
    addr: usize,
) -> (result: *const U)
    ensures
        result == ptr_from_data(PtrData::<U> {
            addr,
            provenance: Provenance::null(),
            metadata: (),
        }),
    opens_invariants none
    no_unwind
;

pub assume_specification<
    T: core::marker::PointeeSized + core::ptr::Pointee<Metadata = ()>,
    U: Sized,
>[ core::ptr::from_raw_parts ](
    data_pointer: *const U,
    metadata: <T as core::ptr::Pointee>::Metadata,
) -> (result: *const T)
    ensures
        result == ptr_from_data(PtrData::<T> {
            addr: data_pointer@.addr,
            provenance: data_pointer@.provenance,
            metadata,
        }),
    opens_invariants none
    no_unwind
;

fn source_core_ptr_null<
    T: core::marker::PointeeSized + core::ptr::Pointee<Metadata = ()>,
>() -> (res: *const T)
    ensures
        res == ptr_null::<T>(),
{
    core::ptr::from_raw_parts(core::ptr::without_provenance::<()>(0), ())
}

}

fn main() {}