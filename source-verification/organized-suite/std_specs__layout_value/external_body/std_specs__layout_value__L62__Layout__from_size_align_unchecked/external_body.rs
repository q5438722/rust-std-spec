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
use vstd::layout::{ align_of_as_usize, align_of_val_as_usize, size_of_as_usize, size_of_val_as_usize, valid_layout, };
use vstd::prelude::*;
use core::alloc::{Layout, LayoutError};
use vstd::std_specs::layout_value::*;
verus! {

#[verifier::external_body]
pub fn external_std_specs__layout_value_rs__l62__layout__from_size_align_unchecked(size: usize, align: usize) -> (result:
    Layout)
    requires
        valid_layout(size, align),
    ensures
        result@ == (LayoutView { size, align }),
    { loop { } }

}

fn main() {}
