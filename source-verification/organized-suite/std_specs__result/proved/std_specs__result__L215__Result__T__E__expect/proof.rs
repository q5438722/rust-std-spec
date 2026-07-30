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

#[inline]
#[track_caller]
pub fn result_expect_proof<T, E: fmt::Debug>(
    result: Result<T, E>,
    msg: &str,
) -> (t: T)
    requires
        result is Ok,
    ensures
        t == result->Ok_0,
{
    match result {
        Ok(t) => t,
        Err(e) => unwrap_failed(msg, &e),
    }
}

} // verus!

fn main() {}