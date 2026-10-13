use core::alloc::Allocator;
use std::borrow::Cow;
use std::vec::IntoIter;
use vstd::prelude::*;
use vstd::std_specs::cmp::PartialEqSpec;
use vstd::std_specs::iter::IteratorSpec;
use vstd::std_specs::vec::into_iter_elts;

verus! {

#[cfg(not(no_global_oom_handling))]
pub assume_specification<'a, T: Clone>[ <Cow<'a, [T]> as From<&'a [T]>>::from ](
    slice: &'a [T],
) -> (result: Cow<'a, [T]>)
    ensures
        match result {
            Cow::Borrowed(contents) => contents@ == slice@,
            Cow::Owned(_) => false,
        },
;

#[cfg(not(no_global_oom_handling))]
pub assume_specification<'a, T: Clone, const N: usize>[ <Cow<'a, [T]> as From<&'a [T; N]>>::from ](
    array: &'a [T; N],
) -> (result: Cow<'a, [T]>)
    ensures
        match result {
            Cow::Borrowed(contents) => contents@ == array@,
            Cow::Owned(_) => false,
        },
;

#[cfg(not(no_global_oom_handling))]
pub assume_specification<'a, T: Clone>[ <Cow<'a, [T]> as From<Vec<T>>>::from ](
    vec: Vec<T>,
) -> (result: Cow<'a, [T]>)
    ensures
        match result {
            Cow::Borrowed(_) => false,
            Cow::Owned(contents) => contents@ == vec@,
        },
;

#[cfg(not(no_global_oom_handling))]
pub assume_specification<'a, T: Clone>[ <Cow<'a, [T]> as From<&'a Vec<T>>>::from ](
    vec: &'a Vec<T>,
) -> (result: Cow<'a, [T]>)
    ensures
        match result {
            Cow::Borrowed(contents) => contents@ == vec@,
            Cow::Owned(_) => false,
        },
;

pub assume_specification<T, A: Allocator + Default>[ <IntoIter<
    T,
    A,
> as Default>::default ]() -> (iter: IntoIter<T, A>)
    ensures
        IteratorSpec::remaining(&iter) == Seq::<T>::empty(),
        IteratorSpec::decrease(&iter) is Some,
        into_iter_elts(iter) == IteratorSpec::remaining(&iter),
;

pub assume_specification<T, A: Allocator>[ <IntoIter<T, A> as Iterator>::count ](
    iter: IntoIter<T, A>,
) -> (result: usize)
    ensures
        result == IteratorSpec::remaining(&iter).len(),
;

pub assume_specification<T, A: Allocator>[ <IntoIter<T, A> as Iterator>::last ](
    iter: IntoIter<T, A>,
) -> (result: Option<T>)
    ensures
        result == if IteratorSpec::remaining(&iter).len() == 0 {
            None
        } else {
            Some(IteratorSpec::remaining(&iter).last())
        },
;

pub assume_specification<'spec0, T: PartialEq<U>, U, A: Allocator>[ <Vec<T, A> as PartialEq<
    &[U],
>>::eq ](left: &Vec<T, A>, right: &&[U]) -> (result: bool)
    ensures
        <T as PartialEqSpec<U>>::obeys_eq_spec() ==> {
            let left_contents = left@;
            let right_contents = right@;
            result == (left_contents.len() == right_contents.len() && forall|i: int|
                #![auto]
                0 <= i < left_contents.len() ==> <T as PartialEqSpec<U>>::eq_spec(
                    &left_contents[i],
                    &right_contents[i],
                ))
        },
;

pub assume_specification<'spec0, T: PartialEq<U>, U, A: Allocator>[ <Vec<T, A> as PartialEq<
    &[U],
>>::ne ](left: &Vec<T, A>, right: &&[U]) -> (result: bool)
    ensures
        <T as PartialEqSpec<U>>::obeys_eq_spec() ==> {
            let left_contents = left@;
            let right_contents = right@;
            result == !(left_contents.len() == right_contents.len() && forall|i: int|
                #![auto]
                0 <= i < left_contents.len() ==> <T as PartialEqSpec<U>>::eq_spec(
                    &left_contents[i],
                    &right_contents[i],
                ))
        },
;

pub assume_specification<'spec0, T: PartialEq<U>, U, A: Allocator>[ <Vec<T, A> as PartialEq<
    &mut [U],
