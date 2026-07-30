#![allow(dead_code)]
#![allow(unused_imports)]
#![feature(panic_internals)]

use core::option::Option;
use vstd::prelude::*;
use vstd::std_specs::option::*;

#[cfg(not(verus_keep_ghost))]
use core::panicking::panic;

verus! {

#[cfg(verus_keep_ghost)]
fn panic(expr: &'static str) -> !
    requires
        false,
{
    vstd::vpanic!(expr)
}

#[cfg_attr(not(panic = "immediate-abort"), inline(never))]
#[cfg_attr(panic = "immediate-abort", inline)]
#[cold]
#[track_caller]
fn unwrap_failed() -> !
    requires
        false,
{
    panic("called `Option::unwrap()` on a `None` value")
}

#[inline(always)]
#[track_caller]
pub fn source_option_unwrap<T>(option: Option<T>) -> (t: T)
    requires
        option is Some,
    ensures
        t == spec_unwrap(option),
{
    match option {
        Some(val) => val,
        None => unwrap_failed(),
    }
}

} // verus!

fn main() {}