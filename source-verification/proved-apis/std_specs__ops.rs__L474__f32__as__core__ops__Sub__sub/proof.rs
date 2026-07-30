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

pub axiom fn axiom_f32_add_has_no_precondition(x: f32, y: f32)
    ensures
        x.add_req(y),
;

pub axiom fn axiom_f32_sub_is_add_negated_rhs(
    x: f32,
    y: f32,
    neg_y: f32,
    result: f32,
)
    requires
        neg_y.to_bits_spec() == (y.to_bits_spec() ^ 0x8000_0000u32),
        add_ensures::<f32>(x, neg_y, result),
    ensures
        sub_ensures::<f32>(x, y, result),
;

pub fn source_f32_sub(x: f32, y: f32) -> (o: f32)
    ensures
        sub_ensures::<f32>(x, y, o),
{
    let bits = y.to_bits();
    let neg_y = f32::from_bits(bits ^ 0x8000_0000u32);
    proof {
        axiom_f32_add_has_no_precondition(x, neg_y);
    }
    let result = <f32 as core::ops::Add>::add(x, neg_y);
    proof {
        axiom_f32_sub_is_add_negated_rhs(x, y, neg_y, result);
    }
    result
}

} // verus!

fn main() {}