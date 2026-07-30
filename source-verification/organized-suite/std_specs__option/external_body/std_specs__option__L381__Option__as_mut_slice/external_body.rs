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
pub fn external_std_specs__option_rs__l381__option__as_mut_slice<T>(option: &mut Option<T>) -> (res: &mut [T])
    ensures
        res@ == (match *old(option) {
            Some(x) => seq![x],
            None => seq![],
        }),
        final(res)@.len() == res@.len(),  // TODO this should be broadcast for all `&mut [T]`
        final(option)@ == (match *old(option) {
            Some(_) => Some(final(res)@[0]),
            None => None,
        }),
    { loop { } }

}

fn main() {}
