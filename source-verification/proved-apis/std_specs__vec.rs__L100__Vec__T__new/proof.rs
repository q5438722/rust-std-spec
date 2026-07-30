#![allow(dead_code)]
#![allow(unused_imports)]
#![feature(allocator_api)]

extern crate alloc;

use alloc::alloc::Global;
use alloc::vec::Vec;
use vstd::prelude::*;
use vstd::std_specs::vec::*;

verus! {

pub assume_specification[
    <Global as core::default::Default>::default
]() -> Global;

fn source_vec_new<T>() -> (v: Vec<T>)
    ensures
        v@ == Seq::<T>::empty(),
{
    // RawVec::new() is RawVec::new_in(Global), so this is the public,
    // allocator-generic form of `Vec { buf: RawVec::new(), len: 0 }`.
    let alloc = <Global as core::default::Default>::default();
    Vec::<T, Global>::new_in(alloc)
}

}

fn main() {}