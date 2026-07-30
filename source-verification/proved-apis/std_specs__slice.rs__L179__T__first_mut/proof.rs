#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::std_specs::slice::*;

verus! {

fn source_slice_first_mut<'a, T>(slice: &'a mut [T]) -> (res: Option<&'a mut T>)
    ensures
        old(slice).len() == 0 ==> res.is_none() && final(slice)@ == seq![],
        old(slice).len() != 0 ==> res.is_some() && *res.unwrap() == old(slice)[0]
            && final(slice)@ == old(slice)@.update(0, *final(res.unwrap())),
{
    if slice.len() != 0 {
        Some(&mut slice[0])
    } else {
        None
    }
}

} // verus!

fn main() {}