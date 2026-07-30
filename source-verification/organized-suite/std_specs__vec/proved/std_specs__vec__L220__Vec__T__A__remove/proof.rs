#![feature(allocator_api)]
#![feature(vec_try_remove)]
#![allow(dead_code)]

extern crate alloc;

use alloc::vec::Vec;
use core::alloc::Allocator;
use vstd::prelude::*;
use vstd::std_specs::vec::*;

verus! {

pub assume_specification<T, A: Allocator>[ Vec::<T, A>::try_remove ](
    vec: &mut Vec<T, A>,
    index: usize,
) -> (result: Option<T>)
    ensures
        index < old(vec)@.len() ==> result == Some(old(vec)@[index as int])
            && final(vec)@ == old(vec)@.remove(index as int),
        index >= old(vec)@.len() ==> result == None::<T> && final(vec)@ == old(vec)@,
;

#[cold]
#[track_caller]
fn assert_failed(index: usize, len: usize) -> !
    requires
        false,
{
    vstd::vpanic!(
        "removal index (is {}) should be < len (is {})",
        index,
        len
    );
}

fn vec_remove_proof<T, A: Allocator>(
    vec: &mut Vec<T, A>,
    index: usize,
) -> (element: T)
    requires
        index < old(vec).len(),
    ensures
        element == old(vec)[index as int],
        final(vec)@ == old(vec)@.remove(index as int),
{
    match vec.try_remove(index) {
        Some(elem) => elem,
        None => assert_failed(index, vec.len()),
    }
}

} // verus!

fn main() {}