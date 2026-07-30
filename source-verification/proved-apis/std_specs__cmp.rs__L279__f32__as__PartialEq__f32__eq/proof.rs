#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::float::FloatBitsProperties;
use vstd::prelude::*;
use vstd::std_specs::cmp::*;

verus! {

pub assume_specification[f32::to_bits](value: f32) -> (result: u32)
    ensures
        result == value.to_bits_spec(),
;

pub open spec fn f32_ieee_eq_from_bits(lhs: f32, rhs: f32) -> bool {
    let lhs_bits = lhs.to_bits_spec();
    let rhs_bits = rhs.to_bits_spec();
    let lhs_abs = if lhs_bits >= 0x8000_0000u32 {
        (lhs_bits - 0x8000_0000u32) as u32
    } else {
        lhs_bits
    };
    let rhs_abs = if rhs_bits >= 0x8000_0000u32 {
        (rhs_bits - 0x8000_0000u32) as u32
    } else {
        rhs_bits
    };
    lhs_abs <= 0x7f80_0000u32
        && rhs_abs <= 0x7f80_0000u32
        && (lhs_bits == rhs_bits || (lhs_abs == 0u32 && rhs_abs == 0u32))
}

pub axiom fn axiom_f32_eq_ensures_ieee(lhs: f32, rhs: f32, result: bool)
    ensures
        eq_ensures::<f32>(lhs, rhs, result)
            <==> result == f32_ieee_eq_from_bits(lhs, rhs),
;

fn source_f32_partial_eq_eq(x: &f32, y: &f32) -> (result: bool)
    ensures
        eq_ensures::<f32>(*x, *y, result),
{
    let lhs_bits = x.to_bits();
    let rhs_bits = y.to_bits();
    let lhs_abs =
        if lhs_bits >= 0x8000_0000u32 { lhs_bits - 0x8000_0000u32 } else { lhs_bits };
    let rhs_abs =
        if rhs_bits >= 0x8000_0000u32 { rhs_bits - 0x8000_0000u32 } else { rhs_bits };
    let result = lhs_abs <= 0x7f80_0000u32
        && rhs_abs <= 0x7f80_0000u32
        && (lhs_bits == rhs_bits || (lhs_abs == 0u32 && rhs_abs == 0u32));

    proof {
        assert(result == f32_ieee_eq_from_bits(*x, *y));
        axiom_f32_eq_ensures_ieee(*x, *y, result);
    }
    result
}

}

fn main() {}