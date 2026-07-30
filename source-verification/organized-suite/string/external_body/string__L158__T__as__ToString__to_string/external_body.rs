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
use alloc::str::Chars;
use alloc::string::{self, String, ToString};
use vstd::prelude::*;
use vstd::seq::Seq;
use vstd::slice::*;
use vstd::std_specs::iter::IteratorSpec;
use vstd::utf8::*;
use vstd::view::*;
use vstd::string::*;
verus! {

#[verifier::external_body]
pub fn external_string_rs__l158__t__as__tostring__to_string<T: core::fmt::Display + ?Sized>(
    t: &T,
) -> (res: String)
    ensures
        to_string_from_display_ensures::<T>(t, res),
    { loop { } }

}

fn main() {}
