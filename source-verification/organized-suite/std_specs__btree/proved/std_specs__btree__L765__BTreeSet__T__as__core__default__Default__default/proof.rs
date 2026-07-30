#![allow(dead_code)]
#![allow(unused_imports)]

use std::collections::BTreeSet;
use vstd::prelude::*;
use vstd::std_specs::btree::*;

verus! {

fn btree_set_default_proof<T>() -> (m: BTreeSet<T>)
    ensures
        m@ == Set::<T>::empty(),
{
    BTreeSet::new()
}

}

fn main() {}