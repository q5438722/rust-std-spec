#![allow(dead_code)]

use core::cmp::{Ordering, PartialOrd};
use vstd::prelude::*;
use vstd::std_specs::cmp::*;

verus! {

pub axiom fn f32_lt_contract_coherence(
    lhs: f32,
    rhs: f32,
    comparison: Option<Ordering>,
    result: bool,
)
    requires
        partial_cmp_ensures::<f32>(lhs, rhs, comparison),
        result <==> comparison == Some(Ordering::Less),
    ensures
        lt_ensures::<f32>(lhs, rhs, result),
;

fn source_f32_lt(x: &f32, y: &f32) -> (result: bool)
    ensures
        lt_ensures::<f32>(*x, *y, result),
{
    let comparison = <f32 as PartialOrd<f32>>::partial_cmp(x, y);
    let result = match comparison {
        Some(ordering) => Ordering::is_lt(ordering),
        None => false,
    };
    proof {
        assert(result <==> comparison == Some(Ordering::Less));
        f32_lt_contract_coherence(*x, *y, comparison, result);
    }
    result
}

}

fn main() {}