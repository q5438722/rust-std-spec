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
use vstd::layout::*;
use vstd::prelude::*;
use vstd::raw_ptr::*;
verus! {

#[verifier::external_body]
pub fn external_raw_ptr_rs__l198__mut__t__as__partialeq__mut__t__eq<T: core::marker::PointeeSized>(
    x: &*mut T,
    y: &*mut T,
) -> (res: bool)
    ensures
        res <==> (x@.addr == y@.addr) && (x@.metadata == y@.metadata),
    { loop { } }

}

fn main() {}