>>::eq ](left: &Vec<T, A>, right: &&mut [U]) -> (result: bool)
    ensures
        <T as PartialEqSpec<U>>::obeys_eq_spec() ==> {
            let left_contents = left@;
            let right_contents = old(*right)@;
            result == (left_contents.len() == right_contents.len() && forall|i: int|
                #![auto]
                0 <= i < left_contents.len() ==> <T as PartialEqSpec<U>>::eq_spec(
                    &left_contents[i],
                    &right_contents[i],
                ))
        },
;

pub assume_specification<'spec0, T: PartialEq<U>, U, A: Allocator>[ <Vec<T, A> as PartialEq<
    &mut [U],
>>::ne ](left: &Vec<T, A>, right: &&mut [U]) -> (result: bool)
    ensures
        <T as PartialEqSpec<U>>::obeys_eq_spec() ==> {
            let left_contents = left@;
            let right_contents = old(*right)@;
            result == !(left_contents.len() == right_contents.len() && forall|i: int|
                #![auto]
                0 <= i < left_contents.len() ==> <T as PartialEqSpec<U>>::eq_spec(
                    &left_contents[i],
                    &right_contents[i],
                ))
        },
;

pub assume_specification<'spec0, T: PartialEq<U>, U, A: Allocator>[ <&'spec0 [T] as PartialEq<
    Vec<U, A>,
>>::eq ](left: &&'spec0 [T], right: &Vec<U, A>) -> (result: bool)
    ensures
        <T as PartialEqSpec<U>>::obeys_eq_spec() ==> {
            let left_contents = left@;
            let right_contents = right@;
            result == (left_contents.len() == right_contents.len() && forall|i: int|
                #![auto]
                0 <= i < left_contents.len() ==> <T as PartialEqSpec<U>>::eq_spec(
                    &left_contents[i],
                    &right_contents[i],
                ))
        },
;

pub assume_specification<'spec0, T: PartialEq<U>, U, A: Allocator>[ <&'spec0 [T] as PartialEq<
    Vec<U, A>,
>>::ne ](left: &&'spec0 [T], right: &Vec<U, A>) -> (result: bool)
    ensures
        <T as PartialEqSpec<U>>::obeys_eq_spec() ==> {
            let left_contents = left@;
            let right_contents = right@;
            result == !(left_contents.len() == right_contents.len() && forall|i: int|
                #![auto]
                0 <= i < left_contents.len() ==> <T as PartialEqSpec<U>>::eq_spec(
                    &left_contents[i],
                    &right_contents[i],
                ))
        },
;

pub assume_specification<'spec0, T: PartialEq<U>, U, A: Allocator>[ <&'spec0 mut [T] as PartialEq<
    Vec<U, A>,
>>::eq ](left: &&'spec0 mut [T], right: &Vec<U, A>) -> (result: bool)
    ensures
        <T as PartialEqSpec<U>>::obeys_eq_spec() ==> {
            let left_contents = old(*left)@;
            let right_contents = right@;
            result == (left_contents.len() == right_contents.len() && forall|i: int|
                #![auto]
                0 <= i < left_contents.len() ==> <T as PartialEqSpec<U>>::eq_spec(
                    &left_contents[i],
                    &right_contents[i],
                ))
        },
;

pub assume_specification<'spec0, T: PartialEq<U>, U, A: Allocator>[ <&'spec0 mut [T] as PartialEq<
    Vec<U, A>,
>>::ne ](left: &&'spec0 mut [T], right: &Vec<U, A>) -> (result: bool)
    ensures
        <T as PartialEqSpec<U>>::obeys_eq_spec() ==> {
            let left_contents = old(*left)@;
            let right_contents = right@;
            result == !(left_contents.len() == right_contents.len() && forall|i: int|
                #![auto]
                0 <= i < left_contents.len() ==> <T as PartialEqSpec<U>>::eq_spec(
                    &left_contents[i],
                    &right_contents[i],
                ))
        },
;

pub assume_specification<T: PartialEq<U>, U, A: Allocator>[ <Vec<T, A> as PartialEq<[U]>>::eq ](
    left: &Vec<T, A>,
    right: &[U],
) -> (result: bool)
    ensures
        <T as PartialEqSpec<U>>::obeys_eq_spec() ==> {
            let left_contents = left@;
            let right_contents = right@;
            result == (left_contents.len() == right_contents.len() && forall|i: int|
                #![auto]
                0 <= i < left_contents.len() ==> <T as PartialEqSpec<U>>::eq_spec(
                    &left_contents[i],
                    &right_contents[i],
                ))
        },
;

pub assume_specification<T: PartialEq<U>, U, A: Allocator>[ <Vec<T, A> as PartialEq<[U]>>::ne ](
    left: &Vec<T, A>,
    right: &[U],
) -> (result: bool)
    ensures
        <T as PartialEqSpec<U>>::obeys_eq_spec() ==> {
            let left_contents = left@;
            let right_contents = right@;
            result == !(left_contents.len() == right_contents.len() && forall|i: int|
                #![auto]
                0 <= i < left_contents.len() ==> <T as PartialEqSpec<U>>::eq_spec(
                    &left_contents[i],
                    &right_contents[i],
                ))
        },
;

pub assume_specification<T: PartialEq<U>, U, A: Allocator>[ <[T] as PartialEq<Vec<U, A>>>::eq ](
    left: &[T],
    right: &Vec<U, A>,
) -> (result: bool)
    ensures
        <T as PartialEqSpec<U>>::obeys_eq_spec() ==> {
            let left_contents = left@;
            let right_contents = right@;
            result == (left_contents.len() == right_contents.len() && forall|i: int|
                #![auto]
                0 <= i < left_contents.len() ==> <T as PartialEqSpec<U>>::eq_spec(
                    &left_contents[i],
                    &right_contents[i],
                ))
        },
;

pub assume_specification<T: PartialEq<U>, U, A: Allocator>[ <[T] as PartialEq<Vec<U, A>>>::ne ](
    left: &[T],
    right: &Vec<U, A>,
) -> (result: bool)
    ensures
        <T as PartialEqSpec<U>>::obeys_eq_spec() ==> {
            let left_contents = left@;
            let right_contents = right@;
            result == !(left_contents.len() == right_contents.len() && forall|i: int|
                #![auto]
                0 <= i < left_contents.len() ==> <T as PartialEqSpec<U>>::eq_spec(
                    &left_contents[i],
                    &right_contents[i],
                ))
        },
;

pub assume_specification<'spec0, T: PartialEq<U> + Clone, U, A: Allocator>[ <Cow<
    'spec0,
    [T],
> as PartialEq<Vec<U, A>>>::eq ](left: &Cow<'spec0, [T]>, right: &Vec<U, A>) -> (result: bool)
    ensures
        <T as PartialEqSpec<U>>::obeys_eq_spec() ==> {
            let left_contents = match left {
                Cow::Borrowed(contents) => contents@,
                Cow::Owned(contents) => contents@,
            };
            let right_contents = right@;
            result == (left_contents.len() == right_contents.len() && forall|i: int|
                #![auto]
                0 <= i < left_contents.len() ==> <T as PartialEqSpec<U>>::eq_spec(
                    &left_contents[i],
                    &right_contents[i],
                ))
        },
;

pub assume_specification<'spec0, T: PartialEq<U> + Clone, U, A: Allocator>[ <Cow<
    'spec0,
    [T],
> as PartialEq<Vec<U, A>>>::ne ](left: &Cow<'spec0, [T]>, right: &Vec<U, A>) -> (result: bool)
    ensures
        <T as PartialEqSpec<U>>::obeys_eq_spec() ==> {
            let left_contents = match left {
                Cow::Borrowed(contents) => contents@,
                Cow::Owned(contents) => contents@,
            };
            let right_contents = right@;
            result == !(left_contents.len() == right_contents.len() && forall|i: int|
                #![auto]
                0 <= i < left_contents.len() ==> <T as PartialEqSpec<U>>::eq_spec(
                    &left_contents[i],
                    &right_contents[i],
                ))
        },
;

pub assume_specification<'spec0, 'spec1, T: PartialEq<U> + Clone, U>[ <Cow<
    'spec1,
    [T],
> as PartialEq<&[U]>>::eq ](left: &Cow<'spec1, [T]>, right: &&[U]) -> (result: bool)
    ensures
        <T as PartialEqSpec<U>>::obeys_eq_spec() ==> {
            let left_contents = match left {
                Cow::Borrowed(contents) => contents@,
                Cow::Owned(contents) => contents@,
            };
            let right_contents = right@;
            result == (left_contents.len() == right_contents.len() && forall|i: int|
                #![auto]
                0 <= i < left_contents.len() ==> <T as PartialEqSpec<U>>::eq_spec(
                    &left_contents[i],
                    &right_contents[i],
                ))
        },
;

pub assume_specification<'spec0, 'spec1, T: PartialEq<U> + Clone, U>[ <Cow<
    'spec1,
    [T],
> as PartialEq<&[U]>>::ne ](left: &Cow<'spec1, [T]>, right: &&[U]) -> (result: bool)
    ensures
        <T as PartialEqSpec<U>>::obeys_eq_spec() ==> {
            let left_contents = match left {
                Cow::Borrowed(contents) => contents@,
                Cow::Owned(contents) => contents@,
            };
            let right_contents = right@;
            result == !(left_contents.len() == right_contents.len() && forall|i: int|
                #![auto]
                0 <= i < left_contents.len() ==> <T as PartialEqSpec<U>>::eq_spec(
                    &left_contents[i],
                    &right_contents[i],
                ))
        },
;

pub assume_specification<'spec0, 'spec1, T: PartialEq<U> + Clone, U>[ <Cow<
    'spec1,
    [T],
> as PartialEq<&mut [U]>>::eq ](left: &Cow<'spec1, [T]>, right: &&mut [U]) -> (result: bool)
    ensures
        <T as PartialEqSpec<U>>::obeys_eq_spec() ==> {
            let left_contents = match left {
                Cow::Borrowed(contents) => contents@,
                Cow::Owned(contents) => contents@,
            };
            let right_contents = old(*right)@;
            result == (left_contents.len() == right_contents.len() && forall|i: int|
                #![auto]
                0 <= i < left_contents.len() ==> <T as PartialEqSpec<U>>::eq_spec(
                    &left_contents[i],
                    &right_contents[i],
                ))
        },
;

pub assume_specification<'spec0, 'spec1, T: PartialEq<U> + Clone, U>[ <Cow<
    'spec1,
    [T],
> as PartialEq<&mut [U]>>::ne ](left: &Cow<'spec1, [T]>, right: &&mut [U]) -> (result: bool)
    ensures
        <T as PartialEqSpec<U>>::obeys_eq_spec() ==> {
            let left_contents = match left {
                Cow::Borrowed(contents) => contents@,
                Cow::Owned(contents) => contents@,
            };
            let right_contents = old(*right)@;
            result == !(left_contents.len() == right_contents.len() && forall|i: int|
                #![auto]
                0 <= i < left_contents.len() ==> <T as PartialEqSpec<U>>::eq_spec(
                    &left_contents[i],
                    &right_contents[i],
                ))
        },
;

pub assume_specification<T: PartialEq<U>, U, A: Allocator, const N: usize>[ <Vec<T, A> as PartialEq<
    [U; N],
>>::eq ](left: &Vec<T, A>, right: &[U; N]) -> (result: bool)
    ensures
        <T as PartialEqSpec<U>>::obeys_eq_spec() ==> {
            let left_contents = left@;
            let right_contents = right@;
            result == (left_contents.len() == right_contents.len() && forall|i: int|
                #![auto]
                0 <= i < left_contents.len() ==> <T as PartialEqSpec<U>>::eq_spec(
                    &left_contents[i],
                    &right_contents[i],
                ))
        },
;

pub assume_specification<T: PartialEq<U>, U, A: Allocator, const N: usize>[ <Vec<T, A> as PartialEq<
    [U; N],
>>::ne ](left: &Vec<T, A>, right: &[U; N]) -> (result: bool)
    ensures
        <T as PartialEqSpec<U>>::obeys_eq_spec() ==> {
            let left_contents = left@;
            let right_contents = right@;
            result == !(left_contents.len() == right_contents.len() && forall|i: int|
                #![auto]
                0 <= i < left_contents.len() ==> <T as PartialEqSpec<U>>::eq_spec(
                    &left_contents[i],
                    &right_contents[i],
                ))
        },
;

pub assume_specification<'spec0, T: PartialEq<U>, U, A: Allocator, const N: usize>[ <Vec<
    T,
    A,
> as PartialEq<&[U; N]>>::eq ](left: &Vec<T, A>, right: &&[U; N]) -> (result: bool)
    ensures
        <T as PartialEqSpec<U>>::obeys_eq_spec() ==> {
            let left_contents = left@;
            let right_contents = right@;
            result == (left_contents.len() == right_contents.len() && forall|i: int|
                #![auto]
                0 <= i < left_contents.len() ==> <T as PartialEqSpec<U>>::eq_spec(
                    &left_contents[i],
                    &right_contents[i],
                ))
        },
;

pub assume_specification<'spec0, T: PartialEq<U>, U, A: Allocator, const N: usize>[ <Vec<
    T,
    A,
> as PartialEq<&[U; N]>>::ne ](left: &Vec<T, A>, right: &&[U; N]) -> (result: bool)
    ensures
        <T as PartialEqSpec<U>>::obeys_eq_spec() ==> {
            let left_contents = left@;
            let right_contents = right@;
            result == !(left_contents.len() == right_contents.len() && forall|i: int|
                #![auto]
                0 <= i < left_contents.len() ==> <T as PartialEqSpec<U>>::eq_spec(
                    &left_contents[i],
                    &right_contents[i],
                ))
        },
;

} // verus!
