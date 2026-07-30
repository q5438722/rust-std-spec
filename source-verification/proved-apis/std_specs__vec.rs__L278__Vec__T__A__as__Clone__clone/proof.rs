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

pub assume_specification<T, A: Allocator>[
    Vec::<T, A>::allocator
](
    vec: &Vec<T, A>,
) -> (result: &A);

fn source_slice_to_vec_in<T: Clone, A: Allocator>(
    slice: &[T],
    alloc: A,
) -> (result: Vec<T, A>)
    ensures
        result@.len() == slice@.len(),
        forall|i: int| #![all_triggers]
            0 <= i < slice@.len() ==> cloned::<T>(slice@[i], result@[i]),
        slice@ =~= result@ ==> slice@ == result@,
{
    // `to_vec_in` writes this same clone sequence into spare capacity, then exposes its length.
    // `push` is the representation-free desugaring of those writes.
    let mut result = Vec::with_capacity_in(slice.len(), alloc);
    let mut i: usize = 0;
    while i < slice.len()
        invariant
            i <= slice@.len(),
            result@.len() == i,
            forall|j: int| #![all_triggers]
                0 <= j < i ==> cloned::<T>(slice@[j], result@[j]),
        decreases slice@.len() - i,
    {
        let value = slice[i].clone();
        assert(cloned::<T>(slice@[i as int], value));
        result.push(value);
        i += 1;
    }
    assert(slice@ =~= result@ ==> slice@ == result@);
    result
}

fn source_vec_clone<T: Clone, A: Allocator + Clone>(
    vec: &Vec<T, A>,
) -> (res: Vec<T, A>)
    ensures
        res.len() == vec.len(),
        forall|i| #![all_triggers] 0 <= i < vec.len() ==> cloned::<T>(vec[i], res[i]),
        vec_clone_trigger(*vec, res),
        vec@ =~= res@ ==> vec@ == res@,
{
    let alloc = vec.allocator().clone();
    let slice: &[T] = &**vec;
    let res = source_slice_to_vec_in(slice, alloc);
    assert(vec_clone_trigger(*vec, res));
    res
}

} // verus!

fn main() {}