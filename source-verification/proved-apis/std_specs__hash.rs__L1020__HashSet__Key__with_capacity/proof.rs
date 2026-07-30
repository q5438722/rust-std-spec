#![allow(dead_code)]

use std::collections::hash_map::RandomState;
use std::collections::HashSet;
use vstd::prelude::*;
use vstd::std_specs::hash::*;

verus! {

pub assume_specification[
    <RandomState as core::default::Default>::default
]() -> RandomState;

pub assume_specification<Key, S>[
    HashSet::<Key, S>::with_capacity_and_hasher
](capacity: usize, hasher: S) -> (m: HashSet<Key, S>)
    ensures
        m@ == Set::<Key>::empty(),
;

fn source_hash_set_with_capacity<Key>(
    capacity: usize,
) -> (m: HashSet<Key, RandomState>)
    ensures
        m@ == Set::<Key>::empty(),
{
    let m = HashSet::with_capacity_and_hasher(capacity, Default::default());
    assert(m@ == Set::<Key>::empty());
    m
}

} // verus!

fn main() {}