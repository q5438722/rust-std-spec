#![allow(dead_code)]

use core::cmp::{Ordering, PartialOrd};
use vstd::prelude::*;
use vstd::std_specs::cmp::*;

verus! {

pub axiom fn f64_le_contract_coherence(
    lhs: f64,
    rhs: f64,
    comparison: Option<Ordering>,
    result: bool,
)
    requires
        partial_cmp_ensures::<f64>(lhs, rhs, comparison),
        result <==> comparison matches Some(Ordering::Less | Ordering::Equal),
    ensures
        le_ensures::<f64>(lhs, rhs, result),
;

fn source_f64_le(x: &f64, y: &f64) -> (result: bool)
    ensures
        le_ensures::<f64>(*x, *y, result),
{
    let comparison = <f64 as PartialOrd<f64>>::partial_cmp(x, y);
    let result = match comparison {
        Some(ordering) => Ordering::is_le(ordering),
        None => false,
    };
    proof {
        assert(result <==> comparison matches Some(
            Ordering::Less | Ordering::Equal
        ));
        f64_le_contract_coherence(*x, *y, comparison, result);
    }
    result
}

}

fn main() {}