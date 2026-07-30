#![feature(nonzero_internals)]
#![allow(dead_code)]
#![allow(unused_imports)]

use core::num::{NonZero, ZeroablePrimitive};
use vstd::prelude::*;
use vstd::std_specs::nonzero::*;

verus! {

fn source_nonzero_clone<T: ZeroablePrimitive>(
    nz: &NonZero<T>,
) -> (res: NonZero<T>)
    ensures
        res == nz,
{
    *nz
}

}

fn main() {}