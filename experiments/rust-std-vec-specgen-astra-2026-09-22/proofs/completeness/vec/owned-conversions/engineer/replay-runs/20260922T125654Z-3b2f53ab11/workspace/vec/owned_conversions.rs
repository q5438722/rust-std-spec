use std::alloc::Allocator;
use vstd::prelude::*;

verus! {

#[cfg(not(no_global_oom_handling))]
pub assume_specification<T, const N: usize>[
    <Vec<T> as From<[T; N]>>::from
](s: [T; N]) -> (result: Vec<T>)
    ensures
        result@ == s@,
;

pub assume_specification<T, A: Allocator>[
    <Vec<T, A> as From<Box<[T], A>>>::from
](s: Box<[T], A>) -> (result: Vec<T, A>)
    ensures
        result@ == s@,
;

}
