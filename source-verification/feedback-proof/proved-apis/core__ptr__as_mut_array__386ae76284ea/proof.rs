#![feature(slice_ptr_get)]
#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;

verus! {

pub assume_specification<T>[ <*mut [T]>::len ](
    ptr: *mut [T],
) -> (len: usize)
    ensures
        len == ptr@.metadata,
;

pub assume_specification<T>[ <*mut [T]>::as_mut_ptr ](
    ptr: *mut [T],
) -> (result: *mut T)
    ensures
        result == ptr as *mut T,
;

pub fn source_as_mut_array<T, const N: usize>(
    ptr: *mut [T],
) -> (result: Option<*mut [T; N]>)
    ensures
        result == if ptr@.metadata == N {
            Some(ptr as *mut [T; N])
        } else {
            None
        },
{
    if ptr.len() == N {
        let me = ptr.as_mut_ptr() as *mut [T; N];
        Some(me)
    } else {
        None
    }
}

}

fn main() {}