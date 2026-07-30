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
use core::option::Option;
use vstd::std_specs::option::*;
verus! {

#[verifier::external_body]
pub fn external_std_specs__option_rs__l193__option__t__expect<T>(option: Option<T>, msg: &str) -> (t: T)
    requires
        option is Some,
    ensures
        t == spec_expect(option, msg),
    { loop { } }

}

fn main() {}
