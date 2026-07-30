#![feature(allocator_api)]
#![allow(dead_code)]

use core::alloc::Allocator;
use std::collections::hash_map::Entry;
use vstd::prelude::*;
use vstd::std_specs::hash::*;

verus! {

fn entry_key_proof<'a, 'b, K, V, A: Allocator>(
    entry: &'b Entry<'a, K, V, A>,
) -> (key: &'b K)
    returns
        &entry.spec_key(),
{
    match *entry {
        Entry::Occupied(ref occupied_entry) => occupied_entry.key(),
        Entry::Vacant(ref vacant_entry) => vacant_entry.key(),
    }
}

} // verus!

fn main() {}