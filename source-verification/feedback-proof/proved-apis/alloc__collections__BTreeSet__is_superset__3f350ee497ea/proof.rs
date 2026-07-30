#![allow(dead_code)]
#![allow(unused_imports)]
#![feature(allocator_api)]

extern crate alloc;

use alloc::alloc::Allocator;
use alloc::collections::BTreeSet;
use vstd::laws_cmp::obeys_cmp;
use vstd::prelude::*;

verus! {

pub assume_specification<T: core::cmp::Ord, A: Allocator + core::clone::Clone>[
    BTreeSet::<T, A>::is_subset
](
    this: &BTreeSet<T, A>,
    other: &BTreeSet<T, A>,
) -> (result: bool)
    requires
        obeys_cmp::<T>(),
    ensures
        result == this@.subset_of(other@),
;

pub fn source_btree_set_is_superset<
    T: core::cmp::Ord,
    A: Allocator + core::clone::Clone,
>(
    this: &BTreeSet<T, A>,
    other: &BTreeSet<T, A>,
) -> (result: bool)
    requires
        obeys_cmp::<T>(),
    ensures
        result == other@.subset_of(this@),
{
    other.is_subset(this)
}

} // verus!

fn main() {}