#![allow(dead_code)]
#![allow(unused_imports)]

use core::fmt;
use core::result::Result;
use vstd::prelude::*;
use vstd::std_specs::result::*;

#[cfg(verus_keep_ghost)]
macro_rules! panic {
    ($($arg:tt)*) => {
        vstd::vpanic!($($arg)*)
    };
}

verus! {

#[cfg(not(panic = "immediate-abort"))]
#[inline(never)]
#[cold]
#[track_caller]
fn unwrap_failed(msg: &str, error: &dyn fmt::Debug) -> !
    requires
        false,
{
    panic!("{msg}: {error:?}");
}

#[cfg(panic = "immediate-abort")]
#[inline]
#[cold]
#[track_caller]
const fn unwrap_failed<T>(_msg: &str, _error: &T) -> !
    requires
        false,
{
    panic!()
}

#[inline(always)]
#[track_caller]
pub fn source_result_unwrap<T, E: fmt::Debug>(result: Result<T, E>) -> (t: T)
    requires
        result is Ok,
    ensures
        t == result->Ok_0,
{
    match result {
        Ok(t) => t,
        Err(e) => unwrap_failed("called `Result::unwrap()` on an `Err` value", &e),
    }
}

} // verus!

fn main() {}