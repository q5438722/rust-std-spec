#![allow(dead_code)]

use vstd::prelude::*;
use vstd::std_specs::bits::*;

verus! {

fn u16_trailing_ones_proof(i: u16) -> (r: u32)
    ensures
        r == u16_trailing_ones(i),
{
    (!i).trailing_zeros()
}

} // verus!

fn main() {}