#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::std_specs::slice::*;

#[cfg(verus_keep_ghost)]
macro_rules! panic {
    ($($arg:tt)*) => {
        vstd::vpanic!($($arg)*)
    };
}

verus! {

pub assume_specification<T>[ <[T]>::split_at_checked ](
    slice: &[T],
    mid: usize,
) -> (ret: Option<(&[T], &[T])>)
    ensures
        ret.is_some() <==> mid <= slice@.len(),
        ret.is_some() ==> ret.unwrap().0@ == slice@.subrange(0, mid as int),
        ret.is_some() ==> ret.unwrap().1@ == slice@.subrange(mid as int, slice@.len() as int),
;

fn source_slice_split_at<T>(slice: &[T], mid: usize) -> (ret: (&[T], &[T]))
    requires
        0 <= mid <= slice.len(),
    ensures
        ret.0@ == slice@.subrange(0, mid as int),
        ret.1@ == slice@.subrange(mid as int, slice@.len() as int),
{
    match slice.split_at_checked(mid) {
        Some(pair) => pair,
        None => panic!("mid > len"),
    }
}

} // verus!

fn main() {}