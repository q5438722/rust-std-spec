#![allow(dead_code)]
#![allow(unused_imports)]

extern crate alloc;

use alloc::string::String;
use vstd::prelude::*;
use vstd::string::*;

verus! {

fn string_deref_proof<'a>(s: &'a String) -> (res: &'a str)
    ensures
        res@ == s@,
{
    s.as_str()
}

} // verus!

fn main() {}