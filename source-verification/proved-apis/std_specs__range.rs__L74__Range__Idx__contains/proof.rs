#![allow(dead_code)]
#![allow(unused_imports)]

use core::ops::{
    Bound::{Excluded, Included, Unbounded},
    Range, RangeBounds,
};
use vstd::prelude::*;
use vstd::std_specs::range::*;

verus! {

fn source_range_contains<Idx: PartialOrd<Idx>, U>(
    r: &Range<Idx>,
    item: &U,
) -> (ret: bool)
where
    Idx: PartialOrd<U>,
    U: ?Sized + PartialOrd<Idx>,
    ensures
        <Range<Idx> as ContainsSpec<Idx, U>>::obeys_contains()
            ==> ret == r.contains_spec(item),
{
    let ret = (match <Range<Idx> as RangeBounds<Idx>>::start_bound(r) {
        Included(start) => start <= item,
        Excluded(start) => start < item,
        Unbounded => true,
    }) && (match <Range<Idx> as RangeBounds<Idx>>::end_bound(r) {
        Included(end) => item <= end,
        Excluded(end) => item < end,
        Unbounded => true,
    });
    proof {
        assert(
            <Range<Idx> as ContainsSpec<Idx, U>>::obeys_contains()
                ==> ret == r.contains_spec(item)
        );
    }
    ret
}

}

fn main() {}