#![allow(dead_code)]
#![allow(unused_imports)]

use core::cmp::PartialEq;
use vstd::prelude::*;
use vstd::std_specs::cmp::*;

verus! {

fn bool_ne_proof(x: &bool, y: &bool) -> (res: bool)
    ensures
        <bool as PartialEqSpec>::obeys_eq_spec() ==>
            res == !<bool as PartialEqSpec>::eq_spec(x, y),
{
    !PartialEq::eq(x, y)
}

}

fn main() {}