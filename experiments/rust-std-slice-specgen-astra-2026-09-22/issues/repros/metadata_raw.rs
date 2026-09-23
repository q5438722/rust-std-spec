#![feature(ptr_metadata)]
use vstd::prelude::*;

verus! {
// Isolate the real delegated operation without a reference-to-pointer coercion.
pub const fn raw_metadata<T>(pointer: *const [T]) -> (result: usize)
    ensures
        result == pointer@.metadata,
{
    core::ptr::metadata(pointer)
}
}
