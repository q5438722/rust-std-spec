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
use vstd::arithmetic::power2::pow2;
use vstd::float::{FloatBitsProperties, ieee_float_cast};
use vstd::prelude::*;
use core::time::{Duration, TryFromFloatSecsError};
use vstd::std_specs::duration::*;
verus! {

#[verifier::external_body]
pub fn external_std_specs__duration_rs__l164__duration__from_millis(millis: u64) -> (result: Duration)
    ensures
        result@ == millis as nat * 1_000_000,
    { loop { } }

}

fn main() {}
