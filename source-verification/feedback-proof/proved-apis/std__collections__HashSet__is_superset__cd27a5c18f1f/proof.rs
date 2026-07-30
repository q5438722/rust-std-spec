#![allow(dead_code)]
#![feature(allocator_api)]

use vstd::prelude::*;
use vstd::std_specs::hash::{builds_valid_hashers, obeys_key_model};

verus! {

pub assume_specification<
    Key: core::cmp::Eq + core::hash::Hash,
    S: core::hash::BuildHasher,
    A: core::alloc::Allocator,
>[ std::collections::HashSet::<Key, S, A>::is_subset ](
    m: &std::collections::HashSet<Key, S, A>,
    other: &std::collections::HashSet<Key, S, A>,
) -> (result: bool)
    requires
        obeys_key_model::<Key>(),
        builds_valid_hashers::<S>(),
    ensures
        result == m@.subset_of(other@),
;

fn source_hash_set_is_superset<
    Key: core::cmp::Eq + core::hash::Hash,
    S: core::hash::BuildHasher,
    A: core::alloc::Allocator,
>(
    m: &std::collections::HashSet<Key, S, A>,
    other: &std::collections::HashSet<Key, S, A>,
) -> (result: bool)
    requires
        obeys_key_model::<Key>(),
        builds_valid_hashers::<S>(),
    ensures
        result == other@.subset_of(m@),
{
    let result = other.is_subset(m);
    proof {
        assert(result == other@.subset_of(m@));
    }
    result
}

}

fn main() {}