#![allow(dead_code)]
#![allow(unused_imports)]

use core::ops::Index;
use vstd::prelude::*;
use vstd::std_specs::core::IndexSpec;
use vstd::std_specs::slice::*;

verus! {

fn array_index_proof<T, I, const N: usize>(
    array: &[T; N],
    index: I,
) -> (output: &<[T; N] as Index<I>>::Output)
where
    [T]: Index<I>,
    requires
        <[T; N] as IndexSpec<I>>::index_req(array, &index),
    ensures
        call_ensures(<[T] as Index<I>>::index, (array, index), output),
{
    let slice: &[T] = array;
    Index::index(slice, index)
}

} // verus!

fn main() {}