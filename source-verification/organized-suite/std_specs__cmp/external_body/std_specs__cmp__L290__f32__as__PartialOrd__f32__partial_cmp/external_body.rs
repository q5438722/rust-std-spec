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
use core::cmp::{Eq, Ord, Ordering, PartialEq, PartialOrd};
use core::marker::PointeeSized;
use vstd::std_specs::cmp::*;
verus! {

#[verifier::external_body]
pub fn external_std_specs__cmp_rs__l290__f32__as__partialord__f32__partial_cmp(x: &f32, y: &f32) -> (o: Option<Ordering>)
    ensures
        partial_cmp_ensures::<f32>(*x, *y, o),
    { loop { } }

}

fn main() {}
