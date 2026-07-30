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
use vstd::raw_ptr::MemContents;
use core::mem::MaybeUninit;
use vstd::std_specs::maybe_uninit::*;
verus! {

#[verifier::external_body]
pub fn external_std_specs__maybe_uninit_rs__l45__maybeuninit__t__assume_init_ref<T>(m: &MaybeUninit<T>) -> (ret: &T)
    requires m.mem_contents().is_init(),
    ensures ret == m.mem_contents().value(),
    opens_invariants none
    no_unwind
    { loop { } }

}

fn main() {}
