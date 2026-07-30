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
pub fn external_std_specs__duration_rs__l379__duration__try_from_secs_f64(secs: f64) -> (result: Result<
    Duration,
    TryFromFloatSecsError,
>)
    ensures
        duration_secs_f64_valid(secs) ==> (result matches Ok(value) && value@
            == duration_from_secs_f64_nanos(secs)),
        !duration_secs_f64_valid(secs) ==> (result matches Err(error) && error@
            == if duration_secs_f64_is_negative(secs) {
            TryFromFloatSecsErrorView::Negative
        } else {
            TryFromFloatSecsErrorView::OverflowOrNan
        }),
    { loop { } }

}

fn main() {}
