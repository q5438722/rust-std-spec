#![allow(dead_code)]
#![allow(unused_imports)]

use core::cmp::PartialOrd;
use core::ops::{
    Bound::{Excluded, Included, Unbounded},
    RangeBounds, RangeFrom,
};
use vstd::prelude::*;
use vstd::std_specs::cmp::{PartialOrdIs, PartialOrdSpec};

verus! {

pub fn source_range_from_contains<Idx: PartialOrd<Idx>, U>(
    range: &RangeFrom<Idx>,
    item: &U,
) -> (result: bool)
where
    Idx: PartialOrd<U>,
    U: ?Sized + PartialOrd<Idx>,
    requires
        <Idx as PartialOrdSpec<U>>::obeys_partial_cmp_spec(),
    ensures
        result == range.start.is_le(item),
{
    let result = (match <RangeFrom<Idx> as RangeBounds<Idx>>::start_bound(range) {
        Included(start) => start <= item,
        Excluded(start) => start < item,
        Unbounded => true,
    }) && (match <RangeFrom<Idx> as RangeBounds<Idx>>::end_bound(range) {
        Included(end) => item <= end,
        Excluded(end) => item < end,
        Unbounded => true,
    });
    proof {
        assert(result == range.start.is_le(item));
    }
    result
}

} // verus!

fn main() {}