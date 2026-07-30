#![allow(dead_code)]
#![allow(unused_imports)]

use std::string::String;
use vstd::prelude::*;
use vstd::string::*;

verus! {

fn string_default_proof() -> (r: String)
    ensures
        r@ == Seq::<char>::empty(),
{
    String::new()
}

}

fn main() {}