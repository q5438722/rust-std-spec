#![cfg(not(no_global_oom_handling))]

use std::borrow::Cow;
use vstd::prelude::*;
use super::observation::{CowContents, CowObservation};

verus! {

pub assume_specification<'a, T: Clone>[
    <Cow<'a, [T]> as From<&'a [T]>>::from
](s: &'a [T]) -> (result: Cow<'a, [T]>)
    where Cow<'a, [T]>: CowObservation<T>,
    ensures
        CowObservation::view(&result) == CowContents::Borrowed(s@),
;

pub assume_specification<'a, T: Clone, const N: usize>[
    <Cow<'a, [T]> as From<&'a [T; N]>>::from
](s: &'a [T; N]) -> (result: Cow<'a, [T]>)
    where Cow<'a, [T]>: CowObservation<T>,
    ensures
        CowObservation::view(&result) == CowContents::Borrowed(s@),
;

pub assume_specification<'a, T: Clone>[
    <Cow<'a, [T]> as From<Vec<T>>>::from
](v: Vec<T>) -> (result: Cow<'a, [T]>)
    where Cow<'a, [T]>: CowObservation<T>,
    ensures
        CowObservation::view(&result) == CowContents::Owned(v@),
;

pub assume_specification<'a, T: Clone>[
    <Cow<'a, [T]> as From<&'a Vec<T>>>::from
](v: &'a Vec<T>) -> (result: Cow<'a, [T]>)
    where Cow<'a, [T]>: CowObservation<T>,
    ensures
        CowObservation::view(&result) == CowContents::Borrowed(v@),
;

}
