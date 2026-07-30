#![allow(dead_code)]
#![allow(unused_imports)]

extern crate alloc;

use alloc::string::String;
use alloc::vec::Vec;
use vstd::prelude::*;
use vstd::std_specs::vec::*;
use vstd::string::*;
use vstd::utf8::*;

verus! {

pub assume_specification[ String::from_utf8_unchecked ](
    bytes: Vec<u8>,
) -> (result: String)
    requires
        valid_utf8(bytes@),
    ensures
        result@ == decode_utf8(bytes@),
;

pub fn source_string_new() -> (res: String)
    ensures
        res@ == Seq::<char>::empty(),
{
    let bytes = Vec::<u8>::new();
    proof {
        assert(bytes@ == Seq::<u8>::empty());
        assert(valid_utf8(bytes@));
    }

    // Rust 1.96 defines this smaller constructor as `String { vec: bytes }`.
    // Inlining it makes this body exactly `String { vec: Vec::new() }`.
    let result = unsafe { String::from_utf8_unchecked(bytes) };
    assert(result@ == Seq::<char>::empty());
    result
}

} // verus!

fn main() {}