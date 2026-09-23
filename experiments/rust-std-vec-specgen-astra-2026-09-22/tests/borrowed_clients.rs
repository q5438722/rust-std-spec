#![feature(allocator_api)]

#[path = "../specs/vec/borrowed.rs"]
mod borrowed;

use std::alloc::Allocator;
use vstd::prelude::*;

verus! {

pub proof fn shared_view_congruence<T, A: Allocator>(left: &Vec<T, A>, right: &Vec<T, A>)
    ensures (left == right) ==> (left@ == right@),
{
}

pub proof fn value_view_congruence<T, A: Allocator>(left: Vec<T, A>, right: Vec<T, A>)
    ensures (left == right) ==> (left@ == right@),
{
}

pub fn shared_previous_contract<'a, T, A: Allocator>(vec: &'a Vec<T, A>)
    -> (result: &'a Vec<T, A>)
    ensures
        result == vec,
        result@ == vec@,
{
    <Vec<T, A> as AsRef<Vec<T, A>>>::as_ref(vec)
}

pub fn mutable_previous_contract<'a, T, A: Allocator>(vec: &'a mut Vec<T, A>)
    -> (result: &'a mut Vec<T, A>)
    ensures
        *result == *old(vec),
        result@ == old(vec)@,
        *final(result) == *final(vec),
        final(result)@ == final(vec)@,
{
    <Vec<T, A> as AsMut<Vec<T, A>>>::as_mut(vec)
}

pub fn vector_writeback<T, A: Allocator>(vec: &mut Vec<T, A>, value: T)
    ensures final(vec)@ == old(vec)@.push(value),
{
    let result: &mut Vec<T, A> = <Vec<T, A> as AsMut<Vec<T, A>>>::as_mut(vec);
    result.push(value);
}

pub fn slice_writeback<T, A: Allocator>(vec: &mut Vec<T, A>, value: T)
    requires old(vec)@.len() > 0,
    ensures final(vec)@ == old(vec)@.update(0, value),
{
    let result: &mut [T] = <Vec<T, A> as AsMut<[T]>>::as_mut(vec);
    result[0] = value;
}

}
