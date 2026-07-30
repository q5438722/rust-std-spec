#![feature(core_intrinsics)]
#![allow(dead_code)]
#![allow(internal_features)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::std_specs::slice::*;

verus! {

pub assume_specification[core::intrinsics::unreachable]() -> !
    requires
        false,
;

pub const unsafe fn source_unreachable_unchecked() -> !
    requires
        false,
{
    proof {
        assert(false);
    }
    unsafe { core::intrinsics::unreachable() }
}

} // verus!

fn main() {}