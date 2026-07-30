#![allow(dead_code)]
#![allow(unused_imports)]
#![feature(allocator_api)]
#![feature(liballoc_internals)]

extern crate alloc;

use alloc::boxed::Box;
use core::alloc::Allocator;
use core::mem::MaybeUninit;
use vstd::prelude::*;
use vstd::raw_ptr::MemContents;
use vstd::std_specs::alloc::*;
use vstd::std_specs::smart_ptrs::*;

verus! {

pub assume_specification<T, A: Allocator>[
    Box::<MaybeUninit<T>, A>::assume_init
](
    value: Box<MaybeUninit<T>, A>,
) -> (result: Box<T, A>)
    requires
        value.mem_contents() is Init,
    ensures
        value.mem_contents() matches MemContents::Init(inner) && *result == inner,
;

fn source_box_new<T>(x: T) -> (v: Box<T>)
    ensures
        *v == x,
{
    // These are the public forms of the source's allocation, move-write, and
    // representation-preserving transmute steps.
    let b: Box<MaybeUninit<T>> = Box::new_uninit();
    let b = alloc::intrinsics::write_box_via_move(b, x);
    unsafe { b.assume_init() }
}

}

fn main() {}