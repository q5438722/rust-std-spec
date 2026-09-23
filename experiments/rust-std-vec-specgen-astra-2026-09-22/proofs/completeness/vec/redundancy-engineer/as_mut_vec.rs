#![feature(allocator_api)]

use std::alloc::Allocator;
use vstd::prelude::*;

// Exact input declaration; specdet stops before proof/query generation.
verus! {

pub assume_specification<'a, T, A: Allocator>[
    <Vec<T, A> as AsMut<Vec<T, A>>>::as_mut
](vec: &'a mut Vec<T, A>) -> (result: &'a mut Vec<T, A>)
    ensures
        *result == *old(vec),
        *final(result) == *final(vec),
;

}
