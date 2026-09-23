use vstd::prelude::*;

#[path = "../../../../specs/slice/raw_post.rs"]
mod contracts;

verus! {

pub assume_specification<T>[ core::slice::from_mut ](s: &mut T) -> (result: &mut [T])
    ensures
        contracts::singleton_post(*old(s), result@),
        contracts::singleton_post(*final(s), final(result)@),
;

}
