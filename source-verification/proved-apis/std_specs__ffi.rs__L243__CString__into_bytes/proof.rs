#![allow(dead_code)]

extern crate alloc;

use alloc::ffi::CString;
use alloc::vec::Vec;
use vstd::prelude::*;
use vstd::std_specs::ffi::*;

verus! {

fn source_cstring_into_bytes(value: CString) -> (result: Vec<u8>)
    ensures
        result@ == value@,
{
    // This public sibling is exactly `self.into_inner().into_vec()`.
    let mut vec = value.into_bytes_with_nul();
    let _nul = vec.pop();
    proof {
        // Desugars the unsupported `debug_assert_eq!` after proving its condition.
        assert(_nul == Some(0u8));
        assert(vec@ == value@);
    }
    vec
}

} // verus!

fn main() {}