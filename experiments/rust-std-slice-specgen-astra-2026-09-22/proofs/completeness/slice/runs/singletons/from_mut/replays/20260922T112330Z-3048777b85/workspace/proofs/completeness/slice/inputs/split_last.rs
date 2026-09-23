use vstd::prelude::*;
#[path = "../../../../specs/slice/mod.rs"]
mod contracts;

mod source {
    pub const fn split_last<T>(slice: &[T]) -> Option<(&T, &[T])> {
        if let [init @ .., last] = slice { Some((last, init)) } else { None }
    }
}

verus! {
// Analysis declaration only; the implementation proof is kept separately.
pub assume_specification<T>[source::split_last::<T>](slice: &[T]) -> (result: Option<(&T, &[T])>)
    ensures
        contracts::split_last_post(slice, result),
;
}
