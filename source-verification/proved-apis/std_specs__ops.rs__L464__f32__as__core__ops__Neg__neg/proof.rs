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

pub axiom fn axiom_f32_neg_ensures_ieee(value: f32, result: f32)
    ensures
        neg_ensures::<f32>(value, result)
            <==> result.to_bits_spec() == (value.to_bits_spec() ^ 0x8000_0000u32),
;

fn source_f32_neg(value: f32) -> (result: f32)
    ensures
        neg_ensures::<f32>(value, result),
{
    let bits = value.to_bits();
    let result = f32::from_bits(bits ^ 0x8000_0000u32);
    proof {
        axiom_f32_neg_ensures_ieee(value, result);
    }
    result
}

}

fn main() {}