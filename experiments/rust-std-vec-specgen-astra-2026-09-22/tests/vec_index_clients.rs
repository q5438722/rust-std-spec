#![feature(allocator_api, slice_index_methods)]

use std::alloc::Allocator;
use std::ops::{Index, Range};
use std::slice::SliceIndex;
use vstd::prelude::*;
use vstd::std_specs::core::IndexSpec;

#[path = "../specs/vec/index.rs"]
mod source;

verus! {

pub fn source_generic<T, I: SliceIndex<[T]>, A: Allocator>(
    vec: &Vec<T, A>, index: I,
) -> (r: &<Vec<T, A> as Index<I>>::Output)
    requires vec.index_req(&index),
    ensures exists|s: &[T]| #[trigger] s@ == vec@
        && call_ensures(<I as SliceIndex<[T]>>::index, (index, s), r),
{
    source::index_source(vec, index)
}

pub fn std_generic<T, I: SliceIndex<[T]>, A: Allocator>(
    vec: &Vec<T, A>, index: I,
) -> (r: &<Vec<T, A> as Index<I>>::Output)
    requires vec.index_req(&index),
    ensures exists|s: &[T]| #[trigger] s@ == vec@
        && call_ensures(<I as SliceIndex<[T]>>::index, (index, s), r),
{
    Index::index(vec, index)
}

pub fn source_element<T, A: Allocator>(vec: &Vec<T, A>, i: usize) -> (r: &T)
    requires i < vec@.len(),
    ensures *r == vec@[i as int],
{
    source::index_source(vec, i)
}

pub fn std_element<T, A: Allocator>(vec: &Vec<T, A>, i: usize) -> (r: &T)
    requires i < vec@.len(),
    ensures *r == vec@[i as int],
{
    Index::index(vec, i)
}

pub fn source_range<T, A: Allocator>(vec: &Vec<T, A>, range: Range<usize>) -> (r: &[T])
    requires range.start <= range.end <= vec@.len(),
    ensures r@ == vec@.subrange(range.start as int, range.end as int),
{
    source::index_source(vec, range)
}

pub fn std_range<T, A: Allocator>(vec: &Vec<T, A>, range: Range<usize>) -> (r: &[T])
    requires range.start <= range.end <= vec@.len(),
    ensures r@ == vec@.subrange(range.start as int, range.end as int),
{
    Index::index(vec, range)
}

pub fn source_full<T, A: Allocator>(vec: &Vec<T, A>) -> (r: &[T])
    ensures r@ == vec@,
{
    source::index_source(vec, ..)
}

pub fn std_full<T, A: Allocator>(vec: &Vec<T, A>) -> (r: &[T])
    ensures r@ == vec@,
{
    Index::index(vec, ..)
}

}
