#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::array::*;
use vstd::prelude::*;

verus! {

fn array_as_slice_proof<T, const N: usize>(ar: &[T; N]) -> (out: &[T])
    ensures
        ar@ == out@,
{
    ar
}

}

fn main() {}