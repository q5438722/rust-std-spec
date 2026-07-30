#![feature(core_intrinsics)]
#![allow(internal_features)]

use vstd::prelude::*;
use vstd::std_specs::core::*;

verus! {

#[cold]
fn source_cold_path() {
    ()
}

fn source_core_intrinsics_unlikely(b: bool) -> (c: bool)
    ensures
        c == b,
{
    if b {
        source_cold_path();
        true
    } else {
        false
    }
}

} // verus!

fn main() {}