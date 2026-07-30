#![feature(sized_hierarchy)]
#![allow(dead_code)]
#![allow(unused_imports)]

use core::cmp::{Ordering, PartialOrd};
use core::marker::PointeeSized;
use vstd::prelude::*;
use vstd::std_specs::cmp::*;

verus! {

fn source_ref_partial_cmp<'a, A: PointeeSized, B: PointeeSized>(
    a: &&'a A,
    b: &&B,
) -> (r: Option<Ordering>)
where
    A: PartialOrd<B>,
    ensures
        <&'a A as PartialOrdSpec<&B>>::obeys_partial_cmp_spec() ==>
            r == <&'a A as PartialOrdSpec<&B>>::partial_cmp_spec(a, b),
{
    PartialOrd::partial_cmp(*a, *b)
}

}

fn main() {}