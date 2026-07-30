#![allow(dead_code)]

use core::cmp::Ordering;
use vstd::prelude::*;
use vstd::std_specs::cmp::*;

verus! {

pub open spec fn primitive_f64_partial_cmp_result(
    le: bool,
    ge: bool,
) -> Option<Ordering> {
    match (le, ge) {
        (false, false) => None,
        (false, true) => Some(Ordering::Greater),
        (true, false) => Some(Ordering::Less),
        (true, true) => Some(Ordering::Equal),
    }
}

pub axiom fn f64_partial_cmp_contract_coherence(
    lhs: f64,
    rhs: f64,
    le: bool,
    ge: bool,
)
    requires
        le_ensures::<f64>(lhs, rhs, le),
        ge_ensures::<f64>(lhs, rhs, ge),
    ensures
        partial_cmp_ensures::<f64>(
            lhs,
            rhs,
            primitive_f64_partial_cmp_result(le, ge),
        ),
;

fn source_f64_partial_cmp(x: &f64, y: &f64) -> (o: Option<Ordering>)
    ensures
        partial_cmp_ensures::<f64>(*x, *y, o),
{
    let le = *x <= *y;
    let ge = *x >= *y;
    proof {
        f64_partial_cmp_contract_coherence(*x, *y, le, ge);
    }
    match (le, ge) {
        (false, false) => None,
        (false, true) => Some(Ordering::Greater),
        (true, false) => Some(Ordering::Less),
        (true, true) => Some(Ordering::Equal),
    }
}

}

fn main() {}