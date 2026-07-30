#![feature(allocator_api)]
#![allow(dead_code)]

use core::alloc::Allocator;
use std::collections::hash_map::{Entry, OccupiedEntry};
use vstd::prelude::*;
use vstd::std_specs::hash::*;

verus! {

fn source_entry_insert_entry<'a, K, V, A: Allocator>(
    entry: Entry<'a, K, V, A>,
    value: V,
) -> (occ_entry: OccupiedEntry<'a, K, V, A>)
    ensures
        occ_entry.key() == entry.key(),
        occ_entry.value() == value,
        entry.final_value() == occ_entry.final_value(),
{
    match entry {
        Entry::Occupied(mut entry) => {
            entry.insert(value);
            entry
        }
        Entry::Vacant(entry) => entry.insert_entry(value),
    }
}

} // verus!

fn main() {}