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
use vstd::utf8::{decode_utf8, valid_utf8};
use core::ffi::CStr;
use alloc::boxed::Box;
use alloc::ffi::CString;
use alloc::string::FromUtf8Error;
use alloc::string::String;
use alloc::vec::Vec;
use vstd::std_specs::ffi::*;
verus! {

#[verifier::external_body]
pub fn external_std_specs__ffi_rs__l261__cstring__from_vec_with_nul(bytes: Vec<u8>) -> (result: Result<
    CString,
    alloc::ffi::FromVecWithNulError,
>)
    ensures
        c_string_bytes_with_nul_valid(bytes@) ==> (result matches Ok(value) && value@
            == bytes@.drop_last()),
        !c_string_bytes_with_nul_valid(bytes@) ==> result is Err,
    { loop { } }

}

fn main() {}
