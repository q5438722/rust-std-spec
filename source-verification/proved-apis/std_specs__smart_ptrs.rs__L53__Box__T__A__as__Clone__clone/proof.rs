#![feature(allocator_api)]
#![allow(dead_code)]
#![allow(unused_imports)]

extern crate alloc;

use alloc::boxed::Box;
use core::alloc::Allocator;
use core::mem::MaybeUninit;
use vstd::prelude::*;
use vstd::raw_ptr::MemContents;
use vstd::std_specs::alloc::*;
use vstd::std_specs::smart_ptrs::*;

verus! {

pub assume_specification<T: ?Sized, A: Allocator>[
    Box::<T, A>::allocator
](
    value: &Box<T, A>,
) -> (result: &A);

pub assume_specification<T, A: Allocator>[
    Box::<T, A>::new_uninit_in
](
    alloc: A,
) -> (result: Box<MaybeUninit<T>, A>)
    where
        A: Allocator,
;

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

fn source_box_clone<T: Clone, A: Allocator + Clone>(
    b: &Box<T, A>,
) -> (res: Box<T, A>)
    ensures
        cloned::<T>(**b, *res),
{
    let alloc = Box::allocator(b).clone();
    let mut boxed = Box::<T, A>::new_uninit_in(alloc);
    unsafe {
        // The sized CloneToUninit path is clone-and-write; its TrivialClone
        // specialization is required to be equivalent to that clone.
        let value = T::clone(&**b);
        assert(cloned::<T>(**b, value));
        *boxed = MaybeUninit::new(value);
        assert(boxed.mem_contents() == MemContents::Init(value));
        boxed.assume_init()
    }
}

} // verus!

fn main() {}