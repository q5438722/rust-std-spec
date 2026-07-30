#![feature(allocator_api)]
#![allow(dead_code)]
#![allow(unused_imports)]

extern crate alloc;

use alloc::boxed::Box;
use core::alloc::Allocator;
use core::mem::MaybeUninit;
use vstd::prelude::*;
use vstd::raw_ptr::MemContents;

verus! {

pub assume_specification<T>[
    MaybeUninit::<T>::write
](
    slot: &mut MaybeUninit<T>,
    value: T,
) -> (res: &mut T)
    ensures
        *res == value,
        final(slot).mem_contents() == MemContents::Init(value),
;

pub assume_specification<T, A: Allocator>[
    Box::<MaybeUninit<T>, A>::assume_init
](
    boxed: Box<MaybeUninit<T>, A>,
) -> (res: Box<T, A>)
    requires
        boxed.mem_contents() is Init,
    ensures
        boxed.mem_contents() matches MemContents::Init(inner) && *res == inner,
;

pub fn source_box_write<T, A: Allocator>(
    mut boxed: Box<MaybeUninit<T>, A>,
    value: T,
) -> (res: Box<T, A>)
    ensures
        *res == value,
{
    unsafe {
        (*boxed).write(value);
        boxed.assume_init()
    }
}

} // verus!

fn main() {}