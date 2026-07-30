#![feature(allocator_api)]
#![allow(dead_code)]

extern crate alloc;

use alloc::string::String;
use vstd::prelude::*;
use vstd::std_specs::capacity::*;
use vstd::utf8::encode_utf8;

verus! {

pub fn source_string_shrink_to_fit(s: &mut String)
    ensures
        final(s)@ == old(s)@,
        final(s).spec_capacity() >= encode_utf8(old(s)@).len(),
        final(s).spec_capacity() <= old(s).spec_capacity(),
{
    let len = s.as_str().len();
    // At the byte length, Vec::shrink_to has the same guard and RawVec call
    // as Vec::shrink_to_fit in Rust 1.96.
    s.shrink_to(len);
}

} // verus!

fn main() {}