#![feature(ptr_metadata)]
use core::ptr;
use vstd::prelude::*;
#[path = "../../specs/slice/mod.rs"]
mod contracts;

verus! {
// Unadopted diagnostic proposal described before creation in V-METADATA.md.
pub const fn len<T>(slice: &[T]) -> (result: usize)
    ensures
        contracts::len_post(slice, result),
{
    ptr::metadata(slice as *const [T])
}
}
