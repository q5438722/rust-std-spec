#![feature(allocator_api)]
#![allow(dead_code)]
#![allow(unused_imports)]

extern crate alloc;

use alloc::vec::Vec;
use core::alloc::Allocator;
use core::clone::Clone;
use vstd::prelude::*;
use vstd::std_specs::vec::*;

verus! {

fn source_extend_with<T: Clone, A: Allocator>(
    vec: &mut Vec<T, A>,
    n: usize,
    value: T,
)
    ensures
        final(vec)@.len() == old(vec)@.len() + n,
        final(vec)@.subrange(0, old(vec)@.len() as int) == old(vec)@,
        forall|j: int| #![all_triggers]
            old(vec)@.len() <= j < old(vec)@.len() + n ==>
                cloned::<T>(value, final(vec)@[j]),
{
    let ghost original = vec@;
    vec.reserve(n);

    if n > 0 {
        let mut i: usize = 0;
        while i < n - 1
            invariant
                i <= n - 1,
                vec@.len() == original.len() + i,
                forall|j: int|
                    #![trigger vec@[j]]
                    0 <= j < original.len() ==> vec@[j] == original[j],
                forall|j: int|
                    #![trigger vec@[original.len() + j]]
                    0 <= j < i ==> cloned::<T>(value, vec@[original.len() + j]),
            decreases
                n - 1 - i,
        {
            let cloned_value = value.clone();
            assert(cloned::<T>(value, cloned_value));
            vec.push(cloned_value);
            i += 1;
        }

        assert(cloned::<T>(value, value));
        vec.push(value);
    }

    assert(vec@.subrange(0, original.len() as int) =~= original) by {
        assert forall|j: int| 0 <= j < original.len() implies
            vec@.subrange(0, original.len() as int)[j] == original[j] by {
            assert(vec@.subrange(0, original.len() as int)[j] == vec@[j]);
        }
    }

    assert forall|j: int| #![all_triggers]
        original.len() <= j < original.len() + n implies
            cloned::<T>(value, vec@[j]) by {
        let offset = j - original.len();
        if offset < n - 1 {
            assert(original.len() + offset == j);
        } else {
            assert(offset == n - 1);
            assert(j == vec@.len() - 1);
        }
    }
}

fn source_vec_resize<T: Clone, A: Allocator>(
    vec: &mut Vec<T, A>,
    new_len: usize,
    value: T,
)
    ensures
        new_len <= old(vec).len() ==>
            final(vec)@ == old(vec)@.subrange(0, new_len as int),
        new_len > old(vec).len() ==> {
            &&& final(vec)@.len() == new_len
            &&& final(vec)@.subrange(0, old(vec).len() as int) == old(vec)@
            &&& forall|i| #![all_triggers]
                old(vec).len() <= i < new_len ==>
                    cloned::<T>(value, final(vec)@[i])
        },
{
    let len = vec.len();

    if new_len > len {
        source_extend_with(vec, new_len - len, value)
    } else {
        vec.truncate(new_len);
    }
}

} // verus!

fn main() {}