#![allow(dead_code)]

extern crate alloc;

use alloc::ffi::CString;
use core::ffi::CStr;
use vstd::prelude::*;

verus! {

fn source_cstr_count_bytes(value: &CStr) -> (result: usize)
    ensures
        result as nat == value@.len(),
{
    value.to_bytes().len()
}

fn source_cstr_is_empty(value: &CStr) -> (result: bool)
    ensures
        result <==> value@.len() == 0,
{
    value.to_bytes().is_empty()
}

fn source_cstring_as_bytes(value: &CString) -> (result: &[u8])
    ensures
        result@ == value@,
{
    value.as_c_str().to_bytes()
}

fn source_cstring_as_bytes_with_nul(value: &CString) -> (result: &[u8])
    ensures
        result@ == value@.push(0),
{
    value.as_c_str().to_bytes_with_nul()
}

} // verus!

fn main() {}
