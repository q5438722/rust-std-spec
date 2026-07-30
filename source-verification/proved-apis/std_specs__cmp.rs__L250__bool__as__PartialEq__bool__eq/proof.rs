#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::std_specs::cmp::*;

verus! {

fn source_bool_eq(x: &bool, y: &bool) -> (res: bool)
    ensures
        res == <bool as PartialEqSpec>::eq_spec(x, y),
{
    *x == *y
}

}

fn main() {}