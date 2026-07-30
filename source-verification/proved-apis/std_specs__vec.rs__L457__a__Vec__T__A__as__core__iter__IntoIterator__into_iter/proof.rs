#![feature(allocator_api)]
#![allow(dead_code)]
#![allow(unused_imports)]

extern crate alloc;

use alloc::vec::Vec;
use core::alloc::Allocator;
use vstd::prelude::*;
use vstd::std_specs::iter::IteratorSpec;
use vstd::std_specs::vec::*;

verus! {

pub axiom fn axiom_vec_iter_model_coherence<'a, T, A: Allocator>(
    vec: &'a Vec<T, A>,
    slice: &'a [T],
)
    requires
        slice@ == vec@,
    ensures
        spec_into_iter_borrowed(vec)
            == vstd::std_specs::slice::spec_slice_iter(slice),
;

fn source_vec_ref_into_iter<'a, T, A: Allocator>(
    vec: &'a Vec<T, A>,
) -> (iter: <&'a Vec<T, A> as core::iter::IntoIterator>::IntoIter)
    ensures
        iter == spec_into_iter_borrowed(vec),
        IteratorSpec::decrease(&iter) is Some,
        IteratorSpec::initial_value_relation(&iter, &iter),
{
    let slice = <Vec<T, A> as core::ops::Deref>::deref(vec);
    let iter = slice.iter();
    proof {
        axiom_vec_iter_model_coherence(vec, slice);
    }
    iter
}

}

fn main() {}