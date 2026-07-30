#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::std_specs::clone::*;

verus! {

fn source_ghost_clone<T>(b: &Ghost<T>) -> (res: Ghost<T>)
    ensures
        res == b,
{
    *b
}

}

fn main() {}