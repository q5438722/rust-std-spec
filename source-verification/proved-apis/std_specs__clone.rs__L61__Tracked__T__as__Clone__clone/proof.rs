#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::std_specs::clone::*;

verus! {

fn source_tracked_clone<T: Copy>(b: &Tracked<T>) -> (res: Tracked<T>)
    ensures
        res == b,
{
    *b
}

}

fn main() {}