#![feature(allocator_api)]

use std::alloc::Allocator;
use vstd::prelude::*;
use vstd::std_specs::iter::IteratorSpec;

#[path = "../proofs/correctness/into_iter/isolated/consumers.rs"]
mod consumers;
#[path = "../proofs/correctness/into_iter/isolated/iterator_methods.rs"]
mod iterator_methods;

verus! {

broadcast use vstd::seq::group_seq_lemmas;

pub fn count_constructed<T, A: Allocator>(v: Vec<T, A>) -> (result: usize)
    ensures result == v@.len(),
{
    let iter = v.into_iter();
    assert(IteratorSpec::remaining(&iter) == v@);
    iter.count()
}

pub fn last_constructed<T, A: Allocator>(v: Vec<T, A>) -> (result: Option<T>)
    ensures result == if v@.len() == 0 { None } else { Some(v@.last()) },
{
    let iter = v.into_iter();
    assert(IteratorSpec::remaining(&iter) == v@);
    iter.last()
}

pub fn count_after_front<T, A: Allocator>(v: Vec<T, A>) -> (result: usize)
    requires v@.len() >= 1,
    ensures result == v@.len() - 1,
{
    let mut iter = v.into_iter();
    let _ = iter.next();
    assert(IteratorSpec::remaining(&iter) == v@.drop_first());
    iter.count()
}

pub fn last_after_front<T, A: Allocator>(v: Vec<T, A>) -> (result: Option<T>)
    requires v@.len() >= 1,
    ensures result == if v@.len() == 1 { None } else { Some(v@.last()) },
{
    let mut iter = v.into_iter();
    let _ = iter.next();
    assert(IteratorSpec::remaining(&iter) == v@.drop_first());
    iter.last()
}

pub fn count_after_back<T, A: Allocator>(v: Vec<T, A>) -> (result: usize)
    requires v@.len() >= 1,
    ensures result == v@.len() - 1,
{
    let mut iter = v.into_iter();
    let _ = iter.next_back();
    assert(IteratorSpec::remaining(&iter) == v@.drop_last());
    iter.count()
}

pub fn last_after_back<T, A: Allocator>(v: Vec<T, A>) -> (result: Option<T>)
    requires v@.len() >= 1,
    ensures result == if v@.len() == 1 { None } else { Some(v@[v@.len() - 2]) },
{
    let mut iter = v.into_iter();
    let _ = iter.next_back();
    assert(IteratorSpec::remaining(&iter) == v@.drop_last());
    iter.last()
}

pub fn count_after_mixed<T, A: Allocator>(v: Vec<T, A>) -> (result: usize)
    requires v@.len() >= 2,
    ensures result == v@.len() - 2,
{
    let mut iter = v.into_iter();
    let _ = iter.next_back();
    let _ = iter.next();
    assert(IteratorSpec::remaining(&iter) == v@.drop_last().drop_first());
    iter.count()
}

pub fn last_after_mixed<T, A: Allocator>(v: Vec<T, A>) -> (result: Option<T>)
    requires v@.len() >= 2,
    ensures result == if v@.len() == 2 { None } else { Some(v@[v@.len() - 2]) },
{
    let mut iter = v.into_iter();
    let _ = iter.next_back();
    let _ = iter.next();
    assert(IteratorSpec::remaining(&iter) == v@.drop_last().drop_first());
    iter.last()
}

}
