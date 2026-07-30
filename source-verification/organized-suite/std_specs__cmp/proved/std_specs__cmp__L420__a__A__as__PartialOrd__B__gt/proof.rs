#![feature(sized_hierarchy)]
#![allow(dead_code)]
#![allow(unused_imports)]

use core::cmp::{Ordering, PartialOrd};
use core::marker::PointeeSized;
use vstd::prelude::*;
use vstd::std_specs::cmp::*;

verus! {

fn ref_gt_proof<'a, A: PointeeSized, B: PointeeSized>(
    a: &&'a A,
    b: &&B,
) -> (r: bool)
where
    A: PartialOrd<B>,
    ensures
        <&'a A as PartialOrdSpec<&B>>::obeys_partial_cmp_spec() ==>
            (r <==>
                <&'a A as PartialOrdSpec<&B>>::partial_cmp_spec(a, b)
                    == Some(Ordering::Greater)),
        exists|o: Option<Ordering>|
            {
                &&& #[trigger] call_ensures(
                    <&'a A as PartialOrd<&B>>::partial_cmp,
                    (a, b),
                    o,
                )
                &&& r <==> o == Some(Ordering::Greater)
            },
{
    let comparison = <&'a A as PartialOrd<&B>>::partial_cmp(a, b);
    let result = match comparison {
        Some(ordering) => Ordering::is_gt(ordering),
        None => false,
    };
    proof {
        assert(result <==> comparison == Some(Ordering::Greater));
    }
    result
}

}

fn main() {}