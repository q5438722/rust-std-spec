#![allow(dead_code)]
#![allow(unused_imports)]

use core::cmp::PartialEq;
use core::option::Option;
use vstd::prelude::*;
use vstd::std_specs::cmp::*;
use vstd::std_specs::option::*;

verus! {

fn option_eq_proof<T: PartialEq>(
    x: &Option<T>,
    y: &Option<T>,
) -> (res: bool)
    ensures
        <Option<T> as PartialEqSpec>::obeys_eq_spec() ==>
            res == <Option<T> as PartialEqSpec>::eq_spec(x, y),
{
    match (x, y) {
        (Some(l), Some(r)) => *l == *r,
        (Some(_), None) => false,
        (None, Some(_)) => false,
        (None, None) => true,
    }
}

}

fn main() {}