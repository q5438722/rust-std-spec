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
use vstd::laws_cmp::obeys_cmp;
use vstd::prelude::*;
use vstd::std_specs::cmp::OrdSpec;
use vstd::std_specs::iter::IteratorSpec;
use alloc::alloc::Allocator;
use alloc::boxed::Box;
use alloc::collections::btree_map;
use alloc::collections::btree_map::{Keys, Values};
use alloc::collections::btree_set;
use alloc::collections::{BTreeMap, BTreeSet};
use core::borrow::Borrow;
use core::marker::PhantomData;
use core::option::Option;
use vstd::std_specs::btree::*;
verus! {

#[verifier::external_body]
pub fn external_std_specs__btree_rs__l853__btreeset__key__a__get__q<
    'a,
    Key: Borrow<Q> + Ord,
    A: Allocator + Clone,
    Q: Ord + ?Sized,
>(m: &'a BTreeSet<Key, A>, k: &Q) -> (result: Option<&'a Key>)
    ensures
        obeys_cmp::<Key>() ==> match result {
            Some(v) => sets_borrowed_key_to_key(m@, k, v),
            None => !set_contains_borrowed_key(m@, k),
        },
    { loop { } }

}

fn main() {}
