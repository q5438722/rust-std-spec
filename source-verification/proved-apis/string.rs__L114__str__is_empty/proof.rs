#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::string::*;
use vstd::utf8::*;

verus! {

fn source_str_len(s: &str) -> (len: usize)
    ensures
        len as nat == s.spec_bytes().len(),
{
    let bytes = s.as_bytes();
    let len = <[u8]>::len(bytes);
    proof {
        vstd::slice::axiom_spec_len(bytes);
    }
    len
}

fn source_str_is_empty(s: &str) -> (result: bool)
    ensures
        result <==> s@.len() == 0,
{
    let len = source_str_len(s);
    let result = len == 0;
    proof {
        assert(result <==> s.spec_bytes().len() == 0);
        if s@.len() == 0 {
            assert(s.spec_bytes().len() == 0);
        } else {
            encode_utf8_first_scalar(s@);
            assert(s.spec_bytes().len() > 0);
        }
    }
    result
}

}

fn main() {}