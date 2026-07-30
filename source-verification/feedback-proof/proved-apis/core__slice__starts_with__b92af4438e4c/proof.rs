#![allow(dead_code)]

use vstd::prelude::*;
use vstd::std_specs::cmp::PartialEqSpec;

verus! {

pub assume_specification<T, U>[ <[T] as core::cmp::PartialEq<[U]>>::eq ](
    left: &[T],
    right: &[U],
) -> (result: bool)
where
    T: core::cmp::PartialEq<U>,
    ensures
        T::obeys_eq_spec() ==> (
            result == (
                left@.len() == right@.len()
                && (forall|i: int| 0 <= i < left@.len() ==>
                    left@[i].eq_spec(&right@[i]))
            )
        ),
;

pub fn source_core_slice_starts_with<T>(
    slice: &[T],
    needle: &[T],
) -> (result: bool)
where
    T: core::cmp::PartialEq,
    requires
        T::obeys_eq_spec(),
    ensures
        result == (
            slice@.len() >= needle@.len()
            && (forall|i: int| i >= 0 && needle@.len() > i ==>
                needle@[i].eq_spec(&slice@[i]))
        ),
{
    let n = needle.len();
    // Inline the reference PartialEq forwarding impl selected by `==`.
    slice.len() >= n
        && <[T] as core::cmp::PartialEq<[T]>>::eq(needle, &slice[0..n])
}

} // verus!

fn main() {}