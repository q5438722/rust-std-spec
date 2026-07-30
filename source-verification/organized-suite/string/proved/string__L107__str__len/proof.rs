#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::string::*;

verus! {

fn str_len_proof(s: &str) -> (len: usize)
    ensures
        len == s.spec_bytes().len() as usize,
{
    let bytes = s.as_bytes();
    let len = <[u8]>::len(bytes);
    proof {
        vstd::slice::axiom_spec_len(bytes);
    }
    len
}

} // verus!

fn main() {}