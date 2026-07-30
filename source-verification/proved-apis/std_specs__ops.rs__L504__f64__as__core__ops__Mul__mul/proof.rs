#![allow(dead_code)]
#![feature(core_intrinsics)]
#![feature(repr_simd)]

use vstd::prelude::*;
use vstd::std_specs::ops::*;

verus! {

#[repr(simd)]
#[derive(Clone, Copy)]
pub struct F64x1(pub [f64; 1]);

pub uninterp spec fn simd_mul_ensures<A>(lhs: A, rhs: A, result: A) -> bool;

pub assume_specification<T>[core::intrinsics::simd::simd_mul](
    lhs: T,
    rhs: T,
) -> (result: T)
    ensures
        simd_mul_ensures(lhs, rhs, result),
;

pub axiom fn axiom_scalar_simd_mul_is_f64_mul(
    x: f64,
    y: f64,
    product: F64x1,
)
    requires
        simd_mul_ensures(F64x1([x]), F64x1([y]), product),
    ensures
        mul_ensures::<f64>(x, y, product.0[0]),
;

pub fn source_f64_mul(x: f64, y: f64) -> (result: f64)
    ensures
        mul_ensures::<f64>(x, y, result),
{
    let lhs = F64x1([x]);
    let rhs = F64x1([y]);
    let product = unsafe { core::intrinsics::simd::simd_mul(lhs, rhs) };
    proof {
        axiom_scalar_simd_mul_is_f64_mul(x, y, product);
    }
    product.0[0]
}

} // verus!

fn main() {}