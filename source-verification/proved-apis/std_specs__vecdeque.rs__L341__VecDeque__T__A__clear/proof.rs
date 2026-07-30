#![feature(allocator_api)]
#![allow(dead_code)]

extern crate alloc;

use alloc::collections::VecDeque;
use core::alloc::Allocator;
use vstd::prelude::*;
use vstd::std_specs::vecdeque::*;

verus! {

fn source_vecdeque_clear<T, A: Allocator>(v: &mut VecDeque<T, A>)
    ensures
        final(v).view() == Seq::<T>::empty(),
{
    v.truncate(0);
    proof {
        assert(v@ == Seq::<T>::empty());
    }
    // The source's subsequent `head = 0` only canonicalizes the private
    // representation of an already-empty deque, so it is erased in this view-level desugaring.
}

} // verus!

fn main() {}