#![feature(allocator_api)]

use std::alloc::Allocator;
use vstd::prelude::*;

#[path = "../specs/vec/owned_conversions.rs"]
mod owned_conversions;

verus! {

#[cfg(not(no_global_oom_handling))]
pub fn array_client<T, const N: usize>(s: [T; N]) -> (result: Vec<T>)
    ensures
        result@ == s@,
{
    <Vec<T> as From<[T; N]>>::from(s)
}

pub fn boxed_client<T, A: Allocator>(s: Box<[T], A>) -> (result: Vec<T, A>)
    ensures
        result@ == s@,
{
    <Vec<T, A> as From<Box<[T], A>>>::from(s)
}

#[cfg(not(no_global_oom_handling))]
pub fn empty_array_client<T>(s: [T; 0]) -> (result: Vec<T>)
    ensures
        result@.len() == 0,
{
    <Vec<T> as From<[T; 0]>>::from(s)
}

#[cfg(not(no_global_oom_handling))]
pub fn duplicate_order_client() -> (result: Vec<u8>)
    ensures
        result@ == seq![8u8, 3u8, 8u8, 1u8],
{
    <Vec<u8> as From<[u8; 4]>>::from([8, 3, 8, 1])
}

pub proof fn order_is_observable<T>(first: T, second: T)
    requires
        first != second,
    ensures
        seq![first, second, first] != seq![second, first, first],
{
    assert(seq![first, second, first][0] != seq![second, first, first][0]);
}

pub proof fn interior_element_is_observable<T>(outer: T, first: T, second: T)
    requires
        first != second,
    ensures
        seq![outer, first, outer] != seq![outer, second, outer],
{
    assert(seq![outer, first, outer][1] != seq![outer, second, outer][1]);
}

}
