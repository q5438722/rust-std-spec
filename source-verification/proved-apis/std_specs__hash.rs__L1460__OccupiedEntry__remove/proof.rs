#![feature(allocator_api)]
#![allow(dead_code)]

use core::alloc::Allocator;
use std::collections::hash_map::OccupiedEntry;
use vstd::prelude::*;
use vstd::std_specs::hash::*;

verus! {

fn source_occupied_entry_remove<'a, K, V, A: Allocator>(
    entry: OccupiedEntry<'a, K, V, A>,
) -> (value: V)
    ensures
        value == entry.value(),
        entry.final_value() == None,
{
    entry.remove_entry().1
}

} // verus!

fn main() {}