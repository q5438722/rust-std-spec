#![allow(dead_code)]
#![feature(core_intrinsics)]
#![feature(repr_simd)]

use vstd::prelude::*;
use vstd::std_specs::ops::*;

verus! {

#[repr(simd)]
#[derive(Clone, Copy)]
pub struct F64x1(pub [f64; 1]);

pub uninterp spec fn simd_div_ensures<A>(lhs: A, rhs: A, result: A) -> bool;

pub assume_specification<T>[core::intrinsics::simd::simd_div](
    lhs: T,
    rhs: T,
) -> (result: T)
    ensures
        simd_div_ensures(lhs, rhs, result),
;

pub axiom fn axiom_scalar_simd_div_is_f64_div(
    x: f64,
    y: f64,
    quotient: F64x1,
)
    requires
        simd_div_ensures(F64x1([x]), F64x1([y]), quotient),
    ensures
        div_ensures::<f64>(x, y, quotient.0[0]),
;

pub fn source_f64_div(x: f64, y: f64) -> (result: f64)
    ensures
        div_ensures::<f64>(x, y, result),
{
    let lhs = F64x1([x]);
    let rhs = F64x1([y]);
    let quotient = unsafe { core::intrinsics::simd::simd_div(lhs, rhs) };
    proof {
        axiom_scalar_simd_div_is_f64_div(x, y, quotient);
    }
    quotient.0[0]
}

} // verus!

fn main() {}