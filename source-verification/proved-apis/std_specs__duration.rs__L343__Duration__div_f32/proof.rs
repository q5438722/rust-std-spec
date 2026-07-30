#![allow(dead_code)]

use core::time::Duration;
use vstd::float::{float_cast_spec, ieee_float_cast, FloatBitsProperties};
use vstd::prelude::*;
use vstd::std_specs::duration::{
    duration_as_secs_f32, duration_as_secs_f64, duration_float_ieee_semantics,
    duration_from_secs_f32_nanos, duration_from_secs_f64_nanos, duration_secs_f32_valid,
    duration_secs_f64_valid,
};
use vstd::std_specs::ops::{
    add_ensures, div_ensures, mul_ensures, AddSpec, DivSpec, MulSpec,
};
use vstd::std_specs::cmp::lt_ensures;

verus! {

pub open spec fn rust_ieee_754_target() -> bool {
    duration_float_ieee_semantics()
}

pub assume_specification[ f32::to_bits ](value: f32) -> (result: u32)
    ensures
        result == value.to_bits_spec(),
;

pub assume_specification[ f64::to_bits ](value: f64) -> (result: u64)
    ensures
        result == value.to_bits_spec(),
;

pub axiom fn rfc_f32_lt(lhs: f32, rhs: f32, result: bool)
    requires
        rust_ieee_754_target(),
        lt_ensures(lhs, rhs, result),
    ensures
        result == (lhs < rhs),
;

pub axiom fn rfc_f64_lt(lhs: f64, rhs: f64, result: bool)
    requires
        rust_ieee_754_target(),
        lt_ensures(lhs, rhs, result),
    ensures
        result == (lhs < rhs),
;

pub axiom fn rfc_u64_as_f64(value: u64, result: f64)
    requires
        rust_ieee_754_target(),
        float_cast_spec(value, result),
    ensures
        result == ieee_float_cast::<u64, f64>(value),
;

pub axiom fn rfc_u32_as_f64(value: u32, result: f64)
    requires
        rust_ieee_754_target(),
        float_cast_spec(value, result),
    ensures
        result == ieee_float_cast::<u32, f64>(value),
;

pub axiom fn rfc_u64_as_f32(value: u64, result: f32)
    requires
        rust_ieee_754_target(),
        float_cast_spec(value, result),
    ensures
        result == ieee_float_cast::<u64, f32>(value),
;

pub axiom fn rfc_u32_as_f32(value: u32, result: f32)
    requires
        rust_ieee_754_target(),
        float_cast_spec(value, result),
    ensures
        result == ieee_float_cast::<u32, f32>(value),
;

pub axiom fn rfc_f64_add_req(lhs: f64, rhs: f64)
    requires
        rust_ieee_754_target(),
    ensures
        lhs.add_req(rhs),
;

pub axiom fn rfc_f64_div_req(lhs: f64, rhs: f64)
    requires
        rust_ieee_754_target(),
    ensures
        lhs.div_req(rhs),
;

pub axiom fn rfc_f64_mul_req(lhs: f64, rhs: f64)
    requires
        rust_ieee_754_target(),
    ensures
        lhs.mul_req(rhs),
;

pub axiom fn rfc_f32_add_req(lhs: f32, rhs: f32)
    requires
        rust_ieee_754_target(),
    ensures
        lhs.add_req(rhs),
;

pub axiom fn rfc_f32_div_req(lhs: f32, rhs: f32)
    requires
        rust_ieee_754_target(),
    ensures
        lhs.div_req(rhs),
;

pub axiom fn rfc_f32_mul_req(lhs: f32, rhs: f32)
    requires
        rust_ieee_754_target(),
    ensures
        lhs.mul_req(rhs),
;

pub axiom fn rfc_f64_add(lhs: f64, rhs: f64, result: f64)
    requires
        rust_ieee_754_target(),
        add_ensures(lhs, rhs, result),
        !(lhs + rhs).is_nan_spec(),
    ensures
        result == lhs + rhs,
;

pub axiom fn rfc_f64_div(lhs: f64, rhs: f64, result: f64)
    requires
        rust_ieee_754_target(),
        div_ensures(lhs, rhs, result),
        !(lhs / rhs).is_nan_spec(),
    ensures
        result == lhs / rhs,
;

pub axiom fn rfc_f64_div_nan(lhs: f64, rhs: f64, result: f64)
    requires
        rust_ieee_754_target(),
        div_ensures(lhs, rhs, result),
        (lhs / rhs).is_nan_spec(),
    ensures
        result.is_nan_spec(),
;

pub axiom fn rfc_f64_mul(lhs: f64, rhs: f64, result: f64)
    requires
        rust_ieee_754_target(),
        mul_ensures(lhs, rhs, result),
        !(lhs * rhs).is_nan_spec(),
    ensures
        result == lhs * rhs,
;

pub axiom fn rfc_f32_add(lhs: f32, rhs: f32, result: f32)
    requires
        rust_ieee_754_target(),
        add_ensures(lhs, rhs, result),
        !(lhs + rhs).is_nan_spec(),
    ensures
        result == lhs + rhs,
;

pub axiom fn rfc_f32_div(lhs: f32, rhs: f32, result: f32)
    requires
        rust_ieee_754_target(),
        div_ensures(lhs, rhs, result),
        !(lhs / rhs).is_nan_spec(),
    ensures
        result == lhs / rhs,
;

pub axiom fn rfc_f32_div_nan(lhs: f32, rhs: f32, result: f32)
    requires
        rust_ieee_754_target(),
        div_ensures(lhs, rhs, result),
        (lhs / rhs).is_nan_spec(),
    ensures
        result.is_nan_spec(),
;

pub axiom fn rfc_f32_mul(lhs: f32, rhs: f32, result: f32)
    requires
        rust_ieee_754_target(),
        mul_ensures(lhs, rhs, result),
        !(lhs * rhs).is_nan_spec(),
    ensures
        result == lhs * rhs,
;

pub axiom fn duration_fraction_f64_not_nan(nanos: u32)
    ensures
        !(ieee_float_cast::<u32, f64>(nanos)
            / ieee_float_cast::<u32, f64>(1_000_000_000u32)).is_nan_spec(),
;

pub axiom fn duration_total_f64_not_nan(secs: u64, nanos: u32)
    ensures
        !(ieee_float_cast::<u64, f64>(secs)
            + ieee_float_cast::<u32, f64>(nanos)
                / ieee_float_cast::<u32, f64>(1_000_000_000u32)).is_nan_spec(),
;

pub axiom fn duration_fraction_f32_not_nan(nanos: u32)
    ensures
        !(ieee_float_cast::<u32, f32>(nanos)
            / ieee_float_cast::<u32, f32>(1_000_000_000u32)).is_nan_spec(),
;

pub axiom fn duration_total_f32_not_nan(secs: u64, nanos: u32)
    ensures
        !(ieee_float_cast::<u64, f32>(secs)
            + ieee_float_cast::<u32, f32>(nanos)
                / ieee_float_cast::<u32, f32>(1_000_000_000u32)).is_nan_spec(),
;

pub axiom fn duration_nanos_product_f64_not_nan(secs: u64)
    ensures
        !(ieee_float_cast::<u64, f64>(secs)
            * ieee_float_cast::<u32, f64>(1_000_000_000u32)).is_nan_spec(),
;

pub axiom fn duration_nanos_total_f64_not_nan(secs: u64, nanos: u32)
    ensures
        !(ieee_float_cast::<u64, f64>(secs)
                * ieee_float_cast::<u32, f64>(1_000_000_000u32)
            + ieee_float_cast::<u32, f64>(nanos)).is_nan_spec(),
;

pub axiom fn duration_nanos_product_f32_not_nan(secs: u64)
    ensures
        !(ieee_float_cast::<u64, f32>(secs)
            * ieee_float_cast::<u32, f32>(1_000_000_000u32)).is_nan_spec(),
;

pub axiom fn duration_nanos_total_f32_not_nan(secs: u64, nanos: u32)
    ensures
        !(ieee_float_cast::<u64, f32>(secs)
                * ieee_float_cast::<u32, f32>(1_000_000_000u32)
            + ieee_float_cast::<u32, f32>(nanos)).is_nan_spec(),
;

pub axiom fn duration_ratio_f64_nan(lhs: nat, rhs: nat)
    requires
        lhs == 0,
        rhs == 0,
    ensures
        (vstd::std_specs::duration::duration_as_nanos_f64(lhs)
            / vstd::std_specs::duration::duration_as_nanos_f64(rhs)).is_nan_spec(),
;

pub axiom fn duration_ratio_f64_not_nan(lhs: nat, rhs: nat)
    requires
        !(lhs == 0 && rhs == 0),
    ensures
        !(vstd::std_specs::duration::duration_as_nanos_f64(lhs)
            / vstd::std_specs::duration::duration_as_nanos_f64(rhs)).is_nan_spec(),
;

pub axiom fn duration_ratio_f32_nan(lhs: nat, rhs: nat)
    requires
        lhs == 0,
        rhs == 0,
    ensures
        (vstd::std_specs::duration::duration_as_nanos_f32(lhs)
            / vstd::std_specs::duration::duration_as_nanos_f32(rhs)).is_nan_spec(),
;

pub axiom fn duration_ratio_f32_not_nan(lhs: nat, rhs: nat)
    requires
        !(lhs == 0 && rhs == 0),
    ensures
        !(vstd::std_specs::duration::duration_as_nanos_f32(lhs)
            / vstd::std_specs::duration::duration_as_nanos_f32(rhs)).is_nan_spec(),
;

fn source_duration_as_secs_f64(duration: &Duration) -> (result: f64)
    requires
        rust_ieee_754_target(),
    ensures
        result == duration_as_secs_f64(duration@),
{
    let secs = duration.as_secs();
    let nanos = duration.subsec_nanos();
    let secs_float = secs as f64;
    let nanos_float = nanos as f64;
    let billion_float = 1_000_000_000u32 as f64;
    proof {
        rfc_u64_as_f64(secs, secs_float);
        rfc_u32_as_f64(nanos, nanos_float);
        rfc_u32_as_f64(1_000_000_000u32, billion_float);
        duration_fraction_f64_not_nan(nanos);
        rfc_f64_div_req(nanos_float, billion_float);
    }
    let fraction = nanos_float / billion_float;
    proof {
        assert(!(nanos_float / billion_float).is_nan_spec());
        rfc_f64_div(nanos_float, billion_float, fraction);
        duration_total_f64_not_nan(secs, nanos);
        rfc_f64_add_req(secs_float, fraction);
    }
    let result = secs_float + fraction;
    proof {
        assert(!(secs_float + fraction).is_nan_spec());
        rfc_f64_add(secs_float, fraction, result);
    }
    result
}

fn source_duration_as_secs_f32(duration: &Duration) -> (result: f32)
    requires
        rust_ieee_754_target(),
    ensures
        result == duration_as_secs_f32(duration@),
{
    let secs = duration.as_secs();
    let nanos = duration.subsec_nanos();
    let secs_float = secs as f32;
    let nanos_float = nanos as f32;
    let billion_float = 1_000_000_000u32 as f32;
    proof {
        rfc_u64_as_f32(secs, secs_float);
        rfc_u32_as_f32(nanos, nanos_float);
        rfc_u32_as_f32(1_000_000_000u32, billion_float);
        duration_fraction_f32_not_nan(nanos);
        rfc_f32_div_req(nanos_float, billion_float);
    }
    let fraction = nanos_float / billion_float;
    proof {
        assert(!(nanos_float / billion_float).is_nan_spec());
        rfc_f32_div(nanos_float, billion_float, fraction);
        duration_total_f32_not_nan(secs, nanos);
        rfc_f32_add_req(secs_float, fraction);
    }
    let result = secs_float + fraction;
    proof {
        assert(!(secs_float + fraction).is_nan_spec());
        rfc_f32_add(secs_float, fraction, result);
    }
    result
}

fn source_duration_mul_f64(duration: Duration, rhs: f64) -> (result: Duration)
    requires
        rust_ieee_754_target(),
        duration_secs_f64_valid(rhs * duration_as_secs_f64(duration@)),
    ensures
        result@ == duration_from_secs_f64_nanos(rhs * duration_as_secs_f64(duration@)),
{
    let secs = source_duration_as_secs_f64(&duration);
    proof {
        rfc_f64_mul_req(rhs, secs);
    }
    let product = rhs * secs;
    proof {
        assert(!(rhs * duration_as_secs_f64(duration@)).is_nan_spec());
        rfc_f64_mul(rhs, secs, product);
        assert(duration_secs_f64_valid(product));
    }
    Duration::from_secs_f64(product)
}

fn source_duration_mul_f32(duration: Duration, rhs: f32) -> (result: Duration)
    requires
        rust_ieee_754_target(),
        duration_secs_f32_valid(rhs * duration_as_secs_f32(duration@)),
    ensures
        result@ == duration_from_secs_f32_nanos(rhs * duration_as_secs_f32(duration@)),
{
    let secs = source_duration_as_secs_f32(&duration);
    proof {
        rfc_f32_mul_req(rhs, secs);
    }
    let product = rhs * secs;
    proof {
        assert(!(rhs * duration_as_secs_f32(duration@)).is_nan_spec());
        rfc_f32_mul(rhs, secs, product);
        assert(duration_secs_f32_valid(product));
    }
    Duration::from_secs_f32(product)
}

fn source_duration_div_f64(duration: Duration, rhs: f64) -> (result: Duration)
    requires
        rust_ieee_754_target(),
        duration_secs_f64_valid(duration_as_secs_f64(duration@) / rhs),
    ensures
        result@ == duration_from_secs_f64_nanos(duration_as_secs_f64(duration@) / rhs),
{
    let secs = source_duration_as_secs_f64(&duration);
    proof {
        rfc_f64_div_req(secs, rhs);
    }
    let quotient = secs / rhs;
    proof {
        assert(!(duration_as_secs_f64(duration@) / rhs).is_nan_spec());
        rfc_f64_div(secs, rhs, quotient);
        assert(duration_secs_f64_valid(quotient));
    }
    Duration::from_secs_f64(quotient)
}

fn source_duration_div_f32(duration: Duration, rhs: f32) -> (result: Duration)
    requires
        rust_ieee_754_target(),
        duration_secs_f32_valid(duration_as_secs_f32(duration@) / rhs),
    ensures
        result@ == duration_from_secs_f32_nanos(duration_as_secs_f32(duration@) / rhs),
{
    let secs = source_duration_as_secs_f32(&duration);
    proof {
        rfc_f32_div_req(secs, rhs);
    }
    let quotient = secs / rhs;
    proof {
        assert(!(duration_as_secs_f32(duration@) / rhs).is_nan_spec());
        rfc_f32_div(secs, rhs, quotient);
        assert(duration_secs_f32_valid(quotient));
    }
    Duration::from_secs_f32(quotient)
}

fn source_duration_as_nanos_f64(duration: &Duration) -> (result: f64)
    requires
        rust_ieee_754_target(),
    ensures
        result == vstd::std_specs::duration::duration_as_nanos_f64(duration@),
{
    let secs = duration.as_secs();
    let nanos = duration.subsec_nanos();
    let secs_float = secs as f64;
    let nanos_float = nanos as f64;
    let billion_float = 1_000_000_000u32 as f64;
    proof {
        rfc_u64_as_f64(secs, secs_float);
        rfc_u32_as_f64(nanos, nanos_float);
        rfc_u32_as_f64(1_000_000_000u32, billion_float);
        duration_nanos_product_f64_not_nan(secs);
        rfc_f64_mul_req(secs_float, billion_float);
    }
    let whole = secs_float * billion_float;
    proof {
        rfc_f64_mul(secs_float, billion_float, whole);
        duration_nanos_total_f64_not_nan(secs, nanos);
        rfc_f64_add_req(whole, nanos_float);
    }
    let result = whole + nanos_float;
    proof {
        rfc_f64_add(whole, nanos_float, result);
    }
    result
}

fn source_duration_as_nanos_f32(duration: &Duration) -> (result: f32)
    requires
        rust_ieee_754_target(),
    ensures
        result == vstd::std_specs::duration::duration_as_nanos_f32(duration@),
{
    let secs = duration.as_secs();
    let nanos = duration.subsec_nanos();
    let secs_float = secs as f32;
    let nanos_float = nanos as f32;
    let billion_float = 1_000_000_000u32 as f32;
    proof {
        rfc_u64_as_f32(secs, secs_float);
        rfc_u32_as_f32(nanos, nanos_float);
        rfc_u32_as_f32(1_000_000_000u32, billion_float);
        duration_nanos_product_f32_not_nan(secs);
        rfc_f32_mul_req(secs_float, billion_float);
    }
    let whole = secs_float * billion_float;
    proof {
        rfc_f32_mul(secs_float, billion_float, whole);
        duration_nanos_total_f32_not_nan(secs, nanos);
        rfc_f32_add_req(whole, nanos_float);
    }
    let result = whole + nanos_float;
    proof {
        rfc_f32_add(whole, nanos_float, result);
    }
    result
}

fn source_duration_div_duration_f64(
    lhs: Duration,
    rhs: Duration,
) -> (result: f64)
    requires
        rust_ieee_754_target(),
    ensures
        lhs@ == 0 && rhs@ == 0 ==> result.is_nan_spec(),
        !(lhs@ == 0 && rhs@ == 0) ==> result
            == vstd::std_specs::duration::duration_as_nanos_f64(lhs@)
                / vstd::std_specs::duration::duration_as_nanos_f64(rhs@),
{
    let lhs_nanos = source_duration_as_nanos_f64(&lhs);
    let rhs_nanos = source_duration_as_nanos_f64(&rhs);
    proof {
        rfc_f64_div_req(lhs_nanos, rhs_nanos);
    }
    let result = lhs_nanos / rhs_nanos;
    proof {
        if lhs@ == 0 && rhs@ == 0 {
            duration_ratio_f64_nan(lhs@, rhs@);
            rfc_f64_div_nan(lhs_nanos, rhs_nanos, result);
        } else {
            duration_ratio_f64_not_nan(lhs@, rhs@);
            rfc_f64_div(lhs_nanos, rhs_nanos, result);
        }
    }
    result
}

fn source_duration_div_duration_f32(
    lhs: Duration,
    rhs: Duration,
) -> (result: f32)
    requires
        rust_ieee_754_target(),
    ensures
        lhs@ == 0 && rhs@ == 0 ==> result.is_nan_spec(),
        !(lhs@ == 0 && rhs@ == 0) ==> result
            == vstd::std_specs::duration::duration_as_nanos_f32(lhs@)
                / vstd::std_specs::duration::duration_as_nanos_f32(rhs@),
{
    let lhs_nanos = source_duration_as_nanos_f32(&lhs);
    let rhs_nanos = source_duration_as_nanos_f32(&rhs);
    proof {
        rfc_f32_div_req(lhs_nanos, rhs_nanos);
    }
    let result = lhs_nanos / rhs_nanos;
    proof {
        if lhs@ == 0 && rhs@ == 0 {
            duration_ratio_f32_nan(lhs@, rhs@);
            rfc_f32_div_nan(lhs_nanos, rhs_nanos, result);
        } else {
            duration_ratio_f32_not_nan(lhs@, rhs@);
            rfc_f32_div(lhs_nanos, rhs_nanos, result);
        }
    }
    result
}

} // verus!

fn main() {}
