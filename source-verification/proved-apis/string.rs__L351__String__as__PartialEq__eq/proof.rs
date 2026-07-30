#![allow(dead_code)]
#![allow(unused_imports)]

extern crate alloc;

use alloc::string::String;
use core::cmp::PartialEq;
use vstd::prelude::*;
use vstd::string::*;
use vstd::utf8::*;

verus! {

fn source_slice_eq_u8(lhs: &[u8], rhs: &[u8]) -> (res: bool)
    ensures
        res == (lhs@ == rhs@),
{
    // Desugars Vec<u8>'s delegated slice equality.
    let len = lhs.len();
    if len == rhs.len() {
        let mut idx = 0usize;
        while idx < len
            invariant
                len == lhs@.len(),
                len == rhs@.len(),
                idx <= len,
                forall|i: int| 0 <= i < idx ==> lhs@[i] == rhs@[i],
            decreases len - idx,
        {
            let equal = PartialEq::eq(&lhs[idx], &rhs[idx]);
            if !equal {
                assert(lhs@ != rhs@);
                return false;
            }
            idx += 1;
        }
        assert(lhs@ =~= rhs@);
        true
    } else {
        assert(lhs@ != rhs@);
        false
    }
}

fn source_string_partial_eq_eq(s: &String, other: &String) -> (res: bool)
    ensures
        res == (s@ == other@),
{
    // The derive expands to `self.vec == other.vec`; these projections expose those bytes.
    let lhs = s.as_str().as_bytes();
    let rhs = other.as_str().as_bytes();
    let equal = source_slice_eq_u8(lhs, rhs);

    proof {
        encode_utf8_decode_utf8(s@);
        encode_utf8_decode_utf8(other@);
        if lhs@ == rhs@ {
            assert(decode_utf8(lhs@) == decode_utf8(rhs@));
            assert(s@ == other@);
        }
    }

    equal
}

}

fn main() {}