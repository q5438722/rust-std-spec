#![allow(dead_code)]

use vstd::prelude::*;

verus! {

pub assume_specification<T>[ <[T]>::split_at_unchecked ](
    slice: &[T],
    mid: usize,
) -> (ret: (&[T], &[T]))
    requires
        mid <= slice.len(),
    ensures
        ret.0@ == slice@.subrange(0, mid as int),
        ret.1@ == slice@.subrange(mid as int, slice@.len() as int),
;

pub const fn source_core_slice_split_at_checked<T>(
    slice: &[T],
    mid: usize,
) -> (ret: core::option::Option<(&[T], &[T])>)
    ensures
        ret.is_some() <==> mid <= slice@.len(),
        ret.is_some() ==> ret.unwrap().0@ == slice@.subrange(0, mid as int),
        ret.is_some() ==> ret.unwrap().1@ == slice@.subrange(mid as int, slice@.len() as int),
{
    if mid <= slice.len() {
        assert(mid <= slice@.len());
        Some(unsafe { slice.split_at_unchecked(mid) })
    } else {
        None
    }
}

} // verus!

fn main() {}