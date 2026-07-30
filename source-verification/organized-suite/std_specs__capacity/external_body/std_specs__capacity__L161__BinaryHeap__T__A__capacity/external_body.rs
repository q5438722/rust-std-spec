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
use vstd::multiset::Multiset;
use vstd::prelude::*;
use vstd::utf8::encode_utf8;
use alloc::collections::{BinaryHeap, TryReserveError, VecDeque};
use alloc::string::String;
use alloc::vec::Vec;
use core::alloc::Allocator;
use vstd::std_specs::capacity::*;
verus! {

#[verifier::external_body]
pub fn external_std_specs__capacity_rs__l161__binaryheap__t__a__capacity<T, A: Allocator>(
    heap: &BinaryHeap<T, A>,
) -> (result: usize)
    ensures
        result as nat == heap.spec_capacity(),
    { loop { } }

}

fn main() {}
