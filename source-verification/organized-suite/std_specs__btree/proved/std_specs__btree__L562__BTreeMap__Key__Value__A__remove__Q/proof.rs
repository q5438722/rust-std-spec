#![feature(allocator_api)]
#![allow(dead_code)]

extern crate alloc;

use alloc::alloc::Allocator;
use alloc::collections::BTreeMap;
use core::borrow::Borrow;
use core::option::Option;
use vstd::laws_cmp::obeys_cmp;
use vstd::prelude::*;
use vstd::std_specs::btree::*;

verus! {

pub assume_specification<
    Key: Borrow<Q> + Ord,
    Value,
    A: Allocator + Clone,
    Q: Ord + ?Sized,
>[ BTreeMap::<Key, Value, A>::remove_entry::<Q> ](
    m: &mut BTreeMap<Key, Value, A>,
    k: &Q,
) -> (result: Option<(Key, Value)>)
    ensures
        obeys_cmp::<Key>() ==> {
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

fn btree_map_remove_proof<
    Key: Borrow<Q> + Ord,
    Value,
    A: Allocator + Clone,
    Q: Ord + ?Sized,
>(
    m: &mut BTreeMap<Key, Value, A>,
    k: &Q,
) -> (result: Option<Value>)
    ensures
        obeys_cmp::<Key>() ==> {
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