#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::array::*;
use vstd::prelude::*;
use vstd::std_specs::iter::IteratorSpec;

verus! {

pub axiom fn axiom_array_iter_model_coherence<'a, T, const N: usize>(
    s: &'a [T; N],
)
    ensures
        spec_array_iter(s)
            == vstd::std_specs::slice::spec_slice_iter(spec_array_as_slice(s)),
;

fn source_array_ref_into_iter<'a, T, const N: usize>(
    s: &'a [T; N],
) -> (iter: core::slice::Iter<'a, T>)
    ensures
        iter == spec_array_iter(s),
        IteratorSpec::decrease(&iter) is Some,
        IteratorSpec::initial_value_relation(&iter, &iter),
{
    let iter = s.iter();
    proof {
        axiom_array_iter_model_coherence(s);
    }
    iter
}

}

fn main() {}