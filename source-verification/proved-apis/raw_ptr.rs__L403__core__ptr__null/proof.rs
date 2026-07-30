#![feature(ptr_metadata)]
#![feature(sized_hierarchy)]
#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::raw_ptr::*;

verus! {

pub assume_specification<T>[ core::ptr::without_provenance::<T> ](
    addr: usize,
) -> (res: *const T)
    ensures
        res == ptr_from_data(
            PtrData::<T> {
                addr,
                provenance: Provenance::null(),
                metadata: (),
            },
        ),
    opens_invariants none
    no_unwind
;

pub assume_specification<
    T: core::marker::PointeeSized + core::ptr::Pointee<Metadata = ()>,
    U,
>[ core::ptr::from_raw_parts ](
    data_pointer: *const U,
    metadata: <T as core::ptr::Pointee>::Metadata,
) -> (res: *const T)
    ensures
        res == ptr_from_data(
            PtrData::<T> {
                addr: data_pointer@.addr,
                provenance: data_pointer@.provenance,
                metadata,
            },
        ),
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