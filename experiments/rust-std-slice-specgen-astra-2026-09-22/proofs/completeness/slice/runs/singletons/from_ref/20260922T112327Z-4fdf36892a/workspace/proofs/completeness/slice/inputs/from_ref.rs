use vstd::prelude::*;

#[path = "../../../../specs/slice/raw_post.rs"]
mod contracts;

verus! {

pub assume_specification<T>[ core::slice::from_ref ](s: &T) -> (result: &[T])
    ensures
        contracts::singleton_post(*s, result@),
;

}
