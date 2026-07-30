#![allow(dead_code)]

use core::option::Option;
use vstd::prelude::*;
use vstd::std_specs::option::*;

verus! {

fn option_unwrap_or_proof<T>(option: Option<T>, default: T) -> (t: T)
    ensures
        t == spec_unwrap_or(option, default),
    no_unwind
{
    match option {
        Some(x) => x,
        None => default,
    }
}

} // verus!

fn main() {}