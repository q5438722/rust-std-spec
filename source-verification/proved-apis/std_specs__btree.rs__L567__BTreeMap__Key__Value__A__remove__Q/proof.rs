#![feature(allocator_api)]
#![allow(dead_code)]

extern crate alloc;

use alloc::alloc::Allocator;
use alloc::collections::BTreeMap;
use core::borrow::Borrow;
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
                Some((_, v)) => maps_borrowed_key_to_value(old(m)@, k, v),
                None => !contains_borrowed_key(old(m)@, k),
            }
        },
;

fn source_btree_map_remove<
    Key: Borrow<Q> + Ord,
    Value,
    A: Allocator + Clone,
    Q: Ord + ?Sized,
>(
    m: &mut BTreeMap<Key, Value, A>,
    key: &Q,
) -> (result: Option<Value>)
    ensures
        obeys_cmp::<Key>() ==> {
            &&& borrowed_key_removed(old(m)@, final(m)@, key)
            &&& match result {
                Some(v) => maps_borrowed_key_to_value(old(m)@, key, v),
                None => !contains_borrowed_key(old(m)@, key),
            }
        },
{
    m.remove_entry(key).map(
        |entry: (Key, Value)| -> (v: Value)
            ensures v == entry.1,
        {
            entry.1
        },
    )
}

} // verus!

fn main() {}