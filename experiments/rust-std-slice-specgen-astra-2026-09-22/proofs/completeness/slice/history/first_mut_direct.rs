use vstd::prelude::*;
#[path = "../../../../specs/slice/mutable_endpoints.rs"]
mod contracts;

mod source {
    pub const fn first_mut<T>(slice: &mut [T]) -> Option<&mut T> {
        if let [first, ..] = slice { Some(first) } else { None }
    }
}

verus! {
// Analysis declaration only; no target binding is imported by the source proof.
pub assume_specification<T>[source::first_mut::<T>](slice: &mut [T]) -> (result: Option<&mut T>)
    ensures
        contracts::first_mut_post(
            old(slice)@,
            match result { None => None, Some(value) => Some(*final(value)) },
            (match result { None => None, Some(value) => Some(*value) }, final(slice)@),
        ),
;
}
