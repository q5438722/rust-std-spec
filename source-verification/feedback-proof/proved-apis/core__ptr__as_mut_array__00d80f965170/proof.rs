#![feature(slice_ptr_get)]
#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::raw_ptr::{ptr_mut_from_data, PtrData};

verus! {

pub assume_specification<T>[<*mut [T]>::len](
    ptr: *mut [T],
) -> (result: usize)
    ensures
        result == ptr@.metadata,
;

pub assume_specification<T>[<*mut [T]>::as_mut_ptr](
    ptr: *mut [T],
) -> (result: *mut T)
    ensures
        result == ptr_mut_from_data::<T>(PtrData::<T> {
            addr: ptr@.addr,
            provenance: ptr@.provenance,
            metadata: (),
        }),
;

pub fn source_as_mut_array<T, const N: usize>(
    ptr: *mut [T],
) -> (result: Option<*mut [T; N]>)
    ensures
        result == if ptr@.metadata == N {
            Some(ptr_mut_from_data::<[T; N]>(PtrData::<[T; N]> {
                addr: ptr@.addr,
                provenance: ptr@.provenance,
                metadata: (),
            }))
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

} // verus!

fn main() {}