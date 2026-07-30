#![allow(dead_code)]

use core::cmp::{Ordering, PartialOrd};
use vstd::prelude::*;
use vstd::std_specs::cmp::*;

verus! {

pub axiom fn f32_ge_contract_coherence(
    lhs: f32,
    rhs: f32,
    comparison: Option<Ordering>,
    result: bool,
)
    requires
        partial_cmp_ensures::<f32>(lhs, rhs, comparison),
        result <==> comparison matches Some(Ordering::Greater | Ordering::Equal),
    ensures
        ge_ensures::<f32>(lhs, rhs, result),
;

fn source_f32_ge(x: &f32, y: &f32) -> (result: bool)
    ensures
        ge_ensures::<f32>(*x, *y, result),
{
    let comparison = <f32 as PartialOrd<f32>>::partial_cmp(x, y);
    let result = match comparison {
        Some(ordering) => Ordering::is_ge(ordering),
        None => false,
    };
    proof {
        assert(result <==> comparison matches Some(
            Ordering::Greater | Ordering::Equal
        ));
        f32_ge_contract_coherence(*x, *y, comparison, result);
    }
    result
}

}

fn main() {}