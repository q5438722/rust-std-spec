use vstd::prelude::*;
#[path = "../../../../specs/slice/mod.rs"]
mod contracts;

mod source {
    pub const fn first<T>(slice: &[T]) -> Option<&T> {
        if let [first, ..] = slice { Some(first) } else { None }
    }
}

verus! {
// Analysis declaration only; the implementation proof is kept separately.
pub assume_specification<T>[source::first::<T>](slice: &[T]) -> (result: Option<&T>)
    ensures
        contracts::first_post(slice, result),
;
}
