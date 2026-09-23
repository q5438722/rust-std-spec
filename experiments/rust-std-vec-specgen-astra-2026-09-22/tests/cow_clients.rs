#![feature(allocator_api)]

// These are observer/assumed-contract clients, not source correctness proofs.
#[path = "../specs/lib.rs"]
mod aggregate;

use aggregate::cow::observation::{CowContents, CowObservation};
use std::borrow::Cow;
use vstd::prelude::*;

verus! {

pub proof fn observer_is_source_bound<'a, T: Clone>(value: Cow<'a, [T]>)
    ensures
        CowObservation::view(&value) == match value {
            Cow::Borrowed(s) => CowContents::Borrowed(s@),
            Cow::Owned(v) => CowContents::Owned(v@),
        },
{
}

pub proof fn equal_observations_preserve_variant_and_contents<'a, T: Clone>(
    left: Cow<'a, [T]>,
    right: Cow<'a, [T]>,
)
    ensures
        (CowObservation::view(&left) == CowObservation::view(&right)) ==> match (left, right) {
            (Cow::Borrowed(s), Cow::Borrowed(t)) => s@ == t@,
            (Cow::Owned(v), Cow::Owned(w)) => v@ == w@,
            _ => false,
        },
{
}

pub proof fn variant_and_order_are_observable()
    ensures
        CowContents::Borrowed(seq![9u8, 1u8]) != CowContents::Owned(seq![9u8, 1u8]),
        CowContents::Borrowed(seq![9u8, 1u8]) != CowContents::Borrowed(seq![1u8, 9u8]),
        CowContents::Owned(seq![9u8, 1u8]) != CowContents::Owned(seq![1u8, 9u8]),
{
    assert(seq![9u8, 1u8][0] != seq![1u8, 9u8][0]);
}

pub fn slice_contract<'a, T: Clone>(s: &'a [T]) -> (result: Cow<'a, [T]>)
    ensures CowObservation::view(&result) == CowContents::Borrowed(s@),
{
    <Cow<'a, [T]> as From<&'a [T]>>::from(s)
}

pub fn array_contract<'a, T: Clone, const N: usize>(s: &'a [T; N])
    -> (result: Cow<'a, [T]>)
    ensures CowObservation::view(&result) == CowContents::Borrowed(s@),
{
    <Cow<'a, [T]> as From<&'a [T; N]>>::from(s)
}

pub fn vec_contract<'a, T: Clone>(v: Vec<T>) -> (result: Cow<'a, [T]>)
    ensures CowObservation::view(&result) == CowContents::Owned(v@),
{
    <Cow<'a, [T]> as From<Vec<T>>>::from(v)
}

pub fn vec_ref_contract<'a, T: Clone>(v: &'a Vec<T>) -> (result: Cow<'a, [T]>)
    ensures CowObservation::view(&result) == CowContents::Borrowed(v@),
{
    <Cow<'a, [T]> as From<&'a Vec<T>>>::from(v)
}

}
