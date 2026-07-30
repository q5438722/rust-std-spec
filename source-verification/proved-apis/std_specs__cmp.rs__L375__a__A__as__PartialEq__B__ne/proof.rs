#![feature(sized_hierarchy)]
#![allow(dead_code)]
#![allow(unused_imports)]

use core::cmp::PartialEq;
use core::marker::PointeeSized;
use vstd::prelude::*;
use vstd::std_specs::cmp::*;

verus! {

fn source_ref_ne<'a, A: PointeeSized, B: PointeeSized>(
    a: &&'a A,
    b: &&B,
) -> (r: bool)
where
    A: PartialEq<B>,
    ensures
        <&'a A as PartialEqSpec<&B>>::obeys_eq_spec() ==>
            r == !<&'a A as PartialEqSpec<&B>>::eq_spec(a, b),
        call_ensures(<&'a A as PartialEq<&B>>::eq, (a, b), !r),
{
    !PartialEq::eq(a, b)
}

}

fn main() {}