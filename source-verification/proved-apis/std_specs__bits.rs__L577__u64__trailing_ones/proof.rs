#![allow(dead_code)]

use vstd::prelude::*;
use vstd::std_specs::bits::*;

verus! {

fn source_u64_trailing_ones(i: u64) -> (r: u32)
    ensures
        r == u64_trailing_ones(i),
{
    (!i).trailing_zeros()
}

} // verus!

fn main() {}