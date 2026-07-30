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
pub fn external_string_rs__l127__str__split_at(s: &str, mid: usize) -> (res: (&str, &str))
    requires
        is_char_boundary(s.spec_bytes(), mid as int),
    ensures
        res.0.spec_bytes() =~= s.spec_bytes().subrange(0, mid as int),
        res.1.spec_bytes() =~= s.spec_bytes().subrange(mid as int, s.spec_bytes().len() as int),
    { loop { } }

}

fn main() {}
