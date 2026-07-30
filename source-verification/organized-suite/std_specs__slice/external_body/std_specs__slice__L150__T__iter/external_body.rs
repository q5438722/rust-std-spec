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
use vstd::slice::SliceIndexSpec;
use vstd::std_specs::core::{IndexSetTrustedSpec, IndexSpec};
use vstd::std_specs::iter::IteratorSpec;
use vstd::std_specs::range::{slice_range_end, slice_range_start, slice_range_valid};
use core::ops::{Index, Range};
use core::slice::{Iter, SliceIndex};
use vstd::std_specs::slice::*;
verus! {

#[verifier::external_body]
pub fn external_std_specs__slice_rs__l150__t__iter<'a, T>(s: &'a [T]) -> (iter: Iter<'a, T>)
    ensures
        iter == spec_slice_iter(s),
        IteratorSpec::decrease(&iter) is Some,
        IteratorSpec::initial_value_relation(&iter, &iter),
    { loop { } }

}

fn main() {}
