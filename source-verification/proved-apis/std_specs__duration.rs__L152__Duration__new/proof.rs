#![allow(dead_code)]

use core::time::Duration;
use vstd::prelude::*;
use vstd::std_specs::duration::*;

verus! {

fn source_duration_from_normalized_parts(
    secs: u64,
    nanos: u32,
) -> (result: Duration)
    requires
        nanos < 1_000_000_000,
    ensures
        result@ == secs as nat * nanos_per_second() + nanos as nat,
{
    let total_nanos =
        secs as u128 * 1_000_000_000u128 + nanos as u128;
    proof {
        assert(
            secs as nat * nanos_per_second() + nanos as nat
                <= duration_max_nanos()
        );
    }
    Duration::from_nanos_u128(total_nanos)
}

fn source_duration_new(secs: u64, nanos: u32) -> (result: Duration)
    requires
        secs as nat + nanos as nat / nanos_per_second() <= u64::MAX as nat,
    ensures
        result@ == secs as nat * nanos_per_second() + nanos as nat,
{
    const NANOS_PER_SEC: u32 = 1_000_000_000;

    if nanos < NANOS_PER_SEC {
        source_duration_from_normalized_parts(secs, nanos)
    } else {
        let secs = secs
            .checked_add((nanos / NANOS_PER_SEC) as u64)
            .expect(concat!("overflow in Duration", "::new"));
        let nanos = nanos % NANOS_PER_SEC;
        source_duration_from_normalized_parts(secs, nanos)
    }
}

} // verus!

fn main() {}