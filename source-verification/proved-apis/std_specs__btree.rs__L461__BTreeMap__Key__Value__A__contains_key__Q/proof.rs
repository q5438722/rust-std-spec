#![feature(allocator_api)]
#![allow(dead_code)]

extern crate alloc;

use alloc::alloc::Allocator;
use alloc::collections::BTreeMap;
use core::borrow::Borrow;
use vstd::prelude::*;
use vstd::std_specs::btree::*;

verus! {

fn source_btree_map_contains_key<
    Key: Borrow<Q> + Ord,
    Value,
    A: Allocator + Clone,
    Q: Ord + ?Sized,
>(
    m: &BTreeMap<Key, Value, A>,
    key: &Q,
) -> (result: bool)
{
    m.get(key).is_some()
}

} // verus!

fn main() {}