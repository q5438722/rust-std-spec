#![allow(dead_code)]
#![allow(unused_imports)]

use std::string::String;
use vstd::prelude::*;
use vstd::string::*;

verus! {

fn source_string_default() -> (r: String)
    ensures
        r@ == Seq::<char>::empty(),
{
    String::new()
}

}

fn main() {}