#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::std_specs::slice::*;

verus! {

fn source_slice_last_mut<'a, T>(slice: &'a mut [T]) -> (res: Option<&'a mut T>)
    ensures
        old(slice).len() == 0 ==> res.is_none() && final(slice)@ == seq![],
        old(slice).len() != 0 ==> res.is_some() && *res.unwrap() == old(slice)@.last()
            && final(slice)@ == old(slice)@.update(
                old(slice).len() - 1,
                *final(res.unwrap()),
            ),
{
    if slice.len() != 0 {
        let last = slice.len() - 1;
        Some(&mut slice[last])
    } else {
        None
    }
}

} // verus!

fn main() {}