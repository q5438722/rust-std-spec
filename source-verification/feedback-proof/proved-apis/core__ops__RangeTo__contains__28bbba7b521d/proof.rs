#![allow(dead_code)]
#![allow(unused_imports)]

use core::cmp::PartialOrd;
use core::ops::{
    Bound::{Excluded, Included, Unbounded},
    RangeBounds, RangeTo,
};
use vstd::prelude::*;
use vstd::std_specs::cmp::{PartialOrdIs, PartialOrdSpec};

verus! {

pub fn source_range_to_contains<Idx: PartialOrd<Idx>, U>(
    range: &RangeTo<Idx>,
    item: &U,
) -> (result: bool)
where
    Idx: PartialOrd<U>,
    U: ?Sized + PartialOrd<Idx>,
    ensures
        <U as PartialOrdSpec<Idx>>::obeys_partial_cmp_spec()
            ==> result == item.is_lt(&range.end),
{
    let result = (match <RangeTo<Idx> as RangeBounds<Idx>>::start_bound(range) {
        Included(start) => start <= item,
        Excluded(start) => start < item,
        Unbounded => true,
    }) && (match <RangeTo<Idx> as RangeBounds<Idx>>::end_bound(range) {
        Included(end) => item <= end,
        Excluded(end) => item < end,
        Unbounded => true,
    });
    proof {
        assert(
            <U as PartialOrdSpec<Idx>>::obeys_partial_cmp_spec()
                ==> result == item.is_lt(&range.end)
        );
    }
    result
}

} // verus!

fn main() {}