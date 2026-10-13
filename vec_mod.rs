use core::alloc::Allocator;
use std::borrow::Cow;
use std::vec::IntoIter;
use vstd::prelude::*;
use vstd::std_specs::cmp::PartialEqSpec;
use vstd::std_specs::iter::IteratorSpec;
use vstd::std_specs::vec::into_iter_elts;

verus! {

pub assume_specification<'a, T, A: Allocator>[ <&'a mut Vec<T, A> as IntoIterator>::into_iter ](
    vec: &'a mut Vec<T, A>,
) -> (iter: <&'a mut Vec<T, A> as IntoIterator>::IntoIter)
    ensures
        IteratorSpec::remaining(&iter).len() == old(vec)@.len() == final(vec)@.len(),
        forall|i: int|
            #![trigger IteratorSpec::remaining(&iter)[i]]
            0 <= i < old(vec)@.len() ==> *IteratorSpec::remaining(&iter)[i] == old(vec)@[i],
        forall|i: int|
            #![trigger IteratorSpec::remaining(&iter)[i]]
            #![trigger final(vec)@[i]]
            0 <= i < old(vec)@.len() ==> *final(IteratorSpec::remaining(&iter)[i])
                == final(vec)@[i],
        IteratorSpec::decrease(&iter) is Some,
;

pub assume_specification<'a, T, A: Allocator>[ <Vec<T, A> as AsRef<Vec<T, A>>>::as_ref ](
    vec: &'a Vec<T, A>,
) -> (result: &'a Vec<T, A>)
    ensures
        result == vec,
;

pub assume_specification<'a, T, A: Allocator>[ <Vec<T, A> as AsRef<[T]>>::as_ref ](
    vec: &'a Vec<T, A>,
) -> (result: &'a [T])
    ensures
        result@ == vec@,
;

pub assume_specification<'a, T, A: Allocator>[ <Vec<T, A> as AsMut<Vec<T, A>>>::as_mut ](
    vec: &'a mut Vec<T, A>,
) -> (result: &'a mut Vec<T, A>)
    ensures
        *result == *old(vec),
        *final(result) == *final(vec),
;

pub assume_specification<'a, T, A: Allocator>[ <Vec<T, A> as AsMut<[T]>>::as_mut ](
    vec: &'a mut Vec<T, A>,
) -> (result: &'a mut [T])
    ensures
        result@ == old(vec)@,
        final(result)@ == final(vec)@,
;

#[cfg(not(no_global_oom_handling))]
pub assume_specification<T, const N: usize>[ <Vec<T> as From<[T; N]>>::from ](
    array: [T; N],
) -> (result: Vec<T>)
    ensures
        result@ == array@,
;

pub assume_specification<T, A: Allocator>[ <Vec<T, A> as From<Box<[T], A>>>::from ](
    slice: Box<[T], A>,
) -> (result: Vec<T, A>)
    ensures
        result@ == slice@,
;

} // verus!
