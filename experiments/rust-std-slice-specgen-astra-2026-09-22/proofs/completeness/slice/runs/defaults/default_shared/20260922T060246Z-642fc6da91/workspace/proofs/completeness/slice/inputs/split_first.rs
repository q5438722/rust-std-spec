use vstd::prelude::*;
#[path = "../../../../specs/slice/mod.rs"]
mod contracts;

mod source {
    pub const fn split_first<T>(slice: &[T]) -> Option<(&T, &[T])> {
        if let [first, tail @ ..] = slice { Some((first, tail)) } else { None }
    }
}

verus! {
// Analysis declaration only; the implementation proof is kept separately.
pub assume_specification<T>[source::split_first::<T>](slice: &[T]) -> (result: Option<(&T, &[T])>)
    ensures
        contracts::split_first_post(slice, result),
;
}
