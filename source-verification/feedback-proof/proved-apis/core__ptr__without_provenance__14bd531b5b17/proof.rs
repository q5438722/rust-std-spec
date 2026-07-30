#![allow(dead_code)]

use core::ptr::without_provenance_mut;
use vstd::prelude::*;
use vstd::raw_ptr::Provenance;

verus! {

pub assume_specification<T>[core::ptr::without_provenance_mut::<T>](
    addr: usize,
) -> (result: *mut T)
    ensures
        result@.addr == addr,
        result@.provenance == Provenance::null(),
        result@.metadata == (),
    opens_invariants none
    no_unwind
;

pub fn source_core_ptr_without_provenance<T>(
    addr: usize,
) -> (result: *const T)
    ensures
        result@.addr == addr,
        result@.provenance == Provenance::null(),
        result@.metadata == (),
    opens_invariants none
    no_unwind
{
    without_provenance_mut(addr)
}

}

fn main() {}