#![feature(allocator_api)]
#![allow(dead_code)]

extern crate alloc;

use alloc::vec::Vec;
use core::alloc::Allocator;
use core::clone::Clone;
use vstd::prelude::*;
use vstd::std_specs::vec::*;

verus! {

fn source_vec_extend_from_slice<T: Clone, A: Allocator>(
    vec: &mut Vec<T, A>,
    other: &[T],
)
    ensures
        final(vec)@.len() == old(vec)@.len() + other@.len(),
        forall|i: int|
            #![trigger final(vec)@[i]]
            0 <= i < final(vec)@.len() ==> if i < old(vec)@.len() {
                final(vec)@[i] == old(vec)@[i]
            } else {
                cloned::<T>(other@[i - old(vec)@.len()], final(vec)@[i])
            },
{
    let ghost original = vec@;
    let mut index: usize = 0;

    // `spec_extend(other.iter())` specializes to cloning the slice in order
    // and appending each result; this exposes that private helper's loop.
    while index < other.len()
        invariant
            index <= other@.len(),
            vec@.len() == original.len() + index,
            forall|i: int|
                #![trigger vec@[i]]
                0 <= i < original.len() ==> vec@[i] == original[i],
            forall|i: int|
                #![trigger vec@[original.len() + i]]
                0 <= i < index ==>
                    cloned::<T>(other@[i], vec@[original.len() + i]),
        decreases
            other@.len() - index,
    {
        let value = other[index].clone();
        assert(cloned::<T>(other@[index as int], value));
        vec.push(value);
        index += 1;
    }

    assert forall|i: int|
        #![trigger vec@[i]]
        0 <= i < vec@.len() implies if i < original.len() {
            vec@[i] == original[i]
        } else {
            cloned::<T>(other@[i - original.len()], vec@[i])
        } by {
        if i >= original.len() {
            assert(0 <= i - original.len() < index);
            assert(original.len() + (i - original.len()) == i);
        }
    }
}

} // verus!

fn main() {}