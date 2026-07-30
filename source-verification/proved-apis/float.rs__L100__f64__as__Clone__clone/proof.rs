#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::float::*;

verus! {

fn source_f64_clone(f: &f64) -> (res: f64)
    ensures
        res == f,
{
    *f
}

}

fn main() {}