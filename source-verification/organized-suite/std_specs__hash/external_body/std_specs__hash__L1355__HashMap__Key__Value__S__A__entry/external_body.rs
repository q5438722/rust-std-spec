#![allow(dead_code, unused_imports, unused_variables)]
#![feature(allocator_api)]
#![feature(box_into_inner)]
#![feature(const_trait_impl)]
#![feature(exact_size_is_empty)]
#![feature(iter_advance_by)]
#![feature(layout_for_ptr)]
#![feature(maybe_uninit_as_bytes)]
#![feature(maybe_uninit_array_assume_init)]
#![feature(never_type)]
#![feature(nonzero_internals)]
#![feature(ptr_metadata)]
#![feature(slice_ptr_get)]
#![feature(sized_hierarchy)]
#![feature(step_trait)]
#![feature(trusted_len)]
#![feature(unsized_fn_params)]
extern crate alloc;
use vstd::prelude::*;
use vstd::prelude::*;
use vstd::std_specs::iter::IteratorSpec;
use core::alloc::Allocator;
use core::borrow::Borrow;
use core::hash::{BuildHasher, Hash, Hasher};
use core::marker::PhantomData;
use core::option::Option;
use core::option::Option::None;
use std::collections::hash_map;
use std::collections::hash_map::{ DefaultHasher, Entry, Keys, OccupiedEntry, RandomState, VacantEntry, Values, };
use std::collections::hash_set;
use std::collections::{HashMap, HashSet};
use vstd::std_specs::hash::*;
verus! {

#[verifier::external_body]
pub fn external_std_specs__hash_rs__l1355__hashmap__key__value__s__a__entry<'a, Key: Hash + Eq, Value, S: BuildHasher, A: Allocator>(m: &'a mut HashMap<Key, Value, S, A>, key: Key) -> (entry: Entry<'a, Key, Value, A>)
    ensures
        obeys_key_model::<Key>() && builds_valid_hashers::<S>() ==> (entry.key() == key
            && entry.value() == old(m)@.get(key) && final(m)@ == (match entry.final_value() {
            Some(value) => old(m)@.insert(key, value),
            None => old(m)@.remove(key),
        })),
    { loop { } }

}

fn main() {}
