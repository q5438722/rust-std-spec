#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::std_specs::cmp::*;

verus! {

fn bool_eq_proof(x: &bool, y: &bool) -> (res: bool)
    ensures
        res == <bool as PartialEqSpec>::eq_spec(x, y),
{
    *x == *y
}

}

fn main() {}