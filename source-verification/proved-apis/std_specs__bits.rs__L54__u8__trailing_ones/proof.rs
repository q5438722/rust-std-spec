#![allow(dead_code)]

use vstd::prelude::*;
use vstd::std_specs::bits::*;

verus! {

fn source_u8_trailing_ones(i: u8) -> (r: u32)
    ensures
        r == u8_trailing_ones(i),
{
    (!i).trailing_zeros()
}

} // verus!

fn main() {}