#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::float::FloatBitsProperties;
use vstd::prelude::*;
use vstd::std_specs::ops::*;

verus! {

pub assume_specification[f32::to_bits](value: f32) -> (result: u32)
    ensures
        result == value.to_bits_spec(),
;

pub assume_specification[f32::from_bits](bits: u32) -> (result: f32)
    ensures
        result.to_bits_spec() == bits,
;

pub uninterp spec fn f32_mul_add_ensures(
    x: f32,
    y: f32,
    addend: f32,
    result: f32,
) -> bool;

pub assume_specification[f32::mul_add](
    x: f32,
    y: f32,
    addend: f32,
) -> (result: f32)
    ensures
        f32_mul_add_ensures(x, y, addend, result),
;

pub axiom fn axiom_f32_mul_add_signed_zero_is_mul(
    x: f32,
    y: f32,
    signed_zero: f32,
    result: f32,
)
    requires
        signed_zero.to_bits_spec()
            == ((x.to_bits_spec() ^ y.to_bits_spec()) & 0x8000_0000u32),
        f32_mul_add_ensures(x, y, signed_zero, result),
    ensures
        mul_ensures::<f32>(x, y, result),
;

pub fn source_f32_mul(x: f32, y: f32) -> (result: f32)
    ensures
        mul_ensures::<f32>(x, y, result),
{
    let sign = (x.to_bits() ^ y.to_bits()) & 0x8000_0000u32;
    let signed_zero = f32::from_bits(sign);
    let result = x.mul_add(y, signed_zero);
    proof {
        axiom_f32_mul_add_signed_zero_is_mul(x, y, signed_zero, result);
    }
    result
}

} // verus!

fn main() {}