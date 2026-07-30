#![feature(sized_hierarchy)]
#![allow(dead_code)]
#![allow(unused_imports)]

use core::cmp::{Ord, Ordering};
use core::marker::PointeeSized;
use vstd::prelude::*;
use vstd::std_specs::cmp::*;

verus! {

fn source_ref_cmp<'a, A: PointeeSized + Ord>(
    a: &&'a A,
    b: &&'a A,
) -> (r: Ordering)
    ensures
        <&'a A as OrdSpec>::obeys_cmp_spec() ==>
            r == <&'a A as OrdSpec>::cmp_spec(a, b),
{
    Ord::cmp(*a, *b)
}

}

fn main() {}