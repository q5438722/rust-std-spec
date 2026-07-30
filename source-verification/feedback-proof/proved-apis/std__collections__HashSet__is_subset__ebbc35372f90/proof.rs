#![allow(dead_code)]
#![allow(unused_imports)]
#![feature(allocator_api)]

use core::alloc::Allocator;
use core::hash::{BuildHasher, Hash};
use std::collections::HashSet;
use vstd::prelude::*;
use vstd::std_specs::hash::{builds_valid_hashers, obeys_key_model};
use vstd::std_specs::iter::IteratorSpec;

verus! {

pub fn source_hash_set_is_subset<
    T: Eq + Hash,
    S: BuildHasher,
    A: Allocator,
>(
    m: &HashSet<T, S, A>,
    other: &HashSet<T, S, A>,
) -> (result: bool)
    requires
        obeys_key_model::<T>(),
        builds_valid_hashers::<S>(),
    ensures
        result == m@.subset_of(other@),
{
    if m.len() <= other.len() {
        let mut iter = m.iter();
        let ghost original_iter = iter;
        let result = iter.all(
            |v: &T| -> (found: bool)
                ensures
                    found == other@.contains(*v),
            {
                other.contains(v)
            },
        );

        proof {
            let keys = original_iter.remaining();
            assert(keys.unref().to_set() == m@);
            keys.unref().to_set_ensures();

            if result {
                assert forall|v: T| m@.contains(v) implies other@.contains(v) by {
                    assert(keys.unref().to_set().contains(v));
                    assert(keys.unref().contains(v));
                    let i = choose|i: int| 0 <= i < keys.len() && keys.unref()[i] == v;
                    assert(*keys[i] == v);
                }
            } else {
                let i = keys.len() - iter.remaining().len() - 1;
                assert(0 <= i < keys.len());
                let v = *keys[i];
                assert(keys.unref()[i] == v);
                assert(keys.unref().to_set().contains(v));
                assert(m@.contains(v));
                assert(!other@.contains(v));
                assert(!m@.subset_of(other@));
            }
        }

        result
    } else {
        proof {
            if m@.subset_of(other@) {
                vstd::set_lib::lemma_len_subset(m@, other@);
                assert(m@.len() <= other@.len());
                assert(false);
            }
        }
        false
    }
}

} // verus!

fn main() {}