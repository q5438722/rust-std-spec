#![feature(allocator_api)]
#![allow(dead_code)]
#![allow(unused_imports)]

extern crate alloc;

use alloc::collections::VecDeque;
use core::alloc::Allocator;
use core::clone::Clone;
use vstd::prelude::*;
use vstd::std_specs::vecdeque::*;

verus! {

fn source_extend_repeat_n<T: Clone, A: Allocator>(
    v: &mut VecDeque<T, A>,
    n: usize,
    value: T,
)
    ensures
        final(v)@.len() == old(v)@.len() + n,
        final(v)@.subrange(0, old(v)@.len() as int) == old(v)@,
        forall|j: int| #![all_triggers]
            old(v)@.len() <= j < old(v)@.len() + n ==>
                cloned::<T>(value, final(v)@[j]),
{
    let ghost original = v@;
    v.reserve(n);

    if n > 0 {
        let mut i: usize = 0;
        while i < n - 1
            invariant
                i <= n - 1,
                v@.len() == original.len() + i,
                forall|j: int|
                    #![trigger v@[j]]
                    0 <= j < original.len() ==> v@[j] == original[j],
                forall|j: int|
                    #![trigger v@[original.len() + j]]
                    0 <= j < i ==> cloned::<T>(value, v@[original.len() + j]),
            decreases
                n - 1 - i,
        {
            let cloned_value = value.clone();
            assert(cloned::<T>(value, cloned_value));
            v.push_back(cloned_value);
            i += 1;
        }

        assert(cloned::<T>(value, value));
        v.push_back(value);
    }

    assert(v@.subrange(0, original.len() as int) =~= original) by {
        assert forall|j: int| 0 <= j < original.len() implies
            v@.subrange(0, original.len() as int)[j] == original[j] by {
            assert(v@.subrange(0, original.len() as int)[j] == v@[j]);
        }
    }

    assert forall|j: int| #![all_triggers]
        original.len() <= j < original.len() + n implies
            cloned::<T>(value, v@[j]) by {
        let offset = j - original.len();
        if offset < n - 1 {
            assert(original.len() + offset == j);
        } else {
            assert(offset == n - 1);
            assert(j == v@.len() - 1);
        }
    }
}

fn source_vecdeque_resize<T: Clone, A: Allocator>(
    v: &mut VecDeque<T, A>,
    new_len: usize,
    value: T,
)
    ensures
        new_len <= old(v).len() ==>
            final(v)@ == old(v)@.subrange(0, new_len as int),
        new_len > old(v).len() ==> {
            &&& final(v)@.len() == new_len
            &&& final(v)@.subrange(0, old(v).len() as int) == old(v)@
            &&& forall|i| #![all_triggers]
                old(v).len() <= i < new_len ==>
                    cloned::<T>(value, final(v)@[i])
        },
{
    if new_len > v.len() {
        let extra = new_len - v.len();
        source_extend_repeat_n(v, extra, value)
    } else {
        v.truncate(new_len);
    }
}

} // verus!

fn main() {}