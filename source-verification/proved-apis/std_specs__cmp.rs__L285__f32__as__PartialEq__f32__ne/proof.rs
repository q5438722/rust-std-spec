#![allow(dead_code)]
#![allow(unused_imports)]

use core::cmp::PartialEq;
use vstd::prelude::*;
use vstd::std_specs::cmp::*;

verus! {

pub axiom fn axiom_f32_ne_from_eq(lhs: f32, rhs: f32, equality: bool)
    requires
        eq_ensures::<f32>(lhs, rhs, equality),
    ensures
        ne_ensures::<f32>(lhs, rhs, !equality),
;

fn source_f32_partial_eq_ne(x: &f32, y: &f32) -> (result: bool)
    ensures
        ne_ensures::<f32>(*x, *y, result),
{
    let equality = <f32 as PartialEq<f32>>::eq(x, y);
    let result = !equality;
    proof {
        axiom_f32_ne_from_eq(*x, *y, equality);
    }
    result
}

}

fn main() {}