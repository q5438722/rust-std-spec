#![allow(dead_code)]
#![allow(unused_imports)]

extern crate alloc;

use alloc::borrow::ToOwned;
use alloc::string::String;
use alloc::vec::Vec;
use vstd::assert_seqs_equal;
use vstd::prelude::*;
use vstd::string::*;
use vstd::utf8::*;

verus! {

pub assume_specification<T: Clone>[ <[T] as ToOwned>::to_owned ](
    slice: &[T],
) -> (result: Vec<T>)
    ensures
        result@.len() == slice@.len(),
        forall|i: int| #![all_triggers]
            0 <= i < slice@.len() ==> cloned::<T>(slice@[i], result@[i]),
;

pub assume_specification[ String::from_utf8_unchecked ](
    bytes: Vec<u8>,
) -> (result: String)
    requires
        valid_utf8(bytes@),
    ensures
        result@ == decode_utf8(bytes@),
;

fn source_str_to_owned(s: &str) -> (res: String)
    ensures
        s@ == res@,
{
    let slice = s.as_bytes();
    let bytes = slice.to_owned();
    proof {
        assert_seqs_equal!(slice@ == bytes@, i => {
            assert(cloned::<u8>(slice@[i], bytes@[i]));
        });
        encode_utf8_valid_utf8(s@);
    }
    let result = unsafe { String::from_utf8_unchecked(bytes) };
    proof {
        encode_utf8_decode_utf8(s@);
    }
    result
}

} // verus!

fn main() {}