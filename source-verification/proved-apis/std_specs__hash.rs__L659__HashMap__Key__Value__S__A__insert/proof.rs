#![feature(allocator_api)]
#![allow(dead_code)]

use core::alloc::Allocator;
use core::hash::{BuildHasher, Hash};
use core::mem;
use core::option::Option;
use core::option::Option::None;
use std::collections::hash_map::Entry;
use std::collections::HashMap;
use vstd::prelude::*;
use vstd::std_specs::hash::*;

verus! {

pub fn source_hash_map_insert<
    Key: Eq + Hash,
    Value,
    S: BuildHasher,
    A: Allocator,
>(
    m: &mut HashMap<Key, Value, S, A>,
    k: Key,
    v: Value,
) -> (result: Option<Value>)
    ensures
        obeys_key_model::<Key>() && builds_valid_hashers::<S>() ==> {
            &&& final(m)@ == old(m)@.insert(k, v)
            &&& match result {
                Some(v) => old(m)@.contains_key(k) && v == old(m)[k],
                None => !old(m)@.contains_key(k),
            }
        },
{
    match m.entry(k) {
        Entry::Occupied(mut entry) => {
            let mut old_value = v;
            mem::swap(entry.get_mut(), &mut old_value);
            Some(old_value)
        },
        Entry::Vacant(entry) => {
            entry.insert_entry(v);
            None
        },
    }
}

} // verus!

fn main() {}