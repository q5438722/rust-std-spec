#![feature(sized_hierarchy)]
#![allow(dead_code)]

use vstd::prelude::*;

verus! {

pub fn source_core_ptr_map_addr<T: core::marker::PointeeSized, F>(
    ptr: *mut T,
    f: F,
) -> (result: *mut T)
where
    F: FnOnce(usize) -> usize,
    requires
        f.requires((ptr@.addr,)),
    ensures
        f.ensures((ptr@.addr,), result@.addr),
        result@.provenance == ptr@.provenance,
        result@.metadata == ptr@.metadata,
{
    ptr.with_addr(f(ptr.addr()))
}

} // verus!

fn main() {}