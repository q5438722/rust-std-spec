use std::alloc::Allocator;
use vstd::prelude::*;

verus! {

pub fn default<T>() -> (v: Vec<T>)
    ensures
        v@ == Seq::<T>::empty(),
{
    Vec::new()
}

pub const fn is_empty<T, A: Allocator>(v: &Vec<T, A>) -> (res: bool)
    ensures
        res <==> v@.len() == 0,
{
    v.len() == 0
}

pub fn deref<T, A: Allocator>(vec: &Vec<T, A>) -> (slice: &[T])
    ensures
        slice@ == vec@,
{
    vec.as_slice()
}

}
