#![allow(dead_code)]

use core::time::Duration;
use vstd::prelude::*;
use vstd::std_specs::duration::*;

verus! {

const NANOS_PER_MICRO: u32 = 1_000;

fn source_duration_subsec_micros(duration: &Duration) -> (result: u32)
    ensures
        result as nat == duration@ % nanos_per_second() / 1_000,
{
    let nanos = duration.subsec_nanos();
    proof {
        assert(nanos as nat == duration@ % nanos_per_second());
    }
    nanos / NANOS_PER_MICRO
}

}

fn main() {}