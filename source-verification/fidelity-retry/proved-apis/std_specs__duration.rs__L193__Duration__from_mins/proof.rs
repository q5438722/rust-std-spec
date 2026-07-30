#![allow(dead_code)]

use core::time::Duration;
use vstd::prelude::*;
use vstd::std_specs::duration::nanos_per_second;

verus! {

const SECS_PER_MINUTE: u64 = 60;
const FROM_MINS_OVERFLOW: &'static str = "overflow in Duration::from_mins";

fn source_duration_from_mins(mins: u64) -> (result: Duration)
    requires
        mins as nat * 60 <= u64::MAX as nat,
    ensures
        result@ == mins as nat * 60 * nanos_per_second(),
{
    if mins > u64::MAX / SECS_PER_MINUTE {
        proof {
            assert(false);
        }
        vstd::vpanic!(FROM_MINS_OVERFLOW);
    }

    Duration::from_secs(mins * SECS_PER_MINUTE)
}

} // verus!

fn main() {}