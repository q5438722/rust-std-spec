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

#[inline]
#[track_caller]
pub fn result_unwrap_err_proof<T: fmt::Debug, E>(
    result: Result<T, E>,
) -> (e: E)
    requires
        result is Err,
    ensures
        e == result->Err_0,
{
    match result {
        Ok(t) => unwrap_failed("called `Result::unwrap_err()` on an `Ok` value", &t),
        Err(e) => e,
    }
}

} // verus!

fn main() {}