#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::std_specs::default::*;

verus! {

fn str_default_proof<'a>() -> (r: &'a str)
    ensures
        r == "",
{
    ""
}

} // verus!

fn main() {}