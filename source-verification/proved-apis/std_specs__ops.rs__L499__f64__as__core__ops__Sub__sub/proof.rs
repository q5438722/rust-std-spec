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

pub axiom fn axiom_f64_add_has_no_precondition(x: f64, y: f64)
    ensures
        x.add_req(y),
;

pub axiom fn axiom_f64_sub_is_add_negated_rhs(
    x: f64,
    y: f64,
    neg_y: f64,
    result: f64,
)
    requires
        neg_y.to_bits_spec() == (y.to_bits_spec() ^ 0x8000_0000_0000_0000u64),
        add_ensures::<f64>(x, neg_y, result),
    ensures
        sub_ensures::<f64>(x, y, result),
;

pub fn source_f64_sub(x: f64, y: f64) -> (o: f64)
    ensures
        sub_ensures::<f64>(x, y, o),
{
    let bits = y.to_bits();
    let neg_y = f64::from_bits(bits ^ 0x8000_0000_0000_0000u64);
    proof {
        axiom_f64_add_has_no_precondition(x, neg_y);
    }
    let result = <f64 as core::ops::Add>::add(x, neg_y);
    proof {
        axiom_f64_sub_is_add_negated_rhs(x, y, neg_y, result);
    }
    result
}

} // verus!

fn main() {}