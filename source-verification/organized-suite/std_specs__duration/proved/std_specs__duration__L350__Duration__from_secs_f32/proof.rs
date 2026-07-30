#![allow(dead_code)]

use core::time::Duration;
use vstd::prelude::*;
use vstd::std_specs::duration::*;

#[cfg(verus_keep_ghost)]
macro_rules! panic {
    ($($arg:tt)*) => {
        vstd::vpanic!($($arg)*)
    };
}

verus! {

fn duration_from_secs_f32_proof(secs: f32) -> (result: Duration)
    requires
        duration_secs_f32_valid(secs),
    ensures
        result@ == duration_from_secs_f32_nanos(secs),
{
    match Duration::try_from_secs_f32(secs) {
        Ok(v) => v,
        Err(e) => panic!("{e}"),
    }
}

} // verus!

fn main() {}