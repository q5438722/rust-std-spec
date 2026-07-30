#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::float::*;

verus! {

fn f32_clone_proof(f: &f32) -> (res: f32)
    ensures
        res == f,
{
    *f
}

}

fn main() {}