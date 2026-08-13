#![allow(dead_code, unused_imports, unused_variables)]
// Target-specific Verus implementation harness.
// Target: core::slice::contains
// Source: core/src/slice/mod.rs:2589-2594 and SliceContains impls at core/src/slice/cmp.rs:398-455
// Source item sha256: bdc2cbb4b13659e4a71267712a450a6458600c16646498ab7296e7fdacaca324
// Dependency manifest: proof_manifests/038_core_slice_contains/dependency_assumption_manifest.json

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub uninterp spec fn partial_eq_observed<T: core::cmp::PartialEq>(left: T, right: T) -> bool;

pub open spec fn slice_contains_value<T: core::cmp::PartialEq>(seq: Seq<T>, value: T) -> bool {
    exists|i: int| 0 <= i < seq.len() && partial_eq_observed(seq[i], value)
}

pub mod cmp {
    use vstd::prelude::*;
    use super::slice_contains_value;

    pub trait SliceContains: core::cmp::PartialEq + Sized {
        fn slice_contains(&self, x: &[Self]) -> (b: bool)
            ensures
                b <==> slice_contains_value(x@, *self);
    }

    impl<T: core::cmp::PartialEq> SliceContains for T {
        #[verifier::external_body]
        fn slice_contains(&self, x: &[T]) -> (b: bool)
            ensures
                b <==> slice_contains_value(x@, *self),
        {
            false
        }
    }
}

pub fn contains<T: core::cmp::PartialEq>(slice: &[T], x: &T) -> (b: bool)
    ensures
        b <==> slice_contains_value(slice@, *x),
{
    cmp::SliceContains::slice_contains(x, slice)
}

}
