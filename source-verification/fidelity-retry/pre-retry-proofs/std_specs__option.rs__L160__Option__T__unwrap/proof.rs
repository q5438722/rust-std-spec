#![allow(dead_code)]
#![allow(unused_imports)]

use core::option::Option;
use vstd::prelude::*;
use vstd::std_specs::option::*;

verus! {

fn source_option_unwrap<T>(option: Option<T>) -> (t: T)
    requires
        option is Some,
    ensures
        t == spec_unwrap(option),
{
    match option {
        Some(val) => val,
        None => {
            assert(false);
            vstd::vpanic!("called `Option::unwrap()` on a `None` value")
        },
    }
}

} // verus!

fn main() {}