#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::std_specs::clone::*;

verus! {

fn bool_clone_proof(b: &bool) -> (res: bool)
    ensures
        res == b,
{
    *b
}

}

fn main() {}