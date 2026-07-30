#![allow(dead_code)]
#![allow(unused_imports)]

use std::collections::HashSet;
use vstd::prelude::*;
use vstd::std_specs::hash::*;

verus! {

pub assume_specification<T, S>[
    HashSet::<T, S>::with_hasher
](hash_builder: S) -> (m: HashSet<T, S>)
    ensures
        m@ == Set::<T>::empty(),
;

fn source_hash_set_default<T, S: core::default::Default>() -> (m: HashSet<T, S>)
    ensures
        m@ == Set::<T>::empty(),
{
    HashSet::with_hasher(Default::default())
}

}

fn main() {}