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
use alloc::boxed::Box;
use alloc::rc::Rc;
use alloc::sync::Arc;
use alloc::vec::Vec;
use core::alloc::Allocator;
use vstd::std_specs::smart_ptrs::*;
verus! {

#[verifier::external_body]
pub fn external_std_specs__smart_ptrs_rs__l17__box__t__new<T>(t: T) -> (v: Box<T>)
    ensures
        *v == t,
    { loop { } }

}

fn main() {}
