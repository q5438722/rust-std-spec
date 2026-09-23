use vstd::prelude::*;
#[path = "../../../../specs/slice/mod.rs"]
mod contracts;

mod source {
    pub const fn is_empty<T>(slice: &[T]) -> bool {
        slice.len() == 0
    }
}

verus! {
// Analysis declaration only; the implementation proof is kept separately.
pub assume_specification<T>[source::is_empty::<T>](slice: &[T]) -> (result: bool)
    ensures
        contracts::is_empty_post(slice, result),
;
}
