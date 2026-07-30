#![feature(allocator_api)]
#![feature(slice_index_methods)]
#![allow(dead_code)]
#![allow(unused_imports)]

extern crate alloc;

use alloc::vec::Vec;
use core::alloc::Allocator;
use core::ops::Index;
use core::slice::SliceIndex;
use vstd::prelude::*;
use vstd::slice::SliceIndexSpec;
use vstd::std_specs::core::IndexSpec;
use vstd::std_specs::slice::*;
use vstd::std_specs::vec::*;

verus! {

fn source_vec_index<T, I: SliceIndex<[T]>, A: Allocator>(
    vec: &Vec<T, A>,
    index: I,
) -> (output: &<Vec<T, A> as Index<I>>::Output)
    requires
        <Vec<T, A> as IndexSpec<I>>::index_req(vec, &index),
    ensures
        exists|slice: &[T]|
            #[trigger] slice@ == vec@
                && call_ensures(<I as SliceIndex<[T]>>::index, (index, slice), output),
{
    Index::index(&**vec, index)
}

} // verus!

fn main() {}