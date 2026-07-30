#![allow(dead_code)]
#![allow(unused_imports)]
#![feature(allocator_api)]
#![feature(liballoc_internals)]

extern crate alloc;

use vstd::prelude::*;
use vstd::raw_ptr::MemContents;
use vstd::std_specs::alloc::*;

verus! {

pub assume_specification<T, A: core::alloc::Allocator>[
    alloc::boxed::Box::<core::mem::MaybeUninit<T>, A>::assume_init
](
    vals: alloc::boxed::Box<core::mem::MaybeUninit<T>, A>,
) -> (result: alloc::boxed::Box<T, A>)
    requires
        vals.mem_contents() is Init,
    ensures
        vals.mem_contents() matches MemContents::Init(value) && *result == value,
;

fn source_box_assume_init_into_vec_unsafe<T, const N: usize>(
    vals: alloc::boxed::Box<core::mem::MaybeUninit<[T; N]>>,
) -> (result: alloc::vec::Vec<T>)
    requires
        vals.mem_contents() is Init,
    ensures
        vals.mem_contents() matches MemContents::Init(array) && result@ == array@,
{
    let initialized: alloc::boxed::Box<[T; N]> = unsafe { vals.assume_init() };
    let slice: alloc::boxed::Box<[T]> = initialized;
    slice.into_vec()
}

} // verus!

fn main() {}