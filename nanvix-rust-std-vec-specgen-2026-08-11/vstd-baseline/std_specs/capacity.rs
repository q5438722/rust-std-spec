//! Experimental capacity specifications for allocation-backed collections.
use super::super::multiset::Multiset;
use super::super::prelude::*;
use super::super::utf8::encode_utf8;

use alloc::collections::{BinaryHeap, TryReserveError, VecDeque};
use alloc::string::String;
use alloc::vec::Vec;
use core::alloc::Allocator;

verus! {

pub trait CapacitySpec {
    spec fn spec_capacity(&self) -> nat;
}

impl<T, A: Allocator> CapacitySpec for Vec<T, A> {
    #[verifier::external_body]
    uninterp spec fn spec_capacity(&self) -> nat;
}

impl CapacitySpec for String {
    #[verifier::external_body]
    uninterp spec fn spec_capacity(&self) -> nat;
}

impl<T, A: Allocator> CapacitySpec for VecDeque<T, A> {
    #[verifier::external_body]
    uninterp spec fn spec_capacity(&self) -> nat;
}

impl<T, A: Allocator> CapacitySpec for BinaryHeap<T, A> {
    #[verifier::external_body]
    uninterp spec fn spec_capacity(&self) -> nat;
}

pub assume_specification<T, A: Allocator>[ Vec::<T, A>::capacity ](v: &Vec<T, A>) -> (result: usize)
    ensures
        result as nat == v.spec_capacity(),
;

pub assume_specification<T, A: Allocator>[ Vec::<T, A>::reserve_exact ](
    v: &mut Vec<T, A>,
    additional: usize,
)
    ensures
        final(v)@ == old(v)@,
        final(v).spec_capacity() >= old(v)@.len() + additional as nat,
;

pub assume_specification<T, A: Allocator>[ Vec::<T, A>::try_reserve_exact ](
    v: &mut Vec<T, A>,
    additional: usize,
) -> (result: Result<(), TryReserveError>)
    ensures
        final(v)@ == old(v)@,
        result is Ok ==> final(v).spec_capacity() >= old(v)@.len() + additional as nat,
;

pub assume_specification<T, A: Allocator>[ Vec::<T, A>::shrink_to_fit ](v: &mut Vec<T, A>)
    ensures
        final(v)@ == old(v)@,
        final(v).spec_capacity() >= old(v)@.len(),
        final(v).spec_capacity() <= old(v).spec_capacity(),
;

pub assume_specification<T, A: Allocator>[ Vec::<T, A>::shrink_to ](
    v: &mut Vec<T, A>,
    min_capacity: usize,
)
    ensures
        final(v)@ == old(v)@,
        final(v).spec_capacity() >= old(v)@.len(),
        final(v).spec_capacity() <= old(v).spec_capacity(),
;

pub assume_specification[ String::capacity ](s: &String) -> (result: usize)
    ensures
        result as nat == s.spec_capacity(),
;

pub assume_specification[ String::with_capacity ](capacity: usize) -> (result: String)
    ensures
        result@ == Seq::<char>::empty(),
        result.spec_capacity() >= capacity as nat,
;

pub assume_specification[ String::reserve ](s: &mut String, additional: usize)
    ensures
        final(s)@ == old(s)@,
        final(s).spec_capacity() >= encode_utf8(old(s)@).len() + additional as nat,
;

pub assume_specification[ String::reserve_exact ](s: &mut String, additional: usize)
    ensures
        final(s)@ == old(s)@,
        final(s).spec_capacity() >= encode_utf8(old(s)@).len() + additional as nat,
;

pub assume_specification[ String::try_reserve ](s: &mut String, additional: usize) -> (result:
    Result<(), TryReserveError>)
    ensures
        final(s)@ == old(s)@,
        result is Ok ==> final(s).spec_capacity() >= encode_utf8(old(s)@).len() + additional as nat,
;

pub assume_specification[ String::try_reserve_exact ](s: &mut String, additional: usize) -> (result:
    Result<(), TryReserveError>)
    ensures
        final(s)@ == old(s)@,
        result is Ok ==> final(s).spec_capacity() >= encode_utf8(old(s)@).len() + additional as nat,
;

pub assume_specification[ String::shrink_to_fit ](s: &mut String)
    ensures
        final(s)@ == old(s)@,
        final(s).spec_capacity() >= encode_utf8(old(s)@).len(),
        final(s).spec_capacity() <= old(s).spec_capacity(),
;

pub assume_specification[ String::shrink_to ](s: &mut String, min_capacity: usize)
    ensures
        final(s)@ == old(s)@,
        final(s).spec_capacity() >= encode_utf8(old(s)@).len(),
        final(s).spec_capacity() <= old(s).spec_capacity(),
;

pub assume_specification<T, A: Allocator>[ VecDeque::<T, A>::capacity ](
    v: &VecDeque<T, A>,
) -> (result: usize)
    ensures
        result as nat == v.spec_capacity(),
;

pub assume_specification<T, A: Allocator>[ VecDeque::<T, A>::try_reserve ](
    v: &mut VecDeque<T, A>,
    additional: usize,
) -> (result: Result<(), TryReserveError>)
    ensures
        final(v)@ == old(v)@,
        result is Ok ==> final(v).spec_capacity() >= old(v)@.len() + additional as nat,
;

pub assume_specification<T, A: Allocator>[ VecDeque::<T, A>::shrink_to_fit ](v: &mut VecDeque<T, A>)
    ensures
        final(v)@ == old(v)@,
        final(v).spec_capacity() >= old(v)@.len(),
        final(v).spec_capacity() <= old(v).spec_capacity(),
;

pub assume_specification<T, A: Allocator>[ VecDeque::<T, A>::shrink_to ](
    v: &mut VecDeque<T, A>,
    min_capacity: usize,
)
    ensures
        final(v)@ == old(v)@,
        final(v).spec_capacity() >= old(v)@.len(),
        final(v).spec_capacity() <= old(v).spec_capacity(),
;

pub assume_specification<T, A: Allocator>[ BinaryHeap::<T, A>::capacity ](
    heap: &BinaryHeap<T, A>,
) -> (result: usize)
    ensures
        result as nat == heap.spec_capacity(),
;

pub assume_specification<T>[ BinaryHeap::<T>::with_capacity ](capacity: usize) -> (result:
    BinaryHeap<T>)
    ensures
        result@ == Multiset::<T>::empty(),
        result.spec_capacity() >= capacity as nat,
;

pub assume_specification<T, A: Allocator>[ BinaryHeap::<T, A>::reserve ](
    heap: &mut BinaryHeap<T, A>,
    additional: usize,
)
    ensures
        final(heap)@ == old(heap)@,
        final(heap).spec_capacity() >= old(heap)@.len() + additional as nat,
;

pub assume_specification<T, A: Allocator>[ BinaryHeap::<T, A>::reserve_exact ](
    heap: &mut BinaryHeap<T, A>,
    additional: usize,
)
    ensures
        final(heap)@ == old(heap)@,
        final(heap).spec_capacity() >= old(heap)@.len() + additional as nat,
;

pub assume_specification<T, A: Allocator>[ BinaryHeap::<T, A>::try_reserve ](
    heap: &mut BinaryHeap<T, A>,
    additional: usize,
) -> (result: Result<(), TryReserveError>)
    ensures
        final(heap)@ == old(heap)@,
        result is Ok ==> final(heap).spec_capacity() >= old(heap)@.len() + additional as nat,
;

pub assume_specification<T, A: Allocator>[ BinaryHeap::<T, A>::try_reserve_exact ](
    heap: &mut BinaryHeap<T, A>,
    additional: usize,
) -> (result: Result<(), TryReserveError>)
    ensures
        final(heap)@ == old(heap)@,
        result is Ok ==> final(heap).spec_capacity() >= old(heap)@.len() + additional as nat,
;

pub assume_specification<T, A: Allocator>[ BinaryHeap::<T, A>::shrink_to_fit ](
    heap: &mut BinaryHeap<T, A>,
)
    ensures
        final(heap)@ == old(heap)@,
        final(heap).spec_capacity() >= old(heap)@.len(),
        final(heap).spec_capacity() <= old(heap).spec_capacity(),
;

pub assume_specification<T, A: Allocator>[ BinaryHeap::<T, A>::shrink_to ](
    heap: &mut BinaryHeap<T, A>,
    min_capacity: usize,
)
    ensures
        final(heap)@ == old(heap)@,
        final(heap).spec_capacity() >= old(heap)@.len(),
        final(heap).spec_capacity() <= old(heap).spec_capacity(),
;

} // verus!
