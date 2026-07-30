#![feature(allocator_api)]
#![allow(dead_code)]

use core::alloc::Allocator;
use std::collections::hash_map::Entry;
use vstd::prelude::*;
use vstd::std_specs::hash::*;

verus! {

fn source_entry_or_insert<'a, K, V, A: Allocator>(
    entry: Entry<'a, K, V, A>,
    default: V,
) -> (value: &'a mut V)
    ensures
        *value == (match entry.value() {
            Some(v) => v,
            None => default,
        }),
        entry.final_value() == Some(*final(value)),
{
    match entry {
        Entry::Occupied(entry) => entry.into_mut(),
        Entry::Vacant(entry) => entry.insert(default),
    }
}

} // verus!

fn main() {}