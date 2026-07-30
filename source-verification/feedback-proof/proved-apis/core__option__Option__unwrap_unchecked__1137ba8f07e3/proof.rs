#![feature(const_precise_live_drops)]
#![allow(dead_code)]

use core::hint;
use core::option::Option;
use vstd::prelude::*;

verus! {

pub const unsafe fn source_option_unwrap_unchecked<T>(
    option: Option<T>,
) -> (ret: T)
    requires
        option is Some,
    ensures
        ret == option->0,
    no_unwind
{
    match option {
        Some(val) => val,
        None => unsafe { hint::unreachable_unchecked() },
    }
}

} // verus!

fn main() {}