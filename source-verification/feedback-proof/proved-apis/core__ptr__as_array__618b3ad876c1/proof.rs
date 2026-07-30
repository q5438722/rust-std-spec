#![feature(slice_ptr_get)]
#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::raw_ptr::{ptr_from_data, PtrData};

verus! {

pub assume_specification<T>[<*const [T]>::len](
    p: *const [T],
) -> (result: usize)
    ensures
        result == p@.metadata,
;

pub assume_specification<T>[<*const [T]>::as_ptr](
    p: *const [T],
) -> (result: *const T)
    ensures
        result == ptr_from_data::<T>(PtrData::<T> {
            addr: p@.addr,
            provenance: p@.provenance,
            metadata: (),
        }),
;

pub fn source_ptr_as_array<T, const N: usize>(
    p: *const [T],
) -> (result: Option<*const [T; N]>)
    ensures
        result == if p@.metadata == N {
            Some(ptr_from_data::<[T; N]>(PtrData::<[T; N]> {
                addr: p@.addr,
                provenance: p@.provenance,
                metadata: (),
            }))
        } else {
            None
        },
{
    if p.len() == N {
        let me = p.as_ptr() as *const [T; N];
        Some(me)
    } else {
        None
    }
}

} // verus!

fn main() {}