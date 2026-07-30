#![allow(dead_code)]

use core::time::Duration;
use vstd::prelude::*;
use vstd::std_specs::duration::{
    axiom_duration_view_valid, duration_max_nanos, nanos_per_second,
};

verus! {

fn source_duration_from_secs(secs: u64) -> (result: Duration)
    ensures
        result@ == secs as nat * nanos_per_second(),
{
    Duration::new(secs, 0)
}

fn source_duration_from_millis(millis: u64) -> (result: Duration)
    ensures
        result@ == millis as nat * 1_000_000,
{
    let secs = millis / 1_000;
    let subsec_millis = (millis % 1_000) as u32;
    Duration::new(secs, subsec_millis * 1_000_000)
}

fn source_duration_from_micros(micros: u64) -> (result: Duration)
    ensures
        result@ == micros as nat * 1_000,
{
    let secs = micros / 1_000_000;
    let subsec_micros = (micros % 1_000_000) as u32;
    Duration::new(secs, subsec_micros * 1_000)
}

fn source_duration_from_nanos(nanos: u64) -> (result: Duration)
    ensures
        result@ == nanos as nat,
{
    let secs = nanos / 1_000_000_000;
    let subsec_nanos = (nanos % 1_000_000_000) as u32;
    Duration::new(secs, subsec_nanos)
}

fn source_duration_from_nanos_u128(nanos: u128) -> (result: Duration)
    requires
        nanos as nat <= duration_max_nanos(),
    ensures
        result@ == nanos as nat,
{
    let secs = (nanos / 1_000_000_000) as u64;
    let subsec_nanos = (nanos % 1_000_000_000) as u32;
    Duration::new(secs, subsec_nanos)
}

fn source_duration_from_hours(hours: u64) -> (result: Duration)
    requires
        hours as nat * 3_600 <= u64::MAX as nat,
    ensures
        result@ == hours as nat * 3_600 * nanos_per_second(),
{
    Duration::from_secs(hours * 60 * 60)
}

fn source_duration_from_mins(mins: u64) -> (result: Duration)
    requires
        mins as nat * 60 <= u64::MAX as nat,
    ensures
        result@ == mins as nat * 60 * nanos_per_second(),
{
    Duration::from_secs(mins * 60)
}

fn source_duration_as_millis(duration: &Duration) -> (result: u128)
    ensures
        result as nat == duration@ / 1_000_000,
{
    duration.as_secs() as u128 * 1_000 + duration.subsec_millis() as u128
}

fn source_duration_as_micros(duration: &Duration) -> (result: u128)
    ensures
        result as nat == duration@ / 1_000,
{
    duration.as_secs() as u128 * 1_000_000 + duration.subsec_micros() as u128
}

fn source_duration_as_nanos(duration: &Duration) -> (result: u128)
    ensures
        result as nat == duration@,
{
    duration.as_secs() as u128 * 1_000_000_000 + duration.subsec_nanos() as u128
}

fn source_duration_is_zero(duration: &Duration) -> (result: bool)
    ensures
        result <==> duration@ == 0,
{
    duration.as_secs() == 0 && duration.subsec_nanos() == 0
}

fn source_duration_checked_add(
    lhs: Duration,
    rhs: Duration,
) -> (result: Option<Duration>)
    ensures
        lhs@ + rhs@ <= duration_max_nanos() ==>
            (result matches Some(value) && value@ == lhs@ + rhs@),
        lhs@ + rhs@ > duration_max_nanos() ==> result is None,
{
    let lhs_nanos = lhs.as_nanos();
    let rhs_nanos = rhs.as_nanos();
    proof {
        axiom_duration_view_valid(&lhs);
        axiom_duration_view_valid(&rhs);
    }
    let total = match lhs_nanos.checked_add(rhs_nanos) {
        Some(total) => total,
        None => return None,
    };
    let max_nanos = u64::MAX as u128 * 1_000_000_000 + 999_999_999;
    if total <= max_nanos {
        Some(source_duration_from_nanos_u128(total))
    } else {
        None
    }
}

fn source_duration_checked_sub(
    lhs: Duration,
    rhs: Duration,
) -> (result: Option<Duration>)
    ensures
        lhs@ >= rhs@ ==> (result matches Some(value) && value@ == lhs@ - rhs@),
        lhs@ < rhs@ ==> result is None,
{
    let lhs_nanos = lhs.as_nanos();
    let rhs_nanos = rhs.as_nanos();
    proof {
        axiom_duration_view_valid(&lhs);
        axiom_duration_view_valid(&rhs);
    }
    if lhs_nanos >= rhs_nanos {
        proof {
            assert((lhs_nanos - rhs_nanos) as nat <= duration_max_nanos());
        }
        Some(source_duration_from_nanos_u128(lhs_nanos - rhs_nanos))
    } else {
        None
    }
}

fn source_duration_checked_mul(
    lhs: Duration,
    rhs: u32,
) -> (result: Option<Duration>)
    ensures
        lhs@ * rhs as nat <= duration_max_nanos() ==>
            (result matches Some(value) && value@ == lhs@ * rhs as nat),
        lhs@ * rhs as nat > duration_max_nanos() ==> result is None,
{
    let lhs_nanos = lhs.as_nanos();
    proof {
        axiom_duration_view_valid(&lhs);
    }
    let total = match lhs_nanos.checked_mul(rhs as u128) {
        Some(total) => total,
        None => return None,
    };
    let max_nanos = u64::MAX as u128 * 1_000_000_000 + 999_999_999;
    if total <= max_nanos {
        Some(source_duration_from_nanos_u128(total))
    } else {
        None
    }
}

fn source_duration_checked_div(
    lhs: Duration,
    rhs: u32,
) -> (result: Option<Duration>)
    ensures
        rhs != 0 ==> (result matches Some(value) && value@ == lhs@ / rhs as nat),
        rhs == 0 ==> result is None,
{
    proof {
        axiom_duration_view_valid(&lhs);
    }
    if rhs != 0 {
        let nanos = lhs.as_nanos() / rhs as u128;
        proof {
            assert(nanos as nat <= duration_max_nanos());
        }
        Some(source_duration_from_nanos_u128(nanos))
    } else {
        None
    }
}

fn source_duration_saturating_add(lhs: Duration, rhs: Duration) -> (result: Duration)
    ensures
        result@ == if lhs@ + rhs@ <= duration_max_nanos() {
            lhs@ + rhs@
        } else {
            duration_max_nanos()
        },
{
    match source_duration_checked_add(lhs, rhs) {
        Some(result) => result,
        None => Duration::new(u64::MAX, 999_999_999),
    }
}

fn source_duration_saturating_sub(lhs: Duration, rhs: Duration) -> (result: Duration)
    ensures
        result@ == if lhs@ >= rhs@ {
            lhs@ - rhs@
        } else {
            0
        },
{
    match source_duration_checked_sub(lhs, rhs) {
        Some(result) => result,
        None => Duration::new(0, 0),
    }
}

fn source_duration_saturating_mul(
    lhs: Duration,
    rhs: u32,
) -> (result: Duration)
    ensures
        result@ == if lhs@ * rhs as nat <= duration_max_nanos() {
            lhs@ * rhs as nat
        } else {
            duration_max_nanos()
        },
{
    match source_duration_checked_mul(lhs, rhs) {
        Some(result) => result,
        None => Duration::new(u64::MAX, 999_999_999),
    }
}

fn source_duration_abs_diff(lhs: Duration, rhs: Duration) -> (result: Duration)
    ensures
        result@ == if lhs@ >= rhs@ {
            lhs@ - rhs@
        } else {
            rhs@ - lhs@
        },
{
    match source_duration_checked_sub(lhs, rhs) {
        Some(result) => result,
        None => match source_duration_checked_sub(rhs, lhs) {
            Some(result) => result,
            None => Duration::new(0, 0),
        },
    }
}

} // verus!

fn main() {}
