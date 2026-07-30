#![allow(dead_code)]

use core::time::Duration;
use vstd::prelude::*;
use vstd::std_specs::duration::{
    duration_from_secs_f32_nanos, duration_from_secs_f64_nanos, duration_secs_f32_valid,
    duration_secs_f64_valid,
};

verus! {

fn source_duration_from_secs_f32(secs: f32) -> (result: Duration)
    requires
        duration_secs_f32_valid(secs),
    ensures
        result@ == duration_from_secs_f32_nanos(secs),
{
    match Duration::try_from_secs_f32(secs) {
        Ok(result) => result,
        Err(_) => {
            assert(false);
            Duration::new(0, 0)
        },
    }
}

fn source_duration_from_secs_f64(secs: f64) -> (result: Duration)
    requires
        duration_secs_f64_valid(secs),
    ensures
        result@ == duration_from_secs_f64_nanos(secs),
{
    match Duration::try_from_secs_f64(secs) {
        Ok(result) => result,
        Err(_) => {
            assert(false);
            Duration::new(0, 0)
        },
    }
}

} // verus!

fn main() {}
