#![feature(allocator_api)]
#![allow(dead_code)]

extern crate alloc;

use alloc::string::String;
use vstd::prelude::*;
use vstd::std_specs::capacity::*;
use vstd::utf8::encode_utf8;

verus! {

pub assume_specification[std::process::abort]() -> !;

pub fn source_string_reserve_exact(s: &mut String, additional: usize)
    ensures
        final(s)@ == old(s)@,
        final(s).spec_capacity() >= encode_utf8(old(s)@).len() + additional as nat,
{
    match s.try_reserve_exact(additional) {
        Ok(()) => {
            assert(s.spec_capacity() >= encode_utf8(s@).len() + additional as nat);
        }
        Err(_) => std::process::abort(),
    }
}

} // verus!

fn main() {}