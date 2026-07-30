#![allow(dead_code)]

use vstd::prelude::*;

verus! {

pub fn source_core_convert_identity<T>(x: T) -> (ret: T)
    ensures
        ret == x,
{
    x
}

} // verus!

fn main() {}