#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::std_specs::slice::*;

verus! {

fn source_usize_slice_index<T>(i: usize, slice: &[T]) -> (out: &T)
    requires
        i < slice@.len(),
    ensures
        *out == slice@[i as int],
{
    &(*slice)[i]
}

}

fn main() {}