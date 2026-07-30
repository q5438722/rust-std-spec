#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::std_specs::default::*;

verus! {

fn source_str_default<'a>() -> (r: &'a str)
    ensures
        r == "",
{
    ""
}

} // verus!

fn main() {}