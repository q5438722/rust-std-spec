#![allow(dead_code)]

use core::ffi::CStr;
use vstd::prelude::*;
use vstd::std_specs::ffi::*;
use vstd::std_specs::slice::*;

verus! {

fn source_cstr_to_bytes(value: &CStr) -> (result: &[u8])
    ensures
        result@ == value@,
{
    let bytes = value.to_bytes_with_nul();
    assert(bytes@.len() > 0);
    // Desugar from_raw_parts(bytes.as_ptr(), len - 1) to the same prefix.
    let (result, _) = bytes.split_at(bytes.len() - 1);
    result
}

} // verus!

fn main() {}