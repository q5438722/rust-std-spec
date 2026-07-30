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
pub fn external_std_specs__layout_value_rs__l113__layout__extend(layout: &Layout, next: Layout) -> (result: Result<
    (Layout, usize),
    LayoutError,
>)
    ensures
        ({
            let offset = round_up_to(layout@.size as nat, next@.align as nat);
            let size = offset + next@.size as nat;
            size <= usize::MAX as nat && valid_layout(
                size as usize,
                max_usize(layout@.align, next@.align),
            )
        }) ==> ({
            let offset = round_up_to(layout@.size as nat, next@.align as nat);
            let size = offset + next@.size as nat;
            result matches Ok(pair) && pair.0@ == (LayoutView {
                size: size as usize,
                align: max_usize(layout@.align, next@.align),
            }) && pair.1 as nat == offset
        }),
        ({
            let offset = round_up_to(layout@.size as nat, next@.align as nat);
            let size = offset + next@.size as nat;
            size > usize::MAX as nat || !valid_layout(
                size as usize,
                max_usize(layout@.align, next@.align),
            )
        }) ==> result is Err,
    { loop { } }

}

fn main() {}
