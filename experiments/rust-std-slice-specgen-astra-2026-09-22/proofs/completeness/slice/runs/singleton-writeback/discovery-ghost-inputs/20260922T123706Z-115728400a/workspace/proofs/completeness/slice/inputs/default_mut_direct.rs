use vstd::prelude::*;

#[path = "../../../../specs/slice/default_post.rs"]
mod contracts;

verus! {

pub assume_specification<'a, T>[ <&'a mut [T] as core::default::Default>::default ]()
    -> (result: &'a mut [T])
    ensures
        contracts::default_post(result),
;

}
