#![allow(dead_code)]

use std::collections::hash_map::RandomState;
use std::collections::HashMap;
use vstd::prelude::*;
use vstd::std_specs::hash::*;

verus! {

fn hash_map_new_proof<Key, Value>() -> (m: HashMap<Key, Value, RandomState>)
    ensures
        m@ == Map::<Key, Value>::empty(),
{
    Default::default()
}

} // verus!

fn main() {}