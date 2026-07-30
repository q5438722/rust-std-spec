#![feature(core_intrinsics)]
#![allow(internal_features)]

use vstd::prelude::*;
use vstd::std_specs::core::*;

verus! {

#[cold]
pub const fn cold_path() {}

#[inline(always)]
pub const fn core_intrinsics_likely_proof(b: bool) -> (c: bool)
    ensures
        c == b,
{
    if b {
        true
    } else {
        cold_path();
        false
    }
}

} // verus!

fn main() {}