#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::float::FloatBitsProperties;
use vstd::prelude::*;
use vstd::std_specs::ops::*;

verus! {

pub assume_specification[f64::to_bits](value: f64) -> (result: u64)
    ensures
        result == value.to_bits_spec(),
;

pub assume_specification[f64::from_bits](bits: u64) -> (result: f64)
    ensures
        result.to_bits_spec() == bits,
;

pub axiom fn axiom_f64_neg_ensures_ieee(value: f64, result: f64)
    ensures
        neg_ensures::<f64>(value, result)
            <==> result.to_bits_spec() == (value.to_bits_spec() ^ 0x8000_0000_0000_0000u64),
;

fn source_f64_neg(value: f64) -> (result: f64)
    ensures
        neg_ensures::<f64>(value, result),
{
    let bits = value.to_bits();
    let result = f64::from_bits(bits ^ 0x8000_0000_0000_0000u64);
    proof {
        axiom_f64_neg_ensures_ieee(value, result);
    }
    result
}

}

fn main() {}