#![allow(dead_code)]

use core::ffi::CStr;
use core::str;
use vstd::prelude::*;
use vstd::std_specs::ffi::*;
use vstd::utf8::{decode_utf8, valid_utf8};

verus! {

pub assume_specification[ str::from_utf8 ](bytes: &[u8]) -> (result: Result<
    &str,
    core::str::Utf8Error,
>)
    ensures
        valid_utf8(bytes@) ==> (result matches Ok(string)
            && string@ == decode_utf8(bytes@)),
        !valid_utf8(bytes@) ==> result is Err,
;

fn source_cstr_to_str(value: &CStr) -> (result: Result<&str, core::str::Utf8Error>)
    ensures
        valid_utf8(value@) ==> (result matches Ok(string) && string@ == decode_utf8(value@)),
        !valid_utf8(value@) ==> result is Err,
{
    str::from_utf8(value.to_bytes())
}

} // verus!

fn main() {}