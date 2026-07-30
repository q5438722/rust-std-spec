#![feature(allocator_api)]
#![allow(dead_code)]

extern crate alloc;

use alloc::collections::TryReserveError;
use alloc::string::String;
use alloc::vec::Vec;
use vstd::prelude::*;
use vstd::std_specs::capacity::*;
use vstd::utf8::{
    encode_utf8, encode_utf8_decode_utf8, encode_utf8_valid_utf8, valid_utf8,
};

verus! {

pub assume_specification[ String::as_mut_vec ](
    s: &mut String,
) -> (v: &mut Vec<u8>)
    ensures
        v@ == encode_utf8(old(s)@),
        v.spec_capacity() == old(s).spec_capacity(),
        final(v).spec_capacity() == final(s).spec_capacity(),
        valid_utf8(final(v)@) ==> final(v)@ == encode_utf8(final(s)@),
;

fn reserve_exact_on_backing_vec(
    v: &mut Vec<u8>,
    additional: usize,
) -> (result: Result<(), TryReserveError>)
    ensures
        final(v)@ == old(v)@,
        result is Ok ==> final(v).spec_capacity()
            >= old(v)@.len() + additional as nat,
{
    Vec::<u8>::try_reserve_exact(v, additional)
}

fn source_string_try_reserve_exact(
    s: &mut String,
    additional: usize,
) -> (result: Result<(), TryReserveError>)
    ensures
        final(s)@ == old(s)@,
        result is Ok ==> final(s).spec_capacity()
            >= encode_utf8(old(s)@).len() + additional as nat,
{
    let ghost old_view = s@;
    let result = unsafe {
        let v = s.as_mut_vec();
        reserve_exact_on_backing_vec(v, additional)
    };
    proof {
        encode_utf8_valid_utf8(old_view);
        encode_utf8_decode_utf8(s@);
        encode_utf8_decode_utf8(old_view);
    }
    result
}

} // verus!

fn main() {}