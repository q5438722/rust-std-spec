#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::float::FloatBitsProperties;
use vstd::prelude::*;
use vstd::std_specs::cmp::*;

verus! {

pub assume_specification[f64::to_bits](value: f64) -> (result: u64)
    ensures
        result == value.to_bits_spec(),
;

pub open spec fn f64_ieee_eq_from_bits(lhs: f64, rhs: f64) -> bool {
    let lhs_bits = lhs.to_bits_spec();
    let rhs_bits = rhs.to_bits_spec();
    let lhs_abs = if lhs_bits >= 0x8000_0000_0000_0000u64 {
        (lhs_bits - 0x8000_0000_0000_0000u64) as u64
    } else {
        lhs_bits
    };
    let rhs_abs = if rhs_bits >= 0x8000_0000_0000_0000u64 {
        (rhs_bits - 0x8000_0000_0000_0000u64) as u64
    } else {
        rhs_bits
    };
    lhs_abs <= 0x7ff0_0000_0000_0000u64
        && rhs_abs <= 0x7ff0_0000_0000_0000u64
        && (lhs_bits == rhs_bits || (lhs_abs == 0u64 && rhs_abs == 0u64))
}

pub axiom fn axiom_f64_eq_ensures_ieee(lhs: f64, rhs: f64)
    ensures
        eq_ensures::<f64>(lhs, rhs, f64_ieee_eq_from_bits(lhs, rhs)),
;

fn source_f64_partial_eq_eq(x: &f64, y: &f64) -> (result: bool)
    ensures
        eq_ensures::<f64>(*x, *y, result),
{
    let lhs_bits = x.to_bits();
    let rhs_bits = y.to_bits();
    let lhs_abs = if lhs_bits >= 0x8000_0000_0000_0000u64 {
        lhs_bits - 0x8000_0000_0000_0000u64
    } else {
        lhs_bits
    };
    let rhs_abs = if rhs_bits >= 0x8000_0000_0000_0000u64 {
        rhs_bits - 0x8000_0000_0000_0000u64
    } else {
        rhs_bits
    };
    let result = lhs_abs <= 0x7ff0_0000_0000_0000u64
        && rhs_abs <= 0x7ff0_0000_0000_0000u64
        && (lhs_bits == rhs_bits || (lhs_abs == 0u64 && rhs_abs == 0u64));

    proof {
        assert(result == f64_ieee_eq_from_bits(*x, *y));
        axiom_f64_eq_ensures_ieee(*x, *y);
    }
    result
}

}

fn main() {}