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
use vstd::seq::*;
use vstd::view::*;
use core::slice::SliceIndex;
use vstd::std_specs::vec::VecAdditionalSpecFns;
use vstd::slice::*;
verus! {

#[verifier::external_body]
pub fn external_slice_rs__l83__t__len<T>(slice: &[T]) -> (len: usize)
    returns
        spec_slice_len(slice),
    { loop { } }

}

fn main() {}
