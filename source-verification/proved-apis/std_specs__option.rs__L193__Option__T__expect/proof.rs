#![allow(dead_code)]
#![allow(unused_imports)]

use core::option::Option;
use vstd::prelude::*;
use vstd::std_specs::option::*;

verus! {

fn source_option_expect<T>(option: Option<T>, msg: &str) -> (t: T)
    requires
        option is Some,
    ensures
        t == spec_expect(option, msg),
{
    match option {
        Some(val) => val,
        None => {
            assert(false);
            vstd::vpanic!("{}", msg)
        },
    }
}

} // verus!

fn main() {}