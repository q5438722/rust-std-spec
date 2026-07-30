#![feature(core_intrinsics)]
#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::layout::*;
use vstd::prelude::*;

verus! {

pub assume_specification<V>[ core::intrinsics::size_of::<V> ]() -> (u: usize)
    ensures
        u as nat == size_of::<V>(),
    opens_invariants none
    no_unwind
;

fn source_core_mem_size_of<V>() -> (u: usize)
    ensures
        u as nat == size_of::<V>(),
{
    core::intrinsics::size_of::<V>()
}

}

fn main() {}