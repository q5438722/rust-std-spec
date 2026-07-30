#![feature(allocator_api)]
#![allow(dead_code)]

use core::alloc::Allocator;
use core::mem;
use std::collections::hash_map::OccupiedEntry;
use vstd::prelude::*;
use vstd::std_specs::hash::*;

verus! {

fn source_occupied_entry_insert<'a, K, V, A: Allocator>(
    entry: &mut OccupiedEntry<'a, K, V, A>,
    value: V,
) -> (old_value: V)
    ensures
        old_value == old(entry).value(),
        final(entry).key() == old(entry).key(),
        final(entry).value() == value,
        final(entry).final_value() == old(entry).final_value(),
{
    let mut old_value = value;
    mem::swap(entry.get_mut(), &mut old_value);
    old_value
}

} // verus!

fn main() {}