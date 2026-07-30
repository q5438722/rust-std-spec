#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::slice::*;

verus! {

fn slice_is_empty_proof<T>(slice: &[T]) -> (b: bool)
    ensures
        b <==> slice@.len() == 0,
{
    slice.len() == 0
}

}

fn main() {}