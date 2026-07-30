#![feature(allocator_api)]
#![allow(dead_code)]

use core::alloc::Allocator;
use core::borrow::Borrow;
use core::hash::{BuildHasher, Hash};
use core::option::Option;
use std::collections::HashMap;
use vstd::prelude::*;
use vstd::std_specs::hash::*;

verus! {

pub assume_specification<
    Key: Borrow<Q> + Hash + Eq,
    Value,
    S: BuildHasher,
    A: Allocator,
    Q: Hash + Eq + ?Sized,
>[ HashMap::<Key, Value, S, A>::remove_entry::<Q> ](
    m: &mut HashMap<Key, Value, S, A>,
    k: &Q,
) -> (result: Option<(Key, Value)>)
    ensures
        obeys_key_model::<Key>() && builds_valid_hashers::<S>() ==> {
            &&& borrowed_key_removed(old(m)@, final(m)@, k)
            &&& match result {
                Some((stored_key, v)) => {
                    &&& contains_borrowed_key(old(m)@, k)
                    &&& maps_borrowed_key_to_value(old(m)@, k, v)
                    &&& old(m)@.contains_key(stored_key)
                    &&& old(m)@[stored_key] == v
                    &&& final(m)@ == old(m)@.remove(stored_key)
                },
                None => {
                    &&& !contains_borrowed_key(old(m)@, k)
                    &&& final(m)@ == old(m)@
                },
            }
        },
;

pub fn source_hash_map_remove<
    Key: Borrow<Q> + Hash + Eq,
    Value,
    S: BuildHasher,
    A: Allocator,
    Q: Hash + Eq + ?Sized,
>(
    m: &mut HashMap<Key, Value, S, A>,
    k: &Q,
) -> (result: Option<Value>)
    ensures
        obeys_key_model::<Key>() && builds_valid_hashers::<S>() ==> {
            &&& borrowed_key_removed(old(m)@, final(m)@, k)
            &&& match result {
                Some(v) => maps_borrowed_key_to_value(old(m)@, k, v),
                None => !contains_borrowed_key(old(m)@, k),
            }
        },
{
    match m.remove_entry(k) {
        Some((_, v)) => Some(v),
        None => None,
    }
}

} // verus!

fn main() {}