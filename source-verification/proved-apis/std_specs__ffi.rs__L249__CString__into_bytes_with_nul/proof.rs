#![allow(dead_code)]

extern crate alloc;

use alloc::ffi::CString;
use alloc::vec::Vec;
use vstd::prelude::*;
use vstd::std_specs::ffi::*;

verus! {

fn source_cstring_into_bytes_with_nul(value: CString) -> (result: Vec<u8>)
    ensures
        result@ == value@.push(0),
{
    let mut result = value.into_bytes();
    result.push(0);
    result
}

} // verus!

fn main() {}