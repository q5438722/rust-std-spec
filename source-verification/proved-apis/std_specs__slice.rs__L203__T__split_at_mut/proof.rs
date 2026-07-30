#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::std_specs::slice::*;

verus! {

pub assume_specification<T>[ <[T]>::split_at_mut_checked ](
    slice: &mut [T],
    mid: usize,
) -> (ret: Option<(&mut [T], &mut [T])>)
    ensures
        ret.is_some() <==> mid <= old(slice)@.len(),
        ret.is_some() ==> ret.unwrap().0@ == old(slice)@.subrange(0, mid as int),
        ret.is_some() ==> ret.unwrap().1@ == old(slice)@.subrange(
            mid as int,
            old(slice)@.len() as int,
        ),
        ret.is_some() ==> final(slice)@ == final(ret.unwrap().0)@
            + final(ret.unwrap().1)@,
        ret.is_none() ==> final(slice)@ == old(slice)@,
;

fn source_slice_split_at_mut<T>(
    slice: &mut [T],
    mid: usize,
) -> (ret: (&mut [T], &mut [T]))
    requires
        0 <= mid <= slice.len(),
    ensures
        ret.0@ == old(slice)@.subrange(0, mid as int),
        ret.1@ == old(slice)@.subrange(mid as int, old(slice)@.len() as int),
        final(slice)@ == final(ret.0)@ + final(ret.1)@,
{
    match slice.split_at_mut_checked(mid) {
        Some(pair) => pair,
        None => {
            assert(false);
            vstd::vpanic!("mid > len")
        },
    }
}

} // verus!

fn main() {}