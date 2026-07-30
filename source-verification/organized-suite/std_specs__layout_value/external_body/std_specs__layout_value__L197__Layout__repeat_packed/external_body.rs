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
pub fn external_std_specs__layout_value_rs__l197__layout__repeat_packed(layout: &Layout, n: usize) -> (result: Result<
    Layout,
    LayoutError,
>)
    ensures
        ({
            let size = layout@.size as nat * n as nat;
            size <= usize::MAX as nat && valid_layout(size as usize, layout@.align)
        }) ==> (result matches Ok(new_layout) && new_layout@ == (LayoutView {
            size: (layout@.size as nat * n as nat) as usize,
            align: layout@.align,
        })),
        ({
            let size = layout@.size as nat * n as nat;
            size > usize::MAX as nat || !valid_layout(size as usize, layout@.align)
        }) ==> result is Err,
    { loop { } }

}

fn main() {}
