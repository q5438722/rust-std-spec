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
use vstd::std_specs::cmp::{ OrdSpec, OrdSpecImpl, PartialEqSpec, PartialEqSpecImpl, PartialOrdSpec, PartialOrdSpecImpl, };
use vstd::std_specs::convert::FromSpecImpl;
use vstd::std_specs::ops::{BitOrSpec, BitOrSpecImpl};
use core::cmp::Ordering;
use core::num::{NonZero, ZeroablePrimitive};
use core::ops::BitOr;
use vstd::std_specs::nonzero::*;
verus! {

#[verifier::external_body]
pub fn external_std_specs__nonzero_rs__l98__nonzero__t__get<T: ZeroablePrimitive>(n: NonZero<T>) -> T
    returns
        n@,
    opens_invariants none
    no_unwind
    { loop { } }

}

fn main() {}
