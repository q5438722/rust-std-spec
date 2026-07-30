#![allow(dead_code)]

use std::collections::hash_map::RandomState;
use std::collections::HashSet;
use vstd::prelude::*;
use vstd::std_specs::hash::*;

verus! {

fn hash_set_new_proof<Key>() -> (m: HashSet<Key, RandomState>)
    ensures
        m@ == Set::<Key>::empty(),
{
    Default::default()
}

} // verus!

fn main() {}