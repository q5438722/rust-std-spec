#![feature(ptr_metadata)]
use core::ptr;
use vstd::prelude::*;
#[path = "../../../specs/slice/mod.rs"]
mod contracts;

verus! {
// Rust 1.96 core/src/slice/mod.rs:101-118; body:116-118.
pub const fn len<T>(slice: &[T]) -> (result: usize)
    ensures
        contracts::len_post(slice, result),
{
    ptr::metadata(slice)
}
}
