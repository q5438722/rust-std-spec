#![feature(core_intrinsics)]
#![allow(internal_features)]

use vstd::prelude::*;
use vstd::std_specs::core::*;

verus! {

#[cold]
fn source_cold_path() {
    ()
}

fn source_core_intrinsics_likely(b: bool) -> (c: bool)
    ensures
        c == b,
{
    if b {
        true
    } else {
        source_cold_path();
        false
    }
}

} // verus!

fn main() {}