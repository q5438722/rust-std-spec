#![cfg(not(no_global_oom_handling))]

use std::alloc::Global;
use vstd::prelude::*;

verus! {

pub const fn with_capacity<T>(capacity: usize) -> (v: Vec<T>)
    ensures
        v@ == Seq::<T>::empty(),
{
    Vec::<T>::with_capacity_in(capacity, Global)
}

}
