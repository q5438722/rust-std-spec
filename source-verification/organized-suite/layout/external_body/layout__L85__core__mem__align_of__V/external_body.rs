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
use vstd::arithmetic::power::*;
use vstd::arithmetic::power2::*;
use vstd::bits::*;
use vstd::math::*;
use vstd::prelude::*;
use core::mem::MaybeUninit;
use vstd::layout::*;
verus! {

#[verifier::external_body]
pub fn external_layout_rs__l85__core__mem__align_of__v<V>() -> (u: usize)
    ensures
        u as nat == align_of::<V>(),
    opens_invariants none
    no_unwind
    { loop { } }

}

fn main() {}
