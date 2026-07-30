#![feature(sized_hierarchy)]
#![allow(dead_code)]

use vstd::prelude::*;
use vstd::raw_ptr::{ptr_from_data, PtrData};

verus! {

pub fn source_core_ptr_cast<T: core::marker::PointeeSized, U>(
    ptr: *const T,
) -> (result: *const U)
    ensures
        result == ptr_from_data::<U>(PtrData::<U> {
            addr: ptr@.addr,
            provenance: ptr@.provenance,
            metadata: ()
        }),
    opens_invariants none
    no_unwind
{
    ptr as _
}

} // verus!

fn main() {}