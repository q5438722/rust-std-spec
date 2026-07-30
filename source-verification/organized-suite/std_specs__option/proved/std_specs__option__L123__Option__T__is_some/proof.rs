#![allow(dead_code)]

use core::option::Option;
use vstd::prelude::*;
use vstd::std_specs::option::*;

verus! {

fn option_is_some_proof<T>(option: &Option<T>) -> (b: bool)
    ensures
        b == is_some(option),
    no_unwind
{
    match *option {
        Some(_) => true,
        _ => false,
    }
}

}

fn main() {}