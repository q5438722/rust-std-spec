#![feature(core_intrinsics)]
#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::layout::align_of;
use vstd::prelude::*;

verus! {

pub assume_specification<T>[ core::intrinsics::align_of::<T> ]() -> (res: usize)
    ensures
        res as nat == align_of::<T>(),
    opens_invariants none
    no_unwind
;

fn source_core_mem_min_align_of<T>() -> (res: usize)
    ensures
        res as nat == align_of::<T>(),
{
    core::intrinsics::align_of::<T>()
}

}

fn main() {}