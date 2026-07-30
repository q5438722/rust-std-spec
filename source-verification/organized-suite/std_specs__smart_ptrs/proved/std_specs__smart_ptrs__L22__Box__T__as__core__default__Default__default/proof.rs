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

fn box_default_proof<T: core::default::Default>() -> (res: Box<T>)
    ensures
        T::default.ensures((), *res),
{
    let mut x: Box<MaybeUninit<T>> = Box::new_uninit();
    unsafe {
        let value = T::default();
        // Source-faithful desugaring of ptr::write into the uninitialized Box slot.
        *x = MaybeUninit::new(value);
        assert(x.mem_contents() == MemContents::Init(value));
        x.assume_init()
    }
}

} // verus!

fn main() {}