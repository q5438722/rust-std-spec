#![allow(dead_code)]
#![allow(unused_imports)]

use core::fmt;
use core::result::Result;
use vstd::prelude::*;

#[cfg(verus_keep_ghost)]
macro_rules! panic {
    ($($arg:tt)*) => {
        vstd::vpanic!($($arg)*)
    };
}

verus! {

#[inline(never)]
#[cold]
#[track_caller]
fn unwrap_failed(msg: &str, error: &dyn fmt::Debug) -> !
    requires
        false,
{
    panic!("{msg}: {error:?}");
}

pub fn source_result_expect_err<T: fmt::Debug, E>(
    result: Result<T, E>,
    msg: &str,
) -> (error: E)
    requires
        result is Err,
    ensures
        error == result->Err_0,
{
    match result {
        Ok(t) => unwrap_failed(msg, &t),
        Err(e) => e,
    }
}

} // verus!

fn main() {}