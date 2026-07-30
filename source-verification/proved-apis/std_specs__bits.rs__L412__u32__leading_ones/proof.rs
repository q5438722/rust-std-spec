#![allow(dead_code)]

use vstd::prelude::*;
use vstd::std_specs::bits::*;

verus! {

fn source_u32_leading_ones(i: u32) -> (r: u32)
    ensures
        r == u32_leading_ones(i),
{
    (!i).leading_zeros()
}

} // verus!

fn main() {}