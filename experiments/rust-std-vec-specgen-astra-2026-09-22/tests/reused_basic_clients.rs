#![feature(allocator_api)]

use std::alloc::Allocator;
use vstd::prelude::*;

#[path = "../specs/vec/reused_basic.rs"]
mod reused_basic;

verus! {

pub fn default_official<T>() -> (v: Vec<T>)
    ensures v@ == Seq::<T>::empty(),
{
    <Vec<T> as core::default::Default>::default()
}

pub fn default_source<T>() -> (v: Vec<T>)
    ensures v@ == Seq::<T>::empty(),
{
    reused_basic::default()
}

pub fn is_empty_official<T, A: Allocator>(v: &Vec<T, A>) -> (res: bool)
    ensures res <==> v@.len() == 0,
{
    Vec::is_empty(v)
}

pub fn is_empty_source<T, A: Allocator>(v: &Vec<T, A>) -> (res: bool)
    ensures res <==> v@.len() == 0,
{
    reused_basic::is_empty(v)
}

pub fn deref_official<T, A: Allocator>(vec: &Vec<T, A>) -> (slice: &[T])
    ensures slice@ == vec@,
{
    <Vec<T, A> as core::ops::Deref>::deref(vec)
}

pub fn deref_source<T, A: Allocator>(vec: &Vec<T, A>) -> (slice: &[T])
    ensures slice@ == vec@,
{
    reused_basic::deref(vec)
}

}
