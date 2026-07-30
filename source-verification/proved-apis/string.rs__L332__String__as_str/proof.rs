#![allow(dead_code)]
#![allow(unused_imports)]

extern crate alloc;

use alloc::string::String;
use vstd::prelude::*;
use vstd::string::*;
use vstd::utf8::*;

verus! {

pub assume_specification<'a>[ String::as_bytes ](
    s: &'a String,
) -> (bytes: &'a [u8])
    ensures
        bytes@ == encode_utf8(s@),
;

pub fn source_string_as_str<'a>(s: &'a String) -> (res: &'a str)
    ensures
        res@ == s@,
{
    // Rust 1.96's `String::as_bytes` is exactly `self.vec.as_slice()`.
    let bytes = s.as_bytes();
    proof {
        encode_utf8_valid_utf8(s@);
    }
    let res = unsafe { str::from_utf8_unchecked(bytes) };
    proof {
        encode_utf8_decode_utf8(res@);
        encode_utf8_decode_utf8(s@);
    }
    res
}

} // verus!

fn main() {}