#![allow(dead_code)]
#![allow(unused_imports)]

use std::collections::HashMap;
use vstd::prelude::*;
use vstd::std_specs::hash::*;

verus! {

pub assume_specification<K, V, S>[
    HashMap::<K, V, S>::with_hasher
](hash_builder: S) -> (m: HashMap<K, V, S>)
    ensures
        m@ == Map::<K, V>::empty(),
;

fn hash_map_default_proof<K, V, S: core::default::Default>() -> (m: HashMap<K, V, S>)
    ensures
        m@ == Map::<K, V>::empty(),
{
    HashMap::with_hasher(Default::default())
}

}

fn main() {}