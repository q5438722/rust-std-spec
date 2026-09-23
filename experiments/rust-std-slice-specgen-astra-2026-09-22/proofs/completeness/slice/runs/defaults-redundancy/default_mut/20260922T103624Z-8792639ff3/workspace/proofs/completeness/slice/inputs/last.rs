use vstd::prelude::*;
#[path = "../../../../specs/slice/mod.rs"]
mod contracts;

mod source {
    pub const fn last<T>(slice: &[T]) -> Option<&T> {
        if let [.., last] = slice { Some(last) } else { None }
    }
}

verus! {
// Analysis declaration only; the implementation proof is kept separately.
pub assume_specification<T>[source::last::<T>](slice: &[T]) -> (result: Option<&T>)
    ensures
        contracts::last_post(slice, result),
;
}
