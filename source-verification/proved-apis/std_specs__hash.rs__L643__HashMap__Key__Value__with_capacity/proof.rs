#![allow(dead_code)]

use std::collections::hash_map::RandomState;
use std::collections::HashMap;
use vstd::prelude::*;
use vstd::std_specs::hash::*;

verus! {

pub assume_specification[
    <RandomState as core::default::Default>::default
]() -> RandomState;

pub assume_specification<Key, Value, S>[
    HashMap::<Key, Value, S>::with_capacity_and_hasher
](capacity: usize, hasher: S) -> (m: HashMap<Key, Value, S>)
    ensures
        m@ == Map::<Key, Value>::empty(),
;

fn source_hash_map_with_capacity<Key, Value>(
    capacity: usize,
) -> (m: HashMap<Key, Value, RandomState>)
    ensures
        m@ == Map::<Key, Value>::empty(),
{
    let m = HashMap::with_capacity_and_hasher(capacity, Default::default());
    assert(m@ == Map::<Key, Value>::empty());
    m
}

} // verus!

fn main() {}