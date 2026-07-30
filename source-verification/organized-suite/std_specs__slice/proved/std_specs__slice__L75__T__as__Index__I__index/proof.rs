#![feature(slice_index_methods)]
#![allow(dead_code)]
#![allow(unused_imports)]

use core::ops::Index;
use core::slice::SliceIndex;
use vstd::prelude::*;
use vstd::slice::SliceIndexSpec;
use vstd::std_specs::slice::*;

verus! {

fn slice_index_proof<T, I: SliceIndex<[T]>>(
    slice: &[T],
    index: I,
) -> (output: &<I as SliceIndex<[T]>>::Output)
    requires
        index.index_req(slice),
    ensures
        call_ensures(<I as SliceIndex<[T]>>::index, (index, slice), output),
{
    index.index(slice)
}

}

fn main() {}