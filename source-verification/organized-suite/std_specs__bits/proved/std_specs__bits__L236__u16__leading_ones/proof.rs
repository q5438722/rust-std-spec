#![allow(dead_code)]

use vstd::prelude::*;
use vstd::std_specs::bits::*;

verus! {

fn u16_leading_ones_proof(i: u16) -> (r: u32)
    ensures
        r == u16_leading_ones(i),
{
    (!i).leading_zeros()
}

} // verus!

fn main() {}