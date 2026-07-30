#![allow(dead_code)]

use vstd::prelude::*;
use vstd::std_specs::bits::*;

verus! {

fn source_u64_leading_ones(i: u64) -> (r: u32)
    ensures
        r == u64_leading_ones(i),
{
    (!i).leading_zeros()
}

} // verus!

fn main() {}