#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::std_specs::clone::*;

verus! {

fn source_bool_clone(b: &bool) -> (res: bool)
    ensures
        res == b,
{
    *b
}

}

fn main() {}