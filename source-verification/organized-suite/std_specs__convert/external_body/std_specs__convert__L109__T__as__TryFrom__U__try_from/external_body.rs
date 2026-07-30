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
use core::convert::{From, Into, TryFrom, TryInto};
use vstd::std_specs::convert::*;
verus! {

#[verifier::external_body]
pub fn external_std_specs__convert_rs__l109__t__as__tryfrom__u__try_from<T, U: Into<T>>(a: U) -> (ret: Result<
    T,
    <T as TryFrom<U>>::Error,
>)
    ensures
        ret.is_ok(),
        call_ensures(U::into, (a,), ret.unwrap()),
    { loop { } }

}

fn main() {}
