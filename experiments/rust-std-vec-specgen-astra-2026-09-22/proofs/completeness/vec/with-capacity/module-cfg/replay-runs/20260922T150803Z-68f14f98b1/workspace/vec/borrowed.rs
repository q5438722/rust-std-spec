use std::alloc::Allocator;
use vstd::prelude::*;

verus! {

pub assume_specification<'a, T, A: Allocator>[
    <Vec<T, A> as AsRef<Vec<T, A>>>::as_ref
](vec: &'a Vec<T, A>) -> (result: &'a Vec<T, A>)
    ensures
        result == vec,
;

pub assume_specification<'a, T, A: Allocator>[
    <Vec<T, A> as AsRef<[T]>>::as_ref
](vec: &'a Vec<T, A>) -> (result: &'a [T])
    ensures
        result@ == vec@,
;

pub assume_specification<'a, T, A: Allocator>[
    <Vec<T, A> as AsMut<Vec<T, A>>>::as_mut
](vec: &'a mut Vec<T, A>) -> (result: &'a mut Vec<T, A>)
    ensures
        *result == *old(vec),
        *final(result) == *final(vec),
;

pub assume_specification<'a, T, A: Allocator>[
    <Vec<T, A> as AsMut<[T]>>::as_mut
](vec: &'a mut Vec<T, A>) -> (result: &'a mut [T])
    ensures
        result@ == old(vec)@,
        final(result)@ == final(vec)@,
;

}
