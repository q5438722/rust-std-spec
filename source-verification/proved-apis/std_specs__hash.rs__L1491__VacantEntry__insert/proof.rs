#![feature(allocator_api)]
#![allow(dead_code)]

use core::alloc::Allocator;
use std::collections::hash_map::VacantEntry;
use vstd::prelude::*;
use vstd::std_specs::hash::*;

verus! {

fn source_vacant_entry_insert<'a, K: 'a, V: 'a, A: Allocator>(
    entry: VacantEntry<'a, K, V, A>,
    value: V,
) -> (value_ref: &'a mut V)
    ensures
        *value_ref == value,
        entry.final_value() == Some(*final(value_ref)),
{
    let occupied = entry.insert_entry(value);
    occupied.into_mut()
}

} // verus!

fn main() {}