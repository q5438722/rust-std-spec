#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;

verus! {

pub assume_specification<T>[
    <*const [T]>::len
](ptr: *const [T]) -> (result: usize)
    ensures
        result == ptr@.metadata,
;

pub fn source_core_ptr_is_empty<T>(
    ptr: *const [T],
) -> (result: bool)
    ensures
        result <==> ptr@.metadata == 0,
{
    ptr.len() == 0
}

} // verus!

fn main() {}