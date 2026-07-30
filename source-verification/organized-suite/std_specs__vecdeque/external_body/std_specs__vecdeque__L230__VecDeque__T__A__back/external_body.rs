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
use vstd::std_specs::cmp::{PartialEqSpec, PartialEqSpecImpl};
use vstd::std_specs::iter::IteratorSpec;
use alloc::collections::TryReserveError;
use alloc::collections::vec_deque::Iter;
use alloc::collections::vec_deque::VecDeque;
use core::alloc::Allocator;
use core::clone::Clone;
use core::ops::Index;
use core::option::Option;
use core::option::Option::None;
use vstd::std_specs::vecdeque::*;
verus! {

#[verifier::external_body]
pub fn external_std_specs__vecdeque_rs__l230__vecdeque__t__a__back<T, A: Allocator>(v: &VecDeque<T, A>) -> (result:
    Option<&T>)
    ensures
        v@.len() == 0 ==> result is None,
        v@.len() > 0 ==> (result matches Some(value) && *value == v@.last()),
    { loop { } }

}

fn main() {}
