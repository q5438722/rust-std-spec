#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::float::*;

verus! {

fn source_f32_clone(f: &f32) -> (res: f32)
    ensures
        res == f,
{
    *f
}

}

fn main() {}