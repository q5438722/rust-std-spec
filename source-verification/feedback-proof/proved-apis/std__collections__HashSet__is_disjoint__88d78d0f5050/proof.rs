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

pub fn source_hash_set_is_disjoint<
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
        result == m@.disjoint(other@),
{
    if m.len() <= other.len() {
        let mut iter = m.iter();
        let ghost initial_iter = iter;
        let result = iter.all(
            |v: &T| -> (ret: bool)
                ensures
                    ret == !other@.contains(*v),
            {
                !other.contains(v)
            },
        );
        proof {
            let initial = initial_iter.remaining();
            let values = initial.unref();
            assert(values.to_set() == m@);
            values.to_set_ensures();
            if result {
                assert forall|x: T| m@.contains(x) implies !other@.contains(x) by {
                    assert(values.to_set().contains(x));
                    assert(values.contains(x));
                    let i = choose|i: int| 0 <= i < values.len() && values[i] == x;
                    assert(initial.len() == values.len());
                    assert(values[i] == *initial[i]);
                    assert(!other@.contains(*initial[i]));
                }
            } else {
                let i = initial.len() - iter.remaining().len() - 1;
                assert(0 <= i < initial.len());
                assert(values.len() == initial.len());
                assert(values[i] == *initial[i]);
                assert(values.to_set().contains(values[i]));
                assert(m@.contains(*initial[i]));
                assert(other@.contains(*initial[i]));
                assert(!m@.disjoint(other@));
            }
        }
        result
    } else {
        let mut iter = other.iter();
        let ghost initial_iter = iter;
        let result = iter.all(
            |v: &T| -> (ret: bool)
                ensures
                    ret == !m@.contains(*v),
            {
                !m.contains(v)
            },
        );
        proof {
            let initial = initial_iter.remaining();
            let values = initial.unref();
            assert(values.to_set() == other@);
            values.to_set_ensures();
            if result {
                assert forall|x: T| other@.contains(x) implies !m@.contains(x) by {
                    assert(values.to_set().contains(x));
                    assert(values.contains(x));
                    let i = choose|i: int| 0 <= i < values.len() && values[i] == x;
                    assert(initial.len() == values.len());
                    assert(values[i] == *initial[i]);
                    assert(!m@.contains(*initial[i]));
                }
                assert(m@.disjoint(other@)) by {
                    assert forall|x: T| m@.contains(x) implies !other@.contains(x) by {
                        if other@.contains(x) {
                            assert(!m@.contains(x));
                        }
                    }
                }
            } else {
                let i = initial.len() - iter.remaining().len() - 1;
                assert(0 <= i < initial.len());
                assert(values.len() == initial.len());
                assert(values[i] == *initial[i]);
                assert(values.to_set().contains(values[i]));
                assert(other@.contains(*initial[i]));
                assert(m@.contains(*initial[i]));
                assert(!m@.disjoint(other@));
            }
        }
        result
    }
}

} // verus!

fn main() {}