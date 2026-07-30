#![allow(dead_code)]

extern crate alloc;

use alloc::ffi::CString;
use core::ffi::CStr;
use vstd::prelude::*;
use vstd::std_specs::ffi::*;

verus! {

axiom fn axiom_cstring_view_valid(value: &CString)
    ensures
        c_string_bytes_valid(value@),
;

pub assume_specification[ CStr::from_bytes_with_nul_unchecked ](
    bytes: &[u8],
) -> (result: &CStr)
    requires
        c_string_bytes_with_nul_valid(bytes@),
    ensures
        result@ == bytes@.drop_last(),
;

fn source_cstring_as_c_str(value: &CString) -> (result: &CStr)
    ensures
        result@ == value@,
{
    let bytes = value.as_bytes_with_nul();
    proof {
        axiom_cstring_view_valid(value);
        assert(bytes@.len() > 0);
        assert(bytes@.last() == 0);
        assert(bytes@.drop_last() == value@);
        assert(c_string_bytes_valid(bytes@.drop_last()));
        assert(c_string_bytes_with_nul_valid(bytes@));
    }
    unsafe { CStr::from_bytes_with_nul_unchecked(bytes) }
}

} // verus!

fn main() {}