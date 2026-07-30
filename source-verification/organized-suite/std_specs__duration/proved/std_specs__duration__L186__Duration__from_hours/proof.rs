#![allow(dead_code)]

use core::time::Duration;
use vstd::prelude::*;
use vstd::std_specs::duration::nanos_per_second;

verus! {

const SECS_PER_MINUTE: u64 = 60;
const MINS_PER_HOUR: u64 = 60;
const FROM_HOURS_OVERFLOW: &'static str = "overflow in Duration::from_hours";

fn duration_from_hours_proof(hours: u64) -> (result: Duration)
    requires
        hours as nat * 3_600 <= u64::MAX as nat,
    ensures
        result@ == hours as nat * 3_600 * nanos_per_second(),
{
    if hours > u64::MAX / (SECS_PER_MINUTE * MINS_PER_HOUR) {
        proof {
            assert(false);
        }
        vstd::vpanic!(FROM_HOURS_OVERFLOW);
    }

    Duration::from_secs(hours * MINS_PER_HOUR * SECS_PER_MINUTE)
}

} // verus!

fn main() {}