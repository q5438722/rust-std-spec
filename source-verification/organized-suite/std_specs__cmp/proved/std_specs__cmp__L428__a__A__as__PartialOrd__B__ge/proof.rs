#![feature(sized_hierarchy)]
#![allow(dead_code)]
#![allow(unused_imports)]

use core::cmp::{Ordering, PartialOrd};
use core::marker::PointeeSized;
use vstd::prelude::*;
use vstd::std_specs::cmp::*;

verus! {

fn ref_ge_proof<'a, A: PointeeSized, B: PointeeSized>(
    a: &&'a A,
    b: &&B,
) -> (r: bool)
where
    A: PartialOrd<B>,
    ensures
        <&'a A as PartialOrdSpec<&B>>::obeys_partial_cmp_spec() ==>
            (r <==>
                <&'a A as PartialOrdSpec<&B>>::partial_cmp_spec(a, b) matches Some(
                    Ordering::Greater | Ordering::Equal,
                )),
{
    let comparison = <&'a A as PartialOrd<&B>>::partial_cmp(a, b);
    match comparison {
        Some(ordering) => Ordering::is_ge(ordering),
        None => false,
    }
}

}

fn main() {}