#![allow(dead_code)]
#![allow(unused_imports)]

use core::slice::Iter;
use vstd::prelude::*;
use vstd::std_specs::iter::IteratorSpec;
use vstd::std_specs::slice::*;

verus! {

fn source_slice_ref_into_iter<'a, T>(s: &'a [T]) -> (iter: Iter<'a, T>)
    ensures
        iter == spec_slice_iter(s),
        IteratorSpec::decrease(&iter) is Some,
        IteratorSpec::initial_value_relation(&iter, &iter),
{
    s.iter()
}

}

fn main() {}