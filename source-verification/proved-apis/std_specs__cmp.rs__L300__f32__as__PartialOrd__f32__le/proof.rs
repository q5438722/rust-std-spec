#![allow(dead_code)]

use core::cmp::{Ordering, PartialOrd};
use vstd::prelude::*;
use vstd::std_specs::cmp::*;

verus! {

pub axiom fn f32_le_contract_coherence(
    lhs: f32,
    rhs: f32,
    comparison: Option<Ordering>,
    result: bool,
)
    requires
        partial_cmp_ensures::<f32>(lhs, rhs, comparison),
        result <==> comparison matches Some(Ordering::Less | Ordering::Equal),
    ensures
        le_ensures::<f32>(lhs, rhs, result),
;

fn source_f32_le(x: &f32, y: &f32) -> (result: bool)
    ensures
        le_ensures::<f32>(*x, *y, result),
{
    let comparison = <f32 as PartialOrd<f32>>::partial_cmp(x, y);
    let result = match comparison {
        Some(ordering) => Ordering::is_le(ordering),
        None => false,
    };
    proof {
        assert(result <==> comparison matches Some(
            Ordering::Less | Ordering::Equal
        ));
        f32_le_contract_coherence(*x, *y, comparison, result);
    }
    result
}

}

fn main() {}