#![feature(ptr_metadata, sized_hierarchy)]
#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::raw_ptr::*;

verus! {

pub assume_specification<U>[ core::ptr::without_provenance_mut::<U> ](
    addr: usize,
) -> (res: *mut U)
    ensures
        res == ptr_mut_from_data(PtrData::<U> {
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
>[ core::ptr::from_raw_parts_mut ](
    data_pointer: *mut U,
    metadata: <T as core::ptr::Pointee>::Metadata,
) -> (res: *mut T)
    ensures
        res == ptr_mut_from_data(PtrData::<T> {
            addr: data_pointer@.addr,
            provenance: data_pointer@.provenance,
            metadata,
        }),
    opens_invariants none
    no_unwind
;

fn source_core_ptr_null_mut<
    T: core::marker::PointeeSized + core::ptr::Pointee<Metadata = ()>,
>() -> (res: *mut T)
    ensures
        res == ptr_null_mut::<T>(),
    opens_invariants none
    no_unwind
{
    core::ptr::from_raw_parts_mut(core::ptr::without_provenance_mut::<()>(0), ())
}

} // verus!

fn main() {}