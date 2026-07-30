#![allow(dead_code)]

use vstd::prelude::*;
use vstd::std_specs::bits::*;

verus! {

fn u8_leading_ones_proof(i: u8) -> (r: u32)
    ensures
        r == u8_leading_ones(i),
{
    (!i).leading_zeros()
}

} // verus!

fn main() {}