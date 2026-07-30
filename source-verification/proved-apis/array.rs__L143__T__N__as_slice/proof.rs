#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::array::*;
use vstd::prelude::*;

verus! {

fn source_array_as_slice<T, const N: usize>(ar: &[T; N]) -> (out: &[T])
    ensures
        ar@ == out@,
{
    ar
}

}

fn main() {}