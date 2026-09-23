use vstd::prelude::*;

#[path = "../../../../specs/slice/default_post.rs"]
mod contracts;

verus! {

pub assume_specification<'a, T>[ <&'a [T] as core::default::Default>::default ]()
    -> (result: &'a [T])
    ensures
        contracts::default_post(result),
;

}
