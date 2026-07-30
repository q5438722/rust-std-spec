#![allow(dead_code)]

use core::cmp::Ordering;
use vstd::prelude::*;
use vstd::std_specs::cmp::*;

verus! {

pub open spec fn primitive_f32_partial_cmp_result(
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

pub axiom fn f32_partial_cmp_contract_coherence(
    lhs: f32,
    rhs: f32,
    le: bool,
    ge: bool,
)
    requires
        le_ensures::<f32>(lhs, rhs, le),
        ge_ensures::<f32>(lhs, rhs, ge),
    ensures
        partial_cmp_ensures::<f32>(
            lhs,
            rhs,
            primitive_f32_partial_cmp_result(le, ge),
        ),
;

fn source_f32_partial_cmp(x: &f32, y: &f32) -> (o: Option<Ordering>)
    ensures
        partial_cmp_ensures::<f32>(*x, *y, o),
{
    let le = *x <= *y;
    let ge = *x >= *y;
    proof {
        f32_partial_cmp_contract_coherence(*x, *y, le, ge);
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