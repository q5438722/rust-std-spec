#![allow(dead_code, non_snake_case, unused_imports, unused_variables)]
// Target-specific Verus implementation harness.
// Target: core::slice::iter
// Source: core/src/slice/mod.rs:1040-1042 and core/src/slice/iter.rs:69-106
// Source item sha256: ed92d2713fefdf67486ea1cb36c5c0626dd7c6496adace2c7876e62081feda37
// Dependency manifest: proof_manifests/151_core_slice_iter/dependency_assumption_manifest.json

use core::marker::PhantomData;
use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub struct Iter<'a, T: 'a> {
    pub view: Ghost<Seq<&'a T>>,
    pub _marker: PhantomData<&'a T>,
}

pub mod IteratorSpec {
    use super::*;

    pub open spec fn remaining<'a, T>(iter: &Iter<'a, T>) -> Seq<&'a T> {
        iter.view@
    }

    pub open spec fn decrease<'a, T>(iter: &Iter<'a, T>) -> Option<nat> {
        Some(0)
    }

    pub open spec fn initial_value_relation<'a, T>(
        iter: &Iter<'a, T>,
        init: &Iter<'a, T>,
    ) -> bool {
        remaining(iter) == remaining(init)
    }
}

pub closed spec fn spec_slice_iter<'a, T>(slice: &'a [T]) -> Iter<'a, T> {
    Iter { view: Ghost(slice@.as_ref()), _marker: PhantomData }
}

impl<'a, T> Iter<'a, T> {
    pub fn new(slice: &'a [T]) -> (ret: Self)
        ensures
            ret == spec_slice_iter(slice),
            IteratorSpec::remaining(&ret) == slice@.as_ref(),
            IteratorSpec::decrease(&ret) is Some,
            IteratorSpec::initial_value_relation(&ret, &ret),
    {
        let ret = Iter { view: Ghost(slice@.as_ref()), _marker: PhantomData };
        proof {
            reveal(spec_slice_iter);
        }
        ret
    }
}

pub fn iter<'a, T>(slice: &'a [T]) -> (iter: Iter<'a, T>)
    ensures
        iter == spec_slice_iter(slice),
        IteratorSpec::remaining(&iter) == slice@.as_ref(),
        IteratorSpec::decrease(&iter) is Some,
        IteratorSpec::initial_value_relation(&iter, &iter),
{
    Iter::new(slice)
}

}
