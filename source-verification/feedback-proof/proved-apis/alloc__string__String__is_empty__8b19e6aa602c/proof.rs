#![allow(dead_code)]
#![allow(unused_imports)]

extern crate alloc;

use alloc::string::String;
use vstd::prelude::*;
use vstd::utf8::{encode_utf8, encode_utf8_first_scalar};

verus! {

pub assume_specification[ String::len ](s: &String) -> (res: usize)
    ensures
        res as nat == encode_utf8(s@).len(),
;

pub fn source_string_is_empty(s: &String) -> (res: bool)
    ensures
        res == (s@.len() == 0),
{
    let res = s.len() == 0;
    proof {
        if s@.len() == 0 {
            assert(encode_utf8(s@).len() == 0);
        } else {
            encode_utf8_first_scalar(s@);
            assert(encode_utf8(s@).len() > 0);
        }
    }
    res
}

} // verus!

fn main() {}