#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::std_specs::cmp::{PartialOrdIs, PartialOrdSpec};

verus! {

pub fn source_range_is_empty<Idx: core::cmp::PartialOrd<Idx>>(
    r: &core::ops::Range<Idx>,
) -> (ret: bool)
where
    Idx: core::cmp::PartialOrd<Idx>,
    requires
        <Idx as PartialOrdSpec<Idx>>::obeys_partial_cmp_spec(),
    ensures
        ret == !r.start.is_lt(&r.end),
{
    let ret = !(r.start < r.end);
    proof {
        assert(ret == !r.start.is_lt(&r.end));
    }
    ret
}

} // verus!

fn main() {}