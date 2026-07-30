#![feature(allocator_api)]
#![allow(dead_code)]

extern crate alloc;

use alloc::collections::VecDeque;
use core::alloc::Allocator;
use vstd::prelude::*;
use vstd::std_specs::vecdeque::*;

verus! {

fn source_vecdeque_truncate<T, A: Allocator>(v: &mut VecDeque<T, A>, len: usize)
    ensures
        len <= old(v).len() ==> final(v)@ == old(v)@.subrange(0, len as int),
        len > old(v).len() ==> final(v)@ == old(v)@,
{
    proof {
        axiom_spec_len(v);
    }
    if len >= v.len() {
        return;
    }

    let ghost original = v@;
    // `as_slices` exposes the same ring split needed by the source branch
    // without retaining the mutable slices across the elementwise desugaring.
    let front_len = v.as_slices().0.len();
    let remaining_len = v.len() - len;
    let mut dropped: usize = 0;

    if len > front_len {
        let _begin = len - front_len;
        // Elementwise desugaring of dropping `back[begin..]`.
        while dropped < remaining_len
            invariant
                len < original.len(),
                remaining_len == original.len() - len,
                dropped <= remaining_len,
                v@ == original.subrange(0, len as int)
                    + original.subrange((len + dropped) as int, original.len() as int),
            decreases
                remaining_len - dropped,
        {
            let _ = v.remove(len);
            dropped += 1;
        }
    } else {
        // On normal return, removing repeatedly at `len` expands the source-order
        // drops of `front[len..]`, followed by the `Dropper`-guarded `back`.
        while dropped < remaining_len
            invariant
                len < original.len(),
                remaining_len == original.len() - len,
                dropped <= remaining_len,
                v@ == original.subrange(0, len as int)
                    + original.subrange((len + dropped) as int, original.len() as int),
            decreases
                remaining_len - dropped,
        {
            let _ = v.remove(len);
            dropped += 1;
        }
    }

    assert(len + dropped == original.len());
    assert(original.subrange(original.len() as int, original.len() as int)
        == Seq::<T>::empty());
    assert(v@ == original.subrange(0, len as int));
}

} // verus!

fn main() {}