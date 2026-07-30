#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::slice::*;

verus! {

fn source_slice_is_empty<T>(slice: &[T]) -> (b: bool)
    ensures
        b <==> slice@.len() == 0,
{
    slice.len() == 0
}

}

fn main() {}