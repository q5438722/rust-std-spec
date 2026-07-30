#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::std_specs::clone::*;

verus! {

fn char_clone_proof(c: &char) -> (res: char)
    ensures
        res == c,
{
    *c
}

}

fn main() {}