#![allow(dead_code)]
#![allow(unused_imports)]
#![feature(liballoc_internals)]

extern crate alloc;

use alloc::boxed::Box;
use core::mem::MaybeUninit;
use vstd::prelude::*;
use vstd::raw_ptr::MemContents;
use vstd::std_specs::alloc::*;

verus! {

fn source_alloc_intrinsics_write_box_via_move<T>(
    mut b: Box<MaybeUninit<T>>,
    x: T,
) -> (result: Box<MaybeUninit<T>>)
    ensures
        result.mem_contents() == MemContents::Init(x),
{
    *b = MaybeUninit::new(x);
    assert(b.mem_contents() == MemContents::Init(x));
    b
}

} // verus!

fn main() {}