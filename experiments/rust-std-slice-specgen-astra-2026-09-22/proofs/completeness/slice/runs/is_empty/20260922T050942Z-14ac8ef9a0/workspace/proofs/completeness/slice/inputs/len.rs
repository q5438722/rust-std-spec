#![feature(ptr_metadata)]
use vstd::prelude::*;
#[path = "../../../../specs/slice/mod.rs"]
mod contracts;

mod source {
    pub const fn len<T>(slice: &[T]) -> usize {
        core::ptr::metadata(slice)
    }
}

verus! {
// Analysis declaration only; the implementation proof is kept separately.
pub assume_specification<T>[source::len::<T>](slice: &[T]) -> (result: usize)
    ensures
        contracts::len_post(slice, result),
;
}
