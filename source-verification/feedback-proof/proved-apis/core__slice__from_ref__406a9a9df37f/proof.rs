#![allow(dead_code)]

use vstd::prelude::*;

verus! {

pub assume_specification<T>[ core::array::from_ref::<T> ](s: &T) -> (out: &[T; 1])
    ensures
        out@ == seq![*s],
;

pub fn source_slice_from_ref<T>(s: &T) -> (r: &[T])
    ensures
        r@ == seq![*s],
{
    core::array::from_ref(s)
}

} // verus!

fn main() {}