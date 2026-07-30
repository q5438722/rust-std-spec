#![allow(dead_code)]
#![allow(unused_imports)]

use std::collections::BTreeMap;
use vstd::prelude::*;
use vstd::std_specs::btree::*;

verus! {

fn btree_map_default_proof<K, V>() -> (m: BTreeMap<K, V>)
    ensures
        m@ == Map::<K, V>::empty(),
{
    BTreeMap::new()
}

}

fn main() {}