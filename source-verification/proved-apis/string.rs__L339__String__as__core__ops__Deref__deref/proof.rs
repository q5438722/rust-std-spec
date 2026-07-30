#![allow(dead_code)]
#![allow(unused_imports)]

extern crate alloc;

use alloc::string::String;
use vstd::prelude::*;
use vstd::string::*;

verus! {

fn source_string_deref<'a>(s: &'a String) -> (res: &'a str)
    ensures
        res@ == s@,
{
    s.as_str()
}

} // verus!

fn main() {}