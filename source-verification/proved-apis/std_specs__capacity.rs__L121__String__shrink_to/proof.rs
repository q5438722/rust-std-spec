#![feature(allocator_api)]
#![allow(dead_code)]

extern crate alloc;

use alloc::string::String;
use alloc::vec::Vec;
use vstd::prelude::*;
use vstd::std_specs::capacity::*;
use vstd::utf8::{
    encode_utf8, encode_utf8_decode_utf8, encode_utf8_valid_utf8, valid_utf8,
};

verus! {

pub assume_specification[ String::as_mut_vec ](s: &mut String) -> (v: &mut Vec<u8>)
    ensures
        v@ == encode_utf8(old(s)@),
        v.spec_capacity() == old(s).spec_capacity(),
        final(v).spec_capacity() == final(s).spec_capacity(),
        valid_utf8(final(v)@) ==> final(v)@ == encode_utf8(final(s)@),
;

fn shrink_backing_vec(v: &mut Vec<u8>, min_capacity: usize)
    ensures
        final(v)@ == old(v)@,
        final(v).spec_capacity() >= old(v)@.len(),
        final(v).spec_capacity() <= old(v).spec_capacity(),
{
    Vec::<u8>::shrink_to(v, min_capacity);
}

fn source_string_shrink_to(s: &mut String, min_capacity: usize)
    ensures
        final(s)@ == old(s)@,
        final(s).spec_capacity() >= encode_utf8(old(s)@).len(),
        final(s).spec_capacity() <= old(s).spec_capacity(),
{
    unsafe {
        let v = s.as_mut_vec();
        shrink_backing_vec(v, min_capacity);
    }
    proof {
        encode_utf8_valid_utf8(old(s)@);
        encode_utf8_decode_utf8(s@);
        encode_utf8_decode_utf8(old(s)@);
    }
}

} // verus!

fn main() {}