#![allow(dead_code)]
#![allow(unused_imports)]

use core::cmp::PartialEq;
use vstd::prelude::*;
use vstd::std_specs::cmp::*;

verus! {

pub axiom fn axiom_f64_ne_from_eq(lhs: f64, rhs: f64, equality: bool)
    requires
        eq_ensures::<f64>(lhs, rhs, equality),
    ensures
        ne_ensures::<f64>(lhs, rhs, !equality),
;

fn source_f64_partial_eq_ne(x: &f64, y: &f64) -> (result: bool)
    ensures
        ne_ensures::<f64>(*x, *y, result),
{
    let equality = <f64 as PartialEq<f64>>::eq(x, y);
    let result = !equality;
    proof {
        axiom_f64_ne_from_eq(*x, *y, equality);
    }
    result
}

}

fn main() {}