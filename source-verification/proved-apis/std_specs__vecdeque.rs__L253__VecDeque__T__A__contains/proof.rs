#![feature(allocator_api)]
#![allow(dead_code)]
#![allow(unused_imports)]

extern crate alloc;

use alloc::collections::VecDeque;
use core::alloc::Allocator;
use core::cmp::PartialEq;
use vstd::prelude::*;
use vstd::std_specs::cmp::{PartialEqSpec, PartialEqSpecImpl};
use vstd::std_specs::vecdeque::*;

verus! {

proof fn lemma_concat_has_eq<T: PartialEq<T>>(
    left: Seq<T>,
    right: Seq<T>,
    value: &T,
)
    ensures
        (exists|i: int|
            0 <= i < (left + right).len()
                && #[trigger] (left + right)[i].eq_spec(value))
        <==> (exists|i: int|
            0 <= i < left.len() && #[trigger] left[i].eq_spec(value))
        || (exists|i: int|
            0 <= i < right.len() && #[trigger] right[i].eq_spec(value)),
{
    if exists|i: int|
        0 <= i < (left + right).len()
            && #[trigger] (left + right)[i].eq_spec(value)
    {
        let i = choose|i: int|
            0 <= i < (left + right).len()
                && #[trigger] (left + right)[i].eq_spec(value);
        if i < left.len() {
            assert((left + right)[i] == left[i]);
            assert(exists|j: int|
                0 <= j < left.len() && #[trigger] left[j].eq_spec(value));
        } else {
            let j = i - left.len();
            assert(0 <= j < right.len());
            assert((left + right)[i] == right[j]);
            assert(exists|k: int|
                0 <= k < right.len() && #[trigger] right[k].eq_spec(value));
        }
    }

    if exists|i: int|
        0 <= i < left.len() && #[trigger] left[i].eq_spec(value)
    {
        let i = choose|i: int|
            0 <= i < left.len() && #[trigger] left[i].eq_spec(value);
        assert((left + right)[i] == left[i]);
        assert(exists|j: int|
            0 <= j < (left + right).len()
                && #[trigger] (left + right)[j].eq_spec(value));
    }

    if exists|i: int|
        0 <= i < right.len() && #[trigger] right[i].eq_spec(value)
    {
        let i = choose|i: int|
            0 <= i < right.len() && #[trigger] right[i].eq_spec(value);
        let j = left.len() + i;
        assert(0 <= j < (left + right).len());
        assert((left + right)[j] == right[i]);
        assert(exists|k: int|
            0 <= k < (left + right).len()
                && #[trigger] (left + right)[k].eq_spec(value));
    }
}

fn source_slice_contains<T: PartialEq<T>>(
    slice: &[T],
    value: &T,
) -> (result: bool)
    requires
        T::obeys_eq_spec(),
    ensures
        result <==> exists|i: int|
            0 <= i < slice@.len() && #[trigger] slice@[i].eq_spec(value),
{
    // Desugars the generic SliceContains implementation's iter().any loop.
    let len = slice.len();
    let mut index = 0usize;
    while index < len
        invariant
            T::obeys_eq_spec(),
            len == slice@.len(),
            index <= len,
            forall|i: int|
                0 <= i < index ==> !#[trigger] slice@[i].eq_spec(value),
        decreases len - index,
    {
        let equal = PartialEq::eq(&slice[index], value);
        if equal {
            assert(slice@[index as int].eq_spec(value));
            assert(exists|i: int|
                0 <= i < slice@.len() && #[trigger] slice@[i].eq_spec(value));
            return true;
        }
        assert(!slice@[index as int].eq_spec(value));
        index += 1;
    }
    false
}

fn source_vecdeque_contains<T: PartialEq<T>, A: Allocator>(
    v: &VecDeque<T, A>,
    value: &T,
) -> (result: bool)
    requires
        T::obeys_eq_spec(),
    ensures
        result <==> exists|i: int|
            0 <= i < v@.len() && #[trigger] v@[i].eq_spec(value),
{
    let (a, b) = v.as_slices();
    let result = source_slice_contains(a, value) || source_slice_contains(b, value);
    proof {
        lemma_concat_has_eq(a@, b@, value);
    }
    result
}

} // verus!

fn main() {}