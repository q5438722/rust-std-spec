#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::std_specs::slice::*;

verus! {

fn source_slice_first<'a, T>(slice: &'a [T]) -> (res: Option<&'a T>)
    ensures
        slice.len() == 0 ==> res.is_none(),
        slice.len() != 0 ==> res.is_some() && res.unwrap() == slice[0],
{
    if slice.len() != 0 {
        Some(&slice[0])
    } else {
        None
    }
}

} // verus!

fn main() {}