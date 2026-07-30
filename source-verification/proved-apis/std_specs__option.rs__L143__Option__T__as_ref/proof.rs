#![allow(dead_code)]

use core::option::Option;
use vstd::prelude::*;
use vstd::std_specs::option::*;

verus! {

fn source_option_as_ref<T>(option: &Option<T>) -> (a: Option<&T>)
    ensures
        a is Some <==> option is Some,
        a is Some ==> option->0 == a->0,
    no_unwind
{
    match *option {
        Some(ref x) => Some(x),
        None => None,
    }
}

} // verus!

fn main() {}