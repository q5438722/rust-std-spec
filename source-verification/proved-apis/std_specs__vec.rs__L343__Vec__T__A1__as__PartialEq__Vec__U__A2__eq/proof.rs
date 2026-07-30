#![feature(allocator_api)]
#![allow(dead_code)]
#![allow(unused_imports)]

extern crate alloc;

use alloc::vec::Vec;
use core::alloc::Allocator;
use core::cmp::PartialEq;
use vstd::prelude::*;
use vstd::std_specs::cmp::*;
use vstd::std_specs::vec::*;

verus! {

fn source_slice_eq<T: PartialEq<U>, U>(
    lhs: &[T],
    rhs: &[U],
) -> (res: bool)
    ensures
        T::obeys_eq_spec() ==>
            (res <==> lhs@.len() == rhs@.len()
                && forall|i: int| #![auto]
                    0 <= i < lhs@.len() ==> lhs@[i].eq_spec(&rhs@[i])),
{
    // Desugars slice equality and its generic SlicePartialEq loop.
    let len = lhs.len();
    if len == rhs.len() {
        let mut idx = 0usize;
        while idx < len
            invariant
                len == lhs@.len(),
                len == rhs@.len(),
                idx <= len,
                T::obeys_eq_spec() ==>
                    forall|i: int| #![auto]
                        0 <= i < idx ==> lhs@[i].eq_spec(&rhs@[i]),
            decreases len - idx,
        {
            let equal = PartialEq::eq(&lhs[idx], &rhs[idx]);
            if !equal {
                assert(T::obeys_eq_spec() ==>
                    !lhs@[idx as int].eq_spec(&rhs@[idx as int]));
                return false;
            }
            idx += 1;
        }
        true
    } else {
        false
    }
}

fn source_vec_eq<T: PartialEq<U>, U, A1: Allocator, A2: Allocator>(
    x: &Vec<T, A1>,
    y: &Vec<U, A2>,
) -> (res: bool)
    ensures
        <Vec<T, A1> as PartialEqSpec<Vec<U, A2>>>::obeys_eq_spec() ==>
            res == <Vec<T, A1> as PartialEqSpec<Vec<U, A2>>>::eq_spec(x, y),
{
    source_slice_eq(x.as_slice(), y.as_slice())
}

}

fn main() {}