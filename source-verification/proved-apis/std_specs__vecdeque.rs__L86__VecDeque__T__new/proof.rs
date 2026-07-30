#![allow(dead_code)]
#![allow(unused_imports)]

extern crate alloc;

use alloc::collections::VecDeque;
use vstd::prelude::*;
use vstd::std_specs::vecdeque::*;

verus! {

fn source_vecdeque_new<T>() -> (v: VecDeque<T>)
    ensures
        v@ == Seq::<T>::empty(),
{
    // At capacity zero, RawVec::with_capacity_in takes its zero-layout branch
    // and constructs RawVecInner::new_in(Global), matching RawVec::new().
    let v = VecDeque::<T>::with_capacity(0);
    assert(v@ == Seq::<T>::empty());
    v
}

} // verus!

fn main() {}